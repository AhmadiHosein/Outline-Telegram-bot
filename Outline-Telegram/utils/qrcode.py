import qrcode


def generate(text:str):
    path = "temp\\qrcode.png"
    img = qrcode.make(text)
    img.save(path)
    return path