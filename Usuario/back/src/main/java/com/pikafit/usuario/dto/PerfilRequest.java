package com.pikafit.usuario.dto;

public class PerfilRequest {
    private String objetivo;
    private String nivelExperiencia;
    private Double tallaCm;
    private Double pesoKg;

    public String getObjetivo() { return objetivo; }
    public void setObjetivo(String objetivo) { this.objetivo = objetivo; }
    public String getNivelExperiencia() { return nivelExperiencia; }
    public void setNivelExperiencia(String nivelExperiencia) { this.nivelExperiencia = nivelExperiencia; }
    public Double getTallaCm() { return tallaCm; }
    public void setTallaCm(Double tallaCm) { this.tallaCm = tallaCm; }
    public Double getPesoKg() { return pesoKg; }
    public void setPesoKg(Double pesoKg) { this.pesoKg = pesoKg; }
}