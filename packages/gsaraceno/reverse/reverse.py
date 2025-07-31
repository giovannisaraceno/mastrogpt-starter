def reverse(args):
  input = args.get("input", "")
  output = "Please provide a valid input"
  if input != "" :
    output = input[::-1]
  return { "output": output }
