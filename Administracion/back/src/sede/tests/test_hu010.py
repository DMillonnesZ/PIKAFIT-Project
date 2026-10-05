from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

from sede import services
from sede.serializers import SedeEntradaSerializer


class SedeHu010Tests(TestCase):
    def test_nombre_direccion_y_estado_son_obligatorios(self):
        datos = {"nombre": "Centro", "direccion": "Av. Principal 1", "activa": True}
        for campo in datos:
            with self.subTest(campo=campo):
                incompletos = {**datos}
                del incompletos[campo]
                serializer = SedeEntradaSerializer(data=incompletos)
                self.assertFalse(serializer.is_valid())
                self.assertIn(campo, serializer.errors)

    def test_desactivar_conserva_la_sede(self):
        sede = SimpleNamespace(activa=True, save=Mock())
        with patch("sede.services._obtener", return_value=sede):
            self.assertIs(services.desactivar("id"), sede)
        self.assertFalse(sede.activa)
        sede.save.assert_called_once_with(update_fields=["activa"])

    def test_sede_inactiva_no_se_asigna(self):
        sede = SimpleNamespace(activa=False)
        with patch("sede.services._obtener", return_value=sede):
            with self.assertRaises(services.SedeNoEncontrada):
                services.obtener_activa_para_asignacion("id")
