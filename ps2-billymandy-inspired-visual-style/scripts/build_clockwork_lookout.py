"""Build an original clockwork lookout from geometry and colors alone.

Blender 5.1: blender --background --factory-startup --python-exit-code 1
    --python scripts/build_clockwork_lookout.py -- NEW_OUTPUT_DIR
"""
import json
import math
from pathlib import Path
import sys

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mathutils import Vector
from style_core import audit, bounds, graphic_material, outline_shell, preview


def color(hex_rgb):
    srgb = [int(hex_rgb[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + .055) / 1.055) ** 2.4 if v > .04045 else v / 12.92 for v in srgb) + (1,)


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    blend = output / 'Clockwork_Lookout.blend'
    if blend.exists():
        raise FileExistsError(blend)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    palette = {
        'ink': '171621', 'jacket': '574d77', 'shadow': '3e344f',
        'brass': 'df9d46', 'ivory': 'ecd8ac', 'red': 'ad404d',
        'glass': 'a6ecda', 'boot': '382f46',
    }
    mats = {name: graphic_material(name.title(), color=color(value)) for name, value in palette.items()}
    parts = []

    def rings(name, rows, mat, width=.008, sides=8, section=None):
        # Rows are z, X center, Y center, X radius and Y radius.
        vertices = [
            (x + rx * math.cos(a * math.tau / sides + math.pi / sides),
             y + ry * math.sin(a * math.tau / sides + math.pi / sides), z)
            for z, x, y, rx, ry in rows for a in range(sides)
        ]
        if section:
            vertices = [section(i // sides, i % sides, *v) for i, v in enumerate(vertices)]
        faces = [tuple(reversed(range(sides)))]
        for ring in range(len(rows) - 1):
            for i in range(sides):
                j = (i + 1) % sides
                start = ring * sides
                faces.append((start+i, start+j, start+j+sides, start+i+sides))
        faces.append(tuple(range(len(vertices)-sides, len(vertices))))
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)
        mesh.materials.append(mats[mat])
        parts.append(obj)
        if width:
            parts.append(outline_shell(obj, mats['ink'], width))
        return obj

    def plate(name, coords, mat):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata([(x, y, z) for x, y, z in coords], [], [tuple(range(len(coords)))])
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        scene.collection.objects.link(obj)
        mesh.materials.append(mats[mat])
        parts.append(obj)

    # Long tapering legs, generous shoes and an angular head with a short brim.
    for sign, side in [(-1, 'R'), (1, 'L')]:
        x = sign * .115
        rings(f'Boot {side}', [(.015,x,-.07,.11,.17),(.06,x,-.075,.12,.18),(.135,x,.008,.075,.09)], 'boot')
        rings(f'Leg {side}', [(.10,x,.022,.048,.062),(.45,x,.015,.053,.063),(.85,sign*.09,.01,.067,.068)], 'shadow')
        rings(f'Sleeve {side}', [(.77,sign*.29,0,.053,.052),(1.02,sign*.26,.025,.062,.063),
                                (1.25,sign*.208,.02,.083,.067)], 'jacket')
        rings(f'Gripper {side}', [(.665,sign*.305,-.015,.044,.035),(.73,sign*.293,0,.069,.047),
                                (.80,sign*.29,.003,.043,.046)], 'brass',.005)
    rings('Tailcoat', [(.805,0,.025,.203,.112),(.94,0,.026,.14,.084),(1.22,0,.023,.217,.111),
                      (1.30,0,.023,.152,.087)], 'jacket',.012)
    rings('Neck', [(1.27,0,0,.042,.044),(1.43,0,0,.047,.044)], 'brass',.005)
    head = rings('Instrument housing', [(1.38,0,0,.141,.107),(1.49,0,0,.238,.146),
                                (1.75,0,.02,.235,.145),(1.81,0,.025,.162,.11)], 'brass',.010)
    rings('Visor brim', [(1.751,.025,-.045,.268,.196),(1.790,.025,-.043,.262,.194)], 'shadow')
    def cap_section(row, sector, x, y, z):
        # Steer the profile as well as the frontal lean. A rear fold breaks the outline.
        if row == 1 and sector in (1, 2):
            y += .043
            z -= .024
        if row == 2:
            y += .067 if sector in (0, 1, 2) else .014
            z += .045 if sector == 1 else -.025 if sector == 3 else 0
        return x, y, z

    rings('Folded cap', [(1.78,.026,.022,.176,.126),(1.91,.068,.04,.134,.103),
                        (1.963,.088,.045,.09,.075)], 'jacket', .009, section=cap_section)
    rings('Cap band', [(1.79,.03,.02,.174,.123),(1.823,.042,.021,.168,.121)], 'red',0)
    plate('Collar graphic', [(-.074,-.084,1.26),(0,-.096,1.11),(.074,-.084,1.26)], 'ivory')

    # Paint a compact graphic directly onto the existing faceted curved head.
    size = 128
    image = bpy.data.images.new('Lookout | generated face', width=size, height=size, alpha=False)
    pixels = []
    # Byte image pixels are sRGB; Blender linearizes them at the texture node.
    tones = {k: tuple(int(v[i:i+2], 16) / 255 for i in (0, 2, 4)) + (1,) for k, v in {
        'base': 'df9d46', 'shade': '8c502d', 'panel': '3e344f',
        'eye': 'a6ecda', 'status': 'ad404d'}.items()}
    for iy in range(size):
        for ix in range(size):
            u, v = (ix+.5)/size, (iy+.5)/size
            tone = 'shade' if v > .77 else 'base'
            if .19 < u < .81 and .35 < v < .68:
                tone = 'panel'
            if .28 < u < .55 and .47 < v < .55:
                tone = 'eye'
            if ((u-.68)/.050)**2 + ((v-.51)/.069)**2 < 1:
                tone = 'status'
            pixels.extend(tones[tone])
    image.pixels.foreach_set(pixels)
    image.pack()
    head.data.materials.append(graphic_material('Lookout | graphic face', image=image))
    uv = head.data.uv_layers.new(name='Projected face graphic')
    mapped = 0
    for face in head.data.polygons:
        if face.normal.y < -.34:
            face.material_index = 1
            mapped += 1
            for loop in face.loop_indices:
                co = head.data.vertices[head.data.loops[loop].vertex_index].co
                uv.data[loop].uv = ((co.x+.24)/.48, (co.z-1.38)/.43)
    assert mapped > 1 and image.packed_file
    report = audit(parts)
    report['asset'] = 'Original static clockwork character'
    report['face_surface_polygons'] = mapped
    report['packed_generated_images'] = [image.name]
    report['contour_width_by_part_m'] = {o.name: o['shell_width_m'] for o in parts if 'shell_width_m' in o}
    cam = preview(parts, output / 'views', 480)

    # One matched camera scale for all diagnostics, with and without contour.
    center, extent = bounds(parts)
    for label, direction, hide_ink in [
        ('top', (0, 0, 1), False), ('elevated', (2, -4, 3), False),
        ('side_no_ink', (1, 0, 0), True), ('side_ink', (1, 0, 0), False),
    ]:
        for ob in parts:
            if ob.get('style_role') == 'outline':
                ob.hide_render = hide_ink
        cam.location = center + Vector(direction).normalized() * extent.length * 3
        cam.rotation_euler = (center - cam.location).to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = str(output / 'views' / f'{label}.png')
        bpy.ops.render.render(write_still=True)
    cam.location = center + Vector((4,-6,3)).normalized() * extent.length * 3
    cam.rotation_euler = (center - cam.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    (output / 'QA.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


if __name__ == '__main__':
    build(Path(sys.argv[sys.argv.index('--')+1]).resolve())

