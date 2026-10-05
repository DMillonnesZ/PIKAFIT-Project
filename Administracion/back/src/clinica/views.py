from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sede.permissions import EsAdministradorGimnasio

from . import services
from .serializers import ClinicaEntradaSerializer, ClinicaSalidaSerializer


def _validar(request, *, parcial=False):
    serializer = ClinicaEntradaSerializer(data=request.data, partial=parcial)
    if not serializer.is_valid():
        return None, Response(
            {"codigo": "DATOS_INVALIDOS", "detalles": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return serializer.validated_data, None


class ClinicasVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request):
        clinicas = services.listar_activas() if request.query_params.get("activas") == "true" else services.listar()
        return Response(ClinicaSalidaSerializer(clinicas, many=True).data)

    def post(self, request):
        datos, error = _validar(request)
        if error:
            return error
        try:
            clinica = services.crear(datos)
        except services.RucDuplicado as exc:
            return Response({"codigo": "RUC_DUPLICADO", "mensaje": str(exc)}, status=409)
        return Response(ClinicaSalidaSerializer(clinica).data, status=status.HTTP_201_CREATED)


class ClinicaDetalleVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def patch(self, request, clinica_id):
        datos, error = _validar(request, parcial=True)
        if error:
            return error
        if not datos:
            return Response({"codigo": "DATOS_INVALIDOS", "mensaje": "No hay campos para actualizar."}, status=400)
        try:
            clinica = services.actualizar(clinica_id, datos)
        except services.ClinicaNoEncontrada as exc:
            return Response({"codigo": "CLINICA_NO_ENCONTRADA", "mensaje": str(exc)}, status=404)
        except services.RucDuplicado as exc:
            return Response({"codigo": "RUC_DUPLICADO", "mensaje": str(exc)}, status=409)
        return Response(ClinicaSalidaSerializer(clinica).data)

    def delete(self, request, clinica_id):
        try:
            clinica = services.desactivar(clinica_id)
        except services.ClinicaNoEncontrada as exc:
            return Response({"codigo": "CLINICA_NO_ENCONTRADA", "mensaje": str(exc)}, status=404)
        return Response(ClinicaSalidaSerializer(clinica).data)
