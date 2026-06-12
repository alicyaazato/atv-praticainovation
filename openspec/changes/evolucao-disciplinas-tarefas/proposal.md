# Evolução das Disciplinas e Tarefas - Proposal

## Summary

Documentar as mudanças necessárias **no Xano** (tabelas e endpoints) para
destravar os itens da seção "🏠 Propostas de Melhoria → Evolução das
Disciplinas e Tarefas" do `checklist.md`, além de corrigir o link de
redefinição de senha enviado por e-mail. Esta proposta **não implementa**
nada — é o roteiro para a segunda etapa (configuração do ambiente Xano).

## Problem

O front-end (Streamlit) já está pronto para consumir as funcionalidades
abaixo, mas o backend (Xano) ainda não suporta:

- **Status da disciplina** (rascunho / ativo / arquivado): não existe campo
  `status` em `tables/809944_subject.xs`. Sem ele não é possível "arquivar"
  uma disciplina nem filtrar por disciplinas ativas no Dashboard.
- **Semestre/período da disciplina**: não existe campo `semester`/`periodo`
  em `tables/809944_subject.xs`. Sem ele não é possível agrupar/exibir
  disciplinas por período.
- **Prioridade da tarefa** (Baixa / Média / Alta): não existe campo
  `priority` em `tables/842368_academic_task.xs`. Sem ele não é possível
  ordenar/destacar tarefas por prioridade.
- **Divergência de valores de status**: `tables/842368_academic_task.xs`
  define o enum `status` em inglês (`pending`, `in_progress`, `completed`,
  `overdue`), enquanto o front-end (`utils/api_client.STATUS_LABELS`) usa
  chaves em português (`Pendente`, `Em_progresso`, `Completa`, `Atrasada`).
  O front funciona hoje porque os dados gravados usam as chaves em
  português — mas o schema documentado está desatualizado/divergente. Isso
  precisa ser conciliado antes de implementar qualquer filtro novo baseado
  em `status` (ex.: "disciplinas ativas" + "tarefas pendentes" cruzados).
- **Link de redefinição de senha**: `apis/authentication/3600536_reset_request_reset_link_GET.xs`
  envia um e-mail cujo link aponta para uma página de demonstração do Xano,
  em vez da página **👤 Perfil** do app Streamlit (que já está pronta para
  receber `?magic_token=...&email=...` e concluir o login, implementado em
  `pages/3_👤_Perfil.py`).

## Solution

1. Adicionar `status` (enum: `rascunho`, `ativo`, `arquivado`, default
   `ativo`) e `semester`/`periodo` (texto, opcional) em `subject`.
2. Atualizar `apis/subjects/subjects_POST.xs` e o futuro
   `subjects_id_PATCH.xs` para aceitar e validar os novos campos.
3. Adicionar `priority` (enum: `Baixa`, `Média`, `Alta`, default `Média`) em
   `academic_task`.
4. Atualizar `apis/tasks/tasks_POST.xs` e `tasks_id_PATCH.xs` para aceitar e
   validar o novo campo.
5. Conciliar os valores do enum `status` de `academic_task`: confirmar no
   Xano quais valores estão realmente gravados hoje e alinhar
   `tables/842368_academic_task.xs` com `utils/api_client.STATUS_LABELS`
   (ou vice-versa), documentando a fonte da verdade.
6. Corrigir o template de e-mail em
   `apis/authentication/3600536_reset_request_reset_link_GET.xs` para que o
   link aponte para a URL pública do app Streamlit (página **Perfil**) com
   os parâmetros `magic_token` e `email`.

## Goals

- Especificar os novos campos (`subject.status`, `subject.semester`,
  `academic_task.priority`) com tipos, valores padrão e enums.
- Especificar quais endpoints (`.xs`) precisam ser atualizados e como.
- Documentar o passo de conciliação do enum `status` de `academic_task`.
- Especificar a correção da URL no template de e-mail de redefinição de
  senha.

## Non-Goals

- Implementar os campos/endpoints no Xano nesta etapa.
- Alterar o front-end além do que já foi feito (o front já está preparado
  para consumir esses campos quando existirem).
- Implementar notificações, automações ou regras de negócio adicionais.
