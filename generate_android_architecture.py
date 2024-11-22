import os
import re
import shutil

def get_architecture_choice():
    print("\nSelecciona la arquitectura que deseas usar:")
    print("1. MVP (Model-View-Presenter)")
    print("2. MVVM (Model-View-ViewModel)")
    print("3. MVI (Model-View-Intent)")

    choice = input("Ingresa el número correspondiente: ").strip()
    architectures = {"1": "MVP", "2": "MVVM", "3": "MVI"}
    return architectures.get(choice)

def add_architecture_to_existing_project(project_path, architecture, use_compose, package_name):
    """
    Añade la arquitectura deseada a un proyecto Android ya existente.
    """
    project_path = os.path.abspath(project_path)

    if not os.path.exists(project_path):
        print(f"El directorio {project_path} no existe. Por favor, verifica la ruta.")
        return

    # Validar si es un proyecto Android (buscar settings.gradle o settings.gradle.kts)
    if not os.path.exists(os.path.join(project_path, "settings.gradle")) and not os.path.exists(os.path.join(project_path, "settings.gradle.kts")):
        print("El directorio no parece ser un proyecto Android. Asegúrate de estar en el lugar correcto.")
        return

    package_path = os.path.join(*package_name.split('.'))
    src_main_path = os.path.join(project_path, "app", "src", "main", "java", package_path)

    if not os.path.exists(src_main_path):
        print(f"El paquete base {src_main_path} no existe. Por favor, verifica el nombre del paquete.")
        return
    
    # Comprobar si ya existe una arquitectura y manejar el cambio si es necesario
    if check_existing_architecture(src_main_path, architecture):
        return

    # Crear la nueva estructura de arquitectura
    create_architecture_structure(src_main_path, architecture, package_name, use_compose)
    add_to_manifest(project_path, package_name)
    print(f"Arquitectura {architecture} añadida correctamente al proyecto en {project_path}.")

    # Crear estructura según la arquitectura
    """if architecture in ["MVP", "MVVM", "MVI"]:
        create_architecture_structure(src_main_path, architecture, package_name, use_compose)
        add_to_manifest(project_path, package_name)
    else:
        print("Arquitectura no válida. Por favor, selecciona MVP, MVVM o MVI.")
        return

    print(f"Arquitectura {architecture} añadida correctamente al proyecto en {project_path}.") """
    # Llama a la función para eliminar kotlin-android-extensions
    remove_kotlin_android_extensions(project_path)

def check_existing_architecture(base_path, architecture):
    """
    Verifica si ya existe una arquitectura en el proyecto.

    Args:
        base_path (str): Ruta base donde se crean las carpetas de la arquitectura.
        architecture (str): Arquitectura actual seleccionada.

    Returns:
        bool: True si las carpetas de la arquitectura seleccionada ya existen, False en caso contrario.
    """
    architectures = {
        "MVP": ["presenter", "view", "model", "repository"],
        "MVVM": ["viewmodel", "repository", "model", "view"],
        "MVI": ["intent", "view", "state", "model", "repository"],
    }

    existing_architecture = None
    for arch, folders in architectures.items():
        if all(os.path.exists(os.path.join(base_path, folder)) for folder in folders):
            existing_architecture = arch
            break

    if existing_architecture == architecture:
        print(f"La arquitectura {architecture} ya está configurada. No se realizaron cambios.")
        return True
    elif existing_architecture:
        print(f"Se detectó una arquitectura diferente ({existing_architecture}). Se eliminarán sus carpetas.")
        for folder in architectures[existing_architecture]:
            folder_path = os.path.join(base_path, folder)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                print(f"Carpeta eliminada: {folder_path}")
    return False

