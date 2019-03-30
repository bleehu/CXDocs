import pytest
from ..server.characters import feats


def test_feat_class():
    expected_tuple = ("4", "test feat", "[]", "This is a test feat", "Travis Test", \
        "timestamp", "True", "0")
    myFeat = feats.Feat(expected_tuple)
    assert myFeat.name == "test feat"
    assert myFeat.nanite_cost == 0
    assert myFeat.pk_id == 4