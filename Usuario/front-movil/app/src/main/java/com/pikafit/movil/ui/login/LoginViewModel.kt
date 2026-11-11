package com.pikafit.movil.ui.login

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.pikafit.movil.data.AuthRepository
import com.pikafit.movil.data.LoginResult
import com.pikafit.movil.network.ApiClient
import kotlinx.coroutines.launch

sealed interface LoginUiState {
    data object Idle : LoginUiState
    data object Loading : LoginUiState
    data class Success(val socioId: String) : LoginUiState
    data class Error(val message: String) : LoginUiState
}

class LoginViewModel(
    private val repository: AuthRepository = AuthRepository(ApiClient.authApi)
) : ViewModel() {

    var state by mutableStateOf<LoginUiState>(LoginUiState.Idle)
        private set

    fun login(dni: String, googleToken: String) {
        if (dni.length != 8 || !dni.all { it.isDigit() }) {
            state = LoginUiState.Error("El DNI debe tener 8 dígitos")
            return
        }
        state = LoginUiState.Loading
        viewModelScope.launch {
            state = when (val r = repository.loginSocio(dni, googleToken)) {
                is LoginResult.Success -> LoginUiState.Success(r.socioId)
                is LoginResult.Failure -> LoginUiState.Error(r.message)
            }
        }
    }
}