package com.pikafit.usuario.socio.repository;

import java.util.Optional;
import org.springframework.data.mongodb.repository.MongoRepository;
import com.pikafit.usuario.socio.model.Socio;

public interface SocioRepository extends MongoRepository<Socio, String> {
    Optional<Socio> findFirstByDni(String dni);
    Optional<Socio> findFirstByCorreoIgnoreCase(String correo);
}
