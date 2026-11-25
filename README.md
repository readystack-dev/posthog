# PostHog: ReadyStack build kit

The offline build kit for the Docker image `readystack/posthog:master-20261022-b904ac8-CE-ubuntu24.04-r5`. It holds what the image is built from (upstream source, base images, toolchain, pinned dependencies) and the documents, so the image can be rebuilt with no network access (`docker build --network=none`).

- Release: [master-20261022-b904ac8-CE-ubuntu24.04-r5](https://github.com/readystack-dev/posthog/releases/tag/master-20261022-b904ac8-CE-ubuntu24.04-r5)
- Image: [`docker.io/readystack/posthog:master-20261022-b904ac8-CE-ubuntu24.04-r5`](https://hub.docker.com/r/readystack/posthog/tags), manifest digest `sha256:5727cfa920c09ee1676454dc7b0bac8e240fe76804f4780565f1bd146e2f7526`
- Product page: https://readystack.dev/products/posthog
- Source and build recipe: https://readystack.dev/products/posthog/recipe
- Build trail: https://readystack.dev/products/posthog/trail/master-20261022-b904ac8-CE-ubuntu24.04-r5
- Defects: this repository's Issues (defects recorded from 25 November 2026 on) and https://readystack.dev/defects.html?product=posthog

## The image

One image, one PostHog role per container (the command argument), all as the non-root user posthog (uid 10001): allinone (default) runs every PostHog process in one container for a single host: Caddy on :8000 (the one HTTP port), the Django web app (granian) and Celery worker+scheduler, the Node ingestion server, and the Rust capture, feature-flags, property-defs and personhog services. The roles web, worker, ingestion, plugins, capture, feature-flags, property-defs, personhog-replica, personhog-router, proxy and migrate run the same processes one per container. PostgreSQL, Redis-protocol cache (Valkey), Apache Kafka and ClickHouse are not in the image: you run them (the run command starts all four as containers).

## Who uses PostHog and why

Product teams and developers who want to see how people use their web or mobile app.

PostHog captures events from a product, automatically or through your own instrumentation, and lets you analyse user behaviour with visualisations or SQL.

A typical use: A team ships a new sign-up flow and wants to know where people drop out. PostHog records each step as an event; the team charts how many users reach each step, finds the screen where people give up, and checks the effect after changing it.

From the upstream project's own description: https://github.com/PostHog/posthog.

## This release

- Docker Scout policy grade at release: **B** (83%), graded 2026-11-12 with `docker scout policy` (CLI 1.26.0, docker-default configuration).
  - Base image docker.io/library/ubuntu:24.04 has been updated since this image was built: it was built on sha256:78d4744ead1f…, and the tag's current linux/amd64 image is sha256:77eb101c607d….
  - Docker Scout counts 115 packages with copyleft licences (GPL, LGPL, MPL), 103 of them operating-system packages (it counts only packages whose licence it can read; the SBOM lists every component).
- Signed with ReadyStack's release key (fingerprint `04daa92344a52dbc`): https://readystack.dev/keys/cosign.pub.
- Runs as a non-root user (`posthog`).
- Attestations on the image: an SPDX SBOM and SLSA provenance v1.
- Rebuilt from this kit with network egress blocked on 2026-11-12; the rebuilt image digest is the published one.
- Base: Ubuntu 24.04.

The current grade, measured again every day, is on https://readystack.dev/products/posthog.

PostHog is distributed under its upstream licence (MIT); the kit contains upstream's source under that licence, and each vendored component under its own.

## Download

From the [master-20261022-b904ac8-CE-ubuntu24.04-r5 release](https://github.com/readystack-dev/posthog/releases/tag/master-20261022-b904ac8-CE-ubuntu24.04-r5): `ReadyStack-posthog-master-20261022-b904ac8-CE-ubuntu24.04-r5.tar.gz` (2.9 GB), SHA-256 `9f66f4f799525ef5be98aac73de1d419b2e8f3882e277c25c2e66c58df681c79`.

GitHub limits a release file to 2 GiB, so the kit is published in 2 parts. Download them all and join them:

```sh
cat ReadyStack-posthog-master-20261022-b904ac8-CE-ubuntu24.04-r5.tar.gz.part-* > ReadyStack-posthog-master-20261022-b904ac8-CE-ubuntu24.04-r5.tar.gz
sha256sum --check --ignore-missing SHA256SUMS
```

## Verify and rebuild

The rebuild statement is signed with the ReadyStack release key. Check the signature before you rely on it:

```sh
cosign verify-blob --key https://readystack.dev/keys/cosign.pub \
  --bundle ReadyStack-posthog-master-20261022-b904ac8-CE-ubuntu24.04-r5.rebuild.json.sigstore ReadyStack-posthog-master-20261022-b904ac8-CE-ubuntu24.04-r5.rebuild.json
```

Unpack with `-p` so file modes are kept, then follow the kit's own README.md and docs/REBUILD.md:

```sh
tar -xpzf ReadyStack-posthog-master-20261022-b904ac8-CE-ubuntu24.04-r5.tar.gz
cd master-20261022-b904ac8-CE-ubuntu24.04-r5
less README.md docs/REBUILD.md
```

The build trail (`ReadyStack-posthog-master-20261022-b904ac8-CE-ubuntu24.04-r5.trail.json`, signed the same way, and its Markdown copy) records how this release was built and checked.

## This repository

`recipe/` holds the kit's recipe files (Dockerfiles, build scripts, pins) as published at https://readystack.dev/products/posthog/recipe. The complete kit is the release download. Each release is a tag here.

— ReadyStack · https://readystack.dev
