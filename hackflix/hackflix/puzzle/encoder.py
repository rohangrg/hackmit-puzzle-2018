import imageio
import numpy as np
import qrcode
import os

ORIGINAL = imageio.get_reader(os.path.join('hackflix', 'static', 'bin', 'original.mp4'), 'ffmpeg')
FPS = ORIGINAL.get_meta_data()['fps']
FRAMES = ORIGINAL.get_meta_data()['nframes']

def to_rgb(im):
    # I would expect this to be identical to 1a
    w, h = im.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 0] = im
    ret[:, :, 1] = ret[:, :, 2] = ret[:, :, 0]
    return ret

def process_frame_wt(image, username, alpha=0.2, wt_size=128):
    username = username[:64]
    code = to_rgb(np.array(qrcode.make(username).resize((wt_size, wt_size)).convert('L')))
    
    h, w, c = image.shape
    blended = (alpha * (255 - code)).astype(np.uint8)

    image[h-10-wt_size:h-10, 10:10+wt_size] += blended
    image[h-10-wt_size:h-10, 10:10+wt_size] = np.clip(image[h-10-wt_size:h-10, 10:10+wt_size], 0, 255)

    return image

# Start and end are frames
def process_video(op, orig, username, start, end):
    writer = imageio.get_writer(op, 'ffmpeg', fps=FPS, quality=8)
    
    for image in [ORIGINAL.get_data(i) for i in range(start, end)]:
        writer.append_data(process_frame_wt(image, username))
    writer.close()

    writer = imageio.get_writer(orig, 'ffmpeg', fps=FPS, quality=8)
    
    for image in [ORIGINAL.get_data(i) for i in range(start, end)]:
        writer.append_data(image)
    writer.close()

# if __name__ == '__main__':
#     process_video(VIDEO_FILENAME, "op.mp4", "op_orig.mp4", "revalo", start=10, end=10+3*30)
