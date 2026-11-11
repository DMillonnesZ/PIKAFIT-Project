package com.pikafit.movil.ui.membresia

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.pikafit.movil.data.EstadoMembresia
import com.pikafit.movil.data.MembresiaRepository
import com.pikafit.movil.data.ResultadoMembresia
import kotlinx.coroutines.launch

sealed interface MembresiaUiState {
    data object Cargando : MembresiaUiState
    data class Listo(val estado: EstadoMembresia) : MembresiaUiState
    data class Error(val mensaje: String) : MembresiaUiState
}

class MembresiaViewModel(
    private val repository: MembresiaRepository = MembresiaRepository()
) : ViewModel() {
    var state by mutableStateOf<MembresiaUiState>(MembresiaUiState.Cargando)
        private set

    fun cargar(token: String) {
        state = MembresiaUiState.Cargando
        viewModelScope.launch {
            state = when (val result = repository.consultar(token)) {
                is ResultadoMembresia.Exito -> MembresiaUiState.Listo(result.estado)
                is ResultadoMembresia.Error -> MembresiaUiState.Error(result.mensaje)
            }
        }
    }
}
