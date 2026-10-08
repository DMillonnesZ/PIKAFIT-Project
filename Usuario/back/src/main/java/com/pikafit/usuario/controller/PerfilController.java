package com.pikafit.usuario.controller;

import com.pikafit.usuario.dto.PerfilRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/perfil")
public class PerfilController {

    @PostMapping("/guardar")
    public ResponseEntity<?> guardarPerfil(@RequestBody PerfilRequest request) {
        if (request.getObjetivo() == null || request.getNivelExperiencia() == null ||
                request.getTallaCm() == null || request.getPesoKg() == null) {
            return ResponseEntity.badRequest().body("Todos los campos son obligatorios para generar rutinas");
        }
        return ResponseEntity.ok("Perfil actualizado correctamente");
    }
}