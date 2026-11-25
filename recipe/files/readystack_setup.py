"""ReadyStack PostHog (CE) setup steps that upstream's hobby deploy does elsewhere or not at all. MIT, ReadyStack.

    python readystack_setup.py kafka-topics     create every topic in docker/kafka/topics.txt (upstream: a Redpanda
                                                rpk container, kafka-init); idempotent
    python readystack_setup.py persons-index    the unique (team_id, uuid) index on posthog_person that the ingestion
                                                server's insertPerson needs (ON CONFLICT (team_id, uuid)); upstream
                                                creates it only in the partitioning migrations its hobby mode skips, so
                                                without it no person (and no event) is ever written; idempotent
"""
import os
import sys
import time


def kafka_topics(path="/code/docker/kafka/topics.txt"):
    from kafka.admin import KafkaAdminClient, NewTopic
    from kafka.errors import TopicAlreadyExistsError

    names = [ln.strip() for ln in open(path) if ln.strip() and not ln.lstrip().startswith("#")]
    hosts = os.environ.get("KAFKA_HOSTS", "kafka:9092").split(",")
    deadline = time.time() + int(os.environ.get("KAFKA_WAIT_S", "120"))
    while True:
        try:
            admin = KafkaAdminClient(bootstrap_servers=hosts, client_id="readystack-setup")
            break
        except Exception as e:  # broker not up yet
            if time.time() > deadline:
                sys.exit(f"readystack_setup: Kafka at {hosts} unreachable: {e}")
            time.sleep(3)
    have = set(admin.list_topics())
    missing = [n for n in names if n not in have]
    rf = int(os.environ.get("KAFKA_REPLICATION_FACTOR", "1"))
    for n in missing:
        try:
            admin.create_topics([NewTopic(name=n, num_partitions=1, replication_factor=rf)])
        except TopicAlreadyExistsError:
            pass
    print(f"readystack_setup: {len(names)} Kafka topics present ({len(missing)} created)")


def persons_index():
    sys.path.insert(0, "/code")
    from posthog.persons_db import persons_db_connection  # the database the ingestion server writes persons to

    with persons_db_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT relkind FROM pg_class WHERE relname = 'posthog_person' AND relnamespace = 'public'::regnamespace")
        row = cur.fetchone()
        if not row:
            sys.exit("readystack_setup: posthog_person does not exist: run the persons migrations first")
        if row[0] == "p":
            print("readystack_setup: posthog_person is partitioned (production layout): index comes from its migrations")
            return
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS readystack_person_team_id_uuid_uniq ON posthog_person (team_id, uuid)")
    print("readystack_setup: posthog_person (team_id, uuid) unique index present")


if __name__ == "__main__":
    {"kafka-topics": kafka_topics, "persons-index": persons_index}[sys.argv[1]]()
