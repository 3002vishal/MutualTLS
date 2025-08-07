import ssl
import socket

def run_client():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile="serviceB.crt", keyfile="serviceB.key")
    context.load_verify_locations(cafile="../ca/intermediate/ca-chain.pem")
    context.verify_mode = ssl.CERT_REQUIRED

    with context.wrap_socket(socket.socket(), server_hostname='service-a') as client_sock:
        client_sock.connect(('service-a', 8443))
        print("🔐 Connected to Service A (mTLS server)")
        client_sock.send(b"Hello from Service B client")
        response = client_sock.recv(1024)
        print("📩 Received from server:", response.decode())

if __name__ == "__main__":
    run_client()
