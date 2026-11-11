package com.pikafit.movil.data

import android.content.Context

/** Contrato de almacenamiento local para que HU-002 comparta el token con el control HU-003. */
class UsuarioSessionStore(context: Context) {
    private val preferences = context.getSharedPreferences("pikafit_session", Context.MODE_PRIVATE)

    fun accessToken(): String? = preferences.getString(KEY_ACCESS_TOKEN, null)

    fun guardarAccessToken(token: String) {
        preferences.edit().putString(KEY_ACCESS_TOKEN, token).apply()
    }

    fun cerrarSesion() {
        preferences.edit().remove(KEY_ACCESS_TOKEN).apply()
    }

    companion object {
        const val KEY_ACCESS_TOKEN = "access_token"
    }
}
