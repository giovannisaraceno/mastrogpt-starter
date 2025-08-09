import os, requests as req

def test_rag_img():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/gsaraceno/rag_img"
    res = req.get(url).json()
    assert res.get("output") == "Your query is then passed to the LLM with the sentences for an answer."
    args = { "input": "Gary Sinise"}
    res = req.post(url, json=args).json()
    assert "Gary Sinise" in res.get("output")