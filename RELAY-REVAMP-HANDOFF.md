# Relay Customer Panel — Revamp Handoff

**Purpose of this document:** a complete, self-contained brief for building a non-functional prototype (NFP) of the redesigned Relay customer panel. It is written so that an engineer or agent with no prior context can build from it without asking questions.

**Deliverable:** a single self-contained `relay-prototype.html` file. No build step, no npm install, no dependencies beyond Google Fonts over CDN. It must open by double-clicking in Chrome.

**Audience for the prototype:** the internal Relay team. This is a pitch artifact meant to align people on a direction — persuasion and clarity of concept matter more than feature completeness or production readiness.

**Data:** entirely invented but plausible. Use the cast and content in §13 verbatim so the screens tell one coherent story.

---

## 1. What Relay is

Relay is positioned as **"the human layer for AI-built software."**

People build software with AI tools (Cursor, Claude, Lovable, v0). They hit walls they cannot get past. Relay puts a real human engineer on a call with them within minutes. If the work is too big for a call, it converts into a fixed-price contract where a Relay engineer takes over development.

The customer is typically a **solo founder or small-team builder, semi-technical**. They can describe symptoms but often not causes. They are not living in a terminal. They are spending real money with strangers on the internet, which makes trust the dominant emotional constraint.

---

## 2. The organizing principle: Relay is two products

This is the single most important concept in the redesign. Everything below follows from it. The current panel renders both modes identically, which is the root cause of it feeling incoherent.

| | **Assist mode** | **Delegate mode** |
|---|---|---|
| Who drives | The customer | The engineer |
| Trigger | "I'm stuck" | "Build this for me" |
| How it starts | Call an engineer | Request a quote → contract |
| Engineer staffing | **Pooled**, continuity preferred | **One** engineer owns it |
| Billing | Per minute, on platform | Fixed price, upfront, **off platform** |
| Shape | Episodic — call, fix, leave | Ongoing — days to weeks |
| What the customer needs | **Access** — who is free, call now | **Visibility** — what happened today |
| Dominant emotion | Urgency | Trust |
| Maps to | "Personal" projects | "Contracted" projects |

**Design consequence:** Assist surfaces lead with availability and a call button. Delegate surfaces lead with progress, deliverables and feedback — and must *not* shout "call now," because that is not the relationship.

---

## 3. Problems with the current panel

Recorded so the prototype can be judged against them, and so a before/after comparison can be made.

### 3.1 From the user's own diagnosis

1. **Sidebar is segregated by projects.** An individual only has ~5–10 projects, but many sessions. Projects are the wrong spine.
2. **Engineers are invisible.** In a product whose entire pitch is humans, the engineer appears only as a grey system pill reading "Satyam joined as engineer." No photo, no profile, no relationship.
3. **The UI looks like a gen-AI platform** (Claude/ChatGPT) — a flat list of past conversations in a dark chrome. Relay is not a gen-AI platform and must not read as one. Reference points should be Slack/Discord: DMs with people, presence, a calls section.
4. **First-time users are confused** about what actions are available and how to do things.
5. **There is no status system at all.** After sending a message or requesting a bid, the user must sit on the page and wait. No browser notifications, no email. For bids there is total silence between request and quote.
6. **No email when a quotation is sent.**
7. **No visibility after a contract starts.** Once a bid is accepted the customer cannot see what the engineer is doing day to day, and has no way to give feedback.
8. **Far too much green.** Green should be emphasised through the orb, not smeared across the entire interface.
9. **Profiles and presence are lifeless.** Wants Discord/Slack-style online dots for the customer and status indicators (online / offline / vacation) for engineers.
10. **Voice should be more prominent** — the audience comes from gen-AI tools where voice is familiar.

### 3.2 Additional structural problems identified in review

11. **Green is semantically overloaded.** It simultaneously means brand, online, selected, call, and active — so it means nothing.
12. **Two vocabularies for one concept.** "Ship it / Maintain it" on the quote buttons vs "Go-live / Maintain" on contracts. Pick one taxonomy and use it everywhere. **Decision: use Ship and Maintain throughout.**
13. **Home is a marketing splash, not a dashboard.** A returning user with 17 projects lands on a tagline and a "how Relay works" link instead of anything actionable.
14. **Projects are auto-created and never curated** — the live sidebar contains `Demo_45`, `demo_2`, `hey`, `playpal`, `Playpal`, `PlayIn`, `PlayIn-New`. The primary navigation object is also the messiest one.
15. **Chat mixes system events and human content** as visually identical pills — Zoom started, call started, call ended and actual conversation all look the same.
16. **Duplicate call CTAs** — a green phone icon in the project header and a full-width "Continue session" button in the chat panel, with no clear precedence.
17. **Contracts are one flat list** blending "awaiting bid" with "active and paid," with no sort, no filter, and no summary.
18. **Sessions show only duration and date.** To learn what actually happened you must read an AI-generated prose blob.
19. **"34.76 min paid"** in the user footer is cryptic and reads like a currency typo.
20. **No representation of the time between sessions.** The chat ends with "Session ended" and then nothing — the entire async middle, where anxiety lives, is unmodelled.

