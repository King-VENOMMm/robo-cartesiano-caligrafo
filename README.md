# Robô Cartesiano Desenhista e Calígrafo

Projeto acadêmico da disciplina **Projeto de Engenharia II: Manipuladores
Robóticos (8790.1.02)**, da PUC Minas.

## Objetivo

Desenvolver um robô cartesiano capaz de desenhar e escrever com uma caneta por
meio de trajetórias vetoriais contínuas. O conceito inicial utiliza:

- eixo X para movimentar a caneta;
- eixo Y para transportar a folha de forma bidirecional;
- eixo Z simplificado, acionado por servo, para levantar e abaixar a caneta;
- ESP32 D1 R32 como controlador principal;
- motores de passo nos eixos X e Y;
- sensores de fim de curso e sensores ópticos de papel.

O MVP deverá trabalhar inicialmente com SVG e texto em fontes monolineares,
convertidos no computador para G-code ou para um protocolo intermediário. O
firmware começará com movimentos lineares e comandos equivalentes a `G0`, `G1`,
`PEN_UP` e `PEN_DOWN`.

## Protótipo A4 — revisão R09

A revisão R09 reúne o CAD mecânico do protótipo, a lista de materiais e os arquivos de fabricação. O conjunto foi projetado para desenhar em papel A4 com uma caneta acionada por servo.

- [Modelo montado em STEP](prototipo/R09/Robo%20Cartografico%20A4%20Montado.step)
- [Projeto de impressão OrcaSlicer em 13 mesas](prototipo/R09/Robo%20Cartografico%20A4%20Desmontado.3mf) e [tempos estimados](prototipo/R09/Pecas/_Desenvolvimento/Impressao_ate5h_R09/Tempos%20e%20pecas%20por%20mesa.md)
- [Lista de materiais](prototipo/R09/Lista%20de%20Materiais.xlsx) e [arquivos de peças](prototipo/R09/Pecas)
- [Montagem e regulagens](prototipo/R09/Pecas/_Desenvolvimento/MONTAGEM_R09.md) e [arquitetura eletrônica](prototipo/R09/Pecas/_Desenvolvimento/ELETRONICA_R07.md)

A montagem física e a calibração do protótipo estão pendentes. O pacote inclui um teste XY para GRBL. O firmware de controle do Calígrafo por ESP32 e a interface web ainda estão planejados.

## Estrutura do repositório

```text
docs/                         documentação do projeto
firmware/esp32/               firmware principal do controlador
firmware/testes_motores/      ensaios isolados de motores e movimento
software/conversor_gcode/     conversão de vetores e texto em trajetórias
software/interface_web/       interface de operação e acompanhamento
mecanica/cad/                 modelos CAD
mecanica/desenhos_tecnicos/   desenhos para fabricação e montagem
mecanica/impressao_3d/        arquivos destinados à impressão 3D
eletronica/                   esquemas, placas e listas de conexões
gcode/                        trajetórias e exemplos de entrada
testes/                       protocolos e recursos de teste
resultados/                   medições e evidências experimentais
```

## Integrantes

- Arthur Artiaga Oliveira
- Daniel Rodrigues dos Reis
- Laila Marques Soares
- Izabelly Pedrosa Belchior
- Maria Eduarda Miranda Araujo

## Próximos passos

1. Definir os componentes do primeiro protótipo.
2. Validar individualmente motores, drivers, servo e sensores.
3. Implementar movimento manual, homing e limites.
4. Calibrar os passos por milímetro dos eixos X e Y.
5. Executar e registrar os ensaios geométricos iniciais.
