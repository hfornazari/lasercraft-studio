# LaserCraft Studio

Editor local para preparar imagens SVG/PNG para corte a laser. **Sprint 0 — fundação executável**.

## Estado atual
- Frontend React + TypeScript + Vite: editor de matriz, upload, visualização e transformação da imagem.
- Backend FastAPI: validação e leitura de metadados de SVG/PNG, configuração da matriz, análise básica das cores PNG.
- Perfil padrão: **350 × 275 mm**, margem **5 mm** por lado, área útil **340 × 265 mm**.
- Imagem sempre enquadrada proporcionalmente na área útil, sem distorção; tamanho efetivo em mm exibido.
- **Não implementados na Sprint 0:** vetorização PNG, caminhos de laser, kerf, controle de máquina, exportação DXF/STL/PDF, simulador de movimentos, projeto `.lcraft` persistido. A prévia atual é geométrica, não simulação física do corte.

## Executar no Windows (PowerShell)

Requisitos: Python 3.11+ e Node.js 20.19+ ou 22.12+ (confira a exigência da versão instalada do Vite).

**Terminal 1:**
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Terminal 2:**
```powershell
cd frontend
npm install
npm run dev
```

Acesse `http://localhost:5173` e API em `http://localhost:8000/docs`.

### Testes

No ambiente de geração: **7 testes do backend passaram**. O build frontend não pôde ser validado porque a instalação npm não foi concluída; execute os comandos abaixo localmente.

```powershell
cd backend
python -m pytest -q
```
```powershell
cd frontend
npm run build
```

## Segurança / limitações
- A API rejeita arquivos acima de 10 MiB e verifica assinatura de PNG; SVG passa por limpeza de elementos/atributos e **não é devolvido como HTML executável**. A prévia de SVG no navegador ainda usa URL `blob:` em `img` isolado — configure política de segurança estrita e revisão do sanitizador antes de publicar o serviço na Internet.
- Não envie caminhos de máquina a partir da prévia: não há geração de G-code nem calibração.
- Cores PNG são contagens aproximadas por quantização RGB, não uma separação de layers.
- Servidor destinado ao uso **local**, sem autenticação: não expor à rede pública.

## Orientações para IA
Leia `AGENTS.md`, `docs/ai/PROJECT_MEMORY.md`, `docs/DECISIONS.md`, `docs/RESOLUTIONS.md` e `docs/backlog/SPRINT_0.md` **antes de alterar o código**. Toda decisão nova deve atualizar os registros de forma atômica com a mudança.

## Estrutura
```
backend/      API FastAPI + testes
frontend/     editor React/Vite
samples/      imagem simples para testes
AGENTS.md     regras operacionais para agentes de IA
docs/ai/      memória rastreável e protocolo de continuidade
docs/adr/     decisões técnicas arquiteturais
docs/        requisitos, decisões, resoluções e roadmap
.github/      CI de testes/build
```
