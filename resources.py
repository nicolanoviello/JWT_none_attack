from flask_restful import Resource, reqparse
from models import UserModel

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

# flask_restful ha una libreria integrata per il parsing
# possiamo usarla per effettuare verifiche sui campi obbligatori
# ad esempio questi sono quelli necessari alla login
parser = reqparse.RequestParser()
parser.add_argument('username', help = 'Questo campo non può essere vuoto', required = True)
parser.add_argument('password', help = 'Questo campo non può essere vuoto', required = True)



# qui è definita la lista di tutti gli endpoint da provare
class Registration(Resource):
    def post(self):
        data = parser.parse_args()
        # Acquisisco i dati da JSON
        nuovo_utente = UserModel(
            username = data['username'],
            password = data['password']
        )
        # Controllo se l'utente è già presente su db
        if UserModel.cerca_su_db(data['username']):
          return {'message': '{} è già presente sul DB'. format(data['username'])}

        try:
            # Provo a creare un nuovo utente con i dati inviati nella post
            nuovo_utente.salva_sul_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Utente {} correttamente creato'.format( data['username']),
                'access_token': access_token
            }
        except:
            # Restituisco un errore 500
            return {'message': 'OPS. Qualcosa è andato storto.'}, 500
        return data


class Login(Resource):
    def post(self):
        data = parser.parse_args()
        # Memorizzo i dati dell'utente in una variabile
        utente_loggato = UserModel.cerca_su_db(data['username'])
        # Controllo se l'utente è presente sul DB
        if not utente_loggato:
            return {'message': '{} non esiste'.format(data['username'])}
        
        if data['password'] == utente_loggato.password:
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Hai effettuato l\'accesso come {}'.format(utente_loggato.username),
                'access_token': access_token
                }
        else:
            return {'message': 'Credenziali sbagliate'}
      
      
class ListaUtenti(Resource):
    def get(self):
        return UserModel.tutta_la_lista()

    def delete(self):
        UserModel.svuota_db()
        return {'message': 'Ripulisco il db cancellando tutti gli utenti'}
      
      
class CheckJWT(Resource):
    @jwt_required
    def get(self):
        return {
            'message': 'Sei riuscito ad accedere alla risorsa'
        }