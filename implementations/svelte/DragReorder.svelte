<script>
  /* ==========================================================================
   * Motif Recipe, Drag Reorder (Svelte, dependency-free)
   * --------------------------------------------------------------------------
   * A reorderable list with calm drag feedback AND a full keyboard alternative,
   * because drag-and-drop alone is inaccessible. Pointer drag uses the native
   * HTML5 Drag and Drop API; keyboard users grab an item with Space/Enter and
   * move it with Arrow keys. Every move is announced on a polite live region.
   *
   * Feedback is restrained: the dragged row dims slightly and the drop target
   * shows a thin insertion line, transform/opacity only, no layout thrash. All
   * motion is removed under prefers-reduced-motion via the scoped <style>.
   *
   * Items are passed in via the `items` prop (array of { id, label }) and the
   * new order is emitted with `reorder`, so the parent owns persistence.
   * Provenance: original (clean-room).
   * ======================================================================== */
  import { createEventDispatcher } from "svelte";

  export let items = []; // [{ id, label }]
  export let label = "Reorderable list";

  const dispatch = createEventDispatcher();

  let dragIndex = -1; // index being dragged (pointer)
  let overIndex = -1; // current drop-target index (pointer)
  let grabbedIndex = -1; // index "picked up" via keyboard
  let liveMessage = "";

  function announce(msg) {
    liveMessage = msg;
  }

  /** Move item from `from` to `to`, returning a new array (immutable update). */
  function moveItem(from, to) {
    if (from === to || from < 0 || to < 0 || to >= items.length) return items;
    const next = items.slice();
    const [moved] = next.splice(from, 1);
    next.splice(to, 0, moved);
    return next;
  }

  function commit(next, movedLabel, position) {
    items = next;
    dispatch("reorder", { items: next });
    announce(`${movedLabel} moved to position ${position} of ${next.length}`);
  }

  /* ---- pointer drag ------------------------------------------------------ */
  function onDragStart(e, i) {
    dragIndex = i;
    e.dataTransfer.effectAllowed = "move";
    // Required for Firefox to initiate a drag.
    e.dataTransfer.setData("text/plain", String(i));
  }
  function onDragOver(e, i) {
    e.preventDefault(); // allow drop
    e.dataTransfer.dropEffect = "move";
    overIndex = i;
  }
  function onDrop(e, i) {
    e.preventDefault();
    if (dragIndex !== -1 && dragIndex !== i) {
      const movedLabel = items[dragIndex].label;
      commit(moveItem(dragIndex, i), movedLabel, i + 1);
    }
    dragIndex = -1;
    overIndex = -1;
  }
  function onDragEnd() {
    dragIndex = -1;
    overIndex = -1;
  }

  /* ---- keyboard reorder -------------------------------------------------- */
  function onKeydown(e, i) {
    const key = e.key;

    // Toggle "grab" with Space or Enter.
    if (key === " " || key === "Enter") {
      e.preventDefault();
      if (grabbedIndex === i) {
        grabbedIndex = -1;
        announce(`${items[i].label} dropped at position ${i + 1}`);
      } else {
        grabbedIndex = i;
        announce(`${items[i].label} grabbed. Use arrow keys to move, space to drop.`);
      }
      return;
    }

    if (key === "Escape" && grabbedIndex !== -1) {
      e.preventDefault();
      announce(`Move cancelled`);
      grabbedIndex = -1;
      return;
    }

    // Arrow keys: if grabbed, move the item; otherwise just roving focus.
    const isUp = key === "ArrowUp" || key === "ArrowLeft";
    const isDown = key === "ArrowDown" || key === "ArrowRight";
    if (!isUp && !isDown) return;
    e.preventDefault();

    if (grabbedIndex === i) {
      const to = isUp ? i - 1 : i + 1;
      if (to < 0 || to >= items.length) return;
      const movedLabel = items[i].label;
      commit(moveItem(i, to), movedLabel, to + 1);
      grabbedIndex = to;
      // Keep focus on the moved item after the DOM updates.
      requestAnimationFrame(() => focusRow(to));
    } else {
      const to = isUp ? i - 1 : i + 1;
      if (to >= 0 && to < items.length) focusRow(to);
    }
  }

  function focusRow(i) {
    const el = document.querySelector(`[data-motif-row="${i}"]`);
    el?.focus();
  }
</script>

<ul class="motif-dnd" role="list" aria-label={label}>
  {#each items as item, i (item.id)}
    <li
      class="motif-dnd__item"
      class:is-dragging={dragIndex === i}
      class:is-grabbed={grabbedIndex === i}
      class:is-over={overIndex === i && dragIndex !== i}
      data-motif-row={i}
      tabindex="0"
      role="button"
      aria-roledescription="sortable item"
      aria-grabbed={grabbedIndex === i}
      aria-label={`${item.label}. Position ${i + 1} of ${items.length}. Press space to reorder.`}
      draggable="true"
      on:dragstart={(e) => onDragStart(e, i)}
      on:dragover={(e) => onDragOver(e, i)}
      on:drop={(e) => onDrop(e, i)}
      on:dragend={onDragEnd}
      on:keydown={(e) => onKeydown(e, i)}
    >
      <span class="motif-dnd__handle" aria-hidden="true">⋮⋮</span>
      <span class="motif-dnd__label">{item.label}</span>
    </li>
  {/each}
</ul>

<!-- Polite live region: announces grabs and moves without stealing focus. -->
<p class="motif-sr-only" role="status" aria-live="polite">{liveMessage}</p>

<style>
  .motif-dnd {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
    max-width: 28rem;
  }
  .motif-dnd__item {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    padding: 0.625rem 0.75rem;
    min-height: 44px; /* coarse-pointer target */
    border-radius: 0.5rem;
    border: 1px solid var(--motif-border, #e2e8f0);
    background: var(--motif-surface, #fff);
    cursor: grab;
    user-select: none;
    transition: opacity 150ms ease, transform 150ms ease;
  }
  .motif-dnd__item:focus-visible {
    outline: 2px solid var(--motif-focus, #1d4ed8);
    outline-offset: 2px;
  }
  .motif-dnd__item.is-dragging {
    opacity: 0.5;
    cursor: grabbing;
  }
  .motif-dnd__item.is-grabbed {
    outline: 2px solid var(--motif-accent, #2563eb);
    outline-offset: 2px;
    transform: scale(1.01);
  }
  /* Thin insertion indicator on the drop target. */
  .motif-dnd__item.is-over {
    box-shadow: inset 0 2px 0 0 var(--motif-accent, #2563eb);
  }
  .motif-dnd__handle {
    color: var(--motif-muted, #94a3b8);
    letter-spacing: -2px;
  }
  .motif-dnd__label {
    font-size: 0.92rem;
  }

  .motif-sr-only {
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

  @media (prefers-reduced-motion: reduce) {
    .motif-dnd__item {
      transition: none !important;
    }
    .motif-dnd__item.is-grabbed {
      transform: none !important;
    }
  }
</style>
