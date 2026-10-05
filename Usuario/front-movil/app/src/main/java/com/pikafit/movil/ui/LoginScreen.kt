package com.pikafit.movil.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun LoginScreen() {
    var dni by remember { mutableStateOf("") }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text("Ingreso de Socio PikaFit", fontSize = 24.sp)
        Spacer(modifier = Modifier.height(24.dp))

        OutlinedTextField(
            value = dni,
            onValueChange = { dni = it },
            label = { Text("Ingresa tu DNI") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = { /* Aquí irá la lógica de Google Sign-In */ },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Continuar con Google")
        }
    }
}