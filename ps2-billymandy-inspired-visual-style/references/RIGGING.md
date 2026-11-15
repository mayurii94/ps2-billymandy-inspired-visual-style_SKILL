# Character rig and deformation

Use this when a request calls for posing, animation or an export skeleton. A static model can use the Clockwork Lookout example. A posed render or successful anatomy audit alone is insufficient to approve a rig.

## Plan the rig for the task

- **Pose study.** Provide explicitly selectable FK bones for each expected adjustment. State how to use Pose Mode and which controls are available. A single rigid glove can work for a static closed shape; animated fingers need their own joints and supporting geometry.
- **Animator rig.** Define the requested controls and motions first. For feet that must stay planted or arms that must reach, add and test IK only if needed. Confirm the bend direction, pole target and end-effector roll. If using a separate game skeleton, the control rig drives it through constraints and the mesh deforms once through the game skeleton.
- **Game export.** Document root, scale, axes, hierarchy and animation range. Export the deform skeleton with baked transforms when the workflow requires it. Test a reimport in the actual destination before claiming equivalence.

## Align the rig and bind it

1. Work from the character's own editable body geometry. Save the neutral stance and place hip, knee, ankle, shoulder, elbow, wrist and digit pivots from front and profile. Record bone axes and orient paired joints deliberately. Use a relaxed bend and sufficient support loops at the actual joint. Preserve the original visual stance as a separate pose if it needs sharper bends.
2. Resolve the armature from the active scene and from the **Armature modifier targets** of the visible meshes. A copied scene may contain a rig with a numeric suffix. Give the intended armature a clear name and select it before delivery. Prefer one active Armature modifier per bound surface. Check that every visible part follows the appropriate bone and all non-rigid parts have appropriate weights. Normalize named deform weights and account for zero-influence vertices.
3. For a corresponding outline shell, build a vertex map or duplicate the bound mesh with its weights. Apply the same weights and modifier evaluation to surface and outline. Compute weights on the surface first. If weights are recomputed from the shell's offset vertex positions, they can differ precisely at the joint. Keep the contour narrow near cuffs and fingers. For a separately authored line mesh, use correspondence or interpolated weight transfer and inspect the relationship while bent.
4. Assign the intended Action Slot, verify frame range and ensure that playback moves the visible rig. For a handoff in Pose Mode, show the working rig and choose a neutral or authored comparison pose. Keep the test pose or animation as a separate action.

## Functional review

- On a test copy, isolate the active action and NLA state. Move controls or pose bones separately while checking both bone movement and **evaluated mesh movement**. Restore the intended active action afterward. In FK, test representative elbow, wrist, knee and ankle motion, on both sides where applicable. Use realistic ranges and compare front, profile and ¾, with close-ups at cuffs and footwear. A scripted rotation is a probe; use the joint's intended axis for visual acceptance.
- Test actual scene actions at the beginning, a movement extreme and end. Check connectedness at joints, skin collapse, unintended stretch, occlusion and whether the silhouette still reads. Compare side-by-side with contours enabled and disabled. If weights agree and a dark shell still overlaps a surface, adjust shell thickness or placement locally.
- If there is IK, move real targets and pole controls, check feet/hand orientation and ensure the bones and mesh follow. If there are face shape keys, verify that corresponding graphic outlines also follow. Reopen the saved blend, select the intended rig and verify the same tests can be repeated. Record procedural checks and visual judgments separately.

## Portable diagnostic

`scripts/audit_rig.py` checks the active scene, Action Slot, evaluated vertex movement, named weight sums and one-to-one _Ink shell pairs. It probes selected joints at 60° around local X in a throwaway Blender process and writes JSON. It never saves the scene. Use this as a functional check. Human review of intended axes, deformation under motion and operation of controls remains necessary.

```text
blender --background "<character.blend>" --python-exit-code 1 --python scripts/audit_rig.py -- "<armature name>" "<report.json>" Forearm.L Hand.L Shin.L Foot.L
```

Use the actual bone names for your character. The automatic pair check expects an _Ink suffix, the corresponding surface name and equal vertex counts. An omitted pair requires manual correspondence inspection. The command isolates FK in memory by removing the active action and disabling NLA after the playback probe. Existing constraints remain active, so a blocked rotation may be an expected control dependency.

## Jack visual rebuild case

In the v04 rebuild, the active scene uses Jack_Rig.001. A different Jack_Rig datablock exists and does not drive those visible meshes. The active rig has a small pose study and no IK. It moved the evaluated meshes in playback and in local FK probes of forearm, hand, shin and foot. That establishes basic binding. It does not establish natural locomotion or articulation of the rigid gloves.

The audit found surface/outline weight mismatches on both trousers and both bent sleeves. The builder computed blends independently from each mesh's Z coordinate after generating a normal-offset shell. Compute weights once on the visible mesh, transfer them by index to its paired contour, and test at deep bends. Also test how the short transition rings hold shape. This is a concrete failure case for visual validation even when the script exports and all vertices have weights.
