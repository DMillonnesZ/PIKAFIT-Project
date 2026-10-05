package com.pikafit.movil.data

import java.io.IOException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONArray

data class ClinicaPublica(
    val id: String,
    val razonSocial: String,
    val direccion: String,
    val telefono: String
)

sealed interface ClinicaResult {
    data class Exito(val clinicas: List<ClinicaPublica>) : ClinicaResult
    data class Error(val mensaje: String) : ClinicaResult
}

class ClinicaRepository(
    private val cliente: OkHttpClient,
    private val baseUrl: String
) {
    suspend fun listarActivas(): ClinicaResult = withContext(Dispatchers.IO) {
        try {
            val peticion = Request.Builder()
                .url(baseUrl.trimEnd('/') + "/api/v1/clinicas")
                .build()
            cliente.newCall(peticion).execute().use { respuesta ->
                if (!respuesta.isSuccessful) {
                    return@withContext ClinicaResult.Error("No se pudieron cargar las clínicas.")
                }
                val arreglo = JSONArray(respuesta.body?.string().orEmpty())
                val clinicas = (0 until arreglo.length()).map { indice ->
                    val item = arreglo.getJSONObject(indice)
                    ClinicaPublica(
                        id = item.getString("id"),
                        razonSocial = item.getString("razon_social"),
                        direccion = item.getString("direccion"),
                        telefono = item.getString("telefono")
                    )
                }
                ClinicaResult.Exito(clinicas)
            }
        } catch (error: IOException) {
            ClinicaResult.Error("No hay conexión con el servidor.")
        } catch (error: org.json.JSONException) {
            ClinicaResult.Error("La lista de clínicas no se pudo leer.")
        }
    }
}
