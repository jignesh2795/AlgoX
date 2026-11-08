# PX-2026-021 — Open-weight model capability updates: Holo4, Beam and Mistral Large 4

**Research date:** 2026-11-08  
**Covered releases:** 2026-09-28 to 2026-10-29  
**Status:** validated model-release findings; capability-catalog input  
**AlgoX area:** model catalog / coding agents / multimodal perception / inference economics / open-weight availability

## Finding

Three substantial releases broaden the open-weight model set relevant to coding, long-horizon agent work and multimodal computer use. They should be cataloged with their distinct availability and evaluation limitations.

### Holo4

H Company announced [Holo4](https://huggingface.co/blog/Hcompany/holo4) on September 28. The family includes a 27B dense model and a 35B-A3B MoE model, with checkpoints offered in FP16, FP8 and GGUF formats. The design targets generalist computer-use workflows across GUIs, code, MCP and APIs. The associated post also describes Holotron4 Nano and a set of trajectories/datasets.

Catalog it as an agentic computer-use and multimodal interaction model family. Record the exact checkpoint, quantization, API/local serving route, license, supported modality and tested harness rather than assigning one family-level capability score.

### Reflection Beam 1.0

Reflection announced Beam on October 5 and released its weights on October 16 under Apache 2.0. The official [model card](https://reflection.ai/beam-model-card) describes a sparse MoE with 501B total parameters, 23B active parameters and a 1M-token context window. It is aimed at coding, reasoning and long-horizon agentic tool use. The release includes BF16, FP8 and NVFP4 variants, with an associated DFlash2 draft model.

Benchmark and token-efficiency claims in the company's announcement/model card are vendor-reported; AlgoX should require independent evaluations under pinned harness and environment configurations before ranking Beam against other models.

### Mistral Large 4

Mistral announced a public preview of [Mistral Large 4](https://mistral.ai/news/mistral-large-4/) on October 6 and released its open weights on October 29. Official documentation describes a multimodal MoE with approximately 1.05T total parameters, 52B active parameters, a 1.6B vision encoder and a 1M-token context. It supports structured outputs, function calling, document question-answering and agent/conversation APIs. The final weight release and preview are distinct release states and should be recorded separately.

## AlgoX implications

For these and future releases, track:

- exact model/checkpoint revision and release date;
- open-weight versus API-only status and license;
- total and active parameters;
- architecture (dense/MoE) and vision/audio encoders;
- input/output modalities and context limit;
- quantization and available weight formats;
- required RAM/VRAM, accelerator and serving engine;
- supported agent/tool protocols and tested harnesses;
- benchmark source, evaluator, environment and independent reproduction status.

Low active-parameter count is not a substitute for total weight storage, expert placement, KV-cache or accelerator-memory requirements. A large MoE can be expensive to host even when token-level active parameters are comparatively small.

## Decision

**ADD to the open-weight model capability catalog as candidates for evaluation.** Do not promote vendor-reported benchmark superiority to validated capability. Maintain preview and final-weight release states separately.

## Sources

- Holo4 announcement: https://huggingface.co/blog/Hcompany/holo4
- Reflection Beam announcement: https://reflection.ai/blog/introducing-beam
- Beam availability and weights: https://reflection.ai/blog/beam-is-available
- Beam model card: https://reflection.ai/beam-model-card
- Mistral Large 4 preview: https://mistral.ai/news/mistral-large-4/
- Mistral Large 4 open-weight release: https://mistral.ai/news/mistral-large-4-oss/
- Mistral model documentation: https://docs.mistral.ai/models/mistral-large-4-0
