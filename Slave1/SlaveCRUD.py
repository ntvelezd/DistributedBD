import json
import FileHandler as file_handler

def create(variables_dict):
    response = file_handler.create(variables_dict["dbname"], variables_dict["table"], variables_dict["key"], variables_dict["values"])
    return json.dumps(response) 

def read(variables_dict):
    return file_handler.read(variables_dict["dbname"], variables_dict["table"], variables_dict["key"])
    
def update(variables_dict):
    response = file_handler.update(variables_dict["dbname"], variables_dict["table"], variables_dict["key"], variables_dict["new_values"])
    return json.dumps(response) 

def delete(variables_dict):
    response = file_handler.delete(variables_dict["dbname"], variables_dict["table"], variables_dict["key"])
    return json.dumps(response) 