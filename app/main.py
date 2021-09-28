from flask import Flask, jsonify, request, render_template
from app.torch_utils import transform_image, get_prediction

app = Flask(__name__)


class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        print(request.files['file'])
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})

        try:
            img_bytes = file.read()
            tensor = transform_image(img_bytes)
            prediction = get_prediction(tensor)
            class_name = class_names[int(prediction.item())]
            data = {'prediction': prediction.item(), 'class_name': class_name}
            return jsonify(data)
        except Exception:
            return jsonify({'error': 'error during prediction'})
