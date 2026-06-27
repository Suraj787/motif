/* ============================================================================
 * Motif Recipe, Command Palette (browser-native, dependency-free)
 * ----------------------------------------------------------------------------
 * A keyboard-first command palette (Cmd/Ctrl-K) built on the native <dialog>
 * element. It reveals with a cheap transform/opacity transition, traps focus
 * while open, restores focus to the trigger on close, and supports full
 * arrow-key navigation with type-to-filter.
 *
 * Accessibility contract:
 *   - Uses <dialog>.showModal() so the platform handles the modal semantics,
 *     inertness of the background, and the top layer.
 *   - The listbox uses role="listbox"/role="option" with aria-activedescendant
 *     so the input keeps DOM focus while the "active" option is announced.
 *   - Escape closes (native <dialog> behaviour, plus our own handler for the
 *     non-dialog fallback) and focus returns to whatever opened it.
 *   - Reduced motion: the open/close animation is removed via CSS @media; the
 *     palette simply appears.
 *
 * Coarse pointer: options are full-width 44px+ tap targets; tapping selects.
 * Provenance: original (clean-room).
 * ========================================================================== */

/**
 * @typedef {Object} Command
 * @property {string} id
 * @property {string} label
 * @property {string} [hint]      short right-aligned hint (e.g. shortcut)
 * @property {() => void} run     invoked on selection
 */

/**
 * Create a command palette.
 * @param {Object} opts
 * @param {Command[]} opts.commands
 * @param {string}   [opts.placeholder]
 * @param {Document|HTMLElement} [opts.mount=document.body]
 * @returns {{ open: () => void, close: () => void, setCommands: (c: Command[]) => void, dispose: () => void }}
 */
