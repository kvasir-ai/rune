"""Agency sections: agents, agent onboarding, skills, rules catalog."""
from __future__ import annotations

from .shared import page_nav


def section_agents(agents_html: str) -> str:
    return f"""\
<section class="section" id="agents">
{page_nav([("home", "Home"), ("agents", "Rune Agency"), "Agents"], 2)}
  <h1>&#x1F916; Agents</h1>
  <p class="subtitle">Meet the specialists Rune dispatches across Explore, Plan, Build, and Validate.</p>

  <p><strong>Read this when:</strong> you want to know who is on the team, what phase they belong to, and which specialist to reach for before you start authoring new ones.</p>
  <p><strong>What you get:</strong> the live agent catalog, grouped by phase, plus the mental model for how Rune keeps agent routing lightweight until one is actually dispatched.</p>

  <p>Each agent lives in a markdown file with lightweight routing metadata and a full system prompt. At session start, Rune only needs the small routing summary to decide when an agent should enter the work. The full prompt loads on demand when that agent is dispatched.</p>
  <p><strong>Want to create or edit an agent?</strong> Go to <button data-section="agent-onboarding">Onboarding an Agent</button> for the file template, frontmatter reference, and prompt-writing guidance.</p>

  <h2>Use the Rune Agency pages this way</h2>
  <table>
    <thead>
      <tr><th>If you need to...</th><th>Open</th></tr>
    </thead>
    <tbody>
      <tr><td>Choose the right specialist for the current bottleneck</td><td><strong>Agents</strong></td></tr>
      <tr><td>Run a repeatable workflow such as planning, auditing, or release prep</td><td><button data-section="skills">Skills</button></td></tr>
      <tr><td>Inspect the doctrine behind how Rune works</td><td><button data-section="rules-catalog">Rules</button></td></tr>
      <tr><td>Recruit or author a new specialist</td><td><button data-section="agent-onboarding">Onboarding an Agent</button></td></tr>
    </tbody>
  </table>

  <h2>How to read the catalog</h2>
  <table>
    <thead>
      <tr><th>Signal</th><th>What it tells you</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Phase pill</strong></td><td>Where the agent naturally enters the four-phase model.</td></tr>
      <tr><td><strong>Description</strong></td><td>The fastest way to see whether the agent matches the current job.</td></tr>
      <tr><td><strong>Tools row</strong></td><td>How much reach the agent has. Read-heavy agents are better for exploration; write-capable agents are for delivery.</td></tr>
      <tr><td><strong>Model + version tags</strong></td><td>Default model choice and current maturity.</td></tr>
    </tbody>
  </table>

  <h2>Agent catalog</h2>
  {agents_html}
</section>
"""


