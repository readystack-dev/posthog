# PostHog: ReadyStack build kit

The offline build kit for the Docker image `readystack/posthog:master-20261022-b904ac8-CE-ubuntu24.04-r5`. It holds what the image is built from (upstream source, base images, toolchain, pinned dependencies) and the documents, so the image can be rebuilt with no network access (`docker build --network=none`).

- Release: [master-20261022-b904ac8-CE-ubuntu24.04-r5](https://github.com/readystack-dev/posthog/releases/tag/master-20261022-b904ac8-CE-ubuntu24.04-r5)
- Image: [`docker.io/readystack/posthog:master-20261022-b904ac8-CE-ubuntu24.04-r5`](https://hub.docker.com/r/readystack/posthog/tags), manifest digest `sha256:5727cfa920c09ee1676454dc7b0bac8e240fe76804f4780565f1bd146e2f7526`
- Product page: https://readystack.dev/products/posthog
- Defects: this repository's Issues (defects recorded from 25 November 2026 on) and https://readystack.dev/defects.html?product=posthog

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
