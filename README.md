# Robô Cartesiano Desenhista e Calígrafo

Protótipo acadêmico para desenhar e escrever em papel A4 com uma caneta. Projeto da disciplina **Projeto de Engenharia II: Manipuladores Robóticos (8790.1.02)**, da PUC Minas.

Na revisão R09, o carro da caneta se desloca em X, a ponte se desloca em Y e um servo SG90 levanta e abaixa a caneta. A janela útil prevista no CAD é de **225 × 310 mm**. A estrutura combina peças impressas em PLA, MDF e componentes comerciais.

## Arquivos da revisão R09

| Arquivo | Uso |
| --- | --- |
| [Modelo montado em STEP](prototipo/R09/Robo%20Cartografico%20A4%20Montado.step) | Inspecionar o conjunto no CAD |
| [Lista de materiais](prototipo/R09/Lista%20de%20Materiais.xlsx) | Conferir componentes e quantidades |
| [Projeto OrcaSlicer em 13 mesas](prototipo/R09/Robo%20Cartografico%20A4%20Desmontado.3mf) | Fatiar as peças em PLA |
| [Peças impressas](prototipo/R09/Pecas/01_Impressao_3D) e [peças em MDF](prototipo/R09/Pecas/02_MDF_NAO_IMPRIMIR) | Consultar arquivos individuais de fabricação |
| [Montagem e regulagens](prototipo/R09/Pecas/_Desenvolvimento/MONTAGEM_R09.md) | Conferir encaixes, fixações, correias e ajuste da caneta |
| [Arquitetura eletrônica](prototipo/R09/Pecas/_Desenvolvimento/ELETRONICA_R07.md) | Consultar o projeto de integração com ESP32 |

## Montagem e ensaios

1. Confira a [classificação das peças](prototipo/R09/Pecas/LEIA%20PRIMEIRO.md) antes de fabricar.
2. Abra o arquivo 3MF como projeto no OrcaSlicer, confira o perfil da impressora e consulte os [tempos estimados por mesa](prototipo/R09/Pecas/_Desenvolvimento/Impressao_ate5h_R09/Tempos%20e%20pecas%20por%20mesa.md).
3. Use o guia de montagem para ajustar a ponte e a caneta. O pacote inclui um [teste XY para GRBL](prototipo/R09/GCode_TXT/Teste_R10_XY.txt).

A montagem física e a calibração do protótipo estão pendentes. O firmware dedicado para ESP32, a conversão de SVG e texto para trajetórias e a interface de operação fazem parte da próxima etapa.

## Vídeos e demonstrações

*Os links do YouTube serão adicionados aqui.*

## Integrantes

- Arthur Artiaga Oliveira
- Daniel Rodrigues dos Reis
- Laila Marques Soares
- Izabelly Pedrosa Belchior
- Maria Eduarda Miranda Araujo
