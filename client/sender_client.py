# sender_client.py
import ssl
import socket

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

# Load client cert and key (this is the CLIENT identity)
context.load_cert_chain(certfile="client.crt", keyfile="client.key.pem")

# Load CA chain to verify SERVER cert
context.load_verify_locations(cafile="../ca/intermediate/ca-chain.pem")

# Enforce mutual TLS
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = False  # Only disable if testing locally

with socket.create_connection(('localhost', 8443)) as sock:
    with context.wrap_socket(sock, server_hostname="DemoServer") as ssock:
        print("Connected to receiver (server)")
        ssock.sendall(b"Hello receiver via mTLS!")
        print("Receiver says:", ssock.recv(1024).decode())
