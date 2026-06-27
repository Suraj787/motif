<script setup>
/* ============================================================================
 * Motif Recipe, Streaming List (Vue 3, <script setup>)
 * ----------------------------------------------------------------------------
 * Renders items as they stream in (e.g. from a generator / SSE / async source),
 * shows a quiet skeleton while waiting for the first batch, and exposes a STOP
 * control so the user can halt an in-progress stream at any time.
 *
 * Announcements are THROTTLED: a naive aria-live region that fires on every
 * appended token/row floods a screen reader. Instead we batch arrivals and
 * announce a periodic summary ("12 results so far") on a polite live region.
 *
 * The data source is injected as an async-iterable factory (`source` prop), so
 * the component is transport-agnostic and testable with a plain async generator.
 *
 * Reduced motion:
 *   - New rows use a transform/opacity enter transition that collapses to an
 *     instant insert under prefers-reduced-motion; the skeleton shimmer is also
 *     disabled (scoped @media guard).
 * Provenance: original (clean-room).
 * ========================================================================== */
import { ref, computed, onUnmounted } from "vue";

const props = defineProps({
  /** () => AsyncIterable<any> | AsyncIterator<any>. Called on start(). */
  source: { type: Function, required: true },
  /** Field name (or function) to render per item. */
  labelKey: { type: [String, Function], default: null },
  /** Skeleton rows shown before the first item arrives. */
  skeletonRows: { type: Number, default: 5 },
  /** Minimum ms between live-region announcements (throttle window). */
  announceEvery: { type: Number, default: 1500 },
  /** Auto-start on mount. */
  autostart: { type: Boolean, default: true },
});

const emit = defineEmits(["start", "item", "stop", "done", "error"]);

const items = ref([]);
const status = ref("idle"); // 'idle' | 'loading' | 'streaming' | 'done' | 'stopped' | 'error'
const liveMessage = ref("");

let abort = false;
let iterator = null;
let announceTimer = null;
let pendingAnnounce = false;

const isActive = computed(() => status.value === "loading" || status.value === "streaming");
const showSkeleton = computed(() => status.value === "loading" && items.value.length === 0);

function labelOf(item) {
  if (typeof props.labelKey === "function") return props.labelKey(item);
  if (props.labelKey) return item?.[props.labelKey];
  return typeof item === "string" ? item : JSON.stringify(item);
}

/* ---- throttled announcer ------------------------------------------------- */
function scheduleAnnounce() {
  pendingAnnounce = true;
  if (announceTimer) return; // already within a throttle window
  flushAnnounce();
  announceTimer = setInterval(() => {
    if (pendingAnnounce) flushAnnounce();
    else {
      clearInterval(announceTimer);
      announceTimer = null;
    }
  }, props.announceEvery);
}
function flushAnnounce() {
  pendingAnnounce = false;
  liveMessage.value = `${items.value.length} ${items.value.length === 1 ? "result" : "results"} so far`;
}
function clearAnnounce() {
  if (announceTimer) {
    clearInterval(announceTimer);
    announceTimer = null;
  }
}

/* ---- stream lifecycle ---------------------------------------------------- */
async function start() {
  if (isActive.value) return;
  abort = false;
  items.value = [];
  status.value = "loading";
  liveMessage.value = "Loading…";
  emit("start");

  try {
    const src = props.source();
    iterator = src[Symbol.asyncIterator] ? src[Symbol.asyncIterator]() : src;

    let first = true;
    while (true) {
      if (abort) break;
      const { value, done } = await iterator.next();
      if (done) break;
      if (first) {
        status.value = "streaming";
        first = false;
      }
      items.value = [...items.value, value];
      emit("item", value);
      scheduleAnnounce();
    }

    if (abort) {
      status.value = "stopped";
      liveMessage.value = `Stopped, ${items.value.length} results`;
      emit("stop", items.value.length);
    } else {
      status.value = "done";
      liveMessage.value = `Done, ${items.value.length} ${items.value.length === 1 ? "result" : "results"}`;
      emit("done", items.value.length);
    }
  } catch (err) {
    status.value = "error";
    liveMessage.value = "Something went wrong loading results";
    emit("error", err);
  } finally {
    clearAnnounce();
  }
}

