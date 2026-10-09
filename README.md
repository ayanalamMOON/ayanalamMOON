<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=36BCF7&height=150&section=header&text=Ayan%20Alam&fontSize=50&fontColor=white&animation=fadeIn" alt="Header"/>

  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=24&duration=3000&pause=1000&color=36BCF7&center=true&vCenter=true&width=700&lines=B.Tech+Data+Science+Student;AI%2FML+%26+Systems+Builder;GPU+Computing+%26+Shader+Engineering;Compiler+%26+Developer+Tooling;Open+Source+Developer" alt="Typing Animation" />

  <img src="https://komarev.com/ghpvc/?username=ayanalamMOON&label=Profile%20views&color=36BCF7&style=flat" alt="Profile Views" />
</div>

---

## About

<img align="right" alt="Coding Animation" width="350" src="https://cdn.dribbble.com/users/1162077/screenshots/3848914/programmer.gif">

I’m a B.Tech Data Science student building systems at the intersection of **AI/ML, systems engineering, and developer tooling**. My current work spans **hardware-aware neural architecture search**, **agentic WebGPU/WGSL shader generation and profiling** with Shader Alchemist, **developer-memory infrastructure** with Cortexta, and **backend systems** with Go and Rust. I’m especially interested in compiler and language design, GPU computing, algorithmic optimization, and turning research ideas into reliable, measurable software.

**Contact:** [mdayanalam12a@gmail.com](mailto:mdayanalam12a@gmail.com)

<br clear="right"/>

---

## Tech Stack & Tools

<div align="center">
  <img src="https://skillicons.dev/icons?i=python,go,rust,cpp,java,js,ts,react,nodejs,docker,git,vscode,linux&theme=dark" alt="Tech Stack" />
</div>

<div align="center">
  <img src="https://github-readme-tech-stack.vercel.app/api/cards?title=AI%2FML+Tools&lineCount=2&theme=github_dark&bg=0d1117&badge=36BCF7&border=36BCF7&titleColor=36BCF7&line1=pytorch%2CPyTorch%2CFF6F61%3Btensorflow%2CTensorFlow%2CFF6F61%3Bscikit-learn%2CScikit-learn%2CF7931E%3Bpandas%2CPandas%2C150458%3B&line2=numpy%2CNumPy%2C013243%3Bmatplotlib%2CMatplotlib%2C11557c%3Bjupyter%2CJupyter%2CF37626%3Banaconda%2CAnaconda%2C44A833%3B" alt="AI/ML Tools" />
</div>

---

## GitHub Analytics

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/overview.dark.svg"/>
    <img src="./assets/overview.light.svg" alt="GitHub profile overview and contribution metrics" width="49%"/>
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/contributions.dark.svg"/>
    <img src="./assets/contributions.light.svg" alt="Contribution streaks and calendar" width="49%"/>
  </picture>
</div>

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/activity-graph.dark.svg"/>
    <img src="./assets/activity-graph.light.svg" alt="GitHub contribution activity over time" width="100%"/>
  </picture>
</div>

<details>
<summary>📊 More Detailed Stats</summary>
<br/>

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/languages.dark.svg"/>
    <img src="./assets/languages.light.svg" alt="Programming language breakdown across public repositories" width="100%"/>
  </picture>
</div>

</details>

---

## Project Portfolio

### Selected Projects

