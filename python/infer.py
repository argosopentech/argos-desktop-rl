import pathlib

import torch
from PIL import Image

import vit
from config import *

timestamp = 1659663835
image_path = TRAINING_DATA_DIRECTORY / str(timestamp) / "screen.png"
print(image_path)
img = Image.open(image_path)
image_tensor = vit.train_transforms(img)
x = torch.zeros(1, 4, 256, 256)
x[0] = image_tensor

model = torch.load(MODEL_PATH, map_location=torch.device(vit.device))

model.eval()

res = model(x)[0]

print(res)
