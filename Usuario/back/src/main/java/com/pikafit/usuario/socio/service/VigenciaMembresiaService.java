package com.pikafit.usuario.socio.service;

import java.time.LocalDate;
import java.time.ZoneId;
import org.springframework.stereotype.Service;
import com.pikafit.usuario.socio.dto.EstadoMembresiaResponse;
import com.pikafit.usuario.socio.model.Membresia;
import com.pikafit.usuario.socio.model.Socio;
import com.pikafit.usuario.socio.repository.MembresiaRepository;

@Service
public class VigenciaMembresiaService {
    private static final ZoneId ZONA_PROYECTO = ZoneId.of("America/Lima");
    private final MembresiaRepository membresias;

    public VigenciaMembresiaService(MembresiaRepository membresias) {
        this.membresias = membresias;
    }

    public EstadoMembresiaResponse consultar(Socio socio) {
        if (!socio.isActivo()) {
            return new EstadoMembresiaResponse("CUENTA_INACTIVA", null,
                    "La cuenta del socio está inactiva.");
        }
        Membresia membresia = membresias.findFirstBySocioIdOrderByFechaFinDesc(socio.getId()).orElse(null);
        if (membresia == null) {
            return new EstadoMembresiaResponse("SIN_MEMBRESIA", null,
                    "La cuenta no tiene una membresía registrada.");
        }

        LocalDate hoy = LocalDate.now(ZONA_PROYECTO);
        if (membresia.getFechaFin() != null && hoy.isAfter(membresia.getFechaFin())) {
            return new EstadoMembresiaResponse("VENCIDA", membresia.getFechaFin(),
                    "Tu membresía venció el " + membresia.getFechaFin() + ". Renueva para recuperar el acceso.");
        }
        if (!membresia.isActiva() || membresia.getFechaInicio() == null
                || hoy.isBefore(membresia.getFechaInicio())) {
            return new EstadoMembresiaResponse("NO_VIGENTE", membresia.getFechaFin(),
                    "Tu membresía no está vigente. Comunícate con la administración del gimnasio.");
        }
        return new EstadoMembresiaResponse("VIGENTE", membresia.getFechaFin(),
                "Tu membresía está vigente.");
    }
}
