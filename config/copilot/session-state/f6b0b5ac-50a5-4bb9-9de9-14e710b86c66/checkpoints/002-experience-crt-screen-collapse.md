<overview>
The user (Spanish-speaking) is polishing the **Experience** screen of a vanilla HTML/CSS/JS "hacker terminal" portfolio (MVC: `js/model.js`, `js/view.js`, `js/controller.js`, `styles.css`, `index.html`) at `c:\Users\victo\WebProjects\Hacker-Portfolio`. The target design has 3 fixed folders on the left and an always-visible CRT "screen" panel on the right. When a folder is confirmed, the screen window collapses toward the centre, reopens, and powers on like an old TV, and the content then appears. The user asked me to **always test changes in the browser**. They sometimes say "la 3ra carpeta se ha roto", and I was investigating that when the context was compacted.
</overview>

<history>
1. Earlier turns (see checkpoint 001). The folder-to-screen morph was built, then replaced by the design below.
2. The user asked that there always be an open folder, with `work` open by default.
   - I made hover/arrow focus open folders. The user then **rejected that**: focus must NOT open a folder, and confirmation needs Enter or ArrowRight (click also opens).
   - I removed the auto-open in `setOptionIndex` and made ArrowRight a no-op when the folder is already open.
   - I tested the keyboard flow in the browser and it worked.
3. The user corrected the design: the right screen must always be visible. No folder should start open, and the 3 folders always stay on the left. Initially (after reload, or on entering the screen) the screen is "NO SIGNAL".
   - `collapseExperienceFolder` now resets the panel to `/`, `STANDBY`, and empty items. `showScreen("experience")` and `View.init` both call it.
   - I removed the `.folder-panel` hidden/visible logic. I added `.folder-items:empty::before` with "NO SIGNAL // SELECT A DIRECTORY AND PRESS ENTER".
   - I verified in the browser.
4. The user said the folder doesn't need to move, and all 3 stay left. I removed the morph overlay (JS `playFolderMorph`, all `.folder-morph` CSS) and made `.topic-folder.is-open` not hidden.
5. The user said that when a folder opens, the screen must not open or resize; it should only look like it powers on.
   - I replaced the scale-based `crt-power-on` with brightness flicker steps and a sweep.
6. The user said the screen should close from top and bottom toward the centre and then open and power on.
   - I added `swapTimer` in `renderExperienceFolder`: content and path swap after 350ms, while the screen is collapsed.
7. The user said the window must collapse but keep its borders and header.
8. The user then corrected that: the window **borders must shrink progressively**, and the header (`/work` · `ACCESS GRANTED`) must keep its size and only move down with the window.
   - I implemented `@property --crt-s`, with `.folder-panel { transform: scaleY(var(--crt-s)) }`, and `.folder-panel-heading { transform-origin: top; transform: scaleY(calc(1 / var(--crt-s))) }`.
   - The `crt-collapse` keyframes run 1s, from 1 down to .17 and back to 1.
   - `crt-body-swap` fades the items out and back in. `crt-power-on` runs .7s with `forwards` fill, delayed .45s.
   - Measured in the browser: the panel height goes 310 → 53 → 296 and the header stays 39px.
9. The user asked for ease-in-out. I set `animation-timing-function: ease-in-out` on both the 0% and 35%/45% keyframes of `crt-collapse`. I verified the heights.
10. The user said "perfecto".
11. The user said the open folder's effect must not change.
    - Problem: when focus moved to another folder, the open folder reverted to its normal look.
    - I added `.topic-folder.is-open` alongside `.is-option-selected` in the rules for z-index/border/background, `folder-file-1/2` transforms, and hiding `.topic-text/.folder-count`.
    - The front is already `rotateX(-105deg)` for `.is-open`.
    - I verified in the browser, and the screenshots looked right.
12. The user said "la 3ra carpeta se ha roto" (the 3rd folder, `projects`, is broken). This is the **current, unresolved task**.
    - Investigation: the open folder and focused folder states look the same as for other folders. For example, `projects` open and focused shows the flipped-front, files-visible state.
    - The one real defect found: opening `projects` makes `#folder-panel` grow to **349px**, because its 2 entries are taller than the 310px left column. `.screen` then gets scrollHeight 582 against clientHeight 573, so a vertical scrollbar appears, shifting the panel and layout. With `work` and `education` the panel stays at 310 and there is no scroll.
    - I assume this scroll/overflow is what the user means, but I'm not fully sure. A less likely alternative is the focused 3rd folder's tilted `rotateX(-40deg)` front overflowing, which is the original hover design.
    - I was grepping the `.folder-entry` and `.folder-items` CSS to tighten spacing so `projects` fits in about 310–319px. The room before overflow is about 319px, and 573 is the current screen height.
