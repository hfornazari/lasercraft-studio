# Memória viva do projeto

Atualizado: **2026-11-06** | Fase: **Sprint 0 — primeira versão entregue para execução local; não validada em máquina laser**

## Visão
LaserCraft Studio é um editor para importar SVG e PNG, preparar geometria vetorial, enquadrar numa matriz física, separar cores, gerar contornos, simular operações e exportar formatos apropriados ao corte a laser. Salvar projeto reeditável com imagem original embutida opcionalmente.

## Decisões confirmadas pelo solicitante
- Dimensões padrão: matriz **350 × 275 mm**, margens **5 mm** em todos os lados; área útil **340 × 265 mm**.
- Entrada desejada: SVG e PNG; modos futuros: separação por cor, contornos; suporte STL solicitado.
- Presets desejados: A4, B5 e customizado; limite customizado inicial 350 × 275 mm.
- Projeto deve preservar etapas e configurações; fonte incorporada de forma opcional.
- Código e decisões devem ficar documentados no GitHub, acompanhados de instruções para IA.

## Decisões técnicas adotadas como baseline, sujeitas a revisão
- Web local React/TypeScript + FastAPI/Python; ver ADR-0001.
- Coordenadas e dimensões canônicas em mm.
- SVG e DXF são formatos de corte 2D; STL será extrusão 3D **opcional**.
- A4: 210 × 297 mm; ISO B5: 176 × 250 mm (não confundir com JIS B5).

## Sprint 0 — entregue neste repositório
- Scaffold backend/frontend, configuração de matriz, upload SVG/PNG com validações básicas, preview de imagem em caixa proporcional, visualização da área segura, endpoint de saúde, testes iniciais e CI.
- Backend: 7 testes pytest aprovados no ambiente de geração em 2026-11-06. Frontend: build não validado porque `npm install` não finalizou neste ambiente.
- Não há integração com máquina, simulação dinâmica, extração vetorial/cor por camada, nem exportação de corte nesta fase.

## Decisões em aberto (não assumir)
1. Marca/modelo de máquina e firmware/controlador, software de destino, perfil de potência e velocidade.
2. Os presets de papel A4 exigem 297 mm de altura em retrato — excedem a altura máxima customizada de 275 mm. Definir política: permitir preset maior com aviso ou ajustar orientação/escala. Implementação atual oferece presets limitados pela matriz.
3. Convenção de âncora de origem, offsets de máquina, sentido dos eixos e kerf.
4. Requisitos de vetorizar PNG e contornos internos/externos.
5. Política de tamanho/versão de arquivos `.lcraft` e comportamento offline com fonte externa ausente.

## Próximos passos
- Executar localmente e confirmar UI/testes.
- Sprint 1: rota de documento versionado, pipeline de transformações, metadados SVG robustos e controles visuais de pan/zoom/rotação.
- Posteriormente: quantização/segmentação, vetorização, camadas, simulator, exportações, `.lcraft`.

## Protocolo
Não substituir histórico por suposições. Ao finalizar cada etapa, registrar data, itens aprovados, artefatos, validação comprovada e pendências; sincronizar ADR/decisões/resoluções/backlog.
