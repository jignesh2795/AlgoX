# PX-2026-020 — AI toolchain supply-chain incidents: Tensorlake and LiteLLM

**Research date:** 2026-11-08  
**Incident dates:** 2026-10-08 and 2026-10-21  
**Status:** vendor advisories and incident analyses; security/provenance input  
**AlgoX area:** dependency integrity / package provenance / developer credentials / agent infrastructure / software supply chain

## Finding

Two October incidents demonstrate that AI developer and inference infrastructure can become a high-impact supply-chain target. In both cases, a package or release artifact associated with an AI toolchain was used as a credential-exfiltration path.

### Tensorlake npm package

The Tensorlake maintainers published [GitHub security advisory GHSA-8g63-53c9-65j2](https://github.com/tensorlakeai/tensorlake/security/advisories/GHSA-8g63-53c9-65j2) for an unauthorized malicious `tensorlake@0.5.144` npm release on October 8, 2026. The advisory describes a compromised maintainer account and malicious code published through the project's release workflow, affecting the package and platform-specific native packages. Sonatype's analysis describes credential collection and remote-command capability in the package's install path. The advisory identifies the affected version; users must follow the latest maintainer instructions for remediation rather than infer safety from package provenance metadata.

### LiteLLM PyPI and container release

LiteLLM's canonical [October 23 incident analysis](https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain) states that the public `litellm==1.107.0` release and specified Docker/GHCR tags were compromised on October 21. The PyPI artifacts were live for approximately two hours; compromised container tags were available for a longer interval. LiteLLM's investigation traces the attack chain to an inadvertently exposed administrative key in a public repository, followed by compromise of internal deployment and release controls. Microsoft Security independently analyzed the malicious package's Python startup-hook behavior and credential collection.

The distinction between the official source tag and the compromised distributed artifacts matters: the incident report says the official v1.107.0 source tag did not contain the malicious files, while distributed artifacts had been built from an attacker-controlled repository.

## AlgoX implications

AI infrastructure dependencies need the same provenance and release controls as application code, with additional attention to credentials and agent-accessible environments.

Recommended controls to capture in an eventual supply-chain policy:

1. Pin package versions, container digests and transitive dependencies.
2. Verify publisher identity, signatures, attestations and release provenance—but do not treat any single metadata signal as sufficient.
3. Prefer reproducible builds and compare distributed artifacts with reviewed source/tag content where feasible.
4. Restrict install/build scripts, network egress and credential visibility.
5. Use short-lived, least-privilege credentials in isolated build and agent environments.
6. Record package name/version, registry, digest, publisher identity, attestation, install time and affected workload for each execution.
7. Have a revocation/containment path for compromised releases and rotate credentials when an affected environment may have executed malicious code.

A valid signature or registry provenance statement proves only a property of the signing/publication process; it does not prove that the artifact is benign or that the publisher account was uncompromised.

## Decision

**ADOPT as security and dependency-provenance evidence.** These incidents justify explicit package/artifact lineage and isolation for agent runtimes, inference servers, MCP servers and development tools. They do not justify treating all releases of either project as compromised; scope remediation to the exact affected versions and tags described by the maintainers.

## Sources

- Tensorlake maintainer advisory: https://github.com/tensorlakeai/tensorlake/security/advisories/GHSA-8g63-53c9-65j2
- Sonatype analysis: https://www.sonatype.com/blog/hijacked-tensorlake-npm-turned-installation-into-a-credential-risk
- LiteLLM canonical incident analysis: https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain
- LiteLLM initial incident notice: https://docs.litellm.ai/blog/security-incident-oct-21-2026
- Microsoft Security analysis: https://www.microsoft.com/en-us/security/blog/2026/10/23/inside-the-litellm-1-107-0-supply-chain-compromise-credential-theft-through-python-startup-hooks/
