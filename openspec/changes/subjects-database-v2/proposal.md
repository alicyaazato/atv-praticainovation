# Subjects Database - Proposal

## Summary

Criar uma base de dados robusta para subjects (disciplinas acadêmicas) que permita a cada usuário registrar e gerenciar suas disciplinas com propriedade definida, além de viabilizar controles de acesso granulares e futuras automações.

## Problem

Atualmente, o sistema não possui uma estrutura adequada para gerenciar disciplinas acadêmicas. Isso impede que:
- Usuários organizem suas disciplinas de forma estruturada
- Professores tenham controle sobre suas disciplinas
- O sistema implemente automações relacionadas a disciplinas
- Haja auditoria e controle de acesso apropriados para dados acadêmicos

## Solution

Implementar uma nova tabela `subject` no banco de dados com:
- Propriedade claramente definida (owned_by user)
- Campos essenciais para disciplinas acadêmicas
- Relacionamentos com outros recursos (accounts, users, event_logs)
- Suporte a auditoria e logging de eventos
- Permissões de acesso baseadas em propriedade e role

## Goals

- ✅ Criar tabela `subject` no banco de dados
- ✅ Definir propriedade de cada disciplina (owner)
- ✅ Implementar auditoria automática via event_logs
- ✅ Preparar infraestrutura para automações futuras
- ✅ Estabelecer controles de acesso baseados em propriedade

## Non-Goals

- Criar APIs de soft-delete ou cascata deletions agora
- Implementar automações específicas de disciplinas
- Criar interface de UI nesta fase
- Definir workflow de aprovação de disciplinas
