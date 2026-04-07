"""Hook sections: safety check, auto-lint, stage complete, context awareness, done criteria, plan mode rules, session discipline."""
from __future__ import annotations

from ..shared import page_nav


def section_hooks_overview() -> str:
    return f"""\
<section class="section" id="hooks-overview">
{page_nav([("home", "Home"), "Hooks"], 4)}
  <h1>&#x1F9F7; Hooks</h1>
  <p class="subtitle">Runtime guardrails and automations that fire around tool use, workflow transitions, and context pressure.</p>

  <p>Hooks are not specialist agents and they are not reusable workflows. They are small runtime interventions that watch specific events and either block, warn, format, or inject guidance. Read this lane when you want to understand what Rune enforces automatically while work is running.</p>

  <h2>Use this lane</h2>
  <table>
    <thead>
      <tr><th>Topic</th><th>Open it when</th></tr>
    </thead>
    <tbody>
      <tr><td><button data-section="hook-safety-check">Safety Check</button></td><td>You want to know which destructive commands are blocked before they hit the shell.</td></tr>
      <tr><td><button data-section="hook-auto-lint">Auto-Lint</button></td><td>You want to see which formatters run automatically after writes or edits.</td></tr>
      <tr><td><button data-section="hook-stage-complete">Stage Complete</button> and <button data-section="hook-done-criteria">Done Criteria</button></td><td>You want to understand how Rune nudges workflow handoff and completion discipline.</td></tr>
      <tr><td><button data-section="hook-context-awareness">Context Awareness</button>, <button data-section="hook-plan-mode-rules">Plan Mode Rules</button>, and <button data-section="hook-session-discipline">Session Discipline</button></td><td>You want the injected guidance that keeps the active workflow and context window in view.</td></tr>
    </tbody>
  </table>

  <h2>Hook catalog</h2>
  <div class="card-grid">
    <button class="card" data-section="hook-safety-check"><span class="emoji" aria-hidden="true">&#x1F6AB;</span><h4>Safety Check</h4><p>Blocks destructive shell, git, SQL, and infra commands before execution</p></button>
    <button class="card" data-section="hook-auto-lint"><span class="emoji" aria-hidden="true">&#x2728;&#xFE0F;</span><h4>Auto-Lint</h4><p>Runs formatter commands after file writes from the project root</p></button>
    <button class="card" data-section="hook-stage-complete"><span class="emoji" aria-hidden="true">&#x1F3C1;</span><h4>Stage Complete</h4><p>Suggests the next owner or review step when workflow work finishes</p></button>
    <button class="card" data-section="hook-done-criteria"><span class="emoji" aria-hidden="true">&#x2705;</span><h4>Done Criteria</h4><p>Warns when an agent tries to stop with unresolved tracked work</p></button>
    <button class="card" data-section="hook-context-awareness"><span class="emoji" aria-hidden="true">&#x26A0;&#xFE0F;</span><h4>Context Awareness</h4><p>Injects a warning when context pressure is getting high</p></button>
    <button class="card" data-section="hook-plan-mode-rules"><span class="emoji" aria-hidden="true">&#x1F4D0;</span><h4>Plan Mode Rules</h4><p>Injects planning discipline while the active workflow is in plan mode</p></button>
    <button class="card" data-section="hook-session-discipline"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Session Discipline</h4><p>Keeps the active workflow and ticket visible in ongoing turns</p></button>
  </div>
</section>
"""


