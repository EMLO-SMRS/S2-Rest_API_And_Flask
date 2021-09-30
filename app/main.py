from flask import Flask, jsonify, request, render_template
from app.torch_utils import transform_image, get_prediction
from werkzeug.utils import secure_filename
from PIL import Image
import copy
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.files['file'])
        file = request.files.get('file')

        
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})

        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], filename))
            print(f"file saved {filename}")
            file = open(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], filename), 'rb')
            img_bytes = file.read()
            tensor = transform_image(img_bytes)
            prediction = get_prediction(tensor)
            class_name = class_names[int(prediction.item())]
            data = {'prediction': prediction.item(), 'class_name': class_name}
            return render_template("home.html", filename = f"{filename}", prediction = class_name)
        except Exception as e:
            print(e )
            return jsonify({'error': 'error during prediction'})
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
    pass

if __name__ == "__main__":
    app.run(debug=True)
