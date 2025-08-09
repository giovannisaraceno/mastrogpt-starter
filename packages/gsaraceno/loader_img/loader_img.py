import os, requests as req
import vision2 as vision
import vdb

USAGE = "Please upload a picture and I will tell you what I see"
FORM = [
  {
    "label": "Load Image",
    "name": "pic",
    "required": "true",
    "type": "file"
  },
]

def loader_img(args):
  res = {}
  out = USAGE
  inp = args.get("input", "")

  if type(inp) is dict and "form" in inp:
    img = inp.get("form", {}).get("pic", "")
    print(f"uploaded size {len(img)}")
    db = vdb.VectorDB(args, "cats")
    vis = vision.Vision(args)
    description = vis.decode(img)
    out = description
    db_res = db.insert(description)
    out += "\n".join([str(x) for x in db_res.get("ids", [])])
    out += "\n"
    
    res['html'] = f'<img src="data:image/png;base64,{img}">'
    
  res['form'] = FORM
  res['output'] = out
  return res
