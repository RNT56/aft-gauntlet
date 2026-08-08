# PWA Platform Pack

Read this with `websites.md`.

## Product Definition

Confirm whether the product truly needs installability, offline operation, push, background work, local persistence, file access, or app-like navigation. Do not call an ordinary responsive site a PWA.

## Real Artifact

Critics inspect the installed experience as well as browser tabs on representative iOS, Android, macOS, Windows, and browser combinations relevant to the audience.

Judge:

- Manifest correctness and install experience
- Standalone display, launch, icons, theme, and deep links
- Service-worker install, activate, update, rollback, and cache invalidation
- Offline, flaky-network, captive-portal, and stale-data behavior
- Local persistence, migration, storage pressure, and conflict handling
- Push and permission timing when required
- Background sync or queued actions when supported
- Browser capability differences and honest fallbacks
- Accessibility, performance, security headers, and HTTPS

## Gates

Require install and update tests, offline task completion, network-failure recovery, browser/device coverage, manifest and service-worker validation, production caching inspection, and standard web performance/accessibility gates.

Do not let a service worker hide deploys behind stale caches. Provide visible update behavior appropriate to the product.

For browser games, combine with `games.md`; preserve frame pacing, input, audio-unlock, fullscreen, pointer-lock, save, and asset-streaming behavior.
