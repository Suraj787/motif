# Success Check, browser-native

A short, dignified success confirmation: a checkmark draws in (SVG stroke) and a brief
message appears, then it quietly settles. **No confetti, no bounce, no sound.** The
outcome is announced to assistive tech via `role="status"`.

Files: [`success-check.js`](./success-check.js), [`success-check.css`](./success-check.css).

## Usage

```html
<link rel="stylesheet" href="./success-check.css" />
<script type="module">
  import { createSuccessCheck } from "./success-check.js";

  const ok = createSuccessCheck({ lingerMs: 1800 });
  // After a successful save:
  ok.show("Saved");   // draws the check, announces "Saved", auto-hides after linger
</script>
```

`createSuccessCheck` builds its own small DOM and returns `{ el, show, hide, dispose }`.
`show(message)` can be called repeatedly; the draw animation restarts each time. Pass
`lingerMs: 0` to keep it until you call `hide()`.

## Algorithm

1. `show(msg)` sets the message text, unhides the element, and, **unless reduced motion is
   requested**, replays the draw by toggling `is-animating` (a forced reflow re-triggers
   the keyframes).
2. CSS draws the ring then the tick via `stroke-dashoffset` (a compositor-cheap stroke
   draw, no layout), and fades the message up.
3. After `lingerMs` the confirmation auto-hides; calling `show()` again before then resets
   the timer.

The **resting/default** CSS state shows the check fully drawn and visible, so if JS never
adds `is-animating` (e.g. reduced motion, or JS disabled after markup exists) the check is
still correct and present, never half-drawn.

## Accessibility

- The container is `role="status"` / `aria-live="polite"`, so the message text is
  announced once when shown, without stealing focus.
- The SVG mark is `aria-hidden`; the meaning is the message text.
- Success is conveyed by the tick shape + text, not colour alone. It is intentionally
  brief and quiet, a calm confirmation, not a celebration.

## Reduced-motion behaviour

Under `@media (prefers-reduced-motion: reduce)` no stroke draw, fade, or movement runs,
the check is shown already complete and the message is static. The JS also skips adding
the animation class.

## Responsive behaviour

Inline-flex; sits naturally next to a button or in a toolbar. The mark is a fixed small
40px SVG; the message text reflows. No layout-affecting motion.

## Browser support

All modern browsers. SVG stroke-dash animation and `matchMedia` are universally
supported; the element is SSR-guarded via a `typeof document` check.

## Provenance: original (clean-room).
