from flask import Blueprint, request, jsonify

model = Blueprint('model', __name__)


@model.route('/image', methods=['POST'])
def inference():
    if 'image' not in request.files:
        return jsonify({"done": False, 'message': 'There was no image for inference'})
    image = request.files['image']
    print(image)
    return []
