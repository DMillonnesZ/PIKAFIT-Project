from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .permissions import EsAdministradorGimnasio
from .serializers import SedeEntradaSerializer, SedeSalidaSerializer


def _validar(request, *, parcial=False):
    serializer = SedeEntradaSerializer(data=request.data, partial=parcial)
    if not serializer.is_valid():
        return None, Response(
            {"codigo": "DATOS_INVALIDOS", "detalles": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return serializer.validated_data, None


class SedesVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request):
        sedes = services.listar_activas() if request.query_params.get("activas") == "true" else services.listar()
        return Response(SedeSalidaSerializer(sedes, many=True).data)

    def post(self, request):
        datos, error = _validar(request)
        if error:
            return error
        sede = services.crear(datos)
        return Response(SedeSalidaSerializer(sede).data, status=status.HTTP_201_CREATED)


class SedeDetalleVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def patch(self, request, sede_id):
        datos, error = _validar(request, parcial=True)
        if error:
            return error
        if not datos:
            return Response({"codigo": "DATOS_INVALIDOS", "mensaje": "No hay campos para actualizar."}, status=400)
        try:
            sede = services.actualizar(sede_id, datos)
        except services.SedeNoEncontrada as exc:
            return Response({"codigo": "SEDE_NO_ENCONTRADA", "mensaje": str(exc)}, status=404)
        return Response(SedeSalidaSerializer(sede).data)

    def delete(self, request, sede_id):
        try:
            sede = services.desactivar(sede_id)
        except services.SedeNoEncontrada as exc:
            return Response({"codigo": "SEDE_NO_ENCONTRADA", "mensaje": str(exc)}, status=404)
        return Response(SedeSalidaSerializer(sede).data)
