import ssl
import socket

# Create context to verify SERVER identity
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

# Load CLIENT cert and private key
context.load_cert_chain(certfile="client.crt", keyfile="client.key.pem")

# Load CA that signed SERVER cert
context.load_verify_locations(cafile="../ca/intermediate/ca-chain.pem")

# Enforce verification
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = False  # Disable only for localhost

with socket.create_connection(('localhost', 8443)) as sock:
    with context.wrap_socket(sock, server_hostname="DemoServer") as ssock:
        print("Connected to receiver (server)")
        ssock.sendall(b"Hello receiver via mTLS!")
        print("Receiver says:", ssock.recv(1024).decode())
