# 📝 Instrucciones para Pull Requests

> 🚨 **REGLA SUPREMA DE PRECEDENCIA:** Lo establecido en este documento (`PULL_REQUEST_INSTRUCTIONS.md`) **primará siempre** sobre cualquier otra directiva de Git, versioning o branch naming del repositorio (incluyendo las secciones de Git y versioning de `CLAUDE.md`).
> 
> 🌿 **CREACIÓN OBLIGATORIA DE NUEVA RAMA:** 
> - Siempre que se inicien nuevos cambios que no tengan relación con los anteriores, O **inmediatamente después de completar/fusionar una PR**, es **estrictamente obligatorio** crear una nueva rama de trabajo (`tipo/nombre`) antes de desarrollar. Queda prohibido reutilizar ramas anteriores para tareas distintas o trabajar directamente en `main`/`develop`.

## 🎯 Objetivo
Automatizar creación de PRs siguiendo estándar del equipo: actualización `develop`, rebase, build, ...



## PASO 0: Verificación e Instalación de GitHub CLI (`gh`)
⚠️ **¡IMPORTANTE! Ejecutar de forma secuencial.**

Verificar si el CLI de GitHub (`gh`) está instalado. Si no está instalado, instalarlo automáticamente:

```powershell
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "GitHub CLI (gh) no detectado. Instalando..."
    winget install --id GitHub.cli -e --silent --accept-source-agreements --accept-package-agreements
} else {
    Write-Host "GitHub CLI (gh) ya está instalado."
}
gh --version
```



## PASO 1: Análisis y Validaciones
⚠️ **¡IMPORTANTE! Ejecutar comandos UNO A UNO, NUNCA en paralelo.**

```sh
# Validar entorno (ejecutar secuencialmente)**
git branch --show-current   # 1. Verificar rama actual

git status --porcelain      # 2. Verificar cambios pendientes

gh --version                # 3. Verificar si gh CLI está instalado

```

**Extraer del prompt:**
1. **`<type>` (obligatorio):** `feature` | `bugfix` | `enhacement`

2. **`<nombre>` (obligatorio):** Descripción corta (ej: "Fix dependencias")

**Decisión de rama:**
* Rama no existe -> Crear nueva rama

* Formato: `tipo/Nombre`

* Otro Formato -> Preguntar al usuario

**Si falta información obligatoria -> PREGUNTAR antes de continuar.**

*Ejemplo: `bugfix/fix-dependencias`*



## PASO 2: Gestión de Ramas

### Rama Nueva (o desde main/develop):

```sh

git checkout main

git pull origin main

git checkout -b <rama-trabajo>

```


### Rama existente (con cambios sin commit):

```sh

git checkout develop

git pull origin develop

git checkout <rama-trabajo>

git stash push -m "Backup antes de rebase"

git rebase develop

git stash pop

```


### Rama existente (cambios con commit):

```sh

git checkout develop

git pull origin develop

git checkout <rama-trabajo>

git rebase develop

```


**Conflictos:**

* `git status` -> Avisar y mostrar error

* Instruir: Resolver usando git tool

* *Mensaje usuario*: `⚠ Conflictos complejos detectados. Resuélvelos manualmente`


**Reglas:**

* NO usar `--force`, siempre `--force-with-lease`

* NO cambiar rama base sin confirmación

* PREGUNTAR si falta tipo/nombre



## PASO 3: Build(opcional: si se usa lenguaje compilado)

✅ Compila -> Continuar

❌ Errores -> "Mostrar" y mostrar errores

**No comitear si no compila en caso de que sea lenguaje compilado.**



## PASO 4: Revisar y Commit
**¡Responsabilidad de Copilot!:** Revisar cambios y comitear en la rama correcta.

**"¡Mostrar archivos modificados al usuario!"**

```sh

git status

git diff --name-status

```


**Excluir archivos temporales:**

`*.user`, `*.suo`, `*.log`, `*tmp*`

Archivos de prueba no relacionados


**Listar archivos que se van a subir** (mostrar en pantalla)

```sh

git add <archivo-especifico> (varios)

git commit -m "Descripción breve del cambio"

```


**Formato mensaje:** `[<tipo>] [<feature>|<bugfix>|<enhacement>] + descripción.`

```sh

git push -u origin [<nombre-rama>]

```

**Si NO hay cambios:** Preguntar si continuar solo actualizando rama.



## PASO 5: Crear Pull Request

**Title:** `[<tipo>] <nombre> - <nombre-descriptivo>`

*Ejemplo:* `[Bugfix] Fix - Corrección dependencias`


**Generar Resumen de Git (solo si existen):**

```sh

git log develop..HEAD --oneline

```


**Body:**

```markdown

## Resumen (1-3 líneas basado en commits y/o archivos modificados)

## Cambios principales (priorizando esto si hay commits)

- [Añadido/Componente 1 Modificado]

- [Corregido/Componente 2 Modificado]

**Mapeo:**

* `feature` -> `Feature`

* `bugfix` -> `Bug`

* `enhacement` -> `Enhacement`


```powershell

# ⚠️ IMPORTANTE:

# - $body debe ser una variable (evitar error con `(comillas)`)

# - --Encoding utf8 -> en `Set-Content` (acentos correctos)

# - TempFile -> `.md` para saltos de línea

# - Etiquetas OBLIGATORIAS -> una línea `--add-label "[<tipo>]"` por cada ID proporcionado



$body = @"

## Resumen

<Resumen generado de commits/archivos>

## Cambios principales

- [Cambio 1]

- [Cambio 2]


"@

$tempPath = [System.IO.Path]::GetTempFileName() + ".md"

$body | Set-Content -Path $tempPath -Encoding UTF8

gh pr create --title "[<tipo>] <nombre>" --body-file $tempPath --add-label "[<tipo>]"

Remove-Item $tempPath -ErrorAction SilentlyContinue

```



## PASO 6: Confirmación ⚠️ OBLIGATORIO
**Siempre crear tras crear el PR:**

1. Mostrar URL de caja de código y enlace clickable:
**Pull Request creado:**

`https://github.com/org...`

[**Clic aquí**](https://github.com/org/repo/pull/numero)



## Gestión de Errores
* `dotnet build-server shutdown` -> Mostrar error y sugerir detener manualmente desde IDE

* `gh pr create` no verificado -> sugerir `winget install --id GitHub.cli` y `gh auth login`

* Conflictos complejos detectados -> Mostrar error e detener (no continuar)

* Warning en `dotnet build` -> Continuar pero notificar

* PowerShell error variables no aceptado -> usar $tempFile simple

* `Set-Content` problemas de encoding -> Usar `-Encoding UTF8`

* Si el push falla -> `git fetch origin` y `git rebase` manual, avisar usuario

* Faltan datos (tipo, nombre) -> Detener ejecución y pedir



## Responsabilidades
* **Generar resumen automático de cambios (basado en commits y/o archivos)**

* **Crear PR: variable y archivo temporal con `-Encoding utf8` y comillas simples en título**

* **PASO 6: Mostrar URL en caja + recordatorios obligatorios**