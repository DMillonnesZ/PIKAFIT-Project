package com.pikafit.usuario.service;

import com.google.api.client.googleapis.auth.oauth2.GoogleIdToken;
import com.google.api.client.googleapis.auth.oauth2.GoogleIdTokenVerifier;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.gson.GsonFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.List;
import java.util.Optional;

@Component
public class GoogleTokenVerifierImpl implements GoogleTokenVerifier {

    private final GoogleIdTokenVerifier verifier;

    public GoogleTokenVerifierImpl(@Value("${google.client-id:}") String clientId) {
        this.verifier = new GoogleIdTokenVerifier.Builder(new NetHttpTransport(), GsonFactory.getDefaultInstance())
                .setAudience(List.of(clientId))
                .build();
    }

    @Override
    public Optional<String> obtenerCorreo(String idToken) {
        try {
            GoogleIdToken token = verifier.verify(idToken);
            if (token == null || !Boolean.TRUE.equals(token.getPayload().getEmailVerified())) {
                return Optional.empty();
            }
            return Optional.ofNullable(token.getPayload().getEmail());
        } catch (IOException e) {
            throw new GoogleNoDisponibleException(e);
        } catch (GeneralSecurityException | IllegalArgumentException e) {
            return Optional.empty();
        }
    }
}