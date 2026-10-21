<overview>
El usuario está puliendo un portfolio web (HTML/CSS/JS vanilla, patrón Model/View/Controller) con selector de temas (HACKER, CYBERPUNK, CLAUDE) y un selector de idiomas (español/inglés) formado por esferas. El trabajo reciente se centró en la calidad visual y de interacción del selector de idiomas: bandera inglesa correcta, colapso inmediato tras el clic, sin saltos visibles de esferas y, lo último, un efecto fade desde la esfera actual hacia la pulsada. Se trabaja con edición directa de archivos y verificación en el navegador integrado (Playwright). Hay que recordar que el navegador puede servir CSS/JS en caché, por lo que conviene recargar antes de verificar.
</overview>

<history>
1. Contexto previo (resumido): el usuario pidió varias mejoras de interacción (sin scroll en About, carpetas de experiencia, rutas, selector de temas con preview y tercer tema CLAUDE) y un selector de idioma bilingüe que traduce toda la web conservando en inglés términos técnicos del sector.
2. Ajuste de términos técnicos en español.
   - Se sustituyeron traducciones literales por *full-stack*, *frontend/backend*, *frameworks*, *ethical hacking*, *Git workflows*, "PORTFOLIO".
   - Se depuró la supuesta falta de expansión del selector de idioma: en realidad funcionaba (expandía a 112px con hover real).
3. "El idioma por defecto es el español".
   - Cambié `Model.locale` a `"es"`, `getSavedLanguage()` (solo respeta `"en"` guardado; si no, `"es"`), `<html lang="es">`, la meta descripción y el estado inicial del selector en `index.html`.
4. "El botón de idiomas del mismo tamaño que el de temas".
   - Se quitó `overflow: hidden` de `.language-orb` y se añadió un aro exterior `.language-orb::before` (inset -7px) igual al de los temas. Ambos orbes miden 30px y los botones 56×56.
5. Bandera inglesa (varias iteraciones).
   - Primero un Union Jack en gradientes, luego (error mío) la bandera de Inglaterra; el usuario aclaró que debía ser la Union Jack con azul y X roja.
   - Se pasó a un SVG inline como `background-image` (fondo `#012169`, diagonales blancas, diagonales rojas, cruz blanca/roja).
   - El usuario pidió que las diagonales rojas estuvieran descentradas (desplazadas a la izquierda, como en la bandera real); tras probar -2, -6, -14 y -20 (demasiado, casi desaparecían), quedó en `M-3 0 57 60` y `M57 0 -3 60` con `stroke-width='5'`.
   - Aprendizaje: varias comprobaciones iniciales usaban CSS en caché; hay que recargar la página.
6. "Si no haces click fuera, el desplegable de idiomas no se cierra".
   - En `bindLanguageMenu` se eliminaron los listeners de `mouseleave`/`focusout` que reabrían el selector al encogerse bajo el cursor. Ahora el `mouseenter` solo reabre si estaba "dismissed" (patrón del selector de temas). Verificado: tras clic sin mover el ratón queda colapsado y re-expande con un nuevo hover.
7. "Al pulsar, cuando colapsa se ve el cambio de esferas".
   - `View.setLanguage(language, persist = true, updatePicker = true)` ahora puede omitir la actualización del selector. Se creó `View.updateLanguagePicker()` (actualiza nombre, `data-language-choice`, aria/title y `data-selected-language`).
   - En el controlador, el clic llama a `setLanguage(..., true, false)` y se aplaza `updateLanguagePicker` hasta `transitionend` de `flex-basis` en `.language-picker` colapsado, con fallback `setTimeout` de 400 ms.
8. Último pedido: "la esfera que has pulsado tiene que empezar a cambiar al instante, con un efecto fade desde la actual a la que has pulsado".
   - Se añadió una esfera superpuesta `.language-orb-fade` dentro de `.language-current`, con fade de opacidad de .25s.
   - Verificado en el navegador: opacidad 0 → ~0.83 a los 120 ms → al terminar el repliegue la base pasa a la bandera nueva y el overlay vuelve a 0. Fue la última acción antes de la compactación.
</history>

<work_done>
Archivos modificados (estado actual):
- `index.html`: `lang="es"`, meta descripción en español, `#language-current` con "Español", `#language-choice` con `data-language-choice="en"` y etiquetas en español, y nuevo `<span class="language-orb language-orb-fade" aria-hidden="true">` dentro de `.language-current`.
- `js/model.js`: `locale: "es"`, términos técnicos en inglés dentro de `translations.es`.
- `js/view.js`: `getSavedLanguage()` por defecto español; `updateLanguagePicker()`; `startLanguageFade(language)` (asigna `data-fade-language` y añade `.is-fading`); `setLanguage(language, persist, updatePicker)`.
- `js/controller.js`: `bindLanguageMenu()` reescrito con `mouseenter` condicional, `focus`, `transitionend`, temporizador de seguridad y clic que llama a `View.startLanguageFade(...)` y luego `View.setLanguage(..., true, false)`.
- `styles.css`: aro `.language-orb::before`; banderas ES e EN (SVG); `.language-current .language-orb { grid-area: 1 / 1; }`, `.language-orb-fade` (opacity 0, transition .25s, `.is-fading` opacity 1); los selectores de bandera de `.language-current` usan `:not(.language-orb-fade)` y hay reglas separadas `.language-orb-fade[data-fade-language="es|en"]`.