def add_dependencies_to_build_gradle(project_path, dependencies, use_aliases=False):
    """
    Añade dependencias al archivo build.gradle.kts o build.gradle del proyecto.
    Si use_aliases es True, usa el formato `implementation(libs.<alias>)`.
    Si es False, usa el formato `implementation("group:name:version")`.
    """
    app_gradle_path_kts = os.path.join(project_path, "app", "build.gradle.kts")
    app_gradle_path = os.path.join(project_path, "app", "build.gradle")

    if os.path.exists(app_gradle_path_kts):
        gradle_path = app_gradle_path_kts
        is_kts = True
    elif os.path.exists(app_gradle_path):
        gradle_path = app_gradle_path
        is_kts = False
    else:
        print("No se encontró el archivo build.gradle.kts o build.gradle en el módulo app.")
        return

    # Leer el contenido actual del archivo
    with open(gradle_path, "r", encoding="utf-8") as file:
        gradle_content = file.read()

    # Filtrar dependencias ya existentes
    if use_aliases:
        dependencies_to_add = [
            f"libs.{alias}" for alias in dependencies if f"libs.{alias}" not in gradle_content
        ]
    else:
        dependencies_to_add = [
            dep for dep in dependencies if (
                f'implementation("{dep}")' not in gradle_content and
                f'implementation "{dep}"' not in gradle_content
            )
        ]

    if not dependencies_to_add:
        print("Todas las dependencias ya están añadidas. No se realizaron cambios.")
        return

    # Crear el bloque de dependencias en el formato adecuado
    dependencies_block = ""
    for dep in dependencies_to_add:
        if use_aliases:
            dependencies_block += f"    implementation({dep})\n"
        else:
            if is_kts:
                dependencies_block += f'    implementation("{dep}")\n'
            else:
                dependencies_block += f'    implementation "{dep}"\n'

    # Añadir dependencias dentro del bloque dependencies
    if "dependencies {" in gradle_content:
        gradle_content = gradle_content.replace(
            "dependencies {",
            f"dependencies {{\n{dependencies_block}"
        )
    else:
        # Si no existe el bloque dependencies, añadirlo
        gradle_content += f"\ndependencies {{\n{dependencies_block}}}\n"

    # Guardar el contenido modificado
    with open(gradle_path, "w", encoding="utf-8") as file:
        file.write(gradle_content)

    print(f"Dependencias añadidas correctamente al archivo {gradle_path}:")
    for dep in dependencies_to_add:
        if use_aliases:
            print(f"- {dep}")
        else:
            print(f"- {dep}")


