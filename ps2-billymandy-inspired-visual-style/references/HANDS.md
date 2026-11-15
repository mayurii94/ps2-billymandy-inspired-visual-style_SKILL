# Character hands — production guidance v1.1

Added 2026-11-14 after the Arun hand correction. This is a project production amendment to the frozen Style Bible v1.0, not a newly recovered rule of the PS2 game. Read before modeling or revising character hands.

## Choose anatomy first

Determine the intended anatomy from the request and references. For a human with ordinary bare hands, default to four fingers and one opposed thumb. A humanoid silhouette alone does not establish human hands. Preserve intentional cartoon digit counts, gloves, paws, claws, hooves, pincers, mechanical grippers and other nonhuman designs. Do not add human fingers or a thumb to anatomy that does not call for them. Ask only if the intended anatomy cannot reasonably be inferred.

## Human hand shape

- Build a flattened, gently cupped palm with a narrower wrist and a clear transition out of the sleeve. Judge its width, depth and length against this character's forearm; do not copy Arun's dimensions as a universal template.
- Give four fingers separate silhouettes, varied lengths, gradual taper, rounded tips and a mild relaxed bend. The middle finger is normally longest and the little finger shortest. Keep small readable gaps without forcing an exaggerated permanent spread.
- Place the thumb on the side of the palm with a broad root and a distinct web space. It should oppose the fingers and remain volumetric from the side, rather than becoming a fifth parallel finger or a pointed spike.
- Use connected palm-to-digit geometry for an ordinary bare hand. For example, extrude finger loops from four distal palm openings and the thumb from a lateral opening. Intersecting ellipsoids or capsules are a blockout, not a finished human hand. Separate parts remain appropriate for intentional segmented or mechanical anatomy.
- Spend geometry on silhouette, knuckle transitions and rounded tips. Orient successive thumb sections along its changing direction without reversing their ordering or folding the root. A manifold mesh can still self-intersect. Subdivision or smooth normals alone do not establish correct anatomy.
- Match the contour to the small features: a body-sized expanded shell can close finger gaps or make the palm look swollen. Inspect surface and reversed shell together; retain single-sided culling and matching skin weights.

Keep the low-poly graphic style. These rules improve readable anatomy; they do not require realistic tendons, nails, finger rigs or a fixed polygon budget. Existing hand-bone weights can suffice for a relaxed hand during walking. Add articulated finger deformation only when the requested animation needs it.

## Acceptance for created or changed hands

Inspect front/palm, side and oblique close-ups plus the intended gameplay distance. For human hands, verify the digit count, palm thickness, rounded tips, thumb web, wrist join and readable gaps. For other anatomy, check the corresponding intended structure and function instead.

Check connectedness, unintended non-manifold edges, self-intersections and flipped surfaces. For rigged characters, inspect representative movement extremes and the sleeve join; ensure surface and contour move together. When Unreal delivery is requested, inspect the imported hands in an engine close-up and during the requested motion. A distant full-body view or successful import does not pass this check. Correct visible failures and repeat affected views.

## Evidence and limits

Arun's original human hands used an oval palm about 0.104 m wide and 0.092 m deep, plus four short overlapping oval fingers and a separate oval thumb. The user reported that these looked like lumps. The correction replaced them with connected palms, narrower wrists, four separated tapered fingers and opposed thumbs. The main palm depth was reduced to roughly 0.028–0.038 m before smoothing; contour thickness was reduced from 0.006 m on the palm to 0.0013 m on the new hand. These are case measurements, not prescribed dimensions.

The revised meshes each had one connected surface, 698 vertices and no non-manifold edges. Front, side and oblique Blender views and an Unreal 5.9 hand close-up were inspected, and locomotion remained functional. An intermediate thumb-section orientation produced a folded dark surface despite manifold topology; visual inspection caught it and section orientation was corrected. Source evidence belongs to the Arun task's `Hands_v2` artifacts (before blend, mesh audit, hand renders and Unreal capture); using this guidance does not require those files. The user requested incorporating the lesson into this skill; this does not establish universal approval of Arun's proportions or validate finger articulation.
