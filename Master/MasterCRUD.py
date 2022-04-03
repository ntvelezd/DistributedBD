import requestParser
import json
import FileHandler as file_handler

def create(variables_dict):
    servers_errors, failed_servers = requestParser.connectToServer(variables_dict)
    response = file_handler.create(variables_dict["dbname"], variables_dict["table"], variables_dict["key"], variables_dict["values"])
    response["failed_servers"] = failed_servers
    response["servers_errors"] = servers_errors
    return json.dumps(response) 

def read(variables_dict):
    return file_handler.read(variables_dict["dbname"], variables_dict["table"], variables_dict["key"])
    
def update(variables_dict):
    servers_errors, failed_servers = requestParser.connectToServer(variables_dict)
    response = file_handler.update(variables_dict["dbname"], variables_dict["table"], variables_dict["key"], variables_dict["new_values"])
    response["failed_servers"] = failed_servers
    response["servers_errors"] = servers_errors
    return json.dumps(response) 

def delete(variables_dict):
    servers_errors, failed_servers = requestParser.connectToServer(variables_dict)
    response = file_handler.delete(variables_dict["dbname"], variables_dict["table"], variables_dict["key"])
    response["failed_servers"] = failed_servers
    response["servers_errors"] = servers_errors
    return json.dumps(response) 