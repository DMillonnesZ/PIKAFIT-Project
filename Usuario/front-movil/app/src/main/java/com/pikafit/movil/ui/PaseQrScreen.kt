package com.pikafit.movil.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun PaseQrScreen() {
    var tiempoRestante by remember { mutableStateOf(15) }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Pase de Atención Médica", fontSize = 24.sp)
        Spacer(modifier = Modifier.height(16.dp))

        // Simulación visual del QR
        Text("[ IMAGEN DEL CÓDIGO QR ]", fontSize = 18.sp, color = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.height(16.dp))

        Text("Código Alternativo: ABC123", fontSize = 18.sp)
        Spacer(modifier = Modifier.height(8.dp))

        Text("Vence en: $tiempoRestante minutos", fontSize = 16.sp, color = MaterialTheme.colorScheme.error)
        Spacer(modifier = Modifier.height(24.dp))

        Button(onClick = { /* Refrescar pase */ }, modifier = Modifier.fillMaxWidth()) {
            Text("Generar nuevo pase")
        }
    }
}