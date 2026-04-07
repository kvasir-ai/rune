"""Home, Quick Start, and Talk sections."""
from __future__ import annotations

from .shared import page_nav


def section_home(
    total_agents: int,
    total_rules: int,
    total_skills: int,
) -> str:
    return f"""\
<section class="section active" id="home">
{page_nav([("home", "Home")], 1)}

  <div style="margin: 2rem 0; text-align: center;">
    <img src="assets/rune-docs.png" alt="Rune Agency Architecture" style="max-width: 100%; border-radius: 8px; border: 1px solid var(--border);">
  </div>

  <h1>Start Here</h1>
  <p class="subtitle">Install Rune, prove it works, and learn the smallest useful workflow before you branch into the deeper material.</p>

  <p><strong>Read this when:</strong> you are new to Rune and want the shortest path from install to a first successful session.</p>
  <p><strong>What you get:</strong> the setup path, the basic conversation model, and a clear handoff into the core workflow and the wider docs.</p>

  <p>AI coding agents work best with structure. Without coordination, they tend to duplicate work, lose context, and occasionally run destructive commands.</p>

  <div class="stat-grid">
    <button class="stat-card" data-section="agents"><div class="number">{total_agents}</div><div class="label">Agents</div></button>
    <button class="stat-card" data-section="rules-catalog"><div class="number">{total_rules}</div><div class="label">Rules</div></button>
    <button class="stat-card" data-section="skills"><div class="number">{total_skills}</div><div class="label">Skills</div></button>
    <button class="stat-card" data-section="four-phase-model"><div class="number">4</div><div class="label">Phases</div></button>
  </div>

  <h2>Your first three stops</h2>
  <p>Follow this order: install Rune, run one small session, then learn how that conversation maps to the four-phase workflow.</p>
  <div class="card-grid">
    <button class="card" data-section="quick-start"><span class="emoji" aria-hidden="true">&#x26A1;&#xFE0F;</span><h4>Quick Start</h4><p>Install and configure Rune</p></button>
    <button class="card" data-section="talk"><span class="emoji" aria-hidden="true">&#x1F4AC;</span><h4>Talk to Your Team</h4><p>Natural language interaction</p></button>
    <button class="card" data-section="four-phase-model"><span class="emoji" aria-hidden="true">&#x1F50D;</span><h4>Learn the Phases</h4><p>Explore, Plan, Build, Validate</p></button>
  </div>

  <h2>Use the Getting Started pages this way</h2>
  <table>
    <thead>
      <tr><th>Page</th><th>Question it answers</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Start Here</strong></td><td>What path should I follow first?</td></tr>
      <tr><td><button data-section="quick-start">Quick Start</button></td><td>How do I install Rune and confirm it works?</td></tr>
      <tr><td><button data-section="talk">Talk to Your Team</button></td><td>What do I actually say once it is installed?</td></tr>
    </tbody>
  </table>

  <h2>The four-phase model</h2>
  <div class="agent-grid">
    <button class="agent-card" data-section="phase-1-explore" style="border-top-color:var(--accent);">
      <span class="agent-emoji" aria-hidden="true">&#x1F50D;</span>
      <div class="agent-info">
        <div class="phase-label phase-explore" style="margin-bottom: 0.5rem;">1 &middot; Explore</div>
        <p>Read-only agents gather context in parallel. They search code and return summaries.</p>
      </div>
    </button>
    <button class="agent-card" data-section="phase-2-plan" style="border-top-color:var(--fg2);">
      <span class="agent-emoji" aria-hidden="true">&#x1F5FA;&#xFE0F;</span>
      <div class="agent-info">
        <div class="phase-label phase-plan" style="margin-bottom: 0.5rem;">2 &middot; Plan</div>
        <p>The Planner decomposes work into a dependency graph with explicit task ownership.</p>
      </div>
    </button>
    <button class="agent-card" data-section="phase-3-build" style="border-top-color:var(--accent2);">
      <span class="agent-emoji" aria-hidden="true">&#x1F3D7;&#xFE0F;</span>
      <div class="agent-info">
        <div class="phase-label phase-build" style="margin-bottom: 0.5rem;">3 &middot; Build</div>
        <p>Independent tasks run simultaneously in parallel waves. Build fast, build reliably.</p>
      </div>
    </button>
    <button class="agent-card" data-section="phase-4-validate" style="border-top-color:var(--accent);">
      <span class="agent-emoji" aria-hidden="true">&#x2705;</span>
      <div class="agent-info">
        <div class="phase-label phase-validate" style="margin-bottom: 0.5rem;">4 &middot; Validate</div>
        <p>The Judge verifies output before shipping. Nothing passes without passing the gate.</p>
      </div>
    </button>
  </div>

  <h2>Suggested path</h2>
  <p>After the first two pages, keep going only as far as you need:</p>
  <table>
    <thead>
      <tr><th>#</th><th>Step</th><th>What You Learn</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td><button data-section="quick-start">Quick Start</button></td><td>Install, deploy a profile, verify it works</td></tr>
      <tr><td>2</td><td><button data-section="talk">Talk to Your Team</button></td><td>How to interact with agents in natural language</td></tr>
      <tr><td>3</td><td><button data-section="four-phase-model">Four-Phase Model</button></td><td>The core workflow: explore, plan, build, validate</td></tr>
      <tr><td>4</td><td><button data-section="agents">Agents</button></td><td>Who does what and how they coordinate</td></tr>
      <tr><td>5</td><td><button data-section="profiles">Profiles</button></td><td>Load the right rules and resources for the task</td></tr>
      <tr><td>6</td><td><button data-section="dag-dispatch">DAG Dispatch</button></td><td>Run work in dependency waves</td></tr>
      <tr><td>7</td><td><button data-section="operating-guides">Operating Guides</button></td><td>See the advanced operating model behind Rune</td></tr>
    </tbody>
  </table>

  <h2>After the basics</h2>
  <p>Once the first-session flow feels solid, either learn the specialist team or move into the deeper operating model.</p>
  <div class="card-grid">
    <button class="card" data-section="agents"><span class="emoji" aria-hidden="true">&#x1F916;</span><h4>Meet the Agents</h4><p>{total_agents} specialists and when to use each one</p></button>
    <button class="card" data-section="operating-guides"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Operating Guides</h4><p>Learn the deeper model once the basics are working</p></button>
  </div>
</section>
"""


