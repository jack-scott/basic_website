from __future__ import division 
import json
from bs4 import BeautifulSoup
import requests
import json


# Finds the code block in the HTML body that contains the error. Defined as containing the word "Traceback"
# Is looking for code blocks defined as <pre><code>
# Returns a dict with {"error": {str}, "link": {str}}
def parse_errors_from_raw_SO(raw_html):
    parsed_errors = []
    raw_dump = json.load(raw_html)
    for item in raw_dump:
        body = item['body']
        soup = BeautifulSoup(body, 'html.parser')
        code_snippets = soup.find_all("pre")
        for code in code_snippets:
            code = str(code)
            if "Traceback" in code:
                error_str = BeautifulSoup(code,'html.parser').get_text()
                parsed_errors.append({"error": error_str, "link":item["link"]})

    return parsed_errors

# Requests data from Stack Overflow (SO), returns as a list of dicts
def get_data_from_SO():
    complete_data=[]
    # Returns the body of question + link of a post that contains the "python" tag and the word "Traceback"
    response = requests.get("https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=Traceback&accepted=True&tagged=python&site=stackoverflow&filter=!YES68u6h(-Jjx*i7h20uA.zjk.Kr)2VnxX9aA_PXmT7q38JLHX4")
    newData=json.loads(response.text)
    for item in newData['items']:
        complete_data.append(item)

    return complete_data


if __name__ == "__main__":
    raw_location = '/home/user/basic_website/test_data/raw_SO_dump.json'
    parsed_location = '/home/user/basic_website/test_data/python_errors.json'

    raw_data = get_data_from_SO()
    
    num_raw = len(raw_data)
    if num_raw > 0:
        print("Succesfully collected data from SO, got {} results returned".format(num_raw))
    #save raw data
    with open(raw_location, 'w+') as outfile:
        json.dump(raw_data, outfile)

    #load raw data and parse
    parsed_errors = []
    with open(raw_location, 'r') as infile:
        parsed_errors = parse_errors_from_raw_SO(infile)
    
    num_parsed = len(parsed_errors)
    if num_parsed > 0:
        print("Succesfully parsed {:.2f}% of raw data".format((num_parsed/num_raw)*100))
    # save parsed errors
    with open(parsed_location, 'w+') as outfile:
        json.dump(parsed_errors, outfile)