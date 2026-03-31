# Subjects Database - Security & RBAC Specification

## Role-Based Access Control

### User Roles

#### 1. Account Owner
- **Permissions**: Full control over account and all subjects
- **Capabilities**:
  - Criar, ler, atualizar e deletar qualquer subject da conta
  - Visualizar event logs de todos os subjects
  - Compartilhar subjects com outros users
  - Mudar owner de um subject

#### 2. Account Admin
- **Permissions**: Gerenciar subjects pela conta
- **Capabilities**:
  - Criar, ler, atualizar e deletar subjects da conta
  - Visualizar event logs de todos os subjects
  - Gerenciar permissões de subjects

#### 3. Member (Padrão)
- **Permissions**: Só de seus subjects ou compartilhados
- **Capabilities**:
  - Criar seus próprios subjects
  - Ler seus subjects
  - Atualizar seus subjects
  - Deletar seus subjects
  - Ler subjects compartilhados com ele
  - Visualizar event logs de seus subjects

#### 4. Guest / Read-Only
- **Permissions**: Visualização apenas
- **Capabilities**:
  - Ler subjects compartilhados publicamente
  - Não pode criar, editar ou deletar

### Access Control Rules

#### Create Subject
```
if current_user has role member|admin|owner in account:
    owner_id = current_user.id
    account_id = requested_account_id
    if current_user.account_id == requested_account_id:
        allowed = true
    else:
        allowed = false
else:
    allowed = false
```

#### Read Subject
```
if subject.owner_id == current_user.id:
    allowed = true
else if current_user has role admin|owner in account:
    if subject.account_id == current_user.account_id:
        allowed = true
else if subject is shared with current_user:
    allowed = true
else:
    allowed = false
```

#### Update Subject
```
if subject.owner_id == current_user.id:
    allowed = true
    can_change_owner = false
else if current_user has role admin|owner in account:
    allowed = true
    can_change_owner = true
else:
    allowed = false
```

#### Delete Subject
```
if subject.owner_id == current_user.id:
    allowed = true
else if current_user has role admin|owner in account:
    allowed = true
else:
    allowed = false
```

### Data Isolation

- Subjects são sempre isolados por account
- Query filtering automático por `account_id` baseado no user's account
- Owner é sempre o usuário que criou o subject (imutável inicialmente)

### Security Measures

1. **Input Validation**
   - Validar todos os campos de entrada
   - Max length constraints
   - XSS prevention (sanitizar descrições)
   - SQL injection prevention (use parameterized queries / ORM)

2. **Rate Limiting**
   - Apply rate limiting to create/update endpoints
   - 10 creates per minute per user
   - 100 reads per minute per user

3. **Audit Trail**
   - Log todas as mudanças em event_logs
   - Incluir IP address e user agent
   - Manter histórico imutável

4. **Encryption**
   - Sensitive data (descriptions) opcional: encrypt at rest
   - All data encrypted in transit (HTTPS/TLS)

## Authorization Middleware

Implementar middleware que:

1. Valida JWT token
2. Extrai user_id e account_id
3. Para endpoints que referenciam um subject:
   - Valida se user tem acesso ao subject
   - Valida se operation é permitida
4. Retorna 403 se não autorizado
5. Retorna 404 se resource não existe (não leaka existence)

## Testing Requirements

- [ ] Testar acesso negado para users sem permissão
- [ ] Testar isolamento de dados entre contas
- [ ] Testar cambio de roles e verificar access changes
- [ ] Testar owner não pode transferir ownership para non-members
- [ ] Testar event logs properly criados para operações autorizadas
