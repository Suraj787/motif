<script setup>
/* ============================================================================
 * Motif Recipe, Destructive Confirmation (Vue 3, <script setup>)
 * ----------------------------------------------------------------------------
 * A modal that asks the user to confirm an irreversible action (delete, revoke,
 * purge). Built on the native <dialog> so the platform provides modality, focus
 * trapping, and background inertness. It spells out the CONSEQUENCE in plain
 * language, defaults focus to the SAFE choice (Cancel), and lets Escape cancel.
 *
 * Optional "type-to-confirm": require the user to type a phrase (e.g. the record
 * name) before the destructive button enables, for genuinely high-stakes deletes.
 *
 * Accessibility:
 *   - <dialog>.showModal() traps focus and inerts the page; Escape fires the
 *     native cancel → we treat that as Cancel and restore focus to the trigger.
 *   - The danger button is described by the consequence text via aria-describedby.
 *   - Focus is restored to whatever opened the dialog on close.
 *
 * Reduced motion: open/close animation (transform/opacity) is disabled via CSS
 * @media; the dialog simply appears.
 * Provenance: original (clean-room).
 * ========================================================================== */
import { ref, computed, watch, nextTick, onBeforeUnmount } from "vue";

const props = defineProps({
  /** Controls visibility (v-model:open). */
  open: { type: Boolean, default: false },
  title: { type: String, default: "Are you sure?" },
  /** Plain-language consequence, e.g. "This permanently deletes 3 invoices." */
  consequence: { type: String, default: "This action cannot be undone." },
  confirmLabel: { type: String, default: "Delete" },
  cancelLabel: { type: String, default: "Cancel" },
  /** If set, user must type this exact phrase to enable the destructive button. */
  confirmPhrase: { type: String, default: "" },
});

const emit = defineEmits(["update:open", "confirm", "cancel"]);

const dialogRef = ref(null);
const typed = ref("");
let lastFocused = null;

const descId = `motif-confirm-desc-${Math.random().toString(36).slice(2, 8)}`;

const needsPhrase = computed(() => props.confirmPhrase.length > 0);
const phraseOk = computed(
  () => !needsPhrase.value || typed.value.trim() === props.confirmPhrase
);

function showModal() {
  const dlg = dialogRef.value;
  if (!dlg || dlg.open) return;
  lastFocused = document.activeElement;
  typed.value = "";
  if (typeof dlg.showModal === "function") dlg.showModal();
  else dlg.setAttribute("open", "");
  // Default focus to the SAFE control (Cancel), not the destructive one.
  nextTick(() => dlg.querySelector("[data-default-focus]")?.focus());
}

function closeModal() {
  const dlg = dialogRef.value;
  if (!dlg || !dlg.open) return;
  if (typeof dlg.close === "function") dlg.close();
  else dlg.removeAttribute("open");
}

function restoreFocus() {
  if (lastFocused && typeof lastFocused.focus === "function") lastFocused.focus();
  lastFocused = null;
}

function onCancel(e) {
  // Native cancel (Escape / backdrop). Prevent default close so we route it
  // through our own cancel path for a single, consistent teardown.
  e.preventDefault();
  cancel();
}
function onClose() {
  // Fired after any close; ensure focus returns to the trigger.
  restoreFocus();
  if (props.open) emit("update:open", false);
}

function cancel() {
  emit("cancel");
  emit("update:open", false);
  closeModal();
}
function confirm() {
  if (!phraseOk.value) return;
  emit("confirm");
  emit("update:open", false);
  closeModal();
}

// Sync the native dialog with the `open` model.
watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) showModal();
    else closeModal();
  }
);

onBeforeUnmount(() => closeModal());
</script>

<template>
  <dialog
    ref="dialogRef"
    class="motif-confirm"
    aria-labelledby="motif-confirm-title"
    :aria-describedby="descId"
    @cancel="onCancel"
    @close="onClose"
  >
    <div class="motif-confirm__panel">
      <h2 id="motif-confirm-title" class="motif-confirm__title">
        <span class="motif-confirm__warn" aria-hidden="true">!</span>
        {{ title }}
      </h2>

      <p :id="descId" class="motif-confirm__consequence">{{ consequence }}</p>

      <label v-if="needsPhrase" class="motif-confirm__phrase">
        <span>Type <strong>{{ confirmPhrase }}</strong> to confirm</span>
        <input
          v-model="typed"
          type="text"
          autocomplete="off"
          spellcheck="false"
          class="motif-confirm__input"
        />
      </label>

      <div class="motif-confirm__actions">
        <button
          type="button"
          class="motif-confirm__btn is-cancel"
          data-default-focus
          @click="cancel"
        >
          {{ cancelLabel }}
        </button>
        <button
          type="button"
          class="motif-confirm__btn is-danger"
          :disabled="!phraseOk"
          :aria-describedby="descId"
          @click="confirm"
        >
          {{ confirmLabel }}
        </button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>
.motif-confirm {
  padding: 0;
  border: none;
  border-radius: 0.875rem;
  width: min(28rem, calc(100vw - 2rem));
  background: var(--motif-surface, #fff);
  color: var(--motif-fg, #0f172a);
  box-shadow: 0 24px 60px -12px rgb(15 23 42 / 0.4);
}
.motif-confirm::backdrop {
  background: rgb(15 23 42 / 0.45);
}
.motif-confirm__panel {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.motif-confirm__title {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
}
.motif-confirm__warn {
  display: grid;
  place-items: center;
  width: 1.6rem;
  height: 1.6rem;
  border-radius: 50%;
  background: var(--motif-danger, #dc2626);
  color: #fff;
  font-weight: 700;
}
.motif-confirm__consequence {
  margin: 0;
  font-size: 0.92rem;
  line-height: 1.5;
  color: var(--motif-muted, #475569);
}
.motif-confirm__phrase {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  font-size: 0.85rem;
}
.motif-confirm__input {
  font: inherit;
  padding: 0.5rem 0.75rem;
  min-height: 44px;
  border-radius: 0.5rem;
  border: 1px solid var(--motif-border, #cbd5e1);
}
.motif-confirm__input:focus-visible {
  outline: 2px solid var(--motif-focus, #1d4ed8);
  outline-offset: 2px;
}
.motif-confirm__actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.625rem;
  margin-top: 0.5rem;
}
.motif-confirm__btn {
  font: inherit;
  font-size: 0.9rem;
  padding: 0.55rem 1.1rem;
  min-height: 44px;
  border-radius: 0.5rem;
  cursor: pointer;
  border: 1px solid var(--motif-border, #cbd5e1);
  background: var(--motif-surface, #fff);
}
.motif-confirm__btn.is-danger {
  background: var(--motif-danger, #dc2626);
  border-color: var(--motif-danger, #dc2626);
  color: #fff;
}
.motif-confirm__btn.is-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.motif-confirm__btn:focus-visible {
  outline: 2px solid var(--motif-focus, #1d4ed8);
  outline-offset: 2px;
}

.motif-confirm[open] {
  animation: motif-confirm-in 150ms ease-out;
}
.motif-confirm[open]::backdrop {
  animation: motif-confirm-fade 150ms ease-out;
}
@keyframes motif-confirm-in {
  from { opacity: 0; transform: translateY(-6px) scale(0.98); }
  to { opacity: 1; transform: none; }
}
@keyframes motif-confirm-fade {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .motif-confirm[open],
  .motif-confirm[open]::backdrop {
    animation: none !important;
  }
}
</style>
