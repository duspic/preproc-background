from flask import Flask, request
from base64 import b64decode, b64encode
from io import BytesIO
from PIL import Image


# local import
import funcs
from controlnet_api import ControlnetRequest

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index page'

@app.route("/generate_new_background", methods=["POST"])
def preproc_for_controlnet():
    
    input = request.get_json(force=True)
    image_b64 = input.get('image')
    size = int(input.get('size'))
    prompt = input.get('prompt')
    
    img = Image.open(BytesIO(b64decode(image_b64)))
    preproc_img = funcs.create_mask(img, size) 
    
    buffered = BytesIO()
    preproc_img.save(buffered, "PNG")
    preproc_b64 = b64encode(buffered.getvalue()).decode('utf-8')
    
    # call controlnet API
    CNR = ControlnetRequest(prompt, size, preproc_b64)
    res = CNR.sendRequest()
    
    gen_imgs = res.get('images')
    for i,img in enumerate(gen_imgs):
        Image.open(BytesIO(b64decode(image_b64))).save(f"img_{i}.png")
    return res


if __name__ == '__main__':
    port = 7860
    app.run(host="0.0.0.0", port=port)
