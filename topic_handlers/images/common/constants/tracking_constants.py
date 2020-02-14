import numpy as np
import matplotlib.cm as cm

PIX_THRESHOLD = 0.6
MIN_AREA = 50
MAX_AREA = 1 * 1e3
G_BLUR = (15, 15)
COLORS = [color * 255 for color in cm.rainbow(np.linspace(0, 1, 3))]  # head, center, tail
