import os
import re

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
        if selected_keys == "9":
            warn_firebase_configuration()
        if selected_keys == "22":
            warn_crashlytics_configuration()

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

                    # Añadir dependencias a la lista seleccionada
                    selected_dependencies.extend(dep_list)

        # Validar conflictos entre Moshi y Gson
        if not validate_moshi_gson_selection(selected_dependencies):
            print("\n⚠️ Error: Se detectó un conflicto entre Moshi y Gson. Por favor, selecciona solo una.")
            print("Volviendo al menú para que ajustes tu selección.\n")
            continue  # Volver al menú

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

        # Escribir secciones en el orden original o en un orden específico
        for section_name in ["[versions]", "[libraries]", "[plugins]"]:
            if section_name in sections:
                file.write(section_name + "\n")
                for line in sections[section_name]:
                    file.write(line + "\n")
                file.write("\n")  # Añadir una línea en blanco después de cada sección

        # Escribir cualquier otra sección que no hayamos cubierto
        for section_name, lines in sections.items():
            if section_name not in ["[versions]", "[libraries]", "[plugins]"]:
                file.write(section_name + "\n")
                for line in lines:
                    file.write(line + "\n")
                file.write("\n")

    print(f"Dependencias añadidas correctamente al archivo {versions_toml_path}:")
    for alias in added_aliases:
        print(f"- {alias}")

    return added_aliases

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
    elif os.path.exists(app_gradle_path):
        gradle_path = app_gradle_path
    else:
        print("No se encontró el archivo build.gradle.kts o build.gradle en el módulo app.")
        return

    # Leer el contenido actual del archivo
    try:
        with open(gradle_path, "r", encoding="utf-8") as file:
            gradle_content = file.read()
    except Exception as e:
        print(f"Error al leer el archivo {gradle_path}: {e}")
        return
    
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
        dependencies_block += f"    implementation({dep})\n"

    # Añadir dependencias dentro del bloque dependencies
    if "dependencies {" in gradle_content:
        gradle_content = gradle_content.replace(
            "dependencies {",
            f"dependencies {{\n{dependencies_block}"
        )
    else:
        # Si no existe el bloque dependencies, añadirlo
        gradle_content += f"\ndependencies {{\n{dependencies_block}}}\n"

    # Configuración adicional según las dependencias
    my_application_path = os.path.join(project_path, "build.gradle.kts")

    # Guardar el contenido modificado
    try:
        with open(gradle_path, "w", encoding="utf-8") as file:
            file.write(gradle_content)
            print(f"Archivo {gradle_path} modificado: {dependencies_block}")
    except Exception as e:
        print(f"Error al escribir en el archivo {gradle_path}: {e}")
        return

    print(f"Dependencias añadidas correctamente al archivo {gradle_path}:")
    for dep in dependencies_to_add:
        if use_aliases:
            print(f"- {dep}")
        else:
            print(f"- {dep}")   

def warn_firebase_configuration():
    print("⚠️  Recuerda añadir el archivo 'google-services.json' en el módulo app para configurar Firebase correctamente.")

def validate_moshi_gson_selection(selected_dependencies):
    """
    Valida que no se seleccionen Moshi y Gson al mismo tiempo.
    """
    if "com.squareup.moshi:moshi-kotlin:1.15.0" in selected_dependencies and "com.google.code.gson:gson:2.10" in selected_dependencies:
        print("⚠️  Solo puedes seleccionar una librería entre Moshi y Gson. Elige una y vuelve a intentarlo.")
        return False
    return True

def warn_crashlytics_configuration():
    print("⚠️  Recuerda que Crashlytics requiere configuración adicional en 'google-services.json'.")


