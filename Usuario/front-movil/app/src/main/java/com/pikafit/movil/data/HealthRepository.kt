package com.pikafit.movil.data

import java.io.IOException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request

sealed interface HealthResult {
    data class Success(val code: Int, val body: String) : HealthResult
    data class Failure(val message: String) : HealthResult
}

class HealthRepository(
    private val client: OkHttpClient,
    private val baseUrl: String
) {
    suspend fun check(): HealthResult = withContext(Dispatchers.IO) {
        try {
            val request = Request.Builder()
                .url(baseUrl + "actuator/health")
                .build()
            client.newCall(request).execute().use { response ->
                HealthResult.Success(response.code, response.body?.string().orEmpty())
            }
        } catch (e: IOException) {
            HealthResult.Failure(e.message ?: "Error de red")
        }
    }
}