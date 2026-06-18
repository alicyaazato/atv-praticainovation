# EduTrack AI

Sistema de acompanhamento acadêmico: gerencie disciplinas, tarefas e progresso estudantil com uma interface web simples e intuitiva.

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Frontend | [Streamlit](https://streamlit.io/) |
| Backend / API | [Xano](https://www.xano.com/) |
| Autenticação | JWT via Xano |
| Linguagem | Python 3.10+ |

---

## Pré-requisitos

- **Python 3.10 ou superior** — [download](https://www.python.org/downloads/)
- **Git** — para clonar o repositório

---

## Instalação e execução local

### 1. Clone o repositório

```bash
git clone https://github.com/alicyaazato/atv-praticainovation.git
cd atv-praticainovation
```

### 2. Crie e ative o ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o app

```bash
streamlit run app.py
```

O app abrirá automaticamente no navegador em `http://localhost:8501`.

---

## Estrutura do projeto

```
atv-praticainovation/
├── app.py                     # Entrada principal + Dashboard
├── requirements.txt
├── .streamlit/
│   └── config.toml            # Tema e configurações visuais
├── pages/
│   ├── 1_📚_Disciplinas.py    # Gestão de disciplinas
│   ├── 2_📝_Tarefas.py        # Gestão de tarefas
│   ├── 3_👤_Perfil.py         # Login, cadastro e perfil
│   └── 4_📈_Relatorios.py     # Relatórios e exportação CSV
└── utils/
    ├── api_client.py           # Acesso à API Xano + helpers
    └── ui.py                   # Estilos e componentes compartilhados
```

---

## Funcionalidades principais

- Cadastro e login com autenticação via token
- Gestão completa de disciplinas (CRUD, semestre, status, arquivar)
- Gestão de tarefas com prioridade, prazo e status automático
- Dashboard com métricas, progresso e próximas tarefas
- Relatórios com histórico por período e exportação em CSV
- Redefinição de senha por código de verificação enviado por e-mail

---

## Equipe

Projeto desenvolvido para a disciplina de Prática Inovação — Impacta Tecnologia.
