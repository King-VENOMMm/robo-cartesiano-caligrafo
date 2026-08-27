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

## Estado atual

O projeto está na fase de concepção e organização. Ainda não há resultados
experimentais registrados, nem CAD, firmware ou aplicação web finalizados.

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
