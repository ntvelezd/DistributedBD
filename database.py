import json
import socket

PORT = 3333  # The port used by the load-balancer

class Connection():
    def __init__(self, sock, dbname):
        self.dbname = dbname
        self.sock = sock

    def close(self):
        self.sock.close()

    def get(self, tableName):
        table = Table(self.sock, self.dbname, tableName)
        return table

class Table(Connection):
    def __init__(self, sock, dbname, table):
        super().__init__(sock, dbname)
        self.table = table

    def put(self, key, value):
        request = {
            "dbname": self.dbname,
            "table": self.table,
            "type": "create",
            "key": key,
            "values": value
            } 
        jsonBytes = bytes(str(request), 'utf-8') 
        self.sock.sendall(jsonBytes)
        response = self.sock.recv(1024)
        strResponse = response.decode('utf-8').replace("'", '"')
        jsonResponse = json.loads(strResponse)
        print("Received:", jsonResponse)

    def get(self, key):
        request = {
            "dbname": self.dbname,
            "table": self.table,
            "type": "read",
            "key": key,
            } 
        jsonBytes = bytes(str(request), 'utf-8') 
        self.sock.sendall(jsonBytes)
        response = self.sock.recv(1024)
        strResponse = response.decode('utf-8').replace("'", '"')
        jsonResponse = json.loads(strResponse)
        print("Recibido:", jsonResponse)
        if jsonResponse["estado"] == 200:
            return jsonResponse["valores"]

    def delete(self, key):
        request = {
            "dbname": self.dbname,
            "table": self.table,
            "type": "delete",
            "key": key
            } 
        jsonBytes = bytes(str(request), 'utf-8') 
        self.sock.sendall(jsonBytes)
        response = self.sock.recv(1024)
        strResponse = response.decode('utf-8').replace("'", '"')
        jsonResponse = json.loads(strResponse)
        print("Received:", jsonResponse)

    def update(self, key, new_values):
        request = {
            "dbname": self.dbname,
            "table": self.table,
            "type": "update",
            "key": key,
            "new_values": new_values,
            } 
        jsonBytes = bytes(str(request), 'utf-8') 
        self.sock.sendall(jsonBytes)
        response = self.sock.recv(1024)
        strResponse = response.decode('utf-8').replace("'", '"')
        jsonResponse = json.loads(strResponse)
        print("Received:", jsonResponse)

def connect(host, db):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, PORT))
    connection = Connection(sock, db)
    return connection