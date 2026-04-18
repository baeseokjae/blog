---
title: "How to Set Up Windsurf IDE 2026: Installation, Config, and First Project"
date: 2026-04-17T23:15:00+00:00
tags: ["windsurf", "ai-ide", "tutorial", "cascade", "developer-tools"]
description: "Complete 2026 guide to installing and configuring Windsurf IDE — from download to your first Cascade flow in 20 minutes."
draft: false
cover:
  image: "/images/windsurf-setup-tutorial-2026.png"
  alt: "How to Set Up Windsurf IDE 2026"
  relative: false
schema: "schema-windsurf-setup-tutorial-2026"
---

Setting up Windsurf IDE in 2026 takes about 20 minutes — download the installer, run the onboarding wizard, create a `.windsurfrules` file, and flip Cascade to Codebase context mode. That sequence unlocks the AI features that make Windsurf worth using.

## Why Windsurf IDE in 2026?

Windsurf IDE is an AI-native code editor built around Cascade, an autonomous agent that plans multi-step tasks, executes terminal commands, and iterates without step-by-step instructions. As of March 2026, Windsurf has over 1 million active developers — double the user count from 2024 — and the AI writes 70 million lines of code per day across those sessions, with 94% of its code output being AI-generated. Over 4,000 enterprises now run Windsurf in production, including 59% of Fortune 500 companies. ServiceNow deployed it across roughly 7,000 engineers and reported a 10% productivity boost. Unlike VS Code with a Copilot plugin bolted on, Windsurf was designed from the ground up so the AI has deep access to your workspace: file tree, terminal, test runner, and diff view. The result is an IDE where you describe an outcome and Cascade figures out which files to create, edit, and test to get there. The $82M ARR Windsurf reported in mid-2025 reflects a market that's moved past curiosity into production adoption.

## System Requirements and Prerequisites

Before downloading, verify your machine meets the minimum specs for Windsurf IDE. Windsurf requires at least 8GB RAM to run comfortably — the AI completion engine and LSP servers consume meaningful memory even at idle, approximately 1.1GB just sitting open. For Codebase context mode, which indexes your entire project so Cascade can reason about it holistically, 16GB RAM is the recommended baseline. Projects over 50,000 lines will hit performance issues on 8GB machines in Codebase mode. The cold start time is 3.4 seconds on a modern machine, and AI completion latency averages 102ms in benchmarks from markaicode.com. Supported operating systems: macOS (minimum OS X Yosemite), Windows 10+, Ubuntu and other major Linux distributions. A Windsurf account is required for AI features; you can create one free during onboarding. The free tier includes 25 Cascade flow actions per month. Pro at $15/month removes the cap entirely.

### Minimum vs. Recommended Specs

| Spec | Minimum | Recommended |
|------|---------|-------------|
| RAM | 8 GB | 16 GB |
| OS | macOS Yosemite / Win 10 / Ubuntu 20.04 | macOS 13+ / Win 11 / Ubuntu 22.04 |
| Storage | 2 GB free | 5 GB free |
| Internet | Required for AI | Required for AI |

## Step 1: Download and Install Windsurf

Windsurf IDE installation differs slightly per platform, but all paths take under five minutes once the download completes. Download the installer from the official Windsurf website. On macOS, the recommended approach is to drag the `.app` file into `/Applications`, though Homebrew also works: `brew install --cask windsurf`. On Ubuntu and Debian-based Linux, download the `.deb` package and install it with `sudo dpkg -i windsurf-*.deb`, then run `sudo apt-get install -f` if there are dependency issues. On Windows, run the `.exe` installer with default settings — no configuration is required during install. After installation, launch Windsurf; the onboarding wizard starts automatically on first run. If macOS Gatekeeper blocks the app with an "unidentified developer" warning, open System Preferences → Privacy & Security, and click "Open Anyway" in the General tab. This is a one-time step; subsequent launches are unblocked.

### macOS Gatekeeper Fix

If you see "Windsurf cannot be opened because the developer cannot be verified":

1. Go to **System Preferences → Privacy & Security**
2. Scroll to the "Security" section
3. Click **Open Anyway** next to the Windsurf message
4. Enter your system password and confirm

