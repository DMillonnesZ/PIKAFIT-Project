package com.pikafit.usuario.socio.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "socios")
public class Socio {
    @Id
    private String id;

    private String dni;
    private String correo;
    private boolean activo;

    @Field("nombres")
    private String nombres;

    @Field("apellidos")
    private String apellidos;

    public String getId() { return id; }
    public String getDni() { return dni; }
    public String getCorreo() { return correo; }
    public boolean isActivo() { return activo; }
    public String getNombres() { return nombres; }
    public String getApellidos() { return apellidos; }
}
