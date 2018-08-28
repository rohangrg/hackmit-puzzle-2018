import glob
from PIL import Image

extensions = ["png", "jpg"]

for ext in extensions:
    imgs = glob.glob("./imgs/*.{}".format(ext))
    for img_path in imgs:
        print("[i] Compressing image: {}".format(img_path))
        img = Image.open(img_path)
        width, height = img.size
        img = img.resize((width // 3, height // 3), Image.ANTIALIAS)
        img.save(img_path.replace("./imgs/", "./compressed/"), optimize=True, quality=70)

print("[i] Done.")