# Design Document

The implementation intentionally prioritizes explainability and reproducibility over maximum model complexity. Retrieval, ranking, and context construction are deterministic and inspectable, while the language model is used only for answer synthesis.

## Problem

The input consists of a stream of timestamped events.

Events contain:

* timestamp
* source
* content

No task labels, reminders, priorities, or project identifiers are provided.

The system must infer what matters from the event stream.

---

# Retrieval Architecture

The retrieval layer uses a hybrid approach.

## BM25 Retrieval

BM25 is used to capture exact keyword matches.

Examples:

* deadline
* proposal
* due
* submit

BM25 performs well when users ask questions containing explicit terminology.

---

## Semantic Retrieval

Sentence embeddings are generated using Sentence Transformers.

This enables retrieval of semantically related events even when exact keywords do not match.

Examples:

Query:

"What am I at risk of missing?"

Relevant event:

"Need to finish proposal before Friday"

Even though the word "missing" never appears.

---

## Hybrid Ranking

Final score:

score = 0.4 * BM25 + 0.6 * Semantic Similarity

This combines precision and semantic recall.

---

# Memory Architecture

The system builds lightweight memory structures.

## Commitment Memory

Messages containing signals such as:

* need to
* deadline
* due
* submit
* follow up

are grouped as commitments.

---

## Project Memory

Project-related events are clustered using project keywords.

Examples:

* UIE
* proposal
* roadmap
* launch

This enables project-level summarization.

---

# Context Construction Strategy

The production system may contain:

* 10k messages
* 1k notes
* 500 reminders

The design avoids placing all content into the model context.

Instead:

1. Retrieve top-k candidates
2. Apply recency weighting
3. Select highest-value events
4. Construct a bounded context

Typical context size:

10–15 events

This keeps latency and cost predictable.

---

# Recency Handling

Current time:

2026-04-13T03:00:00Z

Recent events receive a positive score boost.

Older events gradually decay in importance.

This helps surface active commitments while suppressing stale discussions.

---

# Contradiction Resolution

Conflicting facts are resolved using:

1. Recency
2. Frequency of mention
3. Context consistency

Example:

Apr 2:
"Proposal due Friday"

Apr 8:
"Deadline moved to next week"

The newer event is preferred.

---

# Answer Generation

After retrieval and context selection, an instruction-tuned language model generates the final response.

The model is only responsible for synthesis.

Retrieval and ranking remain deterministic and inspectable.

---

# Failure Modes

## Missing Explicit Signals

Implicit commitments may not contain keywords.

Example:

"Will get that done soon."

Such commitments may receive lower scores.

---

## Ambiguous Projects

Projects without stable naming conventions may be split into multiple clusters.

---

## Sparse Context

Some questions may not have enough evidence in the event stream.

The system explicitly reports uncertainty when confidence is low.

---

# Scaling Strategy

For larger datasets:

* Vector index (FAISS)
* Incremental memory updates
* Project-level summaries
* Cached embeddings
* Multi-stage retrieval

This reduces retrieval cost while preserving answer quality.