---

## 4. Settled decisions

These are **closed**. Do not re-litigate them.

| # | Decision | Notes |
|---|---|---|
| 1 | **Theme is light** | Reverses the current green-on-near-black entirely. Light is also the stronger anti-gen-AI move — dark + green is literally the aesthetic of AI tooling. Dark mode may follow later; the NFP is light only. |
| 2 | **Engineer model: pooled with continuity preferred** for sessions | Whoever is available answers, but the system prefers engineers who already know the project. The customer accumulates a familiar set of 2–4 plus a fallback pool. The UI concept is **"your team"** — not "your engineer," not a marketplace. |
| 3 | **One engineer per contract** | Delegate mode is single-owner. Current copy "Awaiting the team's bid" is misleading and should be rewritten. |
| 4 | **Progress view is feed-first** | Current-focus header above a dated reverse-chronological feed of expandable update cards. |
| 5 | **Kanban is rejected** | The customer is an observer, not a worker. A board reads as inventory and makes people fixate on the size of the "to do" column. A feed reads as momentum. |
| 6 | **Payment is upfront, in full, and off-platform** | Arranged in separate meetings. Relay's panel never processes money. **But payment *status* is still tracked and displayed** — see §8. |
| 7 | **Milestones exist as progress markers only** | Never as payment gates. |
| 8 | **Update cards are auto-drafted from engineer activity**, then edited and confirmed by the engineer | Engineers do push code and open PRs, so cards can cite real commits, PRs and deploys. Pure manual discipline would fail and an empty dashboard is worse than no dashboard. |
| 9 | **The AI project assistant is backstage** | It already exists and stores project context. It is **not** a customer-facing chat participant. It is never shown as a conversational entity. Its only visible role is powering handoff briefings (§7.3) and session summaries. The customer must never be uncertain whether they are talking to a human. |
| 10 | **Prototype data is invented** but plausible | See §13. |
| 11 | **Audience is the internal team** | |
| 12 | **Navigation is a labelled rail** | Not icon-only. An unlabelled icon rail would recreate the exact first-time confusion problem 4 is meant to solve. |
| 13 | **Deliverable format** | Originally planned as static screens then a clickable prototype. Compressed due to timing: build the clickable prototype directly. |

---

## 5. Object model

| Object | Role | Where it surfaces |
|---|---|---|
| **Customer** | The user. Has presence, a minutes balance, settings. | Rail footer |
| **Engineer** | A real person. Photo, bio, tech stack, availability, expertise split by Ship/Maintain, and **shared history with this customer**. | Clickable everywhere their name appears |
| **Your team** | The 2–4 engineers who already know this customer's projects, plus the wider available pool | Home, Chats |
| **Project** | Container. Holds context/knowledge. Typed **Personal** (assist) or **Contracted** (delegate). | Projects, used as a filter elsewhere |
| **Session** | A live call event. Produces **artifacts**, not a prose blob. | Calls, project feed |
| **Chat** | A persistent DM thread **per engineer** — not per session | Chats |
| **Request → Quote → Contract** | The delegate-mode pipeline, with an explicit decision gate | Contracts |
| **Update card** | A daily progress unit under an active contract. Expandable, commentable. | Contract progress |
| **Activity feed** | The chronological spine of a project: sessions, updates, quote events, files | Project page |

**Key structural move:** one **unified activity feed per project**. Sessions, update cards, quote events and file drops all land on a single timeline. "Calls" and "Progress" are then *filters* on that feed rather than separate data stores. Benefit: the project page is never silent, which directly attacks problem 5.

**Project is demoted from spine to lens.** It still exists, but it is no longer the primary navigation axis.

---

## 6. Navigation

A labelled left rail. Flat — the Assist/Delegate distinction is expressed in *content*, not in nested navigation.

