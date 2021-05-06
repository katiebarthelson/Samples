import os
import cv2
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as t
from models.alexnet import KitModel as AlexNet
from models.vgg19 import KitModel as VGG19


def transform(image):
    _transform = t.Compose([
        t.Resize((224, 224)),
        t.ToTensor(),
        t.Lambda(lambda x: x[[2,1,0], ...] * 255),  # RGB -> BGR and [0,1] -> [0,255]
        t.Normalize(mean=[116.8007, 121.2751, 130.4602], std=[1,1,1]),  # mean subtraction
    ])

    cv2.imwrite('image.jpg', image)

    pil_image = Image.fromarray(np.uint8(image))
    return _transform(pil_image)


def get_model():
    modelname = 'hybrid_finetuned_all'
    model = AlexNet if 'hybrid' in modelname else VGG19
    model = model('converted-models/{}.pth'.format(modelname)).to('cuda')
    model.eval()
    return model


def model_inference(model, image):
    image_transformed = transform(image)

    with torch.no_grad():
        result = model(image_transformed.to('cuda')[None, ...]).cpu().numpy()[0]

    neg, neu, pos = result
    return {
        'neg': str(neg),
        'neu': str(neu),
        'pos': str(pos)
    }
