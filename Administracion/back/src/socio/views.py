from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sede.permissions import EsAdministradorGimnasio

from . import services
from .models import Membresia
from .serializers import (
    MembresiaSalidaSerializer,
    PlanEntradaSerializer,
    PlanSalidaSerializer,
    SocioEdicionSerializer,
    SocioEntradaSerializer,
    SocioSalidaSerializer,
)


class PlanesVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request):
        planes = services.listar_planes(incluir_inactivos=request.query_params.get("inactivos") == "true")
        return Response(PlanSalidaSerializer(planes, many=True).data)

    def post(self, request):
        serializer = PlanEntradaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            plan = services.crear_plan(serializer.validated_data)
        except services.PlanDuplicado as exc:
            return Response({"codigo": "PLAN_DUPLICADO", "mensaje": str(exc)}, status=409)
        return Response(PlanSalidaSerializer(plan).data, status=status.HTTP_201_CREATED)


class PlanDetalleVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def patch(self, request, plan_id):
        serializer = PlanEntradaSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data:
            return Response({"codigo": "DATOS_INVALIDOS", "mensaje": "No hay campos para actualizar."}, status=400)
        try:
            plan = services.actualizar_plan(plan_id, serializer.validated_data)
        except services.PlanNoEncontrado as exc:
            return Response({"codigo": "PLAN_NO_ENCONTRADO", "mensaje": str(exc)}, status=404)
        except services.PlanDuplicado as exc:
            return Response({"codigo": "PLAN_DUPLICADO", "mensaje": str(exc)}, status=409)
        return Response(PlanSalidaSerializer(plan).data)

    def delete(self, request, plan_id):
        try:
            plan = services.desactivar_plan(plan_id)
        except services.PlanNoEncontrado as exc:
            return Response({"codigo": "PLAN_NO_ENCONTRADO", "mensaje": str(exc)}, status=404)
        return Response(PlanSalidaSerializer(plan).data)


class SociosVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request):
        resultado = []
        for socio in services.listar_socios():
            ultima = Membresia.objects.filter(socio_id=socio.pk).order_by("-fecha_fin").first()
            resultado.append({
                **SocioSalidaSerializer(socio).data,
                "membresia": MembresiaSalidaSerializer(ultima).data if ultima else None,
            })
        return Response(resultado)

    def post(self, request):
        serializer = SocioEntradaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            socio, membresia = services.crear_socio_con_membresia(serializer.validated_data)
        except services.RenovacionDisponible as exc:
            return Response({
                "codigo": "RENOVACION_DISPONIBLE",
                "mensaje": str(exc),
                "socio": SocioSalidaSerializer(exc.socio).data,
            }, status=409)
        except services.SocioDuplicado as exc:
            return Response({"codigo": "SOCIO_DUPLICADO", "mensaje": str(exc)}, status=409)
        except services.PlanNoEncontrado as exc:
            return Response({"codigo": "PLAN_NO_DISPONIBLE", "mensaje": str(exc)}, status=400)
        except services.SedeNoDisponible as exc:
            return Response({"codigo": "SEDE_NO_DISPONIBLE", "mensaje": str(exc)}, status=400)
        except ValueError as exc:
            return Response({"codigo": "FECHAS_INVALIDAS", "mensaje": str(exc)}, status=400)
        return Response({
            "socio": SocioSalidaSerializer(socio).data,
            "membresia": MembresiaSalidaSerializer(membresia).data,
        }, status=status.HTTP_201_CREATED)


class SocioDetalleVista(APIView):
    permission_classes = [IsAuthenticated, EsAdministradorGimnasio]

    def get(self, request, socio_id):
        try:
            socio = services._obtener_socio(socio_id)
        except services.SocioNoEncontrado as exc:
            return Response({"codigo": "SOCIO_NO_ENCONTRADO", "mensaje": str(exc)}, status=404)
        membresias = Membresia.objects.filter(socio_id=socio.pk).order_by("-fecha_fin")
        return Response({
            "socio": SocioSalidaSerializer(socio).data,
            "membresias": MembresiaSalidaSerializer(membresias, many=True).data,
        })

    def patch(self, request, socio_id):
        serializer = SocioEdicionSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data:
            return Response({"codigo": "DATOS_INVALIDOS", "mensaje": "No hay campos para actualizar."}, status=400)
        try:
            socio = services.actualizar_socio(socio_id, serializer.validated_data)
        except services.SocioNoEncontrado as exc:
            return Response({"codigo": "SOCIO_NO_ENCONTRADO", "mensaje": str(exc)}, status=404)
        except services.SedeNoDisponible as exc:
            return Response({"codigo": "SEDE_NO_DISPONIBLE", "mensaje": str(exc)}, status=400)
        return Response(SocioSalidaSerializer(socio).data)

    def post(self, request, socio_id):
        serializer = SocioEntradaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            socio, membresia = services.renovar_membresia(socio_id, serializer.validated_data)
        except services.SocioNoEncontrado as exc:
            return Response({"codigo": "SOCIO_NO_ENCONTRADO", "mensaje": str(exc)}, status=404)
        except services.SocioDuplicado as exc:
            return Response({"codigo": "RENOVACION_NO_DISPONIBLE", "mensaje": str(exc)}, status=409)
        except services.PlanNoEncontrado as exc:
            return Response({"codigo": "PLAN_NO_DISPONIBLE", "mensaje": str(exc)}, status=400)
        except services.SedeNoDisponible as exc:
            return Response({"codigo": "SEDE_NO_DISPONIBLE", "mensaje": str(exc)}, status=400)
        except ValueError as exc:
            return Response({"codigo": "FECHAS_INVALIDAS", "mensaje": str(exc)}, status=400)
        return Response({
            "socio": SocioSalidaSerializer(socio).data,
            "membresia": MembresiaSalidaSerializer(membresia).data,
        }, status=status.HTTP_201_CREATED)
