# sicurezza2020

Progetto di sicurezza - Anno accademico 2019/2020

## Creazione dell'environment per l'installazione del progetto

- Il primo step prevede l'installazione di [Anaconda](https://www.anaconda.com/products/individual) disponibile per i principali sistemi operativi. Anaconda permette di creare ambienti python virtuali senza alterare le installazioni presenti sul sistema operativo principale

- Una volta installato Anaconda si può procedere all'attivazione dell'ambiente e all'installazione delle componenti necessarie

```
# Si crea una directory per il progetto
$ mkdir jwt
$ cd jwt

# Si crea un ambiente denominato sicurezza2020
$ virtualenv -p python3 jwt_none
$ source jwt_none/bin/activate

# Si installano i pacchetti necessari alla creazione degli endpoint
(jwt_none) $ pip install flask flask-restful flask-jwt-extended pylint-flask

# Se si vuole lavorare su un db locale (nel nostro caso SQLLite) è necessario installare flask_sqlalchemy
# che è in grado di gestire sia db locali che db su server remoti
(jwt_none) $ pip install flask_sqlalchemy
```
pip install jwt
- Per lanciare il server è necessario eseguire questo comando

```
(sicurezza2020) $ FLASK_APP=start.py FLASK_DEBUG=1 flask run
```
