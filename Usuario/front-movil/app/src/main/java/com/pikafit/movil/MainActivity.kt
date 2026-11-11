package com.pikafit.movil

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.pikafit.movil.ui.login.LoginScreen
import com.pikafit.movil.ui.theme.PikaFitTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            PikaFitTheme {
                LoginScreen()
            }
        }
    }
}