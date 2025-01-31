def all_thing_is_obj(object: any) -> int:
    if (type(object) is list):
        print("List : " + str(type(object)))
    elif (type(object) is tuple):
        print("Tuple : " + str(type(object)))
    elif (type(object) is set):
        print("Set : " + str(type(object)))
    elif (type(object) is dict):
        print("Dict : " + str(type(object)))
    elif (type(object) is str):
        print(object, "is in the kitchen :", str(type(object)))
    else:
        print("Type not found")
    return 42
