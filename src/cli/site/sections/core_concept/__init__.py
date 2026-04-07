"""Core concept sections: four-phase model, phases 1-4, profiles, and DAG dispatch."""
from __future__ import annotations

from ..shared import page_nav


def section_four_phase_model() -> str:
    return f"""\
<section class="section" id="four-phase-model">
{page_nav([("home", "Home"), ("four-phase-model", "The Core Concept"), "Four-Phase Model"], 1)}
  <h1>&#x1F3AF; The Four-Phase Model</h1>
  <p class="subtitle">Four phases that turn a vague request into verified output.</p>

  <p><strong>Read this when:</strong> you want the shortest accurate explanation of how Rune turns an ambiguous request into scoped work, implementation, and review.</p>
  <p><strong>What you get:</strong> the full lifecycle, the responsibility of each phase, and the right page to read next when you need more detail.</p>

  <h2>Core idea</h2>
  <p>Rune works best when specialist agents do one kind of work at a time. Explore gathers evidence. Plan decomposes it. Build executes scoped tasks. Validate checks the result before it advances. The rules and profiles carry durable knowledge so the workflow does not depend on one overloaded conversation.</p>

  <h2>The lifecycle</h2>
  <table>
    <thead>
      <tr><th>Phase</th><th>Main question</th><th>What comes out</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>1. Explore</strong></td><td>What is true right now?</td><td>Read-only findings, constraints, and repo context</td></tr>
      <tr><td><strong>2. Plan</strong></td><td>What work exists, and what depends on what?</td><td>A DAG or sequential plan with scoped tasks</td></tr>
      <tr><td><strong>3. Build</strong></td><td>How do we execute the plan safely and quickly?</td><td>Completed task outputs plus short wave summaries</td></tr>
      <tr><td><strong>4. Validate</strong></td><td>Is the result correct enough to advance?</td><td>A Judge verdict, findings, and next owner</td></tr>
    </tbody>
  </table>

  <h2>Phase pages</h2>
  <p>Read the phase page that matches your current bottleneck. The four pages below teach responsibilities and handoffs. `Profiles` and `DAG Dispatch` explain how the phases stay focused and how execution actually runs.</p>
  <div class="card-grid">
    <button class="card" data-section="phase-1-explore"><span class="emoji" aria-hidden="true">&#x1F50D;</span><h4>Phase 1: Explore</h4><p>Understand before acting</p></button>
    <button class="card" data-section="phase-2-plan"><span class="emoji" aria-hidden="true">&#x1F5FA;&#xFE0F;</span><h4>Phase 2: Plan</h4><p>Decompose into a dependency graph</p></button>
    <button class="card" data-section="phase-3-build"><span class="emoji" aria-hidden="true">&#x1F3D7;&#xFE0F;</span><h4>Phase 3: Build</h4><p>Dispatch tasks in parallel waves</p></button>
    <button class="card" data-section="phase-4-validate"><span class="emoji" aria-hidden="true">&#x2705;</span><h4>Phase 4: Validate</h4><p>Verify output before shipping</p></button>
  </div>

  <h2>Next steps</h2>
  <div class="card-grid">
    <button class="card" data-section="profiles"><span class="emoji" aria-hidden="true">&#x1F504;</span><h4>Profiles</h4><p>Load the rules and resources the task needs</p></button>
    <button class="card" data-section="dag-dispatch"><span class="emoji" aria-hidden="true">&#x1F500;</span><h4>DAG Dispatch</h4><p>Run work in dependency waves</p></button>
  </div>
</section>
"""