- **[Shader Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist)** — An agentic engineering workflow for WebGPU/WGSL shader synthesis, validation, GPU profiling, and iterative optimization.
- **[NeuroSwarm AutoML](https://github.com/ayanalamMOON/NeuroswarmAutoml)** — Hardware-aware neural architecture search that co-evolves model topology and hyperparameters under latency and FLOP constraints.
- **[Helios](https://github.com/ayanalamMOON/Helios)** — A Go backend framework focused on durable storage, authentication, authorization, rate limiting, background jobs, and reverse-proxy capabilities.
- **[Cortexta](https://github.com/ayanalamMOON/Cortexta)** — A local-first developer-memory runtime with semantic retrieval and context management for coding workflows.
- **[Nagari](https://github.com/ayanalamMOON/Nagari)** — A Rust-based language project exploring a Python-like authoring experience and JavaScript ecosystem interoperability.

### Architecture Gallery

These high-level diagrams are generated from the portfolio manifest and refreshed automatically.

<!-- ARCHITECTURE-GALLERY-START -->
These high-level flows are rendered from the profile portfolio manifest. Update that manifest when a project's architecture materially changes.

<details>
<summary><strong>Shader Alchemist</strong> · <a href="https://github.com/ayanalamMOON/Shader-Alchemist">repository</a></summary>

Agentic WebGPU/WGSL shader synthesis, validation, GPU profiling, and iterative refinement.

```mermaid
flowchart LR
  N0["User intent"]
  N1["Math Architect / MathSpec"]
  N2["WGSL Writer"]
  N3["WebGPU validation and profiling"]
  N4["EvalReport and artifact"]
  N0 -->|formalize| N1
  N1 -->|contract| N2
  N2 -->|candidate shader| N3
  N3 -->|evidence| N4
  N3 -. "refinement feedback" .-> N2
```

</details>

<details>
<summary><strong>NeuroSwarm AutoML</strong> · <a href="https://github.com/ayanalamMOON/NeuroswarmAutoml">repository</a></summary>

Hardware-aware bi-level co-evolution of network topology and continuous hyperparameters.

```mermaid
flowchart LR
  N0["Search controller"]
  N1["Topology GA"]
  N2["Hyperparameter PSO-DE"]
  N3["GP surrogate / UCB"]
  N4["Distributed training and CUDA"]
  N5["Hardware-aware fitness"]
  N6["Selection and next population"]
  N0 -->|candidate topology| N1
  N1 -->|co-evolution| N2
  N2 -->|candidate parameters| N3
  N3 -->|screen candidates| N4
  N4 -->|measured metrics| N5
  N5 -->|rank| N6
  N6 -. "next generation" .-> N1
```

</details>

<details>
<summary><strong>Helios</strong> · <a href="https://github.com/ayanalamMOON/Helios">repository</a></summary>

Go backend framework with ATLAS storage, Raft replication, gateway controls, jobs, proxying, and observability.

```mermaid
flowchart LR
  N0["Client and reverse proxy"]
  N1["Gateway: authentication, RBAC, rate limits"]
  N2["Services and job workers"]
  N3["ATLAS durable KV store"]
  N4["Raft replication"]
  N5["Metrics, logs, and traces"]
  N0 -->|request| N1
  N1 -->|authorized request| N2
  N2 -->|data operations| N3
  N3 -->|replicated state| N4
  N2 -->|telemetry| N5
```

</details>

<details>
<summary><strong>Cortexta</strong> · <a href="https://github.com/ayanalamMOON/Cortexta">repository</a></summary>

Local-first developer memory with ingestion, hybrid retrieval, temporal context, and agent-facing interfaces.

```mermaid
flowchart LR
  N0["Code and chat ingestion"]
  N1["Parsing, chunking, AST signals"]
  N2["SQLite, vector, and graph memory"]
  N3["Hybrid and temporal retrieval"]
  N4["Context compiler"]
  N5["CX-LINK, MCP, and agent APIs"]
  N0 -->|normalize| N1
  N1 -->|memory units| N2
  N2 -->|index and retrieve| N3
  N3 -->|ranked context| N4
  N4 -->|bounded envelope| N5
```

</details>

<details>
<summary><strong>Nagari</strong> · <a href="https://github.com/ayanalamMOON/Nagari">repository</a></summary>

Rust-based language and toolchain exploring Python-inspired syntax with JavaScript ecosystem interoperability.

```mermaid
flowchart LR
  N0[".nag source"]
  N1["Rust lexer and parser"]
  N2["AST and semantic analysis"]
  N3["JavaScript code generation"]
  N4["Runtime and JS ecosystem"]
  N0 -->|source text| N1
  N1 -->|tokens and AST| N2
  N2 -->|validated program| N3
  N3 -->|generated JavaScript| N4
```

</details>

<details>
<summary><strong>Aletheia</strong> · <a href="https://github.com/ayanalamMOON/aletheia">repository</a></summary>

Document perception pipeline that turns PDFs, scans, and images into structured agent-consumable information.

```mermaid
flowchart LR
  N0["PDF, image, or scan"]
  N1["Ingestion and preprocessing"]
  N2["Layout analysis and OCR"]
  N3["Table extraction and post-processing"]
  N4["Structured agent-ready output"]
  N0 -->|load| N1
  N1 -->|normalized input| N2
  N2 -->|regions and text| N3
  N3 -->|validated document model| N4
```

</details>
<!-- ARCHITECTURE-GALLERY-END -->

### Engineering Notebook

An automatically refreshed index of recent default-branch engineering activity. Entries link to source commits; the feed does not invent experiment results or performance claims. Use the [experiment write-up template](./engineering-notebook/EXPERIMENT_TEMPLATE.md) for reproducible investigations.

<!-- ENGINEERING-NOTEBOOK-START -->
Automatically indexed from the configured repositories' default branches, covering the last 60 days.

- **2026-10-09 · Change · [Shader Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist)** — [Merge branch 'main' of https://github.com/ayanalamMOON/Shader-Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist/commit/4be7bc6a674d653bef6390e958814b8fde299beb)
- **2026-10-09 · Docs · [Shader Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist)** — [updated readme](https://github.com/ayanalamMOON/Shader-Alchemist/commit/9ccf4e05a78604e1482b33255a5908fcee4b1678)
- **2026-10-09 · Docs · [Shader Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist)** — [Add Shader Alchemist README artwork](https://github.com/ayanalamMOON/Shader-Alchemist/commit/2836365b2b76d1473d1cc0412014b3995169906b)
- **2026-10-09 · Feature · [Shader Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist)** — [feat: harden WebGPU execution and expand ADK runtime integration](https://github.com/ayanalamMOON/Shader-Alchemist/commit/2f4bf325443231eb8a5678455adee43d47fbf6a2)
- **2026-10-09 · Feature · [Shader Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist)** — [feat: harden WebGPU execution and expand ADK runtime integration](https://github.com/ayanalamMOON/Shader-Alchemist/commit/4b036c76d1bf79f082ae68850d4c5ee8e602c2e8)
- **2026-10-09 · Feature · [Shader Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist)** — [feat: initial project scaffold with agent-core pipeline and WebGPU harness](https://github.com/ayanalamMOON/Shader-Alchemist/commit/f0f6e8acdc4908cf92a4e08bd5fc870a7fe31e83)
- **2026-09-21 · Change · [NeuroSwarm AutoML](https://github.com/ayanalamMOON/NeuroswarmAutoml)** — [style(context): apply Black formatting](https://github.com/ayanalamMOON/NeuroswarmAutoml/commit/8fdf1c97d3c1e2018f4b51509ff3ce8479a7abc9)
- **2026-09-21 · Feature · [NeuroSwarm AutoML](https://github.com/ayanalamMOON/NeuroswarmAutoml)** — [feat(context): add pretrained Cortexta context bridge](https://github.com/ayanalamMOON/NeuroswarmAutoml/commit/615df7b99840559ef1bfa61176887d313080b021)
- **2026-09-21 · Change · [Helios](https://github.com/ayanalamMOON/Helios)** — [Add realistic Helios retail demo application](https://github.com/ayanalamMOON/Helios/commit/6c065519e43f3c25f4d1310bc3523a085b849e4a)
- **2026-09-21 · Change · [Helios](https://github.com/ayanalamMOON/Helios)** — [Upgrade and integrate Helios command services](https://github.com/ayanalamMOON/Helios/commit/92948416c6feb69619a2af233bdcfa7d7d562158)

Labels are inferred from commit subjects and are navigation hints only. This feed does not claim that a benchmark, experiment, or correctness result passed.
<!-- ENGINEERING-NOTEBOOK-END -->

### Verified Project Health

Latest default-branch checks, release metadata, and declared licenses for the selected public repositories. Projects without configured checks are labelled accordingly rather than being marked as passing.

<!-- PROJECT-HEALTH-START -->
| Project | Latest commit checks | License | Latest release | Last push (UTC) |
|---|---|---|---|---|
| [Shader Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist) | [Not configured](https://github.com/ayanalamMOON/Shader-Alchemist/commit/4be7bc6a674d653bef6390e958814b8fde299beb/checks) | NOASSERTION | None published | 2026-10-09 |
| [NeuroSwarm AutoML](https://github.com/ayanalamMOON/NeuroswarmAutoml) | [Passing](https://github.com/ayanalamMOON/NeuroswarmAutoml/commit/8fdf1c97d3c1e2018f4b51509ff3ce8479a7abc9/checks) | MIT | [v0.2.0](https://github.com/ayanalamMOON/NeuroswarmAutoml/releases/tag/v0.2.0) | 2026-09-21 |
| [Helios](https://github.com/ayanalamMOON/Helios) | [Not configured](https://github.com/ayanalamMOON/Helios/commit/6c065519e43f3c25f4d1310bc3523a085b849e4a/checks) | MIT | [v0.1.0](https://github.com/ayanalamMOON/Helios/releases/tag/v0.1.0) | 2026-09-21 |
| [Cortexta](https://github.com/ayanalamMOON/Cortexta) | [Passing](https://github.com/ayanalamMOON/Cortexta/commit/433b5eb0836fae818dbfc8afeb933df106d61761/checks) | MIT | [v0.1.3](https://github.com/ayanalamMOON/Cortexta/releases/tag/v0.1.3) | 2026-08-11 |
| [Nagari](https://github.com/ayanalamMOON/Nagari) | [Passing](https://github.com/ayanalamMOON/Nagari/commit/7747c5ffed71830c9e8d9135c85fa023e349d320/checks) | MIT | None published | 2025-11-01 |
| [Aletheia](https://github.com/ayanalamMOON/aletheia) | [Not configured](https://github.com/ayanalamMOON/aletheia/commit/5e4fb50bc5b3e088cdb43e88c480dbbb86db9604/checks) | MIT | None published | 2026-01-28 |

<sub>Checks apply to the latest commit on each default branch. “Not configured” means GitHub reported no checks or commit statuses; it is not a passing result. Release and license values come from repository metadata.</sub>
<!-- PROJECT-HEALTH-END -->

### Recently Updated Repositories

<!-- PROJECTS-START -->
**Recently Updated Projects:**

- **[Shader-Alchemist](https://github.com/ayanalamMOON/Shader-Alchemist)** — Agentic WebGPU/WGSL shader synthesis, validation, GPU profiling, and iterative optimization.
  
  `Python` · *Updated Today* · `WebGPU` · `WGSL` · `GPU Computing`

- **[NeuroswarmAutoml](https://github.com/ayanalamMOON/NeuroswarmAutoml)** — Hardware-aware neural architecture search that co-evolves network topologies and hyperparameters under latency and FLOP constraints.
  
  `Python` · *Updated 2 weeks ago* · `AutoML` · `Neural Architecture Search`

- **[Helios](https://github.com/ayanalamMOON/Helios)** — Go backend framework with durable storage, authentication, RBAC, rate limiting, background jobs, and reverse-proxy capabilities.
  
  `Go` · *Updated 2 weeks ago* · `Go` · `Backend Systems`

- **[aletheia](https://github.com/ayanalamMOON/aletheia)** — Document perception for AI coding agents, including OCR, layout analysis, and table extraction.
  
  `Python` · *Updated 1 month ago* · `Document AI` · `Developer Tools`

- **[polyglot-app](https://github.com/ayanalamMOON/polyglot-app)** — Description not provided yet.
  
  `HTML` · *Updated 2 months ago*

- **[Cortexta](https://github.com/ayanalamMOON/Cortexta)** — Local-first developer-memory runtime with semantic retrieval and context management for coding workflows.
  
  `TypeScript` · *Updated 2 months ago* · `Developer Tools` · `Memory Runtime`

*Last updated: October 09, 2026 at 18:08 UTC*
<!-- PROJECTS-END -->

---

## Contribution Footprint

This repository-local chart ranks public repositories by recent commit activity and refreshes automatically.

<div align="center">
  <!-- Generated by .github/workflows/refresh-profile.yml -->
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/repositories.dark.svg"/>
    <img src="./assets/repositories.light.svg" alt="Top repositories ranked by contributions over the trailing year" width="100%"/>
  </picture>
</div>

---

## Connect

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=16&duration=4000&pause=1000&color=36BCF7&center=true&vCenter=true&width=300&lines=Let's+Connect!;Always+Open+to+Collaborate" alt="Connect Animation" />
</div>

<div align="center">
  <a href="https://github.com/ayanalamMOON">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white&labelColor=181717&color=36BCF7" alt="GitHub" />
  </a>
  <a href="mailto:mdayanalam12a@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white&labelColor=D14836&color=36BCF7" alt="Email" />
  </a>
</div>

<div align="center">
  <img src="https://github.com/ayanalamMOON/ayanalamMOON/blob/output/github-contribution-grid-snake-dark.svg" alt="Snake Animation" />
</div>

---

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&size=14&duration=5000&pause=2000&color=36BCF7&center=true&vCenter=true&width=400&lines=Thanks+for+visiting!;Happy+Coding!;Keep+Building+Amazing+Things!" alt="Footer Message" />
</div>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=36BCF7&height=120&section=footer&animation=fadeIn" alt="Footer Wave" />
</div>
