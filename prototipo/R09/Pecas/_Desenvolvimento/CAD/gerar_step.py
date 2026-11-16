"""Executa as mesmas definicoes geometricas da versao Fusion usando CadQuery."""
import ast,json,pathlib,math
from dataclasses import dataclass
import cadquery as cq
import vtk

ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'Exportados'
OUT.mkdir(exist_ok=True)
PARTS=[]
STEPS=[]
NEW,CUT,JOIN=0,1,2
PALETTE={'impresso':(27,142,153),'mdf':(172,130,83),'aco':(169,183,195),'motor':(48,52,61),'correia':(36,39,46),'papel':(242,241,230),'servo':(43,88,186),'caneta':(232,149,44),'parafuso':(85,91,102)}

@dataclass
class Part:
    name:str
    kind:str
    note:str
    shape:object=None
    stage:int=0

def component(name,kind='impresso',note=''):
    p=Part(name,kind,note,stage=len(STEPS)+1)
    PARTS.append(p)
    return p

def apply(p,shape,op):
    if p.shape is None:
        if op==CUT: raise ValueError('Corte sem corpo '+p.name)
        p.shape=shape
    elif op==CUT:
        before=p.shape.Volume()
        p.shape=p.shape.cut(shape).clean()
        if abs(before-p.shape.Volume())<1e-6: raise ValueError('Corte vazio '+p.name)
    elif op==JOIN:
        p.shape=p.shape.fuse(shape).clean()
    else:
        p.shape=cq.Compound.makeCompound([p.shape,shape])
    return p.shape

def box(p,x,y,z,dx,dy,dz,op=NEW,label=''):
    return apply(p,cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z)),op)

