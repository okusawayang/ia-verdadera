# ia-verdadera — A True AI, in Miniature

A working skeleton of a "true AI", written by an army of 10 local AI agents (roles on a single local Qwen2.5-1.5B) and supervised by Muse. Nine Python modules, pure standard library, no dependencies.

## The design: 7 pieces

1. **Training objective** — reward verifiable reasoning, not next-token prediction (`objetivo.py`)
2. **Reasoning** — generate several paths, verify them, pick the best (`razonamiento.py`)
3. **Agent, not model** — perceive, think, act, observe consequences (`agente.py`)
4. **Own goals** — a goal system with priorities (`metas.py`)
5. **Memory** — external memory + verification of each step in code (`memoria.py`)
6. **Continuous learning** — learn from experience, consolidate rules (`aprendizaje.py`)
7. **World** — a 5x5 grid world + a learned world model (`mundo.py`)

`ia_verdadera.py` ties the seven pieces into one runnable AI. `test_ia.py` tests all of it.

## Run it

```bash
python3 test_ia.py        # TODAS LAS PRUEBAS PASARON
python3 ia_verdadera.py   # thinks, walks 10 steps, reports its active goal
```

## Honest limits

- The agent is **greedy with no planning**: it wanders and did not reach the goal in 10 steps.
- The "reasoning" picks between **hand-written example candidates** — it does not generate reasoning.
- The goals are **programmer-set**, not self-chosen.
- "Learning" is a transition table + text facts; **no weights are updated** by reward.
- 6 of the 9 modules came back broken from the agents (undefined variables, invented APIs) and were rewritten by the supervisor. The full failure log is in `informe_supervisor.txt`.

This is a skeleton of the parts we understand — not a true AI. The open question is what the real bottleneck is: the small model, compute, data, or the fact that the recipe itself (own goals, continuous learning without forgetting) does not exist yet.

## The army

10 agents, one per piece + integration + tester + reviewer, all calling a local 1.5B model on port 8080. Muse supervised: reviewed, fixed, and verified. The trained 1.5B specialist (port 8081) sat this one out — it is a hyperfocus specialist, not a programmer.
