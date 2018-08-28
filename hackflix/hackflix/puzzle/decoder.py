import imageio
import numpy as np
import zbar
import cv2
import random
from PIL import Image
from skimage.measure import compare_ssim as ssim
import os
from hackflix.config import PASS_THRESHOLD
from hackflix.utils import username_answer

scanner = zbar.Scanner()

def scan_qr(img):
    results = scanner.scan(img)
    if len(results) == 0:
        return "NULL"
    else:
        return results[0].data.decode('utf-8')

def get_qr(original, vid, idx):
    f1 = vid.get_data(idx)
    f1_o = original.get_data(idx)

    # Attempt to extract code.
    xtract = np.clip(f1 - f1_o, 0, 255)
    xtract[xtract>10] = 255
    xtract[xtract<=10] = 0
    xtract = 255 - xtract

    f = np.dot(xtract[...,:3], [0.299, 0.587, 0.114])

    return scan_qr(cv2.dilate(np.where(f>10, 255, 0).astype(np.uint8), np.ones((2,2),np.uint8)))

def generate_result(message, sender="Revalo"):
    return {
        'message': message,
        'sender': sender
    }

def crop(frame):
    return frame[:, :400]

def rcrop(frame):
    return frame[:, 400:]

def attempt_decode(original, vid, username, seed=None, tries=5):
    try:
        vid = imageio.get_reader(vid, 'ffmpeg')
    except Exception as e:
        print("DECODE ERROR %s" % str(e))
        return generate_result("Could not decode video")

    if not os.path.exists(original):
        vid.close()
        return generate_result("Are you sure this is the right video?")
    
    original = imageio.get_reader(original, 'ffmpeg')

    # Sanity check.
    f1 = vid.get_data(0)
    f1_o = original.get_data(0)

    if f1.shape != f1_o.shape:
        original.close()
        vid.close()
        return generate_result("This isn't the same dimensions")

    if vid._meta['nframes'] != original._meta['nframes']:
        return generate_result("This isn't the same duration")

    frames = vid._meta['nframes']

    ssims = []
    sanity_ssims = []

    if seed:
        random.seed(seed)

    for _ in range(tries):
        frame = random.randrange(frames)
        detection = get_qr(original, vid, frame)

        if detection == "NULL":
            f1 = vid.get_data(frame)
            f1_o = original.get_data(frame)
            ssims.append(ssim(crop(f1), crop(f1_o), data_range=255, multichannel=True))
            sanity_ssims.append(ssim(rcrop(f1), rcrop(f1_o), data_range=255, multichannel=True))
        else:
            original.close()
            vid.close()
            return generate_result("""
            We noticed you uploaded a stolen clip from our website. Our forensic team has traced
            the user back to the username <b>%s</b>. We have removed the file
            but this message serves as a warning.""" % detection, sender="Hackflix Copyright Lawyer")

    original.close()
    vid.close()

    sanity_score = np.min(sanity_ssims)
    score = np.min(ssims)

    print("Username: %s, Sanity: %f, Verify: %f" % (
        username,
        sanity_score,
        score
    ))

    if sanity_score >= 0.97 and score >= 0.965:
        return generate_result("Yo, this clip is awesome. As promised here is a HackMIT puzzle answer: <b> %s </b>" % username_answer(username))
    elif np.min(ssims) <= 0.4:
        return generate_result("This doesn't look anything like the original.")
    else:
        return generate_result("Bruh, the file isn't a clean rip, it still has artifacts / watermarks.")

if __name__ == '__main__':
    print(attempt_decode("op_orig.mp4", "op.mp4"))
