#!/bin/bash
# ReadyStack PostHog (CE): start the official ClickHouse server image with the files PostHog's schema needs.
# Mount the directory `posthog-ce clickhouse-config <dir>` wrote at /posthog (read-only) and use this file as the
# ClickHouse container's entrypoint: it installs PostHog's cluster/macros config, ClickHouse Keeper (in place of a
# ZooKeeper container), the users profile, the UDF definitions and executables, then runs the image's own entrypoint.
set -e
src=/posthog
cp "$src"/config.d/*.xml /etc/clickhouse-server/config.d/
cp "$src"/users.d/*.xml /etc/clickhouse-server/users.d/
cp "$src"/user_defined_function.xml /etc/clickhouse-server/
mkdir -p /var/lib/clickhouse/user_scripts /docker-entrypoint-initdb.d
cp -r "$src"/user_scripts/. /var/lib/clickhouse/user_scripts/
cp "$src"/docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/
exec /entrypoint.sh "$@"
