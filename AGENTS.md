# AGENTS.md — Contrato de continuidade do LaserCraft Studio

**Leia este arquivo integralmente antes de planejar, responder ou escrever código.** Este repositório é a fonte persistente do estado do projeto, não a memória de qualquer sessão de IA.

## Ordem obrigatória de leitura
1. `README.md` — como executar e estado realmente entregue.
2. `docs/ai/PROJECT_MEMORY.md` — resumo vivo do escopo e decisões.
3. `docs/DECISIONS.md` e `docs/adr/` — decisões aprovadas e justificativas.
4. `docs/RESOLUTIONS.md` — problemas e soluções verificadas.
5. `docs/backlog/SPRINT_0.md` e `docs/ROADMAP.md` — entregue, pendente e critérios de aceite.
6. Código e testes relevantes antes de propor alterações.

## Regras inegociáveis
- Não declarar implementada uma funcionalidade apenas porque está descrita no roadmap.
- Matriz inicial **350 × 275 mm**; margens **5 mm** em cada lado; área útil **340 × 265 mm**. Distinguir `bed` de `safe area`.
- Unidades geométricas de domínio em **mm**. Renderização em pixels é apenas uma projeção visual.
- Manter proporção original por padrão; sem cortes silenciosos ou escala distorcida.
- SVG/DXF para trajetórias 2D; STL somente como opção de extrusão 3D. Espessura de traço **não equivale** a potência de laser.
- Potência/velocidade/passadas são parâmetros específicos de máquina e material; não presumir adequação física.
- Sem executar arquivos SVG como scripts; tratamento defensivo de uploads, limites e testes de segurança.
- Separar requisitos confirmados, decisões propostas e hipóteses pendentes.
- Cada mudança de comportamento atualiza documentação, memória, testes e, quando aplicável, ADR na mesma contribuição.
- Toda solução de bug deve registrar sintoma, causa, correção e como foi validada em `docs/RESOLUTIONS.md`.
- Não alterar decisões registradas sem nova decisão numerada, motivo e impacto.

## Protocolo por sessão
**Entrada:** ler os documentos acima; executar os testes disponíveis; resumir o status real e apontar dúvidas.
**Execução:** implementar a menor fatia vertical testável; registrar limitações; não inventar validações.
**Saída:** (a) atualizar `docs/ai/PROJECT_MEMORY.md` com data, versão, entregas, próximos passos e pendências; (b) acrescentar registros a `docs/DECISIONS.md`/`docs/RESOLUTIONS.md`; (c) atualizar backlog e README; (d) listar comandos rodados e resultados; (e) se necessário, criar ADR com estado Proposta/Aceita/Substituída.

## Preferências de implementação
- React + TypeScript + Vite na UI; FastAPI no backend; pytest e build TS como baseline.
- Evitar abstrações sem necessidade; usar nomes claros; tipos explícitos; normalizar transformações e unidades.
- Nunca gravar segredos, credenciais, arquivos de usuário ou configurações pessoais no repositório.
- Para novas funcionalidades de importação/exportação, fornecer fixture e teste de tamanho dimensional.