```
┌──────────────────┐
│  ◉  RELAY        │   orb + wordmark
├──────────────────┤
│  Home            │   whose turn is it
│  Chats        2  │   DMs per engineer, presence
│  Calls           │   session history + start a call
│  Contracts    1  │   quote pipeline + active work + progress
│  Projects        │   Personal | Contracted
├──────────────────┤
│  Help            │   contextual pills, merged with ⌘K
├──────────────────┤
│  ◉ Rohan Mehta   │   presence dot, minutes, settings
└──────────────────┘
```

Badges show counts that **need the user's attention**, not total counts.

**Rejected:** segregating the sidebar by sessions. Sessions are events; at ~3/week a flat session list reaches 150 items in a year, which recreates the clutter problem rather than solving it. The real fix is replacing *one list* with *modes*.

---

## 7. Screen specifications

### 7.1 Home — "whose turn is it"

The thesis screen. This is what makes the whole redesign legible in a demo. It replaces the marketing hero entirely.

Three bands with **deliberately different visual weight** — the weight difference is itself the information.

```
Good morning, Rohan
Thursday, 25 September

┌─ Needs you ─────────────────────────────── 3 ─┐   ← heaviest, amber edge
│ ▌ Quote ready · Palm Seas                      │
│   Satyam priced the auth rebuild at €3,200     │
│   [ Review quote ]                             │
│ ▌ Deliverable ready to approve · daun          │
│   Webhook retry handling                       │
│   [ Review ] [ Request changes ]               │
│ ▌ Priya asked you a question · Epicmail        │
│   "Which domain should the SPF record use?"    │
│   [ Reply ]                                    │
└────────────────────────────────────────────────┘

┌─ Moving ──────────────────────────────────────┐   ← medium, blue edge
│ ▌ daun · Ship            ●●●○○  60%           │
│   Satyam is on: Stripe webhook retries         │
│   Next deliverable Fri 2 Oct                   │
│ ▌ daun · Maintain        ●●●●○  healthy        │
│   Priya · routine monitoring                   │
└────────────────────────────────────────────────┘

┌─ Free right now ──────────────────────────────┐   ← lightest, green, faces
│ ◉ Satyam   replies in ~15 min   [Call] [Chat] │
│ ◉ Priya    replies in ~8 min    [Call] [Chat] │
│ ◐ Meera    in a session until 3pm              │
│ ○ Arjun    away until Friday                   │
└────────────────────────────────────────────────┘
```

Rules:
- "Needs you" is always first and always heaviest. If empty, show a genuine empty state that invites action, not a blank card.
- Each row carries a **3px coloured left edge-marker** encoding its state. This replaces identical rounded cards with identical shadows.
- Every actionable row has its action inline. Do not make the user navigate to find the verb.

### 7.2 Chats

Slack/Discord-shaped, but **not Slack's density** — with only three conversations an airy layout looks abandoned. Tighter and more information-dense than Slack.

- **Left column:** DM list, one row per engineer. Avatar with availability ring, name, last message preview, unread count, and **"knows Palm Seas, daun"** as the continuity signal.
- **Centre:** the thread. System events (call started, session ended) are **visually demoted** to thin centred rules — never styled the same as human messages. This fixes problem 15.
- **Composer:** voice-forward. Order of prominence: **call a human** (primary) > **voice note** (secondary) > text. Label the two voice affordances unambiguously — the current mic vs waveform ambiguity must not survive.
- **Right:** collapsible engineer profile panel (§7.3).

### 7.3 Engineer profile

The human-layer payoff. Opens as a slide-over drawer from anywhere the engineer's name appears.

Contents, in priority order:
1. **Photo**, name, availability state, and **"typically replies in ~15 min"**
2. **Shared history with this customer** — *"12 sessions with you · shipped your Payments contract · knows daun and Palm Seas."* This is the highest-value field and the one that creates switching cost. No AI tool can show it.
3. **Tech stack** as tags
4. **Experience split by Ship vs Maintain** — track record segmented by engagement type, which is what makes a bid credible
5. **One-line bio** in the engineer's own voice
6. **A small human touch** — one hobby line, at the bottom, understated

Keep competence above personality. This profile is attached to a €4,500 decision; it must not read like a dating profile. **Design the degraded state** — some engineers will never fill these fields in.

**Handoff briefing.** Because staffing is pooled, the customer's instinctive fear is "do I have to explain everything again?" The AI assistant solves this in the data layer; the UI must make it *visible*:

