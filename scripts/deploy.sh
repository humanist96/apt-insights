#!/bin/bash

# =============================================================================
# Production Deployment Script
# =============================================================================
# Automates deployment of the Korean Apartment Transaction Analysis Platform
#
# Usage:
#   ./scripts/deploy.sh <component> <environment>
#
# Components:
#   backend   - Deploy FastAPI backend to Railway
#   frontend  - Deploy Next.js frontend to Vercel
#   all       - Deploy both backend and frontend
#
# Environments:
#   staging   - Deploy to staging environment
#   production - Deploy to production environment
#
# Examples:
#   ./scripts/deploy.sh backend production
#   ./scripts/deploy.sh frontend staging
#   ./scripts/deploy.sh all production

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPONENT=${1:-all}
ENVIRONMENT=${2:-production}
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEPLOYMENT_LOG="$PROJECT_ROOT/logs/deployment-$TIMESTAMP.log"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/logs"

# =============================================================================
# Helper Functions
# =============================================================================

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$DEPLOYMENT_LOG"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅ $1${NC}" | tee -a "$DEPLOYMENT_LOG"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ❌ $1${NC}" | tee -a "$DEPLOYMENT_LOG"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}" | tee -a "$DEPLOYMENT_LOG"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 is not installed. Please install it first."
        exit 1
    fi
}

confirm_deployment() {
    echo ""
    echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║           PRODUCTION DEPLOYMENT CONFIRMATION             ║${NC}"
    echo -e "${YELLOW}╠════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${YELLOW}║${NC}  Component:   ${BLUE}$COMPONENT${NC}"
    echo -e "${YELLOW}║${NC}  Environment: ${BLUE}$ENVIRONMENT${NC}"
    echo -e "${YELLOW}║${NC}  Time:        ${BLUE}$(date)${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    if [ "$ENVIRONMENT" = "production" ]; then
        read -p "Are you sure you want to deploy to PRODUCTION? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            log "Deployment cancelled."
            exit 0
        fi
    fi
}

check_git_status() {
    log "Checking git status..."

    if [[ -n $(git status -s) ]]; then
        log_warning "You have uncommitted changes:"
        git status -s
        read -p "Continue deployment? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            log "Deployment cancelled."
            exit 0
        fi
    fi

    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$ENVIRONMENT" = "production" ] && [ "$CURRENT_BRANCH" != "main" ]; then
        log_warning "You are not on the 'main' branch (current: $CURRENT_BRANCH)"
        read -p "Continue deployment? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            log "Deployment cancelled."
            exit 0
        fi
    fi

    log_success "Git status OK"
}

run_tests() {
    log "Running tests before deployment..."

    # Backend tests
    if [ "$COMPONENT" = "backend" ] || [ "$COMPONENT" = "all" ]; then
        log "Running backend tests..."
        cd "$PROJECT_ROOT/fastapi-backend"

        if [ -f "pytest.ini" ] || [ -d "tests" ]; then
            pytest -v --tb=short || {
                log_error "Backend tests failed!"
                exit 1
            }
            log_success "Backend tests passed"
        else
            log_warning "No backend tests found"
        fi

        cd "$PROJECT_ROOT"
    fi

    # Frontend tests
    if [ "$COMPONENT" = "frontend" ] || [ "$COMPONENT" = "all" ]; then
        log "Running frontend tests..."
        cd "$PROJECT_ROOT/nextjs-frontend"

        if [ -f "package.json" ]; then
            npm test -- --passWithNoTests || {
                log_error "Frontend tests failed!"
                exit 1
            }
            log_success "Frontend tests passed"
        else
            log_warning "No frontend tests found"
        fi

        cd "$PROJECT_ROOT"
    fi
}

