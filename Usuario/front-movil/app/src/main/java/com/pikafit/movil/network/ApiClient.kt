package com.pikafit.movil.network

import com.pikafit.movil.BuildConfig
import java.util.concurrent.TimeUnit
import okhttp3.OkHttpClient

object ApiClient {
    val baseUrl: String = BuildConfig.API_BASE_URL

    val http: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(5, TimeUnit.SECONDS)
        .readTimeout(5, TimeUnit.SECONDS)
        .build()
}