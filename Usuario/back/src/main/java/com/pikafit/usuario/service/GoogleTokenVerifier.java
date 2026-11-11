package com.pikafit.usuario.service;

import java.util.Optional;

public interface GoogleTokenVerifier {
    /** Devuelve el correo si el token es válido; vacío si no lo es.
     *  Lanza GoogleNoDisponibleException si Google no responde. */
    Optional<String> obtenerCorreo(String idToken);
}