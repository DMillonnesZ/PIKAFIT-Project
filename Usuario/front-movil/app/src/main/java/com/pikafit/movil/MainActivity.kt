package com.pikafit.movil

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.pikafit.movil.ui.clinica.ClinicasScreen
import com.pikafit.movil.ui.health.HealthScreen
import com.pikafit.movil.ui.theme.PikaFitTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            PikaFitTheme {
                var seccion by remember { mutableStateOf("clinicas") }
                Column(modifier = Modifier.fillMaxSize()) {
                    Row(modifier = Modifier.fillMaxWidth()) {
                        Button(onClick = { seccion = "clinicas" }) { Text("Clínicas") }
                        Button(onClick = { seccion = "conexion" }) { Text("Conexión") }
                    }
                    Box(modifier = Modifier.weight(1f)) {
                        if (seccion == "clinicas") ClinicasScreen()
                        else HealthScreen()
                    }
                }
            }
        }
    }
}
