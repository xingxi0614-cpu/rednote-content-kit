# Image Generation Contract

## What is bundled

This Skill bundles the visual workflow, deterministic slot names, a machine-readable image plan, local file validation, duplicate detection, spec binding, and strict completion rules.

## What is host-provided

The actual image model is a capability of the host application. It may appear as `imagegen`, Imagen, or another approved built-in image-generation tool. The model, credentials, quota, and service terms are not part of this MIT-licensed repository.

The plugin must never ask the user to paste an image-provider API key into a project file or command.

## Required source-image qualities

- landscape raster image, preferably 4:3
- at least 768 pixels wide and 512 pixels high
- no embedded text
- no watermark, logo, brand mark, or app interface
- no fake analytics, testimonials, or screenshots
- enough negative space to survive the final crop
- a fresh visual for each album card

## Honest fallback

When the host does not expose image generation:

1. accept user-supplied images that meet the same validation contract, or
2. emit the image plan and stop before strict rendering.

An abstract placeholder is allowed only when the user explicitly requests a draft or wireframe. It must be labeled as a placeholder and must not be reported as a finished photographic card.
