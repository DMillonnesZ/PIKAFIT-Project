package com.pikafit.movil.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun ConsentScreen(onAccept: () -> Unit, onDecline: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Consentimiento de Datos de Salud", fontSize = 22.sp)
        Spacer(modifier = Modifier.height(16.dp))

        Text(
            "Para brindarte un entrenamiento seguro, PikaFit analizará tus datos de salud (restricciones físicas y diagnóstico) mediante Inteligencia Artificial (LLM externo) sin compartir tu nombre ni DNI. " +
                    "Puedes revocar este consentimiento en cualquier momento desde tu perfil.",
            fontSize = 16.sp
        )
        Spacer(modifier = Modifier.height(32.dp))

        Button(
            onClick = onAccept,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Acepto y continúo")
        }

        Spacer(modifier = Modifier.height(8.dp))

        OutlinedButton(
            onClick = onDecline,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Rechazar (Solo usaré el perfil)")
        }
    }
}