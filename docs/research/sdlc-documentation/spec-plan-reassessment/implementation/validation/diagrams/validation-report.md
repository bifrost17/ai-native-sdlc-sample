# Mermaid diagram validation report

Validated repository revision: `1500b16`

## Scope and method

The validation renderer scanned these candidate source files without modifying them:

- `F03/spec.md` — 1 Mermaid block
- `M01/design/architecture.md` — 3 Mermaid blocks
- `M01/design/storage.md` — 1 Mermaid block
- `W01/spec.md` — 1 Mermaid block

The adapted renderer uses Mermaid 12.0.0, Playwright 1.62.1, and Google Chrome
153.0.8010.36. It separately parses every Mermaid source before rendering, writes
SVG and 2x PNG outputs, measures text, foreign-object, node, and cluster bounding
boxes against the SVG viewport, and records source and output SHA-256 hashes in
`render-manifest.json`.

## Automated results

All 6 expected diagrams rendered successfully. All 6 passed Mermaid syntax parsing.
No measured element exceeded its SVG viewport; every result has an empty `overflow`
array in the manifest.

| Source | Diagram | Syntax/render | Measured overflow |
| --- | --- | --- | ---: |
| `F03/spec.md:44` | state diagram | pass | 0 |
| `M01/design/architecture.md:11` | current/proposed storage flow | pass | 0 |
| `M01/design/architecture.md:54` | storage class diagram | pass | 0 |
| `M01/design/architecture.md:83` | deployment flow | pass | 0 |
| `M01/design/storage.md:31` | concurrent completion sequence | pass | 0 |
| `W01/spec.md:44` | requester API sequence | pass | 0 |

## Visual inspection

Each generated PNG was inspected at its original resolution.

- F03: State labels, transition labels, arrowheads, and the two-way release/disable
  transition are visible and distinguishable. The two lateral transition labels are
  close to one another but do not overlap or obscure the paths.
- M01 architecture diagram 1: Both subgraphs, dashed backend choices, labels, and
  database shapes are clear. The diagram is wide (1448.67 CSS px) but remains readable
  at its native output size.
- M01 architecture diagram 2: Class names, members, types, dependency arrow, and
  relationship label are legible with no clipping.
- M01 architecture diagram 3: Host boundary, configuration text, HTTP credential
  label, operation path, and both storage arrows are legible with no collisions.
- M01 storage: Participant names, messages, `alt` branches, return arrows, and the
  dark note are fully visible and legible.
- W01: Actor and participant labels, self-call, `alt` branches, response paths, and
  bottom participant labels are fully visible and legible.

No material readability error was found.

## Reproduction

Run from the repository root:

```sh
node docs/research/sdlc-documentation/spec-plan-reassessment/implementation/validation/diagrams/render-mermaid.mjs
```

The renderer overwrites only its generated files in this validation directory. The
full source hashes, Mermaid bundle hash, browser version, dimensions, element counts,
overflow findings, output paths, and SVG/PNG hashes are in `render-manifest.json`.
