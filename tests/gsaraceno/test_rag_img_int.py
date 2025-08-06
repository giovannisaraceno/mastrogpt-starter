import os, requests as req
def test_rag_img():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/gsaraceno/rag_img"
    res = req.get(url).json()
    assert res.get("output") == "rag_img"
