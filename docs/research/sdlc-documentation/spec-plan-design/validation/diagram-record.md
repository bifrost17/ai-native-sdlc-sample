# Candidate example Mermaid rendering record

## Result

The 19 Markdown files under `docs/research/sdlc-documentation/spec-plan-design/candidate/examples/` contained five Mermaid blocks. All five rendered successfully to standalone SVG and 2x PNG. The browser-side bounds check found no diagram element outside its SVG viewport, and direct inspection found no clipping or overlap.

One non-blocking readability warning remains in candidate r1 at Git `2634f07`. Mermaid's automatic wrapping splits `기능` across lines in the F03 cleanup node (`cleanup: 최종 기 / 능`). The label remains legible and its meaning is preserved, but a shorter label or wider node would improve presentation.

## First pass and correction history

The first pass at `2026-09-11T07:30:33.967Z` found two warning groups: the F03 state diagram split `정리 요청` and `기능`, while the M01 deployment diagram split `프로세스` and `파일`. The candidate was then shortened before the r1 review snapshot. The rerender confirmed that the F03 transition and both M01 deployment warnings were corrected. The F03 cleanup node still splits `기능`, as recorded above. No pass found clipping or overlap.

The changed block hashes provide the source boundary for this history: F03 changed from `5fb8400dbffd2dc4e3169c142b3fd618f468b028e475b908741dc3c8315945d8` to `5f4913b09f1c8690fa003b6b832935ff068d48c7648cca44ac75bba98591c732`; the M01 deployment block changed from `4c9da86ac69c424d9125fc46799bdb55929f452481a0147ac7aae3aa9c9c88a6` to `ca5877047ebf30bf01c532c347fb3e950caee4880112048e0880809bb429fa9f`.

## Provenance

- Candidate snapshot: r1 at Git `2634f07`
- Rendered at: `2026-09-11T07:33:05.552Z` (`2026-09-11 16:33:05 +09:00`)
- Renderer: Mermaid `12.0.0`, fetched from `https://cdn.jsdelivr.net/npm/mermaid@12.0.0/dist/mermaid.min.js`
- Mermaid distribution SHA-256: `28fca7ae6ebc7ed7bb63bde63136a74bfef14f296a57e403657eeb8b32836073`
- Validation harness SHA-256: `26b54fe2a367c16d4ef2496d41c3b907e3fb477d43108b37f000a2d7be3d0c4e`
- Browser automation: Playwright `1.62.1`
- Browser: Google Chrome `153.0.8010.36`, headless, 2x device scale
- Theme/look/security: Mermaid `neutral`, `classic`, `securityLevel=strict`, deterministic IDs enabled
- Reproduction command from repository root: `node docs/research/sdlc-documentation/spec-plan-design/validation/diagrams/render-mermaid.mjs`
- Repository dependencies/install state: unchanged; the renderer uses the existing Playwright runtime and installed Chrome

## Source and artifact records

Each source hash is SHA-256 over the Mermaid block contents after removal of the closing newline. Artifact hashes are SHA-256 over the produced files.

| Source (opening fence) | Source SHA-256 | SVG (SHA-256) | PNG (SHA-256) | Rendered viewBox | Check |
|---|---|---|---|---|---|
| `F03/spec.md:42` | `5f4913b09f1c8690fa003b6b832935ff068d48c7648cca44ac75bba98591c732` | [`F03-spec-01-stateDiagram-v2.svg`](diagrams/F03-spec-01-stateDiagram-v2.svg) (`c8386e6637de6a79c3028a91969222d39c803ab2e6608ffbaf7529df49f59e6a`) | [`F03-spec-01-stateDiagram-v2.png`](diagrams/F03-spec-01-stateDiagram-v2.png) (`ee8a959a077b82cad558f4a6afba66fd6be85c4821f5ef4f86ff22e081f298f1`) | `299.5 × 726` | PASS with wrapping warning |
| `M01/design/architecture.md:5` | `db6ba75187e82fe6ea328bb034cfd18dc92cd54ec7e6c8f6f65b38be9dfabb61` | [`M01-design-architecture-01-flowchart.svg`](diagrams/M01-design-architecture-01-flowchart.svg) (`e735800d60cb4bfe5206e50df9321d2a8a29cbef8e5070bf4807c8d01d018ff4`) | [`M01-design-architecture-01-flowchart.png`](diagrams/M01-design-architecture-01-flowchart.png) (`40d4c0b34b6a1edbc6801675dffc00aa6f22e4c1e5eed6d40d3082c4e4257dd7`) | `1260.640625 × 211.884628` | PASS |
| `M01/design/architecture.md:23` | `5559f553e2c9a8e6395110ad3d5718f5736815f4ab8254ce31bf55076f968f80` | [`M01-design-architecture-02-classDiagram.svg`](diagrams/M01-design-architecture-02-classDiagram.svg) (`4aec39da9a82bd7d68c71d1992a274ed5413999a10e207d77fd96157d84f1cf0`) | [`M01-design-architecture-02-classDiagram.png`](diagrams/M01-design-architecture-02-classDiagram.png) (`9cb80f62a899143a5500b01d978bfb94418c01702bf15c05949e081b89a6cb7b`) | `368.804688 × 486` | PASS |
| `M01/design/architecture.md:51` | `ca5877047ebf30bf01c532c347fb3e950caee4880112048e0880809bb429fa9f` | [`M01-design-architecture-03-flowchart.svg`](diagrams/M01-design-architecture-03-flowchart.svg) (`bcea82d7ed0a49532e6e9b61a1fb140123e5c2255349c3eb6cd45884229a1ba0`) | [`M01-design-architecture-03-flowchart.png`](diagrams/M01-design-architecture-03-flowchart.png) (`14dac3a4ed3c632dc0bb5f70a59b66a9e0a39cc27760922b5384425ed815bcad`) | `583.605469 × 546.942322` | PASS |
| `M01/design/storage.md:31` | `01d0dee500892ac705f761e240d7435c4fb1e3d6ae9f62bc662b4829aa545071` | [`M01-design-storage-01-sequenceDiagram.svg`](diagrams/M01-design-storage-01-sequenceDiagram.svg) (`e46e5e8df75c3d243edb626810bbe6ed20fce9c2e4d9ab413f5592325850c26b`) | [`M01-design-storage-01-sequenceDiagram.png`](diagrams/M01-design-storage-01-sequenceDiagram.png) (`783c03f824a968294006f114bd3e28e80d7ce17ecfd9180f1dacff33d3eb7f29`) | `819 × 688` | PASS |

## Checks performed

The renderer extracts every fenced `mermaid` block from the explicit example-file inventory, calls `mermaid.render`, writes the returned SVG, and captures the rendered element as PNG. It records parse/render exceptions and compares the client bounds of text, labels, nodes, and clusters with the SVG viewport (one-pixel tolerance).

Direct PNG inspection covered all five artifacts at original resolution:

- F03 state diagram: no clipping or overlap; cycle arrows and transition direction are visible; remaining automatic Korean word split noted above.
- M01 component flowchart: no clipping or overlap; both callers, facade branches, adapters, and stores are distinguishable.
- M01 class diagram: no clipping or overlap; class members and dependency label are legible.
- M01 deployment flowchart: no clipping or overlap; host boundary and four inbound paths are visible; first-pass word-splitting warnings are corrected.
- M01 concurrency sequence: no clipping or overlap; participants, alternate branches, responses, and failure note are legible.

This is artifact validation only. It does not assert that the diagrams' proposed behavior has been implemented or observed in a running product.
