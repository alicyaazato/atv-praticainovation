# Subjects Database - Design

## Architecture Overview

A tabela `subject` será uma entidade central que conecta disciplinas acadêmicas aos usuários e contas. A arquitetura segue padrões existentes de propriedade, auditoria e acesso.

## Data Model

### Table: subject

```
- id: number (primary key)
- name: string (required) - Nome da disciplina
- description: string - Descrição e ementa da disciplina
- code: string - Código da disciplina (ex: CCNA101)
- owner_id: number (foreign key to user) - Usuário proprietário
- account_id: number (foreign key to account) - Conta à qual pertence
- credits: number - Créditos/carga horária
- semester: string - Semestre (1o, 2o, etc)
- year: number - Ano acadêmico
- status: string - Estado da disciplina (active, archived, draft)
- is_active: boolean - Flag de atividade
- created_at: datetime - Timestamp de criação
- updated_at: datetime - Timestamp de atualização
```

## Relationships

```
subject.owner_id -> user.id
subject.account_id -> account.id
```

## Access Control

- **Owner**: Pode editar, deletar e compartilhar sua disciplina
- **Account Admin**: Pode gerir todas as disciplinas da conta
- **Account Member**: Pode visualizar disciplinas conforme permissões

## Event Logging

Todas as mudanças em `subject` geram eventos via `event_logs`:
- `subject.created`
- `subject.updated`
- `subject.deleted`
- `subject.shared`

## Integration Points

1. **User Management**: Disciplinas linkedadas a usuários proprietários
2. **Account Management**: Disciplinas pertencem a contas
3. **Role-Based Access**: Uso de roles existentes para controle
4. **Event Audit Trail**: Logging automático de mudanças
5. **Future Automations**: Hook points para workflows de disciplinas

## Implementation Strategy

1. **Phase 1**: Criar tabela base com CRUD essencial
2. **Phase 2**: Adicionar RBAC e event logging
3. **Phase 3**: Documentar e testar
