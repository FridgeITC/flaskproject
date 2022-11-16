from flask import Blueprint, request, jsonify
import torch
import os
model = Blueprint('model', __name__)

path = os.path.join(os.getcwd(), 'best.pt')
print("Taking model from:", path)
best = torch.hub.load('ultralytics/yolov5', 'custom', path=path, force_reload=True)
best.eval()
@model.route('/image', methods=['POST'])
def inference():
    if 'image' not in request.files:
        return jsonify({"done": False, 'message': 'There was no image for inference'})
    image = request.files['image']
    results = best(image)
    return jsonify(results)
