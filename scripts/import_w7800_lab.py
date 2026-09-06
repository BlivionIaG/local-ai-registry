#!/usr/bin/env python3
"""Import par1-cs13 2× W7800 48GB lab evidence as candidate recipes.

Reads LocalMaxxing/registry-data/w7800-local-ai-registry/. Writes hardware,
missing model-instances, recipes, and speed-sweeps. launch.kind is reference;
status stays candidate. Then:

    python3 scripts/format_registry.py
    python3 scripts/curate_registry.py --index-only
    python3 scripts/format_registry.py
    python3 scripts/validate_registry.py
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REG = Path(__file__).resolve().parent.parent / "registry"
PKG = Path(__file__).resolve().parents[2] / "registry-data" / "w7800-local-ai-registry"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
HW = "radeon-pro-w7800-48gb"
AMD = "https://www.amd.com/en/products/graphics/workstations/radeon-pro/w7800-48gb.html"
SRC = {
    "captured_at": NOW,
    "kind": "lab-measurement",
    "url": "https://github.com/0xSero/local-ai-registry",
    "publisher": "par1-cs13",
}
VENDOR = {
    "captured_at": NOW,
    "kind": "vendor",
    "publisher": "AMD",
    "url": AMD,
}

# slug -> (stock instance, mtp instance)
INSTANCES = {
    "qwen36-27b-q4-k-m": ("unsloth-qwen3-6-27b-gguf--q4-k-m", "unsloth-qwen3-6-27b-mtp-gguf--q4-k-m"),
    "qwen36-27b-q4-k-s": ("unsloth-qwen3-6-27b-gguf--q4-k-s", "unsloth-qwen3-6-27b-mtp-gguf--q4-k-s"),
    "qwen36-27b-q4-k-xl": ("unsloth-qwen3-6-27b-gguf--ud-q4-k-xl", "unsloth-qwen3-6-27b-mtp-gguf--ud-q4-k-xl"),
    "qwen36-27b-q6-k": ("unsloth-qwen3-6-27b-gguf--q6-k", "unsloth-qwen3-6-27b-mtp-gguf--q6-k"),
    "qwen36-27b-iq4-xs": ("unsloth-qwen3-6-27b-gguf--iq4-xs", "unsloth-qwen3-6-27b-mtp-gguf--iq4-xs"),
    "qwen38-27b-ud-q4-k-m": ("unsloth-qwen3-8-27b-gguf--ud-q4-k-m", "unsloth-qwen3-8-27b-gguf--ud-q4-k-m"),
    "qwen38-27b-ud-q4-k-xl": ("unsloth-qwen3-8-27b-gguf--ud-q4-k-xl", "unsloth-qwen3-8-27b-gguf--ud-q4-k-xl"),
    "qwen38-q6": ("orcarouter-qwen3-8-27b-uncensored-gguf--q6-k", "orcarouter-qwen3-8-27b-uncensored-gguf--q6-k"),
    "qwen38-q8": ("orcarouter-qwen3-8-27b-uncensored-gguf--q8-0", "orcarouter-qwen3-8-27b-uncensored-gguf--q8-0"),
    "qwen36-35b-a3b-q4-k-m": ("unsloth-qwen3-6-35b-a3b-gguf--ud-q4-k-m", "unsloth-qwen3-6-35b-a3b-mtp-gguf--q4-k-m"),
    "qwen36-35b-a3b-q4-k-s": (
        "unsloth-qwen3-6-35b-a3b-gguf-qwen3-6-35b-a3b-ud-q4-k-s-gguf--unknown",
        "unsloth-qwen3-6-35b-a3b-mtp-gguf--q4-k-s",
    ),
    "qwen36-35b-a3b-iq4-xs": (
        "unsloth-qwen3-6-35b-a3b-gguf-qwen3-6-35b-a3b-ud-iq4-xs-gguf--iq4xs",
        "unsloth-qwen3-6-35b-a3b-mtp-gguf--ud-iq4-xs",
    ),
    "gemma4-26b-a4b-q4-k-s": (
        "unsloth-gemma-4-26b-a4b-it-gguf--ud-q4-k-s",
        "unsloth-gemma-4-26b-a4b-it-gguf--ud-q4-k-s",
    ),
    "gemma4-26b-a4b-q4-k-xl": (
        "unsloth-gemma-4-26b-a4b-it-gguf--ud-q4-k-xl",
        "unsloth-gemma-4-26b-a4b-it-gguf--ud-q4-k-xl",
    ),
    "qwen3-coder-30b-a3b-q4-k-m": (
        "unsloth-qwen3-coder-30b-a3b-instruct-gguf--q4-k-m",
        "unsloth-qwen3-coder-30b-a3b-instruct-gguf--q4-k-m",
    ),
    "ornith-q5": ("ornith-ai-ornith-1-5-35b-a3b-gguf--q5-k-m", "ornith-ai-ornith-1-5-35b-a3b-gguf--q5-k-m"),
}

CLONE_INSTANCES = [
    ("unsloth-qwen3-6-27b-gguf--q4-k-m", "unsloth-qwen3-6-27b-gguf--q6-k", "Q6_K"),
    ("unsloth-qwen3-6-27b-gguf--q4-k-m", "unsloth-qwen3-6-27b-gguf--iq4-xs", "IQ4_XS"),
    ("unsloth-qwen3-6-27b-mtp-gguf--q4-k-m", "unsloth-qwen3-6-27b-mtp-gguf--q4-k-s", "Q4_K_S"),
    ("orcarouter-qwen3-8-27b-uncensored-gguf--iq2-xxs", "orcarouter-qwen3-8-27b-uncensored-gguf--q6-k", "Q6_K"),
    ("orcarouter-qwen3-8-27b-uncensored-gguf--iq2-xxs", "orcarouter-qwen3-8-27b-uncensored-gguf--q8-0", "Q8_0"),
    ("ornith-ai-ornith-1-5-35b-a3b-gguf--q4-k-m", "ornith-ai-ornith-1-5-35b-a3b-gguf--q5-k-m", "Q5_K_M"),
    ("unsloth-gemma-4-26b-a4b-it-gguf--ud-q4-k-xl", "unsloth-gemma-4-26b-a4b-it-gguf--ud-q4-k-s", "UD-Q4_K_S"),
]


def dump(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def known(path: str) -> dict:
    return {
        "state": "known",
        "provenance": {"captured_at": NOW, "sources": [VENDOR]},
    }


def write_hardware() -> None:
    dump(
        REG / "hardware" / f"{HW}.json",
        {
            "accelerator": {"count": 1, "unit": "GPU"},
            "accelerator_backend": "amd-rocm",
            "aliases": ["radeon pro w7800", "w7800 48gb", "gfx1100 w7800"],
            "captured_at": "2026-09-06",
            "compute": {
                "architecture": "AMD RDNA 3",
                "compute_units": 70,
                "gfx": "gfx1100",
                "stats": {
                    "fp16": {
                        "dense": {
                            "provenance": {"captured_at": NOW, "sources": [VENDOR]},
                            "state": "known",
                            "unit": "tflops",
                            "value": 90.4,
                        }
                    },
                    "fp32": {
                        "dense": {
                            "provenance": {"captured_at": NOW, "sources": [VENDOR]},
                            "state": "known",
                            "unit": "tflops",
                            "value": 45.2,
                        }
                    },
                    "int4": {
                        "dense": {
                            "provenance": {"captured_at": NOW, "sources": [VENDOR]},
                            "state": "known",
                            "unit": "tflops",
                            "value": 181,
                        }
                    },
                    "int8": {
                        "dense": {
                            "provenance": {"captured_at": NOW, "sources": [VENDOR]},
                            "state": "known",
                            "unit": "tflops",
                            "value": 90.4,
                        }
                    },
                },
                "stream_processors": 4480,
            },
            "facts": {
                "accelerator.count": known("accelerator.count"),
                "compute.architecture": known("compute.architecture"),
                "compute.compute_units": known("compute.compute_units"),
                "compute.stream_processors": known("compute.stream_processors"),
                "memory.bandwidth_gb_per_s": known("memory.bandwidth_gb_per_s"),
                "memory.vram_gb": known("memory.vram_gb"),
                "memory.vram_type": known("memory.vram_type"),
            },
            "family": "radeon-pro-w7800",
            "id": HW,
            "kind": "discrete",
            "memory": {
                "bandwidth_gb_per_s": 864,
                "bus_width_bits": 384,
                "cpu_memory_gb": None,
                "vram_gb": 48,
                "vram_type": "GDDR6",
            },
            "name": "AMD Radeon PRO W7800 48GB",
            "notes": [
                "48 GB SKU. A 32 GB W7800 also exists; do not collapse them.",
                "384-bit memory bus (not 256-bit 32 GB W7800).",
                "Lab host par1-cs13 has two identical cards (hardware_count 1 or 2).",
            ],
            "product_names": ["AMD Radeon PRO W7800"],
            "products": [],
            "schema_version": "local-ai-registry/v1",
            "sources": [VENDOR],
            "vendor": "amd",
        },
    )


def clone_instance(src_id: str, new_id: str, precision: str) -> None:
    dest = REG / "model-instance" / f"{new_id}.json"
    if dest.exists():
        return
    src = json.loads((REG / "model-instance" / f"{src_id}.json").read_text())
    src["id"] = new_id
    src["weights"]["format"] = precision
    src["weights"]["precision"] = precision
    src["weights"]["size_gb"] = None
    facts = src.get("facts") or {}
    facts.pop("weights.size_gb", None)
    src["facts"] = facts
    dump(dest, src)


def recipe_and_sweep(sweep_path: Path) -> None:
    sweep = json.loads(sweep_path.read_text())
    rid = sweep["recipe_id"]
    series = "stock"
    slug = None
    if "-lemonade-" in rid:
        series = "lemonade"
    elif "-kernel-anvil-" in rid:
        series = "tuned"
    elif "-mtp-" in rid:
        series = "mtp"
    # recover organizer slug from filename prefix before hardware id
    stem = sweep_path.name.replace(f"-{HW}-", "|").split("|")[0]
    # stem is registry_stem e.g. qwen3-6-27b-q4-k-m
    # map back via ARTIFACTS registry_stem — invert INSTANCES keys via package artifacts
    artifacts = json.loads((PKG / "artifacts.json").read_text())
    for s, art in artifacts.items():
        if art["registry_stem"] == stem:
            slug = s
            break
    if slug is None or slug not in INSTANCES:
        raise SystemExit(f"unmapped sweep {sweep_path.name} stem={stem}")
    stock_id, mtp_id = INSTANCES[slug]
    instance_id = mtp_id if series == "mtp" else stock_id
    if not (REG / "model-instance" / f"{instance_id}.json").exists():
        raise SystemExit(f"missing model-instance {instance_id}")

    engines = {
        "stock": ("c060ca9", "llama-bench-pp512-tg128"),
        "lemonade": ("b1323-95ef7fc", "llama-bench-pp512-tg128"),
        "tuned": ("c060ca9+smithy", "llama-bench-pp512-tg128-ub64-q8kv"),
        "mtp": ("c060ca9", "llama-server-completion-draft-mtp"),
    }
    version, decode_mode = engines[series]
    tp = sweep.get("hardware_count") or 1
    notes = (sweep.get("source") or {}).get("notes") or ""
    rows_in = sweep.get("rows") or []
    row = rows_in[0]
    ctx = int(row.get("context_tokens") or 512)
    out_n = int(row.get("output_tokens") or 128)
    max_ctx = int((sweep.get("metrics") or {}).get("max_context_tokens") or (ctx + out_n))

    recipe = {
        "capabilities": {"chat": None, "reasoning": None, "tools": None, "vision": None},
        "description": (
            "Observed lab run on par1-cs13 (2× AMD Radeon PRO W7800 48GB, gfx1100, ROCm 7.2). "
            "Evidence for compatibility, not an executable launch contract."
        ),
        "engine": {"graph_mode": None, "name": "llama.cpp", "version": version},
        "facts": {},
        "hardware_count": tp,
        "hardware_id": HW,
        "id": rid,
        "launch": {
            "container": {
                "captured_at": NOW,
                "compose_file": None,
                "digest": None,
                "image": None,
                "reason": "reference-only-launch",
                "runtime": None,
                "source": [SRC],
                "state": "none",
            },
            "kind": "reference",
        },
        "metadata": {
            "lab": {
                "host": "par1-cs13",
                "notes": notes,
                "raw_path": (sweep.get("source") or {}).get("paths", [None])[0],
                "series": series,
            }
        },
        "model_instance_id": instance_id,
        "provenance": {"captured_at": NOW, "sources": [SRC]},
        "recipe_source": "0xsero",
        "schema_version": "local-ai-registry/v1",
        "serving": {
            "kv_cache_tokens": None,
            "max_concurrency": 1,
            "max_context_tokens": max_ctx,
            "tensor_parallel": tp,
        },
        "speed_sweep_ids": [sweep["id"]],
        "status": "candidate",
    }
    dump(REG / "recipe" / f"{rid}.json", recipe)

    metrics = {
        "concurrency": 1,
        "decode_mode": decode_mode,
        "inference_engine_version": version,
        "latest_point_at": sweep.get("measured_at"),
        "max_context_tokens": max_ctx,
        "max_prompt_tokens": ctx,
        "peak_generation_tps": sweep["metrics"]["peak_generation_tps"],
        "peak_prompt_tps": sweep["metrics"]["peak_prompt_tps"],
        "point_count": len(rows_in) or 1,
    }
    src_metrics = sweep.get("metrics") or {}
    for key in (
        "decode8k_tps",
        "decode8k_context_tokens",
        "decode32k_tps",
        "decode32k_context_tokens",
        "decode_max_context_tps",
        "decode_max_context_tokens",
    ):
        if src_metrics.get(key) is not None:
            metrics[key] = src_metrics[key]
    out_rows = []
    for r in rows_in:
        out_rows.append(
            {
                "concurrency": 1,
                "context_tokens": r.get("context_tokens"),
                "decode_tok_s": r.get("decode_tok_s"),
                "decode_tok_s_per_stream": r.get("decode_tok_s_per_stream") or r.get("decode_tok_s"),
                "output_tokens": r.get("output_tokens") or 128,
                "peak_vram_gb": None,
                "prefill_tok_s": r.get("prefill_tok_s"),
                "samples": r.get("samples") or 5,
                "status": "observed",
                "ttft_ms_p50": None,
            }
        )
    out_sweep = {
        "accepted_at": None,
        "id": sweep["id"],
        "measured_at": sweep.get("measured_at"),
        "metrics": metrics,
        "recipe_id": rid,
        "rows": out_rows,
        "schema_version": "local-ai-registry/v1",
        "source": {
            "kind": "lab-measurement",
            "host": "par1-cs13",
            "notes": notes,
            "paths": (sweep.get("source") or {}).get("paths"),
            "repository": None,
            "url": None,
        },
    }
    dump(REG / "speed-sweep" / f"{sweep['id']}.json", out_sweep)


def main() -> int:
    if not PKG.is_dir():
        raise SystemExit(f"missing package {PKG}")
    write_hardware()
    for src, dest, prec in CLONE_INSTANCES:
        clone_instance(src, dest, prec)
    sweeps = sorted((PKG / "speed-sweeps").glob("*.json"))
    for path in sweeps:
        recipe_and_sweep(path)
    print(f"wrote hardware {HW}, {len(CLONE_INSTANCES)} instances (if missing), {len(sweeps)} recipes+sweeps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
