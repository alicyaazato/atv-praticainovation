# Frontend: Status/Semestre da Disciplina e Prioridade da Tarefa - Design

## Dados já disponíveis na API (validado em produção)

`GET /subjects`, `GET /subjects/search`, `POST /subjects`,
`PATCH /subjects/{id}`:

```json
{
  "id": 47,
  "name": "Materia Recheck",
  "professor": "Prof Recheck",
  "CargaHoraria": 6,
  "user_id": 14,
  "status": "rascunho",
  "semester": "2026/1"
}
```

`GET /tasks`, `POST /tasks`, `PATCH /tasks/{id}`:

```json
{
  "id": 21,
  "created_at": 1781234655142,
  "user_id": 14,
  "subject_id": 47,
  "title": "Tarefa Recheck",
  "description": "desc recheck",
  "status": "Pendente",
  "data": "01/04/2026",
  "priority": "Alta"
}
```

Defaults confirmados: subject sem `status`/`semester` -> `"ativo"`/`""`;
task sem `priority` -> `"Media"`.

## `utils/api_client.py` — novos mapas e helper

Mesmo padrão de `STATUS_LABELS`/`STATUS_OPTIONS` (chave ASCII interna,
rótulo acentuado para exibição):

```python
# subject.status -> rótulo exibido
SUBJECT_STATUS_LABELS = {
    "rascunho": "Rascunho",
    "ativo": "Ativo",
    "arquivado": "Arquivado",
}
SUBJECT_STATUS_OPTIONS = list(SUBJECT_STATUS_LABELS.keys())

# academic_task.priority -> rótulo exibido
PRIORITY_LABELS = {
    "Baixa": "Baixa",
    "Media": "Média",
    "Alta": "Alta",
}
PRIORITY_OPTIONS = list(PRIORITY_LABELS.keys())

# ícone/peso para exibição e ordenação
PRIORITY_ICONS = {"Baixa": "🟢", "Media": "🟡", "Alta": "🔴"}
PRIORITY_WEIGHT = {"Baixa": 0, "Media": 1, "Alta": 2}
```

`build_subject_payload()` análogo ao `build_task_payload()` existente
(`utils/api_client.py:198-209`), para que o PATCH de edição sempre envie o
conjunto completo de campos editáveis (evita depender de o backend mesclar
corretamente — embora o `$final_*` já trate isso, manter o mesmo padrão usado
em tarefas por consistência):

```python
def build_subject_payload(subject: dict, **changes) -> dict:
    payload = {
        "name": subject.get("name"),
        "professor": subject.get("professor"),
        "carga_horaria": subject.get("CargaHoraria"),
        "status": subject.get("status"),
        "semester": subject.get("semester"),
    }
    payload.update(changes)
    return payload
```

## Disciplinas (`pages/1_📚_Disciplinas.py`)

### Formulário "Nova Disciplina"

Adicionar, após "Carga Horária":

```python
col_status, col_sem = st.columns(2)
with col_status:
    status_novo = st.selectbox(
        "Status", options=SUBJECT_STATUS_OPTIONS, index=SUBJECT_STATUS_OPTIONS.index("ativo"),
        format_func=lambda s: SUBJECT_STATUS_LABELS[s],
    )
with col_sem:
    semestre_novo = st.text_input("Semestre/Período", placeholder="Ex: 2026/1")
```

Payload de criação passa a incluir `"status": status_novo, "semester":
semestre_novo.strip()`.

### Formulário de edição (dentro do `st.expander` de cada disciplina)

Mesmos dois campos (`new_status`, `new_semester`), com valores atuais como
default. `patch_payload` ganha `status`/`semester` quando alterados — igual
ao padrão já usado para `name`/`professor`/`carga_horaria`
(`pages/1_📚_Disciplinas.py:65-71`).

Botão de atalho ao lado do "💾 Salvar":

```python
if subj.get("status") != "arquivado":
    if st.button("📦 Arquivar", key=f"archive_{subj_id}"):
        update_subject(subj_id, build_subject_payload(subj, status="arquivado"))
        st.session_state.pop("subjects_cache", None)
        st.rerun()
else:
    if st.button("♻️ Reativar", key=f"unarchive_{subj_id}"):
        update_subject(subj_id, build_subject_payload(subj, status="ativo"))
        st.session_state.pop("subjects_cache", None)
        st.rerun()
```

### Aba "Minhas Disciplinas" — filtro por status

Acima da listagem, um `st.selectbox`:

```python
filtro_status = st.selectbox(
    "Mostrar", ["Ativas", "Arquivadas", "Rascunhos", "Todas"], index=0,
)
```

Aplicar antes de iterar `subjects`:

