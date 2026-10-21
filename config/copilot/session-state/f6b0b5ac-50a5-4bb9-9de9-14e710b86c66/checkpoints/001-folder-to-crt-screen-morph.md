<overview>
The user (Spanish-speaking) is polishing the **Experience** screen of a vanilla HTML/CSS/JS "hacker terminal" portfolio (MVC: `js/model.js`, `js/view.js`, `js/controller.js`, `styles.css`, `index.html`) at `c:\Users\victo\WebProjects\Hacker-Portfolio`. The goal is a retro CRT-TV-style animation: the opened folder must leave the left column (only 2 folders remain visible on the left), and **the folder itself must become the screen** via an expansion effect with a progressive colour change, followed by an old-TV power-on reveal of the content. The latest request also asked to make the whole thing feel more retro.
</overview>

<history>
1. User asked: in the Experience animation, the open folder should move right, open, and show its content like an old-TV power-on screen.
   - Inspected view.js, styles.css, index.html, controller.js and model.js. The explorer has `.experience-folders` (3 `.topic-folder` buttons) and `#folder-panel` with `#folder-items`.
   - Added `is-opening` class on explorer/folder-items. Added CRT styles to `.folder-panel`: scanlines in `::before`, a sweep bar in `::after`, and a `crt-power-on` keyframe. Delayed the entries' typing animation.
   - Verified in the browser. User said "así mejor".

2. User said the left column should show only 2 folders, because the open one moves right and the screen is visible.
   - Tried several PowerShell/Python/Node patching approaches. Python and Node are not installed, and PS string-replace hit CRLF and literal-`` `r`n `` problems. Fixed the resulting mojibake (`â†—` → `↗`) and the CSS artifacts.
   - Made the open folder `position:absolute` and translated it right, driven by `--open-top`/`--open-height` JS vars. This was later superseded.

3. User asked for a more retro feel, and for the open folder to *become* the screen (expansion effect plus progressive colour change). This is the current task.
   - Implemented a "morph" overlay (details below) and edited view.js and styles.css with the `edit` tool.
   - Browser verification is partial. The tab is in the background (`document.visibilityState === "hidden"`), so CSS animations don't advance in real time and `animationend` doesn't fire. I added a 1000ms `setTimeout` fallback to remove the morph.
   - Last action: reloaded, clicked education, paused all animations via `document.getAnimations()`, and seeked to t = 0/250/400/560/800/1000/1500ms. Screenshots were saved to `C:\Users\victo\AppData\Local\Temp\morph-<t>.png`. **I have not yet viewed them.** They exist to visually confirm the morph.
</history>

