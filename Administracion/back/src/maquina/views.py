from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sede.permissions import EsAdministradorGimnasio

from . import qr, services
from .serializers import MaquinaEntradaSerializer, MaquinaSalidaSerializer


class MaquinasVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request):
        return Response(MaquinaSalidaSerializer(services.listar(), many=True).data)

    def post(self, request):
        serializer = MaquinaEntradaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        maquina = services.registrar(serializer.validated_data)
        return Response(MaquinaSalidaSerializer(maquina).data, status=status.HTTP_201_CREATED)


class MaquinaDetalleVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request, maquina_id):
        return Response(MaquinaSalidaSerializer(services.obtener(maquina_id)).data)


class MaquinaQRVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request, maquina_id):
        maquina = services.obtener(maquina_id)
        respuesta = HttpResponse(qr.generar_svg(maquina), content_type="image/svg+xml")
        respuesta["Content-Disposition"] = f'attachment; filename="pikafit-maquina-{maquina.codigo}.svg"'
        respuesta["X-Content-Type-Options"] = "nosniff"
        return respuesta


class MaquinaIdentificarVista(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token_qr):
        return Response(MaquinaSalidaSerializer(services.identificar(token_qr)).data)
