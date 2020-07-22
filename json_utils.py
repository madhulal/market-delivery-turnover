import json


def write_dict_to_file(dict, complete_file_path):
    with open(complete_file_path, 'a+') as fp:
        json.dump(dict, fp, indent=4)
