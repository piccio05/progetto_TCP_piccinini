import threading
import socket
import mysql.connector
comunicazioni = ["",""]
PASSWORD = "CIAO"

def gestisci_comunicazione(conn):
    conn.send("Benvenuto, inserisci password: ".encode())
    data = conn.recv(1024).decode()
    i=0
    while data != PASSWORD and i<2:
        i+=1
        conn.send(f"Password ERRATA, reinserisci password: tentativi rimasti {2-i} ".encode())
        data = conn.recv(1024).decode()      

    if(data != PASSWORD):
        conn.send(f"Password ERRATA troppe volte, arrivederci".encode())
        conn.close()
        return

    while True:
        conn.send("Benvenuto, cosa vuoi fare: I=insert, U=update,R=read,D=delete".encode())
        data = conn.recv(1024).decode()
        print(data)
        if(data=="R"):
            conn.send("su che tabella vuoi leggere: C=clienti, Z=zone di lavoro".encode())
            tabella = conn.recv(1024).decode()            
            conn.send("Inserisci il nome da cercare: ".encode())
            nome = conn.recv(1024).decode()
            dati_query = db_get(nome, tabella)
            print(dati_query)
        
        elif(data=="I"):
            conn.send("su che tabella vuoi inserire: C=clienti, Z=zone di lavoro".encode())
            tabella = conn.recv(1024).decode()
            if(tabella=='C'):
                conn.send("Inserisci il nome da inserire: ".encode())
                nome = conn.recv(1024).decode()
                conn.send("Inserisci il cognome da inserire: ".encode())
                cognome = conn.recv(1024).decode()
                conn.send("Inserisci il numero di telefono da inserire: ".encode())
                tel = conn.recv(1024).decode()
                inserisci = db_inserisci(nome, cognome, tel, tabella)
                print(inserisci)
            elif(tabella=='Z'):
                conn.send("Inserisci il nome da inserire: ".encode())
                nome = conn.recv(1024).decode()
                conn.send("Inserisci il cognome da inserire: ".encode())
                cognome = conn.recv(1024).decode()
                conn.send("Inserisci il numero di telefono da inserire: ".encode())
                tel = conn.recv(1024).decode()
                conn.send("Inserisci le ore di lavoro: ".encode())
                ore_lavoro = conn.recv(1024).decode()
                inserisci2 = db_inserisci(nome, cognome, tel, tabella, ore_lavoro)
                print(inserisci2)
        
        elif(data=="D"):
            conn.send("su che tabella vuoi eliminare: C=clienti, Z=zone di lavoro".encode())
            tabella = conn.recv(1024).decode()
            conn.send("Inserisci nome da cancellare: ".encode())
            nome = conn.recv(1024).decode()        
            dati_query = db_delete(nome, tabella)
            print(dati_query)  

        elif(data=="U"):
            conn.send("su che tabella vuoi eliminare: C=clienti, Z=zone di lavoro".encode())
            tabella = conn.recv(1024).decode()
            conn.send("Inserisci nome da modificare: ".encode())
            nome = conn.recv(1024).decode() 
            if tabella=='C':
                conn.send("Che parametro vuoi modificare?(N=nome, C=cognome, T=telefono) : ".encode())
                parametro = conn.recv(1024).decode
                if(parametro=="N"):
                    conn.send("Inserisci il parametro modificato: ".encode())
                    nome_mod = conn.recv(1024).decode()
                    dati_query = db_update(nome, tabella, parametro, nome_mod)
                    print(dati_query)
                elif(parametro=="C"):
                    conn.send("Inserisci il parametro modificato: ".encode())
                    cognome_mod = conn.recv(1024).decode()
                    dati_query = db_update(nome, tabella, parametro, cognome_mod)
                    print(dati_query)
                elif(parametro=="T"):
                    conn.send("Inserisci il parametro modificato: ".encode())
                    tel_mod = conn.recv(1024).decode()
                    dati_query = db_update(nome, tabella, parametro, tel_mod)
                    print(dati_query)
            elif tabella=='Z':
                conn.send("Che parametro vuoi modificare?(N=nome, C=cognome, T=telefono, L=ore di lavoro) : ".encode())
                parametro = conn.recv(1024).decode()
                if(parametro=="N"):
                    conn.send("Inserisci il parametro modificato: ".encode())
                    nome_mod = conn.recv(1024).decode()
                    dati_query = db_update(nome, tabella, parametro, nome_mod)
                    print(dati_query)
                elif(parametro=="C"):
                    conn.send("Inserisci il parametro modificato: ".encode())
                    cognome_mod = conn.recv(1024).decode()
                    dati_query = db_update(nome, tabella, parametro, cognome_mod)
                    print(dati_query)
                elif(parametro=="T"):
                    conn.send("Inserisci il parametro modificato: ".encode())
                    tel_mod = conn.recv(1024).decode()
                    dati_query = db_update(nome, tabella, parametro, tel_mod)
                    print(dati_query)
                elif(parametro=='L'):
                    conn.send("Inserisci il parametro modficato: ".encode())
                    ore_mod = conn.recv(1024).decode()
                    dati_query = db_update(nome, tabella, parametro, ore_mod)
                    print(dati_query)


