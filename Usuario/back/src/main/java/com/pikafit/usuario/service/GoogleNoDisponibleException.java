package com.pikafit.usuario.service;

public class GoogleNoDisponibleException extends RuntimeException {
    public GoogleNoDisponibleException(Throwable causa) {
        super("Google no disponible", causa);
    }
}