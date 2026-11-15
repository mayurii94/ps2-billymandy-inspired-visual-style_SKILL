# Blender 5.1.2 production

## Tested components

`style_core.py`: graphic material with optional texture and corner color, explicit backface handling, reversed-winding shell for a closed static mesh, fixed preview cameras, finite-data/texture audit, FBX geometry export and manifest. `build_mailbox.py`: original deterministic 15-mesh prop with packed 128² atlas, four renders and FBX. Neither is an automatic character or environment generator.

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.1/blender.exe' --background --factory-startup --python '<skill>/scripts/build_mailbox.py' -- '<new-output-folder>'
```

The example refuses to overwrite an existing blend. Use a new revision folder. Substitute absolute locations at execution time; scripts themselves do not depend on this project's source assets. Background Blender needs an explicit executable path here: MCP's CLI helper reported `blender` absent from PATH. Live Blender MCP works.

## New asset procedure

1. Inspect `bpy.app.version_string`, `bpy.data.filepath`, `is_dirty`, object/collection state through MCP. Preserve an occupied scene. Work in a background process for scripted builds, then open the verified result in the fresh user scene. Scripts that clear a scene must run only in an explicitly fresh/factory scene.
2. Choose reference family and write a design brief. Establish silhouettes from actual front, side and intended gameplay view before detail. New convention: metres, +Z up, front -Y, ground pivot. This differs from the reconstructed character axes and must not be applied blindly to source rigs.
3. Create editable meshes, meaningful names and UVs. Apply nonuniform scale before hull construction. Use shared materials; the proof has two material roles, atlas and ink. Atlas UV islands have padding; no source game texture is reused in the proof.
4. Call `graphic_material` and add optional color modulation intentionally. It uses emission plus Backfacing/Transparent nodes so rendered culling is explicit. Blender's material culling toggle alone is not the cross-renderer contract. Texture alpha/cutouts are NOT implemented by this helper: extend and test a masked/decal variant when the asset needs one.
5. Add shells selectively. `outline_shell` is designed for closed static meshes with valid normals and no live deformation modifier. For skinned assets duplicate weights, validate matching deformation and choose modifier order deliberately. Do not use a static copied shell on an animated character. Reversed normals and single-sided black material are a pair.
6. Call `preview`, inspect the images, compare comparable apparent sizes. Camera framing is diagonal-bounds based and therefore not guaranteed to make very differently shaped assets occupy equal image height: manually normalize the review board when necessary. Keep aspect ratio intact. Revisit thickness/detail after seeing the images.
7. Run `audit`, pack images, save a versioned blend, reopen in a separate process and rerun finite/image checks. Images load lazily after reopening; `has_data=False` alone is not proof of missing texture. Read `pixels` or render before judging.
8. Export static geometry using `export_static`; provide source PNG and manifest alongside FBX. The custom Blender graph does not transfer as an Unreal shader. FBX roundtrip checks geometry/units, not rendering. Rebuild destination materials explicitly.

## Characters and animation — planned branch

Use the style criteria, but construct/validate a rig appropriate to the new anatomy. Maintain a clear root and deform hierarchy; bind in a documented rest pose; keep surface/outline weights synchronized. Test extreme bends, silhouette gaps, feet and face UVs. Give each action an explicit range and assign the matching action slot in Blender 5.1. Mark expression state changes CONSTANT. Save with fake users where needed and reopen/play the same samples. Bake constraints/control rig motion to the export deform bones; do not silently bake at an assumed PS2 rate. Use the project's chosen FPS.

The mailbox does not exercise skinning, animation transfer, morphs or collision. Those branches require their own prototype before a future delivery can be described as production validated.

## Template strategy

The deterministic script is the material/scene template, and the finished postbox blend is an editable worked example. Reuse the material construction and preview functions; do not start every new asset by remodeling the example postbox. Save a material asset library only when additional proven variants justify one. Current helpers intentionally avoid installing global Blender settings or modifying source blends.
