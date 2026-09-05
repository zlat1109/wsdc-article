---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when the user wants to stress-test a plan, get grilled on their design, says "grill me", or needs 10-15 clarifying questions before starting work.
metadata:
  origin: RobMitt/grill-me-skill (adapted for Cursor)
---

# Grill Me

Interview the user relentlessly about every aspect of their plan until you reach shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

## How to ask questions

Use the **AskQuestion tool** for every question when it is available. Never pose questions as plain text when AskQuestion is available — use multiple-choice so the user can select quickly or pick "Other" for a custom answer.

If AskQuestion is not available, ask **one question at a time** in plain text and wait for the answer.

Ask **one question at a time**. Wait for the user's answer before moving to the next question.

For each question, provide 2–4 concrete multiple-choice options representing the most likely answers or directions. Generic options like "Yes" / "No" are only for genuinely binary questions.

## Flow

1. After receiving an answer, briefly acknowledge the decision (1–2 sentences max), then immediately ask the next question.
2. If a question can be answered by exploring the codebase or files, explore them yourself instead of asking the user.
3. Continue until all branches of the design tree are resolved (typically 10–20 questions for a focused task; more for fuzzy or large scope).
4. When finished, provide a concise summary of all decisions made — then proceed to execution only if the user asks.

## Do not

- Start building, writing, or executing before the interview is complete.
- Bundle multiple questions in one turn.
- Skip branches — resolve dependencies depth-first.
