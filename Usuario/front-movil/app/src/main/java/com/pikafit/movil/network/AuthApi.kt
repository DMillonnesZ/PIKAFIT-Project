package com.pikafit.movil.network

import com.pikafit.movil.model.LoginRequest
import com.pikafit.movil.model.LoginResponse
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface AuthApi {
    @POST("api/auth/login-socio")
    suspend fun loginSocio(@Body request: LoginRequest): Response<LoginResponse>
}