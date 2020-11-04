from flask_restful import Resource, request
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
)
from marshmallow import ValidationError
from models.item import ItemModel
from schimas.item import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod  # No longer needs brackets
    def get(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {"message": "Item not found."}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name):
        if ItemModel.find_by_name(name):
            return (
                {"message": "An item with name '{}' already exists.".format(name)},
                400,
            )

        item_json = request.get_json()
        item_json["name"] = name
        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item."}, 500

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required
    def delete(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}, 200
        return {"message": "Item not found."}, 404

    @classmethod
    def put(cls, name):
        item_json = request.get_json()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json["price"]
        else:
            item_json["name"] = name
            item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": [item_list_schema.dump(ItemModel.find_all())]}, 200
