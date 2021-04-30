from app import app, cluster
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request

mongo = cluster

# {
#           "item_name": "Speaker",
#           "price" : 25.0,
#           "quantity": 3
# }


@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _item_name = _json['item_name']
    _price = _json['price']
    _quantity = _json['quantity']
    # validate the received values
    if _item_name and _price and _quantity and request.method == 'POST':
        # save details
        id = mongo.db.cart.insert_one({'item_name': _item_name, 'price': _price, 'quantity':_quantity})
        resp = jsonify('Item added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/items')
def items():
    items = mongo.db.cart.find()
    resp = dumps(items)
    return resp


@app.route('/item/<id>')
def users(id):
    item = mongo.db.cart.find_one({'_id': ObjectId(id)})
    resp = dumps(item)
    return resp


@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _json = request.json
    # _id = _json['_id']
    _item_name = _json['item_name']
    _price = _json['price']
    _quantity = _json['quantity']

    updated_item = {}
    # validate the received values
    if _item_name:
        updated_item['item_name'] = _item_name
    if _price:
        updated_item['price'] = _price
    if _quantity:
        updated_item['quantity'] = _quantity

    if  id and request.method == 'PUT':
        # save edits
        mongo.db.cart.update_one({'_id': ObjectId(id)},
                                 {'$set': updated_item})
        resp = jsonify('Item updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.cart.delete_one({'_id': ObjectId(id)})
    resp = jsonify('Item deleted successfully!')
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run()