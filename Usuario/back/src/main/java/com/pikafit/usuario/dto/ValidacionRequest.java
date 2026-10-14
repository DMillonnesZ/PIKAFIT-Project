package com.pikafit.usuario.dto;

public class ValidacionRequest {
    private String tokenQr;
    private String codigoAlternativo;

    public String getTokenQr() { return tokenQr; }
    public void setTokenQr(String tokenQr) { this.tokenQr = tokenQr; }
    public String getCodigoAlternativo() { return codigoAlternativo; }
    public void setCodigoAlternativo(String codigoAlternativo) { this.codigoAlternativo = codigoAlternativo; }
}