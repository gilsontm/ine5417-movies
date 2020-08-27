import requests
import PIL.Image
import PIL.ImageTk
from io import BytesIO
from utils import image_sizes

def get_image_or_default(path, size=image_sizes.POSTER_W185):
    try:
        url = f"https://image.tmdb.org/t/p/{size}{path}"
        response = requests.get(url)
        data = BytesIO(response.content)
        image = PIL.Image.open(data)
        photo = PIL.ImageTk.PhotoImage(image)
    except:
        photo = get_default_image(size=size)
    return photo

def get_default_image(size=image_sizes.POSTER_W185):
    path = f"src/default_{size}.jpg"
    image = PIL.Image.open(path)
    photo = PIL.ImageTk.PhotoImage(image)
    return photo
