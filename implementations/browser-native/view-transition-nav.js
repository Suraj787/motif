/* ============================================================================
 * Motif Recipe, Shared-Element Navigation (browser-native, dependency-free)
 * ----------------------------------------------------------------------------
 * Animates a navigation (e.g. list item → detail view) so a shared element
 * (a thumbnail, a title) appears to morph from one screen to the next, using the
 * native View Transitions API (document.startViewTransition). No library.
 *
 * Strategy:
 *   1. If the View Transitions API is unsupported OR the user prefers reduced
 *      motion, the DOM update is applied INSTANTLY (no animation). The content
 *      is always correct; the morph is pure enhancement.
 *   2. Otherwise we tag the shared element on the outgoing and incoming screens
 *      with a matching `view-transition-name`, then run the update inside
 *      startViewTransition so the browser cross-fades + morphs the pair.
 *
 * The actual DOM mutation is injected via an `updateDOM` callback so this works
 * with any rendering approach (innerHTML swap, framework patch, route render).
 * We never trap or drop focus: after the transition we move focus to the new
 * view's heading so keyboard users land in the right place.
 * Provenance: original (clean-room).
 * ========================================================================== */

/**
 * Run a shared-element navigation.
 *
 * @param {Object} opts
 * @param {() => void | Promise<void>} opts.updateDOM
 *        Mutates the DOM to the next view. Must be synchronous-ish (a Promise is
 *        awaited). It should also assign the shared `view-transition-name` to the
 *        incoming element (see `transitionName`).
 * @param {string} [opts.transitionName="motif-shared"]
 *        The view-transition-name shared by the outgoing & incoming elements.
 * @param {Element|null} [opts.fromElement=null]
 *        Outgoing element to tag (e.g. the clicked card). Tagged before capture,
 *        untagged after, so names never collide across multiple navigations.
 * @param {Element|null} [opts.focusTarget=null]
 *        Element (or selector resolved by caller) to focus after navigation.
 * @returns {Promise<void>} resolves when the navigation (and any animation) ends.
 */
export function navigateWithSharedElement({
  updateDOM,
  transitionName = "motif-shared",
  fromElement = null,
  focusTarget = null,
} = {}) {
  if (typeof document === "undefined") return Promise.resolve();

  const prefersReduced =
    typeof window !== "undefined" &&
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const supported = typeof document.startViewTransition === "function";

  // ---- Fallback path: instant, correct, no animation. --------------------
  if (!supported || prefersReduced) {
    return Promise.resolve(updateDOM()).then(() => {
      moveFocus(focusTarget);
    });
  }

  // ---- Enhanced path: native View Transition. ----------------------------
  // Tag the outgoing element so the browser pairs it with the incoming one.
  const prevName = fromElement ? fromElement.style.viewTransitionName : "";
  if (fromElement) fromElement.style.viewTransitionName = transitionName;

  const transition = document.startViewTransition(async () => {
    await updateDOM();
  });

  // Clean up the outgoing tag once the snapshot is captured, so the name is
  // free for the next navigation (names must be unique at any instant).
  transition.ready
    .catch(() => {})
    .finally(() => {
      if (fromElement) fromElement.style.viewTransitionName = prevName;
    });

  return transition.finished
    .catch(() => {}) // a skipped/failed transition still leaves DOM updated
    .finally(() => {
      moveFocus(focusTarget);
    });
}

/** Move keyboard focus to the new view without scrolling jank. */
function moveFocus(target) {
  if (!target) return;
  const el = typeof target === "string" ? document.querySelector(target) : target;
  if (!el) return;
  // Make headings focusable transiently so SR users land on the new context.
  if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "-1");
  el.focus({ preventScroll: false });
}

/**
 * Convenience helper: enhance a list so clicking an item navigates with a shared
 * element. Purely optional sugar around navigateWithSharedElement.
 *
 * @param {Object} opts
 * @param {Element} opts.listRoot      container delegated for clicks
 * @param {string}  opts.itemSelector  selector for clickable items
 * @param {(item: Element) => void | Promise<void>} opts.render
 *        Renders the detail view for the clicked item (and tags the incoming
 *        shared element with the transition name).
 * @param {string}  [opts.transitionName]
 * @param {string}  [opts.focusSelector] heading to focus after navigation
 * @returns {{ dispose: () => void }}
 */
export function enhanceSharedList({
  listRoot,
  itemSelector,
  render,
  transitionName = "motif-shared",
  focusSelector = null,
}) {
  if (typeof document === "undefined" || !listRoot) {
    return { dispose() {} };
  }
  const onClick = (e) => {
    const item = e.target.closest(itemSelector);
    if (!item || !listRoot.contains(item)) return;
    // Let modifier-clicks / middle-clicks behave normally (open in new tab etc.).
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault();
    const shared = item.querySelector("[data-shared]") || item;
    navigateWithSharedElement({
      updateDOM: () => render(item),
      transitionName,
      fromElement: shared,
      focusTarget: focusSelector,
    });
  };
  listRoot.addEventListener("click", onClick);
  return { dispose: () => listRoot.removeEventListener("click", onClick) };
}

export default navigateWithSharedElement;