</history>

<work_done>
Files modified (this and recent sessions):
- `js\view.js`:
  - `renderExperienceFolder(folderId, animate=true)` sets `activeFolder` and `openFolder`, adds `is-expanded`, and toggles `is-open`/`aria-expanded` on buttons.
  - It builds a fragment of entries. It removes `is-opening` from explorer and folderItems. If `!animate` it swaps immediately. Otherwise it forces a reflow, adds `is-opening` to the explorer, and after 350ms (`this.swapTimer`) runs `swap()`.
  - `swap()` sets the path and "ACCESS GRANTED", replaces the items, and adds `is-opening` to folderItems.
  - `collapseExperienceFolder()` clears the timer, sets `openFolder=null`, removes classes, and resets the path to `/`, the status to `STANDBY`, and the items to empty. It is called from `init` and from `showScreen("experience")`.
  - `setOptionIndex` no longer opens or collapses folders. It only moves focus and selection.
  - Removed: `playFolderMorph`, the morph logic, and `openButton`.
- `js\controller.js`:
  - ArrowRight on experience opens the focused folder if it differs from `View.openFolder`.
  - The ArrowLeft-collapse branch was removed. ArrowLeft now falls through to `moveOption(-1)`.
  - Click calls `View.renderExperienceFolder`. Enter on a button likely triggers the click.
- `styles.css`:
  - Removed all `.folder-morph` and morph keyframes, and the `--morph-dur` rules.
  - `.folder-panel` is now `position:relative; display:flex; flex-direction:column; min-height:270px; overflow:hidden; transform: scaleY(var(--crt-s))`, with `border-radius:4px`, background `#080d09`, and an inset shadow. It is always visible.
  - `.folder-panel-heading` has `flex-shrink:0` and the inverse `scaleY(calc(1/var(--crt-s)))` with `transform-origin: top`.
  - `.folder-items` is `display:grid; flex:1; align-content:start; gap:9px; padding:13px`. `.folder-items:empty` centres the "NO SIGNAL" text and flickers.
  - `.experience-explorer.is-opening .folder-panel { animation: crt-collapse 1s both, crt-power-on .7s steps(14,end) .45s forwards }`.
  - `.experience-explorer.is-opening .folder-items { animation: crt-body-swap 1s both }`.
  - `.experience-explorer.is-opening .folder-panel::after` runs `crt-sweep .8s .6s` plus an infinite `crt-roll`.
  - Entry typing delay is `calc(.3s + var(--entry-index)*180ms)`.
  - `.topic-folder.is-open` is now included in the `.is-option-selected` rules (border/z-index, file transforms, hiding text/count).
  - The `.topic-folder.is-open{opacity:0}` rule was removed.

Status:
- [x] Keyboard flow: arrows move focus only, ArrowRight/Enter/click open, initial state is NO SIGNAL (tested).
- [x] Collapse/ease-in-out/power-on animation geometry measured.
- [x] Open folder keeps its open look when focus moves (tested).
- [ ] The `projects` panel (349px) overflows the screen by ~9px and causes a scrollbar. The fix is not yet applied.
- [ ] Not tested: the Cyberpunk theme, the ≤460px layout, and the reduced-motion block (no CSS error was seen). The `problems` tool reported no errors on view.js/styles.css/controller.js at last check.
</work_done>

<technical_details>
- The environment has no Python or Node, and `apply_patch` and `rg` are unavailable. Use the `edit`/`create` tools for changes. Avoid PowerShell file rewrites, which break UTF-8 glyphs such as `↗`.
- The embedded browser tab is hidden (`visibilityState: "hidden"`). CSS animations don't advance in real time, and screenshots can be stale or black (compositor repaint). To inspect frames:
  - Trigger the action.
  - Pause all animations with `document.getAnimations().forEach(a=>a.pause())`, then set `a.currentTime=t`.
  - Measure with `getBoundingClientRect`/`getComputedStyle`.
  - Screenshots after seeking sometimes show stale states. Re-screenshot, or use `page.screenshot({clip})` with `waitForTimeout`.
  - Infinite animations (`crt-flicker`, `crt-roll`) can't be `.finish()`ed.
  - `runPlaywrightCode` with `page.keyboard.press` works for ArrowDown/ArrowRight/Enter.
