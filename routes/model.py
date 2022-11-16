from flask import Blueprint, request, jsonify
from PIL import Image
import torch
import os
import io
model = Blueprint('model', __name__)

path = os.path.join(os.getcwd(), 'best.pt')
print("Taking model from:", path)
yolo = torch.hub.load('ultralytics/yolov5', 'custom', path=path, force_reload=True)
@model.route('/image', methods=['POST'])
def inference():
    if 'image' not in request.files:
        return jsonify({"done": False, 'message': 'There was no image for inference'})
    image = request.files['image']
    image = Image.open(io.BytesIO(image.read()))
    results = yolo(image)
    data = results.pandas().xyxy[0].to_json(orient="records")
    return data
