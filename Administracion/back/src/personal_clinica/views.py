from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sede.permissions import EsAdministradorGimnasio

from . import services
from .serializers import PersonalEntradaSerializer, PersonalSalidaSerializer


class PersonalClinicaListaVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request):
        cuentas = services.listar(request.query_params.get("clinica_id"))
        return Response(PersonalSalidaSerializer(cuentas, many=True).data)

    def post(self, request):
        serializer = PersonalEntradaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cuenta = services.crear(serializer.validated_data)
        return Response({
            "personal": PersonalSalidaSerializer(cuenta).data,
            "mensaje": "Cuenta activa. El personal definirá su contraseña con el enlace de recuperación.",
        }, status=status.HTTP_201_CREATED)


class PersonalClinicaDetalleVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request, cuenta_id):
        return Response(PersonalSalidaSerializer(services.obtener(cuenta_id)).data)

    def patch(self, request, cuenta_id):
        serializer = PersonalEntradaSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data:
            return Response({"codigo": "DATOS_INVALIDOS", "mensaje": "No hay campos para actualizar."}, status=400)
        return Response(PersonalSalidaSerializer(services.actualizar(cuenta_id, serializer.validated_data)).data)

    def delete(self, request, cuenta_id):
        return Response(PersonalSalidaSerializer(services.desactivar(cuenta_id)).data)
