from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda item: item["name"] == name, items), None)
        if not item:
            return ({"message": "no such item"}, 404)
        else:
            return item

    def post(self, name):
        if next(filter(lambda item: item["name"] == name, items), None) is not None:
            return ({"message": f'Item with name "{name}" already exists'}, 400)

        request_data = request.get_json(silent=True)
        item = {"name": name, "price": request_data["price"]}
        items.append(item)
        return (item, 201)


class ItemList(Resource):
    def get(self):
        return items


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

# stores = [{"name": "My Store", "items": [{"name": "My Item", "price": 15.99}]}]


# @app.route("/")
# def home():
#     return ({"hello": "world!"}, 200)


# @app.route("/store", methods=["POST"])
# def create_store():
#     request_data = request.get_json()
#     new_store = {"name": request_data["name"], "items": []}

#     stores.append(new_store)
#     return (jsonify(new_store), 201)


# @app.route("/store/<string:name>")
# def get_store_by_name(name: str):
#     for store in stores:
#         if store["name"] == name:
#             return store
#     return ({"message": "store not found"}, 404)


# @app.route("/store", methods=["GET"])
# def get_all_stores():
#     return jsonify(stores)


# @app.route("/store/<string:name>/item", methods=["POST"])
# def create_store_item(name: str):
#     request_data = request.get_json()
#     for store in stores:
#         if store["name"] == name:
#             store["items"].append(request_data)
#             return jsonify(store["items"])
#     return ({"message": "store not found"}, 404)


# @app.route("/store/<string:name>/item", methods=["GET"])
# def get_store_items(name: str):
#     for store in stores:
#         if store["name"] == name:
#             return jsonify(store["items"])
#     return ({"message": "store not found"}, 404)


app.run(port=5000, debug=True)
