<script setup>
/* ============================================================================
 * OII Recipe — Optimistic Save (Vue 3, <script setup>)
 * ----------------------------------------------------------------------------
 * Demonstrates the optimistic-save UX: the UI assumes success the instant the
 * user acts, shows a transient "Saving…" then "Saved", and rolls back to an
 * "error" state only if the (caller-provided) async save rejects.
 *
 * State machine:  idle ──save()──▶ saving ──ok──▶ saved ──(timeout)──▶ idle
 *                                        └──err─▶ error ──retry/save──▶ saving
 *
 * Accessibility:
 *   - A visually-hidden aria-live="polite" region announces each status so
 *     screen-reader users hear "Saving", "Saved", "Couldn't save" etc.
 *   - The button reflects busy state via aria-busy and is disabled while saving.
 *   - Status icon/text use transform+opacity transitions only.
 *
 * Reduced motion:
 *   - usePrefersReducedMotion() + a scoped @media guard. When reduced, the
 *     <Transition> is bypassed (instant state swap) and no transforms run.
 *
 * No external dependencies. The async work is injected via the `saveFn` prop so
 * the component is transport-agnostic and unit-testable.
 * Provenance: original (clean-room).
 * ========================================================================== */
import { ref, computed, onMounted, onUnmounted } from "vue";

const props = defineProps({
  /** Async function performing the real save. Must return a Promise. */
  saveFn: { type: Function, default: () => Promise.resolve() },
  /** Button label in the idle state. */
  label: { type: String, default: "Save" },
  /** How long the "Saved" confirmation lingers before returning to idle (ms). */
  savedDuration: { type: Number, default: 1600 },
  /** Force-disable animation regardless of system preference. */
  disableAnimation: { type: Boolean, default: false },
});

const emit = defineEmits(["stateChange", "saved", "error"]);

/* ---- reduced-motion: live, dependency-free composable -------------------- */
const reducedMotion = ref(false);
let mq;
const onMqChange = (e) => (reducedMotion.value = e.matches);
onMounted(() => {
  if (typeof window === "undefined" || !window.matchMedia) return;
  mq = window.matchMedia("(prefers-reduced-motion: reduce)");
  reducedMotion.value = mq.matches;
  mq.addEventListener?.("change", onMqChange);
});
onUnmounted(() => mq?.removeEventListener?.("change", onMqChange));

/** True when we must not animate (system pref OR explicit opt-out). */
const noMotion = computed(() => props.disableAnimation || reducedMotion.value);
/** Transition name: a no-op when motion is suppressed. */
const transitionName = computed(() => (noMotion.value ? "oii-none" : "oii-status"));

/* ---- state machine ------------------------------------------------------- */
const state = ref("idle"); // 'idle' | 'saving' | 'saved' | 'error'
let savedTimer = null;

const setState = (next) => {
  state.value = next;
  emit("stateChange", next);
};

const clearSavedTimer = () => {
  if (savedTimer) {
    clearTimeout(savedTimer);
    savedTimer = null;
  }
};

async function save() {
  if (state.value === "saving") return; // ignore re-entry while in flight
  clearSavedTimer();
  setState("saving"); // optimistic: show progress immediately

  try {
    await props.saveFn();
    setState("saved");
    emit("saved");
    // Linger on "Saved", then quietly return to idle so the control is reusable.
    savedTimer = setTimeout(() => {
      if (state.value === "saved") setState("idle");
    }, props.savedDuration);
  } catch (err) {
    setState("error");
    emit("error", err);
  }
}

onUnmounted(clearSavedTimer);

/* ---- view helpers -------------------------------------------------------- */
const isBusy = computed(() => state.value === "saving");

/** Human-readable status used for both the visible chip and the live region. */
const statusText = computed(
  () =>
    ({
      idle: "",
      saving: "Saving…",
      saved: "Saved",
      error: "Couldn't save — tap to retry",
    }[state.value])
);

const buttonLabel = computed(() =>
  state.value === "error" ? "Retry" : props.label
);
</script>

<template>
  <div class="oii-optimistic" :data-state="state">
    <button
      type="button"
      class="oii-optimistic__btn"
      :class="{ 'is-error': state === 'error' }"
      :aria-busy="isBusy"
      :disabled="isBusy"
      @click="save"
    >
      {{ buttonLabel }}
    </button>

    <!-- Visual status chip. aria-hidden because the live region below is the
         accessible source of truth (prevents double announcement). -->
    <Transition :name="transitionName">
      <span
        v-if="statusText"
        :key="state"
        class="oii-optimistic__status"
        :class="`is-${state}`"
        aria-hidden="true"
      >
        <span class="oii-optimistic__dot" />
        {{ statusText }}
      </span>
    </Transition>

    <!-- Polite live region: announces status changes without stealing focus. -->
    <span class="oii-sr-only" role="status" aria-live="polite">
      {{ statusText }}
    </span>
  </div>
</template>

<style scoped>
.oii-optimistic {
  display: inline-flex;
  align-items: center;
  gap: 0.625rem;
}

.oii-optimistic__btn {
  font: inherit;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--oii-border, #cbd5e1);
  background: var(--oii-accent, #2563eb);
  color: #fff;
  cursor: pointer;
  min-height: 44px; /* coarse-pointer friendly target */
}
.oii-optimistic__btn:disabled {
  cursor: progress;
  opacity: 0.8;
}
.oii-optimistic__btn.is-error {
  background: var(--oii-danger, #dc2626);
}
/* Always keep a visible keyboard focus ring. */
.oii-optimistic__btn:focus-visible {
  outline: 2px solid var(--oii-focus, #1d4ed8);
  outline-offset: 2px;
}

.oii-optimistic__status {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  color: var(--oii-muted, #475569);
}
.oii-optimistic__status.is-error {
  color: var(--oii-danger, #dc2626);
}
.oii-optimistic__status.is-saved {
  color: var(--oii-success, #16a34a);
}

.oii-optimistic__dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: currentColor;
}
/* Subtle pulse while saving — transform/opacity only, motion-safe. */
.is-saving .oii-optimistic__dot {
  animation: oii-pulse 1s ease-in-out infinite;
}

@keyframes oii-pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(0.6);
    opacity: 0.5;
  }
}

/* Enter/leave transition for the status chip (transform + opacity). */
.oii-status-enter-active,
.oii-status-leave-active {
  transition: opacity 200ms ease, transform 200ms ease;
}
.oii-status-enter-from,
.oii-status-leave-to {
  opacity: 0;
  transform: translateY(4px);
}

/* Visually-hidden but screen-reader-available live region. */
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

/* Reduced motion: instant state changes, no pulse, no chip transition.
   The `oii-none` transition has no CSS, so <Transition> swaps instantly. */
@media (prefers-reduced-motion: reduce) {
  .oii-optimistic__dot,
  .is-saving .oii-optimistic__dot {
    animation: none !important;
  }
  .oii-status-enter-active,
  .oii-status-leave-active {
    transition: none !important;
  }
  .oii-status-enter-from,
  .oii-status-leave-to {
    transform: none !important;
  }
}
</style>
