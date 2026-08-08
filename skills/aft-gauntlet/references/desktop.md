# Desktop Platform Pack

## Platform Choice

Let the lead agent choose native macOS/Windows, Electron, Tauri, Flutter, Qt, or another runtime from the actual requirements and repository. Require an explicit tradeoff based on native integration, distribution, security, update model, bundle size, memory, performance, team constraints, and shared code—not fashion.

Primary platform sources:

- macOS design guidance: https://developer.apple.com/design/human-interface-guidelines/designing-for-macos
- Windows app design: https://learn.microsoft.com/windows/apps/design/
- Electron docs: https://www.electronjs.org/docs/latest/
- Tauri docs: https://v2.tauri.app/

Research real desktop products with comparable workflows and inspect their installed behavior.

## Real Artifact

Critics inspect packaged builds on each required operating system, not only a browser development server. Judge:

- Windows, tabs, dialogs, menus, context menus, toolbars, and focus
- Keyboard shortcuts and command discoverability
- Drag/drop, clipboard, files, file associations, and recent documents
- Tray/menu-bar behavior, notifications, deep links, and protocol handlers
- Multi-monitor, scaling, appearance, locale, and accessibility
- Permissions, sandbox boundaries, secrets, and untrusted content
- Offline state, persistence, crash recovery, and update behavior
- Startup, idle CPU, memory, bundle size, responsiveness, and long-session stability
- Installer, uninstaller, code signing, notarization, and automatic updates

## Gates

Require representative packaged binaries, platform-specific task tests, keyboard-only use, accessibility inspection, performance profiles, update/recovery tests, and distribution-readiness evidence.

For desktop games, combine with `games.md`; use this pack for packaging, input devices, display modes, storage, updates, crash recovery, and platform conventions.
