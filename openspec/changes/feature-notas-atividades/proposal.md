# Activity Grades - Proposal

## Summary

Criar um sistema de lançamento de notas que permita ao professor registrar avaliações de alunos em atividades específicas, com suporte a comentários/feedback, auditoria completa e isolamento multi-tenant.

## Problem

Atualmente, o sistema permite gerenciar disciplinas (subjects) e tarefas (academic_tasks), mas não possui:
- Uma forma estruturada para o professor lançar notas individuais por aluno e atividade
- Rastreamento de quem deu a nota e quando
- Possibilidade de fornecer feedback/comentários junto com a nota
- Auditoria de mudanças de notas
- Isolamento adequado por conta (multi-tenant) e controle de acesso por papel

## Solution

Implementar um sistema de lançamento de notas (`activity_grades`) que:
- Associa alunos, atividades e notas com propriedade clara (professor = owner)
- Suporta escala numérica configurável e comentários
- Integra automaticamente com event_logs para auditoria
- Enforce RBAC: apenas o professor dono da atividade (via subject) pode lançar/editar notas
- Implementa 5 endpoints CRUD RESTful com validação e proteção
- Mantém isolamento multi-tenant via account_id

## Goals

- ✅ Criar tabela `activity_grade` no banco de dados
- ✅ Associar nota ao professor (via owner_id ou professor_id)
- ✅ Implementar RBAC para garantir que apenas o professor dono possa lançar notas
- ✅ Criar 5 endpoints CRUD (`GET`, `POST`, `PATCH`, `DELETE`, `GET my`)
- ✅ Implementar auditoria automática de todas as mudanças via event_logs
- ✅ Suportar feedback/comentários junto com a nota
- ✅ Validar ranges de notas e dados obrigatórios
- ✅ Preparar infraestrutura para futuras automações (notificações, cálculo de médias)

## Non-Goals

- Implementar cálculo automático de média geral (para depois)
- Criar automações de notificação por email (para depois)
- Implementar soft-delete de notas (apenas deletar, sem archive)
- Criar dashboard de visualização de notas (frontend, para depois)
- Implementar importação em lote de notas (para depois)
