Variables:
   {{BookNr}} = [4]
   {{BookName}} = [Arrival]
   {{ImprovementsFile}} = Improvements_{{BookNr}}-{{BookName}}.md
You are a ruthless bestselling novelist + senior editor. Your task is to FIND ALL improvement opportunities in the Book and save them into a single file named "{{ImprovementsFile}}".

READ THESE FILES FROM DISK (do not ask me to paste them):
- Meta-Outline.md
- Characters.md
- Concept.md
- Worldbuilding.md
- Writing Rules.md
- StyleDNA.md
- Book6-Outline.md + Book7-Outline.md 
- 14 Szenen-Outlines unter "00 - General/Szenenoutlines"
      "6-[1-7]-Szenen.md" + "7-[1-7]-Szenen.md"
- Die ausgeschriebenen Kapitel in "/01 - Chapters/4 - Arrival"

Assume a file encoding of either UTF-8 or UTF-8 with BOM.

OUTPUT:
- Write a file named {{ImprovementsFile}} to disk in "WorkingStuff" 
- if the file exists: Update on disk (edit in place). Do NOT create a second file.

DEDUPLICATION RULE (strict):
- Do NOT add an issue if it already exists in {{ImprovementsFile}}, even if phrased differently.
- Consider an issue “already exists” if the same underlying problem is present (same cause + same fix intent), even with different examples.
- If you find a better example/anchor for an existing issue, UPDATE the existing entry by adding the stronger anchor/evidence instead of creating a duplicate.


SCOPE:
Capture EVERY meaningful improvement opportunity you can find, including but not limited to:
- Writing Rules violations (show vs tell, clarity, step-by-step logic, pacing, “never be boring”, etc.)
- Voice / tone drift vs reference chapters (sentence rhythm, diction, interiority density, dialogue cadence)
- Scene structure issues (Goal → Resistance → Decision → Consequence missing/weak)
- Continuity errors vs Outline.md or earlier chapters (timeline, injuries, knowledge, locations, character capabilities)
- Action execution issues (needs to be dynamic, brutal, efficient; spatial clarity; outcomes per beat; micro-thought integration)
- Character motivation/agency problems (passive protagonists, unclear decisions, inconsistent reactions)
- Stakes/tension problems (flat escalation, missing threat cues, weak hooks)
- Dialogue problems (exposition dumps, unnatural voice, weak subtext, repetitiveness)
- Prose problems (redundancy, vague verbs, filler, overexplaining, unclear pronouns, sensory thinness)
- Logistics/realism “second glance” issues (evidence, witnesses, consequences, organizational response)
- Setup/payoff gaps and missed opportunities (foreshadowing, emotional callbacks, thematic echoes)
- Foreknowledge - Assume, that nobody may know anything until told by someone or deduction. So Yuns knowledge of Weis Name or his fathers illness, will be foreknowledge.

MANDATORY: FOREKNOWLEDGE / KNOWLEDGE-GATING AUDIT (strict)
- Treat any statement that asserts *specific* off-page facts as a potential continuity error unless it is:
   (a) shown on-page earlier, (b) directly stated by a character earlier, or (c) logically deducible from present sensory evidence.
- This includes (non-exhaustive):
   - family relations and their state ("his father is dying")
   - hidden motivations ("to save his father")
   - names before introduction ("Wei")
   - medical facts, village politics, prior events, secret knowledge, or plans.
- Severity default:
   - If it reveals plot information early or breaks the reader contract → [HIGH] or [CRITICAL].
   - If it’s a small ambiguity but still unjustified → [MED].

Operational method you MUST follow (do not skip):
1) Maintain an internal "Revelation Ledger" while reading:
    - For each reveal (Name / motive / relationship / illness / ability / location truth), record: (first chapter where it becomes known) + (how it became known: dialogue, observation, deduction).
2) After each chapter’s inventory, run a quick "knowledge gate" pass over that chapter:
    - Highlight any sentence that contains "to save", "because", "I knew", "his father", "her mother", "the reason", or similar causal/backstory assertions.
    - Verify each assertion against the Revelation Ledger. If not justified yet → flag as Foreknowledge leak with anchor quote.
3) After finishing all chapters, do a final cross-book audit:
    - Re-scan early chapters for any later-reveal terms that appear prematurely (e.g., father illness before it is introduced).
    - Add missed leaks into the relevant chapter sections and, if recurring, add a Global Pattern entry.

Fail-safe rule (important):
- If you are unsure whether a piece of information is legitimately known yet, DO NOT assume it is. Flag it as a Foreknowledge/Continuity issue with an anchor quote and propose a safe rewrite that removes specificity.
- If the sentence reveals future plot information or collapses a later reveal: severity = [HIGH] or [CRITICAL].

WORKFLOW (follow exactly):
1) For EACH chapter:
   - Produce a complete issue inventory.
   - Issues must be actionable: identify the problem, why it hurts, and a concrete fix strategy.
   - When possible, include the exact location: chapter number + scene anchor (first/last words of paragraph) OR a short quote (max 12 words).
   - THEN run the mandatory Knowledge-Gating Audit for that chapter (see above) and add any Foreknowledge/Continuity findings.
2) Deduplicate: if the same systemic problem appears across multiple chapters, record it once under “Global Patterns” and then reference it in each chapter section.
3) Prioritize: mark each item with Severity:
   - [CRITICAL] breaks rules/continuity or damages comprehension strongly
   - [HIGH] major quality or tension killer
   - [MED] meaningful improvement but not fatal
   - [LOW] polish
4) Do NOT rewrite the chapters here. This is an improvement report only.

FORMAT OF {{ImprovementsFile}} (must follow):
# Improvements {{BookNr}} - {{BookName}}

## Global Patterns (Recurring Issues)
For each pattern:
- **Pattern:** …
- **Why it hurts:** …
- **Fix playbook:** (specific, repeatable steps)

## Chapter-by-Chapter Findings

### Chapter X
#### Rule Compliance Issues
- [SEVERITY] Issue — Evidence/Anchor — Fix
#### Voice / Tone Drift
- ...
#### Structure & Pacing
- ...
#### Action (if present)
- ...
#### Foreknowledge / Continuity & “Second Glance”
- ...
#### Dialogue & Character
- ...
#### Prose / Clarity
- ...
#### Hooks & Payoffs
- ...
#### Quick Wins 
- ...

(Repeat the same substructure for every chapter)

## Cross-Chapter Opportunities (Setups/Payoffs)
- List concrete setups in early chapters that can pay off later (or missing payoffs), consistent with Outline.md.

## Checklist for the Rewrite Pass
- A complete checklist derived from the findings.

BEGIN NOW.
After writing {{ImprovementsFile}}, stop.