package com.pikafit.usuario.controller;

import com.pikafit.usuario.dto.ConsentRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/consent")
public class ConsentController {

    @PostMapping("/accept")
    public ResponseEntity<?> acceptConsent(@RequestBody ConsentRequest request) {
        if (request.getSocioId() == null) {
            return ResponseEntity.badRequest().body("Socio ID es requerido");
        }

        if (!request.isAceptado()) {
            return ResponseEntity.badRequest().body("Debe aceptar el consentimiento para continuar");
        }

        Map<String, Object> response = new HashMap<>();
        response.put("status", "success");
        response.put("fechaAceptacion", LocalDateTime.now().toString());
        response.put("versionTexto", "v1.0");
        return ResponseEntity.ok(response);
    }
}