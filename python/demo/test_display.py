import requests
from PIL import Image
import io

property_id = 'f1650f2a99824f349643ad234abff6a2'
response = requests.get(
    'http://localhost:5000/display/{}?image_format=jpeg'.format(property_id)
)
Image.open(io.BytesIO(response.content)).show()
