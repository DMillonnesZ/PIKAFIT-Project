package com.pikafit.movil

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.pikafit.movil.ui.health.HealthScreen
import com.pikafit.movil.ui.theme.PikaFitTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            PikaFitTheme {
                HealthScreen()
            }
        }
    }
}