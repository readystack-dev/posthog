#!/bin/bash
# ReadyStack: upstream's ClickHouse init-db.sh step that PostHog's schema needs -- flush the server logs once so the
# system log tables exist (ClickHouse migration 0159 creates a view over system.crash_log)
set -e
clickhouse client --query 'SYSTEM FLUSH LOGS'
