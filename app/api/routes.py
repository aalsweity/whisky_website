from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Whisky, whisky_schema, whiskys_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'whisky brand': 'jack daniels',
            'whisky flavor': 'black tennessee',
            'whisky age' : '83',
            'whisky image' : 'https://images.gopuff.com/resize/cf/version=1_2%2cformat=auto%2cfit=scale-down%2cquality=70%2cwidth=650%2cheight=650/https://images.gopuff.com/blob/gopuffcatalogstorageprod/catalog-images-container/resize/cf/version=1_2%2cformat=auto%2cfit=scale-down%2cwidth=800%2cheight=800/937f8ca7-6f1f-4278-afae-49cd64e088b9.png'
            }
    
@api.route('/inventory', methods = ['POST'])
@token_required
def create_whisky(current_user_token):
    whisky_brand = request.json['whisky brand']
    whisky_flavor = request.json['whisky flavor']
    whisky_age = request.json['whisky age']
    whisky_image = request.json['whisky image']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    whisky = Whisky(whisky_brand, whisky_flavor, whisky_age, whisky_image, user_token = user_token )

    db.session.add(whisky)
    db.session.commit()

    response = whisky_schema.dump(whisky)
    return jsonify(response)

@api.route('/inventory', methods = ['GET'])
@token_required
def get_whisky(current_user_token):
    a_user = current_user_token.token
    whiskys = Whisky.query.filter_by(user_token = a_user).all()
    response = whiskys_schema.dump(whiskys)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['GET'])
@token_required
def get_single_whisky(current_user_token, id):
    whisky = Whisky.query.get(id)
    response = whisky_schema.dump(whisky)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['POST','PUT'])
@token_required
def update_whisky(current_user_token,id):
    whisky = Whisky.query.get(id) 
    whisky.whisky_brand = request.json['whisky brand']
    whisky.whisky_flavor = request.json['whisky flavor']
    whisky.whisky_age = request.json['whisky age']
    whisky.whisky_image = request.json['whisky image']
    whisky.user_token = current_user_token.token

    db.session.commit()
    response = whisky_schema.dump(whisky)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_whisky(current_user_token, id):
    whisky = Whisky.query.get(id)
    db.session.delete(whisky)
    db.session.commit()
    response = whisky_schema.dump(whisky)
    return jsonify(response)