def section_hook_safety_check() -> str:
    return f"""\
<section class="section" id="hook-safety-check">
{page_nav([("home", "Home"), ("hooks-overview", "Hooks"), "Safety Check"], 4)}
  <h1>&#x1F6AB; Safety Check Hook</h1>
  <p class="subtitle">Regex-based command filter. Intercepts Bash commands before execution and blocks known destructive patterns.</p>

  <p>The <code>safety-check.py</code> hook runs as a <code>PreToolUse</code> hook. When the AI agent requests a shell command, the host fires an event before execution. The hook evaluates the command against patterns in <code>safety-patterns.yaml</code> and either blocks or allows it. The runtime binding itself is declared in <code>src/rune-agency/hooks-meta.yaml</code> and enabled through profile hook lists.</p>

  <table>
    <thead>
      <tr><th>At a glance</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Event</strong></td><td><code>PreToolUse</code> with Bash matcher</td></tr>
      <tr><td><strong>Script</strong></td><td><code>src/rune-agency/hooks/core/safety-check.py</code></td></tr>
      <tr><td><strong>Config</strong></td><td><code>src/rune-agency/hooks/core/safety-patterns.yaml</code></td></tr>
      <tr><td><strong>Result</strong></td><td>Either returns a deny response JSON or exits cleanly and lets the command run</td></tr>
    </tbody>
  </table>

  <h3>How it works</h3>
  <pre><code>Agent requests a Bash command
  &rarr; Host fires PreToolUse event
    &rarr; safety-check.py receives the command string
      &rarr; Evaluates against patterns in safety-patterns.yaml
        &rarr; MATCH: return deny &mdash; command never reaches the shell
        &rarr; NO MATCH: exit 0 &mdash; command executes normally</code></pre>

  <h3>Properties</h3>
  <table>
    <thead>
      <tr><th>Property</th><th>Behavior</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Synchronous</strong></td><td>Blocks until the check finishes. The command cannot race past it.</td></tr>
      <tr><td><strong>Stateless</strong></td><td>Each command is evaluated independently. No session state.</td></tr>
      <tr><td><strong>Fail-open</strong></td><td>If the config is missing, all commands pass. A broken config does not lock you out.</td></tr>
      <tr><td><strong>Zero dependencies</strong></td><td>Includes a minimal YAML parser when PyYAML is unavailable.</td></tr>
    </tbody>
  </table>

  <h2>Blocked patterns</h2>
  <p>Patterns are configured in <code>src/rune-agency/hooks/core/safety-patterns.yaml</code>. The current file mixes built-in checks, regex checks, and optional <code>requires</code> clauses for compound matches.</p>

  <h3>Destructive file operations</h3>
  <table>
    <thead>
      <tr><th>Pattern</th><th>Catches</th><th>Severity</th></tr>
    </thead>
    <tbody>
      <tr><td><code>rm-recursive-force</code></td><td><code>rm -rf</code>, <code>rm -fr</code>, <code>rm -r -f</code>, <code>rm --recursive --force</code>, and other mixed flag orderings</td><td>Block</td></tr>
    </tbody>
  </table>

  <h3>Destructive SQL</h3>
  <table>
    <thead>
      <tr><th>Pattern</th><th>Catches</th><th>Severity</th></tr>
    </thead>
    <tbody>
      <tr><td><code>drop-table</code></td><td><code>DROP TABLE</code> (case-insensitive)</td><td>Block</td></tr>
      <tr><td><code>drop-database</code></td><td><code>DROP DATABASE</code></td><td>Block</td></tr>
      <tr><td><code>delete-from</code></td><td><code>DELETE FROM</code></td><td>Block</td></tr>
      <tr><td><code>truncate</code></td><td><code>TRUNCATE</code></td><td>Block</td></tr>
    </tbody>
  </table>

  <h3>Destructive Git</h3>
  <table>
    <thead>
      <tr><th>Pattern</th><th>Catches</th><th>Severity</th></tr>
    </thead>
    <tbody>
      <tr><td><code>git-force-push</code></td><td><code>git push --force</code>, while still allowing <code>--force-with-lease</code></td><td>Block</td></tr>
      <tr><td><code>git-reset-hard</code></td><td><code>git reset --hard</code></td><td>Block</td></tr>
      <tr><td><code>git-clean</code></td><td><code>git clean -f</code></td><td>Block</td></tr>
      <tr><td><code>git-checkout-dot</code></td><td><code>git checkout .</code></td><td>Block</td></tr>
      <tr><td><code>git-restore-dot</code></td><td><code>git restore .</code></td><td>Block</td></tr>
      <tr><td><code>git-branch-force-delete</code></td><td><code>git branch -D</code></td><td>Block</td></tr>
    </tbody>
  </table>

  <h3>Infrastructure</h3>
  <table>
    <thead>
      <tr><th>Pattern</th><th>Catches</th><th>Severity</th></tr>
    </thead>
    <tbody>
      <tr><td><code>terraform-production-apply</code></td><td><code>terraform apply</code> or <code>terragrunt apply</code> combined with production keywords such as <code>prod</code>, <code>production</code>, or <code>live</code></td><td>Block</td></tr>
      <tr><td><code>terraform-destroy</code></td><td><code>terraform destroy</code> or <code>terragrunt destroy</code></td><td>Block</td></tr>
    </tbody>
  </table>

  <h3>Shell indirection</h3>
  <table>
    <thead>
      <tr><th>Pattern</th><th>Catches</th><th>Severity</th></tr>
    </thead>
    <tbody>
      <tr><td><code>bash-c-destructive</code></td><td>Destructive recursive-force delete hidden inside <code>bash -c</code>, <code>sh -c</code>, or <code>zsh -c</code></td><td>Block</td></tr>
      <tr><td><code>eval-destructive</code></td><td>Destructive recursive-force delete hidden inside <code>eval</code></td><td>Block</td></tr>
    </tbody>
  </table>

  <h3>Authentication</h3>
  <table>
    <thead>
      <tr><th>Pattern</th><th>Catches</th><th>Severity</th></tr>
    </thead>
    <tbody>
      <tr><td><code>gcloud-auth</code></td><td><code>gcloud auth login</code> and <code>gcloud auth application-default</code></td><td>Block</td></tr>
      <tr><td><code>gh-auth</code></td><td><code>gh auth</code></td><td>Block</td></tr>
    </tbody>
  </table>

  <h2>Adding your own patterns</h2>
  <p>Open <code>src/rune-agency/hooks/core/safety-patterns.yaml</code> and add an entry. The hook supports plain regex patterns, optional case-insensitive flags, an optional <code>requires</code> regex for compound checks, and either <code>block</code> or <code>warn</code> severity.</p>

  <pre><code>- name: docker-system-prune
  match: '\\bdocker\\s+system\\s+prune\\b'
  message: "Docker system prune blocked &mdash; removes all unused data"
  severity: warn</code></pre>

  <table>
    <thead>
      <tr><th>Field</th><th>Required</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>name</code></td><td>Yes</td><td>Identifier for logs and messages</td></tr>
      <tr><td><code>match</code></td><td>Usually</td><td>Python regex matched against the command</td></tr>
      <tr><td><code>builtin</code></td><td>No</td><td>Built-in matcher name such as <code>rm_recursive_force</code></td></tr>
      <tr><td><code>flags</code></td><td>No</td><td><code>i</code> for case-insensitive matching</td></tr>
      <tr><td><code>requires</code></td><td>No</td><td>Second regex that must also match before the rule applies</td></tr>
      <tr><td><code>message</code></td><td>Yes</td><td>Shown to the user when blocked or warned</td></tr>
      <tr><td><code>severity</code></td><td>Yes</td><td><code>block</code> denies execution; <code>warn</code> writes a warning to stderr and allows the command</td></tr>
    </tbody>
  </table>

  <p>Redeploy after editing: <code class="copyable">rune profile reapply</code></p>
</section>
"""