## Step 2: Run the Onboarding Flow

The first-launch wizard walks you through three decisions that shape your Windsurf experience: setup path, theme, and account sign-in. For the setup path, you have three choices — Start fresh, Import from VS Code, or Import from Cursor. If you're migrating from either editor, pick the import option; Windsurf reads your existing extensions, keybindings, and settings from the source editor's config folder and applies them automatically. For new users, Start fresh gives you a clean baseline without any legacy configuration. Theme selection is cosmetic — Light, Dark, or Windsurf default. Keybindings offer VS Code-style or Vim bindings; pick based on your muscle memory since relearning keybindings adds friction to the first week. After these choices, you'll be prompted to sign in or create a Windsurf account. The free tier activates immediately on account creation with no credit card required. Once signed in, the main editor opens and Cascade initializes in the sidebar, ready for your first prompt.

## Step 3: Import VS Code or Cursor Configuration

If you chose Import during onboarding but want to add more extensions or settings later, use the Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux) and search for "Import Settings." Windsurf can pull extensions, snippets, and keybindings from VS Code and Cursor at any time — this is useful if you install a new extension in VS Code and want it in Windsurf without going through the extension marketplace again. One important caveat: some extensions are incompatible with Windsurf, specifically other AI code completion extensions (like GitHub Copilot or Tabnine) and certain proprietary extensions with closed binaries. Windsurf will warn you about conflicts during import; simply skip those extensions. If you were using a `.vscode/settings.json` file for workspace-level config, Windsurf reads it directly — no migration needed, since the file format is identical. Remote development via SSH works the same way VS Code handles it: install the Remote - SSH extension and connect to your server with the same connection strings.

## Step 4: Create Your `.windsurfrules` File

The `.windsurfrules` file is the single highest-leverage configuration change you can make in Windsurf IDE. It is a plain text file placed at your project root that tells Cascade your stack, coding conventions, and constraints — essentially a standing brief that the AI reads before every Cascade session in that project. Without it, Cascade makes reasonable guesses about your preferences, which means you spend the first few lines of every prompt re-establishing context. With a well-written `.windsurfrules` file, you cut prompt length roughly in half because that context is already loaded. Create the file at your project root: `touch .windsurfrules`. Then open it in Windsurf and write a structured brief covering: your language and framework ("TypeScript, Next.js 14, Tailwind CSS"), test setup ("Jest with React Testing Library, no snapshot tests"), deployment target ("Vercel, no Docker"), and explicit constraints ("never modify `lib/auth.ts` without asking first"). Commit this file to your repository so the whole team benefits from it.

### Example `.windsurfrules` File

```
Stack: TypeScript, Next.js 14 (App Router), Tailwind CSS, Prisma, PostgreSQL

Testing: Jest + React Testing Library. No snapshot tests. Tests live in __tests__ next to the component.

Patterns:
- Server Components by default. Client Components only when state/events are needed. Add "use client" explicitly.
- All database access through lib/db/. Never import Prisma client directly in components.
- API routes in app/api/ with Zod validation on all inputs.

Off-limits without asking: lib/auth.ts, prisma/schema.prisma, .env files

Preferred response format: code-first, then explain what changed and why.
```

## Step 5: Configure Cascade Context Mode

Cascade context mode determines how much of your project Windsurf's AI can see when it responds, and getting this setting right is the second most impactful configuration change after `.windsurfrules`. There are three modes. **File mode** (the default): Cascade only sees the file currently open and any files you explicitly reference with `@filename`. This is conservative and fast, and appropriate for single-file edits or machines with limited RAM. **Codebase mode**: Cascade indexes your entire project and can reason across all files without you specifying them — it answers "where does this endpoint get validated?" by actually reading your codebase rather than guessing. This is the right choice for any project under 50,000 lines on a 16GB machine. **Explicit references**: You manually drag files into the Cascade context or use `@` mentions. Good for surgical multi-file edits where you know exactly which files matter. To switch to Codebase mode, open Cascade in the sidebar, click the context selector at the top (shows "File" by default), and choose "Codebase." Windsurf will index your project; on a 10,000-line project this takes 10–30 seconds.

### Context Mode Comparison

