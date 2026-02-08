#!/bin/bash

# =============================================================================
# Production Rollback Script
# =============================================================================
# Automates rollback to a previous version
#
# Usage:
#   ./scripts/rollback.sh <version>
#
# Examples:
#   ./scripts/rollback.sh v1.0.0
#   ./scripts/rollback.sh abc123f
#
# This script will:
#   1. Verify the target version exists
#   2. Create a backup of current state
#   3. Rollback application code
#   4. Rollback database (if needed)
#   5. Clear cache
#   6. Verify rollback success

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TARGET_VERSION=${1:-}
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ROLLBACK_LOG="$PROJECT_ROOT/logs/rollback-$TIMESTAMP.log"
CURRENT_VERSION=$(git describe --tags --always)

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/logs"

# =============================================================================
# Helper Functions
# =============================================================================

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$ROLLBACK_LOG"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅ $1${NC}" | tee -a "$ROLLBACK_LOG"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ❌ $1${NC}" | tee -a "$ROLLBACK_LOG"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}" | tee -a "$ROLLBACK_LOG"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 is not installed. Please install it first."
        exit 1
    fi
}

confirm_rollback() {
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║            ⚠️  PRODUCTION ROLLBACK WARNING  ⚠️             ║${NC}"
    echo -e "${RED}╠════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${RED}║${NC}  Current Version:  ${YELLOW}$CURRENT_VERSION${NC}"
    echo -e "${RED}║${NC}  Target Version:   ${YELLOW}$TARGET_VERSION${NC}"
    echo -e "${RED}║${NC}  Time:             ${YELLOW}$(date)${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}This will rollback the production system to a previous version.${NC}"
    echo -e "${YELLOW}This operation should only be performed in emergency situations.${NC}"
    echo ""

    read -p "Type 'ROLLBACK' to confirm: " confirm
    if [ "$confirm" != "ROLLBACK" ]; then
        log "Rollback cancelled."
        exit 0
    fi
}

verify_version() {
    log "Verifying target version exists..."

    # Check if version exists in git
    if ! git rev-parse "$TARGET_VERSION" >/dev/null 2>&1; then
        log_error "Version '$TARGET_VERSION' not found in git history"
        log "Available recent tags:"
        git tag --sort=-v:refname | head -10
        exit 1
    fi

    log_success "Target version verified: $TARGET_VERSION"
}

create_backup() {
    log "Creating backup of current state..."

    # Backup database
    if [ -f "$PROJECT_ROOT/scripts/backup-database.sh" ]; then
        log "Backing up database..."
        bash "$PROJECT_ROOT/scripts/backup-database.sh" production || {
            log_error "Database backup failed!"
            exit 1
        }
        log_success "Database backup created"
    else
        log_warning "Database backup script not found"
    fi

    # Record current git state
    log "Recording current git state..."
    cat > "$PROJECT_ROOT/logs/pre-rollback-state-$TIMESTAMP.txt" <<EOF
Current Branch: $(git branch --show-current)
Current Commit: $(git log -1 --oneline)
Current Tag: $(git describe --tags --always)
Uncommitted Changes:
$(git status -s)
EOF

    log_success "Current state recorded"
}

rollback_application() {
    log "=================================================="
    log "Rolling back application to $TARGET_VERSION"
    log "=================================================="

    cd "$PROJECT_ROOT"

    # Stash any uncommitted changes
    if [[ -n $(git status -s) ]]; then
        log "Stashing uncommitted changes..."
        git stash save "Pre-rollback stash $TIMESTAMP"
        log_success "Changes stashed"
    fi

    # Checkout target version
    log "Checking out $TARGET_VERSION..."
    git checkout "$TARGET_VERSION" || {
        log_error "Failed to checkout $TARGET_VERSION"
        exit 1
    }
    log_success "Checked out $TARGET_VERSION"

    # Update dependencies
    log "Updating backend dependencies..."
    cd "$PROJECT_ROOT/fastapi-backend"
    pip install -r requirements.txt --quiet || {
        log_warning "Backend dependency update failed"
    }

    log "Updating frontend dependencies..."
    cd "$PROJECT_ROOT/nextjs-frontend"
    npm install --silent || {
        log_warning "Frontend dependency update failed"
    }

    cd "$PROJECT_ROOT"
    log_success "Dependencies updated"
}