```
◉ Priya joined this session

  Before joining, Priya reviewed
    ✓ Project brief and stack — Next.js, Stripe
    ✓ Satyam's notes from your last 3 sessions
    ✓ The open issue — webhook retries
```

### 7.4 Contracts — the pipeline

Replaces the flat list. Sections: **Needs your decision**, **Active**, **Completed**.

The pipeline, with the decision gate explicit and off-platform steps marked honestly:

```
Requested → Under review → Quote ready → ⟨ YOUR DECISION ⟩
                                                │
                            ┌───────────────────┘
                            ▼
                  Kickoff call · Thu 2pm        ↗ off-platform
                            ▼
                  Payment confirmed · 24 Sep    ↗ off-platform
                            ▼
                  In progress → Delivered
```

**Every state must carry three facts** or it fails at its job:
1. **Whose turn it is** — you, or Relay
2. **What happens next**
3. **By when** — even approximate: "quotes are usually ready within 4 hours"

A progress bar without timing is just prettier silence.

**Unhappy paths are required**, not optional. Real pipelines are not linear, and a UI that only renders the happy path breaks trust exactly when reality diverges:
- `Declined`
- `Revision requested`
- `Needs more info`
- `Expired`

**Why off-platform steps are still tracked:** the customer pays 100% before any work exists, so the moment of peak anxiety is immediately after paying — maximum money out, zero output in. If the platform shows nothing, the single largest event in the relationship is invisible. You do not need to process payments to show payment status; status is just a flag someone flips. The confirmed-payment stamp is also the only receipt the customer gets, since there is no invoice in the product.

**The engineer's profile belongs inside the quote.** Accepting a quote is accepting a *person* to take control of your product. Showing a price without a face withholds the information that actually drives the decision.

### 7.5 Contract progress — feed-first

```
┌────────────────────────────────────────────────┐
│  daun · Ship                                   │
│  Payments milestone      ●●●○○  60%            │
│  Satyam is on: Stripe webhook retries          │
│  Next deliverable: Fri 2 Oct                   │
├────────────────────────────────────────────────┤
│  Today                                         │
│  ▸ Fixed duplicate charge on retry        ✓    │
│  ▸ Webhook signature validation           ⟳    │
│  Yesterday                                     │
│  ▸ Test mode keys configured              ✓    │
│  ▸ Reviewed your Figma flow               ✓    │
└────────────────────────────────────────────────┘
```

- **Update card** expands in place to show: full description, deliverables, linked commits/PRs/deploys, and the engineer who posted it.
- **Cards are commentable and approvable.** Deliverables get **Approve** / **Request changes**. This is the "reciprocated" note in the wireframes, and it is what turns a status feed into genuine involvement.
- Milestone track is progress only. No money.

### 7.6 Projects

Split into **Personal** and **Contracted** — the Assist/Delegate distinction made concrete.

- **Personal** = the customer is building it, Relay assists.
- **Contracted** = Relay is building it for the customer.

Each project page shows the **unified activity feed** (§5) plus project context — stack, repo, environments — which is the asset that makes pooled staffing survivable.

### 7.7 Help — contextual, merged with search

A persistent affordance (bottom-right, plus ⌘K). Opens to **contextual quick pills**, not a static FAQ. What is offered depends on current state — if a quote is sitting unaccepted, the top pill is about that.

Example pills:
- "I don't know if I need a call or a contract"
- "What's happening with my quote?"
- "I need to change something in an active contract"
- "How does billing work?"
- "Something else — message an available engineer"

Rules:
- **Merge Help and search into one ⌘K surface.** Two separate "find/do things" mechanisms is a tax on exactly the confused user you are trying to help. One surface answers both "take me to X" and "help me with Y."
- The fallback to a human must state a **response time** and have an honest "nobody is free right now, here's when" state.
- Be clear-eyed: Help is a **safety net, not a cure**. The real fix for first-time confusion is that every screen has one obvious primary action. Help catches the people you still failed.

---

## 8. Status and notifications

The largest single problem in the current product. Define the matrix once rather than deciding event by event, or users will mute Relay.

| Event | In-app | Browser push | Email |
|---|---|---|---|
| Quote ready / any money decision | ✓ | ✓ | ✓ immediately |
| Engineer replied to you | ✓ | ✓ | only if unread 10+ min |
| Daily progress card posted | ✓ | — | daily digest, opt-in |
| Session scheduled or starting | ✓ | ✓ | ✓ + calendar invite |
| Deliverable ready to approve | ✓ | ✓ | ✓ immediately |
| Contract state change | ✓ | ✓ | ✓ |