| Mode | Best For | RAM Usage |
|------|----------|-----------|
| File | Single-file edits, < 8GB RAM | Low |
| Codebase | Multi-file tasks, refactoring, Q&A | Medium–High |
| Explicit (@) | Targeted multi-file edits | Medium |

## Step 6: Run Your First Cascade Flow

A Cascade flow is a multi-step AI task where Windsurf's Cascade agent reads files, writes code, runs terminal commands, and checks its own output — all without you manually switching between panels. To start a flow, open the Cascade sidebar and press `Cmd+Shift+L` (macOS) or `Ctrl+Shift+L` (Windows/Linux), or click the lightning bolt icon. The key insight for effective Cascade use is writing outcome-first prompts rather than instruction-first prompts. Instead of "edit the middleware to add rate limiting," write "add Redis-based rate limiting to all `/api/` routes: 100 req/minute per IP, return 429 with Retry-After header, environment variable for the limit." Cascade will read your existing route files, identify the middleware chain, install the Redis client if needed, write the middleware, wire it in, and run your tests. Devtoolsreview benchmarks show Cascade completing a Redis rate-limiting task in 3.5 minutes vs. 45–60 minutes manually. Cascade works correctly on clearly scoped tasks about 75–80% of the time. The most common failure mode is execution loops on ambiguous requirements — if Cascade has been running for more than 10 minutes without progress, cancel and refine your prompt.

### Writing Effective Cascade Prompts

| Weak Prompt | Strong Prompt |
|-------------|---------------|
| "Add tests" | "Add Jest unit tests for `lib/pricing.ts` covering: free tier limit, Pro upgrade path, and invalid plan code — use the existing test fixture pattern in `__tests__/lib/`" |
| "Fix the login" | "The login form at `app/(auth)/login/page.tsx` redirects to `/` instead of the originally-requested URL after sign-in. Fix it to use the `callbackUrl` query param, falling back to `/dashboard`" |
| "Refactor the API" | "Extract the auth check repeated in `app/api/users/route.ts` and `app/api/posts/route.ts` into a shared `withAuth` wrapper in `lib/api/middleware.ts`" |

## Step 7: Configure Memories and Rules

Windsurf Memories allow Cascade to persist information about your project across sessions — architecture decisions, team conventions, or debugging notes you don't want to re-explain every time you open a new Cascade session. Rules are project-level or global instructions that Cascade always follows, similar to `.windsurfrules` but managed through the UI. Think of Memories as dynamic context that grows as you work, and Rules as standing constraints. To manage Memories, open Cascade settings (gear icon in the sidebar) and navigate to the Memories tab. You can see what Cascade has learned, delete irrelevant or stale entries, and add new ones manually. Rules can be global (applied across all projects) or scoped to the current workspace. For teams, `.windsurfrules` in the repo is usually better because it's version-controlled and shared; individual Memories are better for personal preferences that shouldn't affect your teammates. A common pattern: use Memories to track things Cascade discovered about your codebase ("the auth flow uses a custom JWT implementation, not NextAuth"), and use Rules for preferences ("always suggest error boundaries around async data fetches").

## Step 8: Set Up Workspace Snippets and prompts.md

For prompts you run repeatedly — generating a new API route, creating a component scaffold, running a standard code review checklist — save them as workspace snippets or in a `prompts.md` file at your project root. Windsurf reads `prompts.md` and makes those prompts available via `@prompts` in Cascade, so instead of typing a 200-word prompt from memory, you reference it in two words. Create `prompts.md` with named sections: `## new-api-route`, `## component-scaffold`, `## code-review`. Each section body is the full prompt text with any placeholders noted. When working in Cascade, type `@prompts/new-api-route` and Windsurf injects the prompt — you only fill in the specifics like the route name and expected inputs. This is especially valuable for onboarding new team members: give them a `prompts.md` with your team's standard operations and they can run Cascade workflows correctly from day one without needing to know the conventions by heart.

## Step 9: Connect MCP Servers

