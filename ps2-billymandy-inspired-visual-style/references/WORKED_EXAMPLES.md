# Worked examples and handoff

Jack is the approved character reference for this style. Compare new characters with the bundled front, profile and three-quarter views and the animation contact sheet. The bundled images are sufficient to study his silhouette, palette and contours.

Read the Style Bible, Blender Workflow, Style Validation and Hands amendment for new models. Use the bundled boards and images for visual comparisons. These are the starting inputs a new context needs.

| Reference | Reusable observation | Where to look |
|---|---|---|
| Jack | Tall narrow body, oversized hat and shoes, selective face-atlas detail, thin contours | assets/references/Jack_front.png and Jack_side.png |
| GrillO | Few broad facets, a thin rim and sparse functional details, with painted tonal variation | assets/references/Grill_angle.png |
| CarO | Compact wheelbase and large planar body panels with a simple window color block | assets/additional_references/CarO.png |
| Ftree | A bent primary mass, tapered secondary branches and subdued surface markings | assets/additional_references/Ftree.png |
| House4 | Compare ground-level props, broken fragments, furniture, foliage and architectural modules | assets/additional_references/House4_Reference_Board.jpg |
| Skarr and Dracula | Compare hand profiles, changes caused by rig pose, and costume-specific boundaries | assets/additional_references/Skarr_T.jpg and Dracula.jpg |

Use the packaged images of Jack, Ftree, CarO and GrillO as visual references. Both procedural builders start from a clean scene and use only bundled Python and Blender.

```text
blender --background --factory-startup --python-exit-code 1 --python scripts/build_mailbox.py -- "<new prop output>"
blender --background --factory-startup --python-exit-code 1 --python scripts/build_clockwork_lookout.py -- "<new character output>"
```

The mailbox demonstrates atlas, local contour widths and FBX handoff.

The Clockwork Lookout is an original static character. It applies a lanky silhouette, large shoes, a tilted cap, restrained color blocks and controlled outlines to a mechanical design. It demonstrates a cap with irregular cross-sections, a generated packed face graphic UV-mapped directly onto curved polygons, and thinner outlines on grippers than on the coat. Review views include top, elevated ¾ and paired profiles with and without ink. The QA JSON records assigned face polygons and contour widths. See the [generated preview](../assets/proof/Clockwork_Lookout.png). Jack remains the visual benchmark. Apply HANDS.md when designing articulated hands.

For a web LLM, attach SKILL.md and the explicitly referenced Markdown files, a few relevant PNG/JPG views, and optionally style_core.py plus the applicable example. Ask for one standalone Blender Python script that creates your new design, saves an editable blend and renders the necessary review views. Give an output folder argument and exact Blender version. Ask it to state which checks still require local execution.

For a worked revision of head proportions, torso depth, footwear and local ink, see the [Jack v02 silhouette study](CHARACTER_MATCHING.md#6-refine-the-silhouette-using-the-jack-v02-study).
