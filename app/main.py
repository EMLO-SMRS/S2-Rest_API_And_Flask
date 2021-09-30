from flask import Flask, jsonify, request, render_template
from torch_utils import transform_image, get_prediction
from werkzeug.utils import secure_filename
from PIL import Image
import copy
import os

app = Flask(__name__)

APP_ROOT = f"{os.path.dirname(os.path.abspath(__file__))}/static"
app.config['UPLOAD_FOLDER'] = APP_ROOT

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get("clear"):
            return render_template("home.html")
        file = request.files.get('file')
    
        
        if file is None or file.filename == "":
            return render_template("home.html", error = "No File uploaded.")
        if not allowed_file(file.filename):
            return render_template("home.html", error = "Only png, jpg and jpeg file formats are supported.")

        try:
            
            filename = secure_filename(file.filename)
            if not os.path.isdir(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(f"file saved {filename}")
            file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')
            img_bytes = file.read()
            tensor = transform_image(img_bytes)
            prediction = get_prediction(tensor)
            class_name = class_names[int(prediction.item())]
            data = {'prediction': prediction.item(), 'class_name': class_name}
            return render_template("home.html", filename = f"{filename}", prediction = class_name)
        except Exception as e:
            error = "Error in the process"
            return render_template("home.html", error = "Some Error in the process.")
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
    pass

if __name__ == "__main__":
    app.run(debug=True)
