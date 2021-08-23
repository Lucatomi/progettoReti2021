# -*- coding: utf-8 -*-
"""
Progetto di Programmazione di Reti a.a. 2020-21

Cognome e Nome: Tomidei Luca
Matricola: 902747

Traccia 2: Python Web Server
"""

import http.server
import sys,signal
import socketserver
import threading

#manage the wait witout busy waiting
waiting_refresh = threading.Event()


# Legge il numero della porta dalla riga di comando
if sys.argv[1:]:
  port = int(sys.argv[1])
else: #porta di default, nel caso non venga specificato nella linea di comando
  port = 8080
  
  # classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si voglia fare un refresh
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("AllRequestsGET.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          out.write(str(info))
        if self.path == '/refresh':
            resfresh_contents()
            self.path = '/'
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)

#-----------
# la parte iniziale è identica per tutti servizi
header_html = """
<html>
    <head>
        <style>
            h1 {
                text-align: center;
                margin: 0;
            }
            table {width:70%;}
            img {
                max-width:300;
                max-height:200px;
                width:auto;
            }
            td {width: 33%;}
            p {text-align: center;
               font-size: 20px}
            td {
                padding: 20px;
                text-align: center;
            }
            .topnav {
  		        overflow: hidden;
  		        background-color: #333;
  		    }
            .topnav a {
  		        float: left;
  		        color: #f2f2f2;
  		        text-align: center;
  		        padding: 14px 16px;
  		        text-decoration: none;
  		        font-size: 17px;
  		    }        
  		    .topnav a:hover {
  		        background-color: #ddd;
  		        color: black;
  		    }        
  		    .topnav a.active {
  		        background-color: #4CAF50;
  		        color: white;
  		    }
        </style>
    </head>
    <body>
        <title>Azienda Tomidei</title>
"""

# la barra di navigazione è identica per tutti servizi
navigation_bar = """
        <br>
        <br>
        <br>
        <div class="topnav">
            <a class="active" href="http://127.0.0.1:{port}/index.html">Home</a>
            <a href="http://127.0.0.1:{port}/pronto_soccorso.html">Pronto soccorso</a>
            <a href="http://127.0.0.1:{port}/medicina_sport.html">Medicina dello sport</a>
            <a href="http://127.0.0.1:{port}/tamponi.html">Tamponi rapidi</a>
            <a href="http://127.0.0.1:{port}/screening.html">Screening Oncologici</a>
            <a href="http://127.0.0.1:{port}/farmacie.html">Farmacie di turno</a>
  		    <a href="http://127.0.0.1:{port}/refresh" style="float: right">Aggiorna contenuti</a>
            <a href="http://127.0.0.1:{port}/info.pdf" download="info.pdf" style="float: right">Download info pdf</a>
  		</div>
        <br><br>
        <table align="center">
""".format(port=port)

# la parte finale è identica per tutti servizi
footer_html= """
        </table>
    </body>
</html>
"""

#la parte finale per la pagina pronto soccorso
end_page_pronto_soccorso= """
        <br><br>
		<form action="http://127.0.0.1:{port}/pronto_soccorso.html" method="post" style="text-align: center;">
		  <img src='images/pronto_soccorso.png'/ width="150" height="150">
          <h1><strong>PRONTO SOCCORSO</strong></h1><br>
          <p>Il servizio di Pronto Soccorso &egrave rivolto a persone che hanno di bisogno di cure urgenti.<br>
          Per situazioni non urgenti &egrave opportuno rivolgersi direttamente al proprio medico di famiglia od al servizio sostitutivo di guardia medica.<br>
          Qui di seguito &egrave riportato il link alla pagina del pronto soccorso.</p>
          <a href="https://www.auslromagna.it/servizi/pronto-soccorso"><h1>Raggiungi il sito del pronto soccorso.</a></h1>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina medicina sport
end_page_medicina_sport= """
        <br><br>
		<form action="http://127.0.0.1:{port}/pronto_soccorso.html" method="post" style="text-align: center;">
		  <img src='images/medicina.jpg'/ width="150" height="150">
          <h1><strong>MEDICINA SPORT</strong></h1><br>
          <p>Il centro di Medicina dello Sport si occupa della valutazione clinico-funzionale dello sportivo,<br> per il rilascio dell'idoneit&agrave sportiva agonistica e non agonistica.<br>
          Qui di seguito il link alla pagina ufficiale.</p>
          <a href="https://www.ospedaliprivatiforli.it/servizi-e-specialita-mediche/medicina-dello-sport/"><h1>Raggiungi il sito medicina dello sport</a></h1>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina tamponi rapidi
end_page_tamponi= """
        <br><br>
		<form action="http://127.0.0.1:{port}/pronto_soccorso.html" method="post" style="text-align: center;">
		  <img src='images/tamponi.jpg'/ width="150" height="150">
          <h1><strong>TAMPONI RAPIDI</strong></h1><br>
          <p>Come gi&agrave annunciato su giornali e social media nei giorni scorsi, da oggi sono effettivamente operativi i tamponi rapidi e i test sierologici per tutti gli assistiti nella Regione Emilia-Romagna.
          <br>Da oggi, infatti, si potranno effettuare, sempre su base volontaria e su appuntamento, entrambi i due tipi di test, nelle Farmacie che aderiscono al servizio, con alcune novit&agrave.</p>
          <a href="http://www.forlifarma.it/news/tamponi-rapidi-e-test-sierologici-in-farmacia-per-tutti/"><h1>Raggiungi il sito riguardo i tamponi rapidi.</a></h1>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina screening
end_page_screening= """
        <br><br>
		<form action="http://127.0.0.1:{port}/pronto_soccorso.html" method="post" style="text-align: center;">
		  <img src='images/screening.jpg'/ width="150" height="150">
         <h1><strong>SCREENING ONCOLOGICO</strong></h1><br>
          <p>Lo screening oncologico &egrave un intervento di salute pubblica gratuito che consiste nell'invitare la popolazione, apparentemente sana ma potenzialmente esposta al rischio di contrarre il cancro,<br> a sottoporsi a esami di prevenzione e diagnosi precoce.<br>
          Qui di seguito &egrave riportato il collegamento al sito con tutte le informazioni a riguardo.</p>
          <a href="https://www.auslromagna.it/servizi/screening-oncologici"><h1>Raggiungi la pagina riguardo lo screening oncologico.</a></h1>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina farmacie turno
