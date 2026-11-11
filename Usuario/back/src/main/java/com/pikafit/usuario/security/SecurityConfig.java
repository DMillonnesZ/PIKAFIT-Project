package com.pikafit.usuario.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.access.intercept.AuthorizationFilter;
import org.springframework.security.web.SecurityFilterChain;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pikafit.usuario.socio.service.IdentidadSocioService;
import com.pikafit.usuario.socio.service.VigenciaMembresiaService;

@Configuration
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http,
                                    IdentidadSocioService identidadSocio,
                                    VigenciaMembresiaService vigenciaMembresia,
                                    ObjectMapper json) throws Exception {
        http
                .cors(Customizer.withDefaults())
                .csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/actuator/health").permitAll()
                        .requestMatchers(HttpMethod.GET, "/api/v1/clinicas").permitAll()
                        .anyRequest().authenticated())
                .addFilterAfter(new VigenciaMembresiaFilter(identidadSocio, vigenciaMembresia, json),
                        AuthorizationFilter.class);
        return http.build();
    }
}
