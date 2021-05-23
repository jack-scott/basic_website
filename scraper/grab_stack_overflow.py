import requests
import json

complete_data=[]

# Returns the body of question + link of a post that contains the python tag and the word traceback
response = requests.get("https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=Traceback&accepted=True&tagged=python&site=stackoverflow&filter=!YES68u6h(-Jjx*i7h20uA.zjk.Kr)2VnxX9aA_PXmT7q38JLHX4")
newData=json.loads(response.text)
for item in newData['items']:
    complete_data.append(item)

# print(complete_data)
with open('/home/user/basic_website/test_data/raw_SO_dump.json', 'w') as outfile:
    json.dump(complete_data, outfile)