#--kind python:default
#--web true
import loader_img
def main(args):
  return { "body": loader_img.loader_img(args) }
