import qrcode
import random
from datetime import datetime


async def generate_qr_code(user_id):
    random_numb = random.randint(1_000_000, 9_999_999)
    qr = qrcode.QRCode(
        version=13,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=5,
    )
    qr.add_data(f"{user_id}:{random_numb}:{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}")
    qr.make(fit=True)
    qr_code = qr.make_image(fill_color="black", back_color="white")
    qr_code.save(f'media/{user_id}.jpg')
    return