def section_phase_1_explore() -> str:
    return f"""\
<section class="section" id="phase-1-explore">
{page_nav([("home", "Home"), ("four-phase-model", "The Core Concept"), ("four-phase-model", "Four-Phase Model"), "Phase 1: Explore"])}
  <h1>&#x1F50D; Phase 1: Explore</h1>
  <p class="subtitle">Read the codebase before writing anything. It takes a few minutes and saves hours later.</p>

  <p><strong>Read this when:</strong> the problem is still fuzzy and you need trustworthy repo context before anyone starts planning or editing files.</p>
  <p><strong>What you get:</strong> scoped findings, constraints, and a compact brief that the Planner can turn into a task graph.</p>

  <h2>Core idea</h2>
  <p>Explore is read-only by design. The point is not to guess the answer early. It is to let specialist agents read different parts of the repo in parallel, then compress what mattered into a short handoff. Heavy context stays inside the subagents and dies when they finish.</p>

  <h2>How it works</h2>
  <pre><code>====================================================
  FAN-OUT EXECUTION
  Agents: 4  |  Waves: 2  |  Type: explore
====================================================

  Wave 0 ---- parallel ----------------------------
  #1  RESEARCHER            Map service boundaries
  #2  RESEARCHER            Read docs, tickets, and recent changes
  #3  KNOWLEDGE-MANAGER     Check existing rules and known constraints

  Wave 1 ---- sequential --------------------------
  #4  KNOWLEDGE-MANAGER     Synthesize a repo brief
                             depends on: #1, #2, #3

====================================================</code></pre>

  <p>Each agent reads a different slice of the problem and returns a short result. The synthesis pass turns those results into one brief for planning instead of dragging raw logs and files into the main thread.</p>

  <h2>What comes out of Explore</h2>
  <table>
    <thead>
      <tr><th>Output</th><th>Why it matters</th></tr>
    </thead>
    <tbody>
      <tr><td>Repo brief</td><td>Gives the Planner a compact starting point instead of raw exploration notes</td></tr>
      <tr><td>Constraints</td><td>Surfaces what the next phase must respect: architecture, rules, APIs, or known risks</td></tr>
      <tr><td>Open questions</td><td>Makes uncertainty explicit before the plan hardens</td></tr>
    </tbody>
  </table>

  <h2>What to say</h2>
  <table>
    <thead>
      <tr><th>Say this</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td><code>/km-explore</code></td><td>Knowledge Manager researches the repo and returns structured findings</td></tr>
      <tr><td><code>"research this codebase"</code></td><td>Explores the repo structure and returns a structured summary</td></tr>
      <tr><td><code>"learn about the payments service"</code></td><td>Reads the codebase, related tickets, and docs to build a knowledge summary</td></tr>
      <tr><td><code>"explore before you start"</code></td><td>Dispatches read-only agents before any implementation begins</td></tr>
    </tbody>
  </table>

  <h2>Boundaries</h2>
  <p>Explore gathers evidence. It does not commit to a solution, assign dependencies, or edit files. Once the brief is good enough to decompose, move to Plan.</p>

  <h2>Next step</h2>
  <div class="card-grid">
    <button class="card" data-section="four-phase-model"><span class="emoji" aria-hidden="true">&#x1F3AF;</span><h4>Overview</h4><p>Back to the four-phase model</p></button>
    <button class="card" data-section="phase-2-plan"><span class="emoji" aria-hidden="true">&#x1F5FA;&#xFE0F;</span><h4>Phase 2: Plan</h4><p>Decompose findings into a dependency graph</p></button>
  </div>
</section>
"""


def section_phase_2_plan() -> str:
    return f"""\
<section class="section" id="phase-2-plan">
{page_nav([("home", "Home"), ("four-phase-model", "The Core Concept"), ("four-phase-model", "Four-Phase Model"), "Phase 2: Plan"])}
  <h1>&#x1F5FA;&#xFE0F; Phase 2: Plan</h1>
  <p class="subtitle">Decompose work into small, independent, parallelizable tasks. No implementing yet.</p>

  <p><strong>Read this when:</strong> you understand the problem well enough to assign ownership, define outputs, and separate parallel work from dependent work.</p>
  <p><strong>What you get:</strong> a task graph that names owners, files, dependencies, and the output each task is responsible for producing.</p>

  <h2>Core idea</h2>
  <p>The Planner converts exploration findings into an execution-ready contract. Good plans are small, explicit, and honest about dependencies. The point is not to write beautiful prose. The point is to make Build predictable.</p>

  <h2>The plan artifact</h2>
  <p>The output of Phase 2 is usually a plan in <code>docs/plans/</code> or a live DAG in memory. A minimal task contract looks like this:</p>

  <pre><code>tasks:
  - id: t1
    agent: engineer
    title: Design API contract
    depends_on: []
    files: [docs/api-contract.yaml]
    output: API contract with routes, payloads, and error cases

  - id: t2
    agent: engineer
    title: Implement handlers
    depends_on: [t1]
    files: [src/api/handlers.go]
    output: Working handlers that match the contract

  - id: t3
    agent: technical-writer
    title: Draft integration notes
    depends_on: [t1]
    files: [docs/api/quickstart.md]
    output: Reviewer-ready docs that match the contract</code></pre>

  <p>In that example, the contract must exist before implementation or docs can proceed. Once <code>t1</code> finishes, <code>t2</code> and <code>t3</code> can run independently.</p>

  <h2>What comes out of Plan</h2>
  <table>
    <thead>
      <tr><th>Output</th><th>Why it matters</th></tr>
    </thead>
    <tbody>
      <tr><td>Task ownership</td><td>Makes responsibilities explicit before work starts</td></tr>
      <tr><td>Dependencies</td><td>Lets the dispatcher compute safe execution waves</td></tr>
      <tr><td>File scope and outputs</td><td>Prevents vague work and reduces downstream ambiguity</td></tr>
    </tbody>
  </table>

  <h2>What to say</h2>
  <table>
    <thead>
      <tr><th>Say this</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td><code>/write-plan</code></td><td>Generate a strict, step-by-step implementation plan with dependency annotations</td></tr>
      <tr><td><code>"plan a REST API for user management"</code></td><td>Planner explores requirements and breaks the work into tasks with dependencies</td></tr>
      <tr><td><code>"test the DAG"</code></td><td>Dry run &mdash; checks the plan structure without dispatching any agents</td></tr>
    </tbody>
  </table>

  <h2>Boundaries</h2>
  <p>Plan defines work. It does not implement it. If you are still collecting facts, go back to Explore. If you are editing files, you are already in Build.</p>

  <h2>Next step</h2>
  <div class="card-grid">
    <button class="card" data-section="phase-1-explore"><span class="emoji" aria-hidden="true">&#x1F50D;</span><h4>Phase 1: Explore</h4><p>Go back if the problem still lacks evidence</p></button>
    <button class="card" data-section="phase-3-build"><span class="emoji" aria-hidden="true">&#x1F3D7;&#xFE0F;</span><h4>Phase 3: Build</h4><p>Dispatch the plan in parallel waves</p></button>
  </div>
</section>
"""


