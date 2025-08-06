import sys 
sys.path.append("packages/gsaraceno/rag_img")
import rag_img

def test_rag_img():
    res = rag_img.rag_img({})
    assert res["output"] == "rag_img"