Completado:
- [x] Idioma por defecto español (respeta preferencia guardada `en`).
- [x] Esfera de idioma del mismo tamaño/aro que la de temas.
- [x] Union Jack con X roja descentrada, visible.
- [x] El selector se colapsa tras clic sin necesidad de clic externo.
- [x] Las esferas no saltan durante el repliegue (actualización diferida).
- [x] Fade desde la esfera actual hacia la pulsada, verificado numéricamente.
- [ ] No se verificó visualmente (captura) el fade ni se ejecutó `problems` tras esta última tanda de ediciones (CSS/HTML/JS); las capturas de pantalla del navegador fallan o salen diminutas con frecuencia.
- El navegador quedó en inglés tras la última prueba (clic en la opción inglesa); conviene restaurar a español (`View.setLanguage('es')`), ya que `portfolio-language` quedó guardado como `en`.
</work_done>

<technical_details>
- Idioma persistido en `localStorage["portfolio-language"]`; por defecto `es`. El tema usa `portfolio-theme`.
- `.language-picker` expande a 112px con `:hover`/`:focus-within`; `.is-collapsed` fuerza 56px y oculta la segunda esfera con opacidad. Al encogerse bajo un cursor quieto, `:hover` puede dejar de coincidir: por eso se usa un flag `dismissed` y no `mouseleave`.
- El layout evita el salto de esferas aplazando el swap de banderas hasta que la opción pulsada ya está invisible (opacity 0). La opción pulsada se queda en su sitio con la bandera antigua mientras desaparece.
- El fade usa dos esferas apiladas con `grid-area: 1/1` (un `background-image` no se puede transicionar). Al terminar, se quita `.is-fading` y se actualiza `data-selected-language` de la base; como ambas quedan idénticas, no hay salto visual.
- Bandera inglesa: SVG inline URL-encodeado (`%23` para `#`). Las diagonales blancas llevan `stroke-width='12'`; las rojas `5`, desplazadas en x (`M-3 0 57 60`, `M57 0 -3 60`). Valores de desplazamiento demasiado grandes (-14, -20) hacen que casi desaparezcan.
- Herramientas: `apply_patch` y `rg` ya no están disponibles (usar `edit`, `create`, `grep`). El parámetro `paths` de `grep` debe ser un string (no array de un solo elemento) para obtener salida; con `output_mode: "content"` y `path`/`paths` como string funcionó.
- Verificación con Playwright: tras editar archivos hay que recargar la página (hay caché); hacer clic con `{ force: true }` en `#language-choice` si la animación impide la estabilidad; las capturas con `screenshotPage` sobre selectores pequeños salen mínimas o fallan.
- El error recurrente `net::ERR_ABORTED` de `select.mp3` en file:// es inofensivo.
- Incertidumbre: no se ha confirmado visualmente (a ojo) que el fade se vea suave en la UI real; solo se midió la opacidad.
</technical_details>

<important_files>
- `C:\Users\victo\WebProjects\Hacker-Portfolio\index.html`
  - Estructura del footer con `.theme-picker` y `.language-picker`; contiene `.language-current` (esfera base + `.language-orb-fade`) y `#language-choice`.
- `C:\Users\victo\WebProjects\Hacker-Portfolio\styles.css`
  - Reglas de `.theme-picker` (líneas ~501-524) y `.language-picker` (~525-545): tamaños, hover/colapso, banderas ES/EN (SVG), aro y fade del overlay.
- `C:\Users\victo\WebProjects\Hacker-Portfolio\js\controller.js`
  - `bindThemeMenu()` (~210) y `bindLanguageMenu()` (después): lógica de colapso, transitionend, temporizador y llamada a `startLanguageFade`.
- `C:\Users\victo\WebProjects\Hacker-Portfolio\js\view.js`
  - `getSavedLanguage()`, `setLanguage()`, `updateLanguagePicker()`, `startLanguageFade()`, render localizado.
- `C:\Users\victo\WebProjects\Hacker-Portfolio\js\model.js`
  - `locale`, diccionarios `translations.en/es`, contenido dinámico (experiencia, proyectos, skills) con términos técnicos en inglés.
</important_files>

<next_steps>
Remaining work:
- Verificar que no hay errores con `problems` en `styles.css`, `index.html`, `view.js` y `controller.js` tras la última tanda de ediciones.
- Comprobar visualmente (o con muestras de opacidad en varios instantes) que el fade se ve bien en ambas direcciones (ES→EN y EN→ES) y que tras terminar no hay salto ni residuos del overlay.
- Restaurar el navegador a español (`View.setLanguage('es')`) para dejar la preferencia guardada razonable.

Immediate next steps:
- Ejecutar `problems` sobre los archivos modificados.
- Probar el fade en la dirección EN→ES, confirmando también que las etiquetas accesibles se actualizan al final del repliegue.
- Informar al usuario del resultado y pedir feedback sobre duración/suavidad del fade (actualmente .25s, igual que el colapso).
</next_steps>