import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
from PIL import Image
from vit_pytorch import ViT

from config import *

# Based on vit-pytorch example
# https://github.com/lucidrains/vit-pytorch/blob/main/examples/cats_and_dogs.ipynb

device = "cuda"
MODEL_FILE = 

# Training settings
batch_size = 64
epochs = 20
lr = 3e-5
gamma = 0.7
seed = 42

NUM_CLASSES = 2


def embed_class(class_str):
    if class_str == "KEY_W":
        return 0
    return 1
    """
    elif class_str == "KEY_A":
        return 1
    elif class_str == "KEY_S":
        return 2
    elif class_str == "KEY_D":
        return 3
    elif class_str == "KEY_SPACE":
        return 4
    else:
        print("Could not find class")
        return 4
    """


class FrameDataset(Dataset):
    def __init__(self, transform):
        self.transform = transform
        self.frame_dirs = list(TRAINING_DATA_DIRECTORY.iterdir())

    def __len__(self):
        return len(self.frame_dirs)

    def __getitem__(self, idx):
        frame_dir = self.frame_dirs[idx]

        screen_path = frame_dir / "screen.png"
        img = Image.open(screen_path)
        img_transformed = self.transform(img)

        action_path = frame_dir / "action"
        actions = list()
        with open(action_path, "r") as action_file:
            actions = action_file.readlines()
        action = actions[0].strip()
        action = embed_class(action)

        return img_transformed, action


train_transforms = transforms.Compose(
    [
        transforms.Resize((256, 256)),
        transforms.RandomResizedCrop(256),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ]
)

train_data = FrameDataset(train_transforms)
train_loader = DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)

model = ViT(
    image_size=256,
    patch_size=32,
    num_classes=NUM_CLASSES,
    dim=1024,
    depth=6,
    heads=16,
    mlp_dim=2048,
    dropout=0.1,
    emb_dropout=0.1,
    channels=4,
).to(device)

# loss function
criterion = nn.CrossEntropyLoss()
# optimizer
optimizer = optim.Adam(model.parameters(), lr=lr)
# scheduler
scheduler = StepLR(optimizer, step_size=1, gamma=gamma)

for epoch in range(epochs):
    epoch_loss = 0
    epoch_accuracy = 0

    for data, label in train_loader:
        data = data.to(device)
        label = label.to(device)

        output = model(data)
        loss = criterion(output, label)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        acc = (output.argmax(dim=1) == label).float().mean()
        epoch_accuracy += acc / len(train_loader)
        epoch_loss += loss / len(train_loader)

    print(f"Epoch : {epoch+1} - loss : {epoch_loss:.4f} - acc: {epoch_accuracy:.4f} \n")

torch.save(model, MODEL_PATH)
