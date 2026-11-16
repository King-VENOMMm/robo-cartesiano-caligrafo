# R09 — montagem mecanica e interface

Esta revisao fecha as interfaces anteriormente pendentes no CAD. E um prototipo para montagem e ensaio, nao uma maquina cuja precisao ou resistencia ja foi comprovada fisicamente.

## Retencao das hastes e dos rolamentos

- Y: duas hastes retificadas12x500 mm, de y0 a500. Quatro colares DIN705 ID12/OD22/L12, em y5..17 e483..495, fora dos apoios. Instalar os colares antes de apertar e conferir o esquadro. Substituem as hastes450 mm anteriores.
- X: duas hastes8x450 mm, de x0 a450. Nao cortar para440 mm. Colares8 mm em x0..8 e442..450, externos as laterais alargadas.
- LM12UU: ombro frontal integrado ao alojamento, dois rolamentos por lateral, espacador impresso38 mm e tampa traseira removivel com quatro M3x16/porcas quadradas M3. O primeiro rolamento comeca em y192, o segundo em260. Ordem: inserir primeiro rolamento, espacador e segundo rolamento; fechar tampa; introduzir haste. Para retirar, aliviar correia, soltar colares, retirar haste e abrir tampa.
- LM8UU: dois rolamentos por guia no carro, espacador22 mm entre eles e duas tampas axiais, uma em cada extremidade. Cada tampa usa quatro M3x16 e insertos termicos M3x6 no carro. Instalar insertos antes dos rolamentos. A tampa esquerda tem janela para a rampa do sensor X. Desmontagem pelo mesmo caminho, sem cola.
- Os colares prendem axialmente as hastes; ombros, espacadores e tampas prendem os rolamentos. A folga radial dos alojamentos depende da impressora. Imprimir primeiro os cupons opcionais de15/15,1/15,2 e21/21,1/21,2 mm. Se necessario, ajustar o diametro no modelo, sem escalar a peca inteira.

## Tensao das correias

- X: regulagem de6 mm na polia livre. Parafuso M4x35, porca quadrada e contraporca. Rebaixo sob a placa libera a arruela OD15 em todo o curso. Motor fixo; afrouxar fixacao do eixo antes de regular e reapertar depois, conforme pilha real. A correia nao passa pelo bloco central do tensor.
- Y (R09): motor fixo em furos circulares. A polia dianteira desliza de y47 para y41 (6 mm). O M4x30 passa livre na parede frontal, mas rosqueia na porca quadrada M4 cativa do carro. Uma arruela M4 fica entre cabeca e parede; a contraporca fica do lado interno da parede, sem arruela adicional. Soltar apenas a contraporca, girar o M4 para puxar o carro e tensionar, depois travar a contraporca segurando a cabeca. Nao afrouxar os quatro M3 do motor nem o eixo M5 da polia. Guias e labios impedem a polia de inclinar ou levantar.
- Fazer ajuste grosso nas pontas da correia e usar o parafuso apenas para ajuste fino. Nao especificamos uma forca de tensao antes de medir flexao e comportamento do prototipo.

## Caneta, molas e SG90

- Duas guias4x55 mm. Tres colares4 mm por guia: abaixo da ponte superior, acima dela e como limite inferior do cursor. As guias ficam presas entre colares, sem cola.
- Duas molas de compressao OD6 mm, fio0,3 mm, comprimento livre25 mm. Rigidez alvo aproximada0,02 N/mm por mola, cerca de22 espiras ativas. E uma especificacao a conferir no fornecedor e medir: a mesma dimensao externa pode ter rigidez diferente.
- Comprimento instalado nominal17 mm e aproximadamente11 mm ao levantar6 mm. Com k=0,02 N/mm, as duas molas exercem juntas cerca de0,32 N abaixadas, mais o peso do cursor/caneta. Ao levantar6 mm, aproximadamente0,56 N, mais o peso. Conferir altura solida da mola, que deve permanecer abaixo do menor comprimento instalado com margem.
- Pressao ajustavel com os calcos opcionais de1 mm: no maximo2 por guia entre mola e colar de apoio. Com k=0,02 N/mm, um calco em cada guia aumenta a forca total em aproximadamente0,04 N. Para reduzir a pressao, usar mola mais leve ou ajustar a posicao da caneta mantendo folga ao batente. Medir no papel, de preferencia com pequena balanca.
- Ajustar a altura da caneta pelo parafuso lateral M3 com porca quadrada; ponta deve tocar papel antes de o cursor atingir o colar inferior. Existe cerca de1 mm de acomodacao descendente no ponto nominal. Nao apertar o corpo da caneta excessivamente.
- Servo foi orientado com o eixo lateral coerente com o corpo SG90. Suporte tem janela, rasgos para orelhas e dois M3x20 ligando sua flange ao cabecote. Envelope baseado no SG90 TowerPro, mas o servo existente e seu horn precisam ser medidos antes de fabricar a versao definitiva.
- A alavanca comercial fica sob a aba do cursor: embaixo deixa a caneta livre sob molas/peso; ao girar levanta o cursor. O envelope permite aproximadamente5 a6 mm de levantamento, cerca de25 graus na geometria nominal. Calibrar angulos gradualmente no servo real; nao enviar0/180 graus sem verificar. Foram conferidas separadamente a posicao baixa e a elevada6 mm, sem tratar molas como corpos rigidos.

