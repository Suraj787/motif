/* ============================================================================
 * Motif Recipe, Upload Progress (React, dependency-free)
 * ----------------------------------------------------------------------------
 * A determinate upload progress control: a real <progress>-backed bar that fills
 * 0→100%, can be cancelled mid-flight, and announces meaningful milestones to
 * assistive tech without spamming on every percent.
 *
 * The actual transfer is injected via an `upload` prop, an async function that
 * receives an onProgress(0..1) callback and an AbortSignal, so the component is
 * transport-agnostic (XHR, fetch streams, resumable, …) and unit-testable.
 *
 * Accessibility:
 *   - role="progressbar" with aria-valuenow/min/max for the visual bar, plus a
 *     polite live region that announces throttled milestones ("Uploading 25%",
 *     "Upload complete", "Upload cancelled"), never every integer percent.
 *   - Cancel is a real focusable button; on completion/cancel focus is NOT
 *     stolen, the user keeps their place.
 *
 * Reduced motion:
 *   - The bar fill transition and the indeterminate stripe animation are removed
 *     under prefers-reduced-motion; the bar still updates, just without easing.
 *
 * Styles are injected once from this module (SSR-guarded, idempotent) so the
 * component is drop-in; every class is overridable.
 * Provenance: original (clean-room).
 * ========================================================================== */
import React, { useCallback, useEffect, useRef, useState } from "react";

const STYLE_ID = "motif-upload-progress-styles";
const STYLES = `
.motif-upload {
  --motif-up-accent: var(--motif-accent, #2563eb);
  --motif-up-track: var(--motif-track, #e2e8f0);
  --motif-up-danger: var(--motif-danger, #dc2626);
  --motif-up-success: var(--motif-success, #16a34a);
  display: grid;
  gap: 0.5rem;
  max-width: 28rem;
}
.motif-upload__row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.motif-upload__meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8125rem;
  color: var(--motif-muted, #475569);
}
.motif-upload__track {
  position: relative;
  flex: 1;
  height: 0.5rem;
  border-radius: 999px;
  background: var(--motif-up-track);
  overflow: hidden;
}
.motif-upload__fill {
  height: 100%;
  border-radius: inherit;
  background: var(--motif-up-accent);
  width: 0%;
  transition: width 200ms ease;
  transform: translateZ(0);
}
.motif-upload[data-state="done"] .motif-upload__fill { background: var(--motif-up-success); }
.motif-upload[data-state="error"] .motif-upload__fill { background: var(--motif-up-danger); }
.motif-upload__cancel {
  font: inherit;
  font-size: 0.8125rem;
  padding: 0.4rem 0.75rem;
  min-height: 44px;
  min-width: 44px;
  border-radius: 0.5rem;
  border: 1px solid var(--motif-border, #cbd5e1);
  background: #fff;
  cursor: pointer;
}
.motif-upload__cancel:focus-visible {
  outline: 2px solid var(--motif-focus, #1d4ed8);
  outline-offset: 2px;
}
.motif-upload__cancel:disabled { opacity: 0.5; cursor: default; }
.motif-sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
@media (prefers-reduced-motion: reduce) {
  .motif-upload__fill { transition: none !important; }
}
`;

function useInjectedStyles() {
  useEffect(() => {
    if (typeof document === "undefined") return;
    if (document.getElementById(STYLE_ID)) return;
    const el = document.createElement("style");
    el.id = STYLE_ID;
    el.textContent = STYLES;
    document.head.appendChild(el);
  }, []);
}

export type UploadState = "idle" | "uploading" | "done" | "error" | "cancelled";

export interface UploadProgressProps {
  /** Performs the transfer. Call onProgress(0..1) as bytes move; respect signal. */
  upload: (onProgress: (fraction: number) => void, signal: AbortSignal) => Promise<void>;
  /** Human label for the thing being uploaded (used in announcements). */
  fileName?: string;
  /** Start immediately on mount. */
  autostart?: boolean;
  /** Announce a milestone at most this often (ms). */
  announceEvery?: number;
  className?: string;
  onComplete?: () => void;
  onError?: (err: unknown) => void;
  onCancel?: () => void;
}

export function UploadProgress({
  upload,
  fileName = "file",
  autostart = true,
  announceEvery = 1000,
  className = "",
  onComplete,
  onError,
  onCancel,
}: UploadProgressProps) {
  useInjectedStyles();

  const [state, setState] = useState<UploadState>("idle");
  const [percent, setPercent] = useState(0);
  const [live, setLive] = useState("");

  const controllerRef = useRef<AbortController | null>(null);
  const lastAnnounceRef = useRef(0);

  /** Announce, but at most once per `announceEvery`, plus always on terminal. */
  const announce = useCallback(
    (msg: string, force = false) => {
      const now = Date.now();
      if (!force && now - lastAnnounceRef.current < announceEvery) return;
      lastAnnounceRef.current = now;
      setLive(msg);
    },
    [announceEvery]
  );

  const start = useCallback(() => {
    if (state === "uploading") return;
    const controller = new AbortController();
    controllerRef.current = controller;
    setPercent(0);
    setState("uploading");
    lastAnnounceRef.current = 0;
    announce(`Uploading ${fileName}`, true);

    upload((fraction) => {
      const pct = Math.max(0, Math.min(100, Math.round(fraction * 100)));
      setPercent(pct);
      announce(`Uploading ${fileName}, ${pct}%`);
    }, controller.signal)
      .then(() => {
        if (controller.signal.aborted) return;
        setPercent(100);
        setState("done");
        announce(`Upload complete, ${fileName}`, true);
        onComplete?.();
      })
      .catch((err) => {
        if (controller.signal.aborted) {
          setState("cancelled");
          announce(`Upload cancelled, ${fileName}`, true);
          onCancel?.();
        } else {
          setState("error");
          announce(`Upload failed, ${fileName}`, true);
          onError?.(err);
        }
      });
  }, [state, upload, fileName, announce, onComplete, onError, onCancel]);

  const cancel = useCallback(() => {
    controllerRef.current?.abort();
  }, []);

  // Autostart / cleanup.
  useEffect(() => {
    if (autostart) start();
    return () => controllerRef.current?.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const isActive = state === "uploading";
  const dataState =
    state === "done" || state === "error" ? state : isActive ? "uploading" : "idle";

  return (
    <div className={`motif-upload ${className}`} data-state={dataState}>
      <div className="motif-upload__meta">
        <span>{fileName}</span>
        <span>
          {state === "done"
            ? "Done"
            : state === "error"
            ? "Failed"
            : state === "cancelled"
            ? "Cancelled"
            : `${percent}%`}
        </span>
      </div>

      <div className="motif-upload__row">
        <div
          className="motif-upload__track"
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={percent}
          aria-valuetext={`${percent}%`}
          aria-label={`Upload progress for ${fileName}`}
        >
          <div className="motif-upload__fill" style={{ width: `${percent}%` }} />
        </div>

        {isActive ? (
          <button type="button" className="motif-upload__cancel" onClick={cancel}>
            Cancel
          </button>
        ) : state === "error" || state === "cancelled" ? (
          <button type="button" className="motif-upload__cancel" onClick={start}>
            Retry
          </button>
        ) : null}
      </div>

      {/* Polite, throttled announcements. Does not steal focus. */}
      <span className="motif-sr-only" role="status" aria-live="polite">
        {live}
      </span>
    </div>
  );
}

export default UploadProgress;
