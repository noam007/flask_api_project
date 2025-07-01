from flask import Flask, request, jsonify , render_template
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, Item

html_data = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

# http://127.0.0.1:5000/items   127.0.0.1 - main route , 5000 - port

@app.route('/') #main route for Flask app , only 1 '/' this is the main route 127.0.0.1
def index():
    app.logger.info("Flask API is running. (Logged from index route)")

    return render_template("index.html", data = html_data)   # connection to the HTML

# @app.route('/a')  - this will be a different HTML page , 1 route can connect to a single specific HTML page
# all HTML files - on the same /template folder (standard) , CSS , JAVA script

@app.route('/item', methods=['POST']) # separate router (only for POST request) , since "http://127.0.0.1:5000/items"
# item - is a name of route, can use any name.
# POST - example of the actual API

def add_item():
    data = request.get_json()
    name = data.get('name')
    value = data.get('value')

    if not name or value is None:
        return jsonify({'error': 'Missing data'}), 400

    html_data.append((name, value))  # for FE page

    new_item = Item(name=name, value=value)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Item added', 'id': new_item.id}), 201

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item deleted', 'id': item.id}), 200



@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([
        {'id': item.id, 'name': item.name, 'value': item.value}
        for item in items
    ])

if __name__ == '__main__':

    with app.app_context():
        db.create_all()  # יוצרים את הטבלאות לפני הריצה
    app.run(host='0.0.0.0', port=5000, debug=True)