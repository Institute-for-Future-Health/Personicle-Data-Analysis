import json

# Import this module to have access to the fix_json method.
# You can call this with the parameter as a file path, 
# a dict for fixing, a list for fixing, or anything that can be used with
# json.load to yield a dict.

# EXAMPLE: 
# >>> x = fix_json([None,{"meow":"hello"}, {"cats":"happiness"}])
# >>> print(x)
# {'1': {'meow': 'hello'}, '2': {'cats': 'happiness'}}

def fix_json(f):
    out = {}
    if type(f) == str:
        #file path
        with open(f, encoding="utf8") as open_file:
            out = json.load(open_file)  
    elif type(f) == dict or type(f) == list:
        out = f
    else:
        out = json.load(f)
    
    
    def fix(i):
        tmp = {}
        if isinstance(i, list) and len(i) > 0 and i[0] is None:
            for index,value in enumerate(i[1:]):
                tmp[str(index+1)] = value
            i = tmp
        if isinstance(i, dict):
            return {k: fix(v) for k, v in i.items()}
        else:
            return i
    out = fix(out)
    
    return out