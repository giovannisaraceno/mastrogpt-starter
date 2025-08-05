import os
import base64
import vision
import vdb

def is_image_file(filename): 
 return filename.lower().endswith(('.jpeg'))

def encode_image_to_base64(filepath):
  with open(filepath, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  

def load(args, collection):
  image_dir = "/Users/giovannisaraceno/Experimental/mastrogpt-starter/lessons/rag_images"
  out = ""
  vis = vision.Vision(args)
  db = vdb.VectorDB(args, collection)
  for filename in os.listdir(image_dir):
    filepath = os.path.join(image_dir, filename)
    if os.path.isfile(filepath) and is_image_file(filename):
      base64_string = encode_image_to_base64(filepath)
      cat_name, _ = os.path.splitext(filename)      
      description = vis.decode(base64_string, cat_name)
      out += db.insert(description)
  return out
      