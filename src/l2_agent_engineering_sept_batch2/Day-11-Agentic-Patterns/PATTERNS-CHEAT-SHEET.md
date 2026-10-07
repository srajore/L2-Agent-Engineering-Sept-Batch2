# Day 11 Cheat Sheet — Four Patterns, One Question

Every pattern answers the same question: **who decides what happens next?**

Our one problem for the whole day: an **IT helpdesk ticket** arrives ("My VPN is disconnected").

## The ladder (learn them in this order)

| Step | Pattern | Think of it as | Shape | The ticket example |
| --- | --- | --- | --- | --- |
| 1 | **Fixed pipeline** | Assembly line | `receive → reply → close` | Every ticket gets the same 3 steps |
| 2 | **Router** | Hospital reception | `router → network OR account` | Model reads the ticket, sends it to ONE specialist |
| 3 | **Planner-executor** | Architect, then builder | `plan → do the action` | Model picks ONE action from an allowed list, then it runs |
| 4 | **Evaluator-optimizer** | Writer + editor | `draft → check → fix once` | Model drafts a reply, judges PASS/FAIL, fixes at most once |

Why a ladder? Each step only adds ONE new idea:

1. Fixed pipeline: nothing to decide.
2. Router: *which* path?
3. Planner-executor: *what* to do, before doing it.
4. Evaluator-optimizer: *was it good enough?*

## Workflow vs agent (the one rule)

- **Workflow:** the path is fixed. The model may write text, but it never changes the next node.
- **Agent:** the model's output picks the next node (`add_conditional_edges`).

Patterns 2, 3 and 4 in our files are all agents. Pattern 1 becomes one the moment it gets a real choice.

## Which pattern do I pick?

| If the task is... | Use |
| --- | --- |
| Same steps every time | Fixed pipeline |
| Different requests need different handling | Router |
| Needs a plan before acting, and the plan must be limited | Planner-executor |
| Output quality matters and can be checked | Evaluator-optimizer |

## Trade-offs (complexity, reliability, control)

| Pattern | Model calls | Complexity | Main way it fails | Who controls the next step |
| --- | --- | --- | --- | --- |
| Fixed pipeline | 0 or more | Lowest | Can't handle a case it wasn't built for | Developer |
| Router | 1 to route | Low | Model picks the wrong specialist | Model, from 2 allowed branches |
| Planner-executor | 1 to plan | Medium | Model picks a bad action (so the allowed list must be small) | Model, from a fixed action list |
| Evaluator-optimizer | 2 to 3 (draft, judge, maybe revise) | Medium | Judge is wrong, or the revision is still bad | Model's PASS/FAIL |

The pattern: **more model control means more flexibility, but also more ways to be wrong.** That is why every model output here is checked against an allowed list, with a safe default.

## Names to know (no code today)

- **Reflection:** the model critiques its own draft. It can improve style, but it does not prove the answer is true.
- **Verifier:** checks against independent evidence (tests, schemas, facts). It gives a stronger guarantee than reflection.
  Our evaluator-optimizer sits in between: the judge is a model, so it is closer to reflection. Swapping it for a real check (like "does the text contain KB-?") would make it a verifier.

## Multi-agent overview (no code today)

```
          +--> Network agent --+
Request -> Orchestrator        +--> Combined answer
          +--> Account agent --+
```

- Several specialist agents, plus an orchestrator that hands work out and collects results.
- Our router is the simplest start: one orchestrator choosing ONE specialist.
- Every extra agent is an extra handoff that can fail, so **more agents is not automatically better**. Use one agent until the task clearly needs specialists.

## Lab: same problem, two patterns, then compare

Problem for both: the ticket **"My VPN is disconnected"**.

1. Run the router: `uv run python Day-11-Agentic-Patterns\pattern-2-router.py`
2. Run the evaluator-optimizer: `uv run python Day-11-Agentic-Patterns\pattern-4-evaluator-optimizer.py`
3. Fill in this table from what you saw:

| | Router | Evaluator-optimizer |
| --- | --- | --- |
| Model calls per run | | |
| Nodes in the graph | | |
| Complexity (simple / medium / high) | | |
| Reliability: what is the main way it can go wrong? | | |
| Control: who decides the next step? | | |

The evaluator-optimizer will usually print "Inside revise_draft": the first draft rarely contains a "KB-" citation, so the judge says FAIL and the draft is revised once.

Note: these two files use the small local `llama3.2:3b`, so the router can occasionally pick the wrong specialist. Run it a few times and count. That is the *reliability* row of your table.

4. Write 3 sentences: which pattern is simpler, which is more reliable for this ticket, and which gives you more control.

## File map

| File | Pattern |
| --- | --- |
| `pattern-1-pipeline-gains-a-choice.py` | 1 (becomes a decision point, see its docstring) |
| `pattern-2-router.py` | 2 Router (the graded file, renamed from example.py) |
| `pattern-3-planner-executor.py` | 3 |
| `pattern-4-evaluator-optimizer.py` | 4 |
