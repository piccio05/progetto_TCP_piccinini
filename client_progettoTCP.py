import socket

HOST = 'localhost'    # Il nodo remoto, qui metti il tuo indirizzo IP per provare connessione server e client dalla tua macchina alla tua macchina
PORT = 50010             # La stessa porta usata dal server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = s.recv(1024)
    if(data.decode()=="STOP"):
        print("password ERRATA troppe volte, arrivederci")
        break

    print('Received: ', data.decode())
    testo = input("").encode()
    s.send(testo)


s.close()