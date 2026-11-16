"""Execute no Fusion. Cria documento novo; nao altera projetos existentes.
Os componentes prontos aparecem no historico em ordem de montagem, sem replay de usinagem.
"""
import adsk.core, adsk.fusion
import json, os, traceback

def run(context):
    app=adsk.core.Application.get()
    folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Exportados')
    logfile=os.path.join(folder,'fusion_montagem.log')
    tempdoc=None
    try:
        data=json.load(open(os.path.join(folder,'componentes_cadquery.json'),encoding='utf-8'))
        im=app.importManager
        opts=im.createSTEPImportOptions(os.path.join(folder,'Robo_A4_R09_Montagem.step'))
        tempdoc=im.importToNewDocument(opts)
        source=adsk.fusion.Design.cast(tempdoc.products.itemByProductType('DesignProductType'))
        tm=adsk.fusion.TemporaryBRepManager.get()
        shapes={}
        appearances={}
        for c in source.allComponents:
            if c.bRepBodies.count:
                shapes[c.name]=tm.copy(c.bRepBodies.item(0))
                appearances[c.name]=c.bRepBodies.item(0).appearance
        def match(name):
            if name in shapes:return name
            candidates=[s for s in shapes if s.startswith(name) or name.startswith(s)]
            if len(candidates)==1:return candidates[0]
            raise RuntimeError('Componente STEP nao encontrado de forma univoca: '+name+'\nDisponiveis: '+str(list(shapes)))
        keys={p['nome']:match(p['nome']) for p in data}
        doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        doc.name='Robo A4 R09 - Sequencia de montagem'
        design=adsk.fusion.Design.cast(app.activeProduct)
        design.designType=adsk.fusion.DesignTypes.ParametricDesignType
        design.unitsManager.distanceDisplayUnits=adsk.fusion.DistanceUnits.MillimeterDistanceUnits
        root=design.rootComponent
        root.name='Robo_A4_R09_Montagem_ESTUDO'
        labels=['Base e pes','Acionamento Y','Pre-montagem ponte Y','Guias Y','Pre-montagem carro X','Guias X','Acionamento X','Mesa elevada','Cabecote e caneta','Ferragens de referencia','Papel e sensores']
        materials={}
        for stage,label in enumerate(labels,1):
            start=design.timeline.count
            def assembly_order(p):
                n=p['nome']
                if stage==2:
                    if n=='02_Base_tensor_Y':return 1
                    if n=='02_Carro_tensor_Y':return 2
                    if n=='02_Eixo_tensor_Y':return 3
                    if n=='02_Polia_livre_Y_REFERENCIA':return 4
                    if n.startswith(('02_M4_ajuste','02_M3_batente')):return 5
                if stage==3:
                    if n.startswith('03_M3_tampa_LM12'):return 6
                    if n.startswith('03_Tampa_LM12'):return 5
                    if n.startswith('03_LM12UU'):return 4
                    if n.startswith('03_Espacador'):return 3
                if stage==5:
                    if n.startswith('05_M3_tampa'):return 6
                    if n.startswith('05_Tampa_LM8'):return 5
                    if n.startswith('05_LM8UU'):return 4
                    if n.startswith('05_Espacador'):return 3
                return 0
            for p in sorted([p for p in data if p['etapa']==stage],key=assembly_order):
                occ=root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
                c=occ.component
                c.name=p['nome']
                c.description=p['nota']
                c.attributes.add('RoboA4','etapa',str(stage))
                c.attributes.add('RoboA4','tipo',p['tipo'])
                bf=c.features.baseFeatures.add()
                bf.name='Instalar '+p['nome']
                bf.startEdit()
                body=c.bRepBodies.add(shapes[keys[p['nome']]],bf)
                if not body:raise RuntimeError('Falha ao adicionar solido '+p['nome'])
                body.name=p['nome']
                bf.finishEdit()
                if p['tipo'] not in materials:
                    materials[p['tipo']]=design.appearances.addByCopy(appearances[keys[p['nome']]],'A4_'+p['tipo'])
                body.appearance=materials[p['tipo']]
            end=design.timeline.count-1
            if end>=start:
                g=design.timeline.timelineGroups.add(start,end)
                g.name='%02d - %s'%(stage,label)
                g.isCollapsed=True
            adsk.doEvents()
        tempdoc.close(False)
        tempdoc=None
        design.timeline.moveToEnd()
        camera=app.activeViewport.camera
        camera.isPerspective=False
        camera.eye=adsk.core.Point3D.create(85,-85,80)
        camera.target=adsk.core.Point3D.create(22.5,24.5,5.5)
        camera.upVector=adsk.core.Vector3D.create(0,0,1)
        camera.isFitView=True
        camera.isSmoothTransition=False
        app.activeViewport.camera=camera
        app.activeViewport.fit()
        app.activeViewport.refresh()
        em=design.exportManager
        filename=os.path.join(folder,'Robo_A4_R09_Com_Replay.f3d')
        if not em.execute(em.createFusionArchiveExportOptions(filename)):
            raise RuntimeError('Falha ao salvar F3D')
        app.activeViewport.saveAsImageFile(os.path.join(folder,'Vista_Fusion_Replay.png'),1600,1200)
        with open(logfile,'w',encoding='utf-8') as f:
            f.write('SUCESSO\nComponentes: '+str(len(data))+'\nGrupos: 11\nArquivo: '+filename)
        app.userInterface.messageBox('Montagem criada e F3D salvo.\n\nNo ambiente Design, use Voltar ao inicio e Reproduzir no historico inferior.\nOs grupos numerados mostram a ordem de montagem com componentes completos.\n\nEsta revisao e um estudo: retenções, fixacoes e componentes reais ainda precisam ser conferidos.\n\n'+filename,'Robo A4 - replay de montagem')
    except Exception:
        err=traceback.format_exc()
        with open(logfile,'w',encoding='utf-8') as f:f.write(err)
        app.userInterface.messageBox(err,'Erro ao preparar replay A4')