```python
if filtro_status == "Ativas":
    subjects = [s for s in subjects if s.get("status", "ativo") == "ativo"]
elif filtro_status == "Arquivadas":
    subjects = [s for s in subjects if s.get("status") == "arquivado"]
elif filtro_status == "Rascunhos":
    subjects = [s for s in subjects if s.get("status") == "rascunho"]
# "Todas": sem filtro
```

No título do `st.expander`, exibir o semestre quando preenchido:
`f"📘 {subj.get('name', '—')}" + (f" · {subj['semester']}" if
subj.get('semester') else "") + (" 📦" if subj.get('status') ==
"arquivado" else "")`.

### Aba "Buscar"

Adicionar ao label do `st.expander`: status (se != "ativo") e semestre (se
preenchido), reaproveitando a mesma formatação da listagem.

## Tarefas (`pages/2_📝_Tarefas.py`)

### Formulário "Nova Tarefa"

Adicionar seletor de prioridade, default "Media":

```python
prioridade = st.selectbox(
    "Prioridade", options=PRIORITY_OPTIONS,
    index=PRIORITY_OPTIONS.index("Media"),
    format_func=lambda p: PRIORITY_LABELS[p],
)
```

Payload de criação ganha `"priority": prioridade`.

### Aba "Minhas Tarefas"

- Novo filtro `col_d`: `filtro_prioridade = st.selectbox("Prioridade",
  ["Todas"] + list(PRIORITY_LABELS.values()))`, aplicado igual ao filtro de
  status existente (`pages/2_📝_Tarefas.py:93-94`).
- `agrupar_por` ganha a opção `"Prioridade"`: agrupa usando
  `PRIORITY_LABELS.get(t.get("priority", "Media"))`, com a ordem dos grupos
  seguindo `PRIORITY_WEIGHT` decrescente (Alta primeiro).
- No título do expander, prefixar com `PRIORITY_ICONS.get(t.get("priority",
  "Media"))`:
  `titulo_exib = f"{icone} {'🔴 ' if venc else ''}{t.get('title', '—')} ·
  {status_lbl}"`.

### Formulário de edição

Adicionar o mesmo seletor de prioridade (`novo_prioridade`), valor atual via
`PRIORITY_OPTIONS.index(t.get("priority", "Media"))`. `build_task_payload`
ganha `priority=novo_prioridade`.

## Dashboard (`app.py`)

- `subjects_ativas = [s for s in subjects if s.get("status", "ativo") ==
  "ativo"]` — usar essa lista (em vez de `subjects`) para a métrica
  "📚 Disciplinas" (renomear label para "Disciplinas Ativas") e para o cálculo
  de `progress_by_subject`/`progresso_geral` e a seção "Progresso por
  Disciplina". A tela de boas-vindas (`if not subjects`) continua olhando
  para `subjects` (todas), pois um usuário com só rascunhos/arquivadas ainda
  "tem dados".
- Nova seção "Tarefas por Prioridade", ao lado de "Tarefas por Status"
  (`app.py:68-75`), mesmo padrão:

```python
with col_priority:
    st.subheader("Tarefas por Prioridade")
    if not tasks:
        st.caption("Nenhuma tarefa cadastrada ainda.")
    else:
        for p in PRIORITY_OPTIONS:
            count = sum(1 for t in tasks if t.get("priority", "Media") == p)
            st.write(f"{PRIORITY_ICONS[p]} **{PRIORITY_LABELS[p]}:** {count}")
```

Como já existem duas colunas (`col_status`, `col_progress`), a seção de
prioridade entra numa segunda linha de colunas (`col_priority, _ =
st.columns(2)`) para não sobrecarregar a primeira linha.

## Relatórios (`pages/4_📈_Relatorios.py`)

- "Progresso por Disciplina": checkbox `incluir_arquivadas = st.checkbox(
  "Incluir disciplinas arquivadas")` (default `False`); filtrar `subjects`
  por `status == "ativo"` quando desmarcado, antes do loop existente
  (`pages/4_📈_Relatorios.py:41-50`).
- Histórico de tarefas: adicionar `"Prioridade": PRIORITY_LABELS.get(t.get(
  "priority", "Media"), t.get("priority"))` ao dict `linhas`
  (`pages/4_📈_Relatorios.py:88-97`) — aparece automaticamente na tabela e no
  CSV exportado (já usa `linhas[0].keys()` como fieldnames).

## Compatibilidade com dados existentes

Todos os acessos usam `.get("status", "ativo")` / `.get("priority",
"Media")` / `.get("semester", "")` com fallback para o default documentado,
cobrindo tanto registros antigos (já normalizados pelo Xano) quanto qualquer
resposta que omita o campo.
