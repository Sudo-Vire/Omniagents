<overview>
Se está añadiendo un selector de idioma junto al selector de temas para cambiar toda la web entre español e inglés, con dos esferas que representan ambos idiomas. La traducción cubre contenido estático y generado por JavaScript, conserva las rutas y el tema elegidos, y debe mantener en inglés los términos habituales del sector, como *full-stack*, *frontend/backend*, *frameworks* y *hacking*.
</overview>

<history>
1. El contexto anterior resume varias iteraciones de la experiencia del portfolio: navegación por rutas y carpetas, arrastre de carpetas, mejoras de accesibilidad y un selector de tres temas. El tercer tema se llama ahora **CLAUDE**, tiene fondo claro y texto oscuro, y el selector muestra tres esferas.
2. El usuario pidió un selector de idiomas a la derecha del selector de temas, con una esfera para español y otra para inglés.
   - Se aclaró que debía traducir la web completa, no ser solo visual.
   - Se añadió contenido bilingüe para la interfaz, las pantallas y los textos dinámicos; la selección se guarda en `localStorage`.
   - Se probó el cambio real a español y se comprobó que persiste al recargar y que se traducen también las carpetas y sus contenidos.
3. El usuario recalcó que la versión española también debía cubrir textos que aún aparecían en inglés.
   - Se detectó y corrigió un conflicto de clave de traducción que producía `[object Object]` en la etiqueta accesible de Experiencia.
   - Se tradujeron nombres y descripciones de experiencia, proyectos, grupos de habilidades, formulario, rutas visibles y estados de carpetas. Se añadió también el texto localizado para el estado “sin señal”.
4. El usuario aclaró que no quiere traducir absolutamente todos los términos: deben conservarse en inglés las palabras usuales del sector.
   - La copia española quedó parcialmente demasiado traducida —por ejemplo, sustituyó *full-stack*, *frontend/backend*, *frameworks* y *hacking* por equivalentes españoles— y todavía hay que ajustar esos términos conforme a esta preferencia.
5. Durante la verificación más reciente se observó que, aunque el selector de idioma recibe `:hover`, su ancho calculado permanecía en 56px en lugar de expandirse. Esto queda pendiente de depurar.
</history>
<work_done>
Archivos modificados:
- `index.html`: marcado de textos traducibles, etiquetas accesibles y un selector de idioma con una esfera actual y otra opción.
- `js/model.js`: diccionarios `en` y `es`, nombres localizados de secciones y carpetas, y traducciones de contenido dinámico.
- `js/view.js`: persistencia de idioma, aplicación de textos y etiquetas accesibles, localización de rutas, habilidades, tarjetas, contactos y reloj; actualización del idioma del documento y de la descripción meta.
- `js/controller.js`: eventos del selector de idioma.
- `styles.css`: selector adyacente al de temas, esferas con banderas de España y Reino Unido, y texto español para el estado vacío de las carpetas.

Completado:
- [x] El cambio de idioma traduce las pantallas principales y los contenidos dinámicos.
- [x] El idioma se conserva al recargar y el cambio mantiene la carpeta activa.
- [x] Se traducen etiquetas accesibles y botones del selector de temas.
- [x] Se probó el cambio real de inglés a español y la persistencia tras recargar.
- [x] Los diagnósticos del editor no mostraron errores en la última comprobación disponible.

Pendiente:
- [ ] Ajustar la redacción española para conservar términos técnicos de uso habitual en inglés, conforme a la última indicación del usuario.
- [ ] Investigar por qué el selector de idioma no se expande al pasar el cursor, pese a que el elemento coincide con `:hover`.
- [ ] Volver a ejecutar diagnósticos y verificar el selector y las traducciones después de esos cambios.
</work_done>
<technical_details>
- El idioma seleccionado se guarda como `portfolio-language`; si no hay preferencia guardada, se usa inglés. El navegador se restauró a inglés y se eliminó la clave de idioma de prueba.
- `View.setLanguage()` actualiza `html.lang`, aplica traducciones `data-i18n`, renderiza de nuevo habilidades/contactos y conserva los contenidos de la carpeta activa.
- Las traducciones de experiencia y proyectos viven en `translations.es` por elemento; los grupos de habilidades usan `groupEs` y, cuando corresponde, un tercer valor por habilidad.
- Las rutas internas permanecen en inglés para no romper enlaces; sus nombres visibles se localizan.
- El selector de temas actualiza sus etiquetas accesibles según el idioma.
- La regla CSS del mensaje vacío español es `html[lang="es"] .folder-items:empty::before`.
- El selector de idioma está dentro de `.control-pickers`, junto al selector de temas. La evaluación del navegador indicó que `:hover` era verdadero pero el `width` y `flex-basis` seguían en `56px`; averiguar si hay una regla, un estado o una peculiaridad de layout que lo impida.
- En la versión española, mantener en inglés los términos técnicos que suelen escribirse así en el sector, en lugar de traducirlos literalmente. Algunos textos a revisar están en `Model.translations.es` y en las propiedades `translations.es` de los elementos dinámicos.
</technical_details>
<important_files>
- `index.html`
  - Marcado `data-i18n`, atributos de accesibilidad traducibles y la estructura visual del selector de idiomas junto al selector de temas.
- `js/model.js`
  - Diccionarios bilingües y contenido dinámico de habilidades, experiencia, estudios y proyectos. Revisar la redacción española para mantener los términos de sector en inglés.
- `js/view.js`
  - `setLanguage()`, `getSavedLanguage()`, `localized()` y renderizado localizado; clave para persistencia y refresco del contenido.
- `js/controller.js`
  - `bindLanguageMenu()` y eventos de selección; también mantiene la lógica previa de vista previa y repliegue del selector de temas.
- `styles.css`
  - Reglas de tamaño/hover de `.language-picker` y estilos de las esferas. Investigar aquí el ancho que no cambia durante `:hover`.
</important_files>
<next_steps>
1. Revisar y ajustar las traducciones españolas para conservar términos como *full-stack*, *frontend/backend*, *frameworks* y *hacking* en inglés cuando corresponda.
2. Depurar la expansión del selector de idioma: inspeccionar reglas computadas y dimensiones de `.language-picker`, `.control-pickers` y `.page-controls`; verificar tanto con cursor como con foco de teclado.
3. Probar ambos idiomas en Inicio, Sobre mí, Habilidades, Experiencia y Contacto; comprobar rutas localizadas, carpeta activa, mensajes del formulario y persistencia tras recargar.
4. Ejecutar diagnósticos de los archivos modificados y dejar la preferencia de idioma del navegador en un estado razonable tras la prueba.
</next_steps>