package com.pikafit.usuario.dto;

public class ConsentRequest {
    private String socioId;
    private boolean aceptado;

    public String getSocioId() { return socioId; }
    public void setSocioId(String socioId) { this.socioId = socioId; }
    public boolean isAceptado() { return aceptado; }
    public void setAceptado(boolean aceptado) { this.aceptado = aceptado; }
}