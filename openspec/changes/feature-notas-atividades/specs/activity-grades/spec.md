# activity-grades Specification

## Purpose

Define the complete requirements for the activity grades system, enabling professors to assign grades to students for academic tasks with proper access control, auditoria, and multi-tenant isolation.

## ADDED Requirements

### Requirement: Tabela activity_grade com campos obrigatórios
Sistema SHALL armazenar informações de notas de atividades com campos definidos no schema.

#### Scenario: Criar nota com dados obrigatórios
- **WHEN** professor cria nova nota com account_id, activity_id, student_id, professor_id e grade
- **THEN** sistema armazena a nota com timestamps auto-gerenciados

### Requirement: Validar range de notas
Sistema SHALL rejeitar notas fora do intervalo [0.0, 10.0].

#### Scenario: Rejeitar nota inválida
- **WHEN** professor tenta criar nota com grade = 15.0
- **THEN** sistema retorna erro 400 (INVALID_GRADE_VALUE)

#### Scenario: Aceitar nota válida
- **WHEN** professor cria nota com grade = 8.5
- **THEN** sistema armazena com sucesso

### Requirement: Enforce propriedade de professor (RBAC)
Sistema SHALL permitir que apenas o professor dono da atividade (via subject ownership) lance notas.

#### Scenario: Professor dono cria nota
- **WHEN** professor_id é dono da subject que contém a activity
- **THEN** sistema permite criação da nota

#### Scenario: Professor não-dono é bloqueado
- **WHEN** professor_id tenta lançar nota em atividade que não é sua
- **THEN** sistema retorna erro 403 (FORBIDDEN)

### Requirement: Admin pode contornar RBAC
Sistema SHALL permitir admins criarem e editarem notas de qualquer atividade.

#### Scenario: Admin cria nota em atividade de outro professor
- **WHEN** user.role = "admin" cria nota em activity_id de outro professor
- **THEN** sistema permite operação

### Requirement: Isolamento multi-tenant
Sistema SHALL filtrar notas por account_id do usuário autenticado.

#### Scenario: Usuário vê apenas notas de sua conta
- **WHEN** user.account_id = 100 executa GET /activity-grades
- **THEN** sistema retorna apenas notas com account_id = 100

### Requirement: Prevenir dupla-nota
Sistema SHALL rejeitar criação de segunda nota para mesmo student+activity.

#### Scenario: Tentar criar segunda nota para aluno+atividade
- **WHEN** existe activity_grade com account_id=100, activity_id=5, student_id=10
- **THEN** tentar criar outra retorna erro 409 (DUPLICATE_GRADE)

### Requirement: Validar relacionamentos
Sistema SHALL validar que student_id, activity_id e professor_id existem e estão ativos.

#### Scenario: Atividade não existe
- **WHEN** professor tenta criar nota com activity_id inexistente
- **THEN** sistema retorna erro 404 (ACTIVITY_NOT_FOUND)

#### Scenario: Estudante não existe
- **WHEN** professor tenta criar nota com student_id inexistente
- **THEN** sistema retorna erro 404 (STUDENT_NOT_FOUND)

### Requirement: Endpoint GET /activity-grades - Listar
Sistema SHALL retornar lista de notas com paginação e filtros.

#### Scenario: Listar notas (admin)
- **WHEN** admin executa GET /activity-grades com limit=50
- **THEN** sistema retorna array com até 50 notas da conta + metadados de paginação

#### Scenario: Listar notas do professor (próprias)
- **WHEN** professor executa GET /activity-grades
- **THEN** sistema retorna apenas notas onde professor_id = auth.user_id

#### Scenario: Paginação com offset
- **WHEN** cliente executa GET /activity-grades?limit=10&offset=20
- **THEN** sistema retorna notas 21-30

### Requirement: Endpoint POST /activity-grades - Criar
Sistema SHALL criar nova nota com validação completa.

#### Scenario: Criar nota com dados válidos
- **WHEN** professor POST {account_id, activity_id, student_id, professor_id, grade, feedback?}
- **THEN** sistema cria nota, retorna 201 + objeto criado, loga em event_log

### Requirement: Endpoint GET /activity-grades/{id} - Consultar
Sistema SHALL retornar nota específica com validação de acesso.

#### Scenario: Consultar nota própria
- **WHEN** professor GET /activity-grades/42 e é dono
- **THEN** sistema retorna nota com grade + feedback

#### Scenario: Aluno consulta sua nota
- **WHEN** student GET /activity-grades/42 e é student_id
- **THEN** sistema retorna nota (SEM metadata de auditoria sensível)

#### Scenario: Acesso negado
- **WHEN** usuario sem permissão GET /activity-grades/42
- **THEN** sistema retorna 403 (UNAUTHORIZED)

### Requirement: Endpoint PATCH /activity-grades/{id} - Atualizar
Sistema SHALL permitir atualização com registro de mudanças.

