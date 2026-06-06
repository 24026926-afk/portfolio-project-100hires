# AGENTS.md — AI SEO Research Project

> **Context handoff document.** Read this first before doing any work in this
> repo. It tells every IDE agent (Antigravity, Cursor, Claude Code, Codex) what
> the project is, what has been done, and what remains.

---

## What this project is

A take-home assignment for a **Marketing Specialist** role at
[100Hires](https://100hires.com) — a B2B SaaS applicant-tracking system for
startups and SMBs — submitted by **Dante**.

**Deliverable:** pick ONE topic from the provided list, find **10 high-signal
experts**, collect their recent content via APIs and technical tools, organize it
in this repo as raw material for a future playbook, and reply to CEO Alex
Kravets with the repo link.

**Deadline:** 3 days.

**Evaluation criteria:**

| Criterion | What it means |
|-----------|---------------|
| Expert quality | Genuinely strong, respected voices — **NOT** the first Google results |
| Repo structure | Clean, navigable, well-organized |
| Technical ability | Comfortable working with APIs and tooling |
| Playbook-ready material | The collected content must support writing a real playbook |

> **"10 high-signal sources beat 50 generic ones."** — Volume is not scored;
> signal quality is everything.

---

## Chosen topic

**AI-powered SEO content production** (option #3 from the brief).

Why this topic:

- 100Hires is an ATS product — its growth depends on organic search. SEO is
  existential, not optional.
- The top practitioners in AI + SEO publish actively on YouTube, making
  transcript collection practical via API.
- The space is moving fast (AI Overviews, agentic SEO, programmatic content),
  so recent content is both abundant and high-value.

---

## The experts (validate to a final 10)

Strategic balance: mix **"produce at scale"** voices with **"does it actually
rank / is it quality"** voices.

### YouTube (collect via Supadata)

| Expert | Affiliation | Why high-signal |
|--------|-------------|-----------------|
| **Aleyda Solís** | Orainti / SEOFOMO / LearningSEO.io | AI-search authority, hosts "Crawling Mondays", SEOFOMO newsletter 40 k+ subscribers |
| **Sam Oh** | Ahrefs | Ultra-practical YouTube tutorials, massive catalog of actionable SEO walkthroughs |
| **Ross Simmonds** | Foundation Inc | B2B content + distribution strategy, AI content workflows |
| **Nathan Gotch** | Gotch SEO | Practical AI-SEO frameworks with step-by-step breakdowns |
| **Wil Reynolds** | Seer Interactive | Focuses on real user intent over generic "optimize for bots" advice |

### Manual (LinkedIn / newsletter / podcast)

| Expert | Affiliation | Why high-signal |
|--------|-------------|-----------------|
| **Kevin Indig** | Growth Memo | Data-driven strategy, AIO research, coined "agentic SEO" |
| **Jake Ward** | — | Programmatic + AI content at scale, publishes real case studies with numbers |
| **Eli Schwartz** | Author, *Product-Led SEO* | B2B SaaS SEO strategist, counterweight to pure-volume approaches |
| **Lily Ray** | Amsive | Algorithms, E-E-A-T, AI Overviews — what makes AI content actually rank |
| **Marie Haynes** | Marie Haynes Consulting | E-E-A-T authority, deep research on how Google and LLMs judge content quality |

### Bench (swap-ins if needed)

- **Tim Soulo** (Ahrefs CMO)
- **Bernard Huang** (Clearscope)
- **Mark Williams-Cook** (AlsoAsked)

> **Recency rule:** pick content from the **last 6–12 months** — AI search
> moves fast and older material loses relevance quickly.

---

## Repo structure

```
portfolio-project-100hires/
├── AGENTS.md                          # ← you are here
├── README.md                          # project overview + toolchain docs
└── research/
    ├── sources.md                     # all experts: link, date, 2–3 line annotation
    ├── linkedin-posts/                # posts by author (collected manually)
    │   └── .gitkeep
    ├── youtube-transcripts/           # transcripts by author (via collect_transcripts.py)
    │   └── .gitkeep
    └── other/                         # additional material (newsletters, podcasts, etc.)
        └── .gitkeep
```

---

## Tools & conventions

### YouTube transcripts

- Collected via `collect_transcripts.py` using the **Supadata API** (free tier:
  100 requests/month).
- The API key is read from the environment variable `SUPADATA_API_KEY` — **never
  hardcode it**.

### LinkedIn

- Collect posts **manually**. Do NOT scrape — it violates LinkedIn's ToS and is
  a time sink.

### Transcript file format

Every transcript file must include YAML frontmatter:

```yaml
---
author: "Sam Oh"
source_url: "https://www.youtube.com/watch?v=XXXXXXXXXXX"
video_id: "XXXXXXXXXXX"
lang: "en"
collected: "2026-06-06"
---
```

### Commit discipline

- **Commit per block of progress** — NOT one giant commit at the end. This is
  explicitly evaluated.
- Use conventional-commit-style messages (`feat:`, `docs:`, `chore:`).

### sources.md annotations

This file is the **differentiator**. Each expert entry must include 2–3 specific
lines explaining *why* they are high-signal — not just "they do SEO."

---

## Status & next steps

- [x] Repo created + pushed to GitHub
- [x] `research/` directory structure created (sources.md, linkedin-posts/,
      youtube-transcripts/, other/) — commit `ff7d0ef`
- [ ] Validate the final 10 experts
- [ ] Get Supadata API key, fill `SOURCES` in `collect_transcripts.py`, run it
- [ ] Manually collect LinkedIn / newsletter posts for the manual experts
- [ ] Write `sources.md` with per-expert annotations
- [ ] Rewrite `README.md` (what was collected, why these 10 experts, chosen topic)
- [ ] Final review + push

---

*Last updated: 2026-06-06 · Latest commit on main: `ff7d0ef`*
