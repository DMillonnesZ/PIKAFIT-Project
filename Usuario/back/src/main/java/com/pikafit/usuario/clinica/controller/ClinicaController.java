package com.pikafit.usuario.clinica.controller;

import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.pikafit.usuario.clinica.dto.response.ClinicaResponse;
import com.pikafit.usuario.clinica.service.ClinicaService;

@RestController
@RequestMapping("/api/v1/clinicas")
public class ClinicaController {
    private final ClinicaService service;

    public ClinicaController(ClinicaService service) {
        this.service = service;
    }

    @GetMapping
    public List<ClinicaResponse> listarActivas() {
        return service.listarActivas();
    }
}
