from pathlib import Path
from types import SimpleNamespace
import json,math
cad=(Path(__file__).resolve().parent.parent / 'CAD');f=cad/'gerar_step.py';ns={'__file__':str(f),'__name__':'full_audit'}
exec(compile(f.read_text(encoding='utf-8').split('assembly=cq.Assembly')[0],str(f),'exec'),ns)
cq=ns['cq'];parts=ns['PARTS'];named={p.name:p for p in parts};extra=[]
axisvec={'x':(1,0,0),'y':(0,1,0),'z':(0,0,1)}
def cyl(xyz,d,l,a='z'):return cq.Solid.makeCylinder(d/2,l,cq.Vector(*xyz),cq.Vector(*axisvec[a]))
def shift(xyz,a,t):p=list(xyz);p['xyz'.index(a)]+=t;return p
def add(name,shape,g=0,kind='ferragem'):extra.append(SimpleNamespace(name='AUD_'+name,shape=shape,group=g,kind=kind,stage=0))
def ring(name,xyz,d,od,t,a='z',g=0):add(name,cyl(xyz,od,t,a).cut(cyl(xyz,d+.2,t,a)),g)
def nut(name,xyz,d,a='z',g=0,square=False):
    flats={2:4,2.5:5,3:5.5,4:7,5:8}[d];t={2:1.6,2.5:2,3:2.4,4:3.2,5:4}[d]
    if square:
        size=[flats]*3;size['xyz'.index(a)]=t;org=[v-flats/2 for v in xyz];org['xyz'.index(a)]=xyz['xyz'.index(a)]
        shape=cq.Solid.makeBox(*size,cq.Vector(*org));t=2.4 if d==3 else 2.2
        size['xyz'.index(a)]=t;shape=cq.Solid.makeBox(*size,cq.Vector(*org))
    else:shape=cyl(xyz,flats/math.cos(math.pi/6),t,a)
    add(name,shape.cut(cyl(xyz,d+.1,t,a)),g)
def washer(name,xyz,d,a='z',g=0,od=None,t=None):ring(name,xyz,d,od or {2:5,2.5:6,3:7,4:9,5:10}[d],t or {.0:0,2:.3,2.5:.5,3:.5,4:.8,5:1}[d],a,g)
def bolt(name,xyz,d,l,a='z',end=True,g=0,head=True):
    sh=cyl(xyz,d,l,a)
    if head:sh=sh.fuse(cyl(shift(xyz,a,l if end else -.75*d),1.8*d,.75*d,a))
    add(name,sh,g)
def assembly(name,x,y,z,d,l,top,bottom,g=0,a='z',square=False):
    # New missing bolt, top washer and bottom nut/washer, given the washer bearing faces.
    bolt(name,[x,y,z],d,l,a,True,g)
    washer(name+'_Wtop',shift([x,y,z],a,top-z),d,a,g)
    washer(name+'_Wbot',shift([x,y,z],a,bottom-z),d,a,g)
    nut(name+'_N',shift([x,y,z],a,bottom-z-{2:1.6,2.5:2,3:2.4,4:3.2,5:4}[d]),d,a,g,square)
# Existing fixed M4 fasteners.
for x in [80,370]:
    for y in [50,450]:
        washer(f'peWT{x}{y}',[x,y,15],4);washer(f'peWB{x}{y}',[x,y,-30],4);nut(f'peN{x}{y}',[x,y,-33.2],4)
for x in [20,40,410,430]:
    for y in [25,475]:
        washer(f'guiaWT{x}{y}',[x,y,60],4);washer(f'guiaWB{x}{y}',[x,y,-.8],4);nut(f'guiaN{x}{y}',[x,y,-4],4)
for x,y in [(90,7.5),(225,7.5),(360,7.5),(90,492.5),(360,492.5)]:
    washer(f'mesaWT{x}{y}',[x,y,77],4);washer(f'mesaWB{x}{y}',[x,y,-.8],4);nut(f'mesaN{x}{y}',[x,y,-4],4)
for x in [187,263]:
    for y in [462,474]:
        washer(f'motorYWT{x}{y}',[x,y,21],4);washer(f'motorYWB{x}{y}',[x,y,-.8],4);nut(f'motorYN{x}{y}',[x,y,-4],4)
for x in [13,47,403,437]:
    for y in [225,235,245]:
        washer(f'lateralWT{x}{y}',[x,y,129],4,g=1);washer(f'lateralWB{x}{y}',[x,y,20.4],4,g=1);nut(f'lateralN{x}{y}',[x,y,17.2],4,g=1)
# Housing, motor faces and missing carriage/head fixations.
for y in [19,45]:assembly(f'housingY{y}',55,y,-5.5,3,25,19,-.5)
for x,y,z,g in [(225,485,21,0),(425,310,129,1)]:
    for dx in [-15.5,15.5]:
        for dy in [-15.5,15.5]:
            bolt(f'motor{x}{dx}{dy}',[x+dx,y+dy,z-9.5],3,10,g=g);washer(f'motorW{x}{dx}{dy}',[x+dx,y+dy,z],3,g=g)
