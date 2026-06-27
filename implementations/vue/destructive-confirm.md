# Destructive Confirmation, Vue 3

A modal that asks the user to confirm an irreversible action (delete, revoke, purge).
It spells out the **consequence** in plain language, defaults focus to the **safe**
choice (Cancel), lets **Escape cancel**, and traps focus while open, built on the native
`<dialog>` element.

File: [`DestructiveConfirm.vue`](./DestructiveConfirm.vue).

## Usage

```vue
<script setup>
import { ref } from "vue";
import DestructiveConfirm from "./DestructiveConfirm.vue";

const open = ref(false);
function reallyDelete() { /* perform the delete */ }
</script>

<template>
  <button @click="open = true">Delete project</button>

  <DestructiveConfirm
    v-model:open="open"
    title="Delete this project?"
    consequence="This permanently removes the project and its 42 tasks. This cannot be undone."
    confirm-label="Delete project"
    confirm-phrase="my-project"   
    @confirm="reallyDelete"
  />
</template>
```

`confirm-phrase` is optional: when set, the destructive button stays disabled until the
user types that exact phrase (the record name), a deliberate speed-bump for high-stakes
deletes. Omit it for ordinary confirmations.

## Algorithm

1. `v-model:open` drives the dialog; a `watch` calls `showModal()` / `close()`.
2. On open, `document.activeElement` is saved and focus is moved to the element marked
   `data-default-focus`, the **Cancel** button, so the safe choice is selected by default.
3. `<dialog>.showModal()` provides the focus trap and inerts the background (platform
   behaviour, no manual tabindex juggling).
4. **Escape / backdrop** fire the dialog's native `cancel`; we `preventDefault` and route
   through our single `cancel()` path so teardown is consistent.
5. On any close, focus is **restored** to the trigger and `update:open` emits `false`.
6. Confirm is gated by `phraseOk` (always true unless `confirm-phrase` is set and matched).

## Accessibility

- `aria-labelledby` points at the title; the destructive button is `aria-describedby` the
  **consequence text**, so screen-reader users hear exactly what will happen before acting.
- Focus defaults to Cancel; Escape cancels; focus returns to the trigger on close.
- The danger button is disabled (and `aria-disabled` implied via `disabled`) until any
  required phrase matches. The warning is conveyed by an icon + text, not colour alone.
- All targets are 44px with visible focus rings.

## Reduced-motion behaviour

The open animation (small translate + scale + fade) and backdrop fade are disabled under
`@media (prefers-reduced-motion: reduce)`, the dialog appears instantly.

## Responsive behaviour

`min(28rem, 100vw - 2rem)` wide so it fits narrow screens; actions stay right-aligned and
wrap if needed. No fixed pixel motion.

## Browser support

`<dialog>` with `showModal()` and `::backdrop`: current evergreen browsers and Safari
15.4+. Degrades to the `open` attribute if `showModal` is unavailable.

## Provenance: original (clean-room).
