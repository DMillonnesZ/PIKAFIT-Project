package com.pikafit.usuario.controller;

import com.pikafit.usuario.dto.LoginRequest;
import com.pikafit.usuario.model.Socio;
import com.pikafit.usuario.service.AuthException;
import com.pikafit.usuario.service.AuthService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/login-socio")
    public ResponseEntity<?> loginSocio(@RequestBody LoginRequest request) {
        if (request.getDni() == null || request.getDni().isBlank()
                || request.getGoogleToken() == null || request.getGoogleToken().isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("mensaje", "Faltan datos obligatorios"));
        }
        Socio socio = authService.loginSocio(request.getDni().trim(), request.getGoogleToken());
        // TODO (siguiente paso): emitir JWT propio de sesión.
        return ResponseEntity.ok(Map.of("status", "success", "socioId", socio.getId()));
    }

    @ExceptionHandler(AuthException.class)
    public ResponseEntity<Map<String, String>> manejarAuth(AuthException e) {
        return ResponseEntity.status(e.getStatus()).body(Map.of("mensaje", e.getMessage()));
    }
}