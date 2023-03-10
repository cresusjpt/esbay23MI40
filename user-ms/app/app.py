from flask import Flask
from flask import make_response, request, json, jsonify
from passlib.hash import sha256_crypt
import models

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY = 'insecure key',
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@user_db/user'
))

models.init_app(app)
models.create_tables(app)

@app.route('/users/hello')
def hello():
    return 'Hello, Welcome to the ESBay User api\n'

@app.route('/api/users/create', methods=['POST'])
def post_register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = sha256_crypt.hash((str(request.form['password'])))

    user = models.User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password = password
    user.authenticated = True

    models.db.session.add(user)
    models.db.session.commit()

    response = jsonify({
        'message': 'User added',
        'result': user.to_json()
    })

    return response

@app.route('/api/users', methods=['GET'])
def get_users():
    data = []
    for row in models.User.query.all():
        data.append(row.to_json())

    #response = jsonify(data)
    #return response

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)