Model Context Protocol (MCP) servers extend Windsurf's Cascade beyond your local file system, letting the AI interact with external tools — databases, APIs, documentation systems, issue trackers — using the same natural-language interface as local file operations. This is what separates a well-configured Windsurf setup from a basic one. To add an MCP server, open Windsurf settings (`Cmd+,`), navigate to the MCP section, and paste the server URL and any required authentication tokens. Windsurf ships with built-in MCP integrations for common tools, and the community maintains a registry of additional ones. Common setups include: a Postgres MCP server so Cascade can run queries and inspect schemas without you writing raw SQL in the chat, a GitHub MCP server so Cascade can read issues and open PRs directly from the editor, and a documentation MCP server so Cascade can fetch current library docs when it encounters unfamiliar APIs. After connecting an MCP server, test it in Cascade: "what tables are in the database?" or "list open issues in this repo." A working connection returns results within a few seconds.

## Step 10: Create Your First Project End-to-End

With your environment fully configured, run a complete first project to validate every piece of your Windsurf setup. Create a new folder, open it in Windsurf (`File → Open Folder`), and create your `.windsurfrules` file with your stack details. Switch Cascade to Codebase mode. Then write an outcome-first prompt describing the project: "Create a Next.js 14 App Router project with TypeScript and Tailwind that shows a list of blog posts from a JSON file. Include a `/posts/[slug]` dynamic route and basic dark mode support. Use the `shadcn/ui` card component for the post list." Cascade will scaffold the entire project structure, install dependencies, create the components, and wire up the routes — the same kind of task that benchmarks show completing in under 4 minutes. Review the diff Windsurf shows before accepting it; Cascade is accurate but not infallible, and reviewing its first major output in a new project helps you catch any mismatches between what you meant and what it understood. After accepting, run `npm run dev` and verify the result in your browser.

## Windsurf Pricing: Free, Pro, Teams, and Enterprise

Windsurf's pricing is tiered by Cascade usage, not by seat count or model access, which makes the math straightforward for teams trying to forecast costs. The **Free tier** ($0) includes 25 Cascade flow actions per month, basic AI completions, and all editor features. This is enough to evaluate the tool seriously but not for daily professional use — 25 flow actions disappears in two or three working sessions. **Pro** ($15/month) removes the flow action cap and adds priority access to the latest models — this is the right choice for individual developers who use Cascade regularly. **Teams** ($30/user/month) adds collaboration features, shared rules and snippets, centralized billing, and usage analytics. **Enterprise** pricing is custom and adds SSO (SAML, OIDC), FedRAMP High compliance, HIPAA, SOC 2 Type II, RBAC, hybrid deployment options, and dedicated support. The comparison to Cursor Pro at $20/month makes Windsurf 25% cheaper for agent-heavy workflows where you're primarily using the AI agent rather than the inline completion features.

### Pricing at a Glance

| Tier | Price | Cascade Actions | Best For |
|------|-------|-----------------|----------|
| Free | $0 | 25/month | Evaluation |
| Pro | $15/month | Unlimited | Individual devs |
| Teams | $30/user/month | Unlimited | Small–mid teams |
| Enterprise | Custom | Unlimited | Large orgs, compliance |

## Troubleshooting Common Setup Issues

Most Windsurf setup problems fall into three categories that each have straightforward fixes. **macOS Gatekeeper blocks**: If Windsurf won't open because macOS "cannot verify the developer," open System Preferences → Privacy & Security and click "Open Anyway" — this is a one-time step and the app opens normally afterward. **Ubuntu dependency failures**: If Windsurf installs but won't launch on Ubuntu, run `sudo apt-get install -f` to pull any missing shared libraries, then relaunch. **Cascade execution loops**: If Cascade runs for more than 10 minutes without producing output or finishing, it has hit an ambiguous requirement or a circular dependency in its reasoning. Press `Esc` in the Cascade sidebar to cancel, reread your original prompt, identify what was unclear or contradictory, and break the task into smaller steps before re-running. The 75–80% success rate on clearly scoped tasks means the remaining 20–25% is almost always a prompt specificity problem, not a model limitation. **High memory usage**: if Windsurf is consuming excessive RAM, switch from Codebase mode to File mode for the current session — this disables the project-wide index and reduces memory footprint significantly.

## Windsurf vs. Cursor: Different Setup Philosophies

