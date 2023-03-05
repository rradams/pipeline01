"""
Utilities for use with pyproj Transformers to make it easier to transform
GeoJSON geometries.
"""

import pyproj


def transform_coordinates(
    transformer: pyproj.Transformer,
    coordinates: list | tuple,
    geometry_type: str,
) -> list | tuple:
    """
    Transform the coordinates to a new coordinate system using the transformer.
    See https://www.rfc-editor.org/rfc/rfc7946#section-3.1.1 for definitions of
    terms.
    """
    if geometry_type == "Point":
        # For Point, the coordinates are a single position
        #
        # Pyproj transform returns a tuple.
        return transformer.transform(*coordinates)

    elif geometry_type in ("MultiPoint", "LineString"):
        # For MultiPoint and LineString, the coordinates are a list of points
        # (explicitly 2 or more for LineString, but we don't check that here)
        #
        # Pyproj can transform a list of points in one go if you give it the x
        # coords and y coords as separate lists, so we use zip to split the
        # list of points into two lists of x and y coords, transform them, and
        # then zip them back together again.
        return list(zip(*transformer.transform(*zip(*coordinates))))

    elif geometry_type in ("MultiLineString", "Polygon"):
        # For MultiLineString, the coordinates are a list of lines. For Polygon
        # the coordinates are a list of rings. Technically a ring is explicitly
        # a closed line string (i.e. the first and last points are the same),
        # but we don't check that here.
        return [
            transform_coordinates(transformer, line_or_ring, "LineString")
            for line_or_ring in coordinates
        ]

    elif geometry_type == "MultiPolygon":
        # For MultiPolygon, the coordinates are a list of polygons.
        return [
            transform_coordinates(transformer, polygon, "Polygon")
            for polygon in coordinates
        ]

    else:
        raise ValueError(f"Geometry type {geometry_type} not supported")


def transform_geometry(
    transformer: pyproj.Transformer,
    geometry: dict,
    in_place: bool = False,
) -> dict:
    """
    Transform the geometry to a new coordinate system using the transformer.
    """
    if geometry["type"] == "GeometryCollection":
        new_geometries = [
            transform_geometry(transformer, geometry)
            for geometry in geometry["geometries"]
        ]
        if in_place:
            geometry["geometries"] = new_geometries
            return geometry
        else:
            return {
                "type": "GeometryCollection",
                "geometries": new_geometries,
            }

    else:
        new_coordinates = transform_coordinates(
            transformer, geometry["coordinates"], geometry["type"]
        )
        if in_place:
            geometry["coordinates"] = new_coordinates
            return geometry
        else:
            return {
                "type": geometry["type"],
                "coordinates": new_coordinates,
            }
