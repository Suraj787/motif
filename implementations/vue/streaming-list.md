# Streaming List, Vue 3

Renders items as they stream in (async generator, SSE, fetch stream), shows a quiet
skeleton while waiting for the first batch, and gives the user a **Stop** control to halt
an in-progress stream at any moment. Live-region announcements are **throttled** so a
screen reader is not flooded as rows arrive.

File: [`StreamingList.vue`](./StreamingList.vue).

## Usage

```vue
<script setup>
import StreamingList from "./StreamingList.vue";

// Any async iterable works. A generator makes Stop clean (its finally runs).
async function* search() {
  for (let i = 1; i <= 200; i++) {
    await new Promise((r) => setTimeout(r, 80));
    yield { title: `Result ${i}` };
  }
}
</script>

<template>
  <StreamingList :source="search" label-key="title" :skeleton-rows="6" />
</template>
```

`source` is a factory returning an async iterable/iterator (called on each `start()`).
`labelKey` is a field name or a function. The component exposes `start()` and `stop()`.

## Algorithm

1. **First batch:** status is `loading`; a shimmer skeleton of `skeletonRows` rows is
   shown (`aria-hidden`) and the live region says "Loading…".
2. **Streaming:** the component pulls from the iterator in a `while` loop, appending each
   value and emitting `item`. On the first value it switches to `streaming` and the
   skeleton is replaced by the real list.
3. **Throttled announcements:** instead of announcing every row, arrivals set a "pending"
   flag and a single `setInterval` (every `announceEvery`, default 1.5s) flushes a
   summary, "12 results so far", to the polite live region. The interval stops itself
   once no new rows are pending.
4. **Stop:** sets an `abort` flag and calls `iterator.return?.()` so an async generator
   runs its `finally` (closing sockets etc.). Status becomes `stopped`; a **Restart**
   button appears.
5. **Done / error:** the loop ends naturally (`done`) or catches an error, each with its
   own final announcement. `onUnmounted` aborts and clears timers.

## Accessibility

- A single **polite** `role="status"` live region carries throttled summaries, so screen
  readers get useful progress without per-row spam.
- The skeleton is `aria-hidden` (decorative); only real results are exposed.
- Stop/Restart are real buttons, keyboard reachable, 44px tall, with a visible focus
  ring. **Focus is never moved** as rows arrive, the user keeps their place.
- Counts and status are also shown visibly with text ("· streaming…"), not motion alone.

## Reduced-motion behaviour

Under `@media (prefers-reduced-motion: reduce)` the skeleton shimmer and the activity pip
animation stop (the skeleton becomes a flat block) and new rows insert instantly with no
slide.

## Responsive behaviour

Fluid up to a readable `36rem` max width; rows wrap naturally. No fixed pixel motion.

## Browser support

All modern browsers. Relies only on async iterators, `<TransitionGroup>`, and standard
ARIA.

## Provenance: original (clean-room).
