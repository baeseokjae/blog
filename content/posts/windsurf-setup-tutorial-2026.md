---
title: "How to Set Up Windsurf IDE 2026: Installation, Config, and First Project Guide"
date: 2026-04-17T22:09:28+00:00
tags: ["windsurf", "ai-ide", "setup-guide", "cascade", "developer-tools"]
description: "Step-by-step guide to installing and configuring Windsurf IDE in 2026 — from download to first Cascade flow with .windsurfrules and Codebase context mode."
draft: false
cover:
  image: "/images/windsurf-setup-tutorial-2026.png"
  alt: "How to Set Up Windsurf IDE 2026"
  relative: false
schema: "schema-windsurf-setup-tutorial-2026"
---

Setting up Windsurf IDE in 2026 takes under 20 minutes: download, install, complete the onboarding wizard, create a `.windsurfrules` file at your project root, switch Cascade to Codebase context mode, and describe the outcome you want — Windsurf's autonomous agent handles the rest.

## Why Windsurf IDE in 2026?

Windsurf IDE is an AI-native code editor built on Codeium's infrastructure that treats its AI agent — Cascade — as a first-class collaborator rather than a tab-complete plugin. As of March 2026, Windsurf has 1M+ active users (doubled from 500k+ in 2024), generates 70M+ lines of AI-written code per day, and is deployed inside 4,000+ enterprises — including 59% of Fortune 500 companies. ServiceNow rolled out Windsurf to ~7,000 engineers and reported a 10% productivity boost. The core value proposition is autonomy: you describe what you want to build, Cascade plans the multi-step workflow, executes it — reading files, running terminal commands, writing tests, fixing errors — and iterates until done. With the AI coding-tool market crossing $7B in annual revenue by April 2026 and 84% of developers using AI tools in their workflow (Stack Overflow 2025), Windsurf represents the current leading edge of autonomous-agent IDEs. Cascade handles clearly scoped tasks correctly about 75-80% of the time, making it a genuine productivity multiplier for developers who learn to write outcome-first prompts.

## System Requirements

Windsurf runs on macOS (OS X Yosemite and later), Windows 10/11, Ubuntu 20.04+, and most mainstream Linux distributions. Cold start time is 3.4 seconds on a modern machine; AI completion latency averages ~102ms. The RAM requirements directly determine which Cascade context modes you can use:

| Spec | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB |
| Storage | 2 GB free | 5 GB free |
| CPU | Dual-core x64 | Quad-core x64 |
| OS (macOS) | OS X Yosemite | macOS Ventura+ |
| OS (Linux) | Ubuntu 20.04 | Ubuntu 22.04+ |

The 16 GB RAM recommendation matters primarily for **Codebase context mode** on projects larger than ~30k lines. In Codebase mode, Cascade indexes your entire repo into a local embedding store. On 8 GB RAM with a large project, that process may thrash swap and degrade completion performance. For projects under 30k lines or single-file work, 8 GB is fine.

**Note:** Windsurf does not support VS Code Dev Containers natively. If your workflow depends heavily on Dev Containers, account for that gap before migrating.

## Step 1: Download and Install Windsurf

Windsurf IDE is available for macOS (OS X Yosemite or later), Windows 10/11, and Linux (Ubuntu 20.04+, Debian 10+) as a direct download from windsurf.com or via package managers. The installer is about 350 MB; the full footprint including initial cache reaches approximately 500 MB after first launch. On macOS, Homebrew is the recommended install path for developers who manage machine configs with a `Brewfile` — the single command handles download, verification, and PATH setup. On Windows, the `.exe` runs as a standard user install with no admin rights required. On Linux, the `.deb` package auto-registers a desktop entry and adds the `windsurf` CLI to PATH. After installation on any platform, you can open any project directory with `windsurf .` from the terminal. Total install time is typically 3-5 minutes on broadband. The application ships with Codeium's completion engine included — no separate plugin installation required.

