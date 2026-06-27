# Empty State, Frappe-Vue

A calm, guiding empty state for a list/report/section with no rows yet. It offers a
**clear primary action**, stays blame-free, and distinguishes "nothing here yet" from
"no search results".

File: [`EmptyState.vue`](./EmptyState.vue).

## Usage (frappe-ui SPA)

```vue
<script setup>
import EmptyState from "./EmptyState.vue";
import { createResource } from "frappe-ui";

const customers = createResource({ url: "frappe.client.get_list", /* … */ });

function newCustomer() { /* open quick-entry / route to /new */ }
function clearFilters() { /* reset the resource filters */ }
</script>

<template>
  <EmptyState
    v-if="customers.data && customers.data.length === 0"
    variant="empty"
    :primary-label="__('New Customer')"
    :secondary-label="__('Import')"
    @primary="newCustomer"
    @secondary="clearFilters"
  />
</template>
```

It is **presentational**: it renders the labels you pass and emits `primary` /
`secondary`; the parent owns the data/resource. That keeps it usable both in a frappe-ui
SPA and in classic Desk (mount it into a list view's empty slot). Pass `frappe._('…')` /
`__()` strings from the parent so no Frappe dependency is bundled.

## Variants

- `variant="empty"` (default), there is genuinely no data yet. Title defaults to
  "Nothing here yet" and the copy invites the first action.
- `variant="no-results"`, filters/search returned nothing. Copy suggests changing the
  search or clearing filters (pair it with a "Clear filters" `secondaryLabel`).

`title` and `description` override the sensible, calm defaults.

## Accessibility

- The block is a labelled `role="region"` (`aria-label` = the title) so it is reachable
  as a landmark.
- The icon is `aria-hidden`; all meaning is in the heading + description text.
- The primary/secondary actions are real `<button>`s with visible focus rings and 44px
  targets.
- `autofocusPrimary` is **off by default**, so the empty state never yanks focus when it
  appears; opt in only when the empty state is the page's sole purpose.

## Reduced-motion behaviour

A gentle fade/raise (`motif-empty-in`, opacity + translateY) plays on appear and is
removed under `@media (prefers-reduced-motion: reduce)`, the content simply shows.

## Responsive behaviour

Centered, capped at `30rem`, with actions that wrap on narrow screens. No fixed pixel
motion.

## Browser support

All modern browsers. Vue 3 + scoped CSS only.

## Provenance: original (clean-room).
