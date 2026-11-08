# PX-2026-017 — Independent evaluation and cryptographic model provenance

**Research date:** 2026-11-08  
**Covered announcements:** 2026-10-15 to 2026-10-30  
**Status:** validated governance and research-artifact findings; provenance/evaluation architecture input  
**AlgoX area:** evaluator independence / benchmark governance / model identity / cryptographic provenance / publication policy

## Finding

Two developments sharpen different parts of evaluation trust: independent access to the system being evaluated, and cryptographic evidence of which model produced an inference result.

### Anthropic and METR: deeper independent evaluator access

On October 15, Anthropic announced [employee-like access for METR](https://www.anthropic.com/news/an-update-on-independent-evaluators). The arrangement includes access to information and risk-assessment processes, together with publication rights comparable to its higher evaluator-access tier. Anthropic describes restrictions and redaction rules around sensitive information, while METR retains the ability to publish its findings and comment on redactions.

This is a notable governance design: evaluator independence is not merely a third-party API benchmark. It can require scoped access, information-handling rules, publication rights, and a transparent record of access limitations.

### FlashProve: zero-knowledge proofs of inference

[FlashProve](https://github.com/anthropics/FlashProve) is an Apache-2.0 research artifact for zero-knowledge proofs of AI inference. It allows a provider to commit to a set of model weights and generate a proof that a response came from that committed model without revealing the weights. The verifier can check proofs without access to the model weights. The repository describes a demonstration using Llama 4 Maverick at full size on a single NVIDIA H100.

The repository explicitly labels FlashProve a **research artifact that is not maintained and is not accepting contributions**. Its performance figures and supported route requirements should be treated as prototype-specific. It is not evidence that low-cost, production inference attestation is solved.

## AlgoX implications

Extend the conceptual distinction between a provider's assertion and independently verifiable evidence:

- `ModelIdentityClaim` — the model/provider identity asserted for a run.
- `ModelCommitment` — optional cryptographic commitment to a specific set of weights.
- `InferenceProof` — optional proof bound to a request/response and commitment.
- `ProofVerifierVersion` — verifier implementation and version.
- `VerificationResult` — pass, fail, or not checked.
- `EvaluatorAccessRecord` — what an independent evaluator could inspect.
- `PublicationPolicy` / `RedactionRecord` — constraints on publication and the reasons for them.

Do not make cryptographic proof a mandatory condition for every run. It should be an optional provenance-assurance mechanism, and a proof should be bound to an exact request, model commitment, proof system and verifier version.

For external evaluations, record evaluator independence, access scope, conflicts, publication rights and redactions alongside benchmark and evaluator versions.

## Decision

**ADOPT conceptually.** Independent evaluator access and cryptographic inference proof are complementary trust dimensions. AlgoX should represent them separately and preserve the distinction between a claim, an attestation, a verified proof and an independently reproduced capability result.

## Sources

- Anthropic independent evaluators: https://www.anthropic.com/news/an-update-on-independent-evaluators
- FlashProve repository: https://github.com/anthropics/FlashProve