def section_phase_3_build() -> str:
    return f"""\
<section class="section" id="phase-3-build">
{page_nav([("home", "Home"), ("four-phase-model", "The Core Concept"), ("four-phase-model", "Four-Phase Model"), "Phase 3: Build"])}
  <h1>&#x1F3D7;&#xFE0F; Phase 3: Build</h1>
  <p class="subtitle">Execute the plan wave by wave. Fast implementation with high quality.</p>

  <p><strong>Read this when:</strong> the plan is solid and you are ready to execute scoped tasks instead of debating what the work is.</p>
  <p><strong>What you get:</strong> completed task outputs, per-wave summaries, and a clean handoff into validation instead of one giant tangled thread.</p>

  <h2>Core idea</h2>
  <p>Build is where the plan becomes execution. The dispatcher does not ask every agent to rediscover the whole repo. It gives each task a file scope, the needed predecessor summaries, and enough context to finish one job well.</p>

  <h2>How waves work</h2>
  <pre><code>Wave 0
- t1 engineer: design API contract
- t2 researcher: gather integration constraints

Wave 1
- t3 engineer: implement handlers        (depends on t1, t2)
- t4 technical-writer: draft quickstart  (depends on t1)

Wave 2
- t5 engineer: add integration tests     (depends on t3)</code></pre>

  <p>When a task completes, the dispatcher passes a short summary forward instead of the full conversation history. That keeps downstream work focused and prevents later waves from drowning in irrelevant detail.</p>

  <h2>What comes out of Build</h2>
  <table>
    <thead>
      <tr><th>Output</th><th>Why it matters</th></tr>
    </thead>
    <tbody>
      <tr><td>Scoped file changes</td><td>Each task owns one bounded slice of work</td></tr>
      <tr><td>Wave summaries</td><td>Downstream tasks inherit decisions without replaying full histories</td></tr>
      <tr><td>Execution status</td><td>Validate can see what completed, failed, or was blocked</td></tr>
    </tbody>
  </table>

  <h2>What to say</h2>
  <table>
    <thead>
      <tr><th>Say this</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td><code>/rune</code></td><td>Dispatch the plan &mdash; agents run in parallel waves, passing results to each other</td></tr>
      <tr><td><code>"dispatch this plan"</code></td><td>Execute an already-approved DAG or sequential plan</td></tr>
    </tbody>
  </table>

  <h2>Boundaries</h2>
  <p>Build executes the plan. It does not decide whether the work is good enough to ship. If the plan itself is wrong, go back to Plan. If the implementation is done, move to Validate.</p>

  <h2>Next step</h2>
  <div class="card-grid">
    <button class="card" data-section="phase-2-plan"><span class="emoji" aria-hidden="true">&#x1F5FA;&#xFE0F;</span><h4>Phase 2: Plan</h4><p>Go back if the task graph still needs work</p></button>
    <button class="card" data-section="phase-4-validate"><span class="emoji" aria-hidden="true">&#x2705;</span><h4>Phase 4: Validate</h4><p>Verify output before shipping</p></button>
  </div>
</section>
"""


