package com.pikafit.usuario.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDate;

// Los nombres de campo deben coincidir con los de Jesús (HU-057).
@Document(collection = "socios")
public class Socio {
    @Id
    private String id;
    private String dni;
    private String correoGoogle;
    private boolean activo;
    private String plan;
    private LocalDate fechaInicio;
    private LocalDate fechaFin;

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getDni() { return dni; }
    public void setDni(String dni) { this.dni = dni; }
    public String getCorreoGoogle() { return correoGoogle; }
    public void setCorreoGoogle(String correoGoogle) { this.correoGoogle = correoGoogle; }
    public boolean isActivo() { return activo; }
    public void setActivo(boolean activo) { this.activo = activo; }
    public String getPlan() { return plan; }
    public void setPlan(String plan) { this.plan = plan; }
    public LocalDate getFechaInicio() { return fechaInicio; }
    public void setFechaInicio(LocalDate fechaInicio) { this.fechaInicio = fechaInicio; }
    public LocalDate getFechaFin() { return fechaFin; }
    public void setFechaFin(LocalDate fechaFin) { this.fechaFin = fechaFin; }
}