/** Halt the stream. Politely asks the iterator to clean up via .return(). */
function stop() {
  if (!isActive.value) return;
  abort = true;
  iterator?.return?.(); // let generators run their finally blocks
}

if (props.autostart) start();
defineExpose({ start, stop });

onUnmounted(() => {
  abort = true;
  iterator?.return?.();
  clearAnnounce();
});
</script>

<template>
  <section class="motif-stream" :data-status="status">
    <header class="motif-stream__bar">
      <p class="motif-stream__count">
        <span v-if="isActive" class="motif-stream__pip" aria-hidden="true"></span>
        {{ items.length }} {{ items.length === 1 ? "result" : "results" }}
        <span v-if="status === 'streaming' || status === 'loading'"> · streaming…</span>
      </p>

      <button
        v-if="isActive"
        type="button"
        class="motif-stream__stop"
        @click="stop"
      >
        Stop
      </button>
      <button
        v-else-if="status === 'stopped' || status === 'done' || status === 'error'"
        type="button"
        class="motif-stream__stop"
        @click="start"
      >
        Restart
      </button>
    </header>

    <!-- Skeleton placeholder for the very first batch only. -->
    <ul v-if="showSkeleton" class="motif-stream__list" aria-hidden="true">
      <li v-for="n in skeletonRows" :key="`sk-${n}`" class="motif-skel">
        <span class="motif-skel__line" />
      </li>
    </ul>

    <!-- Live results. -->
    <TransitionGroup
      v-else
      tag="ul"
      name="motif-row"
      class="motif-stream__list"
    >
      <li v-for="(item, i) in items" :key="i" class="motif-stream__item">
        {{ labelOf(item) }}
      </li>
    </TransitionGroup>

    <!-- Throttled polite announcer. Visually hidden; do not steal focus. -->
    <p class="motif-sr-only" role="status" aria-live="polite">{{ liveMessage }}</p>
  </section>
</template>

<style scoped>
.motif-stream {
  max-width: 36rem;
}
.motif-stream__bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.5rem;
}
.motif-stream__count {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--motif-muted, #475569);
}
.motif-stream__pip {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: var(--motif-accent, #2563eb);
  animation: motif-pulse 1.1s ease-in-out infinite;
}
.motif-stream__stop {
  font: inherit;
  font-size: 0.85rem;
  padding: 0.4rem 0.8rem;
  min-height: 44px;
  border-radius: 0.5rem;
  border: 1px solid var(--motif-border, #cbd5e1);
  background: var(--motif-surface, #fff);
  cursor: pointer;
}
.motif-stream__stop:focus-visible {
  outline: 2px solid var(--motif-focus, #1d4ed8);
  outline-offset: 2px;
}

.motif-stream__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}
.motif-stream__item {
  padding: 0.625rem 0.75rem;
  border-radius: 0.5rem;
  background: var(--motif-surface, #fff);
  border: 1px solid var(--motif-border, #e2e8f0);
}

/* Skeleton. */
.motif-skel {
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid var(--motif-border, #e2e8f0);
}
.motif-skel__line {
  display: block;
  height: 0.85rem;
  border-radius: 0.25rem;
  background: linear-gradient(
    90deg,
    var(--motif-skel-base, #e2e8f0) 25%,
    var(--motif-skel-hi, #f1f5f9) 37%,
    var(--motif-skel-base, #e2e8f0) 63%
  );
  background-size: 400% 100%;
  animation: motif-shimmer 1.4s ease-in-out infinite;
}

@keyframes motif-shimmer {
  from { background-position: 100% 0; }
  to { background-position: 0 0; }
}
@keyframes motif-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.6); opacity: 0.5; }
}

/* New-row enter: transform + opacity. */
.motif-row-enter-active {
  transition: opacity 180ms ease, transform 180ms ease;
}
.motif-row-enter-from {
  opacity: 0;
  transform: translateY(4px);
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
  .motif-skel__line,
  .motif-stream__pip {
    animation: none !important;
  }
  .motif-skel__line {
    background: var(--motif-skel-base, #e2e8f0);
  }
  .motif-row-enter-active {
    transition: none !important;
  }
  .motif-row-enter-from {
    transform: none !important;
  }
}
</style>
