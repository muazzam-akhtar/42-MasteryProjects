import pandas


def NULL_not_found(object: any) -> int:
    if type(object) is int:
        if object == 0:
            print(str(object) + " " + str(type(object)))
            return 0
        else:
            print("Type not Found")
    if type(object) is bool:
        if object is False:
            print("False " + str(type(object)))
            return 0
        else:
            print("Type not Found")
    if type(object) is float and pandas.isna(object):
        print("nan " + str(type(object)))
        return 0
    elif type(object) is float:
        print("Type not Found")
    if type(object) is str:
        if len(object) == 0:
            print(str(type(object)))
            return 0
        else:
            print("Type not Found")
    if object is None:
        print(str(object) + " " + str(type(object)))
        return 0
    return 1
