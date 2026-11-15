---
name: ps2-billymandy-inspired-visual-style
description: Create or refine original Blender and Unreal game assets in this project's Billy & Mandy PS2-derived visual identity using measured references and visual comparisons. Use for requests in our established game style, not generic cartoons or unrelated reverse engineering.
---

# PS2-inspired project visual style

Load the frozen v1.0 evidence baseline in [STYLE_BIBLE](references/STYLE_BIBLE.md). The [hand production amendment v1.1](references/HANDS.md) provides technical guidance for modeling and validating hands. Build new assets from Python using the included helpers and visual references. Start from a clean Blender scene.

1. Identify the asset family and intended camera distance. Read the Bible and view `assets/references/reference_board.jpg`. Use Jack as the primary character reference and select a relevant prop reference for other asset types. Read [REFERENCE_ASSETS](references/REFERENCE_ASSETS.md) for provenance or deeper investigation only.
2. For a specific likeness, follow [CHARACTER_MATCHING](references/CHARACTER_MATCHING.md) before detail: match camera and pose, build volumes from two views, and check front, profile, ¾ and top at one scale. For all new assets, state a short design brief: silhouette, color regions, identifying detail, contour implementation and deviations. Distinguish observations from adaptable production recommendations. Do not reopen all source blends for every new asset.
3. Use [BLENDER_WORKFLOW](references/BLENDER_WORKFLOW.md) and `scripts/style_core.py` for materials, contours, previews, audit and export. `scripts/build_mailbox.py` is an original worked prop example, not a universal generator. Build editable geometry appropriate to the request. For character hands, read [HANDS](references/HANDS.md) before modeling: identify the intended anatomy, apply human-hand guidance only where appropriate, and validate close-ups as well as gameplay views. Inspect MCP scene state before mutations; preserve existing work.
4. Follow [STYLE_VALIDATION](references/STYLE_VALIDATION.md). Render front/side/rear/oblique views at comparable apparent size, inspect images beside suitable references, correct important differences and repeat affected checks. Use local base/shadow/accent swatches and paired renders with and without outlines. Check head and hat depth, torso posture and footwear spacing before generating local contour widths. See the Jack v02 case in CHARACTER_MATCHING. For characters include deformation and expression samples. Technical success alone is insufficient.
5. For pose, rig or animation requests, follow [RIGGING](references/RIGGING.md). Verify the actual modifier-target rig, Action Slot, weights and surface/contour deformation with deliberate joint bends. Save a rig the user can select and pose.
6. For Unreal delivery use [UNREAL_WORKFLOW](references/UNREAL_WORKFLOW.md). Discover actual engine/MCP capabilities, explicitly rebuild materials, and test scale, culling, camera and color response. Blender renders or an FBX do not validate Unreal appearance. Report untested branches separately.
7. Save versioned editable blends with packed textures, exports and a validation record: baseline version, reference used, corrections, remaining limitations, actual engine versions. Reopen the blend. Show a final preview and usable paths.

For a fresh demonstration run `build_mailbox.py` for props or `build_clockwork_lookout.py` for characters in a background factory scene with a new output directory. For other assets reuse the helpers and artistic criteria, not the postbox shape. Do not ask the user to configure settings that can be scripted.

The baseline is an independently reviewed specification, not a claim of human aesthetic approval or pixel-identical game fidelity. Propose documented version changes rather than silently altering it. For another project copy this entire directory into `.agents/skills/`; reference images and core scripts are portable.

Use [WORKED_EXAMPLES](references/WORKED_EXAMPLES.md) to select reference images, run the original character and prop builders, and prepare attachments for a web LLM.
