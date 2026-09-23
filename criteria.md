# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
I picked 4 of 5 because most of my test questions should have a direct answer
somewhere in the guide, but one question might use different wording than the
document uses. Requiring 5 of 5 would be too strict for a first retrieval setup,
while 3 of 5 would mean the system is missing too many normal questions.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
I picked all five because the system should already know which document each
retrieved chunk came from. If an answer cannot name a source, then the reader
has no easy way to check whether the answer came from the guide or from the
model guessing.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
I picked 4 of 5 because some out-of-scope questions may still use words that
sound similar to the guide, so one false match is possible. A lower target would
let the system answer too many questions that the documents do not actually
cover.

---

## 4. Something about your chunks

Each chunk should usually be 150-200 words, and it should focus on one clear
topic, section, or idea. If a chunk mixes multiple unrelated ideas or is shorter
than 75 words without a good reason, it should be revised.

**Why this target:**
I picked 150-200 words because that is long enough to include useful context
around an answer, but short enough that one chunk should not cover several
different topics at once. A stricter range would create too many tiny fragments,
and a looser range would make retrieval less precise.


---

## 5. My choice

For at least 4 of my 5 in-scope test questions, the named source should directly
support the main answer instead of only being related to the same broad topic.

**Why this target:**
I picked this because naming a source is only useful if the source actually
backs up the answer. I chose 4 of 5 because one question might be answered
across more than one chunk, but 3 of 5 would make the citations too unreliable.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
