import json
import MasterCRUD
import socket
import selectors
import types
import requestParser
import random

sel = selectors.DefaultSelector()

HOST = "127.0.0.1"
PORT = 3335

sel = selectors.DefaultSelector()

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Conexion aceptada con {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Cerrando conexion con {data.addr}")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            jsonRequest = requestParser.parseRequest(data.outb)
            if(jsonRequest["type"] == "create"):
                result = MasterCRUD.create(jsonRequest)
            elif(jsonRequest["type"] == "read"):
                result = MasterCRUD.read(jsonRequest)
            elif(jsonRequest["type"] == "update"):
                result = MasterCRUD.update(jsonRequest)
            elif(jsonRequest["type"] == "delete"):
                result = MasterCRUD.delete(jsonRequest)
            print(result)
            
            sock.send(bytes(str(result), 'utf-8'))
            
            data.outb = b""   


def main():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print(f"Escuchando en {(HOST, PORT)}")
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Interrupcion por teclado encontrada, saliendo")
    finally:
        sel.close()

if __name__=="__main__":
    main()