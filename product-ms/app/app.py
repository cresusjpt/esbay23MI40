from flask import Flask
from flask import make_response, jsonify, request, json
import models

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY = 'insecure key for product',
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:test@product_db/product',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
))

models.init_app(app=app)
models.create_tables(app=app)

@app.route('/products/hello')
def hello():
    return 'Hello, welcome to the ESBay Product API\n'

@app.route('/api/products/create', methods=['POST'])
def post_create():
    name = request.form['name']
    seller = request.form['seller']
    price = request.form['price']

    item = models.Product()
    item.name = name
    item.seller = seller
    item.price = price

    models.db.session.add(item)
    models.db.session.commit()

    response = jsonify({
        'message': 'Product added',
        'product': item.to_json()
    })

    return response

@app.route('/api/products')
def get_products():
    data = []
    for row in models.Product.query.all():
        data.append(row.to_json())

    response = jsonify({
        'results': data
    })

    return response
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)