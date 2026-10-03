package com.pikafit.movil.ui.health

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun HealthScreen(viewModel: HealthViewModel = viewModel()) {
    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Button(onClick = viewModel::check) {
            Text("Probar conexión con la API")
        }
        Text(
            modifier = Modifier.padding(top = 16.dp),
            text = when (val s = viewModel.state) {
                HealthUiState.Idle -> "Sin comprobar"
                HealthUiState.Loading -> "Consultando..."
                is HealthUiState.Done -> s.text
            }
        )
    }
}