def section_quick_start() -> str:
    return f"""\
<section class="section" id="quick-start">
{page_nav([("home", "Home"), "Quick Start"], 2)}
  <h1>&#x26A1;&#xFE0F; Quick Start</h1>
  <p class="subtitle">Install Rune, choose the right scope, verify the deployment, and run one small session.</p>

  <p><strong>Read this when:</strong> you want the shortest reliable path from zero to a working Rune install.</p>
  <p><strong>What you get:</strong> the install prerequisites, the machine-wide vs project-local choice, verification commands, and the first commands to run once setup finishes.</p>

  <h2>Choose your install scope</h2>
  <p>Pick one path. You do not need both.</p>
  <table>
    <thead>
      <tr><th>Use this option when...</th><th>Choose</th></tr>
    </thead>
    <tbody>
      <tr><td>You want Rune available in every repo on this machine</td><td><strong>Machine-wide install</strong></td></tr>
      <tr><td>You want Rune isolated to one repository</td><td><strong>Project-local install</strong></td></tr>
    </tbody>
  </table>

  <h2>Prerequisites</h2>
  <p><strong>Supported environments:</strong> macOS or Linux/WSL2.</p>
  <p>Install <code>uv</code>, clone Rune, and then choose the scope that matches how you work.</p>

  <h3>Install uv</h3>
  <p><a href="https://docs.astral.sh/uv/" target="_blank" rel="noopener">uv</a> is a Python package manager written in Rust. It handles all dependencies automatically.</p>
  <p><strong>For macOS:</strong></p>
  <pre><code>brew install uv</code></pre>
  <p><strong>For Linux/WSL2:</strong></p>
  <pre><code>curl -LsSf https://astral.sh/uv/install.sh | sh</code></pre>

  <h3>Machine-wide install</h3>
  <p>Use this if you want Rune available in every project on your machine.</p>
  <pre><code>git clone https://github.com/kvasir-ai/rune.git
cd rune
uv tool install .
rune setup
rune profile use default</code></pre>

  <h3>Project-local install</h3>
  <p>Use this if you want Rune scoped to a single repo.</p>
  <pre><code>cd your-project
git clone https://github.com/kvasir-ai/rune.git .rune-config
cd .rune-config
uv tool install .
rune setup
rune profile use default --project</code></pre>

  <h2>Verify the deployment</h2>
  <p>Run these once setup finishes:</p>
  <pre><code>rune system verify   # check deployed state
rune resource list   # browse the active team and rules
rune resource skills # browse the workflows</code></pre>

  <p>You can also run Rune directly from the cloned repository using <code>uv run rune [command]</code>.</p>

  <h2>First five minutes</h2>
  <p>Open your coding tool in a project and start small. The goal is to prove the deployment works before you try anything ambitious.</p>
  <ol>
    <li>Run <code>rune system verify</code> to confirm the deployed state.</li>
    <li>Open your coding tool in the target project.</li>
    <li>Ask for a small plan such as <code>"plan a small change in this repo"</code> or use <code>/write-plan</code>.</li>
    <li>Dispatch the work with <code>/rune</code> when the plan looks right, or run <code>rune demo</code> first if you want to watch the workflow before using it.</li>
  </ol>

  <h2>What setup changed</h2>
  <p>Rune is not a wrapper around the AI. It is an orchestration CLI. When you run <code>rune setup</code> or <code>rune profile use &lt;name&gt;</code>, the CLI injects a specific configuration into the configuration directory of your AI coding assistant.</p>

  <p>Specifically, the CLI:</p>
  <ul>
    <li><strong>Injects Agents:</strong> Copies the Planner, Judge, Engineer, etc., into the tool's agent directory.</li>
    <li><strong>Injects Rules:</strong> Copies markdown files containing your engineering conventions and architectural decisions.</li>
    <li><strong>Wires Hooks:</strong> Installs Python scripts that act as lifecycle events (e.g., the safety hook that intercepts destructive commands before execution).</li>
    <li><strong>Updates Config:</strong> Modifies <code>settings.json</code> to grant the necessary tool permissions.</li>
  </ul>

  <p>Because Rune lives entirely in your terminal, you can run <code>rune reset --global</code> to wipe the machine-wide install or <code>rune reset --project</code> to wipe only the current repo&rsquo;s injected configuration.</p>

  <h2>Profiles</h2>
  <p>A profile bundles the rules and resources needed for one kind of work. Browse <button data-section="profiles">Profiles</button> to choose one that fits your task.</p>

  <h2>Next steps</h2>
  <div class="card-grid">
    <button class="card" data-section="talk"><span class="emoji" aria-hidden="true">&#x1F4AC;</span><h4>Talk to Your Team</h4><p>Learn natural language interactions</p></button>
    <button class="card" data-section="profiles"><span class="emoji" aria-hidden="true">&#x1F504;</span><h4>Browse Profiles</h4><p>Switch knowledge for different tasks.</p></button>
    <button class="card" data-section="agents"><span class="emoji" aria-hidden="true">&#x1F916;</span><h4>Meet the Agents</h4><p>See who's on the team</p></button>
    <button class="card" data-section="four-phase-model"><span class="emoji" aria-hidden="true">&#x1F5FA;&#xFE0F;</span><h4>Learn the Phases</h4><p>The four-phase workflow</p></button>
  </div>
</section>
"""


