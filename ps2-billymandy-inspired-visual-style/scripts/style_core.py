"""Reusable Blender 5.1 production helpers. Coordinates: metres, +Z up, face -Y.
These are an adaptation of observed reconstructions, not a PS2 shader emulator.
"""
import bpy, math, json
from pathlib import Path
from mathutils import Vector

def graphic_material(name, image=None, color=(1,1,1,1), vertex_color=None):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.use_backface_culling=True
    n=m.node_tree.nodes;l=m.node_tree.links;n.clear()
    em=n.new('ShaderNodeEmission');em.inputs['Color'].default_value=color
    if image:
        tex=n.new('ShaderNodeTexImage');tex.image=image;tex.interpolation='Linear';l.new(tex.outputs['Color'],em.inputs['Color'])
    if vertex_color:
        attr=n.new('ShaderNodeVertexColor');attr.layer_name=vertex_color
        mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1
        mul.inputs[1].default_value=color
        if image:l.new(tex.outputs['Color'],mul.inputs[1])
        l.new(attr.outputs['Color'],mul.inputs[2]);l.new(mul.outputs[0],em.inputs['Color'])
    # Render engines do not all honor the viewport backface toggle. Explicitly cull backs.
    geom=n.new('ShaderNodeNewGeometry');transparent=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');out=n.new('ShaderNodeOutputMaterial')
    l.new(geom.outputs['Backfacing'],mix.inputs[0]);l.new(em.outputs[0],mix.inputs[1]);l.new(transparent.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
    m['style_role']='unlit_graphic';return m

def outline_shell(obj, ink, thickness):
    """Static closed mesh shell. For rigged meshes copy weights and preserve modifier order."""
    mesh=obj.data.copy();mesh.name=obj.name+'_InkMesh'
    for v in mesh.vertices:v.co+=v.normal*thickness
    for p in mesh.polygons:p.flip()
    mesh.materials.clear();mesh.materials.append(ink)
    for p in mesh.polygons:p.material_index=0
    shell=bpy.data.objects.new(obj.name+'_Ink',mesh);bpy.context.collection.objects.link(shell);shell.matrix_world=obj.matrix_world.copy();shell['style_role']='outline';shell['shell_width_m']=thickness
    return shell

def bounds(objects):
    bpy.context.view_layer.update();points=[o.matrix_world@Vector(v) for o in objects for v in o.bound_box]
    lo=Vector([min(p[i] for p in points) for i in range(3)]);hi=Vector([max(p[i] for p in points) for i in range(3)])
    return (lo+hi)/2,hi-lo

def preview(objects, folder, size=640):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);s=bpy.context.scene
    center,extent=bounds(objects);cam=bpy.data.objects.new('Style_QA_Camera',bpy.data.cameras.new('Style_QA_Camera'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=extent.length*1.12
    s.render.engine='BLENDER_EEVEE';s.render.resolution_x=size;s.render.resolution_y=size;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    if hasattr(s,'eevee'):s.eevee.taa_render_samples=16
    for label,d in [('front',(0,-1,0)),('side',(1,0,0)),('rear',(0,1,0)),('angle',(4,-6,3))]:
        cam.location=center+Vector(d).normalized()*extent.length*3;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(folder/(label+'.png'));bpy.ops.render.render(write_still=True)
    return cam

def audit(objects, check_textures=True):
    data={'blender_version':bpy.app.version_string,'objects':[],'finite':True,'missing_textures':[]}
    for o in objects:
        if o.type!='MESH':continue
        m=o.data;m.calc_loop_triangles()
        finite=all(math.isfinite(x) for v in m.vertices for x in v.co);data['finite'] &= finite
        data['objects'].append({'name':o.name,'vertices':len(m.vertices),'triangles':len(m.loop_triangles),'uv':len(m.uv_layers),'role':o.get('style_role','surface'),'scale':list(o.scale)})
        for mat in m.materials:
            if mat and mat.use_nodes:
                for n in mat.node_tree.nodes:
                    # Reopened packed images load lazily: has_data alone is a false failure.
                    if n.type=='TEX_IMAGE' and (not n.image or len(n.image.pixels)==0):data['missing_textures'].append(mat.name)
    _,e=bounds(objects);data['bounds_m']=list(e)
    assert data['finite'] and (not check_textures or not data['missing_textures']),data
    return data

def export_static(objects, folder, name):
    """FBX carries mesh/UV/material slots. Rebuild shaders in Unreal explicitly."""
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.export_scene.fbx(filepath=str(folder/(name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,path_mode='AUTO')
    (folder/'manifest.json').write_text(json.dumps({'name':name,'metres_per_blender_unit':1,'blender_front':'-Y','blender_up':'+Z','material_transfer':'Rebuild unlit atlas and single-sided black material; no automatic shader equivalence','audit':audit(objects)},indent=2))
