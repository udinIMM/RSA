import socket
from Crypto.PublicKey import RSA

server = socket.socket()
host = 'localhost'
port = 6969

server.connect((host, port))

# Kasih tahu server jika koneksi OK
server.sendall("Client: OK")

# Terima string public key dari server
server_string = server.recv(1024)

# Hapus karakter ekstra
server_string = server_string.replace("public_key=", '')
server_string = server_string.replace("\r\n", '')

# Konversi string ke key
server_public_key = RSA.importKey(server_string)
print server_public_key

# Enkripsi pesan dan kirim ke server
message = "This is my secret message."
encrypted = server_public_key.encrypt(message, 32)
server.sendall("encrypted_message="+str(encrypted))

# Respons dari server
server_response = server.recv(1024)
server_response = server_response.replace("\r\n", '')
if server_response == "Server: OK":
    print "Server decrypted message successfully"  

# Kasih tahu server jika koneksi selesai
# server.sendall("Quit")
# print(server.recv(1024)) # Respons dari server untuk keluar
server.close()