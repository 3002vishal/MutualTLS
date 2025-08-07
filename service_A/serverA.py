import ssl
import socket

def run_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="serviceA.crt", keyfile="serviceA.key")
    context.load_verify_locations(cafile="../ca/intermediate/ca-chain.pem")
    context.verify_mode = ssl.CERT_REQUIRED

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8443))
    server_socket.listen(5)

    with context.wrap_socket(server_socket, server_side=True) as ssock:
        print("✅ Service A listening on port 8443 (mTLS)...")
        conn, addr = ssock.accept()
        print("🔗 Accepted connection from", addr)
        print("🔒 Client cert subject:", conn.getpeercert())
        data = conn.recv(1024)
        print("📩 Received:", data.decode())
        conn.send(b"Hello from Service A")
        conn.close()

if __name__ == "__main__":
    run_server()

