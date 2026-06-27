# Shared-Element Navigation, browser-native

Animates a navigation (list item → detail view) so a shared element, a thumbnail or
title, appears to morph from one screen to the next, using the native **View Transitions
API** (`document.startViewTransition`). No library.

File: [`view-transition-nav.js`](./view-transition-nav.js).

## Usage

```html
<style>
  /* Match an outgoing and incoming element by the same view-transition-name. */
  .card[data-shared] { view-transition-name: var(--vt, none); }
</style>

<script type="module">
  import { enhanceSharedList } from "./view-transition-nav.js";

  enhanceSharedList({
    listRoot: document.querySelector("#cards"),
    itemSelector: ".card",
    focusSelector: "#detail h1",
    render: (item) => {
      // Build the detail view and tag its hero element with the shared name.
      const hero = document.querySelector("#detail .hero");
      hero.style.viewTransitionName = "motif-shared";
      showDetail(item.dataset.id);
    },
  });
</script>
```

Or call the core directly:

```js
import { navigateWithSharedElement } from "./view-transition-nav.js";

await navigateWithSharedElement({
  updateDOM: () => renderDetail(id), // your DOM mutation (sync or async)
  fromElement: clickedThumbnail,     // outgoing element to pair
  transitionName: "motif-shared",
  focusTarget: "#detail h1",
});
```

## Algorithm

1. **Capability + preference check.** If `document.startViewTransition` is missing **or**
   `prefers-reduced-motion: reduce` is set, `updateDOM()` runs **instantly** and focus
   moves to the new view, no animation at all. Content is always correct.
2. **Enhanced path.** The outgoing element gets `view-transition-name = transitionName`,
   then the DOM mutation runs inside `document.startViewTransition`. The browser snapshots
   the before/after states and morphs the matching named pair (cross-fade + transform).
3. **Name hygiene.** Once `transition.ready` settles, the outgoing element's name is
   restored to its previous value, because `view-transition-name` must be unique at any
   instant, this frees it for the next navigation.
4. **Focus.** After `transition.finished`, focus moves to the new view's heading
   (`focusTarget`), making the heading focusable (`tabindex="-1"`) if needed so keyboard
   and screen-reader users land in the new context.

`enhanceSharedList` is optional sugar: it delegates clicks, ignores modifier/middle
clicks (so "open in new tab" still works), finds `[data-shared]` inside the item, and
calls the core.

## Accessibility

- The morph is **pure enhancement**; the DOM is updated correctly on every path.
- Focus is deliberately moved to the new heading after navigation so keyboard users are
  not stranded on a control that no longer exists.
- Modifier/middle clicks are left to the browser's native behaviour.

## Reduced-motion behaviour

`prefers-reduced-motion: reduce` forces the **instant** path: the DOM updates with no
view transition and no morph. (You can additionally scope `::view-transition-*`
animations off in CSS, but the JS already short-circuits before starting one.)

## Browser support

`document.startViewTransition` (same-document view transitions): Chrome/Edge 111+ and
other Chromium browsers, with rollout in Safari/Firefox. Everywhere else the code
automatically takes the instant fallback, so it is safe to ship today.

## Provenance: original (clean-room).
