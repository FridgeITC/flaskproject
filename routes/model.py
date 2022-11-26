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
    """
      Makes the inference on the passed image and inserts the inference to the DB given a fridgeId
      ---
      tags:
        - image
      security:
      - JWT: ['Authorization']
      consumes:
        - multipart/form-data
      parameters:
        - in: formData
          name: image
          type: file
          description: The image for model inference
        - in: formData
          name: fridgeId
          type: int
          description: The id of the fridge from where the foto was taken
      responses:
        200:
          description: The list of the detected objects and their coordinates
          schema:
            type: array
            items:
              type: object
              properties:
                class:
                  type: integer
                  example: 6
                xmin:
                  type: number
                  example: 52.1234567890
                ymin:
                  type: number
                  example: 585.1234567890
                xmax:
                  type: number
                  example: 1234.1234567890
                ymax:
                  type: number
                  example: 1234.1234567890
                confidence:
                  type: number
                  example: 0.93
                name:
                  type: string
                  example: 'coca_cola_light_botella_355ml'
    """
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
