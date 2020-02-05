import os

import orjson

# with open('skill_table.json','rb') as file:
#     data=file.read()
#     data=orjson.loads(data)
#     print(data)
#     for skill in data:
#         print(data[skill])
        
b='n9u0CnXyf8iSNnSnUXjnO8'
b=b[::-1]
b=b.replace('f','').replace('n','')
print(b)
if b == '8OjXUSNSi8yXC0u9':
    print('yes')

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def xor(buf,mask):
    result = bytearray(b ^ m for (b, m) in zip(buf, mask))
    print(result)
    return

AES_MASK = b'8mNWvh7MRLGhyEuQ'

os.chdir("TextAsset")
with open("HotfixProcesser.lua.txt",'rb') as file:
    data = file.read()
    data = data[:144]
    data_list=list(chunks(data,16))
    for buf in data_list:
        xor(buf,AES_MASK)