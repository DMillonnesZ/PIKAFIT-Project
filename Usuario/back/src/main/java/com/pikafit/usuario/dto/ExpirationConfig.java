package com.pikafit.usuario.dto;

public class ExpirationConfig {
    // Tarea de HU-009: Configuración de expiración del pase QR
    private int minutosExpiracion;
    private boolean invalidarPaseAnterior;

    public int getMinutosExpiracion() { return minutosExpiracion; }
    public void setMinutosExpiracion(int minutosExpiracion) { this.minutosExpiracion = minutosExpiracion; }

    public boolean isInvalidarPaseAnterior() { return invalidarPaseAnterior; }
    public void setInvalidarPaseAnterior(boolean invalidarPaseAnterior) { this.invalidarPaseAnterior = invalidarPaseAnterior; }
}