#!/usr/bin/env python3
"""
XanoScript Deployment Tool
Deploy Subject Database changes from Stage to Xano Production

Usage:
    python deploy_xano.py --environment production
    python deploy_xano.py --dry-run
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# Configuration
XANO_API_BASE = os.getenv("XANO_API_BASE", "https://api.xano.io/v1")
XANO_WORKSPACE_ID = os.getenv("XANO_WORKSPACE_ID", "edutrack-ai")
XANO_API_KEY = os.getenv("XANO_API_KEY", "")

# Files to deploy
DEPLOY_MANIFEST = {
    "tables": [
        {
            "id": "753426",
            "name": "subject",
            "type": "table",
            "path": "atv2Lab/tables/753426_subject.xs",
            "description": "Subject (Discipline) table with 14 fields"
        },
        {
            "id": "754426",
            "name": "subject_triggers",
            "type": "triggers",
            "path": "atv2Lab/tables/triggers/754426_subject_triggers.xs",
            "description": "Subject triggers for auditoria (6 triggers)"
        }
    ],
    "endpoints": [
        {
            "id": "3600550",
            "path": "GET /subjects/my",
            "type": "endpoint",
            "file": "atv2Lab/apis/subjects/3600550_subjects_my_GET.xs",
            "description": "List user's subjects with pagination"
        },
        {
            "id": "3600551",
            "path": "GET /subjects/{id}",
            "type": "endpoint",
            "file": "atv2Lab/apis/subjects/3600551_subjects_id_GET.xs",
            "description": "Get single subject by ID with RBAC"
        },
        {
            "id": "3600552",
            "path": "POST /subjects",
            "type": "endpoint",
            "file": "atv2Lab/apis/subjects/3600552_subjects_POST.xs",
            "description": "Create new subject with validation"
        },
        {
            "id": "3600553",
            "path": "PATCH /subjects/{id}",
            "type": "endpoint",
            "file": "atv2Lab/apis/subjects/3600553_subjects_id_PATCH.xs",
            "description": "Update subject with partial data"
        },
        {
            "id": "3600554",
            "path": "DELETE /subjects/{id}",
            "type": "endpoint",
            "file": "atv2Lab/apis/subjects/3600554_subjects_id_DELETE.xs",
            "description": "Delete subject (soft delete via trigger)"
        },
        {
            "id": "subjects_api_group",
            "path": "API Group: Subjects",
            "type": "api_group",
            "file": "atv2Lab/apis/subjects/api_group.xs",
            "description": "API group for subjects resources"
        }
    ],
    "functions": [
        {
            "id": "269538",
            "name": "check_subject_access",
            "type": "function",
            "file": "atv2Lab/functions/getting_started_template/269538_check_subject_access.xs",
            "description": "RBAC access control for subjects"
        }
    ]
}


@dataclass
class DeployStatus:
    success: bool
    item_id: str
    item_name: str
    item_type: str
    message: str
    error: Optional[str] = None


class XanoDeployer:
    def __init__(self, api_key: str, workspace_id: str = XANO_WORKSPACE_ID):
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
        self.results: List[DeployStatus] = []

    def deploy_table(self, table_id: str, table_name: str, dry_run: bool = False) -> DeployStatus:
        """Deploy a database table to production"""
        print(f"  📦 Deploying table: {table_name} (ID: {table_id})")
        
        if dry_run:
            return DeployStatus(
                success=True,
                item_id=table_id,
                item_name=table_name,
                item_type="table",
                message="[DRY RUN] Would deploy table"
            )

        try:
            endpoint = f"{XANO_API_BASE}/tables/{table_id}/deploy"
            payload = {
                "workspace_id": self.workspace_id,
                "environment": "production",
                "action": "deploy"
            }
            
            response = self.session.post(endpoint, json=payload)
            
            if response.status_code in [200, 201]:
                return DeployStatus(
                    success=True,
                    item_id=table_id,
                    item_name=table_name,
                    item_type="table",
                    message=f"✅ Successfully deployed"
                )
            else:
                return DeployStatus(
                    success=False,
                    item_id=table_id,
                    item_name=table_name,
                    item_type="table",
                    message=f"❌ Failed to deploy",
                    error=response.text
                )
        except Exception as e:
            return DeployStatus(
                success=False,
                item_id=table_id,
                item_name=table_name,
                item_type="table",
                message=f"❌ Exception during deploy",
                error=str(e)
            )

    def deploy_endpoint(self, endpoint_id: str, endpoint_path: str, dry_run: bool = False) -> DeployStatus:
        """Deploy an API endpoint to production"""
        print(f"  🔌 Deploying endpoint: {endpoint_path} (ID: {endpoint_id})")
        
        if dry_run:
            return DeployStatus(
                success=True,
                item_id=endpoint_id,
                item_name=endpoint_path,
                item_type="endpoint",
                message="[DRY RUN] Would deploy endpoint"
            )

        try:
            endpoint = f"{XANO_API_BASE}/endpoints/{endpoint_id}/deploy"
            payload = {
                "workspace_id": self.workspace_id,
                "environment": "production",
                "action": "deploy"
            }
            
            response = self.session.post(endpoint, json=payload)
            
            if response.status_code in [200, 201]:
                return DeployStatus(
                    success=True,
                    item_id=endpoint_id,
                    item_name=endpoint_path,
                    item_type="endpoint",
                    message=f"✅ Successfully deployed"
                )
            else:
                return DeployStatus(
                    success=False,
                    item_id=endpoint_id,
                    item_name=endpoint_path,
                    item_type="endpoint",
                    message=f"❌ Failed to deploy",
                    error=response.text
                )
        except Exception as e:
            return DeployStatus(
                success=False,
                item_id=endpoint_id,
                item_name=endpoint_path,
                item_type="endpoint",
                message=f"❌ Exception during deploy",
                error=str(e)
            )

    def deploy_function(self, function_id: str, function_name: str, dry_run: bool = False) -> DeployStatus:
        """Deploy a backend function to production"""
        print(f"  ⚙️ Deploying function: {function_name} (ID: {function_id})")
        
        if dry_run:
            return DeployStatus(
                success=True,
                item_id=function_id,
                item_name=function_name,
                item_type="function",
                message="[DRY RUN] Would deploy function"
            )

        try:
            endpoint = f"{XANO_API_BASE}/functions/{function_id}/deploy"
            payload = {
                "workspace_id": self.workspace_id,
                "environment": "production",
                "action": "deploy"
            }
            
            response = self.session.post(endpoint, json=payload)
            
            if response.status_code in [200, 201]:
                return DeployStatus(
                    success=True,
                    item_id=function_id,
                    item_name=function_name,
                    item_type="function",
                    message=f"✅ Successfully deployed"
                )
            else:
                return DeployStatus(
                    success=False,
                    item_id=function_id,
                    item_name=function_name,
                    item_type="function",
                    message=f"❌ Failed to deploy",
                    error=response.text
                )
        except Exception as e:
            return DeployStatus(
                success=False,
                item_id=function_id,
                item_name=function_name,
                item_type="function",
                message=f"❌ Exception during deploy",
                error=str(e)
            )

    def deploy_all(self, dry_run: bool = False):
        """Deploy all resources"""
        print("\n" + "="*60)
        print("🚀 XanoScript Subject Database Deployment")
        print("="*60 + "\n")

        if dry_run:
            print("⚠️  DRY RUN MODE - No actual changes will be made\n")

        # Deploy tables
        print("📊 1. Deploying Database Tables...")
        for table in DEPLOY_MANIFEST["tables"]:
            status = self.deploy_table(table["id"], table["name"], dry_run)
            self.results.append(status)
            print(f"     {status.message}")

        # Deploy endpoints
        print("\n🔌 2. Deploying REST API Endpoints...")
        for endpoint in DEPLOY_MANIFEST["endpoints"]:
            status = self.deploy_endpoint(endpoint["id"], endpoint["path"], dry_run)
            self.results.append(status)
            print(f"     {status.message}")

        # Deploy functions
        print("\n⚙️  3. Deploying Backend Functions...")
        for function in DEPLOY_MANIFEST["functions"]:
            status = self.deploy_function(function["id"], function["name"], dry_run)
            self.results.append(status)
            print(f"     {status.message}")

        # Summary
        self.print_summary()

    def print_summary(self):
        """Print deployment summary"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        failed = total - successful

        print("\n" + "="*60)
        print("📋 DEPLOYMENT SUMMARY")
        print("="*60)
        print(f"Total Items:    {total}")
        print(f"Successful:     {successful} ✅")
        print(f"Failed:         {failed} ❌")
        print("="*60 + "\n")

        if failed > 0:
            print("Failed items:")
            for result in self.results:
                if not result.success:
                    print(f"  ❌ {result.item_type}: {result.item_name}")
                    if result.error:
                        print(f"     Error: {result.error}")

        return successful == total


def verify_environment():
    """Verify deployment environment"""
    if not XANO_API_KEY:
        print("❌ ERROR: XANO_API_KEY not set in environment")
        print("   Please set: export XANO_API_KEY='your_api_key_here'")
        return False

    print(f"✅ Environment verified:")
    print(f"   API Base: {XANO_API_BASE}")
    print(f"   Workspace: {XANO_WORKSPACE_ID}")
    print(f"   API Key: {'*' * (len(XANO_API_KEY)-4) + XANO_API_KEY[-4:]}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Deploy Subject Database to Xano Production"
    )
    parser.add_argument(
        "--environment",
        default="production",
        choices=["stage", "production"],
        help="Target environment (default: production)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deployed without making changes"
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip environment verification"
    )

    args = parser.parse_args()

    # Verify environment
    if not args.skip_verify:
        if not verify_environment():
            sys.exit(1)

    # Deploy
    deployer = XanoDeployer(XANO_API_KEY)
    deployer.deploy_all(dry_run=args.dry_run)

    # Exit with appropriate code
    sys.exit(0 if deployer.results[-1] if deployer.results else True else 1)


if __name__ == "__main__":
    main()
