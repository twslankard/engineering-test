# zesty.ai engineering test response
# Tom Slankard <twslankard@protonmail.com>

## Features implemented

I implemented the `display` and `find` methods, plus a couple of other random features:

- **Image transcoding:** most browsers lack native TIFF support. I added the ability to convert the images to jpeg and png using Pillow to premit viewing the images in the browser.
- **Image caching:** downloading a TIFF and converting it is slow. I use Redis to speed up downloading a previously-requested image.

## Dependencies

You will need to install docker and docker-compose to run database for the example.

## Building & running

Run

    docker-compose build && docker-compose up

## Running integration tests

There are some integration tests located in `python/web/integration_tests.py`. To run them,

    docker-compose build test && docker-compose run test

## Trying out the API

Run the demo clients in the `python/demo` directory:

    python python/demo/test_find.py
    python python/demo/test_display.py

Note, `test_display.py` requires the Pillow module.

## TODO

* Ensure proper sqlalchemy session management is taking place, perhaps by integrating flask-sqlalchemy.

## Known issues

* The tests may fail if the postgres image hasn't been built previously.
* TIFF downloading is slow because it doesn't stream the data from Google Cloud to the client.
