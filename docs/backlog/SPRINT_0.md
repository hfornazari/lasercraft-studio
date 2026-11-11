# Sprint 0 — Fundação executável

**Objetivo:** abrir interface local Windows, importar imagem, conferir escala e área útil com matriz de fábrica.

## Histórias e critérios
- [x] S0-001 Scaffold Vite/React TS e FastAPI com endpoints documentados.
- [x] S0-002 Configuração de matriz com largura, altura, margem e área útil em mm. Limite customizado 350 × 275 mm.
- [x] S0-003 Upload SVG ou PNG (até 10 MiB) com validação, metadados e feedback de erro.
- [x] S0-004 Prévia proporcional sem distorção, com área útil e dimensões calculadas em mm.
- [x] S0-005 Baseline de testes pytest e pipeline GitHub Actions.
- [x] S0-006 Memória IA, ADRs, decisões, resoluções e roadmap.

## Validação
- [x] `python -m pytest -q`: 7 testes aprovados em ambiente de geração (2026-11-06); ainda requer validação no Windows do usuário.
- [ ] `npm run build`: não validado; `npm install` excedeu tempo disponível neste ambiente.
- [ ] Upload e preview manual validados no Windows do usuário.

## Fora de escopo Sprint 0
Separar cores em layers, vetorizar PNG, simulação de laser, renderização de percurso, STL, DXF, PDF, G-code, `.lcraft`.