def section_agent_onboarding() -> str:
    return f"""\
<section class="section" id="agent-onboarding">
{page_nav([("home", "Home"), ("agents", "Rune Agency"), "Onboarding"], 3)}
  <h1>&#x2795; Onboarding an Agent</h1>
  <p class="subtitle">Add a specialist to your team. Either recruit one from the open-source catalog, or write one yourself.</p>

  <p><strong>Read this when:</strong> the current catalog is close but not enough, and you need to recruit or author a specialist that Rune does not already ship.</p>
  <p><strong>What you get:</strong> the file shape, frontmatter reference, and prompt structure needed to add a new agent without guessing where the routing metadata stops and the prompt begins.</p>

  <p>Every agent is a plain markdown file. The YAML frontmatter is the routing layer: it tells Rune how and when to use the agent. The body is the system prompt: the instructions the agent follows after dispatch.</p>
  <p><strong>Just trying to understand the existing team?</strong> Go back to <button data-section="agents">Agents</button> for the live catalog.</p>

  <h2>Two paths</h2>
  <table>
    <thead>
      <tr><th>Path</th><th>When to use it</th><th>How to start</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Recruit from catalog</strong></td><td>A specialist already exists that fits your need</td><td><code>/km-recruit [description]</code></td></tr>
      <tr><td><strong>Write from scratch</strong></td><td>Your domain is specific and no catalog match exists</td><td>Create a <code>.md</code> file</td></tr>
    </tbody>
  </table>
  <p>The built-in catalog lives at <code>src/rune-agency/agents/</code> in the rune repository. Additional specialists are available in the <a href='https://github.com/msitarzewski/agency-agents' target='_blank' rel='noopener'>agency-agents catalog</a>.</p>

  <h2>Step 1 &mdash; Create the file</h2>
  <p>Put the new agent in the phase folder that matches its primary job. Use the naming pattern <code>role.md</code>.</p>

  <pre><code>src/rune-agency/agents/&lt;phase&gt;/my-specialist.md</code></pre>

  <h2>Step 2 &mdash; Write the frontmatter</h2>
  <pre><code>---
name: my-specialist
description: Use this agent when you need to... Also invoke when
  the user says 'hey my-specialist' or any similar phrase.
model: sonnet
tools: Read, Write, Edit, Bash, fd, rg, Glob, Grep
color: teal
emoji: "&#x1F50D;"
version: 1.0.0
phase: build
---</code></pre>

  <h3>All frontmatter fields</h3>
  <table>
    <thead>
      <tr><th>Field</th><th>Required</th><th>What it does</th></tr>
    </thead>
    <tbody>
      <tr><td><code>name</code></td><td>Yes</td><td>Unique identifier. Used in task plans and dispatch diagrams.</td></tr>
      <tr><td><code>description</code></td><td>Yes</td><td>Tells the AI when to invoke this agent. Write trigger phrases here.</td></tr>
      <tr><td><code>model</code></td><td>No</td><td>Which AI model this agent uses.</td></tr>
      <tr><td><code>tools</code></td><td>No</td><td>Which tools the agent can use.</td></tr>
      <tr><td><code>color</code></td><td>No</td><td>Card border color in the docs site.</td></tr>
      <tr><td><code>emoji</code></td><td>No</td><td>Icon shown in dispatch diagrams and the agent card.</td></tr>
      <tr><td><code>version</code></td><td>No</td><td>Semantic version.</td></tr>
      <tr><td><code>phase</code></td><td>No</td><td>Four-phase model assignment (explore, plan, build, validate).</td></tr>
    </tbody>
  </table>

  <h2>Step 3 &mdash; Write the system prompt</h2>
  <p>The body of the file is the agent&rsquo;s system prompt. This is what the agent reads before every task.</p>

  <p>A good system prompt has three parts:</p>
  <ol>
    <li><strong>Role statement.</strong> Who is this agent and what is their specialty?</li>
    <li><strong>Core responsibilities.</strong> What does this agent do?</li>
    <li><strong>Collaboration.</strong> Hand-off instructions.</li>
  </ol>
</section>
"""


def section_skills(skills_html: str) -> str:
    return f"""\
<section class="section" id="skills">
{page_nav([("home", "Home"), ("agents", "Rune Agency"), "Skills"], 2)}
  <h1>&#x1F4DD; Skills</h1>
  <p class="subtitle">Skills are the workflows you invoke directly. Agents are the specialists they dispatch behind the scenes.</p>

  <p><strong>Read this when:</strong> you know the job you want done and need the fastest command-level entrypoint instead of browsing the team member by member.</p>
  <p><strong>What you get:</strong> the live slash-command catalog and the distinction between an on-demand workflow surface and the agents or rules it pulls in.</p>

  <p>Skills are slash commands that trigger structured workflows. They live in <code>src/rune-agency/skills/</code> as directories containing a <code>SKILL.md</code> and optional supporting files.</p>
  <p>A useful shortcut: if your request starts with a verb like <em>plan</em>, <em>audit</em>, <em>draft</em>, or <em>release</em>, start with a skill. If it starts with a role like <em>researcher</em> or <em>judge</em>, start with an agent.</p>

  <h2>Skill catalog</h2>
  {skills_html}
</section>
"""


def section_rules_catalog(total_rules: int, rules_html: str) -> str:
    return f"""\
<section class="section" id="rules-catalog">
{page_nav([("home", "Home"), ("agents", "Rune Agency"), "Rules"], 3)}
  <h1>&#x1F4DA; Rules</h1>
  <p class="subtitle">Rules are the reusable knowledge layer. Profiles decide which parts of that layer load for a given kind of work.</p>

  <p><strong>Read this when:</strong> you want to understand what Rune already knows, which conventions are loaded by profiles, or where durable team doctrine should live.</p>
  <p><strong>What you get:</strong> the full rules library, grouped by phase, plus the mental split between reusable knowledge and one-off workflow instructions.</p>

  <p>Rules provide the shared knowledge base for your team. They contain conventions, standards, and architectural decisions that guide agent behavior. Total rules in library: <strong>{total_rules}</strong>.</p>
  <p>Put stable canon here. If the content is really a reusable operator motion, it belongs in a skill; if it is only one specialist&rsquo;s role doctrine, it belongs in an agent prompt.</p>

  <h2>Rules library</h2>
  {rules_html}
</section>
"""


def build_agency(
    agents_html: str,
    skills_html: str,
    total_rules: int,
    num_categories: int,
    rules_html: str,
) -> str:
    return (
        section_agents(agents_html)
        + section_skills(skills_html)
        + section_rules_catalog(total_rules, rules_html)
        + section_agent_onboarding()
    )
