import os
import base64
import vision
import vdb

def is_image_file(filename): 
 return filename.lower().endswith(('.jpeg'))

def encode_image_to_base64(filepath):
  with open(filepath, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

USAGE = f"""Welcome to the Vector DB Loader.
Write text to insert in the DB. 
Use `@[<coll>]` to select/create a collection and show the collections.
Use `*<string>` to vector search the <string>  in the DB.
Use `#<limit>`  to change the limit of searches.
Use `!<substr>` to remove text with `<substr>` in collection.
Use `!![<collection>]` to remove `<collection>` (default current) and switch to default.
"""

FORM = [  
  {
    "label": "Load Image",
    "name": "pic",
    "required": "true",
    "type": "file"
  },  
]

def loader(args):
  collection = "cats"
  limit = 30

  sp = args.get("state", "").split(":")
  if len(sp) > 0 and len(sp[0]) > 0:
    collection = sp[0]
  if len(sp) > 1:
    try:
      limit = int(sp[1])
    except: pass
  print(collection, limit)

  out = f"{USAGE}Current collection is {collection} with limit {limit}"
  vis = vision.Vision(args)
  db = vdb.VectorDB(args, collection)
  inp = str(args.get('input', ""))
  res = {}

  if type(inp) is dict and "form" in inp:
    img = inp.get("form", {}).get("pic", "")
    print(f"uploaded size {len(img)}")    
    description = vis.decode(img)
    out += db.insert(description)
    res['html'] = f'<img src="data:image/png;base64,{img}">'
    
  # res['form'] = FORM
  res['output'] = out
  return res

      