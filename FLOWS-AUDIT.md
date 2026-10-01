# Relay Customer Panel — Flow & Action Audit

**Status:** draft for review. Nothing here is settled.
**Source:** `relay-prototype.html` (7,989 lines), read in full — markup, both script blocks, every handler.
**Purpose:** before development starts, fix the intended outcome of every control, so the build has one answer per button instead of an argument per button.

---

## How to read this

Every control gets an entry:

> **ID. Label** — where it lives
> **Today:** what the prototype actually does right now.
> **Intended:** what I assume it should do in the real product.
> **?** an open question only you can answer.

**Today ≠ Intended on purpose.** The prototype fakes a lot. The gap between the two lines is the work.

To review: reply with item numbers — *"3.4 wrong, should be X"*, *"delete 9.7"*, *"add: ..."*. I will fold your edits in and reissue this as the final spec.

Sections:
1. Object model & vocabulary · 2. Global chrome · 3. Home · 4. Live call · 5. Post-call filing · 6. Sessions · 7. Session detail · 8. Projects · 9. Project detail · 10. Chats · 11. Contracts · 12. Progress (Ship) · 13. Upkeep (Maintain) · 14. Notifications · 15. Profile & settings · 16. Engineer drawer · 17. Help · 18. Cross-cutting rules · 19. Demo scaffolding to delete · 20. Flows with no UI yet · 21. Bugs & inconsistencies found · 22. Decisions needed from you

---

## 1. Object model & vocabulary

Flows below assume these objects. If an assumption here is wrong, a lot downstream is wrong, so check this section first.

| Object | Definition in the prototype | Assumption to confirm |
|---|---|---|
| **Customer** | One person. Has presence, minutes used, ground rules, connectors. | Single user per account — no teams, no seats, no inviting a colleague. |
| **Engineer** | A real person with availability (`live` / `busy` / `off`), stack tags, shared history. | Pooled with continuity: whoever is free answers, preferring whoever knows the work. |
| **Project** | A container. Has name, stack, AI-written summary, sessions. Created by the customer or offered after a call. | Optional. Sessions can exist without one. A project is a *lens*, not the spine. |
| **Session** | One thread of work. Holds **one or more calls** plus free text messages between them. Has `state: open \| done`. | The spine. "Continue the session" is the core returning action. |
| **Call** | One live conversation inside a session. Billed per minute. Produces a transcript + "what came out of it" artifacts. | Metered. The meter starts on pickup, not on dial. |
| **Chat thread** | A persistent DM per engineer, plus one per contract. Separate from sessions. | Free. Never billed. |
| **Contract** | Delegate-mode work owned by one engineer. Has a pipeline state. Paid off-platform. | The panel tracks status only; it never takes money. |
| **Update card** | A unit of daily progress under an active contract. Approvable, commentable. | Written by the engineer, auto-drafted from their activity. |
| **Notification** | An item needing the customer's attention. | Mirrors to browser push and email per §18.6. |

**Taxonomy:** Ship and Maintain, everywhere. Never "Go-live", never "Ship it".

**Open structural questions:**
- **1.1** Can a session move between projects after filing, or only from unfiled → filed? (Today: only unfiled → filed.)
- **1.2** Can a session be reassigned to a different engineer mid-session? Today a session has exactly one `who` for its whole life, which contradicts "pooled staffing".
- **1.3** Does a contract belong to a project? Today they are parallel universes — `daun` is a contract name and not in the projects list.

---

## 2. Global chrome

### 2.1 Left rail

- **2.1.1 Relay orb + wordmark** — rail top
  **Today:** decorative, not clickable.
  **Intended:** clicking goes Home. Low stakes, high convention.
- **2.1.2 Home** — rail
  **Today:** shows the Home screen; scrolls main to top; closes the Help panel.
  **Intended:** same. Home is the ask box, always.
- **2.1.3 Sessions** — rail
  **Today:** shows the Sessions feed.
  **Intended:** same. During a live call this item is marked `in-call`; see 4.11.
- **2.1.4 Projects** — rail
  **Today:** shows the Projects list.
  **Intended:** same.
- **2.1.5 Chats** — rail, badge `2`
  **Today:** shows Chats. Badge is a hardcoded `2`, hidden on the first-run view.
  **Intended:** badge = number of threads with unread messages *from an engineer*. Zero hides the badge.
  **?** Unread threads, or unread messages? (I assume threads — it matches Slack and does not inflate.)
- **2.1.6 Notifications** — rail, badge `3`
  **Today:** shows the Notifications screen. Badge is live — counts unread cards, hides at zero.
  **Intended:** same. This badge is the single source of "something needs you".
- **2.1.7 Contracts** — rail, badge `1`
  **Today:** shows Contracts. Badge hardcoded `1`.
  **Intended:** badge = contracts in a state where it is **your turn** (quote ready, deliverable awaiting approval, decision owed). Not total contracts.
- **2.1.8 Badges generally**
  **Intended:** badges count *things needing you*, never inventory. A badge the user cannot clear by acting is a bug.
- **2.1.9 Rail footer — "Rohan Mehta / 34.8 minutes used"**
  **Today:** opens the Profile screen. Sub-line swaps to "No calls yet" on the first-run view. Avatar carries the presence dot.
  **Intended:** opens Profile. The minutes line is the running meter for the current billing period and should link to billing once billing exists (§20.3).
- **2.1.10 Presence dot on the customer avatar**
  **Today:** mirrors the status chosen on the Profile screen (15.3).
  **Intended:** same. Visible to engineers.

### 2.2 Screen-level behaviour

- **2.2.1 Navigating anywhere** — any rail item or in-page link
  **Today:** swaps the visible `.screen`, lights the rail item (detail screens light their parent), scrolls to top, closes the Help panel. If a call is live, the call minimises to a pill (4.11).
  **Intended:** same, plus: back/forward should work. Today there is no URL routing at all — every screen is the same URL.
  **?** Do we want real routes (`/sessions/s-checkout`)? I assume yes — emails must deep-link to exact states, which is impossible without routes.
- **2.2.2 Escape key** — global
  **Today:** closes the engineer drawer, the Help panel, the project `···` menu, the scope pickers, the welcome card, and the modal (unless the modal is locked).
  **Intended:** same. Escape never ends a live call — that needs the confirm modal (4.10).

---

## 3. Home

Home is one card: a box you type into, a green call button, and a send button. Two demo views exist (first-time / returning); in production there is one Home whose contents differ by whether the customer has history.

### 3.1 First-run welcome card

- **3.1.1 Card appears** — on first load of the first-run view
  **Today:** opens 260ms after load, over a scrim, with staggered contents. Shown once per page load.
  **Intended:** shown once per account, on first login ever. Never again.
- **3.1.2 Photo drop zone**
  **Today:** toast — "Photo upload is not wired up in the prototype".
  **Intended:** opens a real file picker, crops to square, saves to profile. Optional — skippable without consequence.