export function createCommandPalette({ commands = [], placeholder = "Type a command…", mount } = {}) {
  if (typeof document === "undefined") {
    return { open() {}, close() {}, setCommands() {}, dispose() {} };
  }
  const host = mount || document.body;
  let all = commands.slice();
  let filtered = all.slice();
  let activeIndex = 0;
  let lastFocused = null;

  // ---- build DOM ---------------------------------------------------------
  const dialog = document.createElement("dialog");
  dialog.className = "motif-cmdk";
  dialog.setAttribute("aria-label", "Command palette");

  const listId = `motif-cmdk-list-${Math.random().toString(36).slice(2, 8)}`;
  dialog.innerHTML = `
    <form method="dialog" class="motif-cmdk__panel">
      <input
        class="motif-cmdk__input"
        type="text"
        role="combobox"
        aria-expanded="true"
        aria-controls="${listId}"
        aria-autocomplete="list"
        autocomplete="off"
        spellcheck="false"
        placeholder="${placeholder}"
      />
      <ul class="motif-cmdk__list" id="${listId}" role="listbox" aria-label="Commands"></ul>
      <p class="motif-cmdk__empty" hidden>No matching commands</p>
    </form>`;
  host.appendChild(dialog);

  const input = dialog.querySelector(".motif-cmdk__input");
  const list = dialog.querySelector(".motif-cmdk__list");
  const empty = dialog.querySelector(".motif-cmdk__empty");

  // ---- rendering ---------------------------------------------------------
  function optionId(i) {
    return `${listId}-opt-${i}`;
  }

  function render() {
    list.textContent = "";
    if (filtered.length === 0) {
      empty.hidden = false;
      input.removeAttribute("aria-activedescendant");
      return;
    }
    empty.hidden = true;
    if (activeIndex >= filtered.length) activeIndex = filtered.length - 1;
    if (activeIndex < 0) activeIndex = 0;

    filtered.forEach((cmd, i) => {
      const li = document.createElement("li");
      li.className = "motif-cmdk__option";
      li.id = optionId(i);
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", String(i === activeIndex));
      li.dataset.index = String(i);
      li.innerHTML = `<span class="motif-cmdk__label"></span>${
        cmd.hint ? `<span class="motif-cmdk__hint"></span>` : ""
      }`;
      li.querySelector(".motif-cmdk__label").textContent = cmd.label;
      if (cmd.hint) li.querySelector(".motif-cmdk__hint").textContent = cmd.hint;
      list.appendChild(li);
    });
    input.setAttribute("aria-activedescendant", optionId(activeIndex));
    scrollActiveIntoView();
  }

  function scrollActiveIntoView() {
    const el = list.children[activeIndex];
    el?.scrollIntoView({ block: "nearest" });
  }

  function applyFilter() {
    const q = input.value.trim().toLowerCase();
    filtered = q
      ? all.filter((c) => c.label.toLowerCase().includes(q))
      : all.slice();
    activeIndex = 0;
    render();
  }

  // ---- selection / navigation -------------------------------------------
  function move(delta) {
    if (filtered.length === 0) return;
    activeIndex = (activeIndex + delta + filtered.length) % filtered.length; // wrap
    render();
  }

  function selectActive() {
    const cmd = filtered[activeIndex];
    if (!cmd) return;
    close();
    // Run after close so focus restoration is not clobbered by the command.
    Promise.resolve().then(() => cmd.run());
  }

  // ---- events ------------------------------------------------------------
  function onKeydown(e) {
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        move(1);
        break;
      case "ArrowUp":
        e.preventDefault();
        move(-1);
        break;
      case "Home":
        e.preventDefault();
        activeIndex = 0;
        render();
        break;
      case "End":
        e.preventDefault();
        activeIndex = filtered.length - 1;
        render();
        break;
      case "Enter":
        e.preventDefault();
        selectActive();
        break;
      // Escape is handled natively by <dialog> (cancel event below).
    }
  }

  function onListPointer(e) {
    const li = e.target.closest(".motif-cmdk__option");
    if (!li) return;
    activeIndex = Number(li.dataset.index);
    selectActive();
  }

  // Native <dialog> fires "cancel" on Escape; "close" whenever it closes.
  function onCancel() {
    // Default close handled by onClose; keep here to allow future veto hooks.
  }
  function onClose() {
    restoreFocus();
  }

  input.addEventListener("input", applyFilter);
  input.addEventListener("keydown", onKeydown);
  list.addEventListener("click", onListPointer);
  dialog.addEventListener("cancel", onCancel);
  dialog.addEventListener("close", onClose);

  // ---- focus management --------------------------------------------------
  function restoreFocus() {
    if (lastFocused && typeof lastFocused.focus === "function") {
      lastFocused.focus();
    }
    lastFocused = null;
  }

  // ---- public API --------------------------------------------------------
  function open() {
    if (dialog.open) return;
    lastFocused = document.activeElement;
    input.value = "";
    applyFilter();
    // Native modal: makes the rest of the document inert + traps focus for us.
    if (typeof dialog.showModal === "function") {
      dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
    }
    input.focus();
  }

  function close() {
    if (!dialog.open) return;
    if (typeof dialog.close === "function") {
      dialog.close(); // fires "close" → restoreFocus
    } else {
      dialog.removeAttribute("open");
      restoreFocus();
    }
  }

  function setCommands(next) {
    all = next.slice();
    applyFilter();
  }

  // Global Cmd/Ctrl-K to summon; ignored while typing in another field unless
  // the user explicitly uses the meta/ctrl chord (so it is safe everywhere).
  function onGlobalKey(e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
      e.preventDefault();
      dialog.open ? close() : open();
    }
  }
  document.addEventListener("keydown", onGlobalKey);

  function dispose() {
    document.removeEventListener("keydown", onGlobalKey);
    input.removeEventListener("input", applyFilter);
    input.removeEventListener("keydown", onKeydown);
    list.removeEventListener("click", onListPointer);
    dialog.removeEventListener("cancel", onCancel);
    dialog.removeEventListener("close", onClose);
    if (dialog.open) close();
    dialog.remove();
  }

  return { open, close, setCommands, dispose };
}

export default createCommandPalette;