#### Scenario: Atualizar grade e feedback
- **WHEN** professor PATCH /activity-grades/42 {grade: 9.5, feedback: "Excelente!"}
- **THEN** sistema atualiza, retorna 200 + nota atualizada, loga alteração em event_log

#### Scenario: Validar nova grade
- **WHEN** professor PATCH com grade = -1.0
- **THEN** sistema rejeita com erro 400 (INVALID_GRADE_VALUE)

### Requirement: Endpoint DELETE /activity-grades/{id} - Deletar
Sistema SHALL suportar deleção com auditoria.

#### Scenario: Deletar nota própria
- **WHEN** professor DELETE /activity-grades/42 (note que é dono)
- **THEN** sistema deleta, retorna 204, loga deleção em event_log

#### Scenario: Admin deleta nota de outro professor
- **WHEN** admin DELETE /activity-grades/42
- **THEN** sistema deleta, retorna 204

### Requirement: Feedback opcional
Sistema SHALL permitir comentários/feedback junto com a nota.

#### Scenario: Criar nota com feedback
- **WHEN** professor cria nota com feedback = "Revise a questão 3"
- **THEN** sistema armazena feedback junto com grade

#### Scenario: Atualizar apenas feedback
- **WHEN** professor PATCH /activity-grades/42 {feedback: "Nota revisada"}
- **THEN** sistema atualiza feedback sem alterar grade

### Requirement: Event logging automático
Sistema SHALL registrar todas as operações em event_log.

#### Scenario: Log de criação
- **WHEN** professor cria nota
- **THEN** sistema cria event_log com action="activity_grade_created", metadata={activity_id, student_id, grade}

#### Scenario: Log de atualização
- **WHEN** professor atualiza grade de 7.0 para 8.0
- **THEN** sistema cria event_log com action="activity_grade_updated", metadata={grade_old: 7.0, grade_new: 8.0}

#### Scenario: Log de deleção
- **WHEN** professor deleta nota
- **THEN** sistema cria event_log com action="activity_grade_deleted", metadata={activity_id, student_id}

### Requirement: Timestamps auto-gerenciados
Sistema SHALL manter created_at e updated_at automaticamente.

#### Scenario: created_at é imutável
- **WHEN** nota é criada em 2026-05-19 14:30:00
- **THEN** created_at permanece 2026-05-19 14:30:00 mesmo após updates

#### Scenario: updated_at atualiza em cada mudança
- **WHEN** nota é atualizada
- **THEN** updated_at é setado para timestamp atual

### Requirement: Rastreabilidade de auditoria
Sistema SHALL manter created_by e updated_by para rastreamento.

#### Scenario: Rastrear criador
- **WHEN** professor_id=5 cria nota
- **THEN** created_by=5 é armazenado

#### Scenario: Rastrear atualizador
- **WHEN** professor_id=5 atualiza nota criada por professor_id=3
- **THEN** updated_by=5 é atualizado, created_by permanece 3

### Requirement: Endpoint GET /activity-grades/activity/{activity_id} - Notas por atividade
Sistema SHALL retornar todas as notas de uma atividade.

#### Scenario: Professor consulta notas de sua atividade
- **WHEN** professor GET /activity-grades/activity/50
- **THEN** sistema retorna array com todas as notas da atividade (apenas se dono)

#### Scenario: Admin consulta notas de qualquer atividade
- **WHEN** admin GET /activity-grades/activity/50
- **THEN** sistema retorna todas as notas da atividade

### Requirement: Endpoint GET /activity-grades/my-grades - Minhas notas
Sistema SHALL retornar notas recebidas pelo aluno autenticado.

#### Scenario: Aluno consulta suas notas
- **WHEN** student GET /activity-grades/my-grades
- **THEN** sistema retorna array de notas onde student_id = auth.user_id (SEM feedback opcional/comentários sensíveis por padrão)

#### Scenario: Paginação de minhas notas
- **WHEN** aluno GET /activity-grades/my-grades?limit=20&offset=0
- **THEN** sistema retorna primeiras 20 notas

### Requirement: Validar dados obrigatórios
Sistema SHALL rejeitar requests faltando campos obrigatórios.

#### Scenario: Criar sem account_id
- **WHEN** POST /activity-grades {activity_id, student_id, professor_id, grade} (falta account_id)
- **THEN** sistema retorna 400 (REQUIRED_FIELDS_MISSING)

#### Scenario: Criar sem grade
- **WHEN** POST /activity-grades {account_id, activity_id, student_id, professor_id} (falta grade)
- **THEN** sistema retorna 400 (REQUIRED_FIELDS_MISSING)

### Requirement: Não permitir professor como estudante
Sistema SHALL rejeitar notas onde professor_id = student_id.

#### Scenario: Professor tenta dar nota para si mesmo
- **WHEN** professor POST com professor_id=5, student_id=5
- **THEN** sistema retorna 400 (INVALID_SELF_GRADE)
