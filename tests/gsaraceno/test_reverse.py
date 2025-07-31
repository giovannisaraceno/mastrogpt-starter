import sys 
sys.path.append("packages/gsaraceno/reverse")
import reverse

def test_reverse():
    res = reverse.reverse({input: "pollo"})
    assert res["output"] == "Please provide a valid input"
