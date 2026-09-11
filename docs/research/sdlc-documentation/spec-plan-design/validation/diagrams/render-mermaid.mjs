#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { chromium } from "/Users/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs";

const repoRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../../../../../..",
);
const examplesRoot = path.join(
  repoRoot,
  "docs/research/sdlc-documentation/spec-plan-design/candidate/examples",
);
const outputRoot = path.join(
  repoRoot,
  "docs/research/sdlc-documentation/spec-plan-design/validation/diagrams",
);
const mermaidUrl =
  "https://cdn.jsdelivr.net/npm/mermaid@12.0.0/dist/mermaid.min.js";
const chromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const markdownFiles = [
  "B01/context.md",
  "B01/intent.md",
  "B01/plan.md",
  "B01/spec.md",
  "F01/context.md",
  "F01/intent.md",
  "F01/plan.md",
  "F01/spec.md",
  "F03/context.md",
  "F03/intent.md",
  "F03/plan.md",
  "F03/spec.md",
  "M01/context.md",
  "M01/design/architecture.md",
  "M01/design/operations.md",
  "M01/design/storage.md",
  "M01/intent.md",
  "M01/plan.md",
  "M01/spec.md",
];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function slug(relativePath, index, source) {
  const kind = source.trim().split(/\s+/u)[0].replace(/[^a-z0-9-]/giu, "-");
  return `${relativePath.replace(/\.md$/u, "").replaceAll("/", "-")}-${String(index + 1).padStart(2, "0")}-${kind}`;
}

await mkdir(outputRoot, { recursive: true });

const response = await fetch(mermaidUrl);
if (!response.ok) {
  throw new Error(`Mermaid fetch failed: ${response.status} ${response.statusText}`);
}
const mermaidScript = await response.text();

const diagrams = [];
for (const relativePath of markdownFiles) {
  const markdown = await readFile(path.join(examplesRoot, relativePath), "utf8");
  const blocks = [...markdown.matchAll(/^```mermaid\s*\n([\s\S]*?)^```\s*$/gmu)];
  for (const [index, match] of blocks.entries()) {
    diagrams.push({
      relativePath,
      index: index + 1,
      source: match[1].trimEnd(),
      sourceHash: sha256(match[1].trimEnd()),
      sourceLine: markdown.slice(0, match.index).split("\n").length,
      slug: slug(relativePath, index, match[1]),
    });
  }
}

const browser = await chromium.launch({
  executablePath: chromePath,
  headless: true,
});
const browserVersion = browser.version();
const page = await browser.newPage({
  viewport: { width: 1800, height: 1200 },
  deviceScaleFactor: 2,
});
await page.setContent(`<!doctype html>
<html><head><meta charset="utf-8"><style>
html, body { margin: 0; background: #fff; }
#diagram { display: inline-block; padding: 24px; background: #fff; }
#diagram svg { display: block; max-width: none; height: auto; }
</style></head><body><main id="diagram"></main></body></html>`);
await page.evaluate(() => {
  let state = 0x5eed1234;
  Math.random = () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 0x100000000;
  };
});
await page.addScriptTag({ content: mermaidScript });
await page.evaluate(() => {
  window.mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: "neutral",
    look: "classic",
    deterministicIds: true,
    deterministicIDSeed: "candidate-example-validation",
  });
});

const results = [];
for (const diagram of diagrams) {
  try {
    const rendered = await page.evaluate(async ({ id, source }) => {
      const result = await window.mermaid.render(id, source);
      const host = document.querySelector("#diagram");
      host.innerHTML = result.svg;
      result.bindFunctions?.(host);
      await document.fonts.ready;
      const svg = host.querySelector("svg");
      const viewBox = svg.viewBox.baseVal;
      svg.style.maxWidth = "none";
      svg.setAttribute("width", String(viewBox.width));
      svg.setAttribute("height", String(viewBox.height));
      const svgRect = svg.getBoundingClientRect();
      const elements = [...svg.querySelectorAll("text, foreignObject, .node, .cluster")];
      const boxes = elements.map((element) => {
        const box = element.getBoundingClientRect();
        return {
          tag: element.tagName,
          className: element.getAttribute("class") ?? "",
          x: box.left - svgRect.left,
          y: box.top - svgRect.top,
          width: box.width,
          height: box.height,
        };
      });
      const tolerance = 1;
      const overflow = boxes.filter(
        (box) =>
          box.x < -tolerance ||
          box.y < -tolerance ||
          box.x + box.width > svgRect.width + tolerance ||
          box.y + box.height > svgRect.height + tolerance,
      );
      return {
        svgMarkup: svg.outerHTML,
        viewBox: {
          x: viewBox.x,
          y: viewBox.y,
          width: viewBox.width,
          height: viewBox.height,
        },
        renderedSize: {
          width: svg.getBoundingClientRect().width,
          height: svg.getBoundingClientRect().height,
        },
        elementCount: boxes.length,
        overflow,
      };
    }, { id: `diagram-${diagram.slug}`, source: diagram.source });

    const svgPath = path.join(outputRoot, `${diagram.slug}.svg`);
    const pngPath = path.join(outputRoot, `${diagram.slug}.png`);
    await writeFile(svgPath, `${rendered.svgMarkup}\n`, "utf8");
    await page.locator("#diagram").screenshot({ path: pngPath });
    const { svgMarkup: _svgMarkup, ...renderMetrics } = rendered;
    results.push({
      ...diagram,
      status: "rendered",
      svg: path.relative(repoRoot, svgPath),
      png: path.relative(repoRoot, pngPath),
      ...renderMetrics,
    });
  } catch (error) {
    results.push({
      ...diagram,
      status: "error",
      error: error instanceof Error ? error.message : String(error),
    });
  }
}

await browser.close();

console.log(JSON.stringify({
  generatedAt: new Date().toISOString(),
  mermaid: {
    version: "12.0.0",
    url: mermaidUrl,
    scriptSha256: sha256(mermaidScript),
  },
  playwright: "1.62.1",
  browser: `Google Chrome ${browserVersion}`,
  markdownFilesScanned: markdownFiles.length,
  diagramCount: diagrams.length,
  results,
}, null, 2));
