package com.pikafit.usuario.clinica.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;

public record ClinicaResponse(
    String id,
    @JsonProperty("razon_social") String razonSocial,
    String direccion,
    String telefono
) {}
