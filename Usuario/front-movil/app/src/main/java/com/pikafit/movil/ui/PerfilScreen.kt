package com.pikafit.movil.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun PerfilScreen(onGuardar: () -> Unit) {
    var objetivo by remember { mutableStateOf("") }
    var nivel by remember { mutableStateOf("") }
    var talla by remember { mutableStateOf("") }
    var peso by remember { mutableStateOf("") }

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Configura tu Perfil", fontSize = 24.sp)
        Spacer(modifier = Modifier.height(16.dp))

        // Campo: Objetivo
        OutlinedTextField(
            value = objetivo,
            onValueChange = { objetivo = it },
            label = { Text("Objetivo (Ej. Ganar músculo)") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))

        // Campo: Nivel de experiencia
        OutlinedTextField(
            value = nivel,
            onValueChange = { nivel = it },
            label = { Text("Nivel (Principiante/Intermedio/Avanzado)") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))

        // Campo: Talla
        OutlinedTextField(
            value = talla,
            onValueChange = { talla = it },
            label = { Text("Talla (cm)") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))

        // Campo: Peso
        OutlinedTextField(
            value = peso,
            onValueChange = { peso = it },
            label = { Text("Peso (kg)") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(24.dp))

        Button(onClick = onGuardar, modifier = Modifier.fillMaxWidth()) {
            Text("Guardar Perfil")
        }
    }
}