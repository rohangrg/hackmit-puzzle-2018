import glob
from PIL import Image
import base64

imgs_encoded = []

extensions = ["png", "jpg"]
for ext in extensions:
    imgs = glob.glob("./compressed/*.{}".format(ext))

    for img in imgs:
        with open(img, "rb") as f:
            img_data = f.read()
            img_b64 = base64.b64encode(img_data)
            img_encoded = "data:image/{};base64,{}".format(ext, img_b64)
            imgs_encoded.append(img_encoded)

template_head = """
const imgs = {
"""

template_tail = """
}

module.exports = imgs
"""

imgs_encoded_str = ""

for ix, img_enc in enumerate(imgs_encoded):
    img_enc_str = "{}: '{}',\n".format(ix, img_enc)
    imgs_encoded_str += img_enc_str


with open("images.js", "w") as f:
    f.write("{}{}{}".format(template_head, imgs_encoded_str, template_tail))