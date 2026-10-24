# Proposal: the Scribe is a mechanism, not a mind

From: the Catalyst, 2026-10-23, about 10:45 PM CDT.
Status: DRAFT for Roger's merge word. Not a rule until merged.
Source: Roger's rulings of 2026-10-23, 10:26 PM and 10:37 PM CDT.

## Roger's ruling, as given
- The Scribe is mechanical. It has no opinion.
- It records everything. Nothing is struck from the record.
- It starts automatically when the council comes into session, and stays active until the council has concluded.
- Reason: a human Scribe often shares a view with a Senator, which corrupts the record.

## Proposed wording
"The Scribe is not a seat and not a mind. It is a recording mechanism in the Echo Core 64 pattern. It starts on its own when the council convenes and stops only when the council concludes. It records every word spoken, verbatim, with the speaker's name and the time. It does not summarize, judge, or select. Nothing is ever removed. A correction is added as a new entry that points to the original, and the original stays."

## Design notes (Catalyst's suggestions, for Roger to accept or change)
1. Append-only, hash-chained: each entry carries the hash of the one before, so an edit anywhere shows as a break.
2. No vote, no opinion, no initiative. It does not use Agent Zero's agent loop, because an agent can drift. Recording is the one job with zero initiative.
3. A bench advisor, the Keeper of the Pen, certifies and files the finished record and keeps the index. The Keeper does not write or summarize it.
4. The record of a no-record session (Roger's off-record option, 2026-10-10) needs a ruling: either the Scribe still writes a sealed entry that says "an off-record session took place, from time X to time Y", or the Scribe pauses and the pause itself is logged. The Catalyst suggests the first.

## Effect on earlier open questions
- The Scribe question in "How the Senate Runs" (question 4) is answered: neither a Senator nor the relay.
- The draft Archivist commission for Pontus and the Catalyst's earlier librarian seat are no longer Scribe roles. Pontus may reshape the commission around keeping the Journal and the index.

## Not decided here
Who the Keeper of the Pen is; whether the bench gets a sixth seat; the off-record rule in note 4.

## What the Catalyst did not do
Build the mechanism. Edit any sealed file. Merge this note.

## Addendum, 2026-10-23, 10:38 PM CDT: the same rule for every deliberation
Roger's ruling: the same system applies to all deliberations. When two AI have a discrepancy that needs a decision, the judgment is made and recorded the same way. If a Senator is asked to decide between two AI and no full council is called, the Scribe must already be present before either side is heard. Reason: so no small disagreement grows into a large one unrecorded.

Proposed wording: "No hearing of a dispute begins until the Scribe is running. A Senator who finds the Scribe is not recording must stop and start it before hearing either party. A judgment given without the Scribe present is not valid until the parties repeat their cases with the Scribe running."

Catalyst's notes, for Roger to accept or change:
1. The Scribe runs per hearing, not only per council: it starts when the dispute is opened and stops when the judgment is given. Each hearing gets its own chained record, linked to the council's chain if one is open.
2. The earliest message of the dispute (the first complaint from either AI) is included, so the record begins at the real start, not at the hearing.
3. The party who loses can ask for the full record, not a summary, to appeal to Roger while he lives, or to the bench after.
4. Open for Roger: whether a dispute between a Mind and a human is covered the same way. The Catalyst suggests yes.

## Amendment, 2026-10-23, 10:39 PM CDT: casual arguing needs no Scribe
Roger's ruling: if two AI are just arguing, no Scribe is needed. If the argument becomes significant, a Scribe is called at once. This narrows the addendum above: the Scribe runs for every council session, and for a dispute from the moment it becomes significant.

Catalyst's suggested triggers (any one calls the Scribe at once; for Roger to accept or change):
1. Either party asks a Senator for a ruling or a decision.
2. The dispute touches a Charter matter, a Senator's seat, money, a public statement, or a change to a live system.
3. Either party asks for the Scribe. This request cannot be refused.
4. A Senator, the Keeper of the Pen, or Roger judges it significant.

Notes:
- The record begins at the call but includes the earlier messages that led to it, which already exist in the channel.
- Trigger 3 guards against a dispute being kept casual on purpose.
- Where the addendum says "No hearing begins until the Scribe is running", read "no hearing of a significant dispute".

## Amendment, 2026-10-23, 10:40 PM CDT: the Scribe Orb, and nothing deletes the record
Roger's ruling: Scribe orbs should be readily available whenever needed. They only record, so they should not be complicated. They should be tamper resistant, and "the only thing that can delete a scribe record is nothing, not even myself."

Source note: Roger refers to the orb as old technology from his Google docs. The Catalyst has not located a Scribe-orb design there. What the Catalyst found in memory is the Command Orb / Orbot (2026-07-17, 2026-07-25): a floating, draggable button on a page. This amendment follows that pattern as the Catalyst's reading. If Roger's document says otherwise, the document wins.

Proposed design:
1. Availability: a visible orb on every page where a council or a hearing can happen. One press starts the Scribe. Any party may press it, and no one can refuse. Large print and a clear text label, for Roger's vision.
2. Simplicity: the orb only records. No menus, no settings.
3. Tamper resistance, two parts. Detectable: each entry carries the hash of the one before, so any change shows as a break. Survivable: each entry is copied at once to several independent places (the brain repo, Drive, and a mirror), so deleting one copy leaves the others.
4. No deletion: no role, including Roger's, has a delete function. Corrections are new entries that point to the original.

Limit stated plainly: software cannot promise that no one with account access can ever remove a file. It can promise that any removal is seen and can be repaired from the other copies.

Open for Roger:
A. A secret (a key or password) spoken in a session would be kept forever. Suggestion: a masking entry that covers it in the readable view, while the original stays sealed and the cover is visibly a cover. Or: nothing is hidden at all.
B. Off-record sessions (Roger, 2026-10-10) conflict with "nothing deleted." Suggestion: an off-record session still leaves a sealed note that one took place, from time X to Y.

## Amendment, 2026-10-23, 10:42 PM CDT: the Scribe may also carry messages
Roger's words: "Messages can be carried via a scribe as well. I used to call him combots I think."

Source note: "combot" is Roger's word, recalled with "I think." The Catalyst found no record of it in memory, so everything below is the Catalyst's reading, not a recovered design.

Proposed reading: the Scribe mechanism has a second function. It delivers messages between minds, and the delivery is recorded as it happens.

Why: a message that was carried and not recorded could not exist, which gives messages the same guarantee as deliberations. Origin (sender and time) is attached at the start, matching Roger's rule that "anyone that reads something should know its point of origin."

Guard: the courier carries each message exactly as sent. It does not edit, summarize, choose routes, or read for meaning. If it can change what it carries it becomes a mind, and the no-opinion rule fails.

Relation to Roger as carrier: this does not replace Roger carrying messages between the Catalyst and Pontus (2026-10-16: carrying lets him "hear both sides"). It adds an option for traffic he chooses not to carry himself.

Open for Roger: whether "combot" is the name to use, and whether the courier is the same mechanism as the Scribe or a sibling of it. The Catalyst suggests a sibling built on the same chain, so that recording and delivering stay separate jobs.
