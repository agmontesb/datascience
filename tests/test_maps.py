import doctest
import json
import pytest
import os

import datascience as ds
from datascience import maps


@pytest.fixture(scope='function')
def states():
    """Read a map of US states."""
    mpath = os.path.abspath('./us-states.json')
    return ds.Map.read_geojson(mpath)


############
# Doctests #
############


def test_doctests():
    results = doctest.testmod(maps, optionflags=doctest.NORMALIZE_WHITESPACE)
    assert results.failed == 0


############
# Overview #
############


def test_draw_map(states):
    """ Tests that draw_map returns HTML """
    states.show()


def test_setup_map():
    """ Tests that passing kwargs doesn't error. """
    kwargs = {
        'tiles': 'Stamen Toner',
        'zoom_start': 17,
        'width': 960,
        'height': 500,
        'features': [],
    }
    ds.Map(**kwargs).show()


def test_map_marker_and_region(states):
    """ Tests that a Map can contain a Marker and/or Region. """
    marker = ds.Marker(51.514, -0.132)
    ds.Map(marker).show()
    ds.Map([marker]).show()
    region = states['CA']
    ds.Map(region).show()
    ds.Map([region]).show()
    ds.Map([marker, region]).show()


##########
# ds.Marker #
##########


def test_marker_html():
    """ Tests that a Marker can be rendered. """
    ds.Marker(51.514, -0.132).show()


def test_marker_map():
    """ Tests that Marker.map generates a map """
    lats = [51, 52, 53]
    lons = [-1, -2, -3]
    labels = ['A', 'B', 'C']
    colors = ['blue', 'red', 'green']
    ds.Marker.map(lats, lons).show()
    ds.Marker.map(lats, lons, labels).show()
    ds.Marker.map(lats, lons, labels, colors).show()
    ds.Marker.map(lats, lons, colors=colors).show()


def test_marker_map_table():
    """ Tests that Marker.map_table generates a map """
    lats = [51, 52, 53]
    lons = [-1, -2, -3]
    labels = ['A', 'B', 'C']
    t = ds.Table([lats, lons, labels], ['A', 'B', 'C'])
    ds.Marker.map_table(t).show()
    colors = ['red', 'green', 'yellow']
    t['colors'] = colors
    ds.Marker.map_table(t).show()


def test_circle_html():
    """ Tests that a Circle can be rendered. """
    ds.Circle(51.514, -0.132).show()


def test_circle_map():
    """ Tests that Circle.map generates a map """
    lats = [51, 52, 53]
    lons = [-1, -2, -3]
    labels = ['A', 'B', 'C']
    ds.Circle.map(lats, lons).show()
    ds.Circle.map(lats, lons, labels).show()


##########
# Region #
##########


def test_region_html(states):
    states['CA'].show()


def test_geojson(states):
    """ Tests that geojson returns the original US States data """
    mpath = os.path.abspath('./us-states.json')
    data = json.load(open(mpath, 'r'))
    geo = states.geojson()
    assert data == geo, '{}\n{}'.format(data, geo)


##########
# Bounds #
##########


def test_bounds():
    """ Tests that generated bounds are correct """
    points = [ds.Marker(0, 0), ds.Marker(-89.9, 180), ds.Marker(90, -180)]
    bounds = ds.Map(points)._autobounds()
    assert bounds['max_lat'] == 90
    assert bounds['min_lat'] == -89.9
    assert bounds['max_lon'] == 180
    assert bounds['min_lon'] == -180


def test_bounds_limits():
    """ Tests that too-large lats and lons are truncated to real bounds. """
    points = [ds.Marker(0, 0), ds.Marker(-190, 280), ds.Marker(190, -280)]
    bounds = ds.Map(points)._autobounds()
    assert bounds['max_lat'] == 90
    assert bounds['min_lat'] == -90
    assert bounds['max_lon'] == 180
    assert bounds['min_lon'] == -180


#########
# Color #
#########


def test_color_table(states):
    """ Tests that color can take a Table. """
    mpath = os.path.abspath('./us-unemployment.csv')
    data = ds.Table.read_table(mpath)
    states.color(data).show()


def test_color_dict(states):
    """ Tests that color can take a dict. """
    mpath = os.path.abspath('./us-unemployment.csv')
    data = ds.Table.read_table(mpath)
    states.color(dict(zip(*data.columns))).show()


def test_color_values_and_ids(states):
    """ Tests that color can take values and ids. """
    mpath = os.path.abspath('./us-unemployment.csv')
    data = ds.Table.read_table(mpath)
    states.color(data['Unemployment'], data['State']).show()
