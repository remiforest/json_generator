Create a json file based on a desired schema with randomly generated values.
Some values can be pulled from an external file if you want to reuse values or create joined files.

<hr>
<h3>Usage</h3>
python generator.py number_of_record file_name [--schema schea_file.json --format json/csv]


Schema definition:
Schema is defined in a json file (default: schema.json).
It has to be a json object.
field names will stay in the final documents.
values will be generated based on the schema value.

values are either :
- a string for a standard value type (ie. last_name, email, country, ...)
- a dictionary for advanced values (custom format) 
<hr>
<h3>Examples</h3> 

{"first":"first_name","last":"last_name","email":"email"}
{"name":"last_name","cust_id":{"format":"cccc-nnnnnnnn","unique":true}}


<hr>
<h3>Standard value types</h3>
last_name
first_name
email
card_vendor
card_number
country

<h3>Generated value types</h3>
n : number 0-9<p>
c : lower case a-z<p>
C : upper case A-Z<p>



