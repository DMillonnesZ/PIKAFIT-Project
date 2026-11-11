package com.pikafit.movil.model

data class LoginRequest(
    val dni: String,
    val googleToken: String
)

data class LoginResponse(
    val status: String?,
    val socioId: String?,
    val mensaje: String?
)