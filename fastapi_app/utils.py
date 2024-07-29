import numpy as np
from PIL import Image
import io
import webcolors
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans
from skimage import io as skio

css4_colors = dict(mcolors.CSS4_COLORS)

def load_image_into_numpy_array(data):
    image = Image.open(io.BytesIO(data))
    image = image.resize((224, 224))
    return np.array(image) / 255.0

def get_center_region(image, size=100):
    h, w, _ = image.shape
    center_x, center_y = w // 2, h // 2
    half_size = size // 2
    return image[center_y - half_size:center_y + half_size, center_x - half_size:center_x + half_size]

def get_dominant_color(image_data, k=1):
    image = skio.imread(io.BytesIO(image_data))
    center_region = get_center_region(image)
    center_region = center_region.reshape((center_region.shape[0] * center_region.shape[1], 3))
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(center_region)
    dominant_color = kmeans.cluster_centers_.astype(int)[0]
    dominant_color_hex = '#{:02x}{:02x}{:02x}'.format(dominant_color[0], dominant_color[1], dominant_color[2])
    return dominant_color_hex

def closest_color(requested_color):
    min_colors = {}
    for key, name in css4_colors.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(name)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = key
    return min_colors[min(min_colors.keys())]
