import configparser
import json

def parseConfig(iniFile, operationType):
    config = configparser.ConfigParser()
    config.read_file(open(iniFile))
    print(config.sections())
    print("\n------ Parsing configurations file ------")
    if operationType == 'WRITE':
        sectionItems = dict(config.items('master'))
    elif operationType == 'READ':
        sectionItems = dict(config.items('master'))
        sectionItems.update(dict(config.items('slaves')))
    else:
        return None            
    return sectionItems

def parseRequest(request):
    # print('\n------- Parsing request --------')
    strRequest = request.decode('utf-8')
    strRequest = strRequest.replace('\'', '\"')
    jsonRequest = json.loads(strRequest)
    # print(jsonRequest)
    return jsonRequest

def getServers(jsonRequest, iniFile):
    requestType = jsonRequest["type"]
    print("Request type:", requestType)
    if requestType == "create" or requestType == "update" or requestType == "delete":
        operationType = "WRITE"
        print('WRITING TO SERVERS')
    elif requestType == "read":
        operationType = "READ"
        print('READING FROM SERVERS')
    print("Operation type:", operationType)
    servers = parseConfig(iniFile, operationType)
    return servers