import os, requests as req
def test_loader_img():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/gsaraceno/loader_img"
    res = req.get(url).json()
    assert res.get("output") == "Please upload a picture and I will tell you what I see"
