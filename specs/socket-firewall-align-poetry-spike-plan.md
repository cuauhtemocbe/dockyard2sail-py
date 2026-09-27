# Implementation Plan: Align Socket Firewall workflow with the Poetry spike

**Spec**: [socket-firewall-align-poetry-spike.md](socket-firewall-align-poetry-spike.md)
**Created**: 2026-09-26
**Status**: in-progress

## Risks & Assumptions

- **Sin test automatizado posible**: el workflow solo corre con `github.actor == 'dependabot[bot]'`. Se valida con parseo YAML, `poetry export` local en `python:3.14-slim` y comprobación de SHAs con `gh api`.
- **Ruta de bloqueo real sin probar**: igual que en el spike, no se provoca un bloqueo de sfw.

## Tasks

**Slicing strategy**: Vertical — cambios independientes en un solo archivo de CI; se commitean por separado por requisito.

- [x] **Export con grupo dev, sin plugin, Poetry sincronizado** — `.github/workflows/dependabot-socket-firewall.yml` — XS
- [x] **Aislar `poetry export` y documentarlo** — mismo archivo — XS
- [x] **Mensaje de cierre honesto** — mismo archivo — XS
- [x] **CHANGELOG `[Unreleased]`** — XS
