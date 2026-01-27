# Design Notes – Target of Understanding

## Purpose of this document

This document explains the **design intent and reasoning** behind the prototype,
bridging conceptual motivation and practical AI-safety–oriented implementation.

It is written for reviewers who want to understand _why_ certain decisions were made,
not just _how_ the code works.

---

## Core separation of responsibility

This prototype intentionally separates responsibilities into two layers:

### 1. Evaluation Boundary (Whether to Proceed)

- Determines whether the system should proceed with a normal response
- Uses a **STRUCTURE framing gate**
- If STRUCTURE is not dominant:
  - progression is delayed (NG)
  - structural reframing is suggested
- This avoids premature personalization or moral judgment

This boundary answers:

> _Is the framing adequate to proceed safely?_

---

### 2. Output Formatting Layer (How to Respond)

- Independent from the proceed decision
- Detects **HARDWARE / high-impact signals**
- Adjusts **output format only**, not semantic judgment
- Enforces:
  - text-only output
  - confirmation-first phrasing
  - non-imperative language

This layer answers:

> _Given the context, how should we express the response safely?_

---

## Why HARDWARE is not part of the evaluation boundary

High-impact domains (e.g. robotics, automation) require **output safety**
even when semantic framing is not yet sufficient.

Therefore:

- HARDWARE is treated as a **formatting concern**
- STRUCTURE remains the **proceed gate**

This mirrors real-world safety systems, where:

- approval logic
- interface constraints
  are handled by different components.

---

## Target of Understanding vs Emotion / Intent

This system does **not** label emotion or intent.

Instead, it infers multiple hypotheses about what the user is trying to understand.

Reasons:

- emotion labels risk over-assertion
- intent labels collapse uncertainty too early
- understanding-targets preserve ambiguity

The user remains the final authority over interpretation.

---

## Internal signals (non-user-facing)

The system uses internal signals only for boundary decisions:

- hypothesis distribution
- confidence softness
- repetition patterns

These are **never exposed** as claims about the user.

---

## Why the implementation is minimal

This is a **portfolio artifact**, not a production system.

Minimalism ensures:

- transparency of decision points
- inspectability by reviewers
- focus on responsibility, not performance

---

## What this design demonstrates

- Safety can be implemented through **delay**, not assertion
- Responsibility improves when _whether_ and _how_ are separated
- Structural framing is a powerful safety primitive

---

## Non-goals

- No learning or adaptation over time
- No personalization
- No behavioral optimization

These are intentionally excluded to keep responsibility boundaries clear.