def section_hook_auto_lint() -> str:
    return f"""\
<section class="section" id="hook-auto-lint">
{page_nav([("home", "Home"), ("hooks-overview", "Hooks"), "Auto-Lint"], 4)}
  <h1>&#x2728;&#xFE0F; Auto-Lint Hook</h1>
  <p class="subtitle">Automatic formatting after file writes. Keeps code clean without manual intervention.</p>

  <p>The <code>auto-lint.py</code> hook runs as a <code>PostToolUse</code> hook. After the AI agent writes or edits a file, the hook checks the file extension against rules in <code>auto-lint-rules.yaml</code> and runs the matching formatters from the active project root.</p>

  <table>
    <thead>
      <tr><th>At a glance</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Event</strong></td><td><code>PostToolUse</code> with <code>Write|Edit</code> matcher</td></tr>
      <tr><td><strong>Script</strong></td><td><code>src/rune-agency/hooks/build/auto-lint.py</code></td></tr>
      <tr><td><strong>Config</strong></td><td><code>src/rune-agency/hooks/build/auto-lint-rules.yaml</code></td></tr>
      <tr><td><strong>Behavior</strong></td><td>Matches by file extension, resolves file paths relative to the project root, applies optional project conditions, then runs formatter commands in order</td></tr>
    </tbody>
  </table>

  <h3>How it works</h3>
  <pre><code>Agent writes or edits a file
  &rarr; Host fires PostToolUse event
    &rarr; auto-lint.py receives the file path
      &rarr; Matches extension against auto-lint-rules.yaml
        &rarr; MATCH: runs the formatter commands in order
        &rarr; NO MATCH: no action</code></pre>

  <h2>Default rules</h2>
  <table>
    <thead>
      <tr><th>Extension</th><th>Commands</th><th>Condition</th></tr>
    </thead>
    <tbody>
      <tr><td><code>.py</code></td><td><code>ruff check --fix</code>, <code>ruff format</code></td><td>&mdash;</td></tr>
      <tr><td><code>.sql</code></td><td><code>sqlfluff fix --force</code></td><td><code>dbt/dbt_project.yml</code> exists</td></tr>
      <tr><td><code>.sqlx</code></td><td><code>sqlfluff fix --force</code></td><td><code>dbt/dbt_project.yml</code> exists</td></tr>
      <tr><td><code>.go</code></td><td><code>goimports -w</code></td><td>&mdash;</td></tr>
      <tr><td><code>.tf</code></td><td><code>terraform fmt</code></td><td>&mdash;</td></tr>
    </tbody>
  </table>

  <p>If a command is not found on <code>PATH</code>, it is silently skipped. This makes the hook safe to deploy even when not every formatter is installed on the machine.</p>

  <h2>Adding your own rules</h2>
  <p>Open <code>src/rune-agency/hooks/build/auto-lint-rules.yaml</code> and add a rule. Extensions match exactly, commands run sequentially, and <code>condition</code> is checked relative to the project root.</p>

  <pre><code>- extension: ts
  commands:
    - "prettier --write {{file}}"
  timeout: 10</code></pre>

  <table>
    <thead>
      <tr><th>Field</th><th>Required</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>extension</code></td><td>Yes</td><td>File extension without the dot</td></tr>
      <tr><td><code>commands</code></td><td>Yes</td><td>List of commands. Use <code>{{file}}</code> as the placeholder for the file path.</td></tr>
      <tr><td><code>timeout</code></td><td>No</td><td>Maximum seconds per command. Defaults to 10.</td></tr>
      <tr><td><code>condition</code></td><td>No</td><td>Only run the rule if this file exists relative to the project root</td></tr>
    </tbody>
  </table>

  <p>Redeploy after editing: <code class="copyable">rune profile reapply</code></p>
</section>
"""


