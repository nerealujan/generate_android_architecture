import os
from generate_android_architecture import *
from generate_dependencies import *

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
                "ConstraintLayout": [
                     "androidx.constraintlayout:constraintlayout-compose:1.0.1"
                ] if use_compose else [ 
                     "androidx.constraintlayout:constraintlayout:2.1.3",]
            },
            7: {
                "Testing JUnit": [
                    "junit:junit:4.13.2",
                ]
            },
            8: {
                "JUnit 5": [
                    "org.junit.jupiter:junit-jupiter-api:5.10.0",
                    "org.junit.jupiter:junit-jupiter-engine:5.10.0",
                ]
            },
            9: {
                "Firebase": [
                    "com.google.firebase:firebase-bom:29.0.0",
                    "com.google.firebase:firebase-analytics-ktx",
                ]
            },
            10: {
                "Retrofit": [
                    "com.squareup.retrofit2:retrofit:2.9.0",
                ]
            },
            11: {
                "Dagger": [
                    "com.google.dagger:hilt-android:2.47",
                    "com.google.dagger:hilt-compiler:2.47",
                    "com.google.dagger:hilt-android-testing:2.47"
                ]
            },
            12: {
                "MockK": [
                    "io.mockk:mockk:1.13.5",
                    "io.mockk:mockk-android:1.13.3",
                    ]
            },
            13: {
                "Mockito": [
                    "org.mockito:mockito-core:4.11.0",
                    "org.mockito.kotlin:mockito-kotlin:4.1.0",
                    "org.mockito:mockito-android:4.11.0"
                ]
            },
            14: {
                "Espresso": [
                    "androidx.test.espresso:espresso-contrib:3.5.1",
                    "androidx.test.espresso:espresso-intents:3.5.1",
                ]
            },
            15: {
                 "Moshi": [
                    "com.squareup.moshi:moshi-kotlin:1.15.0"
                ]
            },
            16: {
                 "Gson": [
                    "com.google.code.gson:gson:2.10"
                ]
            },
            17: {
                 "Ktor Client": [
                    "io.ktor:ktor-client-android:2.3.3" 
                ]
            },
            18: {
                 "ViewPager2": [
                    "androidx.viewpager2:viewpager2:1.1.0"
                 ]
            },
            19: {
                 "Secure Preferences":[
                    "com.scottyab:secure-preferences-lib:0.1.4"
                ]
            },
            20: {
                 "Coil":[
                    "io.coil-kt:coil:2.4.0"
                ]
            },
            21: {
                 "Lottie":[
                    "com.airbnb.android:lottie:6.0.0"
                ]
            },
            22: {
                 "Crashlytics":[
                    "com.google.firebase:firebase-crashlytics-ktx"
                ]
            },
        }
        return dependencies

if __name__ == "__main__":
    main()