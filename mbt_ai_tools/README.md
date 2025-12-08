# mbt_ai_tools

Modernized tools extracted from the MBT repository focused on contradiction
detection, recursive AGI loops, multi-agent simulation, and identity stability.

## Installation

```bash
pip install -e .
```

The package targets Python 3.10+.

## Quickstart

Run a contradiction detection demo:

```bash
python -m mbt_ai_tools.examples.contradiction_demo
```

Execute the recursive loop on sample claims:

```bash
python -m mbt_ai_tools.examples.recursive_loop_demo
```

Generate datasets and exports:

```bash
python -m mbt_ai_tools.examples.dataset_generation_demo
```

## Components

- `contradiction`: rule-based contradiction detector with evaluator and taxonomy.
- `recursive_agi`: symbolic core, neural observer, and loop orchestrator plus benchmarking tools.
- `multi_agent`: lightweight agents, world simulation, and evolutionary helpers.
- `identity`: self-model representation and invariance detection utilities.
- `training`: dataset builders, curriculum generator, and exporters for OpenAI/Anthropic fine-tuning.
- `examples`: runnable scripts demonstrating each subsystem.

## Examples

The `examples/` directory provides end-to-end runnable scripts illustrating the
core capabilities. Generated datasets are written to `./artifacts/` by default
and include JSONL files compatible with both OpenAI and Anthropic fine-tuning
pipelines.