- Page flow: `Controller.init` → `View.init` → `collapseExperienceFolder()`. `showScreen("experience")` also collapses, so the screen starts at NO SIGNAL. `View.optionIndex` and `setOptionIndex` wrap around. `.is-option-selected` is the focus highlight and `.is-open` is the confirmed folder.
- `@property --crt-s` (number, initial 1) is needed so `scaleY` can be animated through a custom property. The header counter-scale is `1/--crt-s`.
- Folder visuals: `.folder-front` is `rotateX(-40deg)` when selected and `rotateX(-105deg)` when open. `backface-visibility:hidden` hides it when flipped. The focused-but-not-open folder shows a big tilted trapezoid. This is the original hover design for all folders.
- Layout detail: the explorer grid is 2 columns, with the left column holding 3 folders at 88px each plus gap, which totals 310px. The panel's `min-height` is 270px but grows with content.
- `select.mp3` net::ERR_ABORTED console messages are harmless.
- Open question: what exactly the user means by "la 3ra carpeta se ha roto". The scroll/overflow of the `projects` panel is my best guess.
</technical_details>

<important_files>
- `c:\Users\victo\WebProjects\Hacker-Portfolio\js\view.js`: `renderExperienceFolder` (~line 142) and `collapseExperienceFolder` (~line 183).
- `c:\Users\victo\WebProjects\Hacker-Portfolio\js\controller.js`: key bindings (~line 70 click, ~line 120 ArrowRight).
- `c:\Users\victo\WebProjects\Hacker-Portfolio\styles.css`: explorer/folder/panel/CRT styles at ~lines 478–546, with:
  - `.folder-items` at 513
  - `.folder-entry` at 514–515 and 543–546 (entry h4/p/meta/cta sizing)
  - the `crt-*` keyframes at ~517–535
  - mobile overrides at ~560–583
  - the reduced-motion block at the end
- `c:\Users\victo\WebProjects\Hacker-Portfolio\index.html`: `#screen-experience` markup (`.experience-explorer`, `.experience-folders` with 3 `.topic-folder[data-folder]`, `#folder-panel` with `#folder-path`, `#folder-status`, `#folder-items`).
- `c:\Users\victo\WebProjects\Hacker-Portfolio\js\model.js`: `experienceFolders` (work/education/projects), `jobExperience`, `studies`, `projects` data. `projects` has 2 entries with a CTA each, so it is the tallest.
</important_files>

<next_steps>
Remaining work:
- Fix the `projects` panel overflow so the screen no longer gets a scrollbar. Options:
  - Tighten `.folder-items` padding/gap (13px/9px), `.folder-entry` padding (12px), and the `h4`/`p` margins or line-height. Spacing tweaks alone saved about 23px by my estimate, and the panel needs about 30px or more, so also reduce text sizes or `.card-meta`/`.card-cta` margins.
  - Alternatively give `.folder-panel` a fixed height equal to the left column (310px) and make `.folder-items` scroll internally (`overflow-y:auto`). Use this as the fallback if tightening isn't enough.
  - Target: panel ≤ 310px, with `.screen` scrollHeight == clientHeight (573) when `projects` is open.
- Verify in the browser:
  - `projects` open: scrollHeight/clientHeight, panel height, no scrollbar, and the third folder looks correct both open and focused.
  - `work` and `education` are unchanged.
- If the user's meaning differs, for example the tilted focused 3rd folder, ask via `ask_user`.
- Optional checks: the Cyberpunk theme, the ≤460px layout, and `problems` on view.js/controller.js/styles.css.
- Then give the user a concise Spanish summary.
- Clean up temp files. `C:\Users\victo\AppData\Local\Temp\p1.png` and `p2.png` may or may not exist, so delete `p*.png` if present.

Immediate next step: edit `.folder-items`/`.folder-entry` spacing in `styles.css` (lines ~513–514 and ~543–546), reload, open `projects` with Right/Enter, and measure.
</next_steps>