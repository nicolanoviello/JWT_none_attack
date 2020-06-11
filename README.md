# JWT_confusion_attack

Progetto di sicurezza - Anno accademico 2019/2020
Componente software in grado simulare un attacco di tipo None algorithm su Token JWT

## Creazione dell'environment per l'installazione del progetto

- Il primo step prevede l'installazione di [Anaconda](https://www.anaconda.com/products/individual) disponibile per i principali sistemi operativi. Anaconda permette di creare ambienti python virtuali senza alterare le installazioni presenti sul sistema operativo principale

- Una volta installato Anaconda si può procedere all'attivazione dell'ambiente e all'installazione delle componenti necessarie

```
# Si crea una directory per il progetto
$ mkdir jwt
$ cd jwt

# Si crea un ambiente denominato jwt_none
$ virtualenv -p python3 jwt_none
$ source jwt_none/bin/activate
```

- Lo step successivo è quello che prevende l'installazione dei pacchetti necessari al funzionamento del codice. Nello specifico il software qui implementato fa uso di alcune routine della libreria jwt nella quale è stato riabilitato l'uso dell'algoritmo "None"  per replicare l'attacco e del framework Flask per la creazione di endpoint REST.

```
# Si installano i pacchetti necessari alla creazione degli endpoint
(jwt_none) $ pip install flask flask-restful flask-jwt-extended pylint-flask
(jwt_none) $ pip install jwt
```
- Se si vuole lavorare su un db locale (nel nostro caso SQLLite) è necessario installare flask_sqlalchemy che è in grado di gestire sia db locali che db su server remoti

```
# Installazione della librearia
(jwt_none) $ pip install flask_sqlalchemy
```

- Copiare i file presenti nella directory *libreria* del progetto all'interno nella directory creata da pip jwt_none/lib/python3.7/site-packages/jwt


- Per lanciare il server è necessario eseguire questo comando

```
(jwt_none) $ FLASK_APP=start.py FLASK_DEBUG=1 flask run
```
## Funzionamento del progetto

Il software implementato provvede ad esporre su *localhost*, sulla porta 3000, quattro servizi:
- */registration* 
  - attraverso una chiamata di tipo *POST* con un JSON contenente *username*, *password*, *ruolo* (non obbligatorio) verrà creato e salvato sul DB un utente in grado di effettuare una login con la coppia di credenziali *username/password*
  ```
  { 
  "username":"username dell'utente",
  "password":"password dell'utente",
  "ruolo":"ruolo dell'utente"
  }
  ```
  -  nel caso venga omesso il *ruolo*, l'utente sarà registrato come **studente**, gli altri ruoli possibili sono **root** e **abcde**. **root** è un utente creato di proposito per evitare che un attaccante in grado di sfruttare la vulnerabilità possa essere in grado di trovare in maniera esplicita il ruolo in grado di "catturare la bandiera", il secondo invece è il ruolo che ci permette di raggiungere il nostro target
  
- */login*
  - attraverso una chiamata di tipo *POST* con un JSON contenente *username* è *password* valide, tra quelle registrate nel DB, l'utente sarà in grado di effettuare una Login e ricevere un Token JWT da usare per la chiamata */scopriruolo*
  ```
  { 
  "username":"username dell'utente",
  "password":"password dell'utente"
  }
  ```
  
- */users*
  - attraverso una chiamata di tipo *GET* il sistema restituirà la lista degli utenti registrati sul sistema
  - attraverso una chiamata di tipo *DELETE* il sistema eliminerà tutti gli utenti presenti sul DB
  
- */scopriruolo*
  - attraverso una chiamata di tipo *GET* inserendo il JWT ricevuto dalla chiamata di login all'interno dell'Authorization Header il software controllerà il ruolo dell'utente e, nel caso si riesca a catturare la bandiera, restituirà il messaggio *"Sei ufficialmente root"* 
  

