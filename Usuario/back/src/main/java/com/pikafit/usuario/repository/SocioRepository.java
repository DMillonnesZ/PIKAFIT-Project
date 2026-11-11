package com.pikafit.usuario.repository;

import com.pikafit.usuario.model.Socio;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface SocioRepository extends MongoRepository<Socio, String> {
    Optional<Socio> findByDni(String dni);
}