package com.pikafit.movil.ui.clinica

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun ClinicasScreen(viewModel: ClinicasViewModel = viewModel()) {
    Column(
        modifier = Modifier.fillMaxSize().padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        Text("Clínicas afiliadas")
        Text("Lugares activos donde puedes solicitar atención médica.")
        when (val estado = viewModel.estado) {
            ClinicasEstado.Cargando -> CircularProgressIndicator(
                modifier = Modifier.align(Alignment.CenterHorizontally)
            )
            is ClinicasEstado.Error -> {
                Text(estado.mensaje)
                Button(onClick = viewModel::cargar) { Text("Reintentar") }
            }
            is ClinicasEstado.Listo -> {
                if (estado.clinicas.isEmpty()) Text("No hay clínicas afiliadas activas.")
                else LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    items(estado.clinicas, key = { it.id }) { clinica ->
                        Card(modifier = Modifier.fillMaxWidth()) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text(clinica.razonSocial)
                                Text(clinica.direccion)
                                Text("Teléfono: " + clinica.telefono)
                            }
                        }
                    }
                }
            }
        }
    }
}
