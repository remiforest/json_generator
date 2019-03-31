#! /usr/bin/python

import time
import binascii
import string
import random
import os
import json
import sys

from argparse import ArgumentParser

parser = ArgumentParser(description='Generate random data in a json file. One record per line')

last_names = json.load(open("last_name.json"))

def last_name():
    return random.choice(last_names)["last"]


def oid():
    timestamp = '{0:x}'.format(int(time.time()))
    rest = binascii.b2a_hex(os.urandom(8)).decode('ascii')
    return timestamp + rest


def custom_string(model_string):
    output_string = ""
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


def join(source_file,field):
    f = open(source_file,"r")
    json_object = json.loads(f.read())
    yield json_object[field]



def generate_field(field_format):
    if isinstance(field_format, basestring):
        if field_format == "OID":
            return oid()
        if field_format == "LAST":
            return last_name()
        else:
            return custom_string(field_format)
    if isinstance(field_format,dict):
        if "FILE" in field_format:
            file_name,field_name = field_format["FILE"].split(":")
            join_file = open(file_name,"r")
            json_object = json.loads(f.read())
            return json_object[field_name]


def main():
    schema = json.load(open("schema.json"))

    # check if FILE in schema
    ext_file = False
    ext_field = False
    for k,v in schema.items():
        if isinstance(v,dict):
            if "FILE" in v:
                ext_file,ext_field = v["FILE"].split(":")


    number_of_records = int(sys.argv[1])
    target_file = open(sys.argv[2],"w")

    # get the list of all values for the given field
    ext_vals = None
    if ext_file:
        ext_vals = []
        a = json.load(open(ext_file))
        for o in a:
            ext_vals.append(o[ext_field])

    new_dataset = []
    for i in range(number_of_records):
        new_doc = {}
        for field_name,field_format in schema.items():
            if ext_vals and field_name == ext_field:
                new_doc[field_name] = ext_vals[i%len(ext_vals)]
            else:
                new_doc[field_name] = generate_field(field_format)
        new_dataset.append(new_doc)

    target_file.write(json.dumps(new_dataset))
    target_file.close()


if __name__ == '__main__':
    main()