**Rule of thumb: money and decisions interrupt; progress accumulates.**

Requirements:
- Browser notifications so the user can close the tab — the current product assumes they will sit and wait, which is the core complaint.
- Every email deep-links to the exact state, never to the homepage.
- The user needs notification preferences.

---

## 9. Presence and availability

**Presence is a promise.** Raw online/offline will backfire: showing an engineer as "online" who is heads-down in someone else's code for 40 minutes does more damage than showing nothing.

Model **availability**, not presence:

| State | Meaning | Colour |
|---|---|---|
| `Available now` | Will pick up a call | Green, filled ring |
| `In a session` | Busy with another customer, ETA shown | Amber, half ring |
| `Heads-down until 4pm` | Working, not interruptible | Grey, dashed ring |
| `Away until Friday` | Out | Grey, hollow ring |
| `Offline` | — | Grey, no ring |

Always pair with the factual **"typically replies in ~15 min."** The customer gets an online dot too, Discord-style.

---

## 10. Visual foundation

Full visual reset. Light theme.

### 10.1 Colour

Green stops being a general accent and gets **exactly one job: live human presence.** Rare, therefore meaningful. The orb carries the brand at full intensity — it becomes the only place that colour lives unrestrained.

| Role | Hex | Tint | Use |
|---|---|---|---|
| Paper | `#F7F8F8` | — | App background. Cool neutral, **not cream** |
| Surface | `#FFFFFF` | — | Cards, panels |
| Line | `#E3E7E8` | — | Hairline borders |
| Ink | `#14181A` | — | Primary text |
| Muted | `#697077` | — | Secondary text |
| Live / human | `#00875A` | `#DCF5EA` | Online, human present — **rare** |
| Your turn | `#B45309` | `#FDF0D5` | Waiting on the customer — the most important state in the app |
| In progress | `#2456C8` | `#DEE8FD` | Engineer is working |
| Contract | `#6D3BD4` | `#EBE3FC` | Delegate mode, money |
| Blocked | `#C0322B` | `#FBE2E0` | Failed, declined, stalled |

Rules:
- On light, status reads as **tinted pills** — more legible than dots and far easier to pass contrast than green-on-black ever was.
- **Always pair colour with an icon or shape.** Never colour alone — colourblind users, and green/red as sole differentiator is the classic failure.
- Do not use pure white as the app background; it reads clinical.

### 10.2 Type

Two families, clearly distinct:
- **Display / headings:** `Bricolage Grotesque` — characterful, slightly irregular proportions that read as crafted rather than corporate.
- **UI / body:** `Public Sans` — clean, slightly warmer than Inter, and not the default everyone reaches for.

Set a real type scale. The current panel's generic UI sans is a large part of why it feels anonymous.

### 10.3 Density and structure

- Tighter and more information-dense than Slack. Borrow Slack's **spine**, not its emptiness.
- Light UIs need hairline borders and soft shadows for elevation, where dark UIs use lightness.
- **Structural device:** a 3px coloured left edge-marker on rows encodes state. This is deliberately chosen over identical rounded cards with identical shadows.

### 10.4 Anti-patterns — do not produce these

These read as machine-generated and will undermine a pitch:
- Cream background (~`#F4F1EA`) + high-contrast serif display + terracotta accent (~`#D97757`)
- Near-black background with a single acid-green accent — **this is close to the current Relay look and is exactly what we are moving away from**
- Tracked-out ALL-CAPS eyebrow labels above every heading
- Meta strings joined with middle dots
- Identical border-radius and identical soft grey shadow on everything regardless of hierarchy
- `→` appended to button and link text
- Accenting a single word of a headline in a different colour
- Numbered markers (01 / 02 / 03) on content that is not actually a sequence
- Fade-and-slide-up entrance animations on every section, hover transitions on every card

Motion should be reserved for **responses to user action** — opening, expanding, confirming — where it shows what changed.

### 10.5 Quality floor

Responsive down to mobile, visible keyboard focus states, `prefers-reduced-motion` respected, accessible contrast throughout.

---

## 11. Copy guidelines

