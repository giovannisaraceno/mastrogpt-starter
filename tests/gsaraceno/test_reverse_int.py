import os, requests as req
def test_reverse():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/gsaraceno/reverse"
    res = req.get(url).json()
    assert res.get("output") == "Please provide a valid input"
