package com.pikafit.usuario.clinica.service;

import java.util.List;
import org.springframework.stereotype.Service;
import com.pikafit.usuario.clinica.dto.response.ClinicaResponse;
import com.pikafit.usuario.clinica.repository.ClinicaRepository;

@Service
public class ClinicaService {
    private final ClinicaRepository repository;

    public ClinicaService(ClinicaRepository repository) {
        this.repository = repository;
    }

    public List<ClinicaResponse> listarActivas() {
        // Solo lectura: Django es dueño de la colección clinicas.
        return repository.findByActivaTrueOrderByRazonSocialAsc().stream()
            .map(c -> new ClinicaResponse(c.getId(), c.getRazonSocial(),
                c.getDireccion(), c.getTelefono()))
            .toList();
    }
}
