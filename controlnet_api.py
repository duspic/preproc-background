import requests
from base64 import b64encode
from io import BytesIO
from PIL import Image
import json

def readImage(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="png")
    img_str = b64encode(buffered.getvalue())
    return img_str.decode('utf-8')
    

class ControlnetRequest():
    def __init__(self, prompt, size, b64img):
        self.b64img = b64img
        self.url = "http://automatic:7861/sdapi/v1/txt2img"
        self.body = {
            "prompt": f"RAW photo, {prompt}, product photography, highres, extremely detailed, best quality,  8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3",
            "negative_prompt": "poorly drawn, lowres, bad quality, worst quality, (unrealistic), (overexposed:1.3), (underexposed), (floating:1.4), (blurry background:1.3)",
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "batch_size": 1,
            "n_iter": 1,
            "steps": 30,
            "cfg_scale": 7,
            "width": size,
            "height": size,
            "restore_faces": False,
            "eta": 0,
            "sampler_index": "Euler a",
            "alwayson_scripts":{
                "controlnet":{
                    "args":[{
                        "input_image": b64img,
                        "module": 'canny',
                        "model": 'control_canny-fp16 [e3fe7712]',
                        "weight": 1.9,
                        "guidance": 2.0,
                        "processor_res": 512
                        }]
                }
            }
        }

    def sendRequest(self):
        r = requests.post(self.url, json=self.body)
        j = r.json()
        j['input_cn_img'] = self.b64img
        return json.dumps(j)