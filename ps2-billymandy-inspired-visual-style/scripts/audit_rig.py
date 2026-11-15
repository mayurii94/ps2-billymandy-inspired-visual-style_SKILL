"""Read-only on disk, evaluate one armature and deliberately bend selected joints.

blender --background MODEL.blend --python-exit-code 1 --python audit_rig.py -- RIG REPORT.json BONE [BONE ...]
"""
import argparse
import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Quaternion


def snapshot(meshes):
    bpy.context.view_layer.update()
    graph = bpy.context.evaluated_depsgraph_get()
    return {o.name: [v.co.copy() for v in o.evaluated_get(graph).data.vertices] for o in meshes}


def analyze(rig, bone_names):
    scene = bpy.context.scene
    if rig.type != 'ARMATURE' or rig.name not in scene.objects:
        raise ValueError(f"{rig.name} is not an armature in active scene {scene.name}")
    meshes = [o for o in scene.objects if o.type == 'MESH' and not o.hide_render and
              any(m.type == 'ARMATURE' and m.object == rig for m in o.modifiers)]
    if not meshes:
        raise ValueError('No visible meshes with a modifier targeting the rig')
    invalid_bones = set(bone_names).difference(rig.pose.bones.keys())
    if invalid_bones:
        raise ValueError(f'Unknown bones: {sorted(invalid_bones)}')
    weights = []
    for o in meshes:
        deform_ids = {g.index for g in o.vertex_groups
                      if g.name in rig.data.bones and rig.data.bones[g.name].use_deform}
        sums = [sum(g.weight for g in v.groups if g.group in deform_ids) for v in o.data.vertices]
        weights.append({'mesh': o.name, 'unweighted': sum(w < 1e-8 for w in sums),
                        'max_sum_error': max((abs(w-1) for w in sums), default=0),
                        'active_modifiers': sum(m.show_viewport and m.type == 'ARMATURE' and m.object == rig
                                                for m in o.modifiers)})
    by_name = {o.name: o for o in meshes}
    shell_pairs = []
    for shell in meshes:
        if not shell.name.endswith('_Ink'):
            continue
        body = by_name.get(shell.name[:-4])
        if body is None or len(body.data.vertices) != len(shell.data.vertices):
            continue
        def influences(o, v):
            return {o.vertex_groups[g.group].name: g.weight for g in v.groups if g.weight > 1e-8}
        mismatches = sum(influences(body, a) != influences(shell, b)
                         for a,b in zip(body.data.vertices, shell.data.vertices))
        shell_pairs.append({'surface': body.name, 'outline': shell.name, 'different_weight_vertices': mismatches})
    data = rig.animation_data
    action = data.action if data else None
    action_info = {
        'name': action.name if action else None,
        'slot': data.action_slot.identifier if action and data.action_slot else None,
        'installed_ik_constraints': sum(c.type == 'IK' for p in rig.pose.bones for c in p.constraints),
    }
    playback = None
    if action:
        start, end = map(int, action.frame_range)
        scene.frame_set(start)
        first = snapshot(meshes)
        samples = sorted({start+(end-start)//4, (start+end)//2, end})
        movement = {}
        for frame in samples:
            scene.frame_set(frame)
            sample = snapshot(meshes)
            movement[str(frame)] = max((a-b).length for k in first for a,b in zip(first[k],sample[k]))
        playback = {'start': start, 'end': end, 'max_vertex_motion_from_start': movement}
        data.action = None
    if data:
        data.use_nla = False
    rig.data.pose_position = 'POSE'
    for bone in rig.pose.bones:
        bone.matrix_basis = Matrix.Identity(4)
        bone.rotation_mode = 'QUATERNION'
    rest = snapshot(meshes)
    probes = []
    for name in bone_names:
        bone = rig.pose.bones[name]
        bone.rotation_quaternion = Quaternion((1,0,0), math.radians(60))
        posed = snapshot(meshes)
        max_motion = max((a-b).length for k in rest for a,b in zip(rest[k],posed[k]))
        moved = sum((a-b).length > 1e-5 for k in rest for a,b in zip(rest[k],posed[k]))
        finite = all(math.isfinite(c) for coords in posed.values() for v in coords for c in v)
        probes.append({'bone': name, 'local_axis': 'X', 'degrees': 60,
                       'max_motion': max_motion, 'moved_vertices': moved, 'finite': finite})
        bone.rotation_quaternion = Quaternion()
    return {'rig': rig.name, 'bones': len(rig.data.bones), 'action': action_info, 'playback': playback,
            'weights': weights, 'paired_shells': shell_pairs, 'manual_fk_probes': probes,
            'scope': 'Geometry and FK probes. Inspect posed renders, control interaction, constraints and seams separately.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rig')
    parser.add_argument('report', type=Path)
    parser.add_argument('bones', nargs='+')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    result = analyze(bpy.data.objects[args.rig], args.bones)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2), encoding='utf-8')

