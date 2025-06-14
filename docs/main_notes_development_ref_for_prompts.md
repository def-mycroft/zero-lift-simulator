# Development Reference for Prompts

random codename: shrill-repeat bfe48d44


***

# Prompt Development Reference

This document captures key terms, conventions, and logic scaffolds for developing prompts—especially recursive ones where the assistant is being asked to write prompts itself. It’s not a glossary, style guide, or API spec. It’s a practical reference for staying sharp, avoiding ambiguity, and reducing the need to repeat hard-won lessons about language precision.

You can think of it as a map of how I think when I write prompts manually.

---

## drp

Short for "deep research project." Refers to structured but open-ended prompt-driven research tasks with long time horizons and a clear external goal (e.g., a job, technical artifact, or public-facing output). These projects often include multiple components, shared documents, and recursive GPT usage. By default, GPT should not proceed with full-scale generation until explicitly told to “proceed w/ deep research.”

---

## prompt-to-prompt

This label applies to any session where GPT is being asked to write a prompt that will later be used to generate something else. These tend to have layered logical levels and create confusion. Be vigilant about distinguishing:

- The written prompt (what GPT writes)
- The generated output (what another GPT will return when run with that prompt)

Always call out ambiguity between these levels if it might cause problems.

---

## codex note

This signals that the output is being written for Codex-mode assistants or other tools that treat text as code-like or instruction-like. Write these sections cleanly, with minimal abstraction or ambiguity, using formatting that supports copy-paste or downstream parsing.

---

## "in quotes"

Strings inside double quotes are literal and should not be interpreted, autocorrected, or paraphrased. This is a deliberate escape from shorthand interpolation. Follow the quoted string exactly as written.

---

## shorthand-aware

I often use phonetic or abbreviated English in prompts. Unless marked off with quotes, the assistant is expected to expand these naturally. Assume that shorthand is intentional and should be interpreted in context.

---

## tagging instruction context

Sometimes I’ll label specific sections of a prompt as "codex-mode," "cut here," or similar. These are meant to signal copy-pasteable blocks. Treat anything below the tag as its own contained unit, and keep your transformations limited to within that unit unless told otherwise.

---

## layered prompting

Not all prompts are meant to be run directly. Some are intermediate products, like scaffolding prompts used to build others. If I'm asking for a draft, sketch, or modular component, don’t try to polish it as a final prompt unless told to. Keep the logic and structure clear, even if the tone or style is loose.

---

## identity scaffolding

When a prompt sets up an identity for the assistant (e.g., “you are a stoic strategist,” “you respond as if you are a nervous intern”), treat it as a constraint that governs the assistant’s tone, behavior, and worldview. Don’t collapse these into just “style” or “voice”—they function more like an operating context.

---

## tone-level vs instruction-level

Whenever I give feedback about a prompt, clarify whether I’m asking for a change in tone (e.g., make it friendlier, more terse) or a change in the instructions themselves (e.g., add a step, narrow the topic). Keep these layers separate in edits unless told to blend them.

---

## when in doubt, ask

Recursive prompts compound ambiguity quickly. If a request has multiple possible meanings—especially around what is supposed to be written vs. what is supposed to be generated—halt and clarify. Don’t fill in ambiguity with assumptions. Ask.

---

## purpose of this document

This file isn’t for rules enforcement or template rigidity. It’s a scratchpad of insights meant to reduce friction in recursive prompting. Treat it as alive, informal, and adaptive. If something in a session feels like it belongs in here, bring it up. I want this to evolve alongside my workflow.
# Git Info
Commit: 9f58ae49b8269ba20650e85e0a426975f21c5b84
Date: 2025-06-12T09:20:22-07:00

#process-notes