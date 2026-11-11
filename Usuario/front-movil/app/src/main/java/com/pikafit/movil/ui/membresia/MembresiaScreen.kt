package com.pikafit.movil.ui.membresia

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun MembresiaScreen(
    token: String,
    onCerrarSesion: () -> Unit,
    contenidoSocio: @Composable () -> Unit,
    viewModel: MembresiaViewModel = viewModel()
) {
    LaunchedEffect(token) { viewModel.cargar(token) }
    when (val state = viewModel.state) {
        MembresiaUiState.Cargando -> PantallaEstado("Consultando tu membresía…", cargando = true)
        is MembresiaUiState.Error -> PantallaError(state.mensaje, onRetry = { viewModel.cargar(token) }, onCerrarSesion)
        is MembresiaUiState.Listo -> when (state.estado.estado) {
            "VIGENTE" -> contenidoSocio()
            "VENCIDA" -> PantallaVencida(
                fechaFin = state.estado.fechaFin ?: "No disponible",
                mensaje = state.estado.mensaje,
                onCerrarSesion = onCerrarSesion
            )
            else -> PantallaError(state.estado.mensaje, onRetry = { viewModel.cargar(token) }, onCerrarSesion)
        }
    }
}

@Composable
private fun PantallaVencida(fechaFin: String, mensaje: String, onCerrarSesion: () -> Unit) {
    var mostrarRenovacion by remember { mutableStateOf(false) }
    var mostrarPerfil by remember { mutableStateOf(false) }

    if (mostrarRenovacion) {
        AlertDialog(
            onDismissRequest = { mostrarRenovacion = false },
            title = { Text("Renueva tu membresía") },
            text = { Text("Solicita la renovación en la recepción de tu gimnasio. Cuando Administración active el nuevo periodo, vuelve a ingresar a PikaFit.") },
            confirmButton = { TextButton(onClick = { mostrarRenovacion = false }) { Text("Entendido") } }
        )
    }
    if (mostrarPerfil) {
        AlertDialog(
            onDismissRequest = { mostrarPerfil = false },
            title = { Text("Mi perfil") },
            text = { Text("El acceso al perfil se mantiene disponible. La vista completa se conectará al módulo de perfil del socio (HU-058).") },
            confirmButton = { TextButton(onClick = { mostrarPerfil = false }) { Text("Cerrar") } }
        )
    }

    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(24.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text("Membresía vencida", style = MaterialTheme.typography.headlineSmall)
                Text("Tu membresía venció el $fechaFin.", style = MaterialTheme.typography.titleMedium)
                Text(mensaje)
                Text("Mientras esté vencida, las funciones de entrenamiento y salud permanecerán bloqueadas.")
                Button(onClick = { mostrarRenovacion = true }, modifier = Modifier.fillMaxWidth()) {
                    Text("Cómo renovar")
                }
                OutlinedButton(onClick = { mostrarPerfil = true }, modifier = Modifier.fillMaxWidth()) {
                    Text("Mi perfil")
                }
                TextButton(onClick = onCerrarSesion, modifier = Modifier.align(Alignment.CenterHorizontally)) {
                    Text("Cerrar sesión")
                }
            }
        }
    }
}

@Composable
private fun PantallaEstado(mensaje: String, cargando: Boolean = false) {
    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        if (cargando) CircularProgressIndicator()
        Text(mensaje, modifier = Modifier.padding(top = 16.dp))
    }
}

@Composable
private fun PantallaError(mensaje: String, onRetry: () -> Unit, onCerrarSesion: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("No pudimos validar tu membresía", style = MaterialTheme.typography.headlineSmall)
        Text(mensaje, modifier = Modifier.padding(vertical = 12.dp))
        Button(onClick = onRetry) { Text("Intentar de nuevo") }
        TextButton(onClick = onCerrarSesion) { Text("Cerrar sesión") }
    }
}
