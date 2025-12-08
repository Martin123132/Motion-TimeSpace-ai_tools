
---

# **`mbt_ai_tools`**

A modern, modular toolkit providing **contradiction detection**, **recursive AGI learning loops**, **multi-agent simulation**, and **identity stability analysis**.
This package extracts the practical, engineering-ready components from the broader MBT research ecosystem and organizes them into a clean, installable Python framework.

---

## **🌐 Features at a Glance**

* **Symbolic contradiction detection engine**
  – detects negations, property mismatches, definitional violations, universals, temporal conflicts.

* **Recursive AGI learning loop**
  – a structured 9-step human–AI–symbolic co-evolution cycle.

* **Neural observer subsystem**
  – compresses symbolic repair patterns into learned embeddings.

* **Identity stability tools**
  – self-embedding tracking and invariance reporting.

* **Multi-agent simulation layer**
  – lightweight message-passing agents with evolutionary dynamics.

* **Dataset + exporter suite**
  – generates JSONL datasets for OpenAI and Anthropic fine-tuning.

* **Full runnable examples**
  – demos for contradiction detection, recursive loops, and dataset generation.

Everything is designed to be **minimal, clean, and production-ready**.

---

## **📦 Installation**

```bash
pip install -e .
```

Requires **Python 3.10+**.

---

## **🚀 Quickstart**

### **1. Run the contradiction detection demo**

```bash
python -m mbt_ai_tools.examples.contradiction_demo
```

### **2. Execute the recursive AGI loop**

```bash
python -m mbt_ai_tools.examples.recursive_loop_demo
```

### **3. Generate datasets + OpenAI/Anthropic exports**

```bash
python -m mbt_ai_tools.examples.dataset_generation_demo
```

Artifacts appear in `./artifacts/`.

---

## **📁 Package Structure**

```
mbt_ai_tools/
    contradiction/
        engine.py            # Rule-based contradiction detector
        evaluator.py         # Precision/recall evaluation tools
        taxonomy.md          # Contradiction class definitions

    recursive_agi/
        loop.py              # 9-step recursive learning engine
        mbt_symbolic_core.py # Symbolic reasoning + pattern learning
        neural_observer.py   # Neural mirror system
        benchmark.py         # Quick benchmarking helpers
        trainer.py           # Batch trainer + export of system state

    multi_agent/
        agent.py             # Lightweight agent architecture
        world.py             # Message-passing environment
        evolution.py         # Simple evolutionary algorithm

    identity/
        self_model.py        # Tracks self-embeddings over time
        invariance_detector.py  # Detects drift/stability

    training/
        dataset_builder.py   # Builds labeled contradiction datasets
        curriculum_generator.py # Staged learning curricula
        export_openai.py     # JSONL for OpenAI fine-tuning
        export_anthropic.py  # JSONL for Claude fine-tuning

    examples/
        contradiction_demo.py
        recursive_loop_demo.py
        dataset_generation_demo.py
```

---

## **🔍 Core Components**

### **1. Contradiction Detection**

A compact symbolic engine that identifies:

* direct negation
* property mismatch
* definitional violation
* universal counterexample
* temporal conflict

Useful for reasoning benchmarks, AI safety experiments, and logic pipelines.

---

### **2. Recursive AGI Loop**

Implements a structured cycle:

1. detect contradiction
2. human patch
3. symbolic learning
4. neural observation
5. neural learning
6. symbolic evolution
7. human evolution
8. neural fluency update
9. repeat

Produces stable logs and a machine-readable learning trace.

---

### **3. Neural Observer**

Learns compressed repair patterns and tracks:

* pattern confidence
* symbolic fluency
* observation counts

A minimal neural-symbolic hybrid.

---

### **4. Multi-Agent Simulation**

Agents exchange messages, evolve policies, and track internal state.

Good for:

* emergent behavior studies
* communication tests
* evolutionary training loops

---

### **5. Identity Stability**

Provides tools for analyzing:

* embedding drift
* identity consistency
* long-term stability

Used for internal model coherence experiments.

---

### **6. Training & Export**

Automatic generation of datasets and exporters:

* `contradictions.jsonl`
* OpenAI style JSONL
* Anthropic completion-format JSONL

Curriculum generator organizes data by difficulty.

---

## **🧪 Example Output**

Contradiction demo:

```
Claim demo1: Water boils at 95C
 -> Contradiction detected: property_mismatch (Boiling point differs...)
```

Recursive AGI loop:

```
System state:
{
  "loop_count": 3,
  "symbolic_evolution_count": 3,
  "neural_fluency": 0.3,
  "total_contradictions": 3
}
```

---

## **📚 Intended Use**

This package is designed for:

* reasoning systems research
* contradiction-training pipelines
* symbolic–neural hybrid AI experiments
* multi-agent simulation prototypes
* AI alignment and safety studies
* identity stability experiments

It contains **only the clean, working, engineering-ready tools**.
Theoretical and speculative MBT content belongs in separate repositories.

---