def section_phase_4_validate() -> str:
    return f"""\
<section class="section" id="phase-4-validate">
{page_nav([("home", "Home"), ("four-phase-model", "The Core Concept"), ("four-phase-model", "Four-Phase Model"), "Phase 4: Validate"])}
  <h1>&#x2705; Phase 4: Validate</h1>
  <p class="subtitle">The quality gate. No code ships without passing review.</p>

  <p><strong>Read this when:</strong> implementation is complete and you need an explicit verdict instead of a vague feeling that the work is probably fine.</p>
  <p><strong>What you get:</strong> findings, a clear verdict, and the next owner or phase if the work is not ready to advance.</p>

  <h2>Core idea</h2>
  <p>The Judge is the final gate. It reviews the work from Build against the plan and the loaded rules. Validation is adversarial by design: it looks for correctness gaps, missing tests, and safety issues before they turn into shipped defects.</p>

  <h2>Validation outcomes</h2>
  <table>
    <thead>
      <tr><th>Verdict</th><th>Meaning</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>APPROVED</strong></td><td>Ready to advance</td></tr>
      <tr><td><strong>APPROVED WITH WARNINGS</strong></td><td>Can advance, but risk remains visible</td></tr>
      <tr><td><strong>BLOCKED</strong></td><td>Must resolve critical issues before proceeding</td></tr>
    </tbody>
  </table>

  <h2>What to say</h2>
  <table>
    <thead>
      <tr><th>Say this</th><th>What happens</th></tr>
    </thead>
    <tbody>
      <tr><td><code>/judge</code></td><td>Code review &mdash; checks output for correctness, safety, and completeness</td></tr>
      <tr><td><code>/judge-audit</code></td><td>Deep review of any agent's output &mdash; correctness, safety, consistency</td></tr>
      <tr><td><code>/judge-panel 3</code></td><td>Three independent judges review the same output from different angles</td></tr>
      <tr><td><code>"hey judge, validate this output"</code></td><td>Judge reviews the most recent output and reports findings</td></tr>
    </tbody>
  </table>

  <h2>Boundaries</h2>
  <p>Validate is not a stealth implementation phase. If the verdict is blocked, the required owner should fix the issue in Build or rework the plan, then come back through the gate.</p>

  <h2>Next step</h2>
  <div class="card-grid">
    <button class="card" data-section="phase-3-build"><span class="emoji" aria-hidden="true">&#x1F3D7;&#xFE0F;</span><h4>Phase 3: Build</h4><p>Go back when findings require implementation fixes</p></button>
    <button class="card" data-section="dag-dispatch"><span class="emoji" aria-hidden="true">&#x1F500;</span><h4>DAG Dispatch</h4><p>Deep dive into parallel execution</p></button>
  </div>
</section>
"""


def section_knowledge_pipeline(total_rules: int) -> str:
    return f"""\
<section class="section" id="knowledge-pipeline">
{page_nav([("home", "Home"), ("operating-guides", "Operating Guides"), "Knowledge Pipeline"], 4)}
  <h1>&#x1F4E5; Knowledge Pipeline</h1>
  <p class="subtitle">Collect raw material. Distill it into rules. Apply it through profiles.</p>

  <p><strong>Read this when:</strong> you want Rune to learn something durable instead of repeating the same context dump in every session.</p>
  <p><strong>What you get:</strong> A compact operating loop for capturing raw material, distilling it into rules, and wiring the result into the profiles that need it.</p>
  <p>Use the knowledge pipeline to turn raw material into guidance the team can reuse. Keep the steps small. Review the result after a few real sessions.</p>

  <h2>Use this flow</h2>
  <table>
    <thead>
      <tr><th>Step</th><th>What to do</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>1. Collect</strong></td><td>Place raw notes, docs, logs, or examples in <code>src/rune-agency/knowledge/</code>.</td></tr>
      <tr><td><strong>2. Distill</strong></td><td>Ask the Knowledge Manager to turn that material into a small set of rules in <code>.claude/rules/</code>.</td></tr>
      <tr><td><strong>3. Refine</strong></td><td>Prefer short tables, checklists, and examples over long prose.</td></tr>
      <tr><td><strong>4. Apply</strong></td><td>Add the rule to the profiles that need it, then use it in real sessions.</td></tr>
    </tbody>
  </table>

  <h2>Keep it practical</h2>
  <ul>
    <li>Start with material that changes decisions, not general background reading.</li>
    <li>Write one rule for one job when possible.</li>
    <li>Revise rules after use. Remove instructions that do not help.</li>
  </ul>

  <p>See <button data-section="prompting">Knowledge Distance</button> for more background on why this helps.</p>

  <h2>Rules library</h2>
  <p>Current library: <strong>{total_rules}</strong> rules.</p>
  <div class="card-grid">
    <button class="card" data-section="operating-guides"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Operating Guides</h4><p>Return to the full operating-model lane</p></button>
    <button class="card" data-section="prompting"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Knowledge Distance</h4><p>Understand when context beats rephrasing</p></button>
    <button class="card" data-section="rules-catalog"><span class="emoji" aria-hidden="true">&#x1F4DA;</span><h4>Browse Rules</h4><p>See the complete rules library</p></button>
  </div>
</section>
"""