def db_get(nome_dipendente, tab):
    conn = mysql.connector.connect(
        host="10.10.0.10",
        user="diego_piccinini",
        password="piccinini1234",
        database="5ATepsit",
        port=3306, # voi qui mettete la porta 3306!! quella di default per mySQL, io ho dovuto mettere la 3307 perche la mia 3306 era gia occupata dal database SQL sul mio PC!
        )

    cur = conn.cursor()

    # si chiama una funzione di libreria passando i parametri di ricerca dell'utente. esempio controlla_caratteri(nome)
    if(tab=='C'):
        query = f"SELECT * FROM clienti_diego_piccinini WHERE nome = '{nome_dipendente}' "
    elif(tab=='Z'):
        query = f"SELECT * FROM zona_di_lavoro_diego_piccinini WHERE nome = '{nome_dipendente}' "
    print(query)
    cur.execute(query)
    dati = cur.fetchall()
    return dati

def db_inserisci(nome_dip, cogn_dip, tel_dip, tab, ore_dip):
    conn = mysql.connector.connect(
        host="10.10.0.10",
        user="diego_piccinini",
        password="piccinini1234",
        database="5ATepsit",
        port=3306, # voi qui mettete la porta 3306!! quella di default per mySQL, io ho dovuto mettere la 3307 perche la mia 3306 era gia occupata dal database SQL sul mio PC!
        )

    cur = conn.cursor()

    # si chiama una funzione di libreria passando i parametri di ricerca dell'utente. esempio controlla_caratteri(nome)
    if tab=='C':
        query = f"INSERT INTO `clienti_diego_piccinini`(`nome`, `cognome`, `telefono`) VALUES ('{nome_dip}', '{cogn_dip}', '{tel_dip}')"
    elif tab=='Z':
        query = f"INSERT INTO `zona_di_lavoro_diego_piccinini`(`nome`, `cognome`, `telefono`, `ore_lavoro`) VALUES ('{nome_dip}', '{cogn_dip}', '{tel_dip}', '{ore_dip}')"
    print(query)
    cur.execute(query)
    dati = conn.commit()
    return dati

def db_delete(data, tab):
    conn = mysql.connector.connect(
        host="10.10.0.10",
        user="diego_piccinini",
        password="piccinini1234",
        database="5ATepsit",
        port=3306, # voi qui mettete la porta 3306!! quella di default per mySQL, io ho dovuto mettere la 3307 perche la mia 3306 era gia occupata dal database SQL sul mio PC!
        )

    cur = conn.cursor()

    # si chiama una funzione di libreria passando i parametri di ricerca dell'utente. esempio controlla_caratteri(nome)
    if tab=='C':
        query = f"DELETE FROM clienti_diego_piccinini where nome= '{data}' "
    elif tab=='Z':
        query = f"DELETE FROM zona_di_lavoro_diego_piccinini where nome= '{data}' "
    print(query)
    cur.execute(query)
    conn.commit()
    return

def db_update(data, tab, par, mod):
    conn = mysql.connector.connect(
        host="10.10.0.10",
        user="diego_piccinini",
        password="piccinini1234",
        database="5ATepsit",
        port=3306, # voi qui mettete la porta 3306!! quella di default per mySQL, io ho dovuto mettere la 3307 perche la mia 3306 era gia occupata dal database SQL sul mio PC!
        )

    cur = conn.cursor()

    #conn.send("Che parametro vuoi modificare?(N=nome, C=cognome, T=telefono) : ".encode())
    if tab=='C':
        if(par=="N"):
            query = f"UPDATE `clienti_diego_piccinini` SET `nome`='{mod}' WHERE 1=1 and nome='{data}'"
            cur.execute(query)
            conn.commit()
            return
        elif(par=="C"):
            query = f"UPDATE `clienti_diego_piccinini` SET `cognome`='{mod}' WHERE 1=1 and nome='{data}'"
            cur.execute(query)
            conn.commit()
            return
        elif(par=="T"):
            query = f"UPDATE `clienti_diego_piccinini` SET `telefono`='{mod}' WHERE 1=1 and nome='{data}'"
            cur.execute(query)
            conn.commit()
            return
    elif tab=='Z':
        if(par=="N"):
            query = f"UPDATE `zona_di_lavoro_diego_piccinini` SET `nome`='{mod}' WHERE 1=1 and nome='{data}'"
            cur.execute(query)
            conn.commit()
            return
        elif(par=="C"):
            query = f"UPDATE `zona_di_lavoro_diego_piccinini` SET `cognome`='{mod}' WHERE 1=1 and nome='{data}'"
            cur.execute(query)
            conn.commit()
            return
        elif(par=="T"):
            query = f"UPDATE `zona_di_lavoro_diego_piccinini` SET `telefono`='{mod}' WHERE 1=1 and nome='{data}'"
            cur.execute(query)
            conn.commit()
            return
        elif par=='L':
            query = f"UPDATE `zona_di_lavoro_diego_piccinini` SET `ore_lavoro`='{mod}' WHERE 1=1 and nome='{data}'"
            cur.execute(query)
            conn.commit()
            return


print("server in ascolto: ")
lock = threading.Lock()
HOST = ''                 # Nome simbolico che rappresenta il nodo locale, ci va l'indirizzo IP
PORT = 50010            # Porta non privilegiata arbitraria
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)
thread = []
lista_connessioni = []
i=0

while True:
    lista_connessioni.append( s.accept() ) #connessione = s.accept() 
    print('Connected by', lista_connessioni[i][1]) # print(connessione[0])
    thread.append(threading.Thread(target=gestisci_comunicazione, args = (lista_connessioni[i][0],) )) 
    thread[i].start()
    i+=1
