#!/bin/bash
# XanoScript Deployment Script (Bash/Zsh)
# Deploy Subject Database changes to Xano Production
# Usage: ./deploy_xano.sh [--dry-run] [--stage|--production]

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT="${ENVIRONMENT:-production}"
DRY_RUN=false
VERBOSE=false

# Xano API configuration
XANO_API_BASE="${XANO_API_BASE:-https://api.xano.io/v1}"
XANO_WORKSPACE_ID="${XANO_WORKSPACE_ID:-edutrack-ai}"
XANO_API_KEY="${XANO_API_KEY:-}"

# Deployment manifest
declare -A TABLES=(
    ["753426"]="subject"
    ["754426"]="subject_triggers"
)

declare -a ENDPOINTS=(
    "3600550:GET /subjects/my"
    "3600551:GET /subjects/{id}"
    "3600552:POST /subjects"
    "3600553:PATCH /subjects/{id}"
    "3600554:DELETE /subjects/{id}"
)

declare -A FUNCTIONS=(
    ["269538"]="check_subject_access"
)

# Functions
print_header() {
    echo ""
    echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}🚀 XanoScript Subject Database Deployment${NC}"
    echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════${NC}"
    echo ""
}

print_step() {
    echo -e "${BOLD}${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

verify_environment() {
    print_step "🔍 Verifying environment..."
    
    if [ -z "$XANO_API_KEY" ]; then
        print_error "XANO_API_KEY not set in environment"
        echo "Please set: export XANO_API_KEY='your_api_key_here'"
        exit 1
    fi
    
    if ! command -v curl &> /dev/null; then
        print_error "curl is required but not installed"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        print_warning "jq is recommended for JSON parsing (optional)"
    fi
    
    print_success "Environment verified"
    echo "   API Base: $XANO_API_BASE"
    echo "   Workspace: $XANO_WORKSPACE_ID"
    echo "   Environment: $ENVIRONMENT"
    echo ""
}

deploy_table() {
    local table_id=$1
    local table_name=$2
    
    echo -n "  📦 Deploying table: $table_name (ID: $table_id)... "
    
    if [ "$DRY_RUN" = true ]; then
        print_success "[DRY RUN] Would deploy"
        return 0
    fi
    
    local endpoint="${XANO_API_BASE}/tables/${table_id}/deploy"
    local payload=$(cat <<EOF
{
  "workspace_id": "$XANO_WORKSPACE_ID",
  "environment": "$ENVIRONMENT",
  "action": "deploy"
}
EOF
    )
    
    local response=$(curl -s -X POST \
        -H "Authorization: Bearer $XANO_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "$endpoint")
    
    if echo "$response" | grep -q "error"; then
        print_error "Failed"
        echo "      Response: $response"
        return 1
    else
        print_success "Deployed"
        return 0
    fi
}

deploy_endpoint() {
    local endpoint_id=$1
    local endpoint_path=$2
    
    echo -n "  🔌 Deploying endpoint: $endpoint_path (ID: $endpoint_id)... "
    
    if [ "$DRY_RUN" = true ]; then
        print_success "[DRY RUN] Would deploy"
        return 0
    fi
    
    local url="${XANO_API_BASE}/endpoints/${endpoint_id}/deploy"
    local payload=$(cat <<EOF
{
  "workspace_id": "$XANO_WORKSPACE_ID",
  "environment": "$ENVIRONMENT",
  "action": "deploy"
}
EOF
    )
    
    local response=$(curl -s -X POST \
        -H "Authorization: Bearer $XANO_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "$url")
    
    if echo "$response" | grep -q "error"; then
        print_error "Failed"
        echo "      Response: $response"
        return 1
    else
        print_success "Deployed"
        return 0
    fi
}

deploy_function() {
    local function_id=$1
    local function_name=$2
    
    echo -n "  ⚙️ Deploying function: $function_name (ID: $function_id)... "
    
    if [ "$DRY_RUN" = true ]; then
        print_success "[DRY RUN] Would deploy"
        return 0
    fi
    
    local url="${XANO_API_BASE}/functions/${function_id}/deploy"
    local payload=$(cat <<EOF
{
  "workspace_id": "$XANO_WORKSPACE_ID",
  "environment": "$ENVIRONMENT",
  "action": "deploy"
}
EOF
    )
    
    local response=$(curl -s -X POST \
        -H "Authorization: Bearer $XANO_API_KEY" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "$url")
    
    if echo "$response" | grep -q "error"; then
        print_error "Failed"
        echo "      Response: $response"
        return 1
    else
        print_success "Deployed"
        return 0
    fi
}

deploy_all() {
    local total=0
    local successful=0
    
    # Deploy tables
    print_step "📊 1. Deploying Database Tables..."
    for table_id in "${!TABLES[@]}"; do
        table_name=${TABLES[$table_id]}
        if deploy_table "$table_id" "$table_name"; then
            ((successful++))
        fi
        ((total++))
    done
    
    echo ""
    print_step "🔌 2. Deploying REST API Endpoints..."
    for endpoint in "${ENDPOINTS[@]}"; do
        IFS=':' read -r endpoint_id endpoint_path <<< "$endpoint"
        if deploy_endpoint "$endpoint_id" "$endpoint_path"; then
            ((successful++))
        fi
        ((total++))
    done
    
    echo ""
    print_step "⚙️ 3. Deploying Backend Functions..."
    for function_id in "${!FUNCTIONS[@]}"; do
        function_name=${FUNCTIONS[$function_id]}
        if deploy_function "$function_id" "$function_name"; then
            ((successful++))
        fi
        ((total++))
    done
    
    # Summary
    echo ""
    echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}📋 DEPLOYMENT SUMMARY${NC}"
    echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════${NC}"
    echo "Total Items:    $total"
    echo "Successful:     $successful ✅"
    echo "Failed:         $((total - successful)) ❌"
    echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ "$successful" -eq "$total" ]; then
        print_success "All items deployed successfully!"
        return 0
    else
        print_error "Some items failed to deploy"
        return 1
    fi
}

show_help() {
    cat << EOF
XanoScript Deployment Tool

Usage: $0 [OPTIONS]

Options:
    --dry-run           Show what would be deployed without making changes
    --stage             Deploy to stage environment (default: production)
    --production        Deploy to production environment (default)
    --verbose           Enable verbose output
    --help              Show this help message

Environment Variables:
    XANO_API_KEY        Xano API key (REQUIRED)
    XANO_WORKSPACE_ID   Xano workspace ID (default: edutrack-ai)
    XANO_API_BASE       Xano API base URL (default: https://api.xano.io/v1)

Examples:
    # Dry run before actual deployment
    $0 --dry-run

    # Deploy to production
    $0 --production

    # Deploy to stage
    $0 --stage

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --stage)
            ENVIRONMENT="stage"
            shift
            ;;
        --production)
            ENVIRONMENT="production"
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main execution
main() {
    print_header
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN MODE - No actual changes will be made"
        echo ""
    fi
    
    verify_environment
    deploy_all
    
    exit $?
}

# Run main function
main "$@"
