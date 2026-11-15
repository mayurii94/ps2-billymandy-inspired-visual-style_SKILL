"""Original crooked postbox proof, built from new geometry. Run in background factory startup.
blender --background --factory-startup --python build_mailbox.py -- OUTPUT_DIRECTORY
Refuses to replace an existing blend. No game geometry or texture is copied.
"""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from style_core import graphic_material,outline_shell,preview,audit,export_static
OUT=Path(sys.argv[sys.argv.index('--')+1]).resolve();OUT.mkdir(parents=True,exist_ok=True)
if (OUT/'Crooked_Postbox.blend').exists():raise FileExistsError('Choose a new output folder to preserve the previous revision')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
# Four original palette tiles in a 128 square atlas. Broad painted bands are design choices.
im=bpy.data.images.new('Postbox_Atlas',128,128,alpha=True)
palette=[(.22,.52,.48),(.85,.81,.57),(.63,.18,.23),(.39,.32,.43)]
pix=[]
for y in range(128):
 for x in range(128):
  tile=(x//64)+2*(y//64);c=palette[tile];u=(x%64)/63;v=(y%64)/63
  factor=1
  if tile==0:factor=.86+.14*v
  if tile==3:factor=.80+.20*(.5+.5*math.sin(u*22+v*3))
  pix.extend([*(a*factor for a in c),1])
im.pixels.foreach_set(pix);im.filepath_raw=str(OUT/'Postbox_Atlas.png');im.file_format='PNG';im.save();im.pack()
mat=graphic_material('M_Postbox_Atlas',image=im);ink=graphic_material('M_Postbox_Ink',color=(.003,.002,.005,1));ink['style_role']='ink'
objects=[]
def mesh(name,verts,faces,tile,outline=.025):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);me.materials.append(mat if tile>=0 else ink)
 uv=me.uv_layers.new(name='UVMap');lo=Vector([min(v[i] for v in verts) for i in range(3)]);hi=Vector([max(v[i] for v in verts) for i in range(3)])
 for poly in me.polygons:
  axes=sorted(range(3),key=lambda i:abs(poly.normal[i]))[:2]
  for li in poly.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;u=(co[axes[0]]-lo[axes[0]])/max(hi[axes[0]]-lo[axes[0]],.001);v=(co[axes[1]]-lo[axes[1]])/max(hi[axes[1]]-lo[axes[1]],.001)
   uv.data[li].uv=((max(tile,0)%2+.08+.84*u)/2,(max(tile,0)//2+.08+.84*v)/2)
 objects.append(ob)
 if outline:objects.append(outline_shell(ob,ink,outline))
 return ob
def prism(name,profile,y0,y1,tile,outline=.025):
 # x,z profile is counterclockwise; front points toward -Y.
 n=len(profile);vs=[(x,y,z) for y in (y0,y1) for x,z in profile];fs=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]+[(i,(i+n)% (2*n),((i+1)%n)+n,(i+1)%n) for i in range(n)]
 return mesh(name,vs,fs,tile,outline)
prism('Bent_Post',[(-.11,.04),(.09,.04),(.04,.47),(.14,.95),(-.04,1.02),(-.16,.48)],-.065,.075,3)
prism('Wide_Foot',[(-.26,0),(.26,0),(.21,.09),(-.19,.12)],-.18,.18,3)
body=[(-.38,.89),(.38,.89),(.43,1.20),(.30,1.47),(.06,1.57),(-.22,1.50),(-.43,1.27)]
prism('Mailbox_Body',body,-.33,.43,0,.028)
door=[(-.33,.94),(.33,.94),(.36,1.19),(.25,1.41),(.055,1.49),(-.18,1.43),(-.35,1.25)]
prism('Cream_Door',door,-.355,-.338,1,.012)
prism('Mail_Slot',[(-.23,1.22),(.23,1.22),(.23,1.265),(-.23,1.265)],-.371,-.359,-1,0)
prism('Door_Handle',[(-.09,1.02),(.10,1.02),(.10,1.07),(-.09,1.07)],-.40,-.365,0,.008)
# Arrow flag: deliberately different silhouette from any reference character or grill.
prism('Flag',[ (.30,1.37),(.34,1.37),(.40,1.81),(.69,1.83),(.60,1.94),(.38,1.92)],.02,.07,2,.012)
# Ink hinges and graphic seam are explicit geometry, independent of silhouette shell.
for z in (1.00,1.31):prism('Hinge_'+str(z),[(-.365,z),(-.31,z),(-.31,z+.055),(-.365,z+.055)],-.374,-.358,-1,0)
for o in objects:
 o['asset_original']=True;o['style_baseline']='v1.0';o['asset_family']='prop'
report=audit(objects);report['originality']='All geometry and atlas generated here; references are read only';report['shell_widths_m']=[.008,.012,.025,.028]
export_static(objects,OUT/'export','SM_Crooked_Postbox');preview(objects,OUT/'previews')
(OUT/'QA.json').write_text(json.dumps(report,indent=2))
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='MATERIAL'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Crooked_Postbox.blend'))
print('POSTBOX_COMPLETE',json.dumps(report),flush=True)
