#! /usr/bin/python

"""
Generate a JSON or CSV file of records based on a given schema

"""



import time
import binascii
import string
import random
import os
import json
import csv
import sys

from bloom import Bloom


from argparse import ArgumentParser

parser = ArgumentParser(description='Generate random data in a json file. One record per line')
parser.add_argument("number")
parser.add_argument("outfile")
parser.add_argument(
    '--schema',
    default="schema.json",
    help='schema definition, default : schema.json'
)

parser.add_argument(
    '--format',
    default="json",
    help='output format, default : json'
)


args = parser.parse_args()
number_of_records = args.number

bloom_filter = Bloom(number_of_records,0.0001,5) # n , fp , k


def create_folder_if_doesnt_exist(dirName):
    try:
        # Create target Directory
        os.mkdir(dirName)
    except :
        pass


out_folder = "output/"
create_folder_if_doesnt_exist(out_folder)

source_folder = "source/"
create_folder_if_doesnt_exist(source_folder)


#### Pre defined value types

source_data = {}

def load_source_data(source_name):
    global source_data
    source_data[source_name] = [record[source_name] for record in json.load(open(source_folder + source_name + ".json"))]

for source_name in ["first_name","last_name"]: # ,"email","country","card_number","card_vendor"]:
    load_source_data(source_name)


def get_value(value_type):
    global source_data
    return random.choice(source_data[value_type])


#### Generated value types

def custom_string(model_string):
    """ randomly generates a custom string based on a given model """
    output_string = ''
    for c in model_string:
        if c == "n":
            output_string += str(random.randint(0,9))
        if c == "-":
            output_string += "-"
        if c == "c":
            output_string += random.choice(string.ascii_lowercase)
        if c == "C":
            output_string += random.choice(string.ascii_uppercase)

    return output_string



#### JOIN management - used for having same values used in different files

# def join(source_file,field):
#     f = open(source_file,"r")
#     json_object = json.loads(f.read())
#     yield json_object[field]


#### Field values generator 

# Used to check value unicity
given_values = {}
MAX_RETRY = 1000 # max number of retry to generate an unique value

def generate_field(field_name, field_format):
    """ generate a value based on the schema definition """
    global bloom_filter
    global given_values

    # Check if the field definition is a base type or a dictionary
    if isinstance(field_format, basestring):
        if field_format in source_data:
            new_value = get_value(field_format)
    if isinstance(field_format,dict):
        if "custom" in field_format:
            if "unique" in field_format:
                unique = field_format["unique"]
                if not field_name in given_values:
                    given_values[field_name] = []
            else:
                unique = False
            number_of_try = 0
            while True:
                number_of_try += 1
                new_value = custom_string(field_format["custom"])
                if unique:
                    # we test if the value has already been given
                    already_given = bloom_filter.query(new_value)
                    bloom_filter.add(new_value)
                    if already_given:
                        # if may exist, so we test the value
                        if not new_value in given_values[field_name]:
                            given_values[field_name].append(new_value)
                            break
                    else:
                        given_values[field_name].append(new_value)
                        break
                else:
                    break
                if number_of_try > MAX_RETRY:
                    print("Failed to generate unique value after {} retries".format(MAX_RETRY))
                    break

    return new_value



def main(number_of_records,outfile,schema,file_format):

    print("Generating {} records with schema {} in file {}.{}".format(number_of_records,schema,outfile,file_format))

    new_dataset = []
    for i in range(number_of_records):
        new_doc = {}
        for field_name,field_format in schema.items():
            new_doc[field_name] = generate_field(field_name,field_format)
        new_dataset.append(new_doc)

    with open("{}.{}".format(out_folder + outfile,file_format),'w') as target_file:
        if file_format == "json":
            target_file.write(json.dumps(new_dataset))
        elif file_format == "csv":
            writer = csv.DictWriter(target_file, new_dataset[0].keys())
            writer.writeheader()
            writer.writerows(new_dataset)
    

if __name__ == '__main__':
    args = parser.parse_args()
    number_of_records = int(args.number)
    target_file = args.outfile
    schema = json.load(open(args.schema))
    file_format = args.format
    start_time = time.time()
    main(number_of_records,target_file,schema,file_format)
    end_time = time.time()

    print("Generated {} documents in {} seconds".format(number_of_records,int(end_time - start_time)))


