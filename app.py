from flask import Flask, request, jsonify
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

@app.route('/')
def index():
    return "Flask API is running."

@app.route('/item', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('name')
    value = data.get('value')

    if not name or value is None:
        return jsonify({'error': 'Missing data'}), 400

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
    app.run(debug=True)