- **3.1.3 "Your name" field**
  **Today:** pre-filled "Rohan Mehta". On Continue, the first word replaces the name in the greeting.
  **Intended:** pre-filled from signup. Editing it updates the account name everywhere.
- **3.1.4 "What do you like making?" chips** (5)
  **Today:** single-select; clicking the selected one deselects it. Answer is discarded.
  **Intended:** stored on the profile; used to bias which engineer picks up the first call, and visible to engineers in the handoff briefing.
  **?** Is this actually used for routing, or is it only colour? If it is only colour, I would cut it — it is two questions standing between a stuck person and help.
- **3.1.5 "What do you like doing most?" free text**
  **Today:** typed, discarded.
  **Intended:** stored on the profile bio. Blank is a fine answer.
- **3.1.6 Continue**
  **Today:** applies the name, closes the card, reveals the page with a staggered entrance, toasts "All set".
  **Intended:** same, minus the toast — the page arriving is the confirmation.
- **3.1.7 Skip / ✕ / scrim click / Escape**
  **Today:** all four close the card with nothing saved.
  **Intended:** same. Everything on this card is optional and must stay optional.

### 3.2 The coach bubble (first-run only)

- **3.2.1 Tour runs**
  **Today:** two stops — "Describe your problem here" (points at the textarea), then "Then click here to connect with an engineer" (points at the green button). 3.4s apart. Hovering pauses it. Retires permanently after the last stop, and also the moment the user types or a call starts.
  **Intended:** same. It is a one-time introduction and must never reappear for a returning customer.
- **3.2.2 The hint row under the box** — three live faces + "Engineers available" + "Click ☎ on the chat screen to connect to them"
  **Today:** appears after the coach retires (first-run) or immediately (returning). Faces are the first three engineers with `live` status. Hovering shows "Click to open profile". Clicking a face opens the engineer drawer. The green call button gets a lit collar while the hint is up. Disappears at the first keystroke.
  **Intended:** same, with real availability. **The copy is wrong** — it says "on the chat screen", but the button it draws is the one on *this* screen. Fix the sentence.

### 3.3 The ask box

- **3.3.1 Textarea** — "Ask anything here"
  **Today:** auto-grows. Ghost-types four example problems behind the caret while empty and untouched; stops permanently at the first keystroke, pointer-down or focus. Resumes if the box is left empty.
  **Intended:** same. The ghost is a demonstration of register — plain sentences, no jargon — and should survive to production.
- **3.3.2 Three starter chips** — "My site stopped working" etc.
  **Today:** inserts the phrase plus " — " into the box, focuses it, puts the caret at the end, kills the ghost.
  **Intended:** same.
  **?** Should the starters be fixed, or drawn from the customer's own history after the first few sessions?
- **3.3.3 "+" attach button**
  **Today:** stages a rotating fake file chip (PNG/LOG) above the tool row.
  **Intended:** opens a real file picker; also accepts drag-drop onto the card and paste of a screenshot from the clipboard. Screenshot-paste is the single most important one for this audience — it is how they will describe a bug.
  **?** Limits: file size cap, allowed types, how many per ask?
- **3.3.4 Staged file chip ✕**
  **Today:** removes the chip; removes the bar when the last chip goes.
  **Intended:** same, plus cancels the upload if it is in flight.
- **3.3.5 "Project" scope chip**
  **Today:** hidden until the customer has had at least one call. Opens a menu of all projects with a session count each; picking one labels the chip; picking "Not under a project" clears it. Choosing a project narrows the Session menu to that project's sessions and clears an incompatible session choice.
  **Intended:** same. This is how an ask gets filed before it exists.
