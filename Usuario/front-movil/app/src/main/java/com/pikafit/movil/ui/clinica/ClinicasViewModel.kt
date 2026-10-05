package com.pikafit.movil.ui.clinica

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.pikafit.movil.data.ClinicaPublica
import com.pikafit.movil.data.ClinicaRepository
import com.pikafit.movil.data.ClinicaResult
import com.pikafit.movil.network.ApiClient
import kotlinx.coroutines.launch

sealed interface ClinicasEstado {
    data object Cargando : ClinicasEstado
    data class Listo(val clinicas: List<ClinicaPublica>) : ClinicasEstado
    data class Error(val mensaje: String) : ClinicasEstado
}

class ClinicasViewModel(
    private val repositorio: ClinicaRepository =
        ClinicaRepository(ApiClient.http, ApiClient.baseUrl)
) : ViewModel() {
    var estado by mutableStateOf<ClinicasEstado>(ClinicasEstado.Cargando)
        private set

    init { cargar() }

    fun cargar() {
        estado = ClinicasEstado.Cargando
        viewModelScope.launch {
            estado = when (val resultado = repositorio.listarActivas()) {
                is ClinicaResult.Exito -> ClinicasEstado.Listo(resultado.clinicas)
                is ClinicaResult.Error -> ClinicasEstado.Error(resultado.mensaje)
            }
        }
    }
}