Understanding the philosophical difference between Windsurf and Cursor setup helps you configure each one correctly — and helps you decide which fits your workflow before investing time in configuration. Cursor's setup emphasizes fine-grained control: you configure which files the AI can see, how much context to include, and when it can make unsupervised changes. It's a precision instrument designed for developers who want to review every AI suggestion before it lands. Windsurf's setup is about building contextual trust: you write a `.windsurfrules` file that gives Cascade enough background to act autonomously, then describe outcomes instead of steps. The practical difference shows up in autocomplete: Cursor's multi-line completions are immediately usable 68–72% of the time, while Windsurf's completions are more conservative but more accurate when they do appear. For developers who prefer reviewing every suggestion, Cursor feels more natural. For developers who want to describe an outcome and handle the result, Windsurf's Cascade delivers. At $15/month vs. Cursor's $20/month, Windsurf costs 25% less for agent-heavy users.

## Tips for Enterprise Teams

Enterprise Windsurf deployments require a few additional setup steps beyond the standard installation process. SSO integration (SAML 2.0 or OIDC) is configured in the Windsurf enterprise admin console — you'll need the identity provider metadata URL and to whitelist Windsurf's assertion consumer service URL in your IdP. Plan for a 30–60 minute SSO setup session with your IT team. RBAC allows you to define which teams have access to which MCP servers and which Cascade capabilities; this is critical in regulated industries where you don't want developers querying production databases via Cascade without controls. FedRAMP High and HIPAA compliance are enabled at the tenant level, not the individual account level — coordinate with your Windsurf account team to activate these before your first production deployment, not after. The 4,000+ enterprises currently in production on Windsurf have largely standardized on centralized `.windsurfrules` files stored in a shared repository that teams fork for their specific projects. This is the fastest path to consistent AI behavior across a large engineering organization and eliminates the "everyone has different Cascade behavior" problem that emerges when teams configure independently.

## FAQ

These are the most common questions developers ask when setting up Windsurf IDE for the first time. Windsurf's free tier gives you 25 Cascade flow actions per month — enough for evaluation but not for sustained daily use. The Pro plan at $15/month removes that cap and adds priority model access, making it the right choice for anyone using Cascade more than a few times per week. The setup questions below — importing VS Code settings, configuring `.windsurfrules`, choosing the right context mode — are the configuration decisions that have the highest impact on your first week productivity. Getting them right before you start your first real project saves hours of re-prompting and configuration mid-task. The Cascade execution loop question is the most common support issue; the answer is almost always prompt specificity, not a model failure.

### Is Windsurf IDE free to use?

Yes, Windsurf has a free tier that includes 25 Cascade flow actions per month, unlimited AI completions, and all editor features. The free tier is sufficient for evaluation but limited for daily professional use — 25 flow actions typically runs out within a few working sessions. Pro at $15/month removes the Cascade action cap entirely.

### How do I import my VS Code settings into Windsurf?

During the onboarding wizard, select "Import from VS Code." If you've already completed onboarding, open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`) and search "Import Settings." Windsurf reads extensions, keybindings, and settings from VS Code's config folder automatically. Incompatible extensions — other AI completions, some proprietary tools — will be flagged and skipped.

### What is the `.windsurfrules` file and do I need one?

The `.windsurfrules` file is a plain text file at your project root that tells Cascade your stack, coding conventions, and constraints before each session. You don't technically need one — Windsurf works without it — but it's the highest-leverage configuration you can make. It cuts prompt length roughly in half by eliminating the need to re-establish project context on every query.

### When should I use Codebase context mode vs. File mode?

Use Codebase mode for any multi-file task: refactoring, adding a feature that touches multiple files, debugging across modules, or asking architectural questions about your project. Use File mode for single-file edits on large projects (over 50,000 lines) where you need faster responses, or on machines with only 8GB RAM. Codebase mode is more powerful but requires 16GB RAM for comfortable use.

### How do I stop Cascade from getting stuck in an execution loop?

If Cascade runs for more than 10 minutes without completing, press `Esc` in the Cascade sidebar to cancel. Reread your original prompt and identify what was ambiguous — execution loops usually happen when requirements are contradictory or when the task has hidden preconditions, like a missing environment variable or an uninstalled dependency. Break the task into two smaller steps, add the missing constraint, and re-run.