def section_hook_stage_complete() -> str:
    return f"""\
<section class="section" id="hook-stage-complete">
{page_nav([("home", "Home"), ("hooks-overview", "Hooks"), "Stage Complete"], 4)}
  <h1>&#x1F3C1; Stage Complete Hook</h1>
  <p class="subtitle">Pipeline stage guidance. Suggests the next step when a subagent finishes.</p>

  <p>The <code>on-stage-complete.py</code> hook runs as a <code>SubagentStop</code> / <code>Stop</code> hook. When an agent finishes work, this hook reads the workflow state file and suggests the next owner or review step.</p>

  <table>
    <thead>
      <tr><th>At a glance</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Events</strong></td><td><code>SubagentStop</code> and <code>Stop</code></td></tr>
      <tr><td><strong>Script</strong></td><td><code>src/rune-agency/hooks/core/on-stage-complete.py</code></td></tr>
      <tr><td><strong>State source</strong></td><td><code>.rune/session-state.json</code></td></tr>
      <tr><td><strong>Behavior</strong></td><td>Prints workflow guidance to stdout when a workflow is active</td></tr>
    </tbody>
  </table>

  <h3>How it works</h3>
  <pre><code>Subagent completes a task
  &rarr; Host fires SubagentStop event
    &rarr; on-stage-complete.py reads .rune/session-state.json
      &rarr; FILE EXISTS: prints workflow stage, ticket, mode, and suggested next owner
      &rarr; NO FILE: prints "No active workflow"</code></pre>

  <h2>The session state file</h2>
  <p>The hook reads a lightweight workflow snapshot from <code>.rune/session-state.json</code>. The current implementation looks for fields like these:</p>

  <pre><code>{{
  "workflow": "feature-implementation",
  "current_stage": "build",
  "current_wave": 2,
  "ticket": "RUNE-123",
  "autonomy_mode": "interactive",
  "next_agent": "judge"
}}</code></pre>

  <table>
    <thead>
      <tr><th>Field</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>workflow</code></td><td>Name of the active workflow</td></tr>
      <tr><td><code>current_stage</code></td><td>Current workflow stage</td></tr>
      <tr><td><code>current_wave</code></td><td>Current execution wave inside the build stage</td></tr>
      <tr><td><code>ticket</code></td><td>Task or ticket identifier shown in guidance output</td></tr>
      <tr><td><code>autonomy_mode</code></td><td>Current workflow autonomy setting</td></tr>
      <tr><td><code>next_agent</code></td><td>Suggested next specialist, if one is known</td></tr>
    </tbody>
  </table>

  <h2>Example output</h2>
  <pre><code>[workflow] Active: feature-implementation | stage: build | wave: 2 | ticket: RUNE-123 | mode: interactive
[workflow] Suggested next owner: judge for "RUNE-123".</code></pre>

  <p>This hook is informational only &mdash; it suggests but does not enforce. If there is no active workflow, it prints a generic <code>No active workflow.</code> message and exits.</p>
</section>
"""


