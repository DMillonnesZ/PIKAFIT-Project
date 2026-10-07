"""Representación descargable del identificador inmutable de una máquina."""
import qrcode
from qrcode.image.svg import SvgPathImage


def contenido(maquina):
    return f"pikafit:maquina:{maquina.token_qr}"


def generar_svg(maquina):
    codigo = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )
    codigo.add_data(contenido(maquina))
    codigo.make(fit=True)
    return codigo.make_image(image_factory=SvgPathImage).to_string()
