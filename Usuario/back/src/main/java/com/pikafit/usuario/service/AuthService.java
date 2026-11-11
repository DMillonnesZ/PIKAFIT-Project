package com.pikafit.usuario.service;

import com.pikafit.usuario.model.Socio;
import com.pikafit.usuario.repository.SocioRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final SocioRepository socioRepository;
    private final GoogleTokenVerifier googleVerifier;

    public AuthService(SocioRepository socioRepository, GoogleTokenVerifier googleVerifier) {
        this.socioRepository = socioRepository;
        this.googleVerifier = googleVerifier;
    }

    public Socio loginSocio(String dni, String googleToken) {
        Socio socio = socioRepository.findByDni(dni)
                .filter(Socio::isActivo)
                .orElseThrow(() -> new AuthException(HttpStatus.UNAUTHORIZED,
                        "DNI no registrado o cuenta no activada. Acude al gimnasio."));

        String correo;
        try {
            correo = googleVerifier.obtenerCorreo(googleToken).orElse(null);
        } catch (GoogleNoDisponibleException e) {
            throw new AuthException(HttpStatus.SERVICE_UNAVAILABLE,
                    "No se pudo contactar con Google. Intenta nuevamente.");
        }

        // Mismo mensaje para token inválido y correo distinto: no revela el correo registrado.
        if (correo == null || !correo.equalsIgnoreCase(socio.getCorreoGoogle())) {
            throw new AuthException(HttpStatus.UNAUTHORIZED,
                    "No se pudo validar tu cuenta de Google para este DNI.");
        }
        return socio;
    }
}