import pytest
from place_matcher import PlaceMatcher
from pandas import DataFrame

@pytest.fixture
def places_list():
    return [" Abercrombie", "Arbroath  ", "Bo'ness", "Brigadoon", "Dullerton", "Perth", 
          "Penicuik", "Ponicuik", "Glasgow", "Galashiels", "'Sconny", "Èirisgeigh"]

@pytest.fixture
def single_place():
    return "Brigadoon"

@pytest.fixture
def places_dict(places_list):
    return {"name": places_list}

@pytest.fixture
def places_dict_single():
    return {"name": "Brigadoon"}

@pytest.fixture
def places_df(places_list):
    return DataFrame({"name": places_list})

@pytest.fixture
def places_df_single(places_list):
    return DataFrame({"name": ["Brigadoon"]})

@pytest.fixture
def places_dict_wrong_key(places_list):
    return {"names": places_list}

@pytest.fixture
def places_df_wrong_key(places_dict_wrong_key):
    return DataFrame(places_dict_wrong_key)

@pytest.fixture
def matcher_usefirst_nothresh(places_df):
    return PlaceMatcher(places_df, use_first=True, unknown_thresh=None)

@pytest.fixture
def matcher_nousefirst_nothresh(places_df):
    return PlaceMatcher(places_df, use_first=False, unknown_thresh=None)

### Error free initialisations

def test_init_with_list(places_list):
    PlaceMatcher(places_list)
    
def test_init_with_single(single_place):
    PlaceMatcher(single_place)
    
def test_init_with_dict(places_dict):
    PlaceMatcher(places_dict)
    
def test_init_with_dict_single(places_dict_single):
    PlaceMatcher(places_dict_single)
    
def test_init_with_df(places_df):
    PlaceMatcher(places_df)
    
def test_init_with_df_single(places_df_single):
    PlaceMatcher(places_df_single)
    
### Initialisations that raise exceptions

def test_init_with_dict_wrong_key_raises_keyerror(places_dict_wrong_key):
    with pytest.raises(KeyError):
        PlaceMatcher(places_dict_wrong_key)
        
def test_init_with_df_wrong_key_raises_keyerror(places_df_wrong_key):
    with pytest.raises(KeyError):
        PlaceMatcher(places_df_wrong_key)
        
### 

def test_use_first_works(matcher_usefirst_nothresh):
    assert matcher_usefirst_nothresh.match("Brogadon") == "Brigadoon"

def test_use_first_no_match_diff_first(matcher_usefirst_nothresh):
    assert matcher_usefirst_nothresh.match("Crigadoon") == "Unknown"