import orjson

with open('skill_table.json','rb') as file:
    data=file.read()
    data=orjson.loads(data)
    print(data)
    for skill in data:
        print(data[skill])