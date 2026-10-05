from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

from bson import ObjectId

from clinica import services
from clinica.serializers import ClinicaEntradaSerializer


class ClinicaHu010Tests(TestCase):
    def setUp(self):
        self.datos = {
            "razon_social": "Clínica de prueba",
            "ruc": "20100070970",
            "direccion": "Av. Central 123",
            "telefono": "014567890",
            "activa": True,
        }

    def test_ruc_no_numerico_o_corto_es_rechazado(self):
        for ruc in ("2010007097", "2010007097A", "99100070970", "20100070971"):
            with self.subTest(ruc=ruc):
                serializer = ClinicaEntradaSerializer(data={**self.datos, "ruc": ruc})
                self.assertFalse(serializer.is_valid())
                self.assertIn("ruc", serializer.errors)

    def test_campos_obligatorios(self):
        for campo in self.datos:
            with self.subTest(campo=campo):
                datos = {**self.datos}
                del datos[campo]
                serializer = ClinicaEntradaSerializer(data=datos)
                self.assertFalse(serializer.is_valid())
                self.assertIn(campo, serializer.errors)

    def test_ruc_duplicado_es_rechazado(self):
        existente = SimpleNamespace(pk=ObjectId())
        with patch("clinica.services.Clinica.objects.filter") as buscar:
            buscar.return_value.first.return_value = existente
            with self.assertRaises(services.RucDuplicado):
                services._verificar_ruc_disponible(self.datos["ruc"])

    def test_desactivar_conserva_el_registro(self):
        clinica = SimpleNamespace(activa=True, save=Mock())
        with patch("clinica.services._obtener", return_value=clinica):
            self.assertIs(services.desactivar("id"), clinica)
        self.assertFalse(clinica.activa)
        clinica.save.assert_called_once_with(update_fields=["activa"])

    def test_clinica_inactiva_no_puede_operar(self):
        clinica = SimpleNamespace(activa=False)
        with patch("clinica.services._obtener", return_value=clinica):
            with self.assertRaises(services.ClinicaNoEncontrada):
                services.obtener_activa_para_operacion("id")