## Madeira e acessibilidade

- Pes reposicionados em x80/370,y50/450 para liberar parafusos das guias. M4x55, porca/arruela em rebaixo acessivel no pe; ponta nao fica abaixo do piso.
- Furos da base, apoios e tampo conciliados para os cinco M4x85 passantes da mesa. As fixacoes antigas sem correspondencia dos pes foram substituidas.
- Incluidos furos do suporte da polia Y, bandeja, guias de cabos e painel. Cada pasta de MDF tem DXF em mm, tabela CSV local e orientacao. Os furos que atravessam a aresta dos apoios de madeira sao uma operacao separada descrita no arquivo de texto.
- Consultar o STEP e conferir escala1:1 do desenho antes do corte. O MDF de6 mm da travessa e mantido; verificar esmagamento junto as arruelas e rigidez do conjunto em ensaio.

## Eletronica, cabos e painel

- Bandeja100x90 sob a parte traseira do tampo, piso z32, acima da travessa movel(z20..26). Quatro M3x20 ao tampo com porcas quadradas nas torres. Perfboard80x60 em quatro apoios, M3x12, porcas e arruelas; modulos montados em soquetes/amarras conforme placa real. Nao existem furos supostamente universais para todas as variantes ESP32.
- Leitor microSD na lateral esquerda da bandeja, junto ao ESP32, para manter SPI curto. Cartao inserido pela lateral com a maquina parada e ponte estacionada a frente. Leitor com fios rentes ou conector90 graus; pinos retos altos nao cabem sob o tampo. Nao e uma porta de pendrive.
- Painel frontal130x40x55 mm, ligado ao apoio frontal por dois M3x25. LCD1602 I2C existente, encoder EC11 com botao/manopla, chave bipolar DC e extensao USB-C de dados para a porta USB-C da placa. Caixa com tampa removivel, quatro M3x12 e insertos M3. LCD tem apoio/furacao nominal75x31; confirmar no exemplar, inclusive espessura do adaptador I2C.
- Cabos fixos correm sob o lado direito do tampo. Alivio fixo realocado para x375..390,y410..440,z54..65, com dois M3x30 ao tampo emx382,5,y416/434. O alivio movel fica fora da lateral direita. Formar laco externo e conferir fisicamente em todo X/Y antes de cortar cabos; trajetoria flexivel nao simulada.
- Separar sinais de sensores/I2C dos cabos de motor; usar pares sinal/GND, conexoes travadas e amarracao. A trajetoria deformavel dos fios nao foi simulada como garantia de ausencia de enrosco. Conferir manualmente X/Y nos extremos antes de energizar.

## Limites e arquivos

Janela proposta da ponta no CAD: X105..330 e Y25..335, ou225x310 mm. Contem A4 em x110..320 e y31,5..328,5. O extremo Y foi reduzido para liberar tampas/parafusos traseiros. Batente X passa a aproximadamente93 mm pela espessura da tampa do carro; sensor nominal atua antes disso, perto94,4 mm. Calibrar novamente homing e recuo; nao reutilizar limites antigos automaticamente.

STL orientados para a impressora e STEP individuais editaveis. O STEP montado nao carrega replay: o script Fusion_Montagem_A4 foi atualizado para R09, mas a execucao/replay continua sem verificacao no Fusion.

A caixa foi modelada, mas o menu LCD/encoder e a selecao de G-code do microSD ainda nao foram programados/testados. ELETRONICA_R07.md descreve a integracao pendente. Nao interpretar os envelopes de componentes como uma PCB pronta ou esquema eletrico validado.


## Montagem do novo tensor Y

1. Testar a guia e o carro separados: folga nominal de 0,3 mm. Remover rebarbas; nao forcar nem aumentar a tensao para vencer atrito. Imprimir apenas estas pecas primeiro se ainda nao fez teste dimensional.
2. Montar no carro o M5x30 de cabeca chata escareada a 90 graus, vindo de baixo. A cabeca deve ficar rente ao fundo. Comprimento total de 30 mm, conforme a ferragem escolhida.
3. Empilhar dois calcos metalicos M5 de 1 mm (OD8, ID5,2), a polia livre com rolamento, mais um calco de 1 mm e uma porca M5. Apoiar somente o anel interno do rolamento; confirmar diametro do anel na polia comprada. Apertar sem prender o giro da polia. Nao usar uma polia motora sem rolamento nesta posicao.
4. Inserir a porca quadrada M4 pelo topo do nariz do carro e deslizar o conjunto pela abertura traseira da guia, com a correia ainda solta.
5. Introduzir M4x30 com uma arruela pela frente da parede. Colocar a contraporca M4 do lado interno e rosquear a ponta na porca quadrada do carro. A contraporca fica apenas encostada depois do ajuste, sem esmagar o plastico.
6. Fixar a guia a base com quatro M3x25, porcas e arruelas: x196/254, y22/49 mm. A furacao antiga x214/236, y24/46 e o furo de eixo y35 foram substituidos. Usar o DXF R09.
7. Fazer ajuste grosso no mordente da correia. Usar o M4 para ajuste fino, mantendo engajamento da rosca e o carro dentro das guias. Curso nominal de 6 mm, de y47 ate y41. Nao puxar o carro para fora da guia nem tensionar excessivamente.