for x,y in [(202,244),(218,244),(196,254),(224,254),(202,224),(218,224)]:assembly(f'carro{x}{y}',x,y,95.5,3,40,135,102.5,2)
# Belt clamps.
for y in [215,230,250,265]:
    washer(f'ancYWT{y}',[224,y,41],3,g=1);washer(f'ancYWB{y}',[224,y,19.5],3,g=1);nut(f'ancYN{y}',[224,y,17.1],3,g=1)
for y in [221,236,244,259]:
    washer(f'capYW1{y}',[210.5,y,37],3,'x',1);washer(f'capYW2{y}',[228.5,y,37],3,'x',1);nut(f'capYN{y}',[229,y,37],3,'x',1)
for x in [199,221]:assembly(f'ancX{x}',x,309,120.5,3,30,150,126.5,2)
for x in [205,215]:
    bolt(f'capX{x}',[x,295.5,146],3,25,'y',False,2);washer(f'capXW1{x}',[x,295.5,146],3,'y',2);washer(f'capXW2{x}',[x,313.5,146],3,'y',2);nut(f'capXN{x}',[x,314,146],3,'y',2)
# Servo and endstop hardware.
for x in [243,272]:
    bolt(f'servo{x}',[x,175.2,112],2,12,'y',False,2);washer(f'servoW1{x}',[x,175.2,112],2,'y',2);washer(f'servoW2{x}',[x,183,112],2,'y',2);nut(f'servoN{x}',[x,183.3,112],2,'y',2)
for x in [29.15,35.65]:
    bolt(f'switchX{x}',[x,251.7,106.2],2,17,'y',False,1);washer(f'switchXW1{x}',[x,251.7,106.2],2,'y',1);washer(f'switchXW2{x}',[x,262,106.2],2,'y',1);nut(f'switchXN{x}',[x,262.3,106.2],2,'y',1)
for y in [28.15,34.65]:
    bolt(f'switchY{y}',[50,y,25.2],2,20,'x',False);washer(f'switchYW1{y}',[50,y,25.2],2,'x');washer(f'switchYW2{y}',[61,y,25.2],2,'x');nut(f'switchYN{y}',[61.3,y,25.2],2,'x')
# Roller retainers and heat-set inserts; only installation interference is permitted explicitly.
pressfit=set()
for x,side in [(30,'E'),(420,'D')]:
    for xx in [x-13,x+13]:
        for z in [34,60]:
            washer(f'capLM12W{xx}{z}',[xx,294,z],3,'y',1);nut(f'capLM12N{xx}{z}',[xx,280.05,z],3,'y',1,True)
for end in [172,245]:
    for y in [238,250]:
        for z in [108,122]:
            washer(f'capLM8W{end}{y}{z}',[171.5 if end==172 else 248,y,z],3,'x',2)
            name=f'insertX{end}{y}{z}';ring(name,[175 if end==172 else 238.5,y,z],3,4.6,6,'x',2);pressfit.add(frozenset(['AUD_'+name,'05_Carro_X']))
for x in [223,231]:
    bolt(f'supportServoBolt{x}',[x,194,121.5],3,20,g=2)
    washer(f'supportServoWT{x}',[x,194,141],3,g=2);washer(f'supportServoWB{x}',[x,194,126.5],3,g=2);nut(f'supportServoN{x}',[x,194,124.1],3,g=2)
# Electronics and panel.
for x in [87.5,162.5]:
    for y in [407.5,462.5]:
        washer(f'perfWT{x}{y}',[x,y,39.6],3);washer(f'perfWB{x}{y}',[x,y,31.5],3);nut(f'perfN{x}{y}',[x,y,29.1],3)
for x in [80,170]:
    for y in [395,475]:
        bolt(f'tray{x}{y}',[x,y,57.5],3,20);washer(f'trayW{x}{y}',[x,y,77],3);nut(f'trayN{x}{y}',[x,y,60.05],3,square=True)
for y in [107,247,387]:
    bolt(f'cable{y}',[381,y,57.5],3,20);washer(f'cableW{y}',[381,y,77],3);nut(f'cableN{y}',[381,y,58.6],3,square=True)
for x in [280,370]:
    bolt(f'panel{x}',[x,-3.5,30],3,25,'y',False);washer(f'panelW1{x}',[x,-3.5,30],3,'y');washer(f'panelW2{x}',[x,15,30],3,'y');nut(f'panelN{x}',[x,15.5,30],3,'y')
