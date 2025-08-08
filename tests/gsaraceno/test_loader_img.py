import sys 
sys.path.append("packages/gsaraceno/loader_img")
import loader_img

def test_loader_img():
    res = loader_img.loader_img({})
    assert res["output"] == "loader_img"
