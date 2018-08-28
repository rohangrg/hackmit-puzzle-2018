VIDEO_FILENAME = "bp_.mp4"

def get_pixel_array(width, height, s, b):
    x_start = width / 2 - s
    x_end = width / 2 + s

    y_start = height / 2 - s
    y_end = height / 2 + s

    step = int((x_end - x_start) / b)
    for x in xrange(x_start, x_end, step):
        for y in xrange(y_start, y_end, step):
            yield (x, y)


def get_wt_pos(width, height, wt_size):
    return (10, height - wt_size - 10)