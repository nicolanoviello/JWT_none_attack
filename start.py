from flask import jsonify
from flask import Flask
from flask_restful import Api

# --- Token da commentare ---
"""
jwt_app = Flask(__name__)
jwt_api = Api(jwt_app)
"""

from flask_sqlalchemy import SQLAlchemy

# Definisco i miei parametri di environment per il db e per la secret
jwt_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jwt_app.db'
jwt_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt_app.config['SECRET_KEY'] = 'abc'


# Instanzio il db
db = SQLAlchemy(jwt_app)


# Inizializzo il db prima di eseguire qualsiasi altra cosa

# --- Token da commentare ---
"""
@jwt_app.before_first_request
"""

def create_tables():
    db.create_all()

# --- Token da commentare ---
"""
# Inizializzo JWT
from flask_jwt_extended import JWTManager
jwt_app.config['JWT_SECRET_KEY'] = 'abc'
jwt = JWTManager(jwt_app)



@jwt.user_claims_loader
def add_claims_to_access_token(user):
    ruolo_check = models.UserModel.cerca_su_db(user)
    if  ruolo_check.ruolo == 'abcde':
        return {'ruolo': 'root'}
    elif ruolo_check.ruolo == 'root':
        return {'ruolo': 'fake_root'}
"""

import models, resources



# Mappo le risorse su specifici endpoint
jwt_api.add_resource(resources.Registration, '/registration')
jwt_api.add_resource(resources.Login, '/login')
jwt_api.add_resource(resources.ListaUtenti, '/users')
jwt_api.add_resource(resources.CheckJWT, '/scopriruolo')