def add_dependencies_to_versions_toml(versions_toml_path, dependencies):
    """
    Añade dependencias al archivo libs.versions.toml, evitando duplicados,
    y gestiona las versiones en la sección `[versions]`.
    """
    if not os.path.exists(versions_toml_path):
        print(f"No se encontró el archivo {versions_toml_path}. Creando uno nuevo.")
        check_or_create_versions_toml(os.path.dirname(versions_toml_path))

    # Leer contenido actual del archivo
    with open(versions_toml_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    import pdb; pdb.set_trace()

    sections = {}
    current_section = None
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("[") and stripped_line.endswith("]"):
            current_section = stripped_line.lower()  # Convertir a minúsculas
            if current_section not in sections:
                sections[current_section] = []
        else:
            if current_section:
                sections[current_section].append(line.rstrip("\n"))
            else:
                # Líneas fuera de secciones (no común en TOML)
                sections.setdefault("header", []).append(line.rstrip("\n"))

    # Imprimir las secciones detectadas
    print("Secciones detectadas en el archivo:")
    for section_name in sections.keys():
        print(f"- {section_name}")

    # Inicializar diccionarios para versiones y librerías existentes
    existing_versions = set()
    existing_libraries = set()

    # Procesar secciones existentes
    if "[versions]" in sections:
        for line in sections["[versions]"]:
            match = re.match(r'^(\w[\w_-]*)\s*=\s*"(.*)"$', line.strip())
            if match:
                key = match.group(1)
                existing_versions.add(key)

    if "[libraries]" in sections:
        for line in sections["[libraries]"]:
            match = re.match(r'^(\w[\w_-]*)\s*=', line.strip())
            if match:
                alias = match.group(1)
                existing_libraries.add(alias)

    added_aliases = []

    # Añadir nuevas dependencias
    for dep in dependencies:
        group, name, version = dep.split(":")
        alias = name.replace("-", "_")
        version_key = f"{alias}_version"

        # Añadir versión si no existe
        if version_key not in existing_versions:
            if "[versions]" not in sections:
                sections["[versions]"] = []
            sections["[versions]"].append(f'{version_key} = "{version}"')
            existing_versions.add(version_key)

        # Añadir librería si no existe
        if alias not in existing_libraries:
            if "[libraries]" not in sections:
                sections["[libraries]"] = []
            lib_entry = f'{alias} = {{ group = "{group}", name = "{name}", version.ref = "{version_key}" }}'
            sections["[libraries]"].append(lib_entry)
            existing_libraries.add(alias)
            added_aliases.append(alias)

        # Reconstruir el contenido del archivo
    with open(versions_toml_path, "w", encoding="utf-8") as file:
        # Escribir encabezado si existe
        if "header" in sections:
            for line in sections["header"]:
                file.write(line + "\n")

        # Escribir secciones en el orden original o en un orden específico
        for section_name in ["[versions]", "[libraries]", "[plugins]"]:
            if section_name in sections:
                file.write(section_name + "\n")
                for line in sections[section_name]:
                    file.write(line + "\n")
                file.write("\n")  # Añadir una línea en blanco después de cada sección

        # Escribir cualquier otra sección que no hayamos cubierto
        for section_name, lines in sections.items():
            if section_name not in ["header", "[versions]", "[libraries]", "[plugins]"]:
                file.write(section_name + "\n")
                for line in lines:
                    file.write(line + "\n")
                file.write("\n")

    print(f"Dependencias añadidas correctamente al archivo {versions_toml_path}:")
    for alias in added_aliases:
        print(f"- {alias}")

    return added_aliases

def extract_section(content, section_header):
    """
    Extrae las líneas correspondientes a una sección específica de un archivo TOML.

    Args:
        content (str): El contenido completo del archivo.
        section_header (str): El encabezado de la sección, como `[versions]` o `[libraries]`.

    Returns:
        set: Un conjunto de las líneas de esa sección.
    """
    if section_header not in content:
        return set()
    
    lines = content.splitlines()
    in_section = False
    section_lines = set()

    for line in lines:
        if line.strip() == section_header:
            in_section = True
        elif in_section and line.startswith("[") and line != section_header:
            break
        elif in_section and line.strip():
            section_lines.add(line.strip())

    return section_lines

def filter_new_dependencies(existing_content, dependencies, is_toml):
    """
    Filtra las dependencias para evitar duplicados en el archivo existente.

    Args:
        existing_content (str): Contenido del archivo donde se agregarán las dependencias.
        dependencies (list): Lista de dependencias a añadir.
        is_toml (bool): Indica si el formato es TOML (True) o Gradle (False).

    Returns:
        list: Dependencias nuevas que no están duplicadas.
    """
    new_dependencies = []
    for dep in dependencies:
        if is_toml:
            group, name, version = dep.split(":")
            toml_entry = f'{name.replace("-", "_")} = {{ group = "{group}", name = "{name}", version = "{version}" }}'
            if toml_entry not in existing_content:
                new_dependencies.append(dep)
        else:
            if (
                f'implementation("{dep}")' not in existing_content and
                f'implementation "{dep}"' not in existing_content
            ):
                new_dependencies.append(dep)
    return new_dependencies

def get_dependencies(dependencies, project_path):
    # Filtrar dependencias vacías (por ejemplo, Jetpack Compose si no aplica)
    dependencies = {k: v for k, v in dependencies.items() if any(v.values())}
    for idx, group in dependencies.items():
        for group_name in group.keys():
            print(f"{idx}. {group_name}")

    while True:  # Mantener el menú hasta que el usuario confirme    
        selected_keys = input("\nIngresa los números de los grupos que deseas añadir, separados por comas o 0 para finalizar: ").strip()
    
        # Si selecciona 0 se sale del menú
        if selected_keys == "0":
            break

        # Limpieza de la entrada
        selected_keys = [key.strip() for key in selected_keys.split(",") if key.strip().isdigit()]

        # Validar entradas inválidas
        invalid_keys = [key for key in selected_keys if int(key) not in dependencies]
        if invalid_keys:
            print("\nERROR: Los siguientes números no son válidos:", ", ".join(invalid_keys))
            print("Por favor, selecciona números del listado anterior.")
            continue

        # Seleccionar las dependencias válidas
        selected_dependencies = []
        for key in selected_keys:
            if key.isdigit() and int(key) in dependencies:
                for dep_list in dependencies[int(key)].values():
                    selected_dependencies.extend(dep_list)

        print("\nDependencias seleccionadas:")
        for dep in selected_dependencies:
            print(f"- {dep}")

        # Confirmación del usuario
        confirm = input("\n¿Estás seguro de añadir estas dependencias? (s/n): ").strip().lower()
        if confirm == 's':
            print("\nAñadiendo dependencias al proyecto...")
             # Detectar si usar libs.versions.toml o build.gradle.kts
            versions_toml_path = check_or_create_versions_toml(project_path)

            if versions_toml_path:
                # Añadir dependencias al archivo TOML y obtener los aliases generados
                aliases = add_dependencies_to_versions_toml(versions_toml_path, selected_dependencies)
                # Añadir los aliases al build.gradle.kts
                add_dependencies_to_build_gradle(project_path, aliases, use_aliases=True)
                print("\nDependencias añadidas a 'libs.versions.toml'.")
                break
            else:
                build_gradle_path = os.path.join(project_path, "app", "build.gradle.kts")
                add_dependencies_to_build_gradle(build_gradle_path, selected_dependencies, use_aliases=False)
                print("\nDependencias añadidas a 'build.gradle.kts'.")
                break
        else:
            print("\nVolviendo al menú de dependencias...\n")

def check_or_create_versions_toml(project_path):
    """
    Verifica si existe el archivo libs.versions.toml. Si no existe, ofrece crearlo.
    """
    versions_toml_path = os.path.join(project_path, "gradle", "libs.versions.toml")
    if not os.path.exists(versions_toml_path):
        create = input(f"El archivo 'libs.versions.toml' no existe. ¿Quieres crearlo? (s/n): ").strip().lower()
        if create == "s":
            print(f"Creando {versions_toml_path}...")
            os.makedirs(os.path.dirname(versions_toml_path), exist_ok=True)
            with open(versions_toml_path, "w", encoding="utf-8") as file:
                file.write("[versions]\n[libraries]\n[plugins]\n")
            print("Archivo 'libs.versions.toml' creado exitosamente.")
        else:
            print("No se creó el archivo 'libs.versions.toml'. Las dependencias se añadirán al archivo 'build.gradle.kts'.")
            return None
    return versions_toml_path

def create_architecture_structure(base_path, architecture, package_name, use_compose):
    """
    Crea la estructura de carpetas y las clases base para la arquitectura especificada.
    """
    if architecture == "MVP":
        paths = ["presenter", "view", "model", "repository"]
    elif architecture == "MVVM":
        paths = ["viewmodel", "repository", "model", "view"]
    elif architecture == "MVI":
        paths = ["intent", "view", "state", "model", "repository"]

    for folder in paths:
        full_path = os.path.join(base_path, folder)
        os.makedirs(full_path, exist_ok=True)
        print(f"Carpeta creada: {full_path}")
    
    create_base_classes(base_path, architecture, package_name, use_compose)
    create_splash_class(base_path, package_name)

def create_base_classes(base_path, architecture, package_name, use_compose):
    """
    Crea las clases base y adicionales según la arquitectura elegida.
    """
    if architecture == "MVP":
        create_mvp_classes(base_path, package_name)
    elif architecture == "MVVM":
        create_mvvm_classes(base_path, package_name, use_compose)
    elif architecture == "MVI":
        create_mvi_classes(base_path, package_name)

def create_mvp_classes(base_path, package_name):
    """
    Crea las clases base y adicionales para la arquitectura MVP.
    """
    presenter_path = os.path.join(base_path, "presenter", "BasePresenter.kt")
    with open(presenter_path, "w", encoding="utf-8") as file:
        file.write(
            f"""package {package_name}.presenter\n\n
            interface BasePresenter {{\n    fun start()\n}}\n""")
    print(f"Clase creada: {presenter_path}")

    model_path = os.path.join(base_path, "model", "BaseModel.kt")
    with open(model_path, "w", encoding="utf-8") as file:
        file.write(f"""package {package_name}.model\n\ninterface BaseModel {{\n    fun getData(): String\n}}\n""")
    print(f"Clase creada: {model_path}")

    repository_path = os.path.join(base_path, "repository", "BaseRepository.kt")
    with open(repository_path, "w", encoding="utf-8") as file:
        file.write(f"""package {package_name}.repository\n\ninterface BaseRepository {{\n    fun fetchData(): String\n}}\n""")
    print(f"Clase creada: {repository_path}")

def create_mvvm_classes(base_path, package_name, use_compose):
    """
    Crea las clases base y adicionales para la arquitectura MVVM.
    """
    viewmodel_path = os.path.join(base_path, "viewmodel", "BaseViewModel.kt")
    with open(viewmodel_path, "w", encoding="utf-8") as file:
        file.write(f"""package {package_name}.viewmodel\n\nimport androidx.lifecycle.ViewModel\n\nopen class BaseViewModel : ViewModel() {{\n    // Configuración base\n}}\n""")
    print(f"Clase creada: {viewmodel_path}")

    model_path = os.path.join(base_path, "model", "BaseModel.kt")
    with open(model_path, "w", encoding="utf-8") as file:
        file.write(f"""package {package_name}.model\n\ninterface BaseModel {{\n    fun getData(): String\n}}\n""")
    print(f"Clase creada: {model_path}")

    repository_path = os.path.join(base_path, "repository", "BaseRepository.kt")
    with open(repository_path, "w", encoding="utf-8") as file:
        file.write(f"""package {package_name}.repository\n\ninterface BaseRepository {{\n    fun fetchData(): String\n}}\n""")
    print(f"Clase creada: {repository_path}")

    view_path = os.path.join(base_path, "view", "BaseView.kt")
    if use_compose:
        with open(view_path, "w", encoding="utf-8") as file:
            file.write(f"""package {package_name}.view\n\nimport androidx.compose.runtime.Composable\n\n@Composable\nfun BaseView() {{\n    // Implementación de la vista con Jetpack Compose\n}}\n""")
    else:
        with open(view_path, "w", encoding="utf-8") as file:
            file.write(f"""package {package_name}.view\n\nimport android.os.Bundle\nimport androidx.appcompat.app.AppCompatActivity\n\nclass BaseView : AppCompatActivity() {{\n    override fun onCreate(savedInstanceState: Bundle?) {{\n        super.onCreate(savedInstanceState)\n        setContentView(R.layout.activity_example)\n    }}\n}}\n""")
    print(f"Clase creada: {view_path}")

def create_mvi_classes(base_path, package_name):
    """
    Crea las clases base y adicionales para la arquitectura MVI.
    """
    model_path = os.path.join(base_path, "model", "BaseModel.kt")
    with open(model_path, "w", encoding="utf-8") as file:
        file.write(f"""package {package_name}.model\n\ninterface BaseModel {{\n    fun getData(): String\n}}\n""")
    print(f"Clase creada: {model_path}")

    view_path = os.path.join(base_path, "view", "BaseView.kt")
    with open(view_path, "w", encoding="utf-8") as file:
            file.write(f"""package {package_name}.view\n\nimport androidx.compose.runtime.Composable\n\n@Composable\nfun BaseView() {{\n    // Implementación de la vista con Jetpack Compose\n}}\n""")

    repository_path = os.path.join(base_path, "repository", "BaseRepository.kt")
    with open(repository_path, "w", encoding="utf-8") as file:
        file.write(f"""package {package_name}.repository\n\ninterface BaseRepository {{\n    fun fetchData(): String\n}}\n""")
    print(f"Clase creada: {repository_path}")

    intent_path = os.path.join(base_path, "intent", "BaseIntent.kt")
    with open(intent_path, "w", encoding="utf-8") as file:
        file.write(f"""package {package_name}.intent\n\ninterface BaseIntent\n""")
    print(f"Clase creada: {intent_path}")

def create_splash_class(base_path, package_name):
    """
    Crea una clase SplashActivity.
    """
    splash_path = os.path.join(base_path, "view", "SplashActivity.kt")
    with open(splash_path, "w", encoding="utf-8") as file:
        file.write(f"""package {package_name}.view\n\nimport android.os.Bundle\nimport androidx.appcompat.app.ComponentActivity\n\nclass SplashActivity : ComponentActivity() {{\n    override fun onCreate(savedInstanceState: Bundle?) {{\n        super.onCreate(savedInstanceState)\n        setContentView(R.layout.activity_splash)\n    }}\n}}\n""")
    print(f"Clase creada: {splash_path}")

def add_to_manifest(project_path, package_name):
    """
    Añade las actividades al AndroidManifest.xml.
    """
    manifest_path = os.path.join(project_path, "app", "src", "main", "AndroidManifest.xml")
    if not os.path.exists(manifest_path):
        print(f"AndroidManifest.xml no encontrado en {manifest_path}.")
        return

    with open(manifest_path, "r", encoding="utf-8") as file:
        content = file.read()

    activities = [
        f"""<activity android:name="{package_name}.view.SplashActivity" android:exported="true"/>"""
    ]

    # Inserta las actividades antes de la etiqueta de cierre </application>
    updated_content = content.replace("</application>", "\n    ".join(activities) + "\n</application>")

    with open(manifest_path, "w", encoding="utf-8") as file:
        file.write(updated_content)

    print("Actividades añadidas al AndroidManifest.xml.")
    add_permissions_to_manifest(manifest_path)

def add_permissions_to_manifest(manifest_path):
    """Permite al usuario seleccionar permisos para añadir al AndroidManifest.xml."""
    manifest_path = os.path.abspath(manifest_path)
    permissions = {
        "1": ("INTERNET", "Acceso a internet"),
        "2": ("ACCESS_FINE_LOCATION", "Acceso a la ubicación precisa"),
        "3": ("ACCESS_COARSE_LOCATION", "Acceso a la ubicación aproximada"),
        "4": ("CAMERA", "Acceso a la cámara"),
        "5": ("WRITE_EXTERNAL_STORAGE", "Escribir en almacenamiento externo"),
        "6": ("READ_EXTERNAL_STORAGE", "Leer desde almacenamiento externo"),
        "7": ("RECORD_AUDIO", "Grabar audio"),
        "8": ("BLUETOOTH", "Acceso a Bluetooth"),
        "9": ("BLUETOOTH_ADMIN", "Administrar Bluetooth"),
        "10": ("VIBRATE", "Control de vibración"),
        "11": ("ACCESS_NETWORK_STATE", "Verificar si el dispositivo tiene conexión a internet"),
        "12": ("ACCESS_WIFI_STATE", "Para apps que necesiten información sobre el Wi-Fi"),
        "13": ("READ_PHONE_STATE", "Acceso a información del dispositivo, como el número de teléfono o la red actual."),
        "14": ("CALL_PHONE", "Permitir realizar llamadas directamente desde la app"),
        "15": ("BODY_SENSORS", "Apps que usen dispositivos de fitness o sensores biométricos"),
        "16": ("ACTIVITY_RECOGNITION", "Apps que rastrean movimiento, como podómetros o aplicaciones de fitness."),
    }

    print("Selecciona los permisos que necesita tu aplicación:")
    for key, (permission, description) in permissions.items():
        print(f"{key}: {description} ({permission})")
    print("0: Finalizar selección")

    selected_permissions = set()
    while True:
        choice = input("Ingresa el número correspondiente o 0 para finalizar: ").strip()
        if choice == "0":
            break
        if choice in permissions:
            selected_permissions.add(permissions[choice][0])
            if permissions[choice][0] == "INTERNET":
                selected_permissions.add("ACCESS_FINE_LOCATION")
                selected_permissions.add("ACCESS_COARSE_LOCATION")
        else:
            print("Opción no válida. Inténtalo de nuevo.")

    if not selected_permissions:
        print("No se añadieron permisos al manifiesto.")
        return

    # Leer el archivo AndroidManifest.xml
    try:
        with open(manifest_path, "r", encoding="utf-8") as manifest_file:
            manifest_content = manifest_file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {manifest_path}.")
        return

   # Insertar los permisos seleccionados antes del tag <application>
    existing_permissions = set()
    for line in manifest_content.splitlines():
        if "<uses-permission android:name=" in line:
            start = line.find('"') + 1
            end = line.rfind('"')
            existing_permissions.add(line[start:end].replace("android.permission.", ""))


     # Añadir solo los permisos que no existan ya
    new_permissions = [
f'<uses-permission android:name="android.permission.{perm}" />'
        for perm in selected_permissions
        if perm not in existing_permissions
    ]

    # Añadir dependencias específicas
    features_block = ""
    if "CAMERA" in selected_permissions:
        camera_feature = '<uses-feature android:name="android.hardware.camera" android:required="false" />'
        if camera_feature not in manifest_content:
            new_permissions.append(camera_feature)
    if "RECORD_AUDIO" in selected_permissions:
        features_block += (
            '<uses-feature android:name="android.hardware.microphone" android:required="false" />\n'
        )
    if "BODY_SENSORS" in selected_permissions:
        features_block += (
            '<uses-feature android:name="android.hardware.sensor.body" android:required="false" />\n'
        )
    if "WRITE_EXTERNAL_STORAGE" in selected_permissions:
        print(
            "Nota: WRITE_EXTERNAL_STORAGE está limitado en Android 10 y versiones superiores. Considere usar Scoped Storage."
        )
    if "ACTIVITY_RECOGNITION" in selected_permissions:
        print(
            "ACTIVITY_RECOGNITION requiere permisos especiales en Android para su uso en segundo plano."
        )

    # Añadir permisos al manifiesto
    if new_permissions:
        permissions_block = "\n".join(new_permissions)
        if "<application" in manifest_content:
            manifest_content = manifest_content.replace(
                "<application",
                f"{permissions_block}\n\n    <application"
            )
        else:
            print("Error: El archivo AndroidManifest.xml no tiene la etiqueta <application>")
            return
        # Guardar el archivo actualizado
        with open(manifest_path, "w", encoding="utf-8") as manifest_file:
            manifest_file.write(manifest_content)

        print(f"Permisos añadidos correctamente: {', '.join(selected_permissions)}")
    else:
        print("Todos los permisos seleccionados ya existen en el manifiesto.")


def remove_kotlin_android_extensions(app_path):
    """
    Elimina el plugin kotlin-android-extensions del archivo build.gradle.kts del módulo app.
    """
    build_gradle_path = os.path.join(app_path, "build.gradle.kts")
    
    try:
        if os.path.exists(build_gradle_path):
            with open(build_gradle_path, "r") as file:
                lines = file.readlines()
            
            # Filtra las líneas que contienen kotlin-android-extensions
            updated_lines = [
                line for line in lines 
                if "kotlin(\"android.extensions\")" not in line and "kotlin-android-extensions" not in line
            ]
            
            # Sobrescribe el archivo sin las líneas obsoletas
            with open(build_gradle_path, "w") as file:
                file.writelines(updated_lines)
            
        else:
            print(f"No se encontró el archivo {build_gradle_path}.")
    except Exception as e:
        print(f"Error eliminando 'kotlin-android-extensions': {e}")

def is_valid_package_name(package_name):
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_.]*$', package_name) is not None
