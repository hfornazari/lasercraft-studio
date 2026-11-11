# ADR-0001: Stack do editor local
**Estado:** Aceita como baseline técnica provisória — 2026-11-06

**Contexto:** precisamos de interface interativa Windows e processamento de imagens, sem dependência de nuvem.

**Decisão:** React/TypeScript/Vite frontend e FastAPI/Python backend. Acesso padrão `localhost`.

**Justificativa:** UI responsiva e bibliotecas maduras de processamento. API isolada permitirá futuramente uso desktop empacotado.

**Consequências:** Node/Python necessários para desenvolvimento; distribuição em executável único requer esforço futuro; CORS restrito à origem local em desenvolvimento.