<work_done>
Files modified:
- `js\view.js`:
  - `els.folderPanel = document.querySelector("#folder-panel")` added.
  - `renderExperienceFolder` now toggles `is-open`/`aria-expanded` per button and captures `openButton`. After `replaceChildren` it removes `is-opening` from explorer and folderItems and removes any old `.folder-morph`. It then forces a reflow (`void this.els.explorer.offsetWidth`). If `animate`, it adds `is-opening` to both and calls `this.playFolderMorph(openButton)`. Otherwise it adds `is-opening` to folderItems only.
  - New `playFolderMorph(button)`:
    - Skipped under `prefers-reduced-motion` or when rects are zero.
    - Creates `div.folder-morph[aria-hidden]` inside the explorer.
    - Sets CSS vars `--mx0/--my0/--mw0/--mh0` (start: the button's rect, inset 5px, with height = 0.88 × the button's height) and `--mx1/--my1/--mw1/--mh1` (end: the panel's `offsetLeft/Top/Width/Height`).
    - Removes itself on `animationend` for `folder-morph-box`, with a 1000ms timeout fallback.
  - `collapseExperienceFolder` is clean (the `--open-*` removeProperty lines were removed).
- `styles.css`:
  - `.experience-explorer` now has `position: relative`. `.experience-explorer.is-opening { --morph-dur: .6s; }` was added.
  - `.topic-folder` transition now includes `opacity .3s`.
  - `.topic-folder.is-open { opacity:0; pointer-events:none; transition:none; }`. The old absolute/translateX rules were removed. The open folder keeps its slot in the left column but is invisible, and the morph covers it.
  - `.folder-morph` is absolute, z-index 7, with `--mx0` etc. geometry. It uses two animations: `folder-morph-box` (smooth, `cubic-bezier(.65,0,.25,1)`) and `folder-morph-color` (`steps(10,end)`, retro banding). The colour animation goes green → darker green with glow → near-black `#080d09`, with a brightness flash, `box-shadow` glow, and border moving from `--green` to `--line`.
  - `.folder-morph::before` is a folder tab that fades out (`folder-morph-tab`).
  - `crt-power-on` was rewritten as a CRT line expanding horizontally then vertically (`scale(0,.006)` → `scale(1,.006)` → `scale(1,1.015)` → `scale(1,.99)` → `scale(1,1)`) with brightness 6→1. The panel animation is .9s with delay `calc(var(--morph-dur) - .05s)`.
  - `.folder-panel` has `border-radius:4px`. Its `::before` has scanlines plus a radial vignette and a `crt-flicker` infinite animation. Its `::after` runs `crt-sweep` plus an infinite `crt-roll`.
  - `.folder-panel-heading, .folder-entry h4` have a green text-shadow glow.
  - Entry typing delay is now `calc(var(--morph-dur, 0s) + .6s + var(--entry-index)*180ms)`.
  - Mobile ≤460px rule: `.folder-morph { border-radius: 3px; }`. The reduced-motion block hides `.folder-morph` and disables the `::before` flicker.

Status:
- [x] Open folder hides and the morph overlay is created. Checked via DOM: after clicking projects, `.is-open` has opacity 0, the panel is visible, and the content is correct.
- [x] No lint errors in view.js or styles.css (checked earlier, before the morph edits).
- [ ] Visual confirmation of the morph frames. The screenshots exist but have not been viewed.
- [ ] Re-check for a transient screen scrollbar during the panel scale overshoot. I reduced the overshoot to 1.015, but it is unverified.
- [ ] Test the 460px mobile layout and the Cyberpunk theme (`--green` is red there; the panel bg `#080d09` is fixed greenish-dark).
- [ ] Re-run the `problems` tool on both files after the latest edits.
</work_done>

<technical_details>
- The environment has no Python or Node. `apply_patch` and `rg` are unavailable in the current toolset. Use the `edit`/`create` tools for file changes, and `grep`/`glob`/`view` for reading. PowerShell `Get-Content -Raw`/`Set-Content -Encoding UTF8` can add a BOM and mangle UTF-8 glyphs (`↗` became `â†—`). Avoid PS rewrites. Single-line and multi-line `edit` calls both worked on these files.
- Page flow:
  - `Controller.init` → `View.init` → `renderExperienceFolder(Model.state.activeFolder, false)`.
  - `showScreen("experience")` calls `renderExperienceFolder("work")` with animate=true.
  - Clicking a folder calls `View.renderExperienceFolder(button.dataset.folder)`.
  - `setOptionIndex` calls `collapseExperienceFolder()` when the focused folder isn't the open one. Hovering or arrowing onto another folder collapses the panel. ArrowRight reopens, ArrowLeft collapses.
- `.is-open` uses `opacity:0` (not `visibility:hidden`) so the button stays focusable for keyboard navigation.
- The panel is positioned via `offsetLeft/offsetTop` against the explorer (`position:relative`) so animation transforms don't skew the measurement. The folder button is measured with `getBoundingClientRect` relative to the explorer.
- The panel stays hidden during the morph via the `animation ... both` backwards fill (opacity 0 in the 0% keyframe) with a delay, so the old content disappears like a channel change when switching folders.
- The embedded browser tab is hidden (`visibilityState: "hidden"`), so animations only advance when seeked manually. To inspect frames: click, `document.getAnimations().forEach(a => a.pause())`, set `a.currentTime = t`, then screenshot. Playwright `locator.click` times out on "stable" in this state; use the `clickElement` tool or `page.evaluate(() => el.click())`.
- `select.mp3` request abort messages in the console are harmless.
- Unknown: how the final morph looks in real-time on a visible tab.
</technical_details>

<important_files>
- `c:\Users\victo\WebProjects\Hacker-Portfolio\js\view.js`: contains `renderExperienceFolder` (~line 143), the new `playFolderMorph`, and `collapseExperienceFolder`. `els.folderPanel` is in `init`.
- `c:\Users\victo\WebProjects\Hacker-Portfolio\styles.css`: experience explorer, folder, panel and CRT/morph styles are around lines 478–540, with mobile overrides near ~560–580 and the reduced-motion block at the end.
- `c:\Users\victo\WebProjects\Hacker-Portfolio\index.html`: `#screen-experience` markup (lines ~70–83): `.experience-explorer`, `.experience-folders` with 3 `.topic-folder[data-folder]` buttons, and `#folder-panel` (`#folder-path`, `#folder-status`, `#folder-items`).
- `c:\Users\victo\WebProjects\Hacker-Portfolio\js\controller.js`: bindings for folder clicks/keys, which call the View render/collapse methods.
- `c:\Users\victo\WebProjects\Hacker-Portfolio\js\model.js`: `experienceFolders`, `jobExperience`, `studies`, `projects` data.
- Temp frames: `C:\Users\victo\AppData\Local\Temp\morph-{0,250,400,560,800,1000,1500}.png` (these can be deleted at the end).
</important_files>

<next_steps>
Remaining work:
- View the saved morph frames (the `view` tool can open the PNGs). Confirm that:
  - the green folder shape expands from the left slot to the panel rect;
  - the colour progresses green → dark;
  - the CRT line power-on reveals the panel and content;
  - only 2 folders are visible on the left.
- Fix any geometry or colour issues (for example, start-rect offsets, z-index, morph still covering the panel, a transient scrollbar).
- Run the `problems` tool on view.js and styles.css. Optionally test the Cyberpunk theme, a narrow viewport (≤460px), and opening a second folder while one is already open.
- Consider an optional CRT-off effect on collapse (not implemented).
- Clean up the temp PNGs, then give the user a concise Spanish summary of the result and offer to tweak timing, distance, or intensity.

Immediate next step: `view` `morph-250.png`, `morph-400.png`, `morph-560.png`, `morph-800.png`, and `morph-1000.png` to evaluate the animation frames.
</next_steps>