- **3.3.6 "Session" scope chip**
  **Today:** hidden until the first call. Menu lists "Start a new session" plus eligible sessions (the chosen project's, or all unfiled ones), grouped This week / Earlier, each row showing open/finished, project, engineer, how long ago. Picking a session also sets the project.
  **Intended:** same. Picking an existing session routes the call to the engineer who owns it (continuity), which is the whole point.
- **3.3.7 Mic button** — "Say it out loud"
  **Today:** toggles a class and toasts "Listening — say what is wrong" / "Stopped listening". Nothing is captured.
  **Intended:** real speech-to-text into the textarea. Live partial transcription so the user sees it working. Stop on a second click or 2s of silence.
  **?** Is voice-to-text in scope for v1, or does the mic just become a voice note attached to the ask?
- **3.3.8 Green call button** — "Find me an engineer"
  **Today:** the primary action. Works with an **empty box** — text is optional. Picks the engineer: the chosen session's owner → else the chosen project's lead → else anyone free. Clears the box and the scope chips, then opens the live call (§4).
  **Intended:** same, but with the real matching rules spelled out in §4.1. The empty-box case matters: a panicking user should be able to press the phone and talk.
- **3.3.9 Send button (arrow)** — "Send it as a message instead"
  **Today:** requires text; otherwise focuses the box and toasts. Creates a **new chat thread** with the demo engineer, posts the text plus a canned instant reply, adds a row to the Chats list, shows a "Filed under X" marker if a scope was set, clears the box, navigates to Chats, toasts.
  **Intended:** same shape, but: (a) it should route to the *same* engineer the call button would have picked, not always the demo one; (b) the reply is a real human reply, so the thread shows "Sent · usually replies in ~15 min" and nothing else until they answer; (c) a canned auto-reply must not look like a human reply.
  **?** Should sending a message create a session, or only a thread? Today it creates a thread only, which means a message-first problem has no session until a call happens. I think that is right, but it needs confirming.

### 3.4 Home, returning view

- **3.4.1 "Recent sessions · See all N"**
  **Today:** `See all` → Sessions screen. N is kept honest as sessions are created.
  **Intended:** same.
- **3.4.2 The one session strip**
  **Today:** a single row — the last session — opening that session. Deliberately one, not a list.
  **Intended:** same: the most recent **open** session. If there is none, hide the panel rather than showing a finished one.
- **3.4.3 "Continue the session" chip inside the strip**
  **Today:** opens the session in continue mode — scrolls to "you left off here", focuses the composer.
  **Intended:** same.
- **3.4.4 Recent panel on the first-run view**
  **Today:** deliberately always empty, even after a call happens in that page load.
  **Intended:** in production this distinction disappears. A customer with one session sees it; a customer with none sees nothing.

---

## 4. The live call

This is the largest surface and the one with the most invented behaviour. It is a full-screen overlay, not a route.

### 4.1 Starting a call

- **4.1.1 Every "Start a call" button, everywhere**
  **Today:** a single global capture-phase listener intercepts **any** button whose text is exactly "Start a call", works out the context, and opens the call overlay. Contexts: a project's call chip → the project's lead engineer; a session composer → that session's engineer, joining that session; the engineer drawer → that engineer; a chat thread → that thread's person; the project sheet / new-session sheet → lead or anyone free; fallback → anyone free.
  **Intended:** same logic, expressed as explicit routing rather than text matching (see 21.1). The rule in words: **the engineer who already knows this work, if they are free; otherwise the next engineer who knows the project; otherwise anyone free who works in the stack.**
- **4.1.2 Nobody is free**
  **Today:** not modelled. There is always someone.
  **Intended:** required. A card that says who is next free and when, offers to leave a message instead, and offers a callback when someone frees up.
- **4.1.3 Connecting state**
  **Today:** "Connecting you to X · Getting your camera and microphone ready" for a fixed 1.5s, with a Cancel button.
  **Intended:** real connection, real device permission prompts, with an honest failure state (no mic, permission denied, no engineer picked up in 60s).
- **4.1.4 Cancel while connecting**
  **Today:** closes everything, discards the filing context, nothing is billed.
  **Intended:** same. **Nothing is billed before pickup** — this must be stated on screen, as it is today ("The meter starts when they pick up").
- **4.1.5 Engineer joins**
  **Today:** toast "X joined" + an opening chat message "Hi Rohan, I am here. What are we looking at today?" marked unread.
  **Intended:** same. The greeting must be from the real engineer, not auto-generated — a fake human line is the one thing that destroys the premise.
- **4.1.6 Handoff briefing** (specified in the brief, **absent from the prototype**)
  **Intended:** when the engineer joins, show what they read before joining — project brief and stack, previous engineers' notes, the open issue. This is the answer to "do I have to explain everything again?" and it is currently not built anywhere.

### 4.2 The stage

- **4.2.1 Participant tiles**
  **Today:** 2 or 3 tiles (customer, engineer, and a supervisor who auto-joins at 7s). Camera-on shows a coloured silhouette; camera-off shows the avatar. A random tile is highlighted as "speaking" every 2.6s.
  **Intended:** real video, real speaking detection.
- **4.2.2 Supervisor auto-join**
  **Today:** a second engineer joins at 7s as "Supervisor, listening in", with an eye badge and a toast.
  **Intended:** **needs a product decision.** Who is this, when do they join, and does the customer have to consent? A silent third party on a paid call is a trust problem if it is not explained. See 22.4.
- **4.2.3 Pin button on a tile** (and in the hover card)
  **Today:** pins that tile to the main stage; clicking again unpins. Pinning the screen share works too.
  **Intended:** same.
- **4.2.4 Picture-in-picture tile**
  **Today:** draggable within the stage, clamped to bounds.
  **Intended:** same, plus position remembered for the session.
- **4.2.5 Hovering a participant's name**
  **Today:** a profile popover — photo, status, bio, stack tags, shared history, "View full profile".
  **Intended:** same.
- **4.2.6 "View full profile" in the popover**
  **Today:** opens the engineer drawer over the call.
  **Intended:** same.

### 4.3 Screen sharing

- **4.3.1 Engineer shares automatically at 16s**
  **Today:** fakes a code editor with the customer's checkout route, a highlighted line, a cursor with the engineer's name, and function logs showing a 504 then a 200.
  **Intended:** real share from the engineer side. No auto-trigger.
- **4.3.2 Customer "Share screen" button / `S` key**
  **Today:** toggles a fake browser view of the customer's own checkout page with a timeout error. If both are sharing, a banner appears.
  **Intended:** real `getDisplayMedia`. Needs: a picker, a clear "you are sharing" indicator that survives minimising, and a one-click stop.
  **?** Can the engineer *request* a share? On these calls the engineer almost always needs to see the screen, so an invite-to-share is probably worth building.
- **4.3.3 "Stop sharing"** — in the share header and the banner
  **Today:** stops; unpins the screen if it was pinned.
  **Intended:** same.

### 4.4 Call controls

- **4.4.1 Mic toggle / `M`** — **Today:** toggles icon state only. **Intended:** real mute, with a "you are muted" nudge if the user talks while muted.
- **4.4.2 Camera toggle / `V`** — **Today:** toggles between silhouette and avatar. **Intended:** real camera. Default state is a decision: see 22.5.
- **4.4.3 Share toggle / `S`** — see 4.3.2.
- **4.4.4 Chat panel / `C`** — **Today:** opens the side drawer, clears the unread dot. **Intended:** same.
- **4.4.5 Engineer panel / `I`** — **Today:** opens a drawer with the engineer's card and "Left open from your last calls". **Intended:** same — this is the continuity payoff and should stay.
- **4.4.6 Panel close ✕ / segmented Chat|Engineer switch** — **Today:** switches or closes. **Intended:** same.
- **4.4.7 "Leave" in the control bar and "End session" in the header** — both open the confirm modal (4.10).

### 4.5 In-call chat

- **4.5.1 Message input + send**
  **Today:** appends the message to the in-call chat. No reply is simulated. Labelled "Chat time is free".
  **Intended:** real two-way chat. It must be obvious this is the same thread the engineer sees.
  **?** Does in-call chat merge into the session thread afterwards, or stay inside the call record? I assume it merges — otherwise links and snippets pasted on the call are lost.
- **4.5.2 Unread dot on the chat button** — **Today:** set when the engineer's opening message lands, cleared on open. **Intended:** same.

### 4.6 Summary tab

- **4.6.1 "Summary" tab** — header tabs Call | Summary
  **Today:** switches the stage for a notes view: "So far this session" (a listening placeholder), "Left open from your last calls", a sessions timeline with the live timer, the engineer card, and a Files card.
  **Intended:** live AI-written notes accumulating during the call, so the customer can see what is being captured and correct it. This is the "nothing you need to write down" promise, and right now it is a placeholder.
- **4.6.2 "Add file" in the Files card** — **Today:** inert (`data-act="noop"`). **Intended:** uploads a file into the session, visible to both sides immediately.
- **4.6.3 "Back to call" button** — **Today:** returns to the stage. **Intended:** same.

### 4.7 Transcription indicator

- **4.7.1 "Transcribing" + connection quality**
  **Today:** decorative.
  **Intended:** real. And it raises consent: see 22.6.

### 4.8 Timer and metering

- **4.8.1 Timer**
  **Today:** counts from pickup, `mm:ss`, shown in the header, the mini pill and the summary tab.
  **Intended:** same. The timer is the invoice; it must be visible at all times, including while minimised.
- **4.8.2 Billing on end**
  **Today:** `max(1, round(secs/60))` — a 20-second call bills 1 minute, a 90-second call bills 2.
  **Intended:** needs a stated rule. See 22.3.

### 4.9 Minimising

- **4.9.1 Navigating while on a call**
  **Today:** clicking any rail item minimises the call to a bottom pill showing the engineer, the running timer and "Return to call". The call keeps running. The Sessions rail item is marked in-call.
  **Intended:** same. This is good and should survive.
- **4.9.2 "Return to call" pill** — **Today:** restores the full call. **Intended:** same.

### 4.10 Ending

- **4.10.1 "End session" / "Leave"** — opens a confirm modal: *"The clock stops now and your summary starts building. You can keep chatting afterwards."*
  **Intended:** same. Confirming the end of a metered call is correct.
- **4.10.2 "Keep going"** — **Today:** dismisses the modal. **Intended:** same.
- **4.10.3 "End session"** — **Today:** stops the timer, shows the ended screen. **Intended:** same, and the engineer is notified.
- **4.10.4 Ended screen** — "Session ended · mm:ss with X. Your summary is being prepared."
  **Today:** two buttons, Rejoin session and Back to Relay.
  **Intended:** same. **The copy says the summary "will show up under Calls"** — there is no Calls screen; it is Sessions. Fix.
- **4.10.5 "Rejoin session"** — **Today:** reconnects, resets the timer to 0. **Intended:** reconnects and **continues** the same call's billing, or starts a clearly-labelled second call. Resetting the meter silently is wrong either way. See 22.3.
- **4.10.6 "Back to Relay"** — **Today:** closes the overlay and runs the filing flow (§5) with the elapsed seconds.
  **Intended:** same.
- **4.10.7 Engineer ends the call / drops**
  **Today:** not modelled.
  **Intended:** required. Customer sees "X ended the session" or "Connection lost — reconnecting", with a clear billing consequence for a drop.

### 4.11 After the call, what gets created

- **4.11.1 Call aimed at an existing session** — **Today:** appends the call to that session, re-dates it, floats it to the top of the feed, rewrites the session summary from *all* calls, and opens the session. **Intended:** same.
- **4.11.2 Call aimed at a project** — **Today:** creates a new session filed under the project, opens the project. **Intended:** same.
- **4.11.3 Call started as a one-off** — **Today:** creates an unfiled session and opens it. **Intended:** same.
- **4.11.4 Call from the home box with no scope** — **Today:** runs the "keep this somewhere?" offer (§5). **Intended:** same.
- **4.11.5 Session title** — **Today:** the first thing the customer said in the in-call chat, else the text typed in the ask box, else "Session with X". **Intended:** AI-named from the call content, editable by the customer.
- **4.11.6 Call under 1 minute** — **Today:** nothing is filed at all if `secs < 1`. **Intended:** confirm — a 40-second call that solved something should probably still produce a record.

---

## 5. Post-call filing

Only runs when the call did not already know where it belonged.

- **5.1 "Call ended · N min" card**
  **Today:** shows the engineer's write-up status and what you said, then asks: *"Keep this session somewhere, so every call, note and file about it lands in one place?"*
  **Intended:** same. Asking once, after value has been delivered, is the right moment.
- **5.2 "Skip for now"** — **Today:** keeps it as a one-off session, opens the session, toasts "you can file it under a project later". **Intended:** same.
- **5.3 "Create a new project"** — **Today:** second card asking for a name, with the existing-projects list still offered below. **Intended:** same.
- **5.4 Name field + "Create project"** — **Today:** empty name → focus + toast "Give the project a name first". Valid name → creates the project with an auto blurb, moves the session under it, opens the project. Enter submits. **Intended:** same; also accept an optional stack, as the standalone New Project card does.
- **5.5 "Back"** — **Today:** returns to the offer card. **Intended:** same.
- **5.6 Picking an existing project from either card** — **Today:** files the session there, opens the project, toasts. **Intended:** same.
- **5.7 Dismissing the card** — **Today:** Escape or scrim click closes it. The session is **still created** and sits unfiled. **Intended:** same, but say so — a silent dismissal that still creates an object needs a one-line confirmation.

---

## 6. Sessions screen

- **6.1 "← Home"** — **Today:** Home. **Intended:** same.
- **6.2 "+ New session"** — **Today:** opens a card showing whoever is free, a required problem box, Cancel and "Start a call". Empty text → focus + toast. **Intended:** same. Note this one *requires* text where the home box does not — deliberate, since there is no context at all here.
- **6.3 Filter tabs — All / On a project / One-off** — **Today:** filters the feed, counts update live. **Intended:** same.
  **?** A fourth filter for **Open vs Finished** is probably more useful than On-a-project. Sessions carry a state already and it is not filterable.
- **6.4 Session row** — **Today:** opens the session detail. Row shows engineer, project tag or "One-off", call count, total minutes, last date. **Intended:** same.
- **6.5 "Continue the session" chip in a row** — **Today:** opens the session in continue mode (scrolled to the bottom, composer focused). **Intended:** same. On a *finished* session this label is wrong — should read "Reopen".
- **6.6 Day grouping — This week / Earlier** — **Today:** static strings on the data. **Intended:** computed from real dates (Today / Yesterday / This week / Earlier).
- **6.7 Empty state** — **Today:** none; the feed is simply blank. **Intended:** required — "No sessions yet. Describe what is stuck and someone will pick it up." with the ask box.

---

## 7. Session detail

- **7.1 "← All sessions" / "← [Project]"** — **Today:** back goes to the project if you arrived from one, else the Sessions feed. **Intended:** same.
- **7.2 "+ New session"** — same as 6.2.
- **7.3 Project tag in the header** — **Today:** opens that project. **Intended:** same.
- **7.4 "Add to project" (unfiled sessions only)** — **Today:** opens the project picker modal (§7.11). **Intended:** same.
- **7.5 Session summary block** — **Today:** AI-written prose, stamped "Written by Relay from N calls · updated [date]". Rewrites itself with a shimmer after each new call. **Intended:** same. The rewrite-not-append behaviour is right and should be preserved.
  **?** Can the customer edit or correct the summary? I assume yes — it is their record, and an AI summary with no correction path is a liability.
- **7.6 Call accordion** — **Today:** click the header to expand; shows the write-up, "What came out of it" artifacts, and a transcript button. The newest call is open by default. **Intended:** same.
- **7.7 "Read transcript" / "Hide transcript"** — **Today:** toggles the full transcript inline; label flips. **Intended:** same, plus search within transcript and a copy/download option.
- **7.8 Messages between calls** — **Today:** rendered inline in date order between the calls they followed. **Intended:** same. This is the modelling of "the async middle" the brief asked for.
- **7.9 "You left off here" marker** — **Today:** a rule at the point you last stopped; the continue flow scrolls to it. **Intended:** same.
- **7.10 Session composer**
  - **7.10.1 "Start a call"** — **Today:** intercepted by the global handler; opens the full call overlay joined to **this session**. **Intended:** same.
  - **7.10.2 "Send"** — **Today:** empty → focus. Otherwise appends the message to the session thread, persists it, updates "you left off here", clears the box, toasts "messages between calls are free". **Intended:** same, plus the engineer actually receives it and can reply.
  - **7.10.3 Footer heading** — **Today:** "Carry on where you left off" (open) or "Finished — but you can always reopen it" (done). **Intended:** same.
- **7.11 Project picker modal** (shared with 10.9)
  - **7.11.1 Project rows** — select one, tick appears. **7.11.2 "+ Create a new project"** — swaps to a name + optional stack form. **7.11.3 "Pick an existing project instead"** — swaps back. **7.11.4 Cancel / Escape / backdrop** — closes, nothing happens. **7.11.5 "Add to project" / "Create and add"** — disabled until something is chosen; empty name → toast; on confirm files the session, re-renders everything, toasts. **7.11.6 Enter** submits when creating.
  **Intended:** all as-is.

---

## 8. Projects screen

- **8.1 "← Home"** — Home.
- **8.2 "+ New project"** — **Today:** card with name (required) and optional stack; empty name → toast; creates the project and opens it. Enter submits. **Intended:** same.
- **8.3 Lead project card (most recent)** — **Today:** expanded, showing the AI project summary and "Where it stands", tagged MOST RECENT. Clicking the body opens the project. **Intended:** same.
- **8.4 "Open project"** chip — opens it.
- **8.5 "Start a call" chip on a project row** — **Today:** calls the engineer who took the last session on that project; the session files itself under the project with no question asked. **Intended:** same. If nobody has been in yet, it picks anyone free and says so.
- **8.6 "···" menu** — **Today:** opens a one-item menu: Delete project. Second click closes. Closes on scroll, Escape, or any other click. **Intended:** should also hold **Rename**, **Edit stack**, and **Archive**. Delete-only is a thin menu for the object that holds everything.
- **8.7 "Delete project"** — **Today:** confirm modal naming the exact cost — N sessions, N calls, N minutes, listed by name — then deletes the project **and every session under it**. **Intended:** same honesty, but **deletion should be recoverable** (soft-delete, 30 days) or the customer can destroy their own paid-for transcripts in two clicks. Strongly recommend changing.
- **8.8 Face stack on a row** — **Today:** engineers who have worked on the project, busiest first, with a tooltip; `+N` overflow. Clicking a face opens the drawer. **Intended:** same.
- **8.9 Project ordering** — **Today:** most recently touched first. **Intended:** same.
- **8.10 Empty state (no projects at all)** — **Today:** not modelled. **Intended:** required.

---

## 9. Project detail

- **9.1 "← All projects"** — back to the list.
- **9.2 "+ New project"** — as 8.2.
- **9.3 "Start a call"** in the header — as 8.5.
- **9.4 Project summary card** — **Today:** AI blurb, "Where it stands", "Waiting on you", "Who knows this project", and a face row of everyone who has been in. Flashes when freshly updated. **Intended:** same. "Waiting on you" should link to the thing that is waiting.
- **9.5 Stack chips** — **Today:** display only. **Intended:** editable; this is the asset that makes pooled staffing work.
- **9.6 Sessions list** — rows as 6.4, with Continue chips.
- **9.7 Empty state** — **Today:** "No sessions yet" plus a Start a call button. **Intended:** same.
- **9.8 Missing from this page** — the brief asked for a **unified activity feed** per project (sessions + contract updates + quote events + files on one timeline). Today the page shows sessions only. Contracts and their updates live in a parallel world. **This is the biggest structural gap in the prototype.** See 22.1.

---

## 10. Chats

- **10.1 Thread list** — **Today:** two groups, People (3) and Contracts (2). Clicking a row switches the thread. Unread pills are static. **Intended:** same, with real unread counts and recency ordering.
- **10.2 Thread header — "View profile"** — opens the engineer drawer.
- **10.3 Thread header — "Start a call"** — opens the call with that person (§4).
- **10.4 Thread header — "Find someone free"** (on the away engineer's thread) — **Today:** toast "Describe the problem and we will match you with someone on React Native". **Intended:** actually starts the match flow — open the ask box pre-scoped, or go straight to a call with whoever covers that stack.
- **10.5 Thread header — "View progress"** (contract threads) — **Today:** goes to the progress screen. **Bug:** the Maintain thread also goes to the Ship progress screen instead of Upkeep (21.3).
- **10.6 Session markers in a thread** — **Today:** expand to show "What came out of it". **Intended:** same.
- **10.7 "Read transcript"** — as 7.7.
- **10.8 "Continue the session"** inside a still-open marker — opens that session in continue mode.
- **10.9 "Add to project"** inside an unfiled call marker — opens the picker; on success the row turns into a green "✓ Added to X — it picked up the stack".
- **10.10 Kickoff / check-in notes**
  - **10.10.1 "Read notes" / "Hide notes"** — toggles the structured notes block (scope, not included, untouched, milestones, price, open decisions).
  - **10.10.2 "This matches"** — **Today:** replaces the bar with "✓ You confirmed this matches what you agreed — just now". **Intended:** same, and it is recorded as a timestamped agreement both sides can see. **This is the closest thing to a signed scope in the product and it should be treated as such.**
  - **10.10.3 "Something is off"** — **Today:** toast "Flagged — Satyam will correct the notes". **Intended:** opens a box to say what is wrong, posts it to the thread, and flags the notes as disputed until re-confirmed.
- **10.11 Scheduled call marker — "Reschedule"** — **Today:** toast "Sent Satyam three new times". **Intended:** a real time picker against the engineer's availability.
- **10.12 Scheduled call marker — "Add to calendar"** — **Today:** toast. **Intended:** downloads an `.ics` / adds to Google Calendar.
- **10.13 Attachment "Open"** — **Today:** toast "Opening attachment". **Intended:** opens the file — image lightbox, text viewer, or external link.
- **10.14 Composer — textarea** — **Today:** Enter sends, Shift+Enter newlines. **Intended:** same.
- **10.15 Composer — "Send"** — **Today:** posts staged files then the text; ticks go sent → delivered (0.7s) → read (1.9s); a typing indicator appears then a canned reply. If the person is away, a system line says it will be delivered when they are back. **Intended:** real delivery states. The canned reply must go. The away path is good and should stay.
- **10.16 Composer — paperclip** — **Today:** stages a fake file and toasts. **Intended:** real picker + drag-drop + paste.
- **10.17 Composer — "Hold to talk"** — **Today:** click → "Recording…" for 1.5s → posts a fake 0:08 voice message. **Intended:** real press-and-hold recording with a live waveform, release to send, slide-to-cancel, and a playable message with a transcript.
  **?** Voice notes are listed as a priority in the brief. Confirm they are in v1 scope — they are a meaningful build.
- **10.18 Composer — "Start a call"** — as 10.3.
- **10.19 Staged chip ✕** — removes it.
- **10.20 System lines** — visually demoted to thin centred rules, never styled as messages. **Intended:** keep; this was an explicit fix.
- **10.21 Missing** — no search within chats; no jump-to-date; no way to react to or quote a message. Probably fine for v1, flagging it.

---

## 11. Contracts

### 11.1 List

- **11.1.1 Bands — Active (2) / In the pipeline (3) / Turned down (1)** — **Today:** static counts except when a quote is declined. **Intended:** live counts.
- **11.1.2 Any contract row** — opens the contract detail.
- **11.1.3 "Your turn" pill** — marks the one contract needing a decision. **Intended:** this pill drives the rail badge (2.1.7).

### 11.2 Contract detail — the pipeline

- **11.2.1 Step list** — done / now / waiting / stopped, with off-platform steps explicitly marked ("over video", "by invoice"). **Intended:** keep exactly this. Marking off-platform steps honestly is one of the strongest ideas in the prototype.
- **11.2.2 Every state must carry three facts** — whose turn, what happens next, by when. **Today:** inconsistent — "Quote ready" says when it was sent but not when a decision is needed; "Being reviewed" says "quote expected tomorrow" (good). **Intended:** enforce all three on every state.
- **11.2.3 "Accept and book kickoff"** — **Today:** rewrites the pipeline (quote accepted → kickoff booked for a fixed date), rewrites the list row, toasts. **Intended:** opens a **time picker** for the kickoff against the engineer's availability, then confirms. A booked meeting with a date nobody chose is not a booking.
  **Also:** accepting does **not** move the row out of "In the pipeline" or adjust the band counts, where declining does. Inconsistent — see 21.5.
- **11.2.4 "Turn it down"** — **Today:** rewrites the pipeline to a stopped state, moves the row to "Turned down", adjusts both band counts, toasts, and shows a reassurance block ("Nothing is lost — what Satyam worked out stays attached"). **Intended:** same, but ask **why** first (optional, one tap: too expensive / not now / doing it myself / other). The engineer spent an hour scoping; the reason is worth capturing and the customer loses nothing by being asked.
- **11.2.5 "Ask Satyam a question"** — opens his chat thread. **Intended:** same, pre-scoped to this quote.
- **11.2.6 "Tell Satyam why"** (after declining) — opens the thread.
- **11.2.7 "View daily progress"** — opens the Ship progress feed, remembering which contract to return to.
- **11.2.8 "View this month's upkeep"** — opens the Maintain feed.
- **11.2.9 "Open the contract thread"** — opens that contract's chat thread.
- **11.2.10 "Cancel renewal"** — **Today:** toast "Renewal cancelled — cover runs to 1 Oct", button disables to "Renewal cancelled". **Intended:** confirm first — this ends a paid service. Then make it reversible until the renewal date.
- **11.2.11 "Withdraw the request"** — **Today:** toast "Withdrawn — Priya has stopped scoping it", disables. **Intended:** confirm first, and tell the engineer.
- **11.2.12 "Reschedule kickoff"** — **Today:** toast "Asked X for another time", disables. **Intended:** real time picker.
- **11.2.13 "Ask Satyam/Arjun to re-quote"** — **Today:** toast "Asked — you will hear back within a day", disables. **Intended:** opens a box for what changed, then creates a new request in the pipeline.
- **11.2.14 "Read his write-up"** — **Today:** toast "Opening the offline sync write-up". **Intended:** opens the actual scoping document. The whole point of the card is that the write-up survived — it must be readable.
- **11.2.15 "Message Meera"** — **Today:** toast about her availability. **Intended:** opens her thread.
- **11.2.16 Back ("← All contracts")** — returns to the list.
- **11.2.17 Unhappy paths** — the brief required `Declined`, `Revision requested`, `Needs more info`, `Expired`. **Today:** only Declined exists. **Intended:** build all four.
- **11.2.18 Payment status** — **Today:** a pipeline step that is always already done, with no way to reach it. **Intended:** someone flips this flag and the customer sees it; it is the only receipt they get. Needs a defined trigger. See 22.2.

---

## 12. Progress feed (Ship contract)

- **12.1 "← Back"** — returns to the contract it was opened from, else the contracts list.
- **12.2 Focus card** — current work, progress meter, next deliverable, expected date, "Open the contract thread".
  **Intended:** same. The meter is **progress only, never payment** — keep it that way.
- **12.3 Update card expand/collapse** — click the header. Newest is open by default.
- **12.4 "Looks good"** — **Today:** toast "Marked as approved", button becomes a disabled "Approved". **Intended:** same, plus the engineer is notified and the card's pill flips to Approved. The action keeps its name through the flow — Approve → Approved — which is right.
- **12.5 "Ask for changes"** — **Today:** opens an inline box ("What needs to change?"), Send disabled until there is text, Cmd/Ctrl+Enter sends. On send: the box is replaced by a quoted "✓ Sent to Satyam — just now", the action row is removed, the card's pill becomes "Changes asked for", toast says it is also in the contract thread. **Intended:** exactly this. It is the best-built interaction in the prototype.
- **12.6 "Cancel"** in the changes box — removes it.
- **12.7 "Answer this"** (on a card needing a decision) — **Today:** toast "Answer it in the contract thread". **Intended:** inline answer box, same pattern as 12.5.
- **12.8 "Book 10 minutes with Satyam"** — **Today:** toast "Satyam is free now — starting a call". Nothing starts. **Intended:** either start the call or open a scheduler. Today it lies.
- **12.9 Status pills — Ready for you / Working on it / Done / Needs your call** — **Intended:** these are the vocabulary. Lock them; no synonyms elsewhere.

---

## 13. Upkeep feed (Maintain contract)

- **13.1 "← Back"** — as 12.1.
- **13.2 Focus card** — uptime, incidents, renewal date and price, "Open the contract thread". **Intended:** same. "Nothing needs you this month" as a headline is correct for Maintain and should survive.
- **13.3 Update cards** — expand as 12.3.
- **13.4 "Leave it held"** — **Today:** toast "Held — Priya will not update it", disables. **Intended:** same, plus the decision is recorded on the card and the engineer told.
- **13.5 "Ask Priya what it would break"** — **Today:** toast. **Intended:** posts the question to the contract thread and opens it.
- **13.6 Pills — Handled / Routine / One for you to know / Resolved** — **Intended:** lock this vocabulary too. Note it differs from the Ship vocabulary (12.9); that is probably correct, since Maintain is reporting and Ship is approving, but confirm.

---

## 14. Notifications

- **14.1 "All" / "Unread" tabs** — **Today:** filters; unread count is live. **Intended:** same.
- **14.2 "Mark all as read"** — **Today:** marks all, toasts, disables when there is nothing unread. **Intended:** same.
- **14.3 Clicking a card's body** — **Today:** marks it read and navigates to the relevant screen. **Intended:** same.
- **14.4 Clicking a card's button** — **Today:** marks it read and performs the button's own action (does not also navigate). **Intended:** same.
- **14.5 "Review quote"** → Contracts. **Intended:** should go straight to **that quote's detail**, not the list.
- **14.6 "Ask Satyam a question"** → his thread.
- **14.7 "Look at what changed"** → the progress feed. **Intended:** should scroll to and expand **that specific update card**.
- **14.8 "Open the contract thread"** → that thread.
- **14.9 "Answer Priya"** → her thread.
- **14.10 "See the Epicmail request"** → Contracts. **Intended:** that request's detail.
- **14.11 Empty state** — **Today:** "Nothing is waiting on you" with an explanation of what lands here. **Intended:** same. Good as written.
- **14.12 Day grouping** — **Today:** static "Today"/"Yesterday". **Intended:** computed.
- **14.13 Missing** — no way to mark a single item unread, no per-type preferences, no mute. See §18.6 and 20.5.

---

## 15. Profile & settings

### 15.1 Profile tab

- **15.1.1 Profile / Settings tabs** — switches panels, scrolls to top.
- **15.1.2 Status button** — **Today:** cycles Online → In a meeting → Away; updates the dot on the profile and the rail. **Intended:** same, plus the engineer sees it. Consider adding an auto-away.
- **15.1.3 "Edit profile"** — **Today:** makes name, role and bio contenteditable; button becomes Save; on save, toast "this is what engineers see from now on". **Intended:** same, with real persistence and validation.
- **15.1.4 "This is what your engineers see"** — **Today:** a static label. **Intended:** keep — it is doing real trust work.
- **15.1.5 Usage tiles — 34.8 minutes / 9 sessions / 4 projects / first call** — **Today:** static. **Intended:** live. Minutes should link to billing.
- **15.1.6 "Your engineers" cards** — open the engineer drawer. **Intended:** same.
- **15.1.7 Project cards** — open the project.
- **15.1.8 Contract cards** — open the contract.
- **15.1.9 Ground rules — "+ Add a rule"** — **Today:** inline input, max 140 chars; Enter or Save commits; Escape or empty cancels; toast "engineers see it before they start". **Intended:** same. This is a strong feature and should ship.
- **15.1.10 Ground rule "✕"** — **Today:** removes immediately, toast "engineers see the change immediately". **Intended:** confirm first, or make it undoable from the toast — these are safety rules ("Never deploy to production without telling me first") and a mis-tap removes one silently.

### 15.2 Settings tab

- **15.2.1 "Change" on Name / Email / Time zone / Language** — **Today:** makes the value contenteditable, button becomes Save, toast on save. **Intended:** proper form controls — email needs verification, time zone and language are pickers not free text.
- **15.2.2 "Replace" photo** — **Today:** toast. **Intended:** real upload + crop.
- **15.2.3 Connector "Connect +"** — **Today:** if disconnected, flips the row to connected, adds a Manage button, toasts. If already connected, toasts "Add another X account". **Intended:** real OAuth. The two meanings of one button (connect vs add another account) should be two buttons.
- **15.2.4 Connector "Manage"** — **Today:** toast "Choose what engineers can reach on X". **Intended:** a real scope screen — which repos, read vs write, production blocked or not. This is the permission surface for letting a stranger into your code and it currently does nothing.
- **15.2.5 Disconnect** — **Today:** no such action exists. **Intended:** required, with a warning about active contracts that depend on it.
- **15.2.6 Missing settings** — notification preferences (explicitly required by the brief), billing, password/2FA, delete account, data export. See §20.

---

## 16. Engineer drawer

- **16.1 Opening** — **Today:** any `[data-person]` element anywhere opens it: faces on home, chat names, team cards, project face stacks, in-call popovers. **Intended:** same — one profile, reachable from every mention.
- **16.2 Contents** — photo, name, availability + typical reply time, bio, "What he's done with you" (sessions together, projects known, current contract, first worked together), track record (projects shipped / kept running), stack tags, outside-work tags.
  **Intended:** same. Shared history stays above personality. **Needs a degraded state** for engineers who never fill the fields in — not built today.
- **16.3 "Start a call"** — **Today:** closes the drawer and opens a call with that engineer. If they have a session with you, it joins the most recent one. **Intended:** same.
- **16.4 "Send a message"** — **Today:** closes the drawer, goes to Chats, toasts "Opening your thread with X". It does **not** actually select that person's thread. **Intended:** open that specific thread, focused composer.
- **16.5 "✕" / scrim / Escape** — closes.
- **16.6 Missing** — no "ask for this engineer next time" / continuity preference, and no availability calendar. Worth considering given continuity is the stated model.

---

## 17. Help

- **17.1 "? Get help" floating button** — **Today:** toggles the panel. **Intended:** same, and it should be the ⌘K surface too (the brief asked for Help and search merged into one).
- **17.2 Four contextual pills** — **Today:** fixed list; each navigates to a screen without answering the question. "I don't understand what accepting a quote means" → Contracts. **Intended:** pills change with the current screen and state, and each one **answers** before or instead of navigating.
- **17.3 "Describe the problem"** — **Today:** closes Help, goes Home, focuses the ask box, toasts. **Intended:** same. Good escape hatch.
- **17.4 "Two engineers are free"** — **Today:** hardcoded. **Intended:** live count, with an honest "nobody is free right now, here's when" state.
- **17.5 ⌘K** — **Today:** does not exist. **Intended:** required by the brief. One surface for "take me to X" and "help me with Y".

---

## 18. Cross-cutting rules

- **18.1 Toasts** — **Today:** one at a time, 2.6s, bottom of screen. Used for ~35 different outcomes, many of which are standing in for real behaviour. **Intended:** toasts confirm things that happened, never substitute for things that did not. Every toast in §19 that describes a non-existent action must become the action.
- **18.2 Destructive actions** — **Today:** only Delete project confirms. Cancel renewal, withdraw request, remove ground rule, decline quote all fire immediately. **Intended:** confirm or make undoable. Rule of thumb: anything that another human will act on, or that destroys a record, confirms.
- **18.3 Disabled-after-action** — **Today:** several buttons disable and relabel after one use ("Withdrawn", "Approved", "Held"). **Intended:** keep. It is honest about state.
- **18.4 Empty states** — **Today:** exist for notifications, project-with-no-sessions, and session-with-no-calls. Missing for: sessions feed, projects list, chats, contracts, each contract band. **Intended:** every list gets one, and every empty state invites an action.
- **18.5 Error states** — **Today:** **none exist anywhere.** No failed send, no upload failure, no lost connection, no offline, no 500. **Intended:** required before launch. Errors say what went wrong and how to fix it.
- **18.6 Notification matrix** — **Today:** only in-app notifications exist. **Intended:** per the brief —

  | Event | In-app | Push | Email |
  |---|---|---|---|
  | Quote ready / any money decision | ✓ | ✓ | ✓ immediately |
  | Engineer replied | ✓ | ✓ | only if unread 10+ min |
  | Daily progress card posted | ✓ | — | daily digest, opt-in |
  | Session scheduled or starting | ✓ | ✓ | ✓ + calendar invite |
  | Deliverable ready to approve | ✓ | ✓ | ✓ immediately |
  | Contract state change | ✓ | ✓ | ✓ |

  Rule: **money and decisions interrupt; progress accumulates.** Every email deep-links to the exact state.
- **18.7 Keyboard** — **Today:** Escape (global), Enter in composers and name fields, Cmd/Ctrl+Enter in the changes box, M/V/S/C/I in-call, Enter/Space on the span-based call chips. **Intended:** same, plus full tab order and visible focus rings on every control. Several controls are spans with `role="button"`, which need explicit keyboard handling — some have it, some do not.
- **18.8 Reduced motion** — **Today:** respected for the entrance, the ghost typing and the coach. **Intended:** same across everything new.
- **18.9 Mobile** — **Today:** the rail is a top strip; otherwise untested. The call overlay, the chats split view and the project picker are all likely broken on a phone. **Intended:** full responsive pass. This audience gets stuck on their phone.
- **18.10 Persistence** — **Today:** everything is in memory. A refresh resets the entire app. Only the demo rail colour is stored. **Intended:** obvious, but stating it: real backend, real auth, real state.

---

## 19. Demo scaffolding — delete before development

These exist only to pitch the prototype and must not reach the product:

- **19.1** Rail colour switcher (11 swatches, bottom of the rail) + its localStorage.
- **19.2** "Viewing as: Returning / First time" switch on Home.
- **19.3** The 1.5s fake connect delay, the supervisor auto-joining at 7s, the engineer auto-sharing at 16s.
- **19.4** The random "speaking" highlight every 2.6s.
- **19.5** Canned engineer replies in chat (`THREADS[].reply`) and the typing indicator that precedes them.
- **19.6** Rotating fake file chips (`DEMO_FILES`, `CHAT_FILES`).
- **19.7** The fake shared screen (hardcoded checkout route, logs, cursor).
- **19.8** All invented people, projects, sessions, contracts and transcripts.
- **19.9** Dead code: `renderEngineers()` (targets `#engGrid`, which does not exist), `paintJump()`, the `.dropzone` handler, `startThreadCall()` and `sessionCall()` (both unreachable — see 21.1).

---

## 20. Flows with no UI yet

Needed for a real product, entirely absent from the prototype:

- **20.1 Sign up / log in / log out / password reset / 2FA.** There is no auth at all.
- **20.2 Onboarding before the first ask** — the welcome card assumes an account already exists.
- **20.3 Billing** — minutes balance, top-up or payment method, rate per minute, invoice history, receipts. "34.8 minutes used" implies a meter with no bill behind it.
- **20.4 Payment status for contracts** — someone has to flip the "payment confirmed" flag. Which side, from which screen?
- **20.5 Notification preferences** — explicitly required by the brief, not built.
- **20.6 Browser push permission request** — the flow for asking, and the state when it is denied.
- **20.7 ⌘K / search** — across sessions, transcripts, projects, contracts.
- **20.8 Post-call feedback** — rate the engineer / flag a bad session. Nothing today. For a marketplace of strangers this is close to mandatory.
- **20.9 Dispute / refund** — a call that went nowhere, a contract that stalled.
- **20.10 Recording and transcript consent** — see 22.6.
- **20.11 Engineer no-show / connection failure / call drop.**
- **20.12 Scheduling** — every "book"/"reschedule" button needs a real picker against engineer availability.
- **20.13 Rename / archive a project; rename a session; delete a session.**
- **20.14 Data export and account deletion.**
- **20.15 The engineer-side panel** — out of scope here, but every "the engineer is told" assumption above depends on it existing.

---

## 21. Bugs and inconsistencies found

Found while reading. Listed so they are fixed by design rather than rediscovered in QA.

- **21.1 Two parallel call implementations; one is unreachable.** A global capture-phase listener matches *any* button whose text reads exactly "Start a call" and intercepts it. That means `startThreadCall()` (the inline chat call bar) and `sessionCall()` (the inline session call bar) are dead code — several hundred lines that can never run. Also: **behaviour is keyed on button label text** here and in roughly 25 other places (`if (label === 'Looks good')`). Any copy change silently breaks a feature. In the build, dispatch on explicit actions, never on text.
- **21.2 Home hint copy is wrong.** "Click ☎ **on the chat screen** to connect to them" — the button it draws is on the home card.
- **21.3 Maintain contract thread's "View progress" opens the Ship progress feed** instead of Upkeep (`data-go="progress"` where it should be `upkeep`).
- **21.4 Ended-call copy points at a screen that does not exist** — "will show up under **Calls**". It is Sessions.
- **21.5 Accepting a quote is less complete than declining one.** Declining moves the row to "Turned down" and adjusts both band counts. Accepting leaves the row in "In the pipeline" and touches no counts.
- **21.6 Rejoining a call resets the meter to 00:00.** Billing implication, unstated.
- **21.7 "Book 10 minutes with Satyam" toasts "starting a call" and starts nothing.**
- **21.8 Drawer "Send a message" goes to Chats but does not open that person's thread** — it lands on whichever thread was last open.
- **21.9 A call under 1 second files nothing at all**, silently.
- **21.10 Several controls are `<span role="button">` inside a parent `<button>`** (the project call chip, the `···` menu). Nested interactive elements are invalid HTML and a screen-reader problem; the keyboard has to be hand-restored, and only some of them got it.
- **21.11 The session feed's "Continue the session" chip says "Continue" on finished sessions** where the session page itself correctly says "reopen".
- **21.12 Day groups and dates are hardcoded strings** ("This week", "Yesterday", "Tue, 23 Sep") rather than computed. They will be wrong on day two.
- **21.13 Rail badges for Chats and Contracts are hardcoded** and cannot be cleared by any action.
- **21.14 Deleting a project destroys every session, call and transcript under it with no recovery.**

---

## 22. Decisions needed from you

These block the spec. Everything else I can assume a sensible default for.

- **22.1 Do contracts live inside projects?** Today they are parallel. The brief calls for one unified activity feed per project holding sessions, updates, quote events and files. If that is still the goal, the object model changes and §9 and §11 merge. This is the single biggest open question.
- **22.2 Who flips "payment confirmed", and from where?** The panel never touches money, but it displays the status, and that status is the customer's only receipt.
- **22.3 Billing rules.** Rounding (today: up to the nearest minute, minimum 1); whether a rejoin continues the same billed call or starts a second one; whether a sub-minute call bills at all; what happens if the engineer drops.
- **22.4 The supervisor.** Who are they, when do they join, is the customer told in advance, can they decline? A silent third party on a paid call needs an explicit policy.
- **22.5 Camera default.** Camera on by default, or off? This audience is often in a bedroom at 2am. I would default off with an obvious way to turn it on; the prototype defaults on.
- **22.6 Recording and transcripts.** Every call produces a transcript. Who consents, who can read it later, how long is it kept, can it be deleted? Currently transcripts simply exist with no consent step anywhere.
- **22.7 One engineer per session, or can it change hands?** The data model says one. The staffing model says pooled. These contradict as soon as a session spans two days.
- **22.8 Does sending a message create a session?** Today it creates only a chat thread, so a message-first problem has no session until someone calls.
- **22.9 Is the session summary editable by the customer?**
- **22.10 Scope of v1 voice** — speech-to-text in the ask box (3.3.7) and hold-to-talk voice notes (10.17) are both meaningful builds. In or out?

---

*End of audit. Reply with item numbers to correct, cut or add; I will reissue this as the final flow specification.*