end_page_farmacie= """
        <br><br>
		<form action="http://127.0.0.1:{port}/pronto_soccorso.html" method="post" style="text-align: center;">
		  <img src='images/farmacie.png'/ width="150" height="150">
          <h1><strong>FARMACIE DI TURNO</strong></h1><br>
          <p>La Guardia Farmaceutica (Farmacia di Turno) &egrave un servizio che ogni farmacia aperta al pubblico deve fornire in base a una specifica Legge Regionale (n. 33 del 30 dicembre 2009). <br> Il servizio viene svolto da un farmacista nella farmacia di turno ed assicura la distribuzione dei farmaci durante gli orari di chiusura delle farmacie.</p>
          <a href="https://www.auslromagna.it/servizi/farmacie"><h1>Trova la farmacia pi&ugrave vicina</a></h1>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#la parte finale per la pagina home
end_page_index = """
        <br><br>
		<form action="http://127.0.0.1:{port}/home.html" method="post" style="text-align: center;">
        <h1><strong>AZIENDA TOMIDEI</strong></h1><br>
          <p>Benvenuti nell'homepage dell'Azienda Tomidei.<br>
          Per navigare all'interno del sito utilizzare i link nella barra di navigazione sovrastante, i quali reindirizzeranno direttamente alla pagina del servizio desiderata.</p>
		</form>
		<br>
    </body>
</html>
""".format(port=port)
    

#metodo lanciato per la creazione delle pagine servizi
def create_page_servizio(title,file_html, end_page):
    f = open(file_html,'w', encoding="utf-8")
    try:
        message = header_html + title + navigation_bar + end_page
        message = message + footer_html
    except:
        pass
    f.write(message)
    f.close()

# creazione della pagina specifica del pronto soccorso
def create_page_pronto_soccorso():
    create_page_servizio("<h1>Pronto soccorso</h1>"  , 'pronto_soccorso.html', end_page_pronto_soccorso )

# creazione della pagina specifica della medicina dello sport
def create_page_medicina_sport():
    create_page_servizio("<h1>Medicina dello sport</h1>"  , 'medicina_sport.html', end_page_medicina_sport)
    
# creazione della pagina specifica dei tamponi
def create_page_tamponi():
    create_page_servizio("<h1>Tamponi rapidi</h1>"  , 'tamponi.html', end_page_tamponi )
    
# creazione della pagina specifica dello screening
def create_page_screening():
    create_page_servizio("<h1>Screening oncologico</h1>"  , 'screening.html', end_page_screening )

# creazione della pagina specifica delle farmacie
def create_page_farmacie():
    create_page_servizio("<h1>Farmacie di turno</h1>"  , 'farmacie.html', end_page_farmacie )
    
# creazione della pagina index.html (iniziale)
# contenente pagina principale del Azienda ospedaliera
def create_index_page():
    create_page_servizio("<h1>Azienda Tomidei</h1>", 'index.html', end_page_index )
    
# creo tutti i file utili per navigare.
def resfresh_contents():
    print("updating all contents")
    create_index_page()
    create_page_pronto_soccorso()
    create_page_medicina_sport()
    create_page_screening()
    create_page_tamponi()
    create_page_farmacie()
    print("finished update")
  
# questo thread ogni 300 secondi (5 minuti) aggiorna contenuti
def launch_thread_resfresh():
    t_refresh = threading.Thread(target=resfresh_contents())
    t_refresh.daemon = True
    t_refresh.start()
    
# definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if(server):
        server.server_close()
    finally:
      # fermo il thread del refresh senza busy waiting
      waiting_refresh.set()
      sys.exit(0)
      
# metodo che viene chiamato al "lancio" del server
def main():
    usr = input("username: ") #richiesto l'username da tastiera
    psw = input("password: ") #richiesta la password
    if(usr != 'luca' or psw != 'tomidei'):
        print("Errore.")
        server.server_close() #Per evitare errori al prossimo avvio
        sys.exit(0)
    # lancio un thread che carica il meteo e aggiorna ricorrentemente i contenuti
    launch_thread_resfresh()
    #Assicura che da tastiera usando la combinazione
    #di tasti Ctrl-C termini in modo pulito tutti i thread generati
    server.daemon_threads = True 
    #il Server acconsente al riutilizzo del socket anche se ancora non è stato
    #rilasciato quello precedente, andandolo a sovrascrivere
    server.allow_reuse_address = True  
    #interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
    signal.signal(signal.SIGINT, signal_handler)
    # cancella i dati get ogni volta che il server viene attivato
    f = open('AllRequestsGET.txt','w', encoding="utf-8")
    f.close()
    # entra nel loop infinito
    try:
      while True:
        server.serve_forever()
    except KeyboardInterrupt:
      pass
    server.server_close()

if __name__ == "__main__":
    main()
