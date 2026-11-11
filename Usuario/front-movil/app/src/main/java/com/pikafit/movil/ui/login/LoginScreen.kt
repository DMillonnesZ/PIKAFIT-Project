package com.pikafit.movil.ui.login

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel

// Token de prueba: Credential Manager lo reemplazará en el siguiente commit.
private const val TOKEN_PRUEBA = "token-de-prueba"

@Composable
fun LoginScreen(
    viewModel: LoginViewModel = viewModel(),
    onLoginExitoso: (String) -> Unit = {}
) {
    var dni by remember { mutableStateOf("") }
    val state = viewModel.state

    LaunchedEffect(state) {
        if (state is LoginUiState.Success) onLoginExitoso(state.socioId)
    }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Ingreso de Socio PikaFit", fontSize = 24.sp)
        Spacer(modifier = Modifier.height(24.dp))

        OutlinedTextField(
            value = dni,
            onValueChange = { if (it.length <= 8) dni = it.filter { c -> c.isDigit() } },
            label = { Text("Ingresa tu DNI") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = { viewModel.login(dni, TOKEN_PRUEBA) },
            enabled = state !is LoginUiState.Loading,
            modifier = Modifier.fillMaxWidth()
        ) {
            if (state is LoginUiState.Loading) {
                CircularProgressIndicator(modifier = Modifier.size(20.dp), strokeWidth = 2.dp)
            } else {
                Text("Continuar con Google")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))
        when (state) {
            is LoginUiState.Error ->
                Text(state.message, color = MaterialTheme.colorScheme.error)
            is LoginUiState.Success ->
                Text("Ingreso correcto", color = MaterialTheme.colorScheme.primary)
            else -> {}
        }
    }
}