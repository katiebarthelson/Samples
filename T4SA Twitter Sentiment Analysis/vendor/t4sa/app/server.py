import logging
from flask import Flask, request
import numpy as np
import cv2
import json
from models.model import get_model, model_inference

logger = logging.getLogger(__name__)

app = Flask(__name__)

model = get_model()


@app.route('/', methods=['POST'])
def index():
    try:
        try:
            array = np.fromstring(request.data, np.uint8)
            image = cv2.imdecode(array, cv2.IMREAD_COLOR)
            return json.dumps(model_inference(model, image))
        except Exception as e:
            logger.error("Error handling request {}".format(e))
            return Response(status=500)
    except Exception as e:
        logger.error(str(e))
