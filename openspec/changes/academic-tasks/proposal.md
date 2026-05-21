# Academic Tasks Database - Proposal

## Summary

Criar uma base de dados robusta para academic_tasks (tarefas acadêmicas) que permita a cada aluno registrar e gerenciar suas obrigações acadêmicas (lições, provas, trabalhos) vinculadas a cada disciplina, com suporte a rastreamento de status e prazos.

## Problem

Atualmente, o sistema não possui uma estrutura adequada para gerenciar tarefas acadêmicas. Isso impede que:
- Alunos organizem suas obrigações acadêmicas de forma estruturada
- O sistema implemente rastreamento de prazos (deadlines)
- Haja integração com disciplinas (subjects) para contexto acadêmico
- Professores ou tutores visualizem status de tarefas dos alunos
- Automações futuras de notificações e lembretes funcionem

## Solution

Implementar uma nova tabela `academic_task` no banco de dados com:
- Propriedade claramente definida (owned_by user)
- Campos essenciais para tarefas acadêmicas (título, descrição, data de vencimento, status)
- Relacionamento com disciplinas (subject_id)
- Suporte a rastreamento de status (pendente, em progresso, concluído)
- Suporte a auditoria e logging de eventos
- Permissões de acesso baseadas em propriedade

## Goals

- ✅ Criar tabela `academic_task` no banco de dados
- ✅ Definir propriedade de cada tarefa (user_id)
- ✅ Implementar relacionamento com subjects
- ✅ Implementar auditoria automática via event_logs
- ✅ Preparar infraestrutura para APIs de gerenciamento de tarefas
- ✅ Estabelecer controles de acesso baseados em propriedade

## Non-Goals

- Criar APIs de CRUD nesta fase
- Implementar automações de notificações/lembretes
- Criar interface de UI nesta fase
- Implementar compartilhamento de tarefas
- Definir workflow de aprovação de tarefas