def section_profiles(total_rules: int) -> str:
    return f"""\
<section class="section" id="profiles">
{page_nav([("home", "Home"), ("four-phase-model", "The Core Concept"), "Profiles"], 3)}
  <h1>&#x1F504; Profiles</h1>
  <p class="subtitle">Activate the first profile, then switch as the work moves through the workflow.</p>

  <p><strong>Read this when:</strong> the workflow is clear but you need to understand how Rune keeps each phase narrow instead of loading everything all the time.</p>
  <p><strong>What you get:</strong> a model for switching knowledge by phase so the same team stays useful without carrying the whole repo into every task.</p>

  <h2>Core idea</h2>
  <p>Profiles do not change who the agents are. They change what knowledge and rules load with them. Start narrow, usually with <code class="copyable">explore</code>, then switch only when the work changes phase or domain.</p>

  <h2>Common profiles</h2>
  <table>
    <thead>
      <tr><th>Profile</th><th>Phase</th><th>Typical use</th></tr>
    </thead>
    <tbody>
      <tr><td><code>explore</code></td><td>Explore</td><td>Read code, gather context, and summarize</td></tr>
      <tr><td><code>plan</code></td><td>Plan</td><td>Break work into steps and dependencies</td></tr>
      <tr><td><code>build</code></td><td>Build</td><td>Implementation work</td></tr>
      <tr><td><code>validate</code></td><td>Validate</td><td>Review output and check completion</td></tr>
      <tr><td><code>default</code></td><td>Mixed</td><td>General-purpose profile when you want the full shared set</td></tr>
    </tbody>
  </table>

  <h2>Use profiles this way</h2>
  <ul>
    <li>Activate <code class="copyable">explore</code> first.</li>
    <li>Switch when the task changes phase or domain.</li>
    <li>Keep each profile focused on one kind of work.</li>
  </ul>

  <p>Use <code class="copyable">rune profile use &lt;name&gt;</code> to switch, <code class="copyable">rune profile current</code> to check the active profile, and <code class="copyable">rune profile reapply</code> after profile changes.</p>

  <h2>Boundaries</h2>
  <p>Profiles are not new agents and not task plans. They are a knowledge-loading mechanism. If you need to decide what work exists, go to Plan. If you need to execute, go to Build.</p>

  <h2>Next step</h2>
  <div class="card-grid">
    <button class="card" data-section="phase-1-explore"><span class="emoji" aria-hidden="true">&#x1F50D;</span><h4>Phase 1: Explore</h4><p>See the first narrow profile in action</p></button>
    <button class="card" data-section="rune-man-profiles"><span class="emoji" aria-hidden="true">&#x1F464;</span><h4>RUNE-PROFILES(5)</h4><p>Read the full profile reference and available shipped profiles</p></button>
  </div>
</section>
"""


def section_dag_dispatch() -> str:
    return f"""\
<section class="section" id="dag-dispatch">
{page_nav([("home", "Home"), ("four-phase-model", "The Core Concept"), "DAG Dispatch"], 4)}
  <h1>&#x1F500; DAG Dispatch</h1>
  <p class="subtitle">Run tasks in dependency order. Run each wave in parallel when you can.</p>

  <p><strong>Read this when:</strong> you already have a plan and want to understand how Build turns dependencies into safe parallel execution.</p>
  <p><strong>What you get:</strong> the execution mechanics behind `/rune`: waves, summaries, task format, and why the dispatcher is separate from planning.</p>

  <h2>Core idea</h2>
  <p>DAG Dispatch is execution mechanics, not planning doctrine. It assumes the work has already been decomposed. The dispatcher computes what can run now, what must wait, and what context needs to move forward.</p>

  <h2>Use this flow</h2>
  <ol>
    <li>Define each task and its dependencies.</li>
    <li>Let <code>/rune</code> compute execution waves.</li>
    <li>Pass short summaries from one wave to the next.</li>
    <li>End with a review step.</li>
  </ol>

  <h2>Example</h2>
  <pre><code>Wave 0
- t1 engineer: design API contract
- t2 researcher: gather integration constraints

Wave 1
- t3 engineer: implement handlers       (depends on t1, t2)
- t4 technical-writer: draft docs       (depends on t1)

Wave 2
- t5 judge: validate result             (depends on t3, t4)</code></pre>

  <h2>Context summaries</h2>
  <p>Each subagent works in its own context and returns a short summary. This helps keep the main session smaller.</p>

  <table>
    <thead>
      <tr><th>Stage</th><th>What moves forward</th></tr>
    </thead>
    <tbody>
      <tr><td>Inside the subagent</td><td>Files, logs, dead ends, and working notes</td></tr>
      <tr><td>Back to the parent</td><td>A short summary with the result, constraints, and open issues</td></tr>
    </tbody>
  </table>

  <h2>Task format</h2>
  <pre><code>tasks:
  - id: t1
    agent: engineer
    title: Design API contract
    depends_on: []
    files: [docs/api-contract.yaml]
    output: API schema with endpoints and error codes

  - id: t2
    agent: technical-writer
    title: Draft quickstart
    depends_on: [t1]
    files: [docs/api/quickstart.md]
    output: Docs that match the contract and implementation</code></pre>

  <h2>Boundaries</h2>
  <p>DAG Dispatch does not decide what the tasks are. That is Plan. It explains how a finished task graph executes once the dependencies and file scopes already exist.</p>

  <h2>Next step</h2>
  <div class="card-grid">
    <button class="card" data-section="phase-3-build"><span class="emoji" aria-hidden="true">&#x1F3D7;&#xFE0F;</span><h4>Phase 3: Build</h4><p>See where dispatch fits inside the phase model</p></button>
    <button class="card" data-section="operating-guides"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Operating Guides</h4><p>Go deeper on budget, knowledge, and execution tradeoffs</p></button>
  </div>
</section>
"""


