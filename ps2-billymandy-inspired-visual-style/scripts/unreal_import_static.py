"""Unreal editor Python. Set STYLE_PROOF_DIR to a build_mailbox output directory.
Imports only into /Game/StyleProof/Postbox. Existing output is refused.
Run with -ExecutePythonScript=... in an isolated UE5.9 project.
"""
import unreal,os,json
from pathlib import Path
SOURCE=Path(os.environ['STYLE_PROOF_DIR']);DEST='/Game/StyleProof/Postbox_v2'
if unreal.EditorAssetLibrary.does_asset_exist(DEST+'/SM_Crooked_Postbox'):raise RuntimeError('Output exists; use fresh isolated project or explicitly version the destination')
tools=unreal.AssetToolsHelpers.get_asset_tools();mel=unreal.MaterialEditingLibrary
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
unreal.SystemLibrary.execute_console_command(world,'Interchange.FeatureFlags.Import.FBX 0')
def import_asset(path,name,options=None):
 t=unreal.AssetImportTask();t.filename=str(path);t.destination_path=DEST;t.destination_name=name;t.automated=True;t.save=True;t.replace_existing=False
 if options:t.options=options
 tools.import_asset_tasks([t]);objs=t.get_objects();assert objs,(path,t.imported_object_paths);return objs[0]
tex=import_asset(SOURCE/'Postbox_Atlas.png','T_Postbox');tex.set_editor_property('srgb',True);tex.set_editor_property('filter',unreal.TextureFilter.TF_BILINEAR)
ui=unreal.FbxImportUI();ui.set_editor_property('import_mesh',True);ui.set_editor_property('import_as_skeletal',False);ui.set_editor_property('import_materials',False);ui.set_editor_property('import_textures',False);ui.set_editor_property('automated_import_should_detect_type',False);ui.set_editor_property('mesh_type_to_import',unreal.FBXImportType.FBXIT_STATIC_MESH)
sd=ui.static_mesh_import_data;sd.combine_meshes=True;sd.auto_generate_collision=False;sd.import_uniform_scale=1;sd.convert_scene=True;sd.convert_scene_unit=True;sd.normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
mesh=import_asset(SOURCE/'export/SM_Crooked_Postbox.fbx','SM_Crooked_Postbox',ui)
materials={}
for name in ['M_Postbox_Atlas','M_Postbox_Ink']:
 m=tools.create_asset(name,DEST,unreal.Material,unreal.MaterialFactoryNew());m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT);m.set_editor_property('two_sided',False)
 if name.endswith('Atlas'):
  n=mel.create_material_expression(m,unreal.MaterialExpressionTextureSample,0,0);n.texture=tex;socket='RGB'
 else:
  n=mel.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,0,0);n.constant=unreal.LinearColor(.003,.002,.005,1);socket=''
 assert mel.connect_material_property(n,socket,unreal.MaterialProperty.MP_EMISSIVE_COLOR);mel.recompile_material(m);materials[name]=m
slots=[]
for i,s in enumerate(mesh.static_materials):
 name=str(s.material_slot_name);assert name in materials,name;mesh.set_material(i,materials[name]);slots.append(name)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actor=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(0,0,0));actor.set_actor_label('StyleProof_Postbox');actor.static_mesh_component.set_static_mesh(mesh)
b=mesh.get_bounding_box();dims=b.max-b.min
expected=json.loads((SOURCE/'export/manifest.json').read_text())['audit']['bounds_m']
# FBX conversion can permute horizontal axes. Height and sorted horizontal spans are invariant.
actual=[dims.x,dims.y,dims.z];error=max(abs(a-b*100) for a,b in zip(sorted(actual),sorted(expected)))
assert error<.1,(actual,expected,error)
unreal.EditorAssetLibrary.save_directory(DEST,only_if_is_dirty=False,recursive=True)
assert unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/StyleProof/Preview')
report={'engine':unreal.SystemLibrary.get_engine_version(),'asset':mesh.get_path_name(),'dimensions_cm':actual,'scale_error_cm':error,'material_slots':slots,'two_sided':False,'visual_validation':'pending rendered comparison','skeletal_validation':'not tested'}
(SOURCE/'UNREAL_IMPORT_REPORT.json').write_text(json.dumps(report,indent=2));unreal.log('STYLE_IMPORT_SUCCESS '+json.dumps(report))
exec(compile((Path(__file__).parent/'unreal_capture.py').read_text(),str(Path(__file__).parent/'unreal_capture.py'),'exec'))
