# Notification Toast, Vue 3

A stacked toast region that slides notifications in (transform/opacity), auto-dismisses
after a timeout, and is fully dismissible by keyboard or pointer. It **never steals
focus**: toasts are announced through an `aria-live` region so the user's current task
is never interrupted.

File: [`NotificationToast.vue`](./NotificationToast.vue).

## Usage

```vue
<script setup>
import { ref } from "vue";
import NotificationToast from "./NotificationToast.vue";

const toasts = ref([]);
let n = 0;
function notify(message, type = "info") {
  toasts.value = [...toasts.value, { id: ++n, message, type }];
}
</script>

<template>
  <button @click="notify('Saved to your library', 'success')">Save</button>
  <NotificationToast v-model:toasts="toasts" position="bottom-end" />
</template>
```

Each toast is `{ id, message, type?, duration?, action? }`. `type` is one of
`info | success | error | warning`. Pass `duration: 0` for a sticky toast, or
`action: { label }` to render an inline action button (emits `action`).

## Algorithm

1. New toasts entering the `TransitionGroup` fire the `@enter` hook, which arms a
   per-toast auto-dismiss timer (`defaultDuration`, default 5s; `duration: 0` = sticky).
2. Hovering or focusing a toast **pauses** its timer (clears it) so it can be read and
   the dismiss button reached; `mouseleave`/`focusout` **resumes** it.
3. Dismissal (timeout, close button, or action) removes the toast from the array via
   `update:toasts` and emits `dismiss`. The `TransitionGroup` animates the exit and the
   `position: absolute` leave-state lets the stack close its gap smoothly.

## Accessibility

- The container is a labelled `role="region"`; each toast is `role="status"`.
- Info/success/warning toasts announce with `aria-live="polite"`; **errors use
  `aria-live="assertive"`** so urgent messages are heard promptly, still without moving
  focus.
- **No focus steal:** focus stays wherever the user left it. The toast is reachable in
  the tab order if the user wants the close/action button, but nothing is auto-focused.
- The close button has a descriptive `aria-label` that includes the message. Type is
  conveyed by a left border + icon + text, never colour alone.
- Close and action targets are 44px for coarse pointers; focus rings are always visible.

## Reduced-motion behaviour

The enter/leave transition (slide-in + fade via `translateX`/opacity) is removed under
`@media (prefers-reduced-motion: reduce)`; toasts appear and disappear instantly.

## Responsive behaviour

Fixed to a configurable corner, capped at `min(28rem, 100vw - 2rem)` so it never
overflows narrow screens. The region uses `pointer-events: none` with toasts re-enabling
pointer events, so clicks pass through the gaps between toasts.

## Browser support

All modern browsers. Uses `<TransitionGroup>` and standard ARIA only.

## Provenance: original (clean-room).
