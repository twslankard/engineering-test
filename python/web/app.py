from flask import Flask, Response, request
import property_service
import requests
import io
import json
import redis
from PIL import Image


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


@app.route('/display/<property_id>')
def display(property_id):
    """
    Given a property ID, return the image located at the property's image_url,
    optionally transcoding the image to the format specified by the
    "image_format" request parameter. Transcoding is useful because most
    browsers do not have native TIFF support.

    TOOO:
    * Handle error conditions
        (e.g. property not found / invalid image_format param.)
    * Caching would be necessary to make this scalable and performant.
    * Streaming would also speed up native TIFF downloads.
    """
    valid_formats = ['tiff', 'png', 'jpeg']
    the_property = property_service.find_property_by_id(property_id)
    image_format = request.args.get('image_format', 'tiff')

    if not the_property:
        return 'Not Found', 404

    if image_format not in valid_formats:
        return 'image_format should be one of {}'.format(valid_formats), 400

    mimetype = 'image/{}'.format(image_format)
    image_cache_key = '{}-{}'.format(the_property.id, image_format)
    cached_image = cache.get(image_cache_key)

    if cached_image:
        return Response(cached_image, mimetype=mimetype)

    image_response = requests.get(the_property.image_url)
    if image_format != 'tiff':
        image = Image.open(io.BytesIO(image_response.content))
        output_buffer = io.BytesIO()
        image.save(output_buffer, image_format)
        response_bytes = output_buffer.getvalue()
    else:
        response_bytes = image_response.content

    cache.set(image_cache_key, response_bytes)
    return Response(response_bytes, mimetype=mimetype)


@app.route('/find')
def find():
    """
    Given a GeoJSON request body, and an optional search_distance in meters,
    return a JSON list of property IDs.

    TODO:
    * Handle error conditions
    (e.g. invalid geojson_string, invalid search_distance.
    """
    search_distance = request.args.get('search_distance')
    geojson_string = request.get_data().decode('utf8')
    properties = property_service.find_properties_near_geojson(
        geojson_string, float(search_distance)
    )
    return Response(
        json.dumps([p.id for p in properties], indent=4),
        mimetype="application/json"
    )