def cylinder(p,x,y,z,dia,length,axis='z',op=NEW,label=''):
    return apply(p,cq.Solid.makeCylinder(dia/2,length,cq.Vector(x,y,z),cq.Vector(*{'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}[axis])),op)


def cone_z(p,x,y,z,d1,d2,height,op=NEW,label='Cone'):
    return apply(p,cq.Solid.makeCone(d1/2,d2/2,height,cq.Vector(x,y,z)),op)


def prism_x(p,x,points,thickness,op=JOIN,label=''):
    wire=cq.Wire.makePolygon([cq.Vector(x,y,z) for y,z in points],close=True)
    return apply(p,cq.Solid.extrudeLinear(wire,[],cq.Vector(thickness,0,0)),op)

def prism_y(p,y,points,thickness,op=JOIN,label=''):
    wire=cq.Wire.makePolygon([cq.Vector(x,y,z) for x,z in points],close=True)
    return apply(p,cq.Solid.extrudeLinear(wire,[],cq.Vector(0,thickness,0)),op)

def finish(*a): pass

def belt(name,axis,a,b,center,z):
    p=component(name,'correia','Envelope continuo; dentes e ancoragens finais pendentes.')
    def capsule(r):
        if axis=='y':
            s=cq.Solid.makeBox(2*r,b-a,6,cq.Vector(center-r,a,z))
            ends=[(center,a),(center,b)]
        else:
            s=cq.Solid.makeBox(b-a,2*r,6,cq.Vector(a,center-r,z))
            ends=[(a,center),(b,center)]
        for x,y in ends: s=s.fuse(cq.Solid.makeCylinder(r,6,cq.Vector(x,y,z)))
        return s
    p.shape=capsule(7.066).cut(capsule(5.666)).clean()
    gap=cq.Solid.makeBox(3,4,8,cq.Vector(center-8,238,z-1)) if axis=='y' else cq.Solid.makeBox(4,3,8,cq.Vector(208,center-8,z-1))
    p.shape=p.shape.cut(gap).clean()
    return p

# Load function definitions only: no adsk dependency and no Fusion side effects.
src=ROOT/'Fusion_A4_R02'/'Fusion_A4_R02.py'
tree=ast.parse(src.read_text(encoding='utf-8'))
defs=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[])
ns=dict(globals())
exec(compile(defs,str(src),'exec'),ns)
for key in ['component','box','cylinder','finish','belt','prism_x','prism_y','cone_z']:
    ns[key]=globals()[key]

plan=[('01 Base e pes','base'),('02 Acionamento Y','transmission_y'),('03 Ponte Y','bridge'),('04 Guias Y','guides_y'),('05 Carro X','carriage'),('06 Guias X','guides_x'),('07 Acionamento X','transmission_x'),('08 Mesa elevada','bed'),('09 Cabecote','penhead'),('10 Ferragens ilustrativas','hardware'),('11 Papel e sensores','references')]
for title,fn in plan:
    print(title,flush=True)
    start=len(PARTS)
    ns[fn]()
    STEPS.append({'etapa':title,'componentes':[p.name for p in PARTS[start:]]})

assembly=cq.Assembly(name='Robo_A4_R09')
invalid=[]
for p in PARTS:
    if not p.shape.isValid() or len(p.shape.Solids())!=1:
        invalid.append({'componente':p.name,'solidos':len(p.shape.Solids()),'valido':p.shape.isValid()})
    rgb=PALETTE[p.kind]
    assembly.add(p.shape,name=p.name,color=cq.Color(*(v/255 for v in rgb)))
assembly.export(str(OUT/'Robo_A4_R09_Montagem.step'))

# Mesh exports are prototypes: do not call them released production parts.
stldir=OUT/'STL_ESTUDO'
stldir.mkdir(exist_ok=True)
for p in PARTS:
    if p.kind=='impresso':
        bb=p.shape.BoundingBox()
        local=p.shape.translate((-bb.xmin,-bb.ymin,-bb.zmin))
        cq.exporters.export(local,str(stldir/(p.name+'.stl')),tolerance=.08,angularTolerance=.15)

# Broad phase bounding-box check, then exact common-volume test.
interferences=[]
for i,p in enumerate(PARTS):
    if p.kind in ['parafuso','correia','papel'] or '_Alavanca_' in p.name: continue
    a=p.shape.BoundingBox()
    for q in PARTS[i+1:]:
        if q.kind in ['parafuso','correia','papel'] or '_Alavanca_' in q.name: continue
        b=q.shape.BoundingBox()
        if min(a.xmax,b.xmax)-max(a.xmin,b.xmin)<=.02 or min(a.ymax,b.ymax)-max(a.ymin,b.ymin)<=.02 or min(a.zmax,b.zmax)-max(a.zmin,b.zmin)<=.02: continue
        vol=p.shape.intersect(q.shape).Volume()
        if vol>.5: interferences.append({'a':p.name,'b':q.name,'volume_mm3':round(vol,3)})
report={'solidos_invalidos':invalid,'interferencias_estaticas':interferences,'componentes':len(PARTS),'etapas':STEPS,'aviso':'Alavancas flexiveis livres excluidas das colisoes rigidas: contato esperado nas rampas de homing, validar deformacao fisicamente. Teste estatico na posicao exibida. Nao valida curso completo, forcas ou componentes comprados.'}
moving=[p for p in PARTS if p.stage in [3,5,6,7,9] and p.kind not in ['correia','parafuso'] and '_Alavanca_' not in p.name]
fixed=[p for p in PARTS if p.stage in [1,2,4,8] and p.kind not in ['correia','parafuso'] and '_Alavanca_' not in p.name]
motion=[]
for dx,dy in [(-110,-146),(120,-146),(-110,171),(120,171),(0,0)]:
    hits=[]
    for p in moving:
        s=p.shape.translate((dx if p.stage in [5,9] else 0,dy,0))
        a=s.BoundingBox()
        for q in fixed:
            b=q.shape.BoundingBox()
            if min(a.xmax,b.xmax)-max(a.xmin,b.xmin)<=.02 or min(a.ymax,b.ymax)-max(a.ymin,b.ymin)<=.02 or min(a.zmax,b.zmax)-max(a.zmin,b.zmin)<=.02: continue
            vol=s.intersect(q.shape).Volume()
            if vol>.5:hits.append({'movel':p.name,'fixo':q.name,'volume_mm3':round(vol,3)})
    motion.append({'ponta_xy_mm':[210+dx,166+dy],'interferencias':hits})
report['amostras_movimento']=motion
(OUT/'validacao_cadquery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'componentes_cadquery.json').write_text(json.dumps([{'nome':p.name,'tipo':p.kind,'etapa':p.stage,'nota':p.note,'volume_mm3':p.shape.Volume()} for p in PARTS],ensure_ascii=False,indent=2),encoding='utf-8')

def actor(p):
    verts,tri=p.shape.tessellate(.35,.25)
    points=vtk.vtkPoints()
    for v in verts: points.InsertNextPoint(v.x,v.y,v.z)
    cells=vtk.vtkCellArray()
    for ids in tri:
        cell=vtk.vtkTriangle()
        for j,k in enumerate(ids): cell.GetPointIds().SetId(j,k)
        cells.InsertNextCell(cell)
    mesh=vtk.vtkPolyData(); mesh.SetPoints(points); mesh.SetPolys(cells)
    mapper=vtk.vtkPolyDataMapper(); mapper.SetInputData(mesh)
    a=vtk.vtkActor(); a.SetMapper(mapper)
    a.GetProperty().SetColor(*(v/255 for v in PALETTE[p.kind]))
    a.GetProperty().SetInterpolationToPhong()
    return a

ren=vtk.vtkRenderer(); ren.SetBackground(.94,.955,.97)
window=vtk.vtkRenderWindow(); window.SetOffScreenRendering(1); window.AddRenderer(ren); window.SetSize(1400,1100)
actors=[]
for p in PARTS:
    a=actor(p);ren.AddActor(a);actors.append(a)
cam=ren.GetActiveCamera(); cam.SetPosition(850,-850,800); cam.SetFocalPoint(225,245,55);cam.SetViewUp(0,0,1);cam.ParallelProjectionOn();cam.SetParallelScale(370)
def save(name):
    ren.ResetCameraClippingRange()
    window.Render(); capture=vtk.vtkWindowToImageFilter();capture.SetInput(window);capture.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(OUT/name));writer.SetInputConnection(capture.GetOutputPort());writer.Write()
save('Montagem_A4_R02.png')
for index in [2,4,7,9,11]:
    for p,a in zip(PARTS,actors): a.SetVisibility(p.stage<=index)
    save('Etapa_%02d.png'%index)
print(json.dumps({'componentes':len(PARTS),'invalidos':invalid,'interferencias':interferences,'amostras_movimento':motion},ensure_ascii=False),flush=True)
