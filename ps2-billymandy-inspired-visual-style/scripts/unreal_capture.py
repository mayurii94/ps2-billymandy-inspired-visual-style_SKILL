"""Run after import, or in the saved Preview level. Offscreen rendered comparison.
Capture is asynchronous; script ends after 180 ticks or an exception, not an endless waiter.
"""
import unreal,os,json,math,time
from pathlib import Path
SOURCE=Path(os.environ['STYLE_PROOF_DIR'])
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actor=next(a for a in actors.get_all_level_actors() if a.get_actor_label()=='StyleProof_Postbox')
origin,extent=actor.get_actor_bounds(False);span=extent*2;diagonal=math.sqrt(span.x**2+span.y**2+span.z**2)
direction=unreal.Vector(4,6,3);direction=direction/math.sqrt(61)
loc=origin+direction*diagonal*3
capture=actors.spawn_actor_from_class(unreal.SceneCapture2D,loc,unreal.MathLibrary.find_look_at_rotation(loc,origin))
c=capture.get_component_by_class(unreal.SceneCaptureComponent2D);c.set_editor_property('projection_type',unreal.CameraProjectionMode.ORTHOGRAPHIC);c.set_editor_property('ortho_width',diagonal*1.12)
c.set_editor_property('capture_every_frame',False);c.set_editor_property('capture_on_movement',False);c.set_editor_property('capture_source',unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR);c.set_editor_property('primitive_render_mode',unreal.SceneCapturePrimitiveRenderMode.PRM_USE_SHOW_ONLY_LIST);c.show_only_actor_components(actor)
flags=[]
for name in ['Tonemapper','EyeAdaptation','Bloom','MotionBlur','Fog','Atmosphere']:
 flag=unreal.EngineShowFlagsSetting();flag.show_flag_name=name;flag.enabled=False;flags.append(flag)
c.set_editor_property('show_flag_settings',flags)
rt=unreal.RenderingLibrary.create_render_target2d(actor,640,640,unreal.TextureRenderTargetFormat.RTF_RGBA8,unreal.LinearColor(0,0,0,0));rt.set_editor_property('target_gamma',2.2);c.set_editor_property('texture_target',rt)
unreal.EditorPythonScripting.set_keep_python_script_alive(True)
state={'ticks':0,'started':time.monotonic()}
def tick(dt):
 try:
  state['ticks']+=1
  if state['ticks'] in (60,120,180):
   c.capture_scene();unreal.RenderingLibrary.export_render_target(actor,rt,str(SOURCE),'unreal_%03d.png'%state['ticks'])
  if state['ticks']>=180 or time.monotonic()-state['started']>180:
   (SOURCE/'UNREAL_CAPTURE_SETTINGS.json').write_text(json.dumps({'location':[loc.x,loc.y,loc.z],'ortho_width_cm':diagonal*1.12,'disabled_show_flags':[f.show_flag_name for f in flags],'target_gamma':2.2,'ticks':state['ticks'],'note':'Technical capture; judge and quantify matching separately'},indent=2))
   unreal.unregister_slate_post_tick_callback(handle);unreal.EditorPythonScripting.set_keep_python_script_alive(False)
 except Exception:
  unreal.unregister_slate_post_tick_callback(handle);unreal.EditorPythonScripting.set_keep_python_script_alive(False);raise
handle=unreal.register_slate_post_tick_callback(tick)
