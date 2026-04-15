## Context

O projeto EduTrack AI utiliza Xano como backend (XanoScript) e Streamlit como frontend (Python). Atualmente, não existe capacidade de registrar notas para atividades específicas. Professores precisam avaliar alunos, mas o sistema não fornece interface ou armazenamento para isso.

**Stakeholders:**
- Professores: Lançam notas
- Alunos: Podem consultar próprias notas (futuro)
- Administradores: Gerenciam dados acadêmicos

## Goals / Non-Goals

**Goals:**
- Criar estrutura de dados para armazenar notas de atividades
- Implementar API REST para professores lançarem notas
- Validar permissões (apenas professor pode lançar notas em sua disciplina)
- Suportar valores numéricos de notas com validação de intervalo

**Non-Goals:**
- Consulta/listagem de notas (podem ser adicionadas posteriormente)
- Cálculo automático de média (fora do escopo inicial)
- Integração com relatórios ou exportação
- Feedback ou comentários nas notas

## Decisions

**Decision 1: Estrutura da tabela `activity_grades`**
- **Choice**: Tabela separada com foreign keys para `users` (aluno), `academic_tasks` (atividade), `users` (professor)
- **Rationale**: Permite rastrear quem lançou nota, em qual atividade, para qual aluno. Facilita auditoria e consultas futuras.
- **Alternative considered**: Armazenar notas dentro de `academic_tasks` - rejeitado pois não escalaria para múltiplos alunos por atividade

**Decision 2: Validação de permissões**
- **Choice**: Implementar check no aplicativo XanoScript: professor só pode lançar notas em tarefas de sua própria disciplina
- **Rationale**: Alinha com segurança no Xano. Reusa lógica de autorização existente.

**Decision 3: Endpoint de lançamento**
- **Choice**: POST `/activity_grades` com validação de escala numérica na API
- **Rationale**: Padrão REST. Facilita futuras extensões (GET, PATCH, DELETE)

## Risks / Trade-offs

- **[Risk] Sem histórico de alterações**: Uma vez lançada, nota não registra quem alterou. → **Mitigation**: Adicionar campo `updated_at` e futuro changelog se necessário
- **[Risk] Sem validação de escala**: O projeto pode usar diferentes escalas (0-10, 0-100). → **Mitigation**: Deixar campo numérico flexível; validação de regra de negócio fica para aplicação frontend
- **[Risk] Professor pode lançar nota duplicada**: Sem constraint UNIQUE. → **Mitigation**: Frontend valida; backend pode adicionar índice composto (task_id, user_id) se necessário

## Migration Plan

1. Criar tabela `activity_grades` no Xano
2. Criar função auxiliar de validação de permissões  
3. Criar API POST `/activity_grades` com tratamento de erro
4. Testar endpoint (cenários happy path e erro)
5. Documentar para consumo no frontend Streamlit

Rollback: Remover tabela e endpoint (sem dados em produção ainda)

## Open Questions

- Escala de notas será validada no frontend ou backend?
- Será permitido ao professor editar/deletar notas já lançadas? (Fora do escopo atual)
