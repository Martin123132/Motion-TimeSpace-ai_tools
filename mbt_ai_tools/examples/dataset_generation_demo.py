"""Generate contradiction datasets and export to common formats."""

from pathlib import Path

from mbt_ai_tools.training.dataset_builder import build_examples, export_jsonl
from mbt_ai_tools.training.export_openai import export_openai_jsonl
from mbt_ai_tools.training.export_anthropic import export_anthropic_jsonl
from mbt_ai_tools.training.curriculum_generator import CurriculumGenerator


def main():
    out_dir = Path("./artifacts")
    out_dir.mkdir(exist_ok=True)

    examples = build_examples()
    export_jsonl(examples, out_dir / "contradictions.jsonl")
    export_openai_jsonl(examples, out_dir / "openai.jsonl")
    export_anthropic_jsonl(examples, out_dir / "anthropic.jsonl")

    curriculum = CurriculumGenerator().build(examples)
    for stage in curriculum:
        print(f"Stage: {stage.name} ({len(stage.examples)} examples)")


if __name__ == "__main__":
    main()
