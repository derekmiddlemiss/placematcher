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
        
### Test basic features

def test_small_dist(matcher_nousefirst_nothresh):
    assert matcher_nousefirst_nothresh.match("Brogadoon") == "Brigadoon"
    
def test_large_dist(matcher_nousefirst_nothresh):
    assert matcher_nousefirst_nothresh.match("Brogandine") == "Brigadoon"
    
def test_strips_whitespace_start_end_ref_and_tomatch(matcher_nousefirst_nothresh):
    assert matcher_nousefirst_nothresh.match("   Arbroath  ") == "Arbroath"

def test_case_equal_dist_returns_unknown(matcher_nousefirst_nothresh):
    assert matcher_nousefirst_nothresh.match("Panicuik") == "Unknown"
    assert matcher_nousefirst_nothresh.match("Panicook") == "Unknown"
    
def test_deals_with_accented_letters(matcher_nousefirst_nothresh, 
                                     matcher_usefirst_nothresh):
    assert matcher_nousefirst_nothresh.match("Eirisgeigh") == "Èirisgeigh"
    assert matcher_usefirst_nothresh.match("Eirisgeigh") == "Unknown"
        
### Test use_first argument

def test_usefirst_works(matcher_usefirst_nothresh):
    assert matcher_usefirst_nothresh.match("Brogadon") == "Brigadoon"

def test_usefirst_no_match_diff_first(matcher_usefirst_nothresh):
    assert matcher_usefirst_nothresh.match("Crigadoon") == "Unknown"
    
def test_nousefirst_match_diff_first(matcher_nousefirst_nothresh):
    assert matcher_nousefirst_nothresh.match("Crigadoon") == "Brigadoon"
    
def test_usefirst_ignores_puntuation(matcher_usefirst_nothresh):
    assert matcher_usefirst_nothresh.match("Sconnay") == "'Sconny"
    
