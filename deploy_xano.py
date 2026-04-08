#!/usr/bin/env python3
"""
Xano Deployment Tool - Corrigido
Usa a Xano Meta API corretamente para criar tabelas, endpoints e funções.

Uso:
    python deploy_xano.py
    python deploy_xano.py --dry-run
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, List
from dataclasses import dataclass

# ─────────────────────────────────────────────
# CONFIGURAÇÃO — edite aqui ou use variáveis de ambiente
# ─────────────────────────────────────────────

# Instância do seu Xano (domínio base, sem /api:...)
XANO_INSTANCE = os.getenv("XANO_INSTANCE", "x8ki-letl-twmt.n7.xano.io")

# Chave de API (Meta Token) — gere em: Settings → API Keys no Xano
XANO_API_KEY = os.getenv("XANO_API_KEY", "eyJhbGciOiJSUzI1NiJ9.eyJ4YW5vIjp7ImRibyI6Im1hc3Rlcjp1c2VyIiwiaWQiOjE1NjMwMiwibmFtZSI6ImFsaWN5YSBhemF0byIsImVtYWlsIjoiYWxpY3lhLmF6YXRvQGFsdW5vLmltcGFjdGEuZWR1LmJyIiwiYWNjZXNzX3Rva2VuIjp7ImtleWlkIjoiZjRlZTYwYjctZWQ0OS00ZTM2LWEzMTQtM2MyNWQzMWJmOWYyIiwic2NvcGUiOnsidGVuYW50X2NlbnRlcjpiYWNrdXAiOjE1LCJ0ZW5hbnRfY2VudGVyOmRlcGxveSI6MTYsInRlbmFudF9jZW50ZXI6aW1wZXJzb25hdGUiOjE2LCJ0ZW5hbnRfY2VudGVyOm1ldGFkYXRhOmFwaSI6MCwidGVuYW50X2NlbnRlcjpsb2ciOjE2LCJ0ZW5hbnRfY2VudGVyOnJiYWMiOjE2LCJ0ZW5hbnRfY2VudGVyOnNlY3JldHMiOjE1LCJ0ZW5hbnRfY2x1c3RlciI6MTUsInRlbmFudF9jbHVzdGVyOnNlY3JldHMiOjE1LCJ0ZW5hbnRfY2VudGVyIjoxNSwicmVsZWFzZSI6MTUsIndvcmtzcGFjZTphZGRvbiI6MTUsIndvcmtzcGFjZTphcGkiOjE1LCJ3b3Jrc3BhY2U6Y29udGVudCI6MTUsIndvcmtzcGFjZTpkYXRhYmFzZSI6MTUsIndvcmtzcGFjZTpkYXRhc291cmNlOmxpdmUiOjE1LCJ3b3Jrc3BhY2U6ZmlsZSI6MTUsIndvcmtzcGFjZTpmdW5jdGlvbiI6MTUsIndvcmtzcGFjZTpzZXJ2aWNlIjoxNSwid29ya3NwYWNlOmxvZyI6MTUsIndvcmtzcGFjZTptaWRkbGV3YXJlIjoxNSwid29ya3NwYWNlOnJlcXVlc3RoaXN0b3J5IjoxNSwid29ya3NwYWNlOnRhc2siOjE1LCJ3b3Jrc3BhY2U6dG9vbCI6MTUsIndvcmtzcGFjZTpyZWFsdGltZSI6MTUsIndvcmtzcGFjZTp3b3JrZmxvd190ZXN0IjoxNX19fSwiaWF0IjoxNzc1NjExMDcyLCJuYmYiOjE3NzU2MTEwNzIsImF1ZCI6Inhhbm86bWV0YSJ9.vhL6TFv4u1bV_AMd741Rlp8AGB3LaB71UvpMU4FoWORJkfr5GmSGmJplzeXUA68SDn0NaC5ijEYqsGhCxkHCLbH99__gICcyOskxx77zYiOLC-uvPzekUmx-phIsO7nAxApan8zHq8TFlesrbBma3eNRBeiToAO7P2rrVlBUbgAr1PALShVMdwoSt23ygJtstYNc2PLy0sF0a0pmgQBf-GN7JLIFvoyNcGZ-v6o3CbumTq3AAxim9E_RAzPHPqHaZoIremETBrA3BZrsbGG3iQgtPO3ABGwIaGAC36VknyaTz1COerXL8Mv6MOw-VEqw219cTj4iukIq3S5XCJu5-ZqqG7mQZzocOu8Y3aUTSO3fUjghFAFC3lQl2_BXgiyMVVYtULnkkVSOQgxAIm6Ty_i-UvyK1aL56HuXW7rfVLMcp9G2-RtwwePWQvZxw0f-aSHBU_By1_VwY5mNB88T6AZnQOT2hMM-p4jVBUGDzie5S-FFYDnOo84eH1l74bgXCfogRFMAwT6Wh0sgTugEhRf55eoqwYInzIqevDKTRYlGuut8GOwX93zfgyTyE8tguYoUfwXFgFaG-ZR2JgUy8tdH63gBmqe9qAjsR7hU2-W7MrL1zXV-UjMl2ObDDC6iR4kjJpelAEKpzwtPxGdBQPmGPOtg4EHz8_5aPKXz2K0")  # ← coloque sua chave aqui ou no .env

# ID do workspace (número antes do traço, ex: "148838" de "148838-0")
XANO_WORKSPACE_ID = os.getenv("XANO_WORKSPACE_ID", "148838")

# ID do API Group onde os endpoints serão criados (398699 = o que você criou)
XANO_API_GROUP_ID = os.getenv("XANO_API_GROUP_ID", "398699")

# Base da Meta API do Xano
META_BASE = f"https://{XANO_INSTANCE}/api:meta"

# ─────────────────────────────────────────────
# DEFINIÇÃO DOS RECURSOS A CRIAR
# ─────────────────────────────────────────────
 
TABLES_TO_CREATE = [
    {
        "name": "subject",
        "description": "Tabela de disciplinas",
        "fields": [
            {"name": "name",        "type": "text"},
            {"name": "code",        "type": "text"},
            {"name": "description", "type": "text"},
            {"name": "owner_id",    "type": "int"},
            {"name": "account_id",  "type": "int"},
            {"name": "credits",     "type": "decimal"},
            {"name": "semester",    "type": "text"},
            {"name": "year",        "type": "int"},
            {"name": "status",      "type": "text"},
            {"name": "is_active",   "type": "bool"},
        ]
    },
]
 
ENDPOINTS_TO_CREATE = [
    {
        "name":        "Get My Subjects",
        "verb":        "GET",
        "path":        "/subjects/my",
        "description": "List user's subjects with pagination",
        "input": [
            {"name": "page",  "type": "int",  "required": False},
            {"name": "limit", "type": "int",  "required": False},
        ],
    },
    {
        "name":        "Get Subject by ID",
        "verb":        "GET",
        "path":        "/subjects/{id}",
        "description": "Get single subject by ID with RBAC",
        "input": [
            {"name": "id", "type": "int", "required": True},
        ],
    },
    {
        "name":        "Create Subject",
        "verb":        "POST",
        "path":        "/subjects",
        "description": "Create new subject with validation",
        "input": [
            {"name": "name",        "type": "text",    "required": True},
            {"name": "code",        "type": "text",    "required": True},
            {"name": "description", "type": "text",    "required": False},
            {"name": "credits",     "type": "decimal", "required": False},
            {"name": "semester",    "type": "text",    "required": False},
            {"name": "year",        "type": "int",     "required": False},
        ],
    },
    {
        "name":        "Update Subject",
        "verb":        "PATCH",
        "path":        "/subjects/{id}",
        "description": "Update subject with partial data",
        "input": [
            {"name": "id",          "type": "int",  "required": True},
            {"name": "name",        "type": "text", "required": False},
            {"name": "description", "type": "text", "required": False},
            {"name": "status",      "type": "text", "required": False},
        ],
    },
    {
        "name":        "Delete Subject",
        "verb":        "DELETE",
        "path":        "/subjects/{id}",
        "description": "Soft delete subject via trigger",
        "input": [
            {"name": "id", "type": "int", "required": True},
        ],
    },
]
 
 
# ─────────────────────────────────────────────
# DATACLASS DE STATUS
# ─────────────────────────────────────────────
 
@dataclass
class DeployStatus:
    success: bool
    name: str
    kind: str
    message: str
    error: Optional[str] = None
 
 
# ─────────────────────────────────────────────
# DEPLOYER
# ─────────────────────────────────────────────
 
class XanoDeployer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {XANO_API_KEY}",
            "Content-Type": "application/json",
            "X-Branch": "main",          # branch padrão do Xano
        })
        self.results: List[DeployStatus] = []
 
    # ── helpers ──────────────────────────────
 
    def _post(self, url: str, payload: dict):
        resp = self.session.post(url, json=payload)
        return resp
 
    def _get(self, url: str):
        return self.session.get(url)
 
    # ── verificar conexão ─────────────────────
 
    def verify(self) -> bool:
        """Verifica se a API Key e o workspace existem."""
        url = f"{META_BASE}/workspace/{XANO_WORKSPACE_ID}"
        resp = self._get(url)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ Workspace encontrado: {data.get('name', XANO_WORKSPACE_ID)}")
            return True
        else:
            print(f"❌ Falha ao acessar workspace {XANO_WORKSPACE_ID}")
            print(f"   Status: {resp.status_code}")
            print(f"   Resposta: {resp.text}")
            return False
 
    # ── tabelas ───────────────────────────────
 
    def create_table(self, table: dict, dry_run: bool) -> DeployStatus:
        name = table["name"]
        print(f"  📦 Tabela: {name}")
 
        if dry_run:
            return DeployStatus(True, name, "table", "[DRY RUN] Criaria a tabela")
 
        # 1. Criar a tabela
        url = f"{META_BASE}/workspace/{XANO_WORKSPACE_ID}/table"
        payload = {
            "name": name,
            "description": table.get("description", ""),
            "docs": "",
            "tag": [],
        }
        resp = self._post(url, payload)
 
        if resp.status_code not in (200, 201):
            err = resp.json() if resp.text else {}
            if "already being used" in err.get("message", ""):
                print(f"     ⚠️  Tabela '{name}' já existe — pulando")
                return DeployStatus(True, name, "table", "⚠️  Já existia, pulado")
            return DeployStatus(False, name, "table", "❌ Falha ao criar tabela", resp.text)
 
        table_id = resp.json().get("id")
        print(f"     ✅ Tabela criada (ID: {table_id})")
 
        # 2. Adicionar campos
        for field in table.get("fields", []):
            field_url = f"{META_BASE}/workspace/{XANO_WORKSPACE_ID}/table/{table_id}/field"
            field_payload = {
                "name": field["name"],
                "type": field["type"],
                "nullable": True,
                "default": None,
            }
            fr = self._post(field_url, field_payload)
            if fr.status_code in (200, 201):
                print(f"     ✅ Campo '{field['name']}' adicionado")
            else:
                print(f"     ⚠️  Campo '{field['name']}' falhou: {fr.text}")
 
        return DeployStatus(True, name, "table", "✅ Tabela criada com sucesso")
 
    # ── endpoints ─────────────────────────────
 
    def create_endpoint(self, ep: dict, dry_run: bool) -> DeployStatus:
        label = f"{ep['verb']} {ep['path']}"
        print(f"  🔌 Endpoint: {label}")
 
        if dry_run:
            return DeployStatus(True, label, "endpoint", "[DRY RUN] Criaria o endpoint")
 
        url = f"{META_BASE}/workspace/{XANO_WORKSPACE_ID}/apigroup/{XANO_API_GROUP_ID}/api"
        payload = {
            "name":        ep["name"],
            "verb":        ep["verb"],
            "path":        ep["path"],
            "description": ep.get("description", ""),
            "input":       ep.get("input", []),
            "tag":         [],
            "docs":        "",
        }
        resp = self._post(url, payload)
 
        if resp.status_code in (200, 201):
            ep_id = resp.json().get("id", "?")
            print(f"     ✅ Endpoint criado (ID: {ep_id})")
            return DeployStatus(True, label, "endpoint", f"✅ Criado (ID: {ep_id})")
        else:
            return DeployStatus(False, label, "endpoint", "❌ Falha ao criar endpoint", resp.text)
 
    # ── deploy completo ───────────────────────
 
    def deploy_all(self, dry_run: bool = False):
        print("\n" + "="*60)
        print("🚀 Xano Deployment — Subjects")
        print("="*60)
        if dry_run:
            print("⚠️  DRY RUN — nenhuma alteração será feita\n")
 
        # Tabelas
        print("\n📊 1. Criando tabelas...")
        for table in TABLES_TO_CREATE:
            status = self.create_table(table, dry_run)
            self.results.append(status)
 
        # Endpoints
        print("\n🔌 2. Criando endpoints no API Group", XANO_API_GROUP_ID, "...")
        for ep in ENDPOINTS_TO_CREATE:
            status = self.create_endpoint(ep, dry_run)
            self.results.append(status)
 
        self._print_summary()
 
    def _print_summary(self):
        total = len(self.results)
        ok = sum(1 for r in self.results if r.success)
        fail = total - ok
 
        print("\n" + "="*60)
        print("📋 RESUMO DO DEPLOY")
        print("="*60)
        print(f"Total:      {total}")
        print(f"Sucesso:    {ok} ✅")
        print(f"Falhas:     {fail} ❌")
        print("="*60)
 
        if fail:
            print("\nItens com falha:")
            for r in self.results:
                if not r.success:
                    print(f"  ❌ [{r.kind}] {r.name}")
                    if r.error:
                        print(f"     Erro: {r.error}")
 
 
# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
 
def main():
    parser = argparse.ArgumentParser(description="Deploy Subjects no Xano")
    parser.add_argument("--dry-run", action="store_true",
                        help="Mostra o que seria feito sem executar")
    args = parser.parse_args()
 
    if not XANO_API_KEY:
        print("❌ XANO_API_KEY não configurada.")
        print("   Defina no arquivo ou via: export XANO_API_KEY='sua_chave'")
        sys.exit(1)
 
    deployer = XanoDeployer()
 
    print(f"🔧 Configuração:")
    print(f"   Instância:   {XANO_INSTANCE}")
    print(f"   Workspace:   {XANO_WORKSPACE_ID}")
    print(f"   API Group:   {XANO_API_GROUP_ID}")
    print(f"   API Key:     {'*' * (len(XANO_API_KEY)-4) + XANO_API_KEY[-4:]}\n")
 
    if not deployer.verify():
        print("\n💡 Dica: verifique se a XANO_API_KEY é um Meta Token (não um Auth Token de usuário).")
        print("   Gere em: Xano → Settings → API Keys")
        sys.exit(1)
 
    deployer.deploy_all(dry_run=args.dry_run)
    ok = all(r.success for r in deployer.results)
    sys.exit(0 if ok else 1)
 
 
if __name__ == "__main__":
    main()