import os, re, requests as req
import json, socket, traceback, time
import vdb

MODEL = "llama3.1:8b"
COLLECTION = "cats"
SIZE = 10
USAGE = "Your query is then passed to the LLM with the sentences for an answer."

def streamlines(args, lines):
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT") or "0")
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    if sock:
      s.connect((sock, port))
    try:
      for line in lines:
        time.sleep(0.1)
        msg = {"output": line }
        #print(msg)
        out += line
        if sock:
          s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
    if sock:
      s.close()
  return out

def stream(args, lines):
  sock = args.get("STREAM_HOST")
  port = int(args.get("STREAM_PORT") or "0")
  out = ""
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    if sock:
      s.connect((sock, port))
    try:
      for line in lines:
        dec = json.loads(line.decode("utf-8")).get("response")
        msg = {"output": dec }
        #print(msg)
        out += dec
        if sock:
          s.sendall(json.dumps(msg).encode("utf-8"))
    except Exception as e:
      traceback.print_exc(e)
      out = str(e)
    if sock:
      s.close()
  return out


def llm(args, model, prompt):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  url = f"https://{auth}@{host}/api/generate"

  msg = {
    "model": model,
    "prompt": prompt,
    "stream": True
  }

  lines = req.post(url, json=msg, stream=True).iter_lines()
  return stream(args, lines)

def rag_img(args):
  inp = str(args.get('input', ""))
  out = USAGE
  if inp != "":
    content = inp
    db = vdb.VectorDB(args, COLLECTION)
    res = db.vector_search(content, limit=SIZE)
    prompt = ""
    if len(res) > 0:
      prompt += "Consider the following text:\n"
      for (w,txt) in res:
        prompt += f"{txt}\n"
      prompt += "Answer to the following prompt:\n"
    prompt += f"{content}"
      
    print(prompt)
    out = llm(args, MODEL, prompt)

  return { "output": out, "streaming": True}
