# 🎯 Implementación: Arquitectura de cifrado estilo Bitwarden/KeePass

## Understanding
El usuario solicita reestructurar el flujo de cifrado para usar una arquitectura segura: derivación de clave (Argon2id), cifrado autenticado (AES-256-GCM) y almacenamiento local cifrado (SQLCipher). El objetivo es diseñar e implementar los componentes necesarios en el proyecto Vega.

## Assumptions
- Proyecto .NET 10 (ya confirmado).
- Se puede añadir/instalar paquetes NuGet y librerías nativas (SQLCipher bundle) al proyecto.
- El usuario quiere integración local (no remoto) y compatibilidad Windows y multiplataforma cuando sea posible.

## Approach
Crear helpers independientes y pruebas mínimas: 1) Key derivation con Argon2id y salt aleatorio; 2) Crypto wrapper para AES-GCM; 3) Integración de SQLCipher (usar SQLitePCLRaw.bundle_sqlcipher + Microsoft.Data.Sqlite.Core) para almacenar entradas; 4) Actualizar la UI para usar el flujo maestro -> derivar clave -> abrir/crear DB. Mantendré los cambios divididos en archivos nuevos para minimizar impacto.

## Key Files
- src/Vega/Crypto/KeyDerivation.cs - implementa Argon2id, generación de salt y parámetros
- src/Vega/Crypto/AesGcmEncryptor.cs - envoltorio para AesGcm (nonce, tag, asociado)
- src/Vega/Data/SqlCipherStore.cs - manejo de creación/conexión a BD cifrada y CRUD básico
- MainWindow.xaml(.cs) - actualizar lógica para usar la nueva arquitectura
- Vega.csproj - añadir paquetes NuGet

## Risks & Open Questions
- SQLCipher añade dependencias nativas; en plataformas no-Windows puede necesitar pasos extra. Confirmar si quieres soporte multiplataforma inmediato o prioridad Windows.
- Argon2 parámetros (memoria, iteraciones, paralelismo) requieren ajuste según target hardware. Propondré valores conservadores por defecto.
- Manejo seguro de la clave en memoria: intentar minimizar exposición (SecureString/clear arrays).

**Progreso**: 100% [██████████]

**Última actualización**: 2026-09-28 16:06:11

## 📝 Pasos del plan
- ✅ **Añadir paquetes NuGet — instalar: Konscious.Security.Cryptography (Argon2), Microsoft.Data.Sqlite.Core, SQLitePCLRaw.bundle_sqlcipher, (opcional) Newtonsoft.Json.**
- ✅ **Crear KeyDerivation.cs — generar salt, DeriveKeyArgon2id(master, salt, memoryKB, iterations, parallelism, keyLen).**
- ✅ **Crear AesGcmEncryptor.cs — métodos Encrypt(plaintext,key,associatedData) y Decrypt(package,key,associatedData) que empaqueten nonce|ciphertext|tag.**
- ✅ **Crear SqlCipherStore.cs — inicializar DB cifrada con contraseña/clave (usar PRAGMA key / Microsoft.Data.Sqlite connection string con SQLitePCLRaw.bundle_sqlcipher), esquema mínimo (entries table) y métodos Open/Create/Insert/Get.**
- ✅ **Conectar UI — modificar MainWindow para flujo: pedir contraseña maestra, generar/obtener salt (almacenarlo en la BD o fichero), derivar clave, abrir DB cifrada, permitir guardar/leer entradas.**
- ✅ **Tests y validación — pruebas básicas: derivación consistente, cifrado/descifrado roundtrip, apertura DB cifrada en nueva instancia.**
- ✅ **Documentación y ajustes — explicar parámetros Argon2, cómo exportar/importar DB, recomendaciones de seguridad.**