def section_token_economics() -> str:
    return f"""\
<section class="section" id="token-economics">
{page_nav([("home", "Home"), ("operating-guides", "Operating Guides"), "Token Economics"], 4)}
  <h1>&#x1F4B0; Token Economics</h1>
  <p class="subtitle">Every token costs money. Every rule consumes context. Lean profiles are not a preference &mdash; they are a practical cost strategy.</p>

  <p><strong>Read this when:</strong> your profiles feel bloated, subagent fan-out is getting expensive, or you need a better model-mix strategy.</p>
  <p><strong>What you get:</strong> A practical cost model for profile size, context budgets, and where expensive reasoning actually pays for itself.</p>
  <h2>The cost of context</h2>
  <p>LLM pricing is per-token. Every rule loaded into an agent&rsquo;s context is charged on input every time the agent processes a prompt. The more context you preload, the more overhead you pay before the agent does any useful work.</p>

  <ul>
    <li>A large rule file loaded into a profile is paid for on every invocation.</li>
    <li>If a rule is irrelevant to the task, that spend bought nothing.</li>
    <li>Multiply that overhead across a team of subagents and it dominates the bill quickly.</li>
  </ul>

  <p>This is why Rune leans so hard on profiles: not for organization alone, but to keep context narrow enough that reasoning space remains available for the actual job.</p>

  <h2>Why input tokens dominate</h2>
  <p>In a typical agent invocation, most tokens are input: system prompt, loaded rules, file contents, and conversation history. The generated answer is usually the smaller share. That means cost is heavily influenced by what you preload, not just what the model says back.</p>

  <ul>
    <li>Rules loaded at session start are re-sent on every turn.</li>
    <li>Lean profiles reduce recurring input cost on every invocation.</li>
    <li>Subagent dispatch resets context, so each task pays only for its own prompt and materials rather than the parent&rsquo;s full history.</li>
  </ul>

  <h2>Model selection per agent</h2>
  <p>Choosing the right model per agent is the single highest-leverage cost decision. <strong>Invest reasoning depth where it has the highest leverage, and use cheaper models everywhere else.</strong></p>

  <h3>The reasoning pyramid</h3>
  <pre><code>        &#x250C;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2510;
        &#x2502;  OPUS   &#x2502;  Plan + Validate
        &#x2502;         &#x2502;  Resolve ambiguity, catch what others miss
        &#x251C;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2524;
        &#x2502; SONNET  &#x2502;  Build + Learn
        &#x2502;         &#x2502;  Write code, implement, structured judgment
        &#x251C;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2524;
        &#x2502;  HAIKU  &#x2502;  Explore + Ship
        &#x2502;         &#x2502;  Read, summarize, follow templates
        &#x2514;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2518;</code></pre>

  <p>A bad plan produced by a cheaper model cascades into bad execution across many build tasks. The Opus investment at the planning phase saves multiples of its cost in rework later. The same logic applies to validation: a weak final gate is expensive because it lets expensive mistakes through.</p>

  <h3>Opus &mdash; Plan + Validate</h3>
  <p>Use your strongest reasoning model at the decision points where failure is most expensive.</p>
  <table>
    <thead>
      <tr><th>Agent</th><th>Phase</th><th>Why stronger reasoning pays off</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Planner</strong></td><td>Plan</td><td>Dependency graphs, task boundaries, and sequencing errors ripple through the entire build.</td></tr>
      <tr><td><strong>Judge</strong></td><td>Validate</td><td>The final gate needs adversarial review depth, not a superficial checklist pass.</td></tr>
    </tbody>
  </table>

  <h3>Sonnet &mdash; Build + Learn</h3>
  <p>Production work that requires domain judgment but operates within an existing plan fits here: implementation, synthesis, architectural refinement, and structured analysis.</p>

  <h3>Haiku &mdash; Explore + Coordinate</h3>
  <p>Read-only research, formatting, summarization, and coordination are where cheap models matter most because these tasks fan out in parallel during Explore.</p>

  <h3>The Explore override rule</h3>
  <p>When an agent is dispatched as a read-only subagent during Phase 1, prefer a cheaper model regardless of its normal default. Exploration is summarization, not open-ended reasoning. This is one of the easiest cost wins in the whole system.</p>

  <h2>Context window budgets</h2>
  <p>Context tokens are a finite resource. Every file read, every rule loaded, and every query result that enters the context window displaces space for reasoning.</p>

  <table>
    <thead>
      <tr><th>What loads</th><th>When</th><th>Typical effect</th></tr>
    </thead>
    <tbody>
      <tr><td>Agent frontmatter</td><td>Session start</td><td>Small baseline overhead</td></tr>
      <tr><td>Rules from the active profile</td><td>Session start</td><td>Main recurring context cost</td></tr>
      <tr><td>Skills</td><td>When invoked</td><td>Focused, task-specific overhead</td></tr>
      <tr><td>Agent full prompts</td><td>When dispatched</td><td>Per-subagent startup cost</td></tr>
      <tr><td>Read files and outputs</td><td>During execution</td><td>Variable, task-shaped overhead</td></tr>
    </tbody>
  </table>

  <h2>Why lean profiles matter</h2>
  <p>The goal is to keep overhead well below the point where it starts crowding out reasoning. A narrow profile leaves more room for the files, logs, specs, and intermediate results that actually matter to the task in front of the agent.</p>

  <table>
    <thead>
      <tr><th>Profile strategy</th><th>Overhead</th><th>Impact</th></tr>
    </thead>
    <tbody>
      <tr><td>Load everything</td><td>High</td><td>Convenient, but expensive and cognitively noisy</td></tr>
      <tr><td>Domain-specific</td><td>Moderate</td><td>Good balance for most work</td></tr>
      <tr><td>Minimal + on-demand</td><td>Low</td><td>Maximum headroom and lowest recurring cost</td></tr>
    </tbody>
  </table>

  <h2>Dispatch cost tracking</h2>
  <p>Every <code>/rune</code> dispatch should be thought of as a small portfolio of model invocations. Track cost per agent, not just total session spend, so you can see where the expensive work is actually happening.</p>

  <pre><code>&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;
Token Economics
&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;
t1  engineer      322K tok
t2  engineer      394K tok
t3  judge         304K tok
&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;
Total tokens:  1,020K
Wall time:     6m 12s
CPU time:      14m 30s
Time saved:    ~55% via parallelism
&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;</code></pre>

  <p>The point of the report is not accounting precision. It is feedback. If planning is cheap and validation is expensive, that may be exactly right. If exploration is consuming the majority of tokens, your read-only fan-out is probably too heavy.</p>

  <h2>Next steps</h2>
  <div class="card-grid">
    <button class="card" data-section="prompting"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Knowledge Distance</h4><p>Close the right context gaps before you spend more</p></button>
    <button class="card" data-section="project-management"><span class="emoji" aria-hidden="true">&#x1F4CB;</span><h4>Planning for DAGs</h4><p>Spend effort where the critical path justifies it</p></button>
    <button class="card" data-section="operating-guides"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Operating Guides</h4><p>Return to the rest of the operating model</p></button>
  </div>
</section>
"""


