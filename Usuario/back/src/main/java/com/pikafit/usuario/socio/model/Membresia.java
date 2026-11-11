package com.pikafit.usuario.socio.model;

import java.time.LocalDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "membresias")
public class Membresia {
    @Id
    private String id;

    @Field("socio_id")
    private String socioId;

    @Field("fecha_inicio")
    private LocalDate fechaInicio;

    @Field("fecha_fin")
    private LocalDate fechaFin;

    private boolean activa;

    public String getId() { return id; }
    public String getSocioId() { return socioId; }
    public LocalDate getFechaInicio() { return fechaInicio; }
    public LocalDate getFechaFin() { return fechaFin; }
    public boolean isActiva() { return activa; }
}
