package com.pikafit.usuario;

import com.pikafit.usuario.controller.AuthController;
import com.pikafit.usuario.model.Socio;
import com.pikafit.usuario.repository.SocioRepository;
import com.pikafit.usuario.service.AuthService;
import com.pikafit.usuario.service.GoogleNoDisponibleException;
import com.pikafit.usuario.service.GoogleTokenVerifier;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.Optional;

import static org.mockito.ArgumentMatchers.anyString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

public class AuthControllerTest {

    private SocioRepository repo;
    private GoogleTokenVerifier google;
    private MockMvc mvc;

    @BeforeEach
    void preparar() {
        repo = Mockito.mock(SocioRepository.class);
        google = Mockito.mock(GoogleTokenVerifier.class);
        mvc = MockMvcBuilders.standaloneSetup(new AuthController(new AuthService(repo, google))).build();
    }

    private Socio socio(boolean activo) {
        Socio s = new Socio();
        s.setId("1");
        s.setDni("12345678");
        s.setCorreoGoogle("socio@gmail.com");
        s.setActivo(activo);
        return s;
    }

    private org.springframework.test.web.servlet.ResultActions login(String json) throws Exception {
        return mvc.perform(post("/api/auth/login-socio")
                .contentType(MediaType.APPLICATION_JSON).content(json));
    }

    @Test
    void dniYCorreoCoinciden_entra() throws Exception {
        Mockito.when(repo.findByDni("12345678")).thenReturn(Optional.of(socio(true)));
        Mockito.when(google.obtenerCorreo(anyString())).thenReturn(Optional.of("socio@gmail.com"));
        login("{\"dni\":\"12345678\",\"googleToken\":\"t\"}")
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("success")));
    }

    @Test
    void correoDistinto_rechazaSinRevelarCorreo() throws Exception {
        Mockito.when(repo.findByDni("12345678")).thenReturn(Optional.of(socio(true)));
        Mockito.when(google.obtenerCorreo(anyString())).thenReturn(Optional.of("otro@gmail.com"));
        login("{\"dni\":\"12345678\",\"googleToken\":\"t\"}")
                .andExpect(status().isUnauthorized())
                .andExpect(content().string(org.hamcrest.Matchers.not(
                        org.hamcrest.Matchers.containsString("socio@gmail.com"))));
    }

    @Test
    void dniNoRegistrado_rechazaConMensajeDeGimnasio() throws Exception {
        Mockito.when(repo.findByDni("99999999")).thenReturn(Optional.empty());
        login("{\"dni\":\"99999999\",\"googleToken\":\"t\"}")
                .andExpect(status().isUnauthorized())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("gimnasio")));
    }

    @Test
    void cuentaNoActivada_rechaza() throws Exception {
        Mockito.when(repo.findByDni("12345678")).thenReturn(Optional.of(socio(false)));
        login("{\"dni\":\"12345678\",\"googleToken\":\"t\"}")
                .andExpect(status().isUnauthorized());
    }

    @Test
    void faltanDatos_devuelve400() throws Exception {
        login("{\"dni\":\"\"}").andExpect(status().isBadRequest());
    }

    @Test
    void googleNoResponde_devuelve503() throws Exception {
        Mockito.when(repo.findByDni("12345678")).thenReturn(Optional.of(socio(true)));
        Mockito.when(google.obtenerCorreo(anyString()))
                .thenThrow(new GoogleNoDisponibleException(new RuntimeException("sin red")));
        login("{\"dni\":\"12345678\",\"googleToken\":\"t\"}")
                .andExpect(status().isServiceUnavailable());
    }
}