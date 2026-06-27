<script setup>
/* ============================================================================
 * OII Recipe — Save Status Indicator (Frappe-Vue)
 * ----------------------------------------------------------------------------
 * A compact "pending / saving / saved / error" status pill suited to a Frappe
 * form field or toolbar. It is a PRESENTATIONAL component: it renders whatever
 * `status` it's given and emits `retry` — it does NOT call the backend itself.
 *
 * This keeps it usable both inside a frappe-ui SPA (driven by a `createResource`
 * or a `frappe.call` promise in the parent) and in classic Desk (mounted into a
 * form via a custom HTML field), without bundling any Frappe dependency. See
 * save-status.md for the wiring snippets.
 *
 * Only Vue 3 + plain scoped CSS. aria-live="polite". Reduced-motion safe.
 * Provenance: original (clean-room).
 * ========================================================================== */
import { computed, onMounted, onUnmounted, ref } from "vue";

const props = defineProps({
  /**
   * Current status. Typically bound to the parent's save lifecycle.
   * 'pending' = unsaved edits, 'saving' = request in flight,
   * 'saved' = persisted, 'error' = request failed, 'idle' = nothing to show.
   */
  status: {
    type: String,
    default: "idle",
    validator: (v) =>
      ["idle", "pending", "saving", "saved", "error"].includes(v),
  },
  /** Optional override for the error sub-message (e.g. frappe._('...')). */
  errorMessage: { type: String, default: "Not saved" },
  /** Force-disable animation regardless of system preference. */
  disableAnimation: { type: Boolean, default: false },
});

const emit = defineEmits(["retry"]);

/* ---- reduced motion: live, dependency-free ------------------------------- */
const reduced = ref(false);
let mq;
const onChange = (e) => (reduced.value = e.matches);
onMounted(() => {
  if (typeof window === "undefined" || !window.matchMedia) return;
  mq = window.matchMedia("(prefers-reduced-motion: reduce)");
  reduced.value = mq.matches;
  mq.addEventListener?.("change", onChange);
});
onUnmounted(() => mq?.removeEventListener?.("change", onChange));

const noMotion = computed(() => props.disableAnimation || reduced.value);

/* ---- presentation -------------------------------------------------------- */
const META = {
  idle: { label: "", icon: "", tone: "muted" },
  pending: { label: "Unsaved changes", icon: "•", tone: "pending" },
  saving: { label: "Saving…", icon: "", tone: "saving" },
  saved: { label: "Saved", icon: "✓", tone: "saved" },
  error: { label: "Not saved", icon: "!", tone: "error" },
};

const meta = computed(() => META[props.status] ?? META.idle);
const visibleLabel = computed(() =>
  props.status === "error" ? props.errorMessage : meta.value.label
);
const isError = computed(() => props.status === "error");
</script>

<template>
  <div
    v-if="status !== 'idle'"
    class="oii-save-status"
    :class="[`is-${status}`, { 'no-motion': noMotion }]"
    :data-status="status"
  >
    <!-- Icon area. The saving spinner uses transform-only animation. -->
    <span class="oii-save-status__icon" aria-hidden="true">
      <span v-if="status === 'saving'" class="oii-save-status__spinner" />
      <span v-else>{{ meta.icon }}</span>
    </span>

    <span class="oii-save-status__label">{{ visibleLabel }}</span>

    <!-- Retry affordance for the error state. Real focusable button. -->
    <button
      v-if="isError"
      type="button"
      class="oii-save-status__retry"
      @click="emit('retry')"
    >
      Retry
    </button>

    <!-- Polite live region — announces status to AT without moving focus. -->
    <span class="oii-sr-only" role="status" aria-live="polite">
      {{ visibleLabel }}
    </span>
  </div>
</template>

<style scoped>
/* Colours read from frappe-ui / Frappe CSS variables where present, with safe
   fallbacks so the component also works standalone. */
.oii-save-status {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  line-height: 1;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  color: var(--text-muted, #6b7280);
  /* Fade/slide in. Animatable, compositor-friendly. */
  animation: oii-status-in 180ms ease-out both;
}

.oii-save-status.is-pending {
  color: var(--oii-pending, #b45309);
}
.oii-save-status.is-saving {
  color: var(--text-muted, #6b7280);
}
.oii-save-status.is-saved {
  color: var(--oii-success, #16a34a);
}
.oii-save-status.is-error {
  color: var(--oii-danger, #dc2626);
}

.oii-save-status__icon {
  display: inline-flex;
  width: 0.875rem;
  justify-content: center;
  font-weight: 700;
}

/* Saving spinner: a rotating ring built from borders, transform-only. */
.oii-save-status__spinner {
  width: 0.75rem;
  height: 0.75rem;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: oii-spin 0.7s linear infinite;
}

.oii-save-status__retry {
  font: inherit;
  font-size: 0.75rem;
  margin-left: 0.25rem;
  padding: 0.125rem 0.375rem;
  min-height: 28px;
  border: 1px solid currentColor;
  border-radius: 0.25rem;
  background: transparent;
  color: inherit;
  cursor: pointer;
}
.oii-save-status__retry:focus-visible {
  outline: 2px solid var(--oii-focus, #1d4ed8);
  outline-offset: 1px;
}

@keyframes oii-spin {
  to {
    transform: rotate(360deg);
  }
}
@keyframes oii-status-in {
  from {
    opacity: 0;
    transform: translateY(2px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.oii-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
  border: 0;
}

/* Reduced motion: no spinner rotation, no entrance animation. The spinner
   becomes a static ring (still a clear "in progress" affordance). The
   .no-motion class (set from JS when matchMedia matches or disableAnimation)
   covers engines that ignore the media query at runtime. */
@media (prefers-reduced-motion: reduce) {
  .oii-save-status,
  .oii-save-status__spinner {
    animation: none !important;
  }
}
.oii-save-status.no-motion,
.oii-save-status.no-motion .oii-save-status__spinner {
  animation: none !important;
}
</style>
