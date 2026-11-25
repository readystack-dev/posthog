# Provenance — PostHog (`master-20261022-b904ac8-CE-ubuntu24.04-r5`)

Every item below is copied from a record in this archive; the record is named in brackets.

## Source

- Upstream repository: https://github.com/PostHog/posthog
- Revision built: `b904ac8008e531c8aaeaf58e523cf97cff9fba41` (commit `b904ac8008e531c8aaeaf58e523cf97cff9fba41`)
- Source tree: `f891353fb4511d2e73ff287c2eaf25af3d55335185787f784cf4ce68a361004b` over 59938 files [`docs/provenance/SOURCE_TREE_HASH.json`]
- Community Edition only: enterprise code is removed or refused before the build (CE audit at acquire).

## Build

- Method: `source-rebuild-python`; base image `ubuntu:24.04`
- Compiled with `--network=none` from vendored source, dependencies and base images; BuildKit pinned to `moby/buildkit:v0.31.2` (shipped in `toolchain/`).
- SOURCE_DATE_EPOCH: `1794384272` [`SOURCE_DATE_EPOCH.txt`]
- Frozen inputs: [`docs/provenance/FREEZE_MANIFEST.json`], build recipe: [`docs/provenance/BUILD_RECIPE.json`].

## Output

- Published image: `readystack/posthog:master-20261022-b904ac8-CE-ubuntu24.04-r5` — index digest `sha256:58905adc60d0a8d903f55061ed8cbe028ab224fc45fafd8b0e72651bb8c71f72` [`docs/provenance/LOCKED_DIGEST.txt`]
- linux/amd64 image digest `sha256:5727cfa920c09ee1676454dc7b0bac8e240fe76804f4780565f1bd146e2f7526` — reproduced from this archive before publishing [`docs/provenance/REPRO_VERIFICATION.json`].

## Attestations and signature

- SBOM + SLSA provenance attached to the image: attached: an SPDX SBOM and SLSA v1 provenance [`docs/provenance/SCOUT_VERDICT.json`]
- cosign signature by the ReadyStack release key: verified before publishing. Check it: `cosign verify --key https://readystack.dev/keys/cosign.pub readystack/posthog:master-20261022-b904ac8-CE-ubuntu24.04-r5`

## Pinned inputs, and why

- 31 pinned inputs, each with where it came from, why this one, how it was checked and when it was decided: `docs/PINS.md` [`docs/provenance/PINS.json`] (upstream source 2, base and build images 1, image digests 3, language runtimes and toolchains 1, dependency versions readystack sets 3, pins in the kit's dockerfiles 14, readystack's build engine 1, dependencies upstream chose 2, services the release checks run beside 4).

## Build trail

- How this release passed through the ReadyStack harness, record by record (every chain, drive, stage, review round, defect and check, each naming the record it is copied from): `ReadyStack-posthog-master-20261022-b904ac8-CE-ubuntu24.04-r5.trail.json`, published beside this archive and signed with the release key (`ReadyStack-posthog-master-20261022-b904ac8-CE-ubuntu24.04-r5.trail.json.sigstore`), and readable at https://readystack.dev/products/posthog/trail/master-20261022-b904ac8-CE-ubuntu24.04-r5.

