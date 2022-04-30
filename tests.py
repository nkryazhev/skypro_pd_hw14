import pytest
import utils

VALID_ACTORS = ['Alice Krige', 'Honor Kneafsey']


def test_actors_pair():
    response = utils.get_actors_by_actors_pair('Rose McIver', 'Ben Lamb')
    for actor in VALID_ACTORS:
        assert actor in response
