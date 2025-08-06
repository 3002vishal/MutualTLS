import ssl
import socket
from pprint import pprint

# Optional: Uncomment to use better cert parsing
# from cryptography import x509
# from cryptography.hazmat.backends import default_backend

# Configuration
SERVER_CERT = "server.crt"
SERVER_KEY = "server.key"
CLIENT_CA_CHAIN = "../ca/intermediate/ca-chain.pem"
HOST = "localhost"
PORT = 8443

# Create context to verify client identity (mTLS)
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
context.load_verify_locations(cafile=CLIENT_CA_CHAIN)
context.verify_mode = ssl.CERT_REQUIRED  # Mandatory client certificate

# Setup listening socket
bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindsocket.bind((HOST, PORT))
bindsocket.listen(5)
print(f"🔐 Server listening on {HOST}:{PORT}...")

while True:
    newsocket, fromaddr = bindsocket.accept()
    try:
        print(f"➡️ Connection received from {fromaddr}")
        with context.wrap_socket(newsocket, server_side=True) as conn:
            print("✅ TLS handshake successful")

            # Attempt to parse client cert
            cert = conn.getpeercert()
            if cert:
                print("🔍 Client certificate (parsed):")
                pprint(cert)

                # Extract subject info
                subject = cert.get("subject", [])
                subject_dict = dict(x[0] for x in subject)
                print("📛 Client certificate subject:", subject_dict)
            else:
                print("⚠️ No client certificate received!")

            # Communication
            data = conn.recv(1024).decode()
            print(f"💬 Client says: {data}")
            conn.sendall(b"Hello sender via mTLS!")

    except ssl.SSLError as e:
        print(f"❌ SSL error during handshake or communication: {e}")
    except Exception as e:
        print(f"❌ General server error: {e}")
