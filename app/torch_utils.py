import io
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision
from PIL import Image


num_classes = 10
PATH = "app/cifar10_resnet18.pth"


device = torch.device('cpu')
model = torchvision.models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, num_classes)
model.load_state_dict(torch.load(PATH, map_location=device))
model.eval()


def transform_image(image_bytes):
    transform = transforms.Compose([
                                    transforms.Resize((32, 32)),
                                    transforms.ToTensor(),
                                    transforms.Normalize((0.5,), (0.5,))])

    image = Image.open(io.BytesIO(image_bytes))
    return transform(image).unsqueeze(0)


def get_prediction(image_tensor):
    outputs = model(image_tensor)
    _, predicted = torch.max(outputs.data, 1)
    return predicted
