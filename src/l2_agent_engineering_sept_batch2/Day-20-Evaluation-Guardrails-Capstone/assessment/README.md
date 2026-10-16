# Assessment Materials

This folder holds the capstone brief, the scoring guide, and the golden test cases. It has no code of its own: the capstone runs Day 20's `example.py` (three guardrail layers, one agent response, and an LLM-judge evaluation over a small test set).

Run it from the repository root (Windows Command Prompt):

```cmd
uv sync
ollama signin
uv run python Day-20-Evaluation-Guardrails-Capstone\example.py
```

Use `final-capstone.md` and `rubric.md` for the final learner presentation, and `golden-cases.json` for the five expected outcomes (four match the starter `CASES`; the fifth, the `malware` training question, is the false positive learners add and see FAIL).
