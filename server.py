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
def generate_new_background():
    '''
    This function pre-processes the image,
    constructs a full request and calls
    the controlnet module of AUTOMATIC1111
    
    The image and prompt are necessary arguments,
    width and height default to 512
    
    The image is b64 encoded string
    The test images were encoded like this:
    
    > from base64 import b64encode
    > with open("512.png", "rb") as img:
    --> b64 = b64encode(img.read()).decode('utf-8')
    
    
   The input request must have a JSON like this:
    {
       "prompt": textual-prompt (str),
       "width": recommended to be 512, 768 or 1024 (int),
       "height": recommended to be 512, 768 or 1024 (int),
       "image" b64-encoded-removed-background-img (str)
    }
    
    
    The output is a str representation of a JSON like this:
    {
        "images": [b64-encoded-canny-img, b64-encoded-generated-img] (list[str]),
        "parameters": (str)
        "info": (str)
    } 
    
    The output contains a list of images, where the
    first image is our Canny edge generated "map".
    The second image is generated via SD + ControlNet
    
    Both images can be retrieved by decoding them
    using b64decode
    > from base64 import b64decode
    
    '''
    
    input = request.get_json(force=True)
    image_b64 = input.get('image')
    prompt = input.get('prompt')
    
    width = funcs.set_width_height(width)
    height = funcs.set_width_height(height)
    
    img = Image.open(BytesIO(b64decode(image_b64)))
    preproc_img = funcs.create_mask(img, width, height) 
    
    buffered = BytesIO()
    preproc_img.save(buffered, "PNG")
    preproc_b64 = b64encode(buffered.getvalue()).decode('utf-8')
    
    # call controlnet API
    CNR = ControlnetRequest(
        prompt=prompt,
        width=width,
        height=height,
        b64img=preproc_b64
        )
    res = CNR.sendRequest()
    
    return res

@app.route("/blend_image", methods=["POST"])
def blend_image():
    pass

if __name__ == '__main__':
    port = 7860
    app.run(host="0.0.0.0", port=port)
