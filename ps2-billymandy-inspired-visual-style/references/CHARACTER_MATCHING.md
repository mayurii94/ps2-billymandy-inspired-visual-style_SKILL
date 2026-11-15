# Character matching and style validation

Use this workflow when reproducing a specific appearance or auditing a close match. For a new design, use the methods to test volume and contrast in that character's own proportions and palette.

## 1. Block volumes in two views

Draw a landmark map over front and profile references at the same apparent character height. On Jack mark the brim and crown, front of the pumpkin and its chin, shoulder, elbows, waist, wrists, heel and toe. Track width from the front and front-to-back extent from the profile. Build a blockout with named editable volumes. Use the profile to place the elbow, wrist and foot in depth. Render front, profile, ¾ and top at one orthographic scale before eyes, creases or outlines. If a feature is obscured in the source top view, use the generated top view to inspect the construction and label the inferred depth.

## 2. Record camera and pose

Record model forward/up axes, camera direction, projection, scale relative to character height, source action/frame or reference image ID and stance. Recreate comparable hip, knee, elbow and wrist rotations before judging likeness. Keep a neutral view for judging construction. Add an elevated ¾ to see how the brim overlaps the eyes. Check occlusion with the actual geometry and reproduce local shade with painted tone where the design calls for it. Avoid interpreting a difference caused by an arm swing as a fixed body proportion.

## 3. Sample local tones

For each important region record base, shadow and accent from fully covered interior pixels. Keep sRGB samples separate from the linear values entered into shader nodes. Use common camera and display settings such as Standard, exposure 0, gamma 1 and a shared neutral background. The rendered values describe the appearance of an area and will differ from a raw palette or shader constant. Correct individual regions. For a new design retain the contrast hierarchy through a palette suited to that design.

In the Jack audit the pumpkin sample was RGB 208/85/26 in the reference and 231/108/24 in the reconstruction. The boots were 88/52/75 and 101/65/94, while the hat was 102/102/151 and 102/97/142. These are illustrative base samples; collect matching source shadow and accent samples in the intended pose before using colors as targets. Shadows beneath the brim and accents on the lips, eyes and feather need their own treatment.

## 4. Inspect outlines at equal apparent size

Render matching views at the same subject pixel height and keep both contour-on and contour-off versions. With the contour off, inspect depth, seams and intersections. With it on, judge brim, digits, sole and small negative spaces separately. Use thinner shells or local line geometry where the full-body line width closes gaps. When the design moves, inspect hands on hips, a grip or other deep bends and test skin weights on the contour alongside the color surface. Technical validity and aesthetic likeness are separate review gates. Record each gate and a concrete fix for failed comparisons.

## 5. Use the bundled example and reference

[Clockwork Lookout builder](../scripts/build_clockwork_lookout.py) runs in a clean Blender scene and generates all geometry and the packed face graphic. Its mechanical grippers and static pose make the example a demonstration of shape and line placement. A moving character needs its own posed review.

Jack's matched views show the same saved body pose used for the measurements.

- [Front](../assets/additional_references/Jack_Matched_front.png)
- [Profile](../assets/additional_references/Jack_Matched_side.png)
- [¾](../assets/additional_references/Jack_Matched_angle.png)
- [Posed proportions and camera setup](../assets/additional_references/Jack_Posed_Measurements.json)

The base Jack in frame 47 measured width 45.6% and depth 43.0% of height. A height band can include several parts and their contours. The archived values describe one pose on one character. Use them as an example of what to measure and confirm the comparable pose before turning any value into an asset target.

## 6. Refine the silhouette using the Jack v02 study

Use this pass when a procedural character reads too flat or its outline is too weak. Compare at a common pixel height. Apply changes locally and review the resulting shape before assigning new contour widths.

| Region | Production decision | Acceptance check |
|---|---|---|
| Head, hat and face | Tune width, height and depth independently. Shape the rear crown and brim in profile. Turn the head, surface graphics, hat and feather together around the head pivot. | In front and ¾, the head has room to read against the shoulders. In profile, the brim follows the intended overlap without clipping the head. Inspect the face from an elevated ¾. |
| Tunic, upper arms and hands | A fitted silhouette can be narrow across the front while retaining a substantial depth in profile. Place shoulders, elbows, cuffs and hands in depth as a chain. Move buttons, belt and buckle with the adjusted cloth surface. | The arms on hips read as a spatial gesture. The waist and hem remain distinct, and the cuffs meet the hands from front and profile. |
| Footwear and hem | Define the heel, ankle opening, sole and toe in profile. Use variable cross-sections and preserve the hooked toe and sharper ankle edge when matching Jack. Set each foot's yaw and spacing, then align the lower leg to the new ankle. | Review the toe and heel from the side, and retain a visible gap between the shoes and their outlines in the front view. Check that cuffs and ankles still meet after repositioning. |
| Contour hierarchy | Generate shells after the geometry pass. Strengthen large silhouettes locally at brim, skull and boots, use a moderate line on clothes, and retain a fine line at fingers and tight seams. Sample the ink under the same display settings. | Compare on/off at identical framing. Put the ink back on and inspect the shoe gap, the hat–face overlap and the finger gaps. For a rigged asset also test the outlined surfaces in bent poses using RIGGING.md. |

The static Jack v02 revision changed head width by −7.5%, head height by −4% and head depth by +6.5%, then narrowed the tunic by 11.5% while deepening it by 24%. These are local v01-to-v02 builder adjustments for this case. Use the board to judge the shape and treat the values as examples of a controlled revision. The board compares the frame-47 reference and the two procedural versions at equal apparent height. The source profile was mirrored for presentation and the poses and angles differ slightly. The study covers static shape and contour.

[Jack v02 comparison, with reference and v01 for context](../assets/proof/Jack_Proportion_Study_v02.jpg)
