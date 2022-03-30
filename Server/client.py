import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3333  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    json = {
            "type": "read",
            "value": "lo que sea"
            } 
    jsonBytes = bytes(str(json), 'utf-8') 
    print(str(json))
    s.sendall(jsonBytes)
    data = s.recv(1024)

print(f"Received {data!r}")