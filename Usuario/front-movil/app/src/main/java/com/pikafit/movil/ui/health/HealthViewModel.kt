package com.pikafit.movil.ui.health

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.pikafit.movil.data.HealthRepository
import com.pikafit.movil.data.HealthResult
import com.pikafit.movil.network.ApiClient
import kotlinx.coroutines.launch

sealed interface HealthUiState {
    data object Idle : HealthUiState
    data object Loading : HealthUiState
    data class Done(val text: String) : HealthUiState
}

class HealthViewModel(
    private val repository: HealthRepository =
        HealthRepository(ApiClient.http, ApiClient.baseUrl)
) : ViewModel() {

    var state by mutableStateOf<HealthUiState>(HealthUiState.Idle)
        private set

    fun check() {
        state = HealthUiState.Loading
        viewModelScope.launch {
            state = when (val result = repository.check()) {
                is HealthResult.Success -> HealthUiState.Done("HTTP ${result.code}: ${result.body}")
                is HealthResult.Failure -> HealthUiState.Done("Error: ${result.message}")
            }
        }
    }
}