# PostHog master-20261022-b904ac8 — ReadyStack release `master-20261022-b904ac8-CE-ubuntu24.04-r5`

Generated 2026-11-12 from this release's build records and strategy. Statements that come from a single record name it in brackets; the others come from this release's strategy and build log.

## Release

- **Image:** `readystack/posthog:master-20261022-b904ac8-CE-ubuntu24.04-r5` (linux/amd64). Index digest `sha256:58905adc60d0a8d903f55061ed8cbe028ab224fc45fafd8b0e72651bb8c71f72` [`docs/provenance/LOCKED_DIGEST.txt`].
- **Image manifest digest:** `sha256:5727cfa920c09ee1676454dc7b0bac8e240fe76804f4780565f1bd146e2f7526` [`TARGET_DIGEST.txt`].
- **Upstream:** PostHog master-20261022-b904ac8 built from source at `b904ac8008e531c8aaeaf58e523cf97cff9fba41` of https://github.com/PostHog/posthog — upstream notes: https://github.com/PostHog/posthog/releases/tag/b904ac8008e531c8aaeaf58e523cf97cff9fba41 [`docs/provenance/BUILD_RECIPE.json`].
- **Base image:** `ubuntu:24.04`; runtime user `posthog`.
- **Build:** `source-rebuild-python`, compiled offline with `--network=none`.
- **Supersedes:** ReadyStack release `master-20261022-b904ac8-CE-ubuntu24.04-r4`.

## What changed in this release

- Upstream version unchanged (master-20261022-b904ac8); ReadyStack rebuild.
- PostHog master-20261022-b904ac8 is unchanged from the release this supersedes (master-20261022-b904ac8-CE-ubuntu24.04-r4); this release rebuilds it. Changes: thrift moves from 0.24.0 to 0.25.0 in the Python environment (CVE-2026-66055, CVE-2026-66858, CVE-2026-85494, CVE-2026-94634, CVE-2026-94636, CVE-2026-94654) and from 0.23.0 to 0.25.0 in the Node ingestion server (CVE-2026-83745, CVE-2026-86535, CVE-2026-94645, CVE-2026-94646, CVE-2026-96294), all high. Settings, ports and data volumes are those of master-20261022-b904ac8-CE-ubuntu24.04-r4: replace the containers with this image on the same volumes.

## Security status at release (measured 2026-11-11)

- **Docker Scout:** 0 fixable critical/high vulnerabilities; runs as `posthog` (non-root); SBOM + provenance attestations present (SPDX SBOM + SLSA v1) [`docs/provenance/SCOUT_VERDICT.json`].
- **OSV cross-check:** no fixable critical/high vulnerability beyond Docker Scout's findings.
- **Signature:** cosign signature verified by ReadyStack's release gate before publishing; check it yourself with `cosign verify --key https://readystack.dev/keys/cosign.pub readystack/posthog:master-20261022-b904ac8-CE-ubuntu24.04-r5` (signatures are recorded in the public Sigstore transparency log).
- **ReadyStack release check at release:** passed (ReadyStack's own test, not a Docker Scout grade). Vulnerabilities are disclosed every day and the image never changes, so it is re-checked daily, beside Docker Scout's own dated grade, at https://readystack.dev/queue.
- **Before exposing this service:** Runs as the non-root user posthog (uid 10001) in every role; the image declares USER posthog.
- **Before exposing this service:** The first user to sign up on an instance with no users becomes the owner: create it before the port is reachable by others.
- **Before exposing this service:** Production needs your own SECRET_KEY and ENCRYPTION_SALT_KEYS (the image's examples are not secrets); keep them, PostHog encrypts integration credentials with ENCRYPTION_SALT_KEYS.
- **Before exposing this service:** No PostHog Enterprise code is present (ee/ removed); /code/ee is ReadyStack's MIT CE compatibility package.
- **Before exposing this service:** CVE floors: the Python, npm and Go dependencies with fixable critical, high or medium advisories at build time are raised to the lowest fixed version (product-kits/posthog/build/py-floors.txt, npm-floors.json; Caddy and the Go UDFs build on Go 1.27.3).

## Reproducibility

Rebuilds offline from this archive to the identical image digest `sha256:5727cfa920c09ee1676454dc7b0bac8e240fe76804f4780565f1bd146e2f7526`: run `./BUILD_OFFLINE.sh`, then `./VERIFY_OFFLINE.sh` (add `--online` to confirm the Docker Hub tag holds the same digest). Before publishing, ReadyStack rebuilt the kit with `./BUILD_OFFLINE.sh` and compared the result with the published digest [`docs/provenance/REPRO_VERIFICATION.json`], then ran `./BUILD_OFFLINE.sh` and `./VERIFY_OFFLINE.sh` from this archive (without `--online`).

## Validation

- 2 of 2 use cases passed (3 authored, 2 kept in the suite; 1 not exercised, see below) against a container of this image started with `allinone` after the image name instead of the image's default command (`allinone`) [`docs/validation/test-results.json`]. A container started the default way can answer differently.
- The cases are `GET /_health` (200), `GET /` (200); the suite checks nothing else.
- 1 further authored check was not exercised and is not counted above: it needed credentials the build's check does not have (listed under Not exercised in `docs/validation/FAILED_TESTS.md`).

## Known issues

- None found (reviewed by held semantic review (Claude) on 2026-11-12).

## Differences from upstream (by design)

- Enterprise / non-open-source components are removed from the source before the build: ee [`RSD-posthog-6062a5bdb3`]

## Defects fixed

- 1 problem found before release and fixed before it shipped (1 by review); each is listed in `docs/defects/defects.json`.

## Verify this archive

```
sha256sum -c CHECKSUMS.sha256
./BUILD_OFFLINE.sh && ./VERIFY_OFFLINE.sh --online
cosign verify --key https://readystack.dev/keys/cosign.pub readystack/posthog:master-20261022-b904ac8-CE-ubuntu24.04-r5
```

ReadyStack records every signature in the public Sigstore transparency log (Rekor), so the command needs no extra flags.

