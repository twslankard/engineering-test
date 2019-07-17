import property_service


def test_find_property_by_id():
    property_id = 'f1650f2a99824f349643ad234abff6a2'
    the_property = property_service.find_property_by_id(property_id)
    assert the_property.image_url \
        == 'https://storage.googleapis.com/engineering-test/images/{}.tif'\
        .format(property_id)


def test_find_properties_near_ewkt():
    properties = property_service.find_properties_near_ewkt(
        'SRID=4326;POINT(-73.748751 40.9185483)',
        0.1
    )
    assert properties[0].id == 'f1650f2a99824f349643ad234abff6a2'


def test_find_properties_near_geojson():
    properties = property_service.find_properties_near_geojson(
        '{ "type": "Point", "coordinates": [-73.748751, 40.9185483] }',
        0.1
    )
    assert properties[0].id == 'f1650f2a99824f349643ad234abff6a2'

    # show that the property isn't near an entirely different point
    properties = property_service.find_properties_near_geojson(
        '{ "type": "Point", "coordinates": [-122.1, 37.1] }',
        0.1
    )
    assert not properties
