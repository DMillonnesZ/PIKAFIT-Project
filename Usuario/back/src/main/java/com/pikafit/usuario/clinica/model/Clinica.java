package com.pikafit.usuario.clinica.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "clinicas")
public class Clinica {
    @Id
    private String id;
    @Field("razon_social")
    private String razonSocial;
    private String direccion;
    private String telefono;
    private boolean activa;

    public String getId() { return id; }
    public String getRazonSocial() { return razonSocial; }
    public String getDireccion() { return direccion; }
    public String getTelefono() { return telefono; }
    public boolean isActiva() { return activa; }
}
