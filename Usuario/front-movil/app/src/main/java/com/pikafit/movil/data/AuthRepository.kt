package com.pikafit.movil.data

import com.google.gson.Gson
import com.pikafit.movil.model.LoginRequest
import com.pikafit.movil.model.LoginResponse
import com.pikafit.movil.network.AuthApi
import java.io.IOException

sealed interface LoginResult {
    data class Success(val socioId: String) : LoginResult
    data class Failure(val message: String) : LoginResult
}

class AuthRepository(private val api: AuthApi) {

    suspend fun loginSocio(dni: String, googleToken: String): LoginResult {
        return try {
            val response = api.loginSocio(LoginRequest(dni, googleToken))
            if (response.isSuccessful) {
                LoginResult.Success(response.body()?.socioId.orEmpty())
            } else {
                val raw = response.errorBody()?.string().orEmpty()
                val mensaje = try {
                    Gson().fromJson(raw, LoginResponse::class.java)?.mensaje
                } catch (e: Exception) { null }
                LoginResult.Failure(mensaje ?: "Error ${response.code()}")
            }
        } catch (e: IOException) {
            LoginResult.Failure("No se pudo conectar con el servidor")
        }
    }
}