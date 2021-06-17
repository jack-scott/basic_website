# Parser

Running `error_parser.py` will process all the errors in `python_errors.json` 

## To run

Run `python3 error_parser.py` in the docker container. Will print the parsed output and tokens

Example of input:
```
Here is some data that is approximately the length
of the data that I am sending in my real server. It is a string that
doesn't contain any unordinary characters except for maybe a tab.
Traceback (most recent call last):
    File "client.py", line 49, in <moduel>
        main()
    File "client.py", line 46, in main
        getData()
    File "client.py", line 11, in getData
        data = sendDataRequest()
    File "client.py", line 37, in sendDataRequest
        print data
UnboundLocalError: local variable 'data' referenced before assignment
```

Example of output:

```
****** Got tokens ******
TRACEBACK
	str: Traceback (most recent call last):
GENERIC_FILE
	file path: "client.py"
	line num: 49
	function: <moduel>
	line: main()
GENERIC_FILE
	file path: "client.py"
	line num: 46
	function: main
	line: getData()
GENERIC_FILE
	file path: "client.py"
	line num: 11
	function: getData
	line: data = sendDataRequest()
GENERIC_FILE
	file path: "client.py"
	line num: 37
	function: sendDataRequest
	line: print data
ERROR
	type: UnboundLocalError
	str: UnboundLocalError: local variable 'data' referenced before assignment
************************
DEBUG - Finishing up scanner. Lines left 0
DEBUG - Finishing up parser. Number of unparsed lines 3
----------------------------------------------------->>
Here is some data that is approximately the length
of the data that I am sending in my real server. It is a string that
doesn't contain any unordinary characters except for maybe a tab.
<<-----------------------------------------------------
Traceback (most recent call last):
    File "client.py", line 49, in <moduel>
        main()
    File "client.py", line 46, in main
        getData()
    File "client.py", line 11, in getData
        data = sendDataRequest()
    File "client.py", line 37, in sendDataRequest
        print data
UnboundLocalError: local variable 'data' referenced before assignment

```

## Next steps 

* Test new errors and pass back to the server to see if we get good results
* Make the file parser differentiate a module or library error from a user file error
* Save errors in a database in a smart way so that they can be accessed again