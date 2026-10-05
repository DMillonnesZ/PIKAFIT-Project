package com.pikafit.usuario.clinica;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.List;
import org.junit.jupiter.api.Test;
import com.pikafit.usuario.clinica.model.Clinica;
import com.pikafit.usuario.clinica.repository.ClinicaRepository;
import com.pikafit.usuario.clinica.service.ClinicaService;

class ClinicaServiceTests {
    @Test
    void devuelveSoloLasClinicasActivasDelRepositorio() {
        ClinicaRepository repositorio = mock(ClinicaRepository.class);
        Clinica clinica = mock(Clinica.class);
        when(clinica.getId()).thenReturn("507f1f77bcf86cd799439011");
        when(clinica.getRazonSocial()).thenReturn("Clínica Centro");
        when(clinica.getDireccion()).thenReturn("Av. Central 100");
        when(clinica.getTelefono()).thenReturn("014567890");
        when(repositorio.findByActivaTrueOrderByRazonSocialAsc()).thenReturn(List.of(clinica));

        var resultado = new ClinicaService(repositorio).listarActivas();

        assertEquals(1, resultado.size());
        assertEquals("Clínica Centro", resultado.getFirst().razonSocial());
        assertEquals("Av. Central 100", resultado.getFirst().direccion());
    }
}
