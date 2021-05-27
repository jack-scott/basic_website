# Scraper

Currently just collates a JSON file full of Python errors and a link to the Stack Overflow page

## To run

Run `python testing_tools.py` in the docker container. Will output a raw and a parsed `.json` file in the `test_data` folder

## Next steps 

* Split the error message into useful components
* Pass components of the error to the server to see if we get the same link back
* Create a way to bulk retrieve and store the errors