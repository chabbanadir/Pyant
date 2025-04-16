```markdown
# PydanticAI and MCP Service Highlights

Based on the provided documentation (`pydantic.txt`):

## PydanticAI Core Concepts

*   **Agent Framework:** Built by the Pydantic team, designed to simplify building production-grade Generative AI applications in Python, aiming for a developer experience similar to FastAPI.
*   **Model-Agnostic:** Supports various LLMs (OpenAI, Anthropic, Gemini, Ollama, Groq, Mistral, Cohere, Bedrock, etc.) and allows adding custom models.
*   **Structured Data:** Leverages Pydantic for defining schemas and validating structured inputs and outputs from LLMs, ensuring consistency.
*   **Tools:** Allows defining functions (tools) that the LLM can call during its execution to retrieve information or perform actions.
*   **Dependency Injection:** Provides a system to inject data, connections, or services into system prompts, tools, and result validators, aiding testing and customization.
*   **Type Safety:** Designed to work well with static type checkers like mypy and pyright.
*   **Streaming:** Supports streaming LLM responses, including partial validation for structured data.
*   **Pydantic Graph:** Includes `pydantic-graph`, a library for defining and running complex workflows using graph-based state machines, useful for multi-agent systems.
*   **Monitoring & Debugging:** Integrates seamlessly with Pydantic Logfire for observability (tracing, debugging, performance monitoring).
*   **Evaluation:** Offers `pydantic-evals` for systematically evaluating the performance and accuracy of AI systems.
*   **Multi-Agent:** Supports building applications with multiple agents through delegation (tools calling other agents), programmatic hand-off, or graph-based control flow.
*   **Input Flexibility:** Handles various input types including text, images, audio, and documents.
*   **Agent Structure:** Conceptually, an `Agent` contains:
    *   System prompt(s): Instructions for the LLM.
    *   Function tool(s): Functions the LLM can call.
    *   Structured result type: The expected output data structure.
    *   Dependency type constraint: Defines types for injected data/services.
    *   LLM model: The default language model to use.
    *   Model Settings: Default configuration for model requests.

## MCP Service Relation

*   **Mentioned:** The documentation mentions Model Context Protocol (MCP) servers primarily in two contexts:
    *   **Agent Initialization:** The `Agent` class constructor accepts an `mcp_servers` parameter to register `MCPServer` instances.
    *   **CLI:** The PydanticAI command-line interface (`pai`) documentation notes future plans to add interaction with MCP servers.
*   **Limited Detail:** The provided text does not elaborate significantly on the specifics of the interaction between PydanticAI agents and MCP services beyond registration and potential future CLI support.
```