for y in [416,434]:assembly(f'fixedCable{y}',382.5,y,47.5,3,30,77,53.5)
for x in [265,385]:
    for y in [-35,-5]:
        bolt(f'lid{x}{y}',[x,y,61.5],3,12);washer(f'lidW{x}{y}',[x,y,73],3)
        name=f'insertLid{x}{y}';ring(name,[x,y,64],3,4.6,6);pressfit.add(frozenset(['AUD_'+name,'08_Painel_operador']))
for x in [272.5,347.5]:
    for z in [28.5,59.5]:
        bolt(f'lcd{x}{z}',[x,-40.5,z],2.5,12,'y',False);washer(f'lcdW1{x}{z}',[x,-40.5,z],2.5,'y');washer(f'lcdW2{x}{z}',[x,-32.4,z],2.5,'y');nut(f'lcdN{x}{z}',[x,-31.9,z],2.5,'y')
# Adjustment nuts, axles and pen/knob contact screws.
washer('adjustXW',[51,310,132],4,'x',1);nut('adjustXN',[51.8,310,132],4,'x',1);nut('adjustXsquare',[44.2,310,132],4,'x',1,True)
washer('adjustYW',[214,19,24.5],4,'y');nut('adjustYN',[214,24.5,24.5],4,'y');nut('adjustYsquare',[214,37.2,24.5],4,'y',square=True)
for x in [196,254]:
    for y in [22,49]:
        washer(f'guideYWtop{x}{y}',[x,y,19],3);washer(f'guideYWbot{x}{y}',[x,y,-.5],3);nut(f'guideYN{x}{y}',[x,y,-2.9],3)
washer('axleXwide',[25,310,122],5,g=1,od=15)
nut('axleXN',[25,310,118],5,g=1)
for z in [149,150,151]:washer(f'axleXW{z}',[25,310,z],5,g=1)
for z in [24,25,41]:washer(f'axleYW{z}',[225,47,z],5,od=8)
nut('axleYN',[225,47,42],5)
nut('penSquare',[210,158,101],3,'y',2,True)
bolt('knobGrub',[375,-48.5,46],3,8,'x',g=0,head=False);nut('knobSquare',[378,-48.5,46],3,'x',0,True)

def group(p):
    if hasattr(p,'group'):return p.group
    if p.stage in [5,9]:return 2
    if p.stage in [3,6,7] or p.name.startswith('10_M4_lateral_'):return 1
    return 0
bbox_cache={}
def common(a,b):
    if id(a) not in bbox_cache:bbox_cache[id(a)]=a.BoundingBox()
    if id(b) not in bbox_cache:bbox_cache[id(b)]=b.BoundingBox()
    aa=bbox_cache[id(a)];bb=bbox_cache[id(b)]
    if min(aa.xmax,bb.xmax)-max(aa.xmin,bb.xmin)<=.002 or min(aa.ymax,bb.ymax)-max(aa.ymin,bb.ymin)<=.002 or min(aa.zmax,bb.zmax)-max(aa.zmin,bb.zmin)<=.002:return 0
    return a.intersect(b).Volume()
intent={frozenset(p) for p in [('11_Fim_curso_X_REFERENCIA','11_Alavanca_X_REFERENCIA'),('11_Fim_curso_Y_REFERENCIA','11_Alavanca_Y_REFERENCIA'),('09_Ponta_caneta_REFERENCIA','11_Folha_A4_210x297')]}
for belt,contacts in [('02_Correia_Y_envelope',['02_Polia_Y_REFERENCIA','02_Polia_livre_Y_REFERENCIA','03_Ancora_correia_Y']),('07_Correia_X_envelope',['07_Polia_X_REFERENCIA','07_Polia_livre_X_REFERENCIA','05_Ancora_correia_X'])]:
    for c in contacts:intent.add(frozenset([belt,c]))
allparts=parts+extra;hits=[];allowed=[]
for i,p in enumerate(allparts):
    for q in allparts[i+1:]:
        vol=common(p.shape,q.shape)
        if vol<.02:continue
        pair=frozenset([p.name,q.name]);row={'a':p.name,'b':q.name,'mm3':round(vol,4)}
        if pair in intent:row['motivo']='Contato funcional nominal explicitamente identificado';allowed.append(row)
        elif pair in pressfit:row['motivo']='Inserto termico OD4,6 em piloto4,2; interferencia de instalacao prevista';allowed.append(row)
        else:hits.append(row)
report={'componentes_modelo':len(parts),'envelopes_ferragens_suplementares':len(extra),'interferencias_nao_previstas':hits,'contatos_previstos':allowed,'metodo':'Solidos exatos; porcas hexagonais com cilindro circunscrito conservador; sem exclusao por categoria de ferragem.','teste_fisico':False}
out=Path(__file__).with_name('auditoria_ferragens_R09.json');out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'modelos':len(parts),'extras':len(extra),'hits':hits},ensure_ascii=False,indent=2),flush=True)
