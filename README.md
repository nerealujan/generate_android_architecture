# 🛠️ Android Project Architecture Script 
Automatiza y optimiza la configuración de proyectos Android con este script, diseñado para facilitar el trabajo de los desarrolladores 🚀.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)  
[![Android](https://img.shields.io/badge/android-11+-green.svg)](https://developer.android.com/)  
[![License: CC BY-NC](https://img.shields.io/badge/License-CC--BY--NC-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---  

### 🌟 **Características**  

✅ Configuración de Arquitecturas

- Crea estructuras completas para MVP, MVVM y MVI.
- Genera carpetas y clases base según la arquitectura seleccionada.
- Detección y eliminación de arquitecturas previas: Si ya existe una arquitectura (ej. MVP) y seleccionas una diferente (ej. MVVM), el script borrará automáticamente las carpetas y archivos relacionados con la arquitectura anterior antes de establecer la nueva configuración.
  
✅ Gestión de Dependencias
- Añade dependencias automáticamente en:
  - build.gradle(.kts)
  - libs.versions.toml (si está disponible).
- Gestiona versiones de librerías en la sección [versions].
- Si no existe el archivo libs.versions.toml, el script permite al usuario decidir si desea crearlo. Si no lo desea, las dependencias se añadirán al build.gradle(.kts) en el formato clásico.
- Elimina duplicados automáticamente.
  
✅ Configuración del Proyecto
- Configura permisos de forma interactiva para el archivo AndroidManifest.xml.
- Crea actividades predeterminadas como SplashActivity.
  
✅ Menú Interactivo
- Permite personalizar cada aspecto del proyecto según tus necesidades.
- Opciones de proyecto: XML o Jetpack Compose.

---  

### 📋 **Requisitos previos**  

1. 🐍 Python 3.6 o superior.
2. 🏗️ Un proyecto Android base con los archivos settings.gradle(.kts) y build.gradle(.kts).
3. ✍️ Permisos de escritura en el proyecto Android.

---  

### ⚙️ **Instalación**  

1. **Clona este repositorio**:  

    ```bash
    git clone https://github.com/<tu-usuario>/android-project-architecture-script.git
    cd android-project-architecture-script  
    ```  

2. **Instala las dependencias necesarias (si las hay)**:  

    ```bash
    pip install -r requirements.txt
    ```
3. **Asegúrate de que tienes permisos de escritura en el proyecto Android**

---  

### 🛠️ **Cómo Usar**

1. **Ejecuta el script principal**:

   ```bash
   python3 main.py
   ```
2. **Sigue el menú interactivo para**:
   - **Introduce la ruta del proyecto y el nombre del paquete**:
     - Al iniciar el script, se te pedirá que indiques:
       ```plaintext
       Introduce la ruta completa del proyecto Android: /Users/tu_usuario/AndroidProjects/MyApp (o donde lo tengas configurado)
       Introduce el nombre del paquete base (e.g., com.example.myapp): com.example.myapp
       ```
       Esto permite que el script configure correctamente las rutas internas del proyecto.

   - **Configurar la arquitectura del proyecto**: 
     Selecciona entre MVP, MVVM o MVI, y el script generará las carpetas y clases base según la arquitectura elegida.
     
   - **Configurar el tipo de proyecto (XML o Compose)**: 
     En base a tu elección, el script ajustará las dependencias en libs.versions.toml y build.gradle(.kts) o solo en build.gradle(.kts).
     
   - **Añadir dependencias al proyecto**: 
     Añade dependencias esenciales como Kotlin Coroutines, Lifecycle ViewModel, Room, entre otras, y configúralas automáticamente en libs.versions.toml y build.gradle.
     
   - **Gestionar permisos en el AndroidManifest.xml**: 
     Permite gestionar permisos como INTERNET, CAMERA o ACCESS_FINE_LOCATION, añadiéndolos al manifiesto de forma interactiva

---

### 📂 **Estructura Generada**

Ejemplo: Arquitectura MVVM

```plaintext
📦 MyApp  
 ┣ 📂 app  
 ┃ ┣ 📂 src  
 ┃ ┃ ┣ 📂 main  
 ┃ ┃ ┃ ┣ 📂 java  
 ┃ ┃ ┃ ┃ ┗ 📂 com/example/myapp  
 ┃ ┃ ┃ ┃   ┣ 📂 model  
 ┃ ┃ ┃ ┃   ┣ 📂 view  
 ┃ ┃ ┃ ┃   ┗ 📂 viewmodel  
 ┃ ┃ ┃ ┣ 📂 res  
 ┃ ┃ ┃ ┃ ┣ 📂 drawable  
 ┃ ┃ ┃ ┃ ┣ 📂 values  
 ┃ ┃ ┃ ┃ ┗ 📂 layout  
 ┃ ┣ 📜 build.gradle.kts  
 ┃ ┗ 📜 proguard-rules.pro  
 ┣ 📂 gradle  
 ┃ ┗ 📜 libs.versions.toml  
 ┣ 📜 build.gradle.kts  
 ┣ 📜 gradle.properties  
 ┗ 📜 settings.gradle.kts  
```

---

### 📜 **Ejemplo de Dependencias**

En libs.versions.toml: Si seleccionas que el archivo libs.versions.toml se crea automáticamente, las dependencias se estructurarán de la siguiente manera:

```toml
[versions]
kotlin = "1.7.21"
room = "2.5.2"

[libraries]
kotlinx-coroutines-core = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-core", version = "1.7.1" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
```

En build.gradle.kts

```kotlin
dependencies {
    implementation(libs.kotlinx.coroutines.core)
    implementation(libs.room.ktx)
}
```

---

### 🛡️ **Gestión de permisos en el AndroidManifest.xml**:

1. Interfaz de selección:
```plaintext
Selecciona los permisos que necesita tu aplicación:  
1. INTERNET  
2. ACCESS_FINE_LOCATION  
3. CAMERA  
...  
Ingresa el número correspondiente o 0 para finalizar: 1
```
Nota: Si introduces 0, el script asumirá que no deseas añadir permisos adicionales.
   
2. Salida esperada en el AndroidManifest.xml:

```xml
<uses-permission android:name="android.permission.INTERNET" />  
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

 ---

### 💡 **Consideraciones**:

1. **Detección de duplicados**:
   - El script valida automáticamente si las dependencias o permisos ya existen antes de añadirlos.
   - Las dependencias duplicadas no se añadirán ni al archivo libs.versions.toml ni al build.gradle(.kts).
2. **Elección del archivo libs.versions.toml**:
   - Si el archivo no existe, el script preguntará si deseas crearlo.
   - Si decides no crearlo, las dependencias se añadirán al archivo build.gradle(.kts) en el formato clásico:
     ```kotlin
     implementation("group:name:version")
     ```
3. **Cambio de arquitectura**:
   - Si ya existe una arquitectura configurada y seleccionas una nueva, el script eliminará las carpetas de la arquitectura anterior antes de generar la nueva estructura.

---

### 📄 **Licencia**

Este proyecto está licenciado bajo la Licencia Creative Commons BY-NC 4.0.  
Puedes consultar más detalles en el archivo [LICENSE](LICENSE).  

**Nota:** No se permite el uso comercial de este proyecto sin la autorización previa del autor.

---

### 📞 **Contacto**

Si tienes preguntas, sugerencias o quieres colaborar, no dudes en ponerte en contacto conmigo a través de mi perfil de LinkedIn:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nerea%20Luján%20Pintado-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/nerea-lujan-pintado/)


















