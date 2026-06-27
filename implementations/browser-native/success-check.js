/* ============================================================================
 * Motif Recipe, Success Check (browser-native, dependency-free)
 * ----------------------------------------------------------------------------
 * A short, dignified success confirmation: a checkmark draws in (SVG stroke) and
 * a brief message appears, then it quietly settles. No confetti, no bounce, no
 * sound. The outcome is announced to assistive tech via role="status".
 *
 * It builds its own small DOM so it is drop-in:
 *   const ok = createSuccessCheck();
 *   ok.show('Saved');            // draws the check, announces "Saved"
 *
 * The check animation is a stroke-dashoffset draw (transform/opacity friendly,
 * compositor-cheap). Under prefers-reduced-motion the check is shown already
 * complete (no draw) and the message simply appears, the CSS owns this via a
 * media query, and JS also skips the draw class.
 * Provenance: original (clean-room).
 * ========================================================================== */

/**
 * Create a reusable success-check element.
 * @param {Object} [opts]
 * @param {HTMLElement} [opts.mount=document.body] where to append the element.
 * @param {number} [opts.lingerMs=1800] how long the confirmation stays before auto-hide (0 = stay).
 * @returns {{ el: HTMLElement, show: (msg?: string) => void, hide: () => void, dispose: () => void }}
 */
export function createSuccessCheck({ mount, lingerMs = 1800 } = {}) {
  if (typeof document === "undefined") {
    return { el: null, show() {}, hide() {}, dispose() {} };
  }
  const host = mount || document.body;

  const el = document.createElement("div");
  el.className = "motif-success";
  el.hidden = true;
  // role="status" → polite announcement of the message text on show.
  el.setAttribute("role", "status");
  el.setAttribute("aria-live", "polite");
  el.innerHTML = `
    <span class="motif-success__mark" aria-hidden="true">
      <svg viewBox="0 0 52 52" width="40" height="40">
        <circle class="motif-success__ring" cx="26" cy="26" r="24" fill="none" stroke-width="3" />
        <path class="motif-success__tick" fill="none" stroke-width="4"
              stroke-linecap="round" stroke-linejoin="round"
              d="M14 27 l8 8 l16 -18" />
      </svg>
    </span>
    <span class="motif-success__msg"></span>`;
  host.appendChild(el);

  const msgEl = el.querySelector(".motif-success__msg");
  let hideTimer = null;

  const prefersReduced = () =>
    typeof window !== "undefined" &&
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function show(message = "Success") {
    if (hideTimer) {
      clearTimeout(hideTimer);
      hideTimer = null;
    }
    msgEl.textContent = message;
    el.hidden = false;

    // Restart the draw animation: toggle a class on the next frame so the
    // keyframes replay even if show() is called repeatedly. Skipped entirely
    // under reduced motion (CSS shows the tick already complete).
    el.classList.remove("is-animating");
    if (!prefersReduced()) {
      // Force reflow so removing/adding the class re-triggers the animation.
      void el.offsetWidth;
      el.classList.add("is-animating");
    }

    if (lingerMs > 0) {
      hideTimer = setTimeout(hide, lingerMs);
    }
  }

  function hide() {
    el.hidden = true;
    el.classList.remove("is-animating");
    if (hideTimer) {
      clearTimeout(hideTimer);
      hideTimer = null;
    }
  }

  function dispose() {
    hide();
    el.remove();
  }

  return { el, show, hide, dispose };
}

export default createSuccessCheck;
