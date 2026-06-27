<script setup>
/* ============================================================================
 * Motif Recipe, Notification Toast (Vue 3, <script setup>)
 * ----------------------------------------------------------------------------
 * A stacked toast region that slides notifications in (transform/opacity), auto-
 * dismisses after a timeout, and is fully dismissible by keyboard or pointer.
 * It NEVER steals focus: toasts are announced via an aria-live region so the
 * user's current task is never interrupted.
 *
 * Design:
 *   - Toasts are passed in as a reactive array via v-model:toasts (or pushed by
 *     a parent). Each toast: { id, message, type?, duration?, action? }.
 *   - role="status" + aria-live="polite" for info/success; aria-live="assertive"
 *     for errors, so urgent messages are heard promptly without a focus grab.
 *   - Hovering or focusing a toast pauses its auto-dismiss timer (so it can be
 *     read / the dismiss button reached); leaving resumes it.
 *
 * Reduced motion:
 *   - The TransitionGroup slide collapses to an instant add/remove under
 *     prefers-reduced-motion (scoped @media guard); no movement, just appear.
 * Provenance: original (clean-room).
 * ========================================================================== */
import { ref, onUnmounted } from "vue";

const props = defineProps({
  /** Array of toast objects: { id, message, type?, duration?, action? }. */
  toasts: { type: Array, default: () => [] },
  /** Default auto-dismiss in ms; pass 0 on a toast to make it sticky. */
  defaultDuration: { type: Number, default: 5000 },
  /** Corner: 'top-end' | 'bottom-end' | 'top-start' | 'bottom-start'. */
  position: { type: String, default: "bottom-end" },
});

const emit = defineEmits(["update:toasts", "dismiss", "action"]);

/** id -> timer handle, so we can pause/resume per toast. */
const timers = new Map();

function durationFor(t) {
  return typeof t.duration === "number" ? t.duration : props.defaultDuration;
}

function startTimer(t) {
  const ms = durationFor(t);
  if (!ms || ms <= 0) return; // sticky toast
  clearTimer(t.id);
  timers.set(
    t.id,
    setTimeout(() => dismiss(t.id), ms)
  );
}
function clearTimer(id) {
  const h = timers.get(id);
  if (h) {
    clearTimeout(h);
    timers.delete(id);
  }
}

function dismiss(id) {
  clearTimer(id);
  emit("dismiss", id);
  emit(
    "update:toasts",
    props.toasts.filter((t) => t.id !== id)
  );
}

function runAction(t) {
  emit("action", t);
  dismiss(t.id);
}

/* Pause on hover/focus so the toast can be read and reached; resume on leave. */
function pause(id) {
  clearTimer(id);
}
function resume(t) {
  startTimer(t);
}

/* Arm timers as toasts enter via the TransitionGroup hook. */
function onEnter(el) {
  const id = el.getAttribute("data-toast-id");
  const t = props.toasts.find((x) => String(x.id) === id);
  if (t) startTimer(t);
}

function liveness(t) {
  return t.type === "error" ? "assertive" : "polite";
}

onUnmounted(() => {
  timers.forEach((h) => clearTimeout(h));
  timers.clear();
});
</script>

<template>
  <!-- The region is a label-only container; individual toasts carry the live
       semantics so they announce as they arrive without moving focus. -->
  <div
    class="motif-toasts"
    :class="`is-${position}`"
    role="region"
    aria-label="Notifications"
  >
    <TransitionGroup name="motif-toast" tag="ol" class="motif-toasts__list" @enter="onEnter">
      <li
        v-for="t in toasts"
        :key="t.id"
        :data-toast-id="t.id"
        class="motif-toast"
        :class="`is-${t.type || 'info'}`"
        role="status"
        :aria-live="liveness(t)"
        @mouseenter="pause(t.id)"
        @mouseleave="resume(t)"
        @focusin="pause(t.id)"
        @focusout="resume(t)"
      >
        <span class="motif-toast__icon" aria-hidden="true"></span>
        <p class="motif-toast__msg">{{ t.message }}</p>

        <button
          v-if="t.action"
          type="button"
          class="motif-toast__action"
          @click="runAction(t)"
        >
          {{ t.action.label }}
        </button>

        <button
          type="button"
          class="motif-toast__close"
          :aria-label="`Dismiss: ${t.message}`"
          @click="dismiss(t.id)"
        >
          <span aria-hidden="true">×</span>
        </button>
      </li>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.motif-toasts {
  position: fixed;
  z-index: 1000;
  padding: 1rem;
  pointer-events: none; /* let clicks pass through gaps; toasts re-enable below */
  max-width: min(28rem, calc(100vw - 2rem));
}
.motif-toasts.is-bottom-end { right: 0; bottom: 0; }
.motif-toasts.is-top-end { right: 0; top: 0; }
.motif-toasts.is-bottom-start { left: 0; bottom: 0; }
.motif-toasts.is-top-start { left: 0; top: 0; }

.motif-toasts__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.motif-toast {
  pointer-events: auto;
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  align-items: center;
  gap: 0.625rem;
  padding: 0.75rem 0.875rem;
  border-radius: 0.625rem;
  background: var(--motif-surface, #ffffff);
  color: var(--motif-fg, #0f172a);
  border: 1px solid var(--motif-border, #e2e8f0);
  border-left: 4px solid var(--motif-accent, #2563eb);
  box-shadow: 0 12px 28px -12px rgb(15 23 42 / 0.35);
}
.motif-toast.is-success { border-left-color: var(--motif-success, #16a34a); }
.motif-toast.is-error { border-left-color: var(--motif-danger, #dc2626); }
.motif-toast.is-warning { border-left-color: var(--motif-warning, #d97706); }

.motif-toast__icon {
  width: 0.625rem;
  height: 0.625rem;
  border-radius: 50%;
  background: var(--motif-accent, #2563eb);
}
.motif-toast.is-success .motif-toast__icon { background: var(--motif-success, #16a34a); }
.motif-toast.is-error .motif-toast__icon { background: var(--motif-danger, #dc2626); }
.motif-toast.is-warning .motif-toast__icon { background: var(--motif-warning, #d97706); }

.motif-toast__msg {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.35;
}

.motif-toast__action {
  font: inherit;
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--motif-accent, #2563eb);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  min-height: 44px;
}
.motif-toast__close {
  font: inherit;
  line-height: 1;
  font-size: 1.25rem;
  color: var(--motif-muted, #64748b);
  background: none;
  border: none;
  cursor: pointer;
  width: 44px;
  height: 44px; /* coarse-pointer friendly */
  border-radius: 0.375rem;
}
.motif-toast__action:focus-visible,
.motif-toast__close:focus-visible {
  outline: 2px solid var(--motif-focus, #1d4ed8);
  outline-offset: 2px;
}

/* Enter/leave: slide + fade using transform/opacity only. */
.motif-toast-enter-active,
.motif-toast-leave-active {
  transition: opacity 220ms ease, transform 220ms ease;
}
.motif-toast-enter-from,
.motif-toast-leave-to {
  opacity: 0;
  transform: translateX(16px);
}
/* Smoothly close the gap when a toast leaves. */
.motif-toast-leave-active {
  position: absolute;
}

@media (prefers-reduced-motion: reduce) {
  .motif-toast-enter-active,
  .motif-toast-leave-active {
    transition: none !important;
  }
  .motif-toast-enter-from,
  .motif-toast-leave-to {
    transform: none !important;
  }
}
</style>
