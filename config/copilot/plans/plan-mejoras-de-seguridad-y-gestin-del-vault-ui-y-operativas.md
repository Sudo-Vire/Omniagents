# Mejoras de seguridad y gestión del Vault — UI y operativas
## Understanding
El objetivo es añadir mejoras que aumenten la usabilidad y seguridad del vault: UI para crear/abrir vaults, configurar parámetros Argon2, export/import, aplicar permisos de archivo y ejecutar pruebas de verificación. Cambios serán mínimos y seguros.

## Assumptions
- Proyecto WPF existente (MainWindow) y módulos VaultManager/SqlCipherStore ya incluidos.
- Se puede modificar XAML y añadir helpers C#.
- Windows es plataforma principal; usaré APIs Win32/NTFS donde aplique.

## Approach
1. Extender MainWindow.xaml para añadir controles: campos para memory/iterations/parallelism, botones Crear Vault, Abrir Vault, Exportar, Importar, Ejecutar Prueba.
2. Implementar manejadores en MainWindow.xaml.cs que llamen a VaultManager.CreateVault/OpenVault y a métodos nuevos ExportVault/ImportVault; validar entradas y mostrar resultados al usuario.
3. Añadir protección de archivos en Windows con FileSecurity (FileProtection.cs) y usarla tras crear vault o al exportar/importar.
4. Añadir métodos en VaultManager: ExportVault (zip o copia segura) e ImportVault (validar y reemplazar).
5. Añadir botón "Run Self-Test" que invoque Utils.DevSmokeTests.RunAll y muestre resultado.
6. Actualizar Docs/CryptoDesign.md con instrucciones de uso y notas sobre export/import y permisos.

## Key Files
- MainWindow.xaml - UI
- MainWindow.xaml.cs - handlers
- Data/VaultManager.cs - añadir ExportVault/ImportVault
- Utils/FileProtection.cs - aplicar permisos NTFS en Windows
- Docs/CryptoDesign.md - actualizar

## Risks & Open Questions
- Importación sobreescribe archivos; pedir confirmación al usuario.
- Permisos NTFS solo válidos en Windows; implementar comprobación de plataforma.

## Steps
1. Edit MainWindow.xaml — añadir controles y botones.
2. Edit MainWindow.xaml.cs — implementar handlers para crear/abrir/exportar/importar/run-test.
3. Edit Data/VaultManager.cs — añadir ExportVault/ImportVault utilitarios.
4. Create Utils/FileProtection.cs — aplicar permisos restrictivos para el usuario en Windows.
5. Update Docs/CryptoDesign.md — describir nuevas operaciones y recomendaciones.
6. Build project and fix compile issues.