def section_talk() -> str:
    return f"""\
<section class="section" id="talk">
{page_nav([("home", "Home"), "Talk to Your Team"], 2)}
  <h1>&#x1F4AC; Talk to Your Team</h1>
  <p class="subtitle">Use natural language for intent and slash commands for repeatable workflows. Rune supports both in the same session.</p>

  <p><strong>Read this when:</strong> Rune is installed and you want to know what to actually say next.</p>
  <p><strong>What you get:</strong> a simple first conversation, plus example prompts and commands mapped to Explore, Plan, Build, Validate, and ongoing team maintenance.</p>

  <p>You do not need perfect phrasing. Use natural language when the intent is obvious, and use slash commands when you want a specific workflow with a stronger contract.</p>

  <h2>Use both interaction styles</h2>
  <table>
    <thead>
      <tr><th>Style</th><th>Best for</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Plain English</strong></td><td>Stating the goal, asking for research, or requesting validation in normal language.</td></tr>
      <tr><td><strong>Slash commands</strong></td><td>Starting a known workflow such as planning, DAG execution, or knowledge audit.</td></tr>
    </tbody>
  </table>

  <h2>A good first conversation</h2>
  <table>
    <thead>
      <tr><th>Say this</th><th>Why start here</th></tr>
    </thead>
    <tbody>
      <tr><td><code>/km-explore your-repo-name</code></td><td>Gets trustworthy repo context before you ask for implementation.</td></tr>
      <tr><td><code>/write-plan</code></td><td>Turns that context into a small, executable plan.</td></tr>
      <tr><td><code>/rune</code></td><td>Runs the plan in parallel waves once it looks right.</td></tr>
      <tr><td><code>/judge</code></td><td>Checks the result before you treat the work as done.</td></tr>
    </tbody>
  </table>

  <p>The four-phase workflow maps to a natural conversation. Start with Explore, then let planning, execution, and validation narrow the work step by step.</p>

  <h3>Phase 1: Explore</h3>
  <table>
    <thead>
      <tr><th>You say</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td><code>/km-explore</code></td><td>Knowledge Manager researches a repo, feature, ticket, or problem domain and returns structured findings</td></tr>
      <tr><td><code>"learn about the payments service"</code></td><td>Knowledge Manager reads the codebase, related tickets, and docs to build a knowledge summary</td></tr>
      <tr><td><code>"research this codebase"</code></td><td>Knowledge Manager explores the repo structure and returns a structured summary</td></tr>
      <tr><td><code>/rune-demo</code></td><td>Run a showcase task plan with simulated agents</td></tr>
    </tbody>
  </table>

  <h3>Phase 2: Plan</h3>
  <table>
    <thead>
      <tr><th>You say</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td><code>"plan a REST API for user management"</code></td><td>Planner explores requirements and breaks the work into tasks with dependencies</td></tr>
      <tr><td><code>/write-plan</code></td><td>Generate a strict, step-by-step implementation plan with dependency annotations</td></tr>
      <tr><td><code>"test this DAG"</code></td><td>Zero-cost dry run &mdash; checks the plan structure without dispatching any agents</td></tr>
    </tbody>
  </table>

  <h3>Phase 3: Build</h3>
  <table>
    <thead>
      <tr><th>You say</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td><code>/rune</code></td><td>Dispatch the plan &mdash; agents run in parallel waves, passing results to each other</td></tr>
      <tr><td><code>/tw-draft-pr</code></td><td>Draft a PR description from the completed work</td></tr>
      <tr><td><code>/tw-release</code></td><td>Prepare a release &mdash; changelog, notes, version bump, tag</td></tr>
    </tbody>
  </table>

  <h3>Phase 4: Validate</h3>
  <table>
    <thead>
      <tr><th>You say</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td><code>/judge</code></td><td>Code review &mdash; checks output for correctness, safety, and completeness</td></tr>
      <tr><td><code>/judge-audit</code></td><td>Deep review of any agent's output &mdash; correctness, safety, consistency</td></tr>
      <tr><td><code>/judge-panel 3</code></td><td>Three independent judges review the same output from different angles</td></tr>
      <tr><td><code>"hey judge, validate this output"</code></td><td>Judge reviews the most recent output and reports findings</td></tr>
    </tbody>
  </table>

  <h3>Keep the team current</h3>
  <p>Every session is a chance to make the team smarter. When you find reusable knowledge or catalog gaps, hand that work to the Knowledge Manager.</p>
  <table>
    <thead>
      <tr><th>You say</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td><code>/km-audit</code></td><td>Audit the knowledge base &mdash; finds stale rules, orphaned files, and context budget issues</td></tr>
      <tr><td><code>/km-recruit</code></td><td>Find and recruit a specialist agent from the <a href="https://github.com/msitarzewski/agency-agents" target="_blank" rel="noopener noreferrer">agency-agents</a> catalog</td></tr>
      <tr><td><code>"recruit an agent for data analysis"</code></td><td>Knowledge Manager searches the catalog and adapts the best match to your toolkit</td></tr>
      <tr><td><code>"teach the agent about our dbt conventions"</code></td><td>Knowledge Manager distills the material into a rule and deploys it to relevant profiles</td></tr>
      <tr><td><code>"audit the knowledge base"</code></td><td>Knowledge Manager scans all rules for staleness, size issues, and coverage gaps</td></tr>
      <tr><td><code>"switch to the security profile"</code></td><td>Knowledge Manager swaps the active rule set to match your current task</td></tr>
    </tbody>
  </table>

  <p>Rune supports both styles. Use the CLI for setup and configuration, then talk to agents naturally inside your coding session.</p>

  <h2>Next steps</h2>
  <div class="card-grid">
    <button class="card" data-section="four-phase-model"><span class="emoji" aria-hidden="true">&#x1F3AF;</span><h4>Four-Phase Model</h4><p>See the workflow behind the conversation</p></button>
    <button class="card" data-section="agents"><span class="emoji" aria-hidden="true">&#x1F916;</span><h4>Meet the Agents</h4><p>Learn which specialist does what</p></button>
    <button class="card" data-section="profiles"><span class="emoji" aria-hidden="true">&#x1F504;</span><h4>Profiles</h4><p>Load the right doctrine for the task</p></button>
    <button class="card" data-section="operating-guides"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Operating Guides</h4><p>Learn the deeper model after the basics click</p></button>
  </div>
</section>
"""


def build_home(
    total_agents: int,
    total_rules: int,
    total_skills: int,
) -> str:
    return (
        section_home(total_agents, total_rules, total_skills)
        + section_quick_start()
        + section_talk()
    )
