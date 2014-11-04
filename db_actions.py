#!/usr/bin/python
import model

def __format_fields(fields_list):
    s = ""
    for f in fields_list:
        s += f + ","
    return s[:-1]

def save_object(obj, cursor):
    fields = obj.__dict__.keys()
    ss = __format_fields(["%s" for i in fields])
    values = tuple([ obj.__dict__[f] for f in fields ])
    query = "INSERT INTO " + obj.__tablename__ + " ("+ __format_fields(fields)+" ) values (" + ss +")"
    #print query, values
    cursor.execute(query, values)

def dump_cache(cache_dict, cursor):
    for obj in cache_dict.values():
        save_object(obj, cursor)



def test():
    class MockCursor:
        def execute(self,q,p):
            print q,p



    l = ['a','b','c']
    assert(__format_fields(l) == "a,b,c")
    p = model.Period("p1")
    save_object(p, MockCursor())

if __name__ == '__main__':
    test()
