package com.pikafit.usuario.socio.controller;

import java.security.Principal;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.pikafit.usuario.socio.dto.EstadoMembresiaResponse;
import com.pikafit.usuario.socio.service.IdentidadSocioService;
import com.pikafit.usuario.socio.service.VigenciaMembresiaService;

@RestController
@RequestMapping("/api/v1/membresia")
public class EstadoMembresiaController {
    private final IdentidadSocioService identidad;
    private final VigenciaMembresiaService vigencia;

    public EstadoMembresiaController(IdentidadSocioService identidad, VigenciaMembresiaService vigencia) {
        this.identidad = identidad;
        this.vigencia = vigencia;
    }

    @GetMapping("/estado")
    public ResponseEntity<?> estado(Principal principal) {
        var socio = identidad.buscar(principal == null ? null : principal.getName());
        if (socio.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(Map.of(
                    "codigo", "SOCIO_NO_IDENTIFICADO",
                    "mensaje", "La sesión no identifica a un socio registrado."));
        }
        EstadoMembresiaResponse estado = vigencia.consultar(socio.get());
        return ResponseEntity.ok(estado);
    }
}