def section_prompting() -> str:
    return f"""\
<section class="section" id="prompting">
{page_nav([("home", "Home"), ("operating-guides", "Operating Guides"), "Knowledge Distance"], 4)}
  <h1>&#x1F9ED; Knowledge Distance</h1>
  <p class="subtitle">A bad result does not mean you prompted wrong. It means the agent lacks context. Feed it.</p>

  <p><strong>Read this when:</strong> results are weak and you need to decide whether to add context, split the task, or distill knowledge into reusable rules.</p>
  <p><strong>What you get:</strong> A mental model for knowledge distance, context pressure, and when to use the Knowledge Manager instead of more prompt churn.</p>
  <h2>The knowledge distance problem</h2>
  <p>When an LLM gives a poor answer, the instinct is to rephrase the prompt or start over. Resist that instinct. The root cause is rarely the prompt &mdash; it is <strong>knowledge distance</strong>. The agent simply does not have enough context to produce a good answer.</p>

  <p>Large context windows let you provide far more material than most people instinctively use. A codebase slice, an ADR, an error trace, and a product spec can all fit into one working session. When the result is wrong, do not rephrase first. Add more context. Point the agent at more files. Paste in the error log. Include the spec. Close the knowledge distance, and the quality of responses rises dramatically.</p>

  <h2>What happens to all that context</h2>
  <p>Large context does not mean the model reasons about every token equally. Transformers read broadly and focus narrowly. By the time the agent answers, the huge input has effectively been compressed down to the handful of facts, constraints, and patterns that mattered most for the question.</p>

  <p>This is why <strong>more context usually helps</strong>. It gives the model more useful material to select from even though only a small fraction survives into the answer.</p>

  <h2>Why teaching sessions fill up fast</h2>
  <p>Learning sessions are where the main context window fills fastest. If you dump documentation, code samples, architecture decisions, and reference material into one conversation, the window eventually scrolls and earlier knowledge falls out.</p>

  <p>This is exactly why the <strong>Knowledge Manager</strong> exists. Instead of cramming everything into one session, the Knowledge Manager can start an independent chain of subagents. Each subagent gets its own fresh context window and returns a distilled result.</p>

  <h2>The distillation pipeline</h2>
  <p>Depending on your budget and appetite for iteration, you can fan out multiple subagents and feed them raw material in parallel. Each subagent distills its slice into structured findings, and a follow-on synthesis pass merges the results into high-density rules.</p>

  <table>
    <thead>
      <tr><th>Stage</th><th>Volume</th><th>What Happens</th></tr>
    </thead>
    <tbody>
      <tr><td>Raw input</td><td>Large, messy, source-shaped</td><td>Documentation, specs, code, logs fed to parallel subagents</td></tr>
      <tr><td>First distillation</td><td>Smaller, structured</td><td>Each agent produces findings or draft rules from its slice</td></tr>
      <tr><td>Refinement pass</td><td>Tighter, deduplicated</td><td>A synthesis pass merges, removes overlap, and tightens the wording</td></tr>
      <tr><td>Final polish</td><td>High-density instructions</td><td>Tables over prose, checklists over paragraphs, code blocks over explanation</td></tr>
    </tbody>
  </table>

  <p>That compression is the real point of the pipeline. Raw research is expensive to keep in every session. Distilled rules are cheap to load and change behavior immediately.</p>

  <h2>The refinement cycle</h2>
  <p>Distillation is cyclical. The first pass produces good rules. The second pass makes them sharper. The final pass makes them LLM-optimal: structured for how models actually consume information.</p>

  <ol>
    <li><strong>Ingest</strong> &mdash; Raw material lands in <code>src/rune-agency/knowledge/</code>.</li>
    <li><strong>Distill</strong> &mdash; The Knowledge Manager produces structured rules and findings.</li>
    <li><strong>Deploy</strong> &mdash; Rules are wired into profiles and used in real sessions.</li>
    <li><strong>Observe</strong> &mdash; You notice gaps, noise, and weak instructions.</li>
    <li><strong>Refine</strong> &mdash; Feed those observations back and tighten the material.</li>
  </ol>

  <h3>The budget trap</h3>
  <p>This cycle is powerful, but it is easy to overspend on learning. You can burn serious quota teaching and re-synthesizing material across agents, rules, and skills without shipping a line of production work. Set a budget before you start a knowledge-building session.</p>

  <table>
    <thead>
      <tr><th>Pass</th><th>Value captured</th><th>Cost profile</th><th>Recommendation</th></tr>
    </thead>
    <tbody>
      <tr><td>First distillation</td><td>Most of the value</td><td>Base cost</td><td>Always do this</td></tr>
      <tr><td>Refinement</td><td>Useful tightening</td><td>Additional overhead</td><td>Use for important rules</td></tr>
      <tr><td>Polish</td><td>Marginal gains</td><td>Additional overhead</td><td>Reserve for material loaded in many sessions</td></tr>
    </tbody>
  </table>

  <h2>Practical advice</h2>
  <ul>
    <li><strong>Bad result?</strong> Add context first, rephrase second, start over last.</li>
    <li><strong>Teaching the system?</strong> Use the Knowledge Manager, not the main conversation.</li>
    <li><strong>Large knowledge dump?</strong> Split across subagents so each gets a clean context window.</li>
    <li><strong>Refining rules?</strong> One pass is usually enough. Two for important rules. More only when the rule is heavily reused.</li>
    <li><strong>Budget?</strong> Decide before you start. Distillation can be addictive and expensive.</li>
  </ul>

  <h2>Next steps</h2>
  <div class="card-grid">
    <button class="card" data-section="operating-guides"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Operating Guides</h4><p>See how this guide fits the wider Rune operating model</p></button>
    <button class="card" data-section="knowledge-pipeline"><span class="emoji" aria-hidden="true">&#x1F4E5;</span><h4>Knowledge Pipeline</h4><p>How knowledge enters the system</p></button>
    <button class="card" data-section="token-economics"><span class="emoji" aria-hidden="true">&#x1F4B0;</span><h4>Token Economics</h4><p>Cost tracking and budgets</p></button>
    <button class="card" data-section="markdown-management"><span class="emoji" aria-hidden="true">&#x1F4C4;</span><h4>Documentation Structure</h4><p>Organize project documentation</p></button>
  </div>
</section>
"""


def build_core_concept(total_rules: int) -> str:
    return (
        section_four_phase_model()
        + section_phase_1_explore()
        + section_phase_2_plan()
        + section_phase_3_build()
        + section_phase_4_validate()
        + section_profiles(total_rules)
        + section_dag_dispatch()
    )