### macOS Installation

```bash
# Homebrew (recommended for managed dev machines)
brew install --cask windsurf

# Or: download the .dmg from windsurf.com, drag to /Applications
```

If macOS Gatekeeper blocks the first launch ("developer cannot be verified"), run:

```bash
xattr -cr /Applications/Windsurf.app
```

This removes the quarantine attribute and only needs to be run once.

### Windows Installation

Download the `.exe` installer from windsurf.com. No admin rights required — it installs to `%LOCALAPPDATA%\Programs\Windsurf` and adds itself to PATH automatically.

### Ubuntu / Linux Installation

```bash
# .deb package (Ubuntu/Debian)
wget https://windsurf.com/download/linux/deb -O windsurf.deb
sudo dpkg -i windsurf.deb
sudo apt-get install -f   # resolve any dependency issues

# AppImage (no install required — works on Fedora/RHEL)
chmod +x Windsurf-<version>.AppImage
./Windsurf-<version>.AppImage
```

The `.deb` path handles PATH and desktop integration automatically. For RHEL/Fedora, use the AppImage since Windsurf doesn't publish `.rpm` packages.

## Step 2: Complete the Onboarding Flow

Windsurf's first-launch wizard sets three things: your configuration source, your theme, and your account. The choices here have downstream consequences worth getting right.

**Setup path options:**

| Path | When to choose |
|---|---|
| **Start Fresh** | New to AI IDEs, want a clean slate |
| **Import from VS Code** | Migrating from VS Code — copies extensions, keybindings, settings.json |
| **Import from Cursor** | Migrating from Cursor — same as VS Code import plus Cursor-specific configs |

After choosing a path, the wizard asks for a color theme and keybinding style (VS Code defaults or Vim). Then sign up or log in — the free tier requires an account.

