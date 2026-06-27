<script setup>
/* ============================================================================
 * Motif Recipe, Inline Validation (Vue 3, <script setup>)
 * ----------------------------------------------------------------------------
 * Validates a single field as the user works, but announces calmly: errors are
 * shown on blur (or on submit), cleared the moment the field becomes valid, and
 * never flashed mid-typing. The message is wired to the input via
 * aria-describedby and aria-invalid so assistive tech hears it.
 *
 * Strategy:
 *   - "eager once dirty": stay silent until the user leaves the field the first
 *     time (or a submit is attempted). After that, re-validate live on input so
 *     a correction is acknowledged immediately. This avoids yelling at someone
 *     who is still typing their email.
 *   - The validator is injected via the `rules` prop (array of pure functions)
 *     so the component is transport/domain-agnostic and unit-testable.
 *
 * Accessibility:
 *   - aria-invalid reflects the error state; aria-describedby links the message.
 *   - The message container is role="alert" only while erroring so a newly
 *     surfaced error is announced once, without spamming on every keystroke.
 *   - Error is conveyed with text + icon, never colour alone.
 *
 * Reduced motion:
 *   - The message reveal uses a transform/opacity <Transition> that collapses to
 *     an instant swap under prefers-reduced-motion (scoped @media guard).
 * Provenance: original (clean-room).
 * ========================================================================== */
import { ref, computed, watch, onMounted, onUnmounted } from "vue";

const props = defineProps({
  modelValue: { type: String, default: "" },
  label: { type: String, required: true },
  /** Array of (value) => string|undefined. Return a message to flag an error. */
  rules: { type: Array, default: () => [] },
  type: { type: String, default: "text" },
  /** Stable id base for input/message wiring. */
  id: { type: String, default: () => `motif-field-${Math.random().toString(36).slice(2, 8)}` },
  required: { type: Boolean, default: false },
});

const emit = defineEmits(["update:modelValue", "validity"]);

/* ---- reduced motion (dependency-free) ----------------------------------- */
const reduced = ref(false);
let mq;
const onMq = (e) => (reduced.value = e.matches);
onMounted(() => {
  if (typeof window === "undefined" || !window.matchMedia) return;
  mq = window.matchMedia("(prefers-reduced-motion: reduce)");
  reduced.value = mq.matches;
  mq.addEventListener?.("change", onMq);
});
onUnmounted(() => mq?.removeEventListener?.("change", onMq));
const transitionName = computed(() => (reduced.value ? "motif-none" : "motif-msg"));

/* ---- validation lifecycle ----------------------------------------------- */
const touched = ref(false); // becomes true on first blur or submit attempt
const error = ref("");

/** Run rules; return first message or "". Pure, no side effects. */
function evaluate(value) {
  for (const rule of props.rules) {
    const msg = rule(value);
    if (msg) return msg;
  }
  return "";
}

/** Re-validate and emit current validity. Only surfaces the message if touched. */
function revalidate() {
  const next = evaluate(props.modelValue);
  error.value = touched.value ? next : "";
  emit("validity", { valid: next === "", message: next });
}

function onInput(e) {
  emit("update:modelValue", e.target.value);
}
function onBlur() {
  touched.value = true;
  revalidate();
}

/** Public: force-show validation (e.g. called by a parent form on submit). */
function validate() {
  touched.value = true;
  revalidate();
  return error.value === "";
}
defineExpose({ validate });

// Live re-validation once the field is dirty, so corrections clear instantly.
watch(() => props.modelValue, () => { if (touched.value) revalidate(); });

const describedBy = computed(() => (error.value ? `${props.id}-error` : undefined));
const invalid = computed(() => Boolean(error.value));
</script>

<template>
  <div class="motif-field" :data-invalid="invalid">
    <label :for="id" class="motif-field__label">
      {{ label }}<span v-if="required" aria-hidden="true"> *</span>
    </label>

    <input
      :id="id"
      class="motif-field__input"
      :type="type"
      :value="modelValue"
      :aria-invalid="invalid"
      :aria-describedby="describedBy"
      :required="required"
      @input="onInput"
      @blur="onBlur"
    />

    <Transition :name="transitionName">
      <p
        v-if="error"
        :id="`${id}-error`"
        class="motif-field__error"
        role="alert"
      >
        <span class="motif-field__icon" aria-hidden="true">!</span>
        {{ error }}
      </p>
    </Transition>
  </div>
</template>

<style scoped>
.motif-field {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  max-width: 28rem;
}
.motif-field__label {
  font: inherit;
  font-weight: 600;
  font-size: 0.875rem;
}
.motif-field__input {
  font: inherit;
  padding: 0.5rem 0.75rem;
  min-height: 44px; /* coarse-pointer friendly */
  border-radius: 0.5rem;
  border: 1px solid var(--motif-border, #cbd5e1);
  background: var(--motif-surface, #fff);
}
.motif-field__input:focus-visible {
  outline: 2px solid var(--motif-focus, #1d4ed8);
  outline-offset: 2px;
}
.motif-field[data-invalid="true"] .motif-field__input {
  border-color: var(--motif-danger, #dc2626);
}
.motif-field__error {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  color: var(--motif-danger, #dc2626);
}
.motif-field__icon {
  display: inline-grid;
  place-items: center;
  width: 1.1rem;
  height: 1.1rem;
  border-radius: 50%;
  background: var(--motif-danger, #dc2626);
  color: #fff;
  font-weight: 700;
  font-size: 0.75rem;
}

/* Message reveal: transform + opacity only. */
.motif-msg-enter-active,
.motif-msg-leave-active {
  transition: opacity 160ms ease, transform 160ms ease;
}
.motif-msg-enter-from,
.motif-msg-leave-to {
  opacity: 0;
  transform: translateY(-2px);
}

@media (prefers-reduced-motion: reduce) {
  .motif-msg-enter-active,
  .motif-msg-leave-active {
    transition: none !important;
  }
  .motif-msg-enter-from,
  .motif-msg-leave-to {
    transform: none !important;
  }
}
</style>
