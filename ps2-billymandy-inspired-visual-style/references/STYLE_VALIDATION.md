# Acceptance and drift control

Maintain two independent decisions: **technical pass** and **artistic review**. The agent can review and iterate autonomously. Record human approval only when actually given. A successful script, a low polygon count or a matching palette is not a style certificate.

## Reference and capture setup

Start with `assets/references/reference_board.jpg`, then inspect the individual PNGs for the most appropriate family. Use original aspect ratio; match subject pixel height when judging contour thickness. Reference camera directions and bounds are in `measurements.json`. Four directions for asymmetric props; front/profile/oblique and movement extremes for characters; gameplay-scale and overview for environments. Add intended perspective view beyond the diagnostic ortho board.

Use a common neutral backdrop and record view transform/exposure, resolution, camera, asset pose, baseline version and reference. Do not compare a tiny thumbnail to a large close-up and conclude the outline matches. Different character palettes/proportions are legitimate.

For created or revised character hands, apply the anatomy-specific close-up and motion checks in [HANDS](HANDS.md). A whole-character thumbnail cannot establish finger separation, thumb shape or palm depth. Human digit counts are not acceptance criteria for nonhuman anatomy.

## Technical gates

| Check | Passing evidence | Failure response |
|---|---|---|
| File preservation | Source hashes unchanged, new version path | Stop destructive write; recover from untouched input |
| Mesh validity | Finite vertices, intentional topology/normals, expected materials and UVs | Repair geometry/UVs before judging render |
| Texture portability | Packed image readable after reopen, standalone export PNG present | Pack or fix source path; don't rely on open-session cache |
| Hull behavior | Single-sided reverse winding, no surface occlusion or intersection holes in reviewed views | Fix winding, thickness or use local strips |
| Scale/orientation | Manifest and destination bounds agree in cm; asymmetric front marker faces intended axis | Correct import/export transform; don't guess a 100x scale |
| Rig, when applicable | Named hierarchy, normalized weights/quaternions, finite sampled poses, matching surface/hull deformation | Repair before transfer; static test does not cover this |
| Actions, when applicable | Separate named ranges, slots assigned, reopened playback and facial states checked | Fix action binding/export baking |
| Export | Reimport geometry/units, explicitly rebuild shader and inspect destination images | Treat FBX material conversion as unvalidated |
| Runtime | Profile intended target scene/hardware | No performance claim from one static render |

Proof numeric tolerances: 1e-5 m Blender roundtrip and .1 cm Unreal bounds are numerical transfer checks chosen well above observed float noise and far below an artist-visible size change. They are not artistic tolerances or original PS2 constants. Hash equality is exact. Do not use arbitrary shape/similarity scores to automate artistic acceptance.

## Artistic review prompts

- Can the asset be recognized from its major silhouette at the intended distance?
- Are the most important color masses coherent, with quieter supporting regions?
- Does its contour have similar visual prominence to the selected reference at comparable size? Are necessary gaps still open?
- Do internal lines communicate articulation/function rather than cover the model with decoration?
- Are texture variations broad and purposeful? If a glossy/light response is introduced, does it overwhelm the established color hierarchy?
- Does profile depth support the design rather than reveal an accidental flat cutout? Are camera occlusions deliberate?
- For motion, do identity, gaps, face and contour remain readable at extremes?

Describe each significant mismatch and the correction, then re-render affected views. Avoid forcing a new character into Fred's proportions or a prop into the postbox palette simply to improve a numeric comparison.

## Controlled counterexamples and demonstrated iteration

The proof's initial contour was too thin compared with Grill/Pumpkin. Revision 2 increased selected shell widths while preserving geometry design and palette. `assets/proof/DEVIATIONS.jpg` shows the baseline, a no-shell version and a deliberately glossy version. These are visual experiments, not additional approved materials. The no-shell result loses separation; the glossy result introduces dark/reflection-dependent masses. `assets/proof/STYLE_COMPARISON.jpg` records the corrected result beside source props.

## Cross-engine comparison

Compare the same asset/pose, camera projection and framing with explicit color-management settings. First verify silhouette alignment, material slots, culling and UV orientation. Then inspect broad patch colors and contour weight. For aligned images, report silhouette intersection-over-union and RGB differences on interior pixels away from edges; record background/alpha handling and filtering. Metrics diagnose transfer errors, not creative similarity. If exposure/tonemapping differ, do not hide the difference behind an overall perceptual score.

A static proof validates only its tested material/mesh path. Skeletal meshes, face-atlas state control, gameplay lighting, LOD, collision, temporal effects and runtime performance need additional gates. State exactly which passed and which remain pending.

## Record format

Use a JSON or Markdown record with asset/revision, style version, references, engine versions, views/frames, technical results, artistic observations, corrections, intentional deviations and untested branches. Keep new experiments outside the frozen baseline. Any shared-rule change must include supporting before/after evidence and a versioned proposal.

## Specific character likeness

Apply the [character matching workflow](CHARACTER_MATCHING.md). Save the pose and camera record with the comparison. Review a four-view blockout before details, sample local tones, and keep a matched contour-on/off diagnostic. Record problems with silhouette, palette or moving contours even if the mesh passes technical checks.

For rigged assets use [RIGGING](RIGGING.md). Test the active rig and Action Slot, verify paired surface/outline weights, and inspect actual posed deformation after reopening.