A mudanca desloca a polia livre 12 mm em relacao a R07. Cortar a correia somente apos montagem e regulagem. A quantidade de correia comprada foi mantida com sobra para corte.

O modelo e os arquivos individuais sao R09. Sequencia de montagem do Fusion atualizada, mas ainda nao executada/inspecionada no Fusion. Sem teste fisico ou ensaio de resistencia.


## Correcoes de interferencias R09 — ler antes de fabricar

- Laterais Y alargadas para44 mm. M4 em duas colunas a17 mm do centro da haste (x13/47 e403/437), y225/235/245. Ha4,15 mm nominais de material entre a passagem M4 e o alojamento LM12. Os parafusos nao atravessam o espacador. A tampa de retencao dos rolamentos continua removivel.
- Travessa inferior agora MDF440x80x6, origem x5,y200. Nos doze M4 fazer rebaixo pela face inferior OD10, profundidade1,2 mm. Arruela inferior M4 OD9 x0,8 emz20,4..21,2; porca emz17,2..20,4. A ponta do M4 de114 mm fica emz15,8, acima da base z15. Conferir empilhamento real antes de cortar e apertar sem esmagar o MDF. Arruela superior0,8 emz129..129,8. Nao fabricar pela furacao R08.
- Apoios superiores X foram ajustados as laterais alargadas; hastes X passaram a450 mm e os colares foram reposicionados. Reforcos das placas passam a comecar atras da lateral, sem sobrepor os corpos impressos.
- Carro X: fixacoes do cabecote emx202/218,y224; do braco emx202/218,y244 e x196/224,y254. Flanges ampliadas; as passagens M3 ficam fora dos alojamentos LM8, sem atravessar os espacadores. Parafusos M3x40 com arruelas0,5 e porcas, conforme BOM.
- Mordente X: rebaixos traseiros liberam porcas e arruelas. Tensor X: bloco estreitado entre os dois trechos da correia e M4x35 para a cabeca nao atingir a contraporca no curso total. A arruela inferior OD15 tem folga de0,25 mm no rebaixo.
- Retentores LM8: considerar arruela M3 de0,5 mm sob a cabeca. Insertos OD4,6 em piloto4,2 sao interferencia de instalacao termica prevista; fazer cupom antes. O piloto impresso nao representa um inserto ja instalado.
- Sensor Y: cabecas M2 e arruelas em rebaixos, livres do apoio da haste. Sensor X: cortar dois M2x20 para17 mm para evitar a ponta reentrar na parede. Regular sensores sem energizar motores.
- Suporte SG90: M3x20 emx223/231,y194; porcas e arruelas inferiores livres do carro.
- Guias de cabos: porca quadrada M3 dentro do canal, emz58,6..61, nao acima do canal. A arruela fica sobre o tampo.
- Cursor: bolso da porca quadrada ampliado para2,6 mm; M3 da caneta ajustado ate apenas tocar a caneta, sem atravessar seu corpo.
- LCD: M2,5x12 nos quatro cantos da PCB nominal de1,6 mm. O corpo LCD nao ocupa os cantos de fixacao. Conferir modulo real; o modelo e uma reserva dimensional.

Auditoria: 176 componentes do modelo e358 envelopes suplementares de ferragens. Verificacao estatica de todas as combinacoes; 25 posicoes XY,13 posicoes em cada tensor e5 alturas da caneta. Contatos de dentes/correia, alavancas de sensores, ponta/papel e instalacao termica de insertos sao listados explicitamente no relatorio, sem exclusao geral de parafusos. Isso nao e ensaio fisico, analise de resistencia ou prova de ausencia de colisoes em qualquer estado continuo.

Pilha do eixo livre X (z, em mm): cabeca M5 de152 para cima; tres arruelas de149 a152; polia134..149; espacador metalico129..134; placa123..129; arruela larga122..123 e porca118..122. M5x35 de117 a152, introduzido por cima. Conferir apoio no anel interno e giro livre da polia real.


Plano de impressao atual: PLA,41 unidades em13 mesas. Nove mesas entre4h27min39s e4h34min25s; quatro excecoes individuais acima de5h aprovadas pelo usuario. Projeto: Robo Cartografico A4 Desmontado.3mf, na pasta principal. Detalhes em Pecas/_Desenvolvimento/Impressao_ate5h_R09/Tempos e pecas por mesa.md.
