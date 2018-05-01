import socket
from Crypto.PublicKey import RSA
from Crypto import Random

# Generate private dan public key
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()

# Socket biasa
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 6969
encrypt_string = "encrypted_message="

# Jika socket.error: [Errno 98] Address already in use
mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mysocket.bind((host, port))
mysocket.listen(5)
c, addr = mysocket.accept()

while True:
    print "got connection from ", c.getpeername()
    # Tunggu sampai data diterima
    rcstring = ''
    data = c.recv(1024)
    data = data.replace("\r\n", '') # hapus new line
    rcstring += data
    print len(data)
    print len(rcstring)
    if not len(data):
        break

    if data == "Client: OK":
        c.send("public_key=" + public_key.exportKey() + "\n")
        print "Public key sent to client."
        print public_key

    elif encrypt_string in data: # Terima pesan terenkripsi dan mendekripnya
        data = data.replace(encrypt_string, '')
        print "Received:\nEncrypted message = "+str(data)
        encrypted = eval(data)
        decrypted = private_key.decrypt(encrypted)
        c.send("Server: OK")
        print "Decrypted message = " + decrypted

    # elif data == "Quit": break

# Print server berhenti
c.send("Server stopped\n")
print "Server stopped"
c.close()