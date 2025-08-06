# receiver_server.py
import ssl
import socket

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

# Load server certificate and key (this is the SERVER identity)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Load CA chain to verify CLIENT cert
context.load_verify_locations(cafile="../ca/intermediate/ca-chain.pem")

# Enforce mutual TLS
context.verify_mode = ssl.CERT_REQUIRED

bindsocket = socket.socket()
bindsocket.bind(('localhost', 8443))
bindsocket.listen(5)
print("Receiver (server) listening on port 8443...")

while True:
    newsocket, fromaddr = bindsocket.accept()
    with context.wrap_socket(newsocket, server_side=True) as conn:
        print("Accepted connection from", fromaddr)
        print("Client cert subject:", conn.getpeercert()["subject"])
        data = conn.recv(1024)
        print("Client says:", data.decode())
        conn.sendall(b"Hello sender via mTLS!")
