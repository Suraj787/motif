# Drag Reorder, Svelte

A reorderable list with calm drag feedback **and** a full keyboard alternative, because
drag-and-drop alone is inaccessible. Pointer users drag (native HTML5 DnD); keyboard
users grab an item with Space/Enter and move it with Arrow keys. Every move is announced
on a polite live region.

File: [`DragReorder.svelte`](./DragReorder.svelte).

## Usage

```svelte
<script>
  import DragReorder from "./DragReorder.svelte";
  let tasks = [
    { id: 1, label: "Draft proposal" },
    { id: 2, label: "Review budget" },
    { id: 3, label: "Send invoice" },
  ];
  function save(e) { tasks = e.detail.items; /* persist new order */ }
</script>

<DragReorder items={tasks} label="Tasks" on:reorder={save} />
```

`items` is `[{ id, label }]`; the new order is emitted via `reorder` (`e.detail.items`),
so the parent owns persistence. State updates are immutable (`slice`/`splice` into a new
array).

## Algorithm

**Pointer drag** uses the native Drag and Drop API: `dragstart` records the source index
(and sets `text/plain` for Firefox), `dragover` `preventDefault`s to allow dropping and
marks the hovered target, and `drop` moves the item from source to target index.

**Keyboard reorder** (the accessible alternative):

1. Focus a row (rows are `tabindex="0"`, `role="button"`).
2. **Space/Enter** grabs the item (announced: "… grabbed. Use arrow keys to move, space to
   drop."). Pressing it again drops.
3. **Arrow Up/Left** and **Down/Right** move the grabbed item one slot; the array updates,
   `reorder` emits, and focus follows the item (`requestAnimationFrame` → focus). When
   nothing is grabbed, arrows simply rove focus between rows.
4. **Escape** cancels the in-progress move.

## Accessibility

- Each row is operable by keyboard (`role="button"`, `aria-roledescription="sortable
  item"`, `aria-grabbed`) with a label that states its position ("Position 2 of 3").
- A **polite** `role="status"` live region announces grabs, moves ("… moved to position 3
  of 5"), drops, and cancels, without stealing focus.
- The drag handle glyph is `aria-hidden`; the item label carries the meaning.
- Focus rings are always visible; targets are 44px for coarse pointers.
- Feedback is conveyed structurally (outline, insertion line) plus the live region, not
  by motion or colour alone.

## Reduced-motion behaviour

The item `transition` and the grabbed `scale` are removed under `@media
(prefers-reduced-motion: reduce)`; reordering still works, just without easing or scaling.

## Responsive behaviour

Fluid up to `28rem`; rows are full-width and stack. No fixed pixel motion.

## Browser support

All modern browsers. Native HTML5 DnD for pointer; the keyboard path needs no DnD support
at all, so touch/keyboard-only users are fully covered.

## Provenance: original (clean-room).
