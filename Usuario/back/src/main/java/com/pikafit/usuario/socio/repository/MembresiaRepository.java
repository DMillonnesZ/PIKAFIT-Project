package com.pikafit.usuario.socio.repository;

import java.util.Optional;
import org.springframework.data.mongodb.repository.MongoRepository;
import com.pikafit.usuario.socio.model.Membresia;

public interface MembresiaRepository extends MongoRepository<Membresia, String> {
    Optional<Membresia> findFirstBySocioIdOrderByFechaFinDesc(String socioId);
}
