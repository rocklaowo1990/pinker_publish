import json


class string:
    # 
    # 这里真是更改字符串
    def removeSymbols(value: str):

        new = ''
        for i in value:
            if i.isalnum(
            ) or '\u4e00' <= i <= '\u9fa5':
                new += i
        return new
    
    def toJson(value):
       jsonStr = json.dumps(value,ensure_ascii=False)
       return json.loads(jsonStr)