def section_hook_context_awareness() -> str:
    return f"""\
<section class="section" id="hook-context-awareness">
{page_nav([("home", "Home"), ("hooks-overview", "Hooks"), "Context Awareness"], 4)}
  <h1>&#x26A0;&#xFE0F; Context Awareness Hook</h1>
  <p class="subtitle">Notification hook &mdash; warns when context pressure is high.</p>

  <p>The <code>context-awareness.py</code> hook runs as a <code>Notification</code> hook. It monitors context window usage and warns the agent when the window is filling up (80%+).</p>

  <table>
    <thead>
      <tr><th>At a glance</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Event</strong></td><td><code>Notification</code></td></tr>
      <tr><td><strong>Script</strong></td><td><code>src/rune-agency/hooks/core/context-awareness.py</code></td></tr>
      <tr><td><strong>Trigger</strong></td><td>Active workflow state exists and <code>context_window.used_percentage</code> is 80 or above</td></tr>
      <tr><td><strong>Result</strong></td><td>Returns JSON with <code>decision: continue</code> and additional warning context</td></tr>
    </tbody>
  </table>

  <h3>How it works</h3>
  <pre><code>Notification event fires
  &rarr; context-awareness.py reads session state
    &rarr; STATE EXISTS: reads context_window.used_percentage from event payload
      &rarr; 80% OR ABOVE: injects context warning into additionalContext</code></pre>

  <h2>What it injects</h2>
  <p>When the threshold is crossed, the hook returns a small JSON payload rather than plain text. The message is intentionally short so it reduces further context growth instead of making the problem worse.</p>

  <pre><code>{{
  "decision": "continue",
  "additionalContext": "[workflow] Context warning: 83% used. Prefer summaries, finish the current task, and avoid loading broad new context."
}}</code></pre>

  <p>If no workflow is active, or the usage stays below the threshold, the hook stays silent.</p>
</section>
"""


def section_hook_done_criteria() -> str:
    return f"""\
<section class="section" id="hook-done-criteria">
{page_nav([("home", "Home"), ("hooks-overview", "Hooks"), "Done Criteria"], 4)}
  <h1>&#x2705; Done Criteria Hook</h1>
  <p class="subtitle">Remind Claude to verify completion evidence before stopping.</p>

  <p>The <code>done-criteria.py</code> hook runs as a <code>SubagentStop</code> / <code>Stop</code> hook. If the agent tries to stop while unresolved tasks remain in the active DAG, the hook injects a reminder to verify completion.</p>

  <table>
    <thead>
      <tr><th>At a glance</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Events</strong></td><td><code>SubagentStop</code> and <code>Stop</code></td></tr>
      <tr><td><strong>Script</strong></td><td><code>src/rune-agency/hooks/validate/done-criteria.py</code></td></tr>
      <tr><td><strong>State source</strong></td><td><code>.rune/session-state.json</code> with a <code>tasks</code> list</td></tr>
      <tr><td><strong>Goal</strong></td><td>Prevent premature “done” claims when tracked work is still pending, running, or blocked</td></tr>
    </tbody>
  </table>

  <h3>How it works</h3>
  <pre><code>Agent attempts to stop
  &rarr; Host fires Stop or SubagentStop event
    &rarr; done-criteria.py reads .rune/session-state.json
      &rarr; UNRESOLVED TASKS: prints a completion warning with task IDs
      &rarr; ALL TASKS RESOLVED: prints a reminder to verify tests and docs</code></pre>

  <h2>What counts as unresolved</h2>
  <p>The hook looks at the <code>tasks</code> array in workflow state and treats these statuses as unfinished: <code>pending</code>, <code>running</code>, and <code>blocked</code>.</p>

  <pre><code>{{
  "tasks": [
    {{"id": "t1", "status": "completed"}},
    {{"id": "t2", "status": "running"}},
    {{"id": "t3", "status": "blocked"}}
  ]
}}</code></pre>

  <h2>Example output</h2>
  <pre><code>[workflow] Completion check: unresolved tasks remain (t2, t3). Do not present the workflow as complete without fresh verification.</code></pre>
</section>
"""


