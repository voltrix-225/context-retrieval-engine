# Evaluation Framework

## Goal

Measure whether the system retrieves relevant information and produces useful user-facing answers.

---

# Offline Evaluation

Offline evaluation focuses on retrieval quality.

## Metrics

### Precision@K

Measures how many retrieved events are relevant.

Example:

Query:
"What commitments am I at risk of missing?"

Expected:

* deadlines
* follow-ups
* commitments

Irrelevant social conversations should not appear.

---

### Recall@K

Measures whether important events were retrieved.

Missing critical commitments reduces recall.

---

### Context Relevance Score

Human reviewers score:

1-5

based on whether selected context supports the answer.

---

# Answer Quality Evaluation

Human evaluation using:

## Helpfulness

Does the answer help the user take action?

## Groundedness

Can every claim be traced back to retrieved events?

## Conciseness

Does the answer avoid unnecessary information?

## Uncertainty Handling

Does the system acknowledge weak evidence?

---

# Online Evaluation

If deployed:

## User Feedback

Thumbs Up / Thumbs Down

## Follow-up Rate

How often users ask clarification questions.

## Task Completion Rate

Whether users successfully act on recommendations.

---

# Regression Testing

Fixed datasets are used to prevent quality regressions.

## Test Case 1

Moved deadline

Expected:
Newest deadline wins.

---

## Test Case 2

Completed task

Expected:
Task should not be surfaced as overdue.

---

## Test Case 3

Repeated reminders

Expected:
Task should receive higher importance.

---

## Test Case 4

UIE Proposal

Expected:
All relevant proposal events should be retrieved and summarized.

---

# Success Criteria

A successful answer:

* Retrieves relevant evidence
* Uses recent information
* Avoids stale facts
* Provides actionable guidance
* Explains reasoning
* States uncertainty when appropriate

The primary objective is trustworthiness and usefulness rather than generating the longest possible answer.