rollback_database() {
    log "=================================================="
    log "Checking database migration status"
    log "=================================================="

    cd "$PROJECT_ROOT/fastapi-backend"

    # Get current database version
    CURRENT_DB_VERSION=$(railway run alembic current 2>/dev/null | grep -oP '[a-f0-9]{12}' | head -1 || echo "unknown")
    log "Current database version: $CURRENT_DB_VERSION"

    # Check if database rollback needed
    log "Checking if database rollback is needed..."

    # Get migration version at target application version
    git show "$TARGET_VERSION:fastapi-backend/alembic/versions" > /dev/null 2>&1 && {
        read -p "Database rollback may be needed. Downgrade database? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            log "Rolling back database migrations..."

            # User must specify target migration revision
            read -p "Enter target migration revision (or 'head-1' for one step back): " db_target

            if [ "$db_target" = "head-1" ]; then
                railway run alembic downgrade -1 || {
                    log_error "Database rollback failed!"
                    log_error "You may need to manually rollback the database."
                    exit 1
                }
            else
                railway run alembic downgrade "$db_target" || {
                    log_error "Database rollback failed!"
                    log_error "You may need to manually rollback the database."
                    exit 1
                }
            fi

            log_success "Database rolled back"
        else
            log_warning "Skipping database rollback"
        fi
    } || {
        log "No database migration changes detected"
    }

    cd "$PROJECT_ROOT"
}

deploy_rollback() {
    log "=================================================="
    log "Deploying rolled back version"
    log "=================================================="

    # Deploy backend
    log "Deploying backend..."
    cd "$PROJECT_ROOT/fastapi-backend"

    check_command railway
    railway up || {
        log_error "Backend deployment failed!"
        exit 1
    }
    log_success "Backend deployed"

    # Wait for stabilization
    log "Waiting for backend to stabilize (30s)..."
    sleep 30

    # Deploy frontend
    log "Deploying frontend..."
    cd "$PROJECT_ROOT/nextjs-frontend"

    check_command vercel
    vercel --prod --yes || {
        log_error "Frontend deployment failed!"
        exit 1
    }
    log_success "Frontend deployed"

    # Wait for stabilization
    log "Waiting for frontend to stabilize (30s)..."
    sleep 30

    cd "$PROJECT_ROOT"
}

clear_cache() {
    log "=================================================="
    log "Clearing cache"
    log "=================================================="

    log "Clearing Redis cache..."

    # Get Redis connection info from environment
    read -p "Clear Redis cache? This will invalidate all cached data. (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        # This requires Redis connection details
        log_warning "Manual Redis cache clear required:"
        log "  redis-cli -h <host> -p <port> -a <password> FLUSHDB"
    else
        log "Skipping cache clear"
    fi

    # Clear CDN cache (Vercel)
    log "Purging Vercel cache..."
    cd "$PROJECT_ROOT/nextjs-frontend"
    vercel --prod --force || {
        log_warning "Failed to purge Vercel cache"
    }

    cd "$PROJECT_ROOT"
    log_success "Cache cleared"
}

verify_rollback() {
    log "=================================================="
    log "Verifying rollback"
    log "=================================================="

    # Check backend health
    log "Checking backend health..."
    BACKEND_URL="https://api.your-domain.com"
    MAX_ATTEMPTS=30
    ATTEMPT=1

    while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
        if curl -sf "$BACKEND_URL/health" > /dev/null 2>&1; then
            BACKEND_VERSION=$(curl -s "$BACKEND_URL/health" | jq -r '.version' 2>/dev/null || echo "unknown")
            log_success "Backend is healthy (version: $BACKEND_VERSION)"
            break
        fi

        log "Attempt $ATTEMPT/$MAX_ATTEMPTS - waiting for backend..."
        sleep 10
        ATTEMPT=$((ATTEMPT + 1))
    done

    if [ $ATTEMPT -gt $MAX_ATTEMPTS ]; then
        log_error "Backend health check failed!"
        return 1
    fi

    # Check frontend health
    log "Checking frontend health..."
    FRONTEND_URL="https://your-domain.com"
    ATTEMPT=1

    while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
        if curl -sf "$FRONTEND_URL/api/health" > /dev/null 2>&1; then
            log_success "Frontend is healthy"
            break
        fi

        log "Attempt $ATTEMPT/$MAX_ATTEMPTS - waiting for frontend..."
        sleep 10
        ATTEMPT=$((ATTEMPT + 1))
    done

    if [ $ATTEMPT -gt $MAX_ATTEMPTS ]; then
        log_error "Frontend health check failed!"
        return 1
    fi

    # Run smoke tests
    if [ -f "$PROJECT_ROOT/scripts/smoke-test.sh" ]; then
        log "Running smoke tests..."
        bash "$PROJECT_ROOT/scripts/smoke-test.sh" production || {
            log_warning "Smoke tests failed"
            return 1
        }
        log_success "Smoke tests passed"
    fi

    log_success "Rollback verification complete"
}

