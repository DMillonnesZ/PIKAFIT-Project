package com.pikafit.usuario.controller;

import com.pikafit.usuario.dto.PaseQrRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.UUID;

@RestController
@RequestMapping("/api/pases")
public class PaseQrController {

    @PostMapping("/generar")
    public ResponseEntity<?> generarPase(@RequestBody PaseQrRequest request) {
        if (request.getSocioId() == null) {
            return ResponseEntity.badRequest().body("Socio ID es requerido");
        }

        // Lógica de negocio de la HU: Token aleatorio y código alternativo de 6 caracteres
        String tokenQr = UUID.randomUUID().toString();
        String codigoAlternativo = generarCodigo6Caracteres();

        Map<String, Object> response = new HashMap<>();
        response.put("tokenQr", tokenQr);
        response.put("codigoAlternativo", codigoAlternativo);
        response.put("expiracionMinutos", 15); // Viene de configuración (HU-060)
        response.put("estado", "ACTIVO");

        return ResponseEntity.ok(response);
    }

    private String generarCodigo6Caracteres() {
        String caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        StringBuilder codigo = new StringBuilder();
        Random rnd = new Random();
        while (codigo.length() < 6) {
            int index = (int) (rnd.nextFloat() * caracteres.length());
            codigo.append(caracteres.charAt(index));
        }
        return codigo.toString();
    }
}