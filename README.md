# MLOps Digester

[![check.yml](https://github.com/fmind/mlops-digester/actions/workflows/check.yml/badge.svg)](https://github.com/fmind/mlops-digester/actions/workflows/check.yml)
[![publish.yml](https://github.com/fmind/mlops-digester/actions/workflows/publish.yml/badge.svg)](https://github.com/fmind/mlops-digester/actions/workflows/publish.yml)
[![Documentation](https://img.shields.io/badge/documentation-available-brightgreen.svg)](https://fmind.github.io/mlops-digester/)
[![License](https://img.shields.io/github/license/fmind/mlops-digester)](https://github.com/fmind/mlops-digester/blob/main/LICENCE.txt)
[![Release](https://img.shields.io/github/v/release/fmind/mlops-digester)](https://github.com/fmind/mlops-digester/releases)

Let your agent digest MLOps information.

# Installation

Use the package manager [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

# Preparation

```bash
uv run logfire auth
uv run logire projects new
```

# Usage

```bash
uv run mlops-digester
```

# Notes

- Installation: https://ai.pydantic.dev/install/
  - slim install: https://ai.pydantic.dev/install/#slim-install
    - packages to install
- Troubleshooting: https://ai.pydantic.dev/troubleshooting/
  - jupyter event loop: https://ai.pydantic.dev/troubleshooting/
- Multiple agent delegation: https://ai.pydantic.dev/multi-agent-applications/
- Graph: https://ai.pydantic.dev/graph/#mermaid-diagrams
  - Super complex (similar to LangGraph), too complex for this use case

# Ideas

- Sent a digest per channel or to the user on Slack?
- Create a Slack AI Assistant: https://api.slack.com/docs/apps/ai

# Limitations

- Configuration at the distance
  - must wrap agents in function, not pydantic ai idiomatic
- Advanced foundation models features
  - e.g., Gemini 2.0 (audio, live API, ...)
- Streaming challenges: https://ai.pydantic.dev/results/#streaming-structured-responses
