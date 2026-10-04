package com.pikafit.usuario.dto;

public class LoginRequest {
    private String dni;
    private String googleToken;

    public String getDni() { return dni; }
    public void setDni(String dni) { this.dni = dni; }
    public String getGoogleToken() { return googleToken; }
    public void setGoogleToken(String googleToken) { this.googleToken = googleToken; }
}