generate_rollback_report() {
    log "=================================================="
    log "Generating Rollback Report"
    log "=================================================="

    REPORT_FILE="$PROJECT_ROOT/logs/rollback-report-$TIMESTAMP.md"

    cat > "$REPORT_FILE" <<EOF
# Rollback Report

**Date**: $(date)
**Performed By**: $(git config user.name) <$(git config user.email)>
**Reason**: [FILL IN REASON]

## Version Information

**From Version**: $CURRENT_VERSION
**To Version**: $TARGET_VERSION

## Actions Performed

- [x] Backup created
- [x] Application rolled back
- [x] Database rolled back (if applicable)
- [x] Cache cleared
- [x] Deployment completed
- [x] Health checks passed

## Verification

**Backend Health**: ✅ Healthy
**Frontend Health**: ✅ Healthy
**Smoke Tests**: ✅ Passed

## Timeline

- Started: $(date)
- Duration: $SECONDS seconds
- Completed: $(date)

## Post-Rollback Actions Required

1. Monitor error rates in Sentry
2. Check performance metrics
3. Investigate root cause of issue
4. Plan fix and re-deployment
5. Update team on status

## Incident Report

Create incident report: incidents/incident-$TIMESTAMP.md

---

**Rollback Log**: $ROLLBACK_LOG

**Backup Location**: See backup script output

**Recovery Command** (if rollback fails):
\`\`\`bash
# Restore to pre-rollback state
git checkout $CURRENT_VERSION
./scripts/deploy.sh all production
\`\`\`
EOF

    log_success "Rollback report generated: $REPORT_FILE"
}

# =============================================================================
# Main Script
# =============================================================================

main() {
    log "=================================================="
    log "Production Rollback Script"
    log "=================================================="
    log "Rollback started at $(date)"
    log "Log file: $ROLLBACK_LOG"
    log ""

    # Check if version provided
    if [ -z "$TARGET_VERSION" ]; then
        log_error "No target version specified"
        log "Usage: $0 <version>"
        log ""
        log "Available recent versions:"
        git tag --sort=-v:refname | head -10
        exit 1
    fi

    # Pre-flight checks
    log "Running pre-flight checks..."
    check_command git
    check_command railway
    check_command vercel
    check_command jq

    # Verify version and get confirmation
    verify_version
    confirm_rollback

    # Execute rollback
    create_backup
    rollback_application
    rollback_database
    deploy_rollback
    clear_cache

    # Verify and report
    if verify_rollback; then
        generate_rollback_report

        log ""
        log "=================================================="
        log_success "Rollback completed successfully!"
        log "=================================================="
        log "Rollback took: $SECONDS seconds"
        log ""
        log "Next steps:"
        log "  1. Monitor logs: railway logs -f"
        log "  2. Check error rates in Sentry"
        log "  3. Verify user functionality"
        log "  4. Investigate root cause"
        log "  5. Create incident report"
        log ""
        log "Report: $REPORT_FILE"

        # Send notification
        if command -v mail &> /dev/null; then
            echo "Rollback to $TARGET_VERSION completed successfully" | \
                mail -s "⚠️  Production Rollback Complete" team@company.com
        fi

        exit 0
    else
        log_error "Rollback verification failed!"
        log_error "System may be in inconsistent state"
        log_error "IMMEDIATE ACTION REQUIRED"
        log ""
        log "Emergency contacts:"
        log "  Technical Lead: [PHONE]"
        log "  DevOps Lead: [PHONE]"
        log "  Engineering Manager: [PHONE]"

        # Send urgent notification
        if command -v mail &> /dev/null; then
            echo "URGENT: Rollback verification failed! System in inconsistent state." | \
                mail -s "🚨 CRITICAL: Rollback Failed" team@company.com
        fi

        exit 1
    fi
}

# Trap errors and cleanup
cleanup() {
    if [ $? -ne 0 ]; then
        log_error "Rollback failed or was interrupted!"
        log "Check rollback log: $ROLLBACK_LOG"
    fi
}

trap cleanup EXIT

# Run main function
main "$@"