**Important:** Windsurf blocks competing AI completions extensions (GitHub Copilot, Tabnine, Codeium's own VS Code extension) because running two completion engines simultaneously causes conflicts and degraded performance. After importing from VS Code, you'll see an incompatibility warning for these — they simply won't load. Disable them in your VS Code profile too if you plan to use both editors.

You can re-run the VS Code import after onboarding: Command Palette → `Windsurf: Import VS Code Settings`.

## Step 3: Create Your `.windsurfrules` File

The `.windsurfrules` file is the single highest-leverage configuration change you can make after installing Windsurf. It is a plain-text file placed at your project root that Cascade reads at the start of every session to understand your stack, coding conventions, and off-limits areas. Without it, Cascade makes reasonable guesses — but those guesses cost tokens and occasionally produce wrong assumptions about your patterns. A well-written `.windsurfrules` cuts prompt length roughly in half because you never have to re-explain your stack or naming conventions. Think of it as the standing brief you'd give a new contractor: here's what we're building, here's how we write code, here's what never to touch.

Create the file:

```bash
touch .windsurfrules
```

A solid starting template for a TypeScript/Node project:

```
# Stack
Runtime: Node 22, TypeScript 5.4 strict mode
Framework: Express 5, Prisma 5 (PostgreSQL)
Test runner: Vitest
Package manager: pnpm

# Conventions
- All files use named exports — no default exports
- Database queries live in src/db/ — never inline in route handlers
- Error handling: use Result<T, E> pattern from src/lib/result.ts
- No console.log in production code — use the logger at src/lib/logger.ts

# Boundaries
- Never modify migrations directly — create a new migration file
- Don't touch src/generated/ — auto-generated by Prisma
- Ask before adding new dependencies

# Testing
- Vitest unit tests alongside source files
- Integration tests in tests/integration/
- Don't mock the database in integration tests
```

The `Boundaries` section is particularly effective. Cascade respects explicit "never touch" constraints reliably and it prevents the most common source of agent loops on existing codebases.

Commit `.windsurfrules` to the repo so your whole team benefits from the same context. Only add it to `.gitignore` if it contains personal preferences that differ per developer.

## Step 4: Configure Cascade Context Mode

Cascade context mode determines how much of your codebase the AI can see when planning a task. Choosing the wrong mode is one of the most common causes of poor Cascade output — either it lacks context to understand what already exists, or it loads too much and slows down. For most projects under 50k lines, setting Cascade to Codebase mode immediately after opening a project resolves the majority of "Cascade created a duplicate utility / used an outdated API" complaints from new users. File mode (the default) only loads the currently open file and a few recent ones — fine for isolated single-file edits, but it breaks down on tasks that touch multiple modules.

Access context mode from the Cascade panel (bottom of the left sidebar) → context selector dropdown:

| Mode | What Cascade sees | Best for |
|---|---|---|
| **File** (default) | Current file + recent files | Single-file edits, large codebases on 8 GB RAM |
| **Codebase** | Full project, indexed locally | Multi-file refactors, features, projects under 50k lines |
| **Manual (@file)** | Only explicitly referenced files | Surgical edits, large monorepos, sensitive context control |

**Recommendation:** Switch to **Codebase mode** immediately after opening a new project. Initial indexing takes 10-30 seconds; incremental updates after edits are near-instant.

If Codebase mode crashes or fails to index, you're likely on 8 GB RAM with a project over 30k lines. Either switch to `@file` references mode or create a `.windsurfignore` file (`.gitignore` syntax) to exclude `node_modules`, build artifacts, and generated directories.

## Step 5: Run Your First Cascade Flow

A Cascade flow is a multi-step agentic task where Cascade plans the work, executes it sequentially — reading files, writing changes, running terminal commands, running tests — and loops on failures until done, all without step-by-step prompting. The keyboard shortcut is `Cmd+Shift+L` on macOS or `Ctrl+Shift+L` on Windows/Linux. A benchmark from devtoolsreview.com: Cascade completed a Redis rate limiting implementation (reading existing files, writing middleware, adding env vars, wiring routes, writing tests, fixing test failures) in 3.5 minutes vs 45-60 minutes manually. The critical technique that makes that possible is outcome-first prompting — describing what you want, not how to do it.

**Bad prompt:** "Open auth.ts, add a middleware function, check the Authorization header, decode the JWT, attach user to req.user"

**Good prompt:** "Add JWT authentication middleware that validates Bearer tokens against JWT_SECRET env var and attaches the decoded user to req.user. Use our existing logger and Result pattern."

The second prompt lets Cascade plan the execution rather than follow a script. It reads your `.windsurfrules`, understands the Result pattern, and writes code that fits your conventions.

**Starting a flow:**
1. Press `Cmd+Shift+L` to open Cascade panel
2. Write your outcome-first prompt
3. Cascade shows a plan — review and approve or refine
4. Watch the execution log in real time

**One caveat:** On complex or ambiguous tasks, Cascade can enter execution loops — making the same change repeatedly without making progress. If this happens, press `Escape` to stop, identify the ambiguous constraint, tighten your `.windsurfrules`, and restart with a more specific prompt.

## Step 6: Set Up Memories and Rules

Windsurf Memories are persistent facts Cascade stores and retrieves across sessions — not just for one project but globally. Rules are standing behavioral guidelines that apply to every Cascade session. Together, they replace the need to repeat context in every prompt and prevent Cascade from regressing on previously established patterns after a context reset. Access both from Settings (`Cmd+,`) → Windsurf → Memories & Rules. The most effective setup adds 3-5 rules during initial configuration — universal preferences like "Never use `any` type in TypeScript" or "Always prefer functional components over class components in React" — and then lets Cascade auto-create project-specific Memories during flows as it learns facts about your codebase.

**Adding rules:**
```
Settings → Windsurf → Rules → Add Rule

Examples:
- Always use TypeScript strict mode
- Never use any type
- Prefer named exports over default exports
- Run tests after every code change
```

**Adding Memories manually:** During a Cascade session, say "Remember that this project deploys to Railway" or "Remember that we use Prisma 5's client extensions API." Cascade confirms and stores the fact, which it retrieves automatically in future sessions.

`.windsurfrules` handles project-specific conventions; Rules handle universal preferences; Memories handle session-learned facts. Use all three layers for the best results.

## Step 7: Workspace Snippets and `prompts.md`

Windsurf supports a `prompts.md` file at the project root that stores reusable Cascade prompt templates — a productivity pattern that teams find essential once a project has established workflows. Instead of rewriting the same scaffolding prompt every time you need to generate a new component, add a migration, or scaffold a route, define it once in `prompts.md` and reference it with `@prompts.md {template-name}` in any Cascade flow. The format is plain Markdown with `##` headings as template names. Committing `prompts.md` to the repo standardizes how every developer initiates common tasks, eliminating prompt quality variance across the team. Unlike `.windsurfrules` (applied globally each session), prompt templates are invoked explicitly per task, giving precise control over when templates fire. For solo developers, even 3-5 templates for common operations like generating typed API routes, creating test suites, or running a standard pre-commit check save meaningful time per week.

Example `prompts.md`:

```markdown
### generate-route
Create a new Express route at src/routes/{name}.ts.
Include: TypeScript types, Zod validation, error handling using Result pattern.
Create a corresponding test file at src/routes/{name}.test.ts with at least 3 test cases.
Run: pnpm test {name} after writing.

### add-migration
Create a new Prisma migration for the change I describe.
Do not modify the existing schema file directly — add to it.
Generate the migration file and run: pnpm prisma migrate dev --name {name}.
```

## Step 8: Connect MCP Servers

MCP (Model Context Protocol) servers extend Cascade's capabilities beyond the filesystem — giving it access to databases, GitHub, Slack, browser automation, and internal APIs. Windsurf has native MCP support as of 2026, configured through a `mcp_config.json` file. With MCP, a single Cascade flow can read your database schema, write and test a migration, create a GitHub PR, and post a summary to Slack — without leaving the editor. This is particularly powerful for enterprise teams where context switches between tools are a major source of developer overhead. Adding an MCP server takes about 2 minutes: open the MCP config file, define the server, and reload Windsurf. Cascade lists available MCP tools in its context panel and uses them autonomously when they're relevant to the task.

Open Command Palette → `Windsurf: Open MCP Config` to edit `mcp_config.json`:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

After saving, reload the window (`Cmd+Shift+P` → `Reload Window`). Popular MCP servers: GitHub (PRs, issues), Postgres (schema queries), Linear (tickets), Brave Search (web lookup during flows), and Playwright (browser automation).

## Step 9: Create Your First Project — Full Walkthrough

With Windsurf configured, here is a complete walkthrough creating a new Express API project from scratch using Cascade, demonstrating the full setup flow in a real scenario:

**1. Open an empty folder:**

```bash
mkdir my-api && cd my-api
windsurf .
```

**2. Create `.windsurfrules`:**

```
Stack: Node.js 22, Express 5, TypeScript 5 strict mode
Package manager: pnpm
Test framework: Vitest
```

**3. Switch to Codebase context mode** in the Cascade panel.

**4. Open a Cascade Flow** (`Cmd+Shift+L`) and paste:

```
Scaffold a new Express 5 + TypeScript project with pnpm and Vitest.
Include:
- package.json with express, typescript, zod, @types/node, @types/express
- tsconfig.json targeting Node 22, strict mode
- src/index.ts with a health check at GET /health
- src/routes/ with a users CRUD router (in-memory array for now)
- Vitest config and one test for the health endpoint
Run: pnpm install && pnpm test after scaffolding. Fix any test failures.
```

**5. Watch Cascade execute** — it creates all files, runs the install, executes tests, and fixes any failures automatically. Total time from empty folder to passing tests: approximately 3-5 minutes.

## Windsurf Pricing Tiers

Windsurf offers four pricing tiers as of 2026: Free, Pro, Teams, and Enterprise. The free tier includes 25 Cascade flow actions per month — enough for initial evaluation but not sustained daily development. Pro at $15/month removes the flow action cap and is the right choice for individual developers who use Cascade regularly. Teams at $30/user/month adds shared context and admin controls. Enterprise unlocks SSO (SAML/OIDC), FedRAMP High, HIPAA compliance, RBAC, and hybrid/on-premises deployment. For context on value: Cursor Pro is $20/month, making Windsurf the more affordable option for agent-heavy workflows. The free tier's 25 flow actions reset monthly; a complex multi-file Cascade task consumes roughly one flow action regardless of how many files it touches.

| Plan | Price | Cascade Flow Actions | Best for |
|---|---|---|---|
| **Free** | $0/month | 25/month | Evaluation, light use |
| **Pro** | $15/month | Unlimited | Individual developers |
| **Teams** | $30/user/month | Unlimited + shared context | Small to mid-size teams |
| **Enterprise** | Custom | Custom + RBAC, SSO, FedRAMP | Regulated industries, large orgs |

## Troubleshooting Common Setup Issues

Most Windsurf setup problems fall into five categories: macOS Gatekeeper blocking the first launch, Cascade entering execution loops on ambiguous tasks, Codebase context mode failing due to insufficient RAM, VS Code extension conflicts after migration, and Linux dependency errors after package install. The underlying cause of most Cascade quality issues — loops, wrong file edits, missing context, duplicate utilities — is insufficient prompt specificity or a missing `.windsurfrules` configuration file, not bugs in the tool itself. Before debugging agent behavior, verify you have both a `.windsurfrules` file at the project root and Codebase context mode enabled in the Cascade panel. These two settings resolve the majority of first-week complaints from new users switching from VS Code or Cursor. For hardware-related failures (RAM-caused context crashes), the fix is either upgrading to 16 GB or switching to `@file` reference mode for large projects. The fixes below cover all five categories — none require reinstalling Windsurf or starting your configuration over.

### macOS Gatekeeper Block

```bash
xattr -cr /Applications/Windsurf.app
```

Run this once after install. Alternatively: System Settings → Privacy & Security → "Windsurf was blocked" → Open Anyway.

### Cascade Enters a Loop

If Cascade repeats the same failing fix:
1. Press `Escape` to stop the flow
2. Read Cascade's last action in the conversation panel
3. Identify the missing or ambiguous constraint
4. Add it to `.windsurfrules` as an explicit boundary
5. Restart with a more specific prompt

Loops most commonly happen on tasks involving existing code Cascade doesn't fully understand, or tasks with conflicting constraints in the codebase.

### Codebase Mode Fails on Large Projects

You're likely under 16 GB RAM with a project over 30k lines. Two options:
- Switch to `@file` references mode (manually reference files in your prompt)
- Create `.windsurfignore` (`.gitignore` syntax) excluding `node_modules/`, `dist/`, `.next/`, and other generated directories

### VS Code Extension Conflicts

After VS Code import, disable competing AI completions extensions (GitHub Copilot, Tabnine). Open Extensions panel, search "Copilot" or "AI", and disable. Running two completion engines simultaneously causes conflicts at the editor API level.

### Linux Dependency Errors

On Ubuntu after `dpkg -i windsurf.deb`:

```bash
sudo apt-get install -f
```

If that fails, manually install the two most common missing dependencies:

```bash
sudo apt-get install libgbm1 libasound2
```

## Windsurf vs Cursor: Setup Philosophy

Windsurf and Cursor are both VS Code forks with AI agents, but their setup philosophies differ in a fundamental way: Windsurf is built around autonomous execution, while Cursor is precision-oriented. Windsurf's setup investment is front-loaded — you spend time on `.windsurfrules`, Memories, and context configuration upfront, then Cascade handles tasks end-to-end. Cursor's setup is lighter but the work is distributed throughout each session as you guide the agent step by step. Neither is objectively better. Windsurf pays off on prototyping, greenfield projects, and repetitive implementation tasks (scaffolding, migrations, test coverage). Cursor stays more in control for exploratory work — reading unfamiliar codebases and making targeted surgical changes. The autocomplete philosophies also differ: Windsurf is conservative (current line + 2-3 lines), while Cursor is more aggressive with multi-line completions immediately usable 68-72% of the time.

| Aspect | Windsurf | Cursor |
|---|---|---|
| Setup time | ~20 min (with .windsurfrules) | ~10 min |
| Config investment | High (.windsurfrules, Memories, context mode) | Low |
| Agent autonomy | High — Cascade plans and executes full tasks | Medium — confirms steps with user |
| Autocomplete style | Conservative (line + 2-3) | Aggressive multi-line |
| Workflow fit | Outcome-first prompts, prototyping | Step-by-step guidance, surgical edits |
| Pro pricing | $15/month | $20/month |

## Enterprise Team Setup: SSO, FedRAMP, and RBAC

Windsurf Enterprise adds RBAC (role-based access control), SSO via SAML 2.0 or OIDC, FedRAMP High and HIPAA compliance, and hybrid deployment — relevant for government contractors, healthcare organizations, and any enterprise with procurement requirements that block standard SaaS AI tools. SOC 2 Type II certification means audit logs, access controls, and data handling meet enterprise procurement requirements. The enterprise setup path begins with provisioning a Windsurf tenant through your account manager, then integrating SSO through your identity provider (Okta, Azure AD, and Google Workspace are supported out of the box). RBAC policies control which users can access which Cascade capabilities and MCP server connections — preventing, for example, production database access for developers without that clearance level. ServiceNow's deployment across ~7,000 engineers used the SSO + RBAC combination to roll out Windsurf as a standard toolchain item with zero per-user configuration. With 4,000+ enterprises and 59% of Fortune 500 in production, Windsurf's enterprise tier has the compliance track record to pass most security reviews.

## FAQ

**How long does Windsurf setup take from download to first Cascade flow?**
With a `.windsurfrules` file and Codebase context mode configured, the full setup takes 15-20 minutes: 2-3 minutes to download and install, 2-3 minutes for onboarding, 5-7 minutes to write `.windsurfrules`, and a few minutes to switch context mode and run your first flow. Most of that time is project indexing on first open.

**Can I use Windsurf if I'm already paying for GitHub Copilot?**
You can have both installed, but you must disable Copilot within Windsurf. Running two AI completion engines simultaneously causes conflicts at the editor API level — both work poorly. Windsurf uses Codeium's completion engine, which is included in all plans. Evaluate whether Windsurf's Cascade agent replaces your Copilot use case before canceling Copilot.

**What happens when the free tier hits 25 flow actions?**
Cascade stops executing autonomous multi-step plans. Basic completions and chat still work. Upgrade to Pro ($15/month) for unlimited flow actions, or wait for the monthly reset. The 25-action limit runs out in roughly the first week for active daily users.

**Is Windsurf safe to use with a sensitive codebase?**
Windsurf sends code to Codeium's servers for context processing by default. Enterprise plan users can configure VPC or on-premises deployment to keep all code within their own infrastructure. For sensitive codebases, use Enterprise with VPC deployment and review Windsurf's data processing agreement. SOC 2 Type II and FedRAMP High certifications are available for compliance documentation.

**What is the difference between `.windsurfrules`, Memories, and Rules?**
`.windsurfrules` is a project-scoped plain-text file committed to your repo — stack, conventions, boundaries for that specific project. Rules (in Settings) are global preferences that apply to every Cascade session across all projects. Memories are facts Cascade learns and stores during flows — project-specific but managed by Windsurf, not by you. Use all three for the best results: Rules for universal style preferences, `.windsurfrules` for project constraints, and Memories for session-learned facts.
