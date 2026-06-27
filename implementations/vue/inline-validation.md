# Inline Validation, Vue 3

A single text field that validates as the user works, but speaks calmly: it stays
silent while you are still typing, surfaces the first error when you leave the field
(or when the parent calls `validate()` on submit), and clears the message the instant
the value becomes valid again.

File: [`InlineValidation.vue`](./InlineValidation.vue).

## Usage

```vue
<script setup>
import { ref } from "vue";
import InlineValidation from "./InlineValidation.vue";

const email = ref("");
const rules = [
  (v) => (!v ? "Email is required" : undefined),
  (v) => (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v) ? "Enter a valid email" : undefined),
];
</script>

<template>
  <InlineValidation v-model="email" label="Work email" type="email" :rules="rules" required />
</template>
```

`rules` is an array of pure `(value) => string | undefined` functions; the first one
that returns a string wins. Inject domain logic there, the component stays generic.

## Algorithm

1. The field is **untouched** initially, so no error is shown even if invalid (do not
   yell at someone mid-typing).
2. On **blur** (or when a parent calls the exposed `validate()`), `touched` becomes
   true and the rules run. The first failing rule's message is surfaced.
3. Once touched, a `watch` on the model **re-validates on every input**, so a
   correction clears the message immediately, positive, prompt feedback.
4. Every evaluation emits `validity: { valid, message }` so a parent form can gate
   submission. `validate()` returns a boolean and force-shows the error.

## Accessibility

- `aria-invalid` mirrors the error state on the input.
- `aria-describedby` links the input to the message id only while erroring, so AT
  reads the message as the field's description.
- The message is `role="alert"`, announced once when it appears; because it is only
  rendered while erroring (not on every keystroke), there is no announcement spam.
- The error is conveyed by **text + icon**, never colour alone. The label keeps its
  `for`/`id` association and the focus ring is always visible.

## Reduced-motion behaviour

The message uses a small transform/opacity `<Transition>`. Under
`prefers-reduced-motion: reduce` the transition is switched to the empty `motif-none`
name and the scoped `@media` guard removes the transform, so the message simply
appears, no slide.

## Browser support

All modern browsers. Uses only `matchMedia`, `<Transition>`, and standard ARIA. The
`matchMedia` change listener uses optional chaining so its absence is harmless.

## Responsive behaviour

Fluid; the field is capped at a readable `max-width` and the input target is at least
44px tall for coarse pointers. No fixed pixel motion.

## Provenance: original (clean-room).
