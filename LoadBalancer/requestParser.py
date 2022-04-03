import configparser
import json
import socket
import random
import debug

from builtins import ConnectionRefusedError

PORT = 3334
INIFILE = "myconfig.ini"

def parseConfig(iniFile, operationType):
    config = configparser.ConfigParser()
    config.read_file(open(iniFile))

    if operationType == 'WRITE':
        sectionItems = dict(config.items('master'))
    elif operationType == 'READ':
        sectionItems = dict(config.items('master'))
        sectionItems.update(dict(config.items('slaves')))
    else:
        return None            
    return sectionItems

def parseRequest(request):

    strRequest = request.decode('utf-8')
    strRequest = strRequest.replace('\'', '\"')
    jsonRequest = json.loads(strRequest)

    return jsonRequest

def getServers(jsonRequest, iniFile):
    requestType = jsonRequest["type"]

    if requestType == "create" or requestType == "update" or requestType == "delete":
        operationType = "WRITE"
        print('Escribiendo a los servidores')
    elif requestType == "read":
        operationType = "READ"
        print('Leyendo de los servidores')
    print("Tipo de operacion:", operationType)

    servers = parseConfig(iniFile, operationType)
    return servers

def getRandomServer(servers):
    serverNames = list(servers)
    return random.choice(serverNames)

def connectToServer(request, servers):
    while len(servers) > 0:
        randomServer = getRandomServer(servers)
        server = servers[randomServer]
        serverIp, serverSock = server.split(',')
        serverSock = int(serverSock)
        response = b''

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((serverIp, serverSock))
            debug.printSuccess(f"Conectado a {serverIp, serverSock}")
            sock.sendall(request)
            response = sock.recv(1024)

            if response != b'':
                strResponse = response.decode('utf-8').replace('\'', '"')
                jsonResponse = json.loads(strResponse)

                try:

                    if jsonResponse["servers_errors"] == True:
                        failed_servers = jsonResponse["failed_servers"]

                        for server in failed_servers:
                            deleteServer(server)
                        print(failed_servers)
                except:
                    pass
            else:
                debug.printWarning(f"ALERTA: servidor {(serverIp, serverSock)} cerrado inesperadamente")
            sock.close()
            debug.printSuccess(f"Se cerró la conexión con{serverIp, serverSock}")
            break
        except ConnectionRefusedError:
            print("------------------------------------------")
            debug.printWarning(f"ALERTA: Servidor {serverIp, serverSock} caido")
            debug.printWarning("Intentando conectarse con otros servidores")
            print("------------------------------------------")
            servers.pop(randomServer)
            
    return response    

def deleteServer(server, iniFile=INIFILE):
    config = configparser.ConfigParser()
    config.read(iniFile)
    config.remove_option('slaves', server)
    with open(iniFile, "w") as file:
        config.write(file)