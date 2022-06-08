import base64

def encode(file):
    with open(file,"rb")as icon:
        ic = base64.b64encode(icon.read())
    return f"data:image/png;base64,{ic.decode('utf-8')}"