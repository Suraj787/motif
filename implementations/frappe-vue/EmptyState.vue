<script setup>
/* ============================================================================
 * Motif Recipe, Empty State (Frappe-Vue)
 * ----------------------------------------------------------------------------
 * A calm, guiding empty state for a list/report/section that has no rows yet.
 * It distinguishes "nothing here yet" (offer a clear primary action) from "no
 * search results" (offer to clear filters), and never blames the user.
 *
 * Presentational only: it emits `primary` / `secondary` and renders the labels
 * it is given, so it works both inside a frappe-ui SPA (parent calls a resource)
 * and in classic Desk (mounted into a list view). No Frappe dependency bundled;
 * pass frappe._('…') strings in from the parent. See empty-state.md.
 *
 * Accessibility: the block is a labelled region; the icon is decorative; the
 * primary action is a real button that receives focus on mount only when the
 * caller opts in (so it never yanks focus unexpectedly).
 *
 * Reduced motion: a gentle fade/raise on appear, removed under
 * prefers-reduced-motion (scoped @media guard); content is otherwise static.
 * Provenance: original (clean-room).
 * ========================================================================== */
import { computed, onMounted, ref } from "vue";

const props = defineProps({
  /** 'empty' (no data yet) or 'no-results' (filters returned nothing). */
  variant: {
    type: String,
    default: "empty",
    validator: (v) => ["empty", "no-results"].includes(v),
  },
  title: { type: String, default: "" },
  /** Supportive, blame-free description. */
  description: { type: String, default: "" },
  /** Primary action label, e.g. frappe._('New Customer'). Omit to hide. */
  primaryLabel: { type: String, default: "" },
  /** Secondary action label, e.g. 'Import' or 'Clear filters'. Omit to hide. */
  secondaryLabel: { type: String, default: "" },
  /** Focus the primary action when the state appears (off by default). */
  autofocusPrimary: { type: Boolean, default: false },
});

const emit = defineEmits(["primary", "secondary"]);

const primaryRef = ref(null);

const resolvedTitle = computed(
  () =>
    props.title ||
    (props.variant === "no-results" ? "No matches" : "Nothing here yet")
);
const resolvedDescription = computed(
  () =>
    props.description ||
    (props.variant === "no-results"
      ? "Try a different search or clear your filters to see everything."
      : "When you add your first item, it will show up here.")
);

onMounted(() => {
  if (props.autofocusPrimary) primaryRef.value?.focus();
});
</script>

<template>
  <section
    class="motif-empty"
    :data-variant="variant"
    role="region"
    :aria-label="resolvedTitle"
  >
    <!-- Decorative glyph; meaning lives in the text below. -->
    <span class="motif-empty__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="28" height="28" fill="none"
           stroke="currentColor" stroke-width="1.5"
           stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="5" width="18" height="14" rx="2" />
        <path d="M3 9h18" />
        <path v-if="variant === 'no-results'" d="M9 14l6-3" />
      </svg>
    </span>

    <h3 class="motif-empty__title">{{ resolvedTitle }}</h3>
    <p class="motif-empty__desc">{{ resolvedDescription }}</p>

    <div v-if="primaryLabel || secondaryLabel" class="motif-empty__actions">
      <button
        v-if="primaryLabel"
        ref="primaryRef"
        type="button"
        class="motif-empty__btn is-primary"
        @click="emit('primary')"
      >
        {{ primaryLabel }}
      </button>
      <button
        v-if="secondaryLabel"
        type="button"
        class="motif-empty__btn is-secondary"
        @click="emit('secondary')"
      >
        {{ secondaryLabel }}
      </button>
    </div>

    <!-- Slot for anything bespoke (e.g. a help link). -->
    <slot />
  </section>
</template>

<style scoped>
.motif-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.5rem;
  padding: 2.5rem 1.5rem;
  max-width: 30rem;
  margin-inline: auto;
  color: var(--motif-fg, #0f172a);
  animation: motif-empty-in 240ms ease-out both;
}
.motif-empty__icon {
  display: grid;
  place-items: center;
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  background: var(--motif-subtle, #f1f5f9);
  color: var(--motif-muted, #64748b);
  margin-bottom: 0.25rem;
}
.motif-empty__title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 600;
}
.motif-empty__desc {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--motif-muted, #475569);
}
.motif-empty__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
  justify-content: center;
  margin-top: 0.75rem;
}
.motif-empty__btn {
  font: inherit;
  font-size: 0.9rem;
  padding: 0.55rem 1rem;
  min-height: 44px; /* coarse-pointer friendly */
  border-radius: 0.5rem;
  cursor: pointer;
  border: 1px solid var(--motif-border, #cbd5e1);
  background: var(--motif-surface, #fff);
}
.motif-empty__btn.is-primary {
  background: var(--motif-accent, #2563eb);
  border-color: var(--motif-accent, #2563eb);
  color: #fff;
}
.motif-empty__btn:focus-visible {
  outline: 2px solid var(--motif-focus, #1d4ed8);
  outline-offset: 2px;
}

@keyframes motif-empty-in {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: none; }
}

@media (prefers-reduced-motion: reduce) {
  .motif-empty {
    animation: none !important;
  }
}
</style>
