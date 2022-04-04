import socket
import selectors
import types
import requestParser
import debug

sel = selectors.DefaultSelector()

HOST = "127.0.0.1"
PORT = 3333

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Conexion aceptada con {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Cerrando conexion con {data.addr}")
            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            jsonRequest = requestParser.parseRequest(data.outb)
            servers = requestParser.getServers(jsonRequest, "myconfig.ini")
            response = requestParser.connectToServer(data.outb, servers)
            
            if response == b'':
                response = b'{"estado" : 500, "mensaje" : "Error"}'
                debug.printError("\nNo hay respuesta e los servidores, deberian estar caidos")
    
            sock.send(response)
            data.outb = b''

def main():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print(f"Escuchando en {(HOST, PORT)}")
    lsock.setblocking(False)
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