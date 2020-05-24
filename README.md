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
$ virtualenv -p python3 sicurezza2020
$ source sicurezza2020/bin/activate

# Si installano i pacchetti necessari
(sicurezza2020) $ pip install flask flask-restful flask-jwt-extended
```
