# Parallel Agent Prompt Template

Use this template when dispatching each parallel agent.

```
Task tool (general-purpose, model: sonnet):
  description: "[domain]: [short goal]"
  prompt: |
    ## Problem

    [Specific problem description — what's broken, what needs investigating, or what needs building]

    ## Scope

    [Exact files, test names, or subsystem boundaries this agent owns]

    ## Context

    [Error messages, stack traces, relevant code snippets — everything the agent needs to start immediately]

    ## Constraints

    - Only modify files within your scope
    - Do NOT change code outside your domain
    - [Any additional constraints]

    ## Expected Output

    Return:
    - What you found (root cause, analysis, or implementation summary)
    - What you changed (files and description)
    - What you tested and results
    - Any concerns or open questions
```

## Tips

- Paste error messages and test names directly — don't make the agent search for them
- Be explicit about file boundaries to prevent conflicts with other parallel agents
- Include enough context that the agent can start working immediately without exploration
