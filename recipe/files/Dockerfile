# =====================================================================
# PostHog (MIT; Enterprise ee/ removed) -- HERMETIC OFFLINE BUILD (docker build --network=none).
# Reassembles the filesystem Dockerfile.vendor built from upstream's source (vendored/posthog-src/*.tar.gz)
# onto the digest-pinned ubuntu:24.04, with CPython 3.14.10 compiled here, offline, from python.org's tarball
# (sha256 re-checked) and the vendored build debs -- the same command the vendor stage ran.
# =====================================================================
FROM ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852 AS cpython
ARG SOURCE_DATE_EPOCH=1794384272
ENV SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH}
COPY vendored/posthog-src/python/debs/ /tmp/cpython-debs/
COPY vendored/posthog-src/python/Python-3.14.10.tar.xz /tmp/Python-3.14.10.tar.xz
RUN set --; for f in /tmp/cpython-debs/*.deb; do [ -e "$f" ] && set -- "$@" "$f"; done; \
    for pass in 1 2 3 4 5; do [ $# -eq 0 ] || dpkg -i --skip-same-version "$@" >/dev/null 2>&1 && break; done; \
    dpkg --configure -a && bad= && for d in "$@"; do p=$(dpkg-deb -f "$d" Package) v=$(dpkg-deb -f "$d" Version); \
      case "$(dpkg-query -W -f='${Version} ${db:Status-Abbrev}' "$p" 2>/dev/null)" in "$v ii"*) ;; *) bad="$bad $p=$v" ;; esac; done && \
    { [ -z "$bad" ] || { echo "vendored debs not installed at their vendored version:$bad" >&2; false; }; } && \
    : "${SOURCE_DATE_EPOCH:?the CPython build needs SOURCE_DATE_EPOCH}" && \
    echo "de414a57119abef52784d8993e341d53aed635fc2b05c2607d9f98a2c5b72032  /tmp/Python-3.14.10.tar.xz" | sha256sum -c - && \
    mkdir -p /usr/src/python && tar -xJf /tmp/Python-3.14.10.tar.xz -C /usr/src/python --strip-components=1 --no-same-owner && \
    rm -rf /tmp/cpython-debs /tmp/Python-3.14.10.tar.xz && cd /usr/src/python && \
    export DEB_BUILD_MAINT_OPTIONS=optimize=-lto && \
    PYCF="$(dpkg-buildflags --get CFLAGS) $(dpkg-buildflags --get CPPFLAGS)" && PYLD="$(dpkg-buildflags --get LDFLAGS)" && \
    ./configure --build=x86_64-linux-gnu --prefix=/usr/local --enable-shared --enable-loadable-sqlite-extensions --enable-option-checking=fatal --disable-test-modules --without-static-libpython --with-ensurepip=install --with-system-expat --without-system-libmpdec --with-dbmliborder= py_cv_module__dbm=n/a py_cv_module__gdbm=n/a py_cv_module__tkinter=n/a && \
    make -j"$(nproc)" "EXTRA_CFLAGS=$PYCF" "LDFLAGS=$PYLD,--strip-all" && \
    rm python && make -j"$(nproc)" "EXTRA_CFLAGS=$PYCF" "LDFLAGS=$PYLD,--strip-all,-rpath='\$\$ORIGIN/../lib'" python && \
    make install COMPILEALL_OPTS=--invalidation-mode=checked-hash && \
    cd / && rm -rf /usr/src/python /usr/local/lib/python3.14/idlelib /usr/local/lib/python3.14/tkinter /usr/local/lib/python3.14/turtledemo /usr/local/bin/idle3* && \
    for s in pip3 pydoc3 python3 python3-config; do ln -sfT "$s" "/usr/local/bin/${s%3*}${s#*3}"; done && \
    ldconfig && /usr/local/bin/python3 -I -B -c "import ssl, sqlite3, zlib, bz2, lzma, ctypes, uuid, pyexpat, decimal, readline, curses, hashlib, compression.zstd, sys, importlib.util as u; bad = [m for m in ('_dbm', '_gdbm', '_tkinter') if u.find_spec(m)]; assert not bad, ('built but must not be', bad); print(sys.version.replace(chr(10), ' '), '|', ssl.OPENSSL_VERSION, '| sqlite', sqlite3.sqlite_version, '| expat', pyexpat.EXPAT_VERSION)" && \
    ldd /usr/local/lib/python3.14/lib-dynload/_ssl.cpython-*.so | grep -qE 'libssl.so.3 => /(usr/)?lib/x86_64-linux-gnu/' && ldd /usr/local/lib/python3.14/lib-dynload/_sqlite3.cpython-*.so | grep -qE 'libsqlite3.so.0 => /(usr/)?lib/x86_64-linux-gnu/' && ldd /usr/local/lib/python3.14/lib-dynload/pyexpat.cpython-*.so | grep -qE 'libexpat.so.1 => /(usr/)?lib/x86_64-linux-gnu/' && ldd /usr/local/lib/python3.14/lib-dynload/_ctypes.cpython-*.so | grep -qE 'libffi.so.8 => /(usr/)?lib/x86_64-linux-gnu/' && ldd /usr/local/lib/python3.14/lib-dynload/_lzma.cpython-*.so | grep -qE 'liblzma.so.5 => /(usr/)?lib/x86_64-linux-gnu/' && ldd /usr/local/lib/python3.14/lib-dynload/_bz2.cpython-*.so | grep -qE 'libbz2.so.1.0 => /(usr/)?lib/x86_64-linux-gnu/' && ldd /usr/local/lib/python3.14/lib-dynload/_uuid.cpython-*.so | grep -qE 'libuuid.so.1 => /(usr/)?lib/x86_64-linux-gnu/' && ldd /usr/local/lib/python3.14/lib-dynload/zlib.cpython-*.so | grep -qE 'libz.so.1 => /(usr/)?lib/x86_64-linux-gnu/'

# Runtime: ubuntu:24.04 (digest-pinned) + the interpreter compiled above; then the vendored system files (runtime
# libraries, the posthog user), the Python environment, PostHog's binaries and the app.
FROM ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852
ARG SOURCE_DATE_EPOCH=1794384272
ENV PATH=/python-runtime/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PYTHONPATH=/python-runtime PYTHONUNBUFFERED=1 PYTHONUTF8=1 LANG=C.UTF-8 NODE_ENV=production
COPY --from=cpython /usr/local/ /usr/local/
ADD vendored/posthog-src/system.tar.gz /
ADD vendored/posthog-src/venv.tar.gz /
ADD vendored/posthog-src/bin.tar.gz /
ADD vendored/posthog-src/app.tar.gz /
# pip is build-only: the CPython compile's ensurepip put one under /usr/local; nothing runs it at runtime.
# The installed apt, libapt-pkg6.0t64 and libpcre2-8-0 (system.tar.gz carries the vendor run's dpkg database) must meet
# strategies/posthog.json apt_refresh (CVE-2026-109518 and the pcre2 mediums): a stale vendored tar fails here.
RUN rm -rf /usr/local/lib/python3.14/site-packages/pip /usr/local/lib/python3.14/site-packages/pip-*.dist-info /usr/local/bin/pip /usr/local/bin/pip3 /usr/local/bin/pip3.14 && \
    ldconfig && id posthog && test "$(stat -c %u /code)" = 10001 && \
    for m in apt=2.8.4ubuntu0.1 libapt-pkg6.0t64=2.8.4ubuntu0.1 libpcre2-8-0=10.42-4ubuntu2.2; do p=${m%%=*} v=${m#*=}; \
      dpkg --compare-versions "$(dpkg-query -W -f='${Version}' "$p" 2>/dev/null)" ge "$v" || \
        { echo "$p is below $v, the CVE minimum of strategies/posthog.json apt_refresh" >&2; exit 1; }; done && \
    : "${SOURCE_DATE_EPOCH:?}" && \
    sed -ri "s/^([^:]*:[^:]*):[0-9]*:/\1:$((SOURCE_DATE_EPOCH/86400)):/" /etc/shadow && \
    rm -f /etc/passwd- /etc/shadow- /etc/group- /etc/gshadow- && \
    rm -rf /var/log/dpkg.log /var/log/alternatives.log /var/log/apt /var/cache/ldconfig/aux-cache /var/cache/fontconfig
USER posthog
WORKDIR /code
EXPOSE 8000 3000 3001
ENTRYPOINT ["/usr/local/bin/posthog-ce"]
CMD ["allinone"]
# >>> readystack OCI labels: strategies/posthog.json image_labels plus the standard OCI labels,
# the set a generated kit carries (gen_dockerfile.label_lines). Written by scripts/kit_migrations.py;
# scripts/retarget.py re-renders it with every retarget. Never edit it by hand.
LABEL org.opencontainers.image.licenses="MIT"
LABEL com.readystack.license.disclosure="This image includes PostHog (https://github.com/PostHog/posthog), licensed under MIT, built from upstream's default-branch commit b904ac8008e531c8aaeaf58e523cf97cff9fba41 (upstream's last tagged server release is 1.43.1, 2023-05-17). The PostHog Enterprise code (the upstream ee/ directory, PostHog Enterprise license) is REMOVED and not present. PostHog's MIT code no longer runs without that directory, so the image's /code/ee is ReadyStack's own MIT-licensed CE compatibility package (no PostHog Enterprise code); Enterprise-only features are absent. Modifications to upstream source: posthog/settings/web.py and posthog/settings/__init__.py register that package when the Enterprise package is absent. Not shipped: dagster-cloud and pex (PostHog Cloud's deployment tooling), the session-replay recording rasterizer (nodejs/src/session-replay/recording-rasterizer; it needs a browser and ffmpeg, which the image does not contain) with its browser drivers puppeteer and puppeteer-capture and MaxMind's GeoLite2 database (an empty database of the same format is in its place); playwright's bundled node is replaced by a link to the image's node. Security fixes are applied only through vendored updates to upstream-published Python, npm, Go and apt dependencies (unmodified). ReadyStack license holders have access to the image build recipe and patched-package manifest on request via contact@readystack.dev."
LABEL org.opencontainers.image.title="PostHog"
LABEL org.opencontainers.image.description="PostHog is open-source product analytics: capture events from your websites and apps, then explore them with trends, funnels, retention, paths, dashboards and SQL, with feature flags and experiments alongside."
LABEL org.opencontainers.image.source="https://github.com/PostHog/posthog"
LABEL org.opencontainers.image.version="master-20261022-b904ac8-CE-ubuntu24.04-r5"
LABEL org.opencontainers.image.revision="b904ac8008e531c8aaeaf58e523cf97cff9fba41"
# <<< readystack OCI labels
