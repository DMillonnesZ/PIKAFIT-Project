package com.pikafit.usuario.controller;

import com.pikafit.usuario.dto.LoginRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @PostMapping("/login-socio")
    public ResponseEntity<?> loginSocio(@RequestBody LoginRequest request) {
        if (request.getDni() == null || request.getGoogleToken() == null) {
            return ResponseEntity.badRequest().body("Faltan datos obligatorios");
        }

        if ("12345678".equals(request.getDni()) && "token-google-valido".equals(request.getGoogleToken())) {
            Map<String, String> response = new HashMap<>();
            response.put("status", "success");
            response.put("token", "jwt-token-simulado-para-el-socio");
            return ResponseEntity.ok(response);
        }
        return ResponseEntity.status(401).body("Credenciales inválidas o cuenta no activada");
    }
}