- **One taxonomy: Ship and Maintain.** Never "Go-live," never "Ship it / Maintain it" as a separate vocabulary.
- Sentence case everywhere. No ALL-CAPS labels.
- Active voice. A button says what happens: "Review quote," not "Submit."
- An action keeps its name through the whole flow — the button that says "Approve" produces "Approved."
- Name things as users understand them, not as the system is built.
- Empty states are invitations to act, not decoration. Errors say what went wrong and how to fix it, without apologising or being vague.
- **Fix "34.76 min paid."** It reads like a currency typo. Use something like "34.8 minutes used this month."
- **Fix "Awaiting the team's bid."** Contracts are single-owner. Use "Satyam is preparing your quote" or "Being reviewed."

---

## 12. High-value additions

Three things that were not in the original brief but should be built:

1. **"Waiting on you" as the organizing principle of Home** — §7.1. Solves activation and status anxiety in one move.
2. **Sessions produce artifacts, not prose.** A session currently outputs an AI summary paragraph. It should output referenceable items: what was fixed, files touched, recording/transcript, and next steps as discrete objects.
3. **The session → quote → contract path must be one continuous thread.** Today these are three disconnected areas. *"Satyam couldn't finish this in 20 minutes → get a quote for the rest"* should be a button **inside the session summary**, not a trip to a separate Request-a-Quote form. This is probably the highest-revenue UI change on the table.

---

## 13. Invented data — use verbatim

**Customer:** Rohan Mehta. 34.8 minutes used this month. Online.

**Engineers**

| Name | Focus | Stack | Availability | Replies in | Shared history |
|---|---|---|---|---|---|
| Satyam Jha | Ship | Next.js, Stripe, Postgres | Available now | ~15 min | 12 sessions with you · shipped your Payments contract · knows daun, Palm Seas |
| Priya Nair | Maintain | Python, AWS, Postgres | Available now | ~8 min | 4 sessions with you · maintains Epicmail |
| Meera Iyer | Ship | React, TypeScript | In a session until 3pm | ~20 min | 2 sessions with you |
| Arjun Desai | Ship | React Native, Expo | Away until Friday | ~1 hr | 1 session with you |
| Kabir Shah | Maintain | Go, Kubernetes | Offline | ~30 min | No history yet |

Bios (one line, engineer's own voice):
- Satyam — "Payments and checkout flows, mostly. I like the boring parts that have to not break."
- Priya — "I keep things running. Most of my work is invisible, which is the point."
- Meera — "Front-end. I care more about the empty states than anyone should."

Hobby lines (understated, bottom of profile):
- Satyam — "Makes filter coffee, badly."
- Priya — "Long-distance runner. Slowly."

**Projects**

| Project | Type | State |
|---|---|---|
| Palm Seas | Personal | Quote ready — €3,200, auth rebuild, from Satyam |
| daun | Contracted · Ship | Active, €4,500, 60%, Satyam |
| daun | Contracted · Maintain | Active, €2,500, healthy, Priya |
| Epicmail | Personal | Open question from Priya |
| TrackFit | Personal | Dormant |
| YopBox | Personal | Dormant |

**Home "Needs you" items**
1. Quote ready · Palm Seas — "Satyam priced the auth rebuild at €3,200" → Review quote
2. Deliverable ready to approve · daun — "Webhook retry handling" → Review / Request changes
3. Priya asked you a question · Epicmail — "Which domain should the SPF record use?" → Reply

**daun progress feed**
- Today — "Fixed duplicate charge on retry" ✓ · "Webhook signature validation" in progress
- Yesterday — "Test mode keys configured" ✓ · "Reviewed your Figma flow" ✓
- Milestone: Payments, 60%. Next deliverable Fri 2 Oct.

**Palm Seas quote detail:** €3,200 · Ship · rebuild auth with proper session handling · 2 weeks · prepared by Satyam Jha · kickoff call proposed Thu 2pm.

---

## 14. Build order

If time is constrained, build in this order — the first four carry the entire argument:

1. **Home** — the thesis screen
2. **Contracts pipeline** — solves the biggest complaint
3. **Contract progress feed** — solves the second biggest
4. **Chats + engineer profile drawer** — delivers the "human layer" payoff
5. Calls
6. Projects
7. Help / ⌘K overlay

A **before/after pair of the Home screen** is worth building if time allows — it is what actually lands with a team.

---

## 15. Open questions

Not blocking the prototype, but unresolved:

1. Does a session need to belong to a project, or can it exist standalone?
2. Does a project map to a repo, a deployed app, or neither?
3. Is there onboarding for first-time users today, or do they land cold on the hero screen?
4. What is the engineer-side panel, and how much of this model does it need to mirror?
5. Should dark mode follow, given the current product is dark and existing users are accustomed to it?
