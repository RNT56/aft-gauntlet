# iOS and Mobile Platform Pack

## Product Bar

Research actual App Store products with comparable tasks and inspect real flows, not marketing pages alone. Use official platform guidance as a constraint, not a substitute for product comparison.

Primary iOS sources:

- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Apple Design Resources: https://developer.apple.com/design/resources/
- SF Symbols: https://developer.apple.com/sf-symbols/
- Accessibility: https://developer.apple.com/accessibility/

For Android or cross-platform targets, research current Material guidance and actual platform behavior. Let the lead agent choose SwiftUI, UIKit, Kotlin, Compose, Flutter, React Native, or another stack based on the brief and repository.

## Real Artifact

Critics inspect simulator and, when available, physical-device builds across representative sizes, orientations, appearances, locales, text sizes, and connectivity states. Record interactions when visual judgment matters.

Judge:

- Navigation, sheets, gestures, haptics, keyboard, and system conventions
- Touch targets, Dynamic Type, VoiceOver, contrast, and Reduce Motion
- Launch, background/foreground, restoration, interruption, and deep-link behavior
- Permission timing, privacy disclosures, and denial recovery
- Offline behavior, synchronization, conflicts, and network failure
- Notifications, widgets, Live Activities, StoreKit, or account flows when relevant
- Localization, safe areas, rotation, and device-specific layout
- Startup time, frame pacing, memory, energy, storage, and crash behavior

## Gates

Require build and test evidence, accessibility inspection, performance profiling, and realistic task completion. Do not claim App Store readiness without checking signing, entitlements, privacy manifests, permission strings, screenshots, metadata, and review-sensitive behavior relevant to the app.

For mobile games, combine with `games.md`; game feel remains the primary loop while this pack supplies device, touch, lifecycle, energy, and distribution gates.
