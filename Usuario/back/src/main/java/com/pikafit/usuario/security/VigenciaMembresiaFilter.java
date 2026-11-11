package com.pikafit.usuario.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.pikafit.usuario.socio.dto.EstadoMembresiaResponse;
import com.pikafit.usuario.socio.service.IdentidadSocioService;
import com.pikafit.usuario.socio.service.VigenciaMembresiaService;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Map;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.web.filter.OncePerRequestFilter;

public class VigenciaMembresiaFilter extends OncePerRequestFilter {
    private final IdentidadSocioService identidad;
    private final VigenciaMembresiaService vigencia;
    private final ObjectMapper json;

    public VigenciaMembresiaFilter(IdentidadSocioService identidad,
                                   VigenciaMembresiaService vigencia,
                                   ObjectMapper json) {
        this.identidad = identidad;
        this.vigencia = vigencia;
        this.json = json;
    }

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        String path = request.getRequestURI();
        if (!path.startsWith("/api/") || "OPTIONS".equalsIgnoreCase(request.getMethod())) return true;
        return path.equals("/api/v1/membresia/estado")
                || path.equals("/api/auth/login-socio")
                || path.equals("/api/auth/logout")
                || path.startsWith("/api/perfil/")
                || path.startsWith("/api/v1/membresia/renovacion");
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated() || auth instanceof AnonymousAuthenticationToken) {
            filterChain.doFilter(request, response);
            return;
        }

        var socio = identidad.buscar(auth.getName());
        EstadoMembresiaResponse estado = socio.map(vigencia::consultar).orElseGet(() ->
                new EstadoMembresiaResponse("SOCIO_NO_IDENTIFICADO", null,
                        "La sesión no corresponde a un socio registrado."));
        if (!"VIGENTE".equals(estado.estado())) {
            response.setStatus(HttpServletResponse.SC_FORBIDDEN);
            response.setContentType("application/json");
            response.setCharacterEncoding("UTF-8");
            json.writeValue(response.getOutputStream(), Map.of(
                    "codigo", "MEMBRESIA_NO_VIGENTE",
                    "estado", estado.estado(),
                    "fechaFin", estado.fechaFin() == null ? "" : estado.fechaFin().toString(),
                    "mensaje", estado.mensaje()));
            return;
        }
        filterChain.doFilter(request, response);
    }
}
