package com.pikafit.usuario.clinica.repository;

import java.util.List;
import org.springframework.data.mongodb.repository.MongoRepository;
import com.pikafit.usuario.clinica.model.Clinica;

public interface ClinicaRepository extends MongoRepository<Clinica, String> {
    List<Clinica> findByActivaTrueOrderByRazonSocialAsc();
}
