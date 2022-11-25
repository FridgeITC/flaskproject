from flask import Blueprint, request, jsonify
import json
from PIL import Image
import torch
import os
import io
from type.ModelImageRecord import ModelInferenceInsertion
model = Blueprint('model', __name__)

path = os.path.join(os.getcwd(), 'best.pt')
print("Taking model from:", path)
yolo = torch.hub.load('ultralytics/yolov5', 'custom', path=path)
# TODO: ADD DIFERENT HTTP CODES ON ERROR
@model.route('/image', methods=['POST'])
def inference():
    '''
    TODO: FINISH THE COMMENT OF THIS ENDPOINT
    Receives a json with the folowing format:
        fridgeId: The id of the fridge that is going to be populated
        image: The multipart form data of the image to run the inference on
    :return:
    JSON with and array of the detected objects and their position
    '''
    # -- Validation
    fridge_id = request.form.get('fridgeId')
    if fridge_id is None:
        return jsonify(({"done": False, 'message': 'Missing fridgeId'}))
    if 'image' not in request.files:
        return jsonify({"done": False, 'message': 'There was no image for inference'})
    image = request.files['image']
    # -- Running inference
    image = Image.open(io.BytesIO(image.read()))
    results = yolo(image)
    if not len(results):
        return jsonify({'done': False, 'message': 'No products detected'})
    # -- Inserting the results to the db
    list_dict = results.pandas().xyxy[0].to_dict('records')
    inference_model = ModelInferenceInsertion(fridge_id, list_dict)
    inference_model.insert()
    data = results.pandas().xyxy[0].to_json(orient="records")
    return data
