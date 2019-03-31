Create a json file based on a desired schema with randomly generated values.
Some values can be pulled from an external file if you want to reuse values or create joined files.

<hr>
<h3>Usage</h3>
python generator.py number_of_record file_name


Schema definition:
Schema is defined in the schema.json file.
It has to be a json object.
field names will stay in the final documents.
values will be generated based on the schema value.

<hr>
<h3>Examples</h3> 

{"_id":"OID","name":"LAST","card":"nnnn-nnnn-nnnn-nnnn"}

{"name":{"FILE":"customers.json:last_name"},"new_id":"OID","product_id":"nncc-CCCC"}


<hr>
<h3>Value types</h3>
OID : mongodb type UID
n : number 0-9
c : lower case a-z
C : upper case A-Z
LAST : last name (english)
FIRST : first name (english)

{"FILE":"file_name:field_name"} : references a filed in an external file.

