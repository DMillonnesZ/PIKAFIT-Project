package com.pikafit.usuario.socio.dto;

import java.time.LocalDate;

public record EstadoMembresiaResponse(
        String estado,
        LocalDate fechaFin,
        String mensaje
) {
}
