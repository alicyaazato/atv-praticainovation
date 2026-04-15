## Why

Professores precisam avaliar o trabalho realizado pelos alunos em atividades específicas. Atualmente, não há como registrar notas para cada atividade, impossibilitando a geração de históricos de desempenho e relatórios acadêmicos.

## What Changes

- **Criar tabela `activity_grades`**: Armazena notas lançadas pelos professores para alunos em atividades específicas
- **Nova API POST `/activity_grades`**: Permite que professores registrem notas para atividades

## Capabilities

### New Capabilities
- `activity-grades`: Capacidade de armazenar e recuperar notas de atividades para alunos

### Modified Capabilities
<!-- Nenhuma capacidade existente será modificada -->

## Impact

- **Banco de dados**: Nova tabela `activity_grades` com relacionamento com `users` (aluno), `academic_tasks` (atividade) e `users` (professor)
- **APIs**: Nova endpoint POST para lançar notas
- **Schema**: Requer validação de permissões (apenas professor pode lançar notas)