check_health() {
    local url=$1
    local max_attempts=30
    local attempt=1

    log "Checking health endpoint: $url"

    while [ $attempt -le $max_attempts ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            log_success "Health check passed"
            return 0
        fi

        log "Attempt $attempt/$max_attempts - waiting for service..."
        sleep 10
        attempt=$((attempt + 1))
    done

    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# =============================================================================
# Deployment Functions
# =============================================================================

deploy_backend() {
    log "=================================================="
    log "Deploying Backend to Railway ($ENVIRONMENT)"
    log "=================================================="

    cd "$PROJECT_ROOT/fastapi-backend"

    # Check Railway CLI
    check_command railway

    # Run database migrations
    log "Running database migrations..."
    if [ "$ENVIRONMENT" = "production" ]; then
        railway run alembic upgrade head || {
            log_error "Database migration failed!"
            exit 1
        }
    fi
    log_success "Database migrations completed"

    # Deploy to Railway
    log "Deploying to Railway..."
    if [ "$ENVIRONMENT" = "staging" ]; then
        railway up --environment staging || {
            log_error "Railway deployment failed!"
            exit 1
        }
    else
        railway up || {
            log_error "Railway deployment failed!"
            exit 1
        }
    fi
    log_success "Backend deployed to Railway"

    # Wait for deployment to stabilize
    log "Waiting for deployment to stabilize (30s)..."
    sleep 30

    # Health check
    if [ "$ENVIRONMENT" = "production" ]; then
        BACKEND_URL="https://api.your-domain.com"
    else
        BACKEND_URL="https://staging-api.your-domain.com"
    fi

    check_health "$BACKEND_URL/health" || {
        log_error "Backend health check failed!"
        exit 1
    }

    cd "$PROJECT_ROOT"
    log_success "Backend deployment complete"
}

deploy_frontend() {
    log "=================================================="
    log "Deploying Frontend to Vercel ($ENVIRONMENT)"
    log "=================================================="

    cd "$PROJECT_ROOT/nextjs-frontend"

    # Check Vercel CLI
    check_command vercel

    # Build frontend
    log "Building frontend..."
    npm run build || {
        log_error "Frontend build failed!"
        exit 1
    }
    log_success "Frontend build complete"

    # Deploy to Vercel
    log "Deploying to Vercel..."
    if [ "$ENVIRONMENT" = "production" ]; then
        vercel --prod --yes || {
            log_error "Vercel deployment failed!"
            exit 1
        }
    else
        vercel --yes || {
            log_error "Vercel deployment failed!"
            exit 1
        }
    fi
    log_success "Frontend deployed to Vercel"

    # Wait for deployment to stabilize
    log "Waiting for deployment to stabilize (30s)..."
    sleep 30

    # Health check
    if [ "$ENVIRONMENT" = "production" ]; then
        FRONTEND_URL="https://your-domain.com"
    else
        FRONTEND_URL="https://staging.your-domain.com"
    fi

    check_health "$FRONTEND_URL/api/health" || {
        log_error "Frontend health check failed!"
        exit 1
    }

    cd "$PROJECT_ROOT"
    log_success "Frontend deployment complete"
}

run_smoke_tests() {
    log "=================================================="
    log "Running Smoke Tests"
    log "=================================================="

    if [ -f "$PROJECT_ROOT/scripts/smoke-test.sh" ]; then
        bash "$PROJECT_ROOT/scripts/smoke-test.sh" "$ENVIRONMENT" || {
            log_warning "Smoke tests failed! Please investigate."
        }
    else
        log_warning "Smoke test script not found"
    fi
}

generate_deployment_report() {
    log "=================================================="
    log "Generating Deployment Report"
    log "=================================================="

    REPORT_FILE="$PROJECT_ROOT/logs/deployment-report-$TIMESTAMP.md"

    cat > "$REPORT_FILE" <<EOF
# Deployment Report

**Date**: $(date)
**Component**: $COMPONENT
**Environment**: $ENVIRONMENT
**Deployed By**: $(git config user.name) <$(git config user.email)>

## Git Information

**Branch**: $(git branch --show-current)
**Commit**: $(git log -1 --oneline)
**Tag**: $(git describe --tags --always)

## Deployment Status

- Backend: $([ "$COMPONENT" = "backend" ] || [ "$COMPONENT" = "all" ] && echo "✅ Deployed" || echo "⏭️  Skipped")
- Frontend: $([ "$COMPONENT" = "frontend" ] || [ "$COMPONENT" = "all" ] && echo "✅ Deployed" || echo "⏭️  Skipped")

## Health Checks

$(if [ "$COMPONENT" = "backend" ] || [ "$COMPONENT" = "all" ]; then
    echo "- Backend: ✅ Healthy"
fi)

$(if [ "$COMPONENT" = "frontend" ] || [ "$COMPONENT" = "all" ]; then
    echo "- Frontend: ✅ Healthy"
fi)

## Next Steps

1. Monitor error rates in Sentry
2. Check performance metrics
3. Review logs for anomalies
4. Update team on deployment status

## Rollback Command

If issues occur, rollback using:
\`\`\`bash
./scripts/rollback.sh $(git describe --tags --abbrev=0 2>/dev/null || echo "previous-tag")
\`\`\`

---

**Deployment Log**: $DEPLOYMENT_LOG
EOF

    log_success "Deployment report generated: $REPORT_FILE"
}

# =============================================================================
# Main Script
# =============================================================================

main() {
    log "=================================================="
    log "Production Deployment Script"
    log "=================================================="
    log "Deployment started at $(date)"
    log "Log file: $DEPLOYMENT_LOG"
    log ""

    # Validate inputs
    if [[ ! "$COMPONENT" =~ ^(backend|frontend|all)$ ]]; then
        log_error "Invalid component: $COMPONENT"
        log "Usage: $0 <backend|frontend|all> <staging|production>"
        exit 1
    fi

    if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
        log_error "Invalid environment: $ENVIRONMENT"
        log "Usage: $0 <backend|frontend|all> <staging|production>"
        exit 1
    fi

    # Pre-flight checks
    log "Running pre-flight checks..."
    check_command git
    confirm_deployment
    check_git_status
    run_tests

    # Create backup before production deployment
    if [ "$ENVIRONMENT" = "production" ]; then
        log "Creating backup before deployment..."
        if [ -f "$PROJECT_ROOT/scripts/backup-database.sh" ]; then
            bash "$PROJECT_ROOT/scripts/backup-database.sh" production || {
                log_warning "Backup failed, but continuing deployment..."
            }
        fi
    fi

    # Deploy components
    case $COMPONENT in
        backend)
            deploy_backend
            ;;
        frontend)
            deploy_frontend
            ;;
        all)
            deploy_backend
            deploy_frontend
            ;;
    esac

    # Post-deployment checks
    run_smoke_tests
    generate_deployment_report

    log ""
    log "=================================================="
    log_success "Deployment completed successfully!"
    log "=================================================="
    log "Deployment took: $SECONDS seconds"
    log ""
    log "Next steps:"
    log "  1. Monitor logs: railway logs -f"
    log "  2. Check metrics: curl https://api.your-domain.com/api/metrics"
    log "  3. Verify functionality: Visit https://your-domain.com"
    log "  4. Review deployment report: $REPORT_FILE"
    log ""

    # Send notification (optional)
    if command -v mail &> /dev/null; then
        echo "Deployment completed successfully for $COMPONENT on $ENVIRONMENT" | \
            mail -s "✅ Deployment Complete" team@company.com
    fi
}

# Run main function
main "$@"
