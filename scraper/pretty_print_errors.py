from bs4 import BeautifulSoup
import json

if __name__ == "__main__":
    parsed_location = '/home/user/basic_website/test_data/python_errors.json'
    
    #load raw data and print
    with open(parsed_location, 'r') as infile:
        errors = json.load(infile)
        count = 1
        for dict in errors:
            print("---------------- {} ----------------".format(count))
            soup = BeautifulSoup(dict["error"], 'html.parser')
            print(soup.prettify())  
            print("------------------------------------")
            count += 1