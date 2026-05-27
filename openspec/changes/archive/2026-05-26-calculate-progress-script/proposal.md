# Calculate Progress Script - Proposal

## Summary

Implementar um script Python (`scripts/calculate_progress.py`) que calcula a porcentagem de progresso de um aluno em uma disciplina, dividindo tarefas concluídas pelo total de tarefas, e retorna os resultados em formato JSON estruturado.

## Problem

Atualmente, o sistema não possui um mecanismo centralizado e reutilizável para:
- Calcular progresso por disciplina (subjects)
- Agregar dados de tarefas acadêmicas (academic_tasks) de forma eficiente
- Fornecer resultados em formato JSON para integração com APIs e frontend
- Suportar filtros de data, status e disciplina
- Lidar com casos edge (sem tarefas, todas concluídas, etc.)
- Validar dados antes de retornar resultados

## Solution

Criar um módulo Python que:
- Conecta ao banco de dados Xano via API ou query local
- Calcula progresso como: `(completed_tasks / total_tasks) * 100`
- Retorna JSON estruturado com:
  - Porcentagem de progresso
  - Contagem de tarefas (concluídas, pendentes, total)
  - Informações da disciplina
  - Timestamps e metadados
- Suporta múltiplos usuários, disciplinas e períodos
- Inclui validação e tratamento de erros
- Permite reutilização em APIs e relatórios

## Goals

- ✅ Criar arquivo `scripts/calculate_progress.py` com função principal
- ✅ Implementar lógica de cálculo de progresso (completed/total)
- ✅ Suportar filtros por user_id, subject_id e date range
- ✅ Retornar JSON estruturado e validado
- ✅ Implementar tratamento robusto de erros
- ✅ Suportar múltiplos cenários (sem tarefas, tudo concluído, etc.)
- ✅ Documentar função com examples de uso e retorno
- ✅ Preparar para integração com APIs de relatórios

## Non-Goals

- Implementar UI/endpoint de API nesta fase
- Criar dashboard interativo de progresso
- Implementar histórico de progresso por data
- Suportar importação/exportação de arquivos
- Criar automações de notificações baseadas em progresso
- Implementar cache ou otimizações de performance (primeira versão)

## Success Criteria

- [ ] Script executa sem erros com dados válidos
- [ ] Retorna JSON bem-formado seguindo schema definido
- [ ] Trata corretamente casos edge (0 tarefas, 100% concluído, etc.)
- [ ] Valida inputs (user_id, subject_id, dates existentes)
- [ ] Documentação clara com exemplos de uso
- [ ] Pronto para integração com APIs existentes
