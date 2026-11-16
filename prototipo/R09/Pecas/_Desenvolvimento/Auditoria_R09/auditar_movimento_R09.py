from pathlib import Path
import runpy,json
script=Path(__file__).with_name('auditar_ferragens_R09.py');ns=runpy.run_path(str(script))
assert not ns['hits'],ns['hits']
parts=ns['allparts'];group=ns['group'];common=ns['common'];intent=ns['intent'];pressfit=ns['pressfit'];extra_allowed=[];hits=[];positions=[]
# Only the flexible switch lever is allowed to contact its designated homing ramp.
flex={frozenset(['11_Alavanca_X_REFERENCIA','05_Carro_X']),frozenset(['11_Alavanca_Y_REFERENCIA','03_Lateral_integrada_Y_E'])}
for x in [94.5,105,210,320,330]:
    for y in [21,25,166,328.5,335]:
        pos=(x,y);ns['bbox_cache'].clear()
        shapes=[p.shape.translate((x-210 if group(p)==2 else 0,y-166 if group(p) else 0,0)) for p in parts]
        for i,p in enumerate(parts):
            for j in range(i+1,len(parts)):
                q=parts[j]
                if group(p)==group(q):continue
                v=common(shapes[i],shapes[j])
                if v<.02:continue
                pair=frozenset([p.name,q.name]);row={'xy':pos,'a':p.name,'b':q.name,'mm3':round(v,4)}
                if pair in intent or pair in pressfit or pair in flex:extra_allowed.append(row)
                else:hits.append(row)
        positions.append(pos)
        print('Posicao '+str(pos)+' verificada; interferencias='+str(len(hits)),flush=True)

# Check all hardware while moving the two adjustment mechanisms through their full ranges.
config_positions=[]
def belt_at(axis,distance):
    cq=ns['cq'];start=(25 if axis=='x' else 47)-distance;end=425 if axis=='x' else 485;center=310 if axis=='x' else 225;z=135 if axis=='x' else 27
    def capsule(radius):
        if axis=='x':shape=cq.Solid.makeBox(end-start,2*radius,6,cq.Vector(start,center-radius,z));points=[(start,center),(end,center)]
        else:shape=cq.Solid.makeBox(2*radius,end-start,6,cq.Vector(center-radius,start,z));points=[(center,start),(center,end)]
        for xx,yy in points:shape=shape.fuse(cq.Solid.makeCylinder(radius,6,cq.Vector(xx,yy,z)))
        return shape
    return capsule(7.066).cut(capsule(5.666)).clean()
for axis,names,prefixes in [
    ('x',{'07_Eixo_tensor_X','07_Polia_livre_X_REFERENCIA','07_Espacador_metal_M5','07_M4_ajuste_X'},('AUD_axleX',)),
    ('y',{'02_Carro_tensor_Y','02_Eixo_tensor_Y','02_Polia_livre_Y_REFERENCIA'},('AUD_axleY','AUD_adjustYsquare'))]:
    for distance in [i*.5 for i in range(13)]:
        ns['bbox_cache'].clear();shapes=[];affected=[]
        for i,p in enumerate(parts):
            moving=p.name in names or p.name.startswith(prefixes)
            delta=(-distance,0,0) if axis=='x' else (0,-distance,0)
            is_belt=p.name==('07_Correia_X_envelope' if axis=='x' else '02_Correia_Y_envelope')
            shapes.append(belt_at(axis,distance) if is_belt else (p.shape.translate(delta) if moving else p.shape))
            if is_belt:moving=True
            if moving:affected.append(i)
        for i in affected:
            for j,q in enumerate(parts):
                if j==i or j in affected and j<i:continue
                p=parts[i];v=common(shapes[i],shapes[j]);pair=frozenset([p.name,q.name])
                if v>.02 and pair not in intent and pair not in pressfit:hits.append({'ajuste':axis,'distancia':distance,'a':p.name,'b':q.name,'mm3':round(v,4)})
        config_positions.append([axis,distance])
print('Cursos dos tensores conferidos.',flush=True)
pen_positions=[]
for lift in [0,1.5,3,4.5,6]:
    ns['bbox_cache'].clear();shapes=[];affected=[]
    for i,p in enumerate(parts):
        moving=p.name.startswith(('09_Cursor','09_Caneta','09_Ponta','09_M3_aperto','AUD_penSquare'))
        shape=p.shape
        if moving:shape=shape.translate((0,0,lift));affected.append(i)
        elif p.name=='09_Horn_REFERENCIA':shape=shape.rotate((252,0,112),(252,1,112),25*lift/6);affected.append(i)
        elif p.name.startswith('09_Mola_REFERENCIA_'):
            xx=int(p.name.rsplit('_',1)[1]);cq=ns['cq'];shape=cq.Solid.makeCylinder(3,17-lift,cq.Vector(xx,170,106+lift)).cut(cq.Solid.makeCylinder(2.7,17-lift,cq.Vector(xx,170,106+lift)))
        shapes.append(shape)
    for i in affected:
        for j,q in enumerate(parts):
            if j==i or j in affected and j<i:continue
            p=parts[i];v=common(shapes[i],shapes[j]);pair=frozenset([p.name,q.name])
            if v>.02 and pair not in intent and pair not in pressfit:hits.append({'caneta_elevacao':lift,'a':p.name,'b':q.name,'mm3':round(v,4)})
    pen_positions.append(lift)
print('Curso da caneta conferido.',flush=True)
report=ns['report'];report.update(posicoes_movimento=positions,posicoes_tensores=config_positions,posicoes_caneta=pen_positions,interferencias_movimento=hits,contatos_funcionais_movimento=extra_allowed)
Path(__file__).with_name('auditoria_ferragens_R09.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert not hits,hits
print('Auditoria completa sem interferencias nao previstas.',flush=True)
