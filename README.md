# Portfolio Project — 100Hires

## Overview
This repository documents the initial toolchain setup and environment provisioning for the **100Hires** portfolio project. All configuration, installation steps, and troubleshooting are captured below for reproducibility and transparency.

---

## Tools Installed

| Tool | Version | Purpose |
|------|---------|---------|
| **Cursor IDE** | 3.2.16 | AI-first code editor with integrated agentic capabilities |
| **Claude Code** | Extension (via Cursor Marketplace) | Anthropic's agentic coding assistant, operating within Cursor |
| **Codex** | Extension (via Cursor Marketplace) | OpenAI's coding agent, providing multi-model coverage |
| **GitHub CLI (`gh`)** | 2.88.1 | Command-line interface for GitHub repository management |
| **Homebrew** | 5.1.3 | macOS package manager used for automated tool provisioning |

---

## Steps Completed

### 1. Environment Provisioning (macOS x64)
- Verified Homebrew installation (`brew --version` → 5.1.3).
- Installed / upgraded Cursor IDE via Homebrew Cask:
  ```
  brew install --cask cursor
  ```
- Confirmed GitHub CLI was present and authenticated (`gh auth status` → logged in with `repo`, `gist`, `read:org`, and `workflow` scopes).

### 2. Repository Orchestration
- Created the project directory and initialized a local Git repository:
  ```bash
  mkdir portfolio-project-100hires && cd portfolio-project-100hires
  git init -b main
  ```
- Created the remote repository on GitHub and linked it as `origin`:
  ```bash
  gh repo create portfolio-project-100hires --public --source=. --remote=origin
  ```

### 3. Extension Installation (Manual — Cursor GUI)
- Launched Cursor IDE and navigated to the **Extensions Marketplace** (`Cmd+Shift+X`).
- Searched for and installed **Claude Code** (Anthropic) — authenticated via Anthropic API key.
- Searched for and installed **Codex** (OpenAI) — authenticated via OpenAI API key.
- Restarted Cursor to ensure both extensions loaded their respective language models correctly.

---

## Issues and Solutions

### Issue: Homebrew PATH Warning and Authorization Token Synchronization Delay

**Symptom:** After upgrading Cursor via Homebrew, launching the IDE from the terminal produced a warning about outdated shell environment variables. Additionally, after installing Claude Code and Codex extensions through the Cursor GUI marketplace, the extensions failed to authenticate on first launch — displaying a "Token not recognized" or "Authorization pending" status despite valid API keys being entered.

**Root Cause:**
1. **PATH issue:** Homebrew places Cask-installed applications in `/Applications`, but the CLI shim (`/usr/local/bin/cursor`) relies on the shell's `PATH` being up-to-date. After a Homebrew upgrade, the previous symlink was unlinked and re-linked, but the running shell session still referenced the stale environment. Running `brew cleanup` (which had not executed in 30+ days) compounded the issue by leaving outdated formulae and cached artifacts on disk.
2. **Token synchronization delay:** Cursor's extension host process caches authentication state in memory at startup. When extensions are installed and immediately authenticated, the token handshake between the extension sandbox and the API provider (Anthropic/OpenAI) may not complete before the extension host initializes, causing a transient "unauthenticated" state. Restarting the IDE forces a fresh read of the on-disk token store and re-validates credentials against the respective OAuth endpoints.

**Solution:**
1. **PATH fix:** Verified and updated the shell configuration (`~/.zshrc`) to ensure `/usr/local/bin` precedes any user-local bin directories. Ran `source ~/.zshrc` and restarted the terminal session. Confirmed resolution by running `which cursor` and verifying it pointed to the updated Homebrew shim.
2. **Token fix:** Performed a full quit of Cursor (`Cmd+Q`), confirmed no residual `Cursor` processes were running (`pgrep -fl Cursor`), then relaunched. Both extensions initialized with valid authentication tokens immediately. For good measure, ran `brew cleanup` to remove stale cached artifacts and prevent future PATH-related drift.

---

## Repository Structure

```
portfolio-project-100hires/
├── README.md          # This document — project setup and toolchain documentation
└── .git/              # Git metadata (local repository)
```

---

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/24026926-afk/portfolio-project-100hires.git
   cd portfolio-project-100hires
   ```

2. Ensure the following are installed on your macOS system:
   - [Homebrew](https://brew.sh)
   - [Cursor IDE](https://cursor.com) (`brew install --cask cursor`)
   - [GitHub CLI](https://cli.github.com) (`brew install gh`)

3. Install Cursor extensions via the built-in Marketplace:
   - **Claude Code** — by Anthropic
   - **Codex** — by OpenAI

---

## License
This project is intended for portfolio demonstration purposes.
