# ADR-0003: Projeto `.lcraft` versionado
**Estado:** Proposta — 2026-11-06

**Contexto:** permitir reproduzir edições e opcionalmente incorporar fonte.

**Proposta:** pacote ZIP com manifest.json (versão de esquema), document.json, operations.json, geometry/paths.json, preview/thumbnail.png e assets/original.* opcional. Sem fonte embutida, armazenar referência relativa e SHA-256; conservar geometria derivada editável quando possível.

**Pendências:** migração de esquema, integridade de blobs, tamanho máximo e permissões.
