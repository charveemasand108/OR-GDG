import qrcode

def generate_qr(data: str, filename: str) -> str:
    img = qrcode.make(data)
    path = f"app/qr_codes/{filename}.png"
    img.save(path)
    return path