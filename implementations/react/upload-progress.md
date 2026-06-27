# Upload Progress, React

A determinate upload progress control: a `role="progressbar"` bar that fills 0→100%, can
be **cancelled** mid-flight, and **announces** meaningful milestones to assistive tech
without spamming every percent.

File: [`UploadProgress.tsx`](./UploadProgress.tsx).

## Usage

```tsx
import { UploadProgress } from "./UploadProgress";

// Inject the real transfer. Call onProgress(0..1); respect the AbortSignal.
function uploadFile(file: File) {
  return (onProgress: (f: number) => void, signal: AbortSignal) =>
    new Promise<void>((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open("POST", "/api/upload");
      xhr.upload.onprogress = (e) => e.lengthComputable && onProgress(e.loaded / e.total);
      xhr.onload = () => (xhr.status < 400 ? resolve() : reject(new Error(`${xhr.status}`)));
      xhr.onerror = () => reject(new Error("network"));
      signal.addEventListener("abort", () => xhr.abort());
      const body = new FormData();
      body.append("file", file);
      xhr.send(body);
    });
}

<UploadProgress upload={uploadFile(file)} fileName={file.name} onComplete={refresh} />
```

The `upload` prop receives `(onProgress, signal)`; it is transport-agnostic (XHR shown,
but fetch streams or resumable uploads work too) and easy to unit-test with a fake.

## Algorithm

1. **Start** creates an `AbortController` and calls `upload(onProgress, signal)`, state →
   `uploading`.
2. **Progress** rounds the fraction to an integer percent, updates `aria-valuenow` and the
   fill width, and announces a **throttled** milestone ("Uploading file, 25%"), at most
   once per `announceEvery` (default 1s).
3. **Complete** sets 100%, state → `done`, and force-announces "Upload complete".
4. **Cancel** calls `controller.abort()`; the rejected promise is recognised as an abort
   (via `signal.aborted`) and yields state `cancelled` with its own announcement and a
   **Retry** button. Real errors become state `error`.
5. **Cleanup:** unmount aborts any in-flight transfer.

## Accessibility

- The bar is a `role="progressbar"` with `aria-valuemin/max/now`, `aria-valuetext`, and a
  descriptive `aria-label`.
- A separate **polite** `role="status"` live region carries throttled milestone text, so
  screen readers hear useful progress, not a flood of integers. Terminal events (done /
  cancelled / failed) always announce.
- Cancel/Retry are real focusable buttons (44px) with a visible focus ring. **Focus is
  never stolen** on completion or cancel.
- Status is shown with text ("Done" / "Failed" / "Cancelled" / "NN%"), not colour alone.

## Reduced-motion behaviour

The fill's `width` transition is removed under `@media (prefers-reduced-motion: reduce)`,
the bar still updates to the correct value, just without easing.

## Responsive behaviour

Fluid up to `28rem`; the track flexes to fill available width and the cancel button keeps
a 44px target. No fixed pixel motion.

## Browser support

All modern browsers. Self-contained, idempotent style injection is SSR-guarded
(`typeof document` check). Uses `AbortController`, supported everywhere current.

## Provenance: original (clean-room).
