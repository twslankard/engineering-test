from sqlalchemy import create_engine
from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, column_property
from sqlalchemy.types import ARRAY
from sqlalchemy.sql import cast, func
from geoalchemy2.types import Geography
from geoalchemy2.functions import ST_AsGeoJSON
import os

engine = create_engine(os.environ['DB_CONNECTION_URL'], echo=True)
Base = declarative_base()


class Property(Base):
    __tablename__ = 'properties'
    id = Column(String, primary_key=True)
    geocode_geo = Column(Geography)
    parcel_geo = Column(Geography)
    building_geo = Column(Geography)
    image_bounds = Column(ARRAY(Float))
    image_url = Column(String)
    geocode_geojson = column_property(ST_AsGeoJSON(geocode_geo))

    def __repr__(self):
        return "<Property(id='{}', image_url='{}')>"\
            .format(self.id, self.image_url)


Session = sessionmaker()
Session.configure(bind=engine)


def find_property_by_id(property_id):
    session = Session()
    return session.query(Property).filter(Property.id == property_id).one()


def find_properties_near_ewkt(ewkt_string, distance_meters):
    """
    Finds all properties within `distance_meters` of the geometry
    specified by `ewkt_string`.
    """
    session = Session()
    return session.query(Property).filter(
        func.ST_DWithin(
            Property.geocode_geo,
            cast(func.ST_GeomFromEWKT(ewkt_string), Geography),
            distance_meters
        )
    ).all()


def find_properties_near_geojson(geojson_string, distance_meters):
    """
    Finds all properties within `distance_meters` of the geometry
    specified by `geojson_string`.
    """
    session = Session()
    return session.query(Property).filter(
        func.ST_DWithin(
            Property.geocode_geo,
            cast(func.ST_GeomFromGeoJSON(geojson_string), Geography),
            distance_meters
        )
    ).all()
