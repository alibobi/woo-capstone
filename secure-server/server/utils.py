from io import BytesIO
import qrcode
from base64 import b64encode


def get_b64encoded_qr_image(data):
    print(data)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered)
    return b64encode(buffered.getvalue()).decode("utf-8")


def is_password_in_list(password):
    with open("./server/10-million-password-list-top-10000.txt", 'r') as file:
        dictionary = set(line.strip() for line in file)

    if password in dictionary:
        return True
    else:
        return False
