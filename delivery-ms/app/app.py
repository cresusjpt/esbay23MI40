from flask import Flask
from flask import jsonify, request, json
import models

app = Flask(__name__)

app.config.update(
    dict(
        SECRET_KEY="insecure key for delivery",
        SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root:test@delivery_db/delivery",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
)

models.init_app(app)
models.create_tables(app)

@app.route("/deliveries/hello")
def hello():
    return "Hello, welcome to the ESBay Deliveries app\n"

# seller submit delivery informations and an evaluation of the winner buyer
@app.route("/api/deliveries/create", methods=["POST"])
def post_delivery_create():
    product = request.form["product"]
    buyer = request.form["buyer"]
    tracking_code = request.form["tracking_code"]
    winner_eval = request.form["winner_evaluation"]
    date_sended = request.form["date_sended"]

    delivery = models.Delivery()
    delivery.product = product
    delivery.buyer = buyer
    delivery.tracking_code = tracking_code
    delivery.winner_evaluation = winner_eval
    delivery.date_sended = date_sended
    delivery.received = False

    models.db.session.add(delivery)
    models.db.session.commit()

    return (
        jsonify(
            {
                "message": "Delivery information subitted",
                "status_code": 200,
                "delivery": delivery.to_json(),
            }
        ),
        201,
    )

# list all the deliveries
@app.route("/api/deliveries")
def get_deliveries():
    data = []
    for row in models.Delivery.query.all():
        data.append(row.to_json())

    return jsonify({"status_code": 200, "results": data})


# get one delivery by id
@app.route("/api/deliveries/<int:id>")
def get_delivery(id):
    delivery = models.Delivery()
    delivery.id = id
    row = models.Delivery.query.get(id)

    return jsonify({"results": row.to_json()})


# update the delivery with the submission of the winner buyer evaluation and the receiption date
@app.route("/api/deliveries/<int:id>/receive", methods=["PUT"])
def post_receipt_create(id):
    if not request.json:
        return {"result": "not a json"}
    delivery = models.Delivery.query.get(id)
    date_received = request.json.get("date_received", delivery.date_received)
    sender_evaluation = request.json.get(
        "sender_evaluation", delivery.sender_evaluation
    )

    delivery.date_received = date_received
    delivery.sender_evaluation = sender_evaluation
    delivery.received = True

    models.db.session.commit()
    process_ended = update_delivery_state(id)

    return (
        jsonify(
            {
                "message": "Delivery information submitted",
                "status_code": 200,
                "delivery": delivery.to_json(),
            }
        ),
        200,
    )

#close delivery process when evaluations and receiption date added
def update_delivery_state(id:int)->bool:
    delivery = models.Delivery.query.get(id)
    if not delivery.sender_evaluation and not delivery.winner_evaluation and not delivery.date_sended and not delivery.date_received:
        delivery.received = True
        models.db.session.add(delivery)
        models.db.session.commit()
        return True
    return False

@app.route('/api/delivery/<int:id>/check/status')
def check_status(id:int):
    delivery = models.Delivery.query.get(id)
    return {
        'id': delivery.id,
        'date_sended': delivery.date_sended,
        'received': delivery.received
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