def section_hook_plan_mode_rules() -> str:
    return f"""\
<section class="section" id="hook-plan-mode-rules">
{page_nav([("home", "Home"), ("hooks-overview", "Hooks"), "Plan Mode Rules"], 4)}
  <h1>&#x1F4D0; Plan Mode Rules Hook</h1>
  <p class="subtitle">Reinforce planning rules during active workflow planning.</p>

  <p>The <code>plan-mode-rules.py</code> hook runs as a <code>Notification</code> hook. When the active pipeline stage is <code>plan</code>, it injects additional guidance on DAG construction and task decomposition.</p>

  <table>
    <thead>
      <tr><th>At a glance</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Event</strong></td><td><code>Notification</code></td></tr>
      <tr><td><strong>Script</strong></td><td><code>src/rune-agency/hooks/plan/plan-mode-rules.py</code></td></tr>
      <tr><td><strong>Trigger</strong></td><td><code>.rune/session-state.json</code> exists and <code>current_stage</code> is <code>plan</code></td></tr>
      <tr><td><strong>Result</strong></td><td>Injects concise planning guidance into <code>additionalContext</code></td></tr>
    </tbody>
  </table>

  <h3>What it injects</h3>
  <p>The current hook adds a short checklist that keeps planning sessions grounded in evidence and explicit deliverables.</p>

  <pre><code>[plan] Planning rules:
- include explicit verification steps
- include completion criteria
- align the plan with the current ticket and workflow boundaries
- do not claim a phase is complete without fresh evidence</code></pre>

  <p>If the workflow is not in the plan stage, the hook exits without adding anything.</p>
</section>
"""


def section_hook_session_discipline() -> str:
    return f"""\
<section class="section" id="hook-session-discipline">
{page_nav([("home", "Home"), ("hooks-overview", "Hooks"), "Session Discipline"], 4)}
  <h1>&#x1F9ED; Session Discipline Hook</h1>
  <p class="subtitle">Inject Claude workflow discipline when a workflow is active.</p>

  <p>The <code>session-discipline.py</code> hook runs as a <code>Notification</code> hook. It ensures the agent maintains the Four-Phase Model structure by injecting the current workflow state into every turn.</p>

  <table>
    <thead>
      <tr><th>At a glance</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Event</strong></td><td><code>Notification</code></td></tr>
      <tr><td><strong>Script</strong></td><td><code>src/rune-agency/hooks/core/session-discipline.py</code></td></tr>
      <tr><td><strong>State source</strong></td><td><code>.rune/session-state.json</code></td></tr>
      <tr><td><strong>Purpose</strong></td><td>Keep the active workflow, stage, and ticket visible while work is in progress</td></tr>
    </tbody>
  </table>

  <h3>What it injects</h3>
  <p>The hook emits JSON with <code>decision: continue</code> and a compact workflow reminder. This gives the assistant just enough context to stay in scope without restating the whole plan every turn.</p>

  <pre><code>{{
  "decision": "continue",
  "additionalContext": "[workflow] Active: feature-implementation | stage: build | ticket: RUNE-123\n[workflow] Stay within the active task scope, verify before claiming done, and hand off to the next agent explicitly."
}}</code></pre>

  <p>If there is no active workflow state file, the hook exits silently.</p>
</section>
"""


def build_hooks() -> str:
    return (
        section_hooks_overview()
        + section_hook_safety_check()
        + section_hook_auto_lint()
        + section_hook_stage_complete()
        + section_hook_context_awareness()
        + section_hook_done_criteria()
        + section_hook_plan_mode_rules()
        + section_hook_session_discipline()
    )
