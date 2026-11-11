package com.pikafit.usuario.socio.service;

import java.util.Optional;
import org.bson.types.ObjectId;
import org.springframework.stereotype.Service;
import com.pikafit.usuario.socio.model.Socio;
import com.pikafit.usuario.socio.repository.SocioRepository;

@Service
public class IdentidadSocioService {
    private final SocioRepository socios;

    public IdentidadSocioService(SocioRepository socios) {
        this.socios = socios;
    }

    public Optional<Socio> buscar(String identidadAutenticada) {
        if (identidadAutenticada == null || identidadAutenticada.isBlank()) {
            return Optional.empty();
        }
        String identidad = identidadAutenticada.trim();
        if (ObjectId.isValid(identidad)) {
            Optional<Socio> porId = socios.findById(identidad);
            if (porId.isPresent()) return porId;
        }
        if (identidad.matches("\\d{8}")) return socios.findFirstByDni(identidad);
        if (identidad.contains("@")) return socios.findFirstByCorreoIgnoreCase(identidad);
        return Optional.empty();
    }
}
