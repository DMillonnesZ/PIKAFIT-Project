# Documentación de la API - PikaFit (Módulo Usuario)

Esta es la documentación técnica de los endpoints desarrollados para el Sprint 1 en el módulo de Usuario, correspondientes a las Historias de Usuario asignadas a Luis Antonio Vasquez Flores.

## 1. Autenticación (HU-002)
- **POST** `/api/auth/login-socio`
    - **Body:** `{ "dni": "12345678", "googleToken": "token-valido" }`
    - **Respuesta exitosa (200):** `{ "status": "success", "token": "jwt-token-simulado..." }`
    - **Respuesta error (401):** `"Credenciales inválidas o cuenta no activada"`

## 2. Consentimiento de Datos (HU-013)
- **POST** `/api/consent/accept`
    - **Body:** `{ "socioId": "1", "aceptado": true }`
    - **Respuesta exitosa (200):** `{ "status": "success", "fechaAceptacion": "2026-10-XX...", "versionTexto": "v1.0" }`

## 3. Perfil del Socio (HU-058)
- **POST** `/api/perfil/guardar`
    - **Body:** `{ "objetivo": "Ganar músculo", "nivelExperiencia": "Intermedio", "tallaCm": 175.0, "pesoKg": 70.0 }`
    - **Respuesta exitosa (200):** `"Perfil actualizado correctamente"`
    - **Respuesta error (400):** `"Todos los campos son obligatorios para generar rutinas"`

## 4. Generación de Pase QR (HU-009)
- **POST** `/api/pases/generar`
    - **Body:** `{ "socioId": "1" }`
    - **Respuesta exitosa (200):** `{ "tokenQr": "uuid...", "codigoAlternativo": "ABC123", "expiracionMinutos": 15, "estado": "ACTIVO" }`

## 5. Validación en Recepción (HU-011)
- **POST** `/api/recepcion/validar-pase`
    - **Body:** `{ "tokenQr": "uuid...", "codigoAlternativo": "ABC123" }`
    - **Respuesta exitosa (200):** `{ "autorizado": true, "mensaje": "Autorizado para atención médica", "socioNombre": "Luis Vasquez" }`
    - **Respuesta error (422):** `"Pase inválido o expirado"`