package com.pikafit.movil.data

import com.pikafit.movil.network.ApiClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.Request
import org.json.JSONObject

data class EstadoMembresia(
    val estado: String,
    val fechaFin: String?,
    val mensaje: String
)

sealed interface ResultadoMembresia {
    data class Exito(val estado: EstadoMembresia) : ResultadoMembresia
    data class Error(val mensaje: String) : ResultadoMembresia
}

class MembresiaRepository {
    suspend fun consultar(token: String): ResultadoMembresia = withContext(Dispatchers.IO) {
        val request = Request.Builder()
            .url("${ApiClient.baseUrl.trimEnd('/')}/api/v1/membresia/estado")
            .header("Authorization", "Bearer $token")
            .get()
            .build()

        try {
            ApiClient.http.newCall(request).execute().use { response ->
                val body = response.body?.string().orEmpty()
                if (!response.isSuccessful) {
                    val mensaje = runCatching { JSONObject(body).optString("mensaje") }
                        .getOrDefault("No se pudo consultar la membresía (${response.code}).")
                    return@withContext ResultadoMembresia.Error(mensaje)
                }
                val json = JSONObject(body)
                ResultadoMembresia.Exito(
                    EstadoMembresia(
                        estado = json.optString("estado", "DESCONOCIDO"),
                        fechaFin = json.optString("fechaFin").takeIf { it.isNotBlank() && it != "null" },
                        mensaje = json.optString("mensaje", "No se recibió el estado de la membresía.")
                    )
                )
            }
        } catch (_: Exception) {
            ResultadoMembresia.Error("No se pudo conectar con PikaFit. Revisa tu conexión e inténtalo otra vez.")
        }
    }
}
