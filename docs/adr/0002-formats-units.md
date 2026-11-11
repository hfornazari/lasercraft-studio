# ADR-0002: Geometria física e formatos de exportação
**Estado:** Aceita como baseline técnica provisória — 2026-11-06

**Decisão:** dimensões canônicas em milímetros; pixels só para visualização. SVG/DXF são preferenciais para corte vetorial 2D. STL atende apenas extrusão opcional 3D e não contém parâmetros de potência.

**Consequências:** futura engine deve transformar curvas e offsets em mm e testar fidelidade dimensional; separar largura do stroke, kerf e parâmetros físicos do laser.
