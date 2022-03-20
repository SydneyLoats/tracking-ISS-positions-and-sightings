from app import*

import pytest

load_data()

def test_interact():
    assert isinstance(interact(), str) == True

def test_all_epochs():
    assert isinstance(all_epochs(), str) == True

def test_specific_epoch():
    assert isinstance(specific_epoch('a'), dict) == True

def test_all_countries():
    assert isinstance(all_countries(), dict) == True

def test_specific_country():
    assert isinstance(specific_country('a'), dict) == True

def test_all_regions():
    assert isinstance(all_regions('a'), dict) == True

def test_specific_region():
    assert isinstance(specific_region('a', 'b'), dict) == True

def test_all_cities():
    assert isinstance(all_cities('a', 'b'), dict) == True

def test_specific_city():
    assert isinstance(specific_city('a', 'b', 'c'), dict) == True
