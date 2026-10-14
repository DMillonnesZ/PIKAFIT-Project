package com.pikafit.usuario.controller;

import com.pikafit.usuario.dto.ValidacionRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/recepcion")
public class RecepcionController {

    @PostMapping("/validar-pase")
    public ResponseEntity<?> validarPase(@RequestBody ValidacionRequest request) {
        if (request.getTokenQr() == null && request.getCodigoAlternativo() == null) {
            return ResponseEntity.badRequest().body("Debe proporcionar un QR o código alternativo");
        }

        // Simulamos la validación en base de datos
        // En un caso real, aquí se buscaría el token, se verificaría si expiró o ya se usó
        boolean esValido = true;

        if (esValido) {
            Map<String, Object> response = new HashMap<>();
            response.put("autorizado", true);
            response.put("mensaje", "Autorizado para atención médica");
            response.put("socioNombre", "Luis Vasquez");
            response.put("fechaValidacion", LocalDateTime.now().toString());
            return ResponseEntity.ok(response);
        } else {
            // Criterio de aceptación: Pase inválido o expirado
            return ResponseEntity.status(422).body("Pase inválido o expirado");
        }
    }
}