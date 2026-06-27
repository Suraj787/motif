# Command Palette, browser-native

A keyboard-first command palette (Cmd/Ctrl-K) built on the native `<dialog>` element.
It reveals with a cheap transform/opacity transition, traps focus while open, restores
focus to whatever opened it on close, and supports full arrow-key navigation with
type-to-filter.

Files: [`command-palette.js`](./command-palette.js), [`command-palette.css`](./command-palette.css).

## Usage

```html
<link rel="stylesheet" href="./command-palette.css" />
<script type="module">
  import { createCommandPalette } from "./command-palette.js";

  const palette = createCommandPalette({
    commands: [
      { id: "new", label: "New document", hint: "⌘N", run: () => createDoc() },
      { id: "search", label: "Search…", hint: "/", run: () => focusSearch() },
      { id: "theme", label: "Toggle theme", run: () => toggleTheme() },
    ],
  });
  // Cmd/Ctrl-K toggles it automatically; you can also call palette.open().
</script>
```

`createCommandPalette` returns `{ open, close, setCommands, dispose }`. Each command is
`{ id, label, hint?, run }`; `run` is invoked after the palette closes so focus
restoration is never clobbered by the command's own focus moves.

## Algorithm

1. **Summon:** a global `keydown` listener catches the Cmd/Ctrl-K chord and toggles the
   palette. `open()` records `document.activeElement` as `lastFocused`, clears the
   input, then calls `dialog.showModal()`.
2. **Native modality:** `<dialog>.showModal()` makes the rest of the document inert,
   moves the dialog to the top layer, and provides the focus trap for free, no manual
   tabindex juggling. The text input receives focus.
3. **Filter:** typing filters commands by case-insensitive substring; the active index
   resets to the top and the list re-renders.
4. **Navigate:** Arrow Up/Down (with wrap-around), Home, and End move the active option.
   The input keeps DOM focus throughout; the active option is communicated via
   `aria-activedescendant` + `aria-selected` (combobox/listbox pattern).
5. **Select:** Enter or a pointer tap runs the active command. The palette closes first,
   then the command runs on a microtask.
6. **Dismiss:** Escape triggers the dialog's native `cancel`/`close`; our `close`
   handler restores focus to `lastFocused`.

## Accessibility

- Built on `<dialog>` for correct modal semantics and background inertness.
- The input is `role="combobox"` with `aria-controls`, `aria-autocomplete="list"`, and
  `aria-activedescendant`; the list is `role="listbox"` of `role="option"` items. This
  keeps focus on the input while screen readers announce the active option.
- **Escape restores focus** to the trigger element; selection also restores focus.
- An empty-state message appears (and `aria-activedescendant` is dropped) when nothing
  matches.
- A `forced-colors` rule keeps the active option visible in high-contrast mode.

## Reduced-motion behaviour

The open animation (`motif-cmdk-in`, a small translate + scale + fade) and the backdrop
fade are disabled under `@media (prefers-reduced-motion: reduce)`, so the palette
appears instantly with no movement.

## Coarse pointer / responsive

Options are full-width rows at least 44px tall; tapping selects. The panel is
`min(40rem, 100vw - 2rem)` wide and pinned near the top so it does not jump with content
height. The list scrolls within a `60vh` cap.

## Browser support

`<dialog>` with `showModal()` and `::backdrop`: all current evergreen browsers and
Safari 15.4+. The code degrades to the `open` attribute and manual focus restoration if
`showModal` is unavailable. `color-mix` is used only for the subtle active tint and
falls back gracefully.

## Provenance: original (clean-room).
