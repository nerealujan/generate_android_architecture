import os
from generate_android_architecture import *

def main() -> None:
    """Punto de entrada del script."""
    print("=" * 50)
    """
    Añade la arquitectura deseada a un proyecto Android ya existente.
    """
    print("Bienvenido al configurador de arquitecturas para tu proyecto Android.")
    print("=" * 50)
    try:
        # Entrada de datos
        project_directory = input("Introduce la ruta completa del proyecto Android: ").strip()
       
        # Solicitar el nombre del paquete base
        package_name = input("Introduce el nombre del paquete base (e.g., com.ejemplo.app): ").strip()
        if not is_valid_package_name(package_name):
            print("El nombre del paquete no es válido. Asegúrate de que sigue el formato correcto (e.g., com.example.app).")
            return

        # Selección de arquitectura
        architecture = get_architecture_choice()
        if not architecture:
            print("Opción no válida.")
            return
        
        # Selección del tipo de proyecto
        print("\n¿Es un proyecto en XML o en Compose?")
        print("1. XML (Vista tradicional con View Binding)")
        print("2. Compose (Jetpack Compose)")
        project_type = input("Ingresa el número correspondiente: ").strip()
        use_compose = project_type == "2"
    
        
        # Crear proyecto base
        print("\nCreando proyecto...")

        # Generar estructura según arquitectura
        print("Generando arquitectura...")
        
        # Añadir arquitectura
        add_architecture_to_existing_project(project_directory, architecture, use_compose, package_name)

        #Mostrar dependencias
        dependenciesGroup = show_dependencies(use_compose)
        get_dependencies(dependenciesGroup, project_directory)

        print(f"\nArquitectura {architecture} configurada exitosamente en el proyecto ubicado en: {project_directory}")

    except Exception as e:
        print(f"Error: {e}")

def show_dependencies(use_compose):
    # Dependencias organizadas por categorías
        print("\nSelecciona las dependencias que deseas añadir:")
        dependencies = {
            1: {
            "Kotlin Coroutines": [
                "org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.1",
                "org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3",]
            },
            2: {
                "Lifecycle ViewModel y LiveData": [
                    "androidx.lifecycle:lifecycle-viewmodel-ktx:2.6.1",
                    "androidx.lifecycle:lifecycle-livedata-ktx:2.6.1",
                ]
            },
            3: {
                "Room KTX": [
                    "androidx.room:room-ktx:2.5.2",
                    "androidx.room:room-runtime:2.5.2",
                ]
            },
            4: {
                "OkHttp": [
                    "com.squareup.okhttp3:okhttp:4.9.3",
                    "com.squareup.okhttp3:logging-interceptor:4.10.0",
                ]
            },
            5: {
                "Glide": [
                    "com.github.bumptech.glide:glide:4.12.0",
                ]
            },
            6: {
                "WorkManager": [
                    "androidx.work:work-runtime-ktx:2.8.0",
                ]
            },
            7: {
                "Timber": [
                    "com.jakewharton.timber:timber:5.0.1",
                ]
            },
            8: {
                "ConstraintLayout": [
                    "androidx.constraintlayout:constraintlayout:2.1.3",
                ]
            },
            9: {
                "Jetpack Compose": [
                    "androidx.compose.ui:ui:1.5.3",
                    "androidx.compose.material:material:1.5.3",
                ] if use_compose else [],
            },
            10: {
                "Testing JUnit": [
                    "junit:junit:4.13.2",
                    "androidx.test.ext:junit:1.1.3",
                ]
            },
            11: {
                "JUnit 5": [
                    "org.junit.jupiter:junit-jupiter-api:5.10.0",
                    "org.junit.jupiter:junit-jupiter-engine:5.10.0",
                ]
            },
            12: {
                "Navigation Safe Args": [
                    "androidx.navigation:navigation-safe-args-gradle-plugin:2.7.3",
                    "androidx.navigation:navigation-fragment-ktx:2.7.3",
                    "androidx.navigation:navigation-ui-ktx:2.7.3",
                ]
            },
            13: {
                "Firebase": [
                    "com.google.firebase:firebase-bom:29.0.0",
                    "com.google.firebase:firebase-analytics-ktx",
                ]
            },
            14: {
                "Retrofit Converters": [
                    "com.squareup.retrofit2:retrofit:2.9.0",
                    "com.squareup.retrofit2:converter-moshi:2.9.0",
                ]
            },
            15: {
                "Material Design Icons": [
                    "com.google.android.material:material-icons-extended:1.9.0",
                ]
            },
            16: {
                "Anko": [
                    "org.jetbrains.anko:anko:0.10.8",
                ]
            },
            17: {
                "Dagger": [
                    "com.google.dagger:hilt-android:2.47",
                    "kapt com.google.dagger:hilt-compiler:2.47",
                ]
            },
            18: {
                "MockK": [
                    "io.mockk:mockk:1.13.5",
                    "io.mockk:mockk-android:1.13.3",
                    ]
            },
            19: {
                "Mockito": [
                    "org.mockito:mockito-core:4.11.0",
                    "org.mockito.kotlin:mockito-kotlin:4.1.0",
                    "org.mockito:mockito-android:4.11.0",
                    "org.mockito:mockito-inline:4.11.0"
                ]
            },
            20: {
                "JetBrains Annotations": [
                    "org.jetbrains:annotations:24.0.1",
                ]
            },
            21: {
                "Espresso": [
                    "androidx.test.espresso:espresso-core:3.5.1",
                    "androidx.test.espresso:espresso-contrib:3.5.1",
                    "androidx.test.espresso:espresso-intents:3.5.1",
                ]
            },
            22: {
                "Robolectric": [
                    "org.robolectric:robolectric:4.9",
                ]
            },
            23: {
                "Hamcrest": [
                    "org.hamcrest:hamcrest:2.2",
                ]
            },
            24: {
                 "Kotlin Test": [
                    "org.jetbrains.kotlin:kotlin-test:1.9.0"
                ]
            },
            25: {
                 "Moshi": [
                    "com.squareup.moshi:moshi-kotlin:1.15.0"
                ]
            },
            26: {
                 "Gson": [
                    "com.google.code.gson:gson:2.10"
                ]
            },
            27: {
                 "Ktor Client": [
                    "io.ktor:ktor-client-android:2.3.3" 
                ]
            },
            28: {
                 "ViewPager2": [
                    "androidx.viewpager2:viewpager2:1.1.0"
                 ]
            },
            29: {
                 "DataStore":[
                    "androidx.datastore:datastore-preferences:1.0.0"
                ]
            },
            30: {
                 "Tink":[
                    "com.google.crypto.tink:tink-android:1.7.0"
                ]
            },
            31: {
                 "Secure Preferences":[
                    "com.scottyab:secure-preferences-lib:0.1.4"
                ]
            },
            32: {
                 "Coil":[
                    "io.coil-kt:coil:2.4.0"
                ]
            },
            33: {
                 "Lottie":[
                    "com.airbnb.android:lottie:6.0.0"
                ]
            },
            34: {
                 "Crashlytics":[
                    "com.google.firebase:firebase-crashlytics-ktx"
                ]
            },
            35: {
                 "LeakCanary":[
                    "com.squareup.leakcanary:leakcanary-android:2.10"
                ]
            },
            36: {
                 "Kotlin Reflect":[
                    "org.jetbrains.kotlin:kotlin-reflect:1.9.0"
                ]
            },
            37: {
                 "Hilt Testing":[
                    "com.google.dagger:hilt-android-testing:2.47"
                ]
            },
        }
        return dependencies

if __name__ == "__main__":
    main()