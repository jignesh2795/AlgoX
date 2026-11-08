# PX-2026-015 — Inference-stack evolution and multi-agent cache sharing

**Research date:** 2026-11-08  
**Covered releases:** 2026-09-28 to 2026-10-20  
**Status:** validated project and paper findings; inference-architecture input  
**AlgoX area:** inference runtime / serving / kernels / cache / accelerator portability / distributed execution

## Finding

Several developments show that inference is no longer adequately described by a single `engine` field. Runtime, kernel implementation, scheduling, parallelism, cache topology, model architecture and accelerator backend are evolving as distinct layers.

### DeepInfer

[DeepInfer](https://github.com/deepseek-ai/DeepInfer) is an Apache-2.0 inference framework released by DeepSeek in October 2026. Its README describes it as the inference framework powering DeepSeek's large-scale production services. The public release supports DeepSeek-V4.1-Flash and lists optimized kernels, attention/data parallelism, MoE expert parallelism and load balancing, speculative verification, sliding-window replay, asynchronous scheduling, batch-invariant inference, deterministic sampling and structured outputs.

The documented hardware targets are NVIDIA SM100 GPUs and Huawei Ascend 950 NPUs. Importantly, the public release explicitly says a complete service still needs a KV-cache system, prefill/decode disaggregation and load balancing across data-parallel replicas. These should not be assumed to be included merely because the framework is described as production-derived.

### vLLM 0.31.0

[vLLM v0.31.0](https://github.com/vllm-project/vllm/releases/tag/v0.31.0), released October 5, 2026, includes a large set of inference changes. Its release notes highlight DeepSeek-V4.1-Flash optimizations including FlashMLA attention with compressed NVFP4 KV cache on SM100, sparse MQA logits, fused MoE operations, and additional speculative-decoding and model support.

This is a significant ecosystem integration signal: specialized model architectures and cache formats are increasingly reflected directly in common serving engines.

### TorchNeuron

[AWS TorchNeuron](https://github.com/aws-neuron/torch-neuronx) became public beta on October 20, 2026 as an open-source native PyTorch backend for Trainium2 and Trainium3. It supports eager execution, `torch.compile`, standard PyTorch APIs and custom Neuron Kernel Interface operators. The important catalog distinction is that this is a hardware-specific PyTorch backend, not a universal inference engine.

### KVCMAS

The September 28 paper [KVCMAS: Efficient KV Cache Correction for Shared Context in Multi-Agent Systems](https://arxiv.org/abs/2609.34060) addresses redundant prefill and cache construction when prompt-specialized agents share a model and context. It uses compact low-rank correction states to account for agent-specific prefixes while chaining cache corrections through a workflow. The authors report 2.0x TTFT improvement over inference without KV sharing and up to 3.7x lower peak GPU memory than a prior cache-correction method in their evaluated setting. These are paper-reported results, not a general guarantee.

### Apple Minions

Apple's [Minions](https://machinelearning.apple.com/research/distributed-gpu-cloud) paper, submitted October 9, 2026, describes an internal dynamic virtual-GPU cloud that aggregates idle Apple Silicon GPUs across macOS devices for distributed inference. The system emphasizes task distribution, fault tolerance and reuse of otherwise idle hardware. This is an architectural case study, not a public inference service or dependency.

## AlgoX implications

The inference capability catalog should distinguish at least:

- model architecture and checkpoint;
- inference framework/runtime and exact version;
- kernel libraries and kernel/quantization path;
- scheduler and batching semantics;
- attention, tensor, context and expert parallelism;
- KV-cache representation, sharing/correction and persistence;
- prefill/decode topology and disaggregation;
- accelerator/backend and supported hardware envelope;
- determinism and structured-output guarantees;
- independently measured latency, throughput, memory and cost.

For multi-agent workloads, cache compatibility and shared-context reuse are first-class serving capabilities. Cache performance must be evaluated together with correctness, isolation between agent-specific prefixes, concurrency and memory pressure.

## Decision

**ADOPT as a capability-catalog and inference-evaluation requirement.** DeepInfer, vLLM and TorchNeuron belong in the runtime/backend registry with their exact support boundaries. KVCMAS is a research reference for shared-context inference. Apple Minions is a distributed-resource architecture reference only.

## Sources

- DeepInfer: https://github.com/deepseek-ai/DeepInfer
- vLLM 0.31.0 release: https://github.com/vllm-project/vllm/releases/tag/v0.31.0
- AWS TorchNeuron announcement: https://aws.amazon.com/about-aws/whats-new/2026/10/aws-announce-native-pytorch-support-trainium/
- TorchNeuron repository: https://github.com/aws-neuron/torch-neuronx
- KVCMAS paper: https://arxiv.org/abs/2609.34060
- Apple Minions paper: https://arxiv.org/abs/2610.12970
- Apple ML Research summary: https://machinelearning.apple.com/research/distributed-gpu-cloud
