
def list_item(_class, list_from_api):
    obj_list_ret = []
    for elements in list_from_api:
        obj_list_ret.append(_class(elements))
    return obj_list_ret