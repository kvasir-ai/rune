"""Reference sections: documentation structure, planning for DAGs, references, glossary, sitemap."""
from __future__ import annotations

from ..shared import page_nav


def section_markdown_management(total_rules: int) -> str:
    return f"""\
<section class="section" id="markdown-management">
{page_nav([("home", "Home"), ("operating-guides", "Operating Guides"), "Documentation Structure"], 4)}
  <h1>&#x1F4C4; Documentation Structure</h1>
  <p class="subtitle">Organize project documentation so agents and humans can find source-of-truth quickly.</p>

  <p><strong>Read this when:</strong> the repo has docs, but agents still miss the right files, repeat settled decisions, or wander the tree blindly.</p>
  <p><strong>What you get:</strong> A practical layout for plans, ADRs, runbooks, `.rune/`, and a few habits that keep documentation useful as live context.</p>
  <h2>Recommended directory structure</h2>
  <p>Keep documentation close to the code. Use a flat, predictable layout that agents can navigate without guessing:</p>

  <pre><code>your-project/
&#x251C;&#x2500;&#x2500; docs/                    # Project documentation root
&#x2502;   &#x251C;&#x2500;&#x2500; plans/               # Active implementation plans
&#x2502;   &#x2502;   &#x251C;&#x2500;&#x2500; completed/       # Finished plans (archive, do not delete)
&#x2502;   &#x2502;   &#x251C;&#x2500;&#x2500; add-metrics.md
&#x2502;   &#x2502;   &#x2514;&#x2500;&#x2500; migrate-auth.md
&#x2502;   &#x251C;&#x2500;&#x2500; decisions/           # Architectural Decision Records
&#x2502;   &#x2502;   &#x251C;&#x2500;&#x2500; 001-use-grpc.md
&#x2502;   &#x2502;   &#x2514;&#x2500;&#x2500; 002-event-schema.md
&#x2502;   &#x251C;&#x2500;&#x2500; runbooks/            # Operational runbooks
&#x2502;   &#x2514;&#x2500;&#x2500; architecture.md      # High-level system overview
&#x251C;&#x2500;&#x2500; .rune/                   # Rune working directory (gitignored)
&#x2514;&#x2500;&#x2500; ...</code></pre>

  <h3>docs/plans/</h3>
  <p>Store implementation plans here. When the Planner produces a plan via <code>/write-plan</code>, save it to this directory. Active plans live at the top level. Move completed plans to <code>docs/plans/completed/</code> &mdash; archive them instead of deleting them. Old plans are valuable context for future planning.</p>

  <h3>docs/decisions/</h3>
  <p>Architectural Decision Records capture <em>why</em> a decision was made, not just what was decided. Number them sequentially. Each ADR should include context, the decision, consequences, and alternatives considered. Agents read these to avoid re-litigating settled decisions.</p>

  <h2>The .rune/ directory</h2>
  <p>The <code>.rune/</code> directory is Rune&rsquo;s working directory inside your project. It stores session-specific workflow state and execution artifacts that should stay local to the machine running the work.</p>

  <table>
    <thead>
      <tr><th>Path</th><th>Purpose</th></tr>
    </thead>
    <tbody>
      <tr><td><code>.rune/session-state.json</code></td><td>Active workflow state used by hooks and stage transitions</td></tr>
      <tr><td><code>.rune/</code> scratch artifacts</td><td>Local execution metadata and temporary workflow files</td></tr>
    </tbody>
  </table>

  <p>Add <code>.rune/</code> to your <code>.gitignore</code>. It contains local working data rather than durable project knowledge.</p>

  <pre><code># .gitignore
.rune/</code></pre>

  <h2>INDEX.md &mdash; a project map</h2>
  <p>Consider adding an <code>INDEX.md</code> at the root of <code>docs/</code>. This acts as a table of contents that both humans and agents can scan quickly:</p>

  <pre><code># docs/INDEX.md

## Plans
- [Add metrics pipeline](plans/add-metrics.md) &mdash; active
- [Migrate auth to OAuth2](plans/migrate-auth.md) &mdash; active
- [Add caching layer](plans/completed/add-caching.md) &mdash; done

## ADRs
- [001 Use gRPC](decisions/001-use-grpc.md)
- [002 Event schema design](decisions/002-event-schema.md)

## Runbooks
- [Deploy to production](runbooks/deploy.md)
- [Rotate secrets](runbooks/rotate-secrets.md)</code></pre>

  <p>When an agent needs to understand the project, telling it to read <code>docs/INDEX.md</code> first is usually cheaper and cleaner than having it wander the tree blind.</p>

  <h2>Documents as context</h2>
  <p>Markdown files in your project are a valuable source of context for agents. Plans, ADRs, and runbooks contain the <em>why</em> behind the code, not just the code itself.</p>

  <ul>
    <li><strong>Point agents at docs.</strong> Context before action.</li>
    <li><strong>Keep docs current.</strong> Outdated docs actively mislead agents.</li>
    <li><strong>Write for machines too.</strong> Prefer headings, tables, and code blocks over long prose walls.</li>
  </ul>

  <h2>The 500-line rule</h2>
  <p>Any agent, rule, or skill file longer than 500 lines is usually too long. Long files dilute attention, waste context tokens, and increase cost without proportional benefit.</p>

  <ol>
    <li>Distill prose into tables, checklists, and code examples.</li>
    <li>Move background reading into <code>docs/</code>.</li>
    <li>Keep action-oriented instructions in rules and skills.</li>
  </ol>

  <h2>Context hygiene: one context, one mission</h2>
  <p>A context window has a fixed size. Every file read, every instruction loaded, and every message in the conversation takes up space. When one context tries to serve too many goals at once, the quality of every goal suffers.</p>

  <p>This is not a model failure. It is a design failure. An agent asked to debug a pipeline, review a pull request, and draft a status update in the same thread will do all three worse than three focused agents working in clean contexts.</p>

  <h3>The signs of a diverging context</h3>
  <ul>
    <li>You are switching topics mid-session.</li>
    <li>The agent references stale material from many turns ago instead of the current task.</li>
    <li>You feel tempted to copy the conversation into a new chat just to reset it.</li>
    <li>The agent starts hedging or contradicting earlier answers.</li>
  </ul>

  <h3>How Rune is designed around this</h3>
  <table>
    <thead>
      <tr><th>Mechanism</th><th>How it prevents diverging context</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Phases</strong></td><td>Explore, Plan, Build, and Validate each have one job.</td></tr>
      <tr><td><strong>Subagents</strong></td><td>Each dispatched task gets a fresh context window and returns only a short summary.</td></tr>
      <tr><td><strong>Profiles</strong></td><td>Only the rules relevant to one kind of work load at session start.</td></tr>
      <tr><td><strong>Rules</strong></td><td>Background knowledge is preloaded rather than rediscovered mid-task.</td></tr>
    </tbody>
  </table>

  <h3>Practical guidelines</h3>
  <ol>
    <li><strong>One goal per session.</strong> Start a new session when the task changes significantly.</li>
    <li><strong>Split large tasks into a plan.</strong> If a task spans domains or many files, use <code>/write-plan</code> and dispatch with <code>/rune</code>.</li>
    <li><strong>Do not paste everything in.</strong> Distill large knowledge dumps before loading them repeatedly.</li>
    <li><strong>Switch profiles when the work changes.</strong> Review work needs different context from implementation work.</li>
    <li><strong>Let subagents read.</strong> If a file is large and you only need a summary, dispatch Explore rather than dragging the whole thing into the main context.</li>
  </ol>

  <h2>Next steps</h2>
  <div class="card-grid">
    <button class="card" data-section="operating-guides"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Operating Guides</h4><p>Return to the full operating-model lane</p></button>
    <button class="card" data-section="knowledge-pipeline"><span class="emoji" aria-hidden="true">&#x1F4E5;</span><h4>Knowledge Pipeline</h4><p>How rules are created</p></button>
    <button class="card" data-section="prompting"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Knowledge Distance</h4><p>Knowledge distance and economics</p></button>
    <button class="card" data-section="rules-catalog"><span class="emoji" aria-hidden="true">&#x1F4DA;</span><h4>Rules Catalog</h4><p>Browse all {total_rules} rules</p></button>
  </div>
</section>
"""


def section_project_management() -> str:
    return f"""\
<section class="section" id="project-management">
{page_nav([("home", "Home"), ("operating-guides", "Operating Guides"), "Planning for DAGs"], 4)}
  <h1>&#x1F4CB; Planning for DAGs</h1>
  <p class="subtitle">Project-planning principles, Work Breakdown Structures, and how they map to Rune execution waves.</p>

  <p><strong>Read this when:</strong> you know the feature scope, but need to turn it into planner-ready tasks, dependencies, and parallel waves.</p>
  <p><strong>What you get:</strong> A bridge from classic planning concepts to Rune tasks, `depends_on` relationships, and critical-path thinking.</p>
  <p>Rune Agency&rsquo;s four-phase model is grounded in structured project management practice. Understanding that foundation makes the dispatch model easier to use well.</p>

  <h2>The 7 planning principles</h2>
  <p>Sound project delivery rests on a small set of universal principles. Each one maps directly to how Rune coordinates agents:</p>

  <table>
    <thead>
      <tr><th>#</th><th>Principle</th><th>Rune Agency Mapping</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td><strong>Continued justification</strong></td><td>Every plan must have a valid reason to proceed. If justification weakens, stop and reassess.</td></tr>
      <tr><td>2</td><td><strong>Learn from experience</strong></td><td>The Knowledge Manager captures lessons and turns them into reusable rules.</td></tr>
      <tr><td>3</td><td><strong>Clear roles and responsibilities</strong></td><td>Every task is assigned to a named agent. Ownership is explicit.</td></tr>
      <tr><td>4</td><td><strong>Stage-by-stage delivery</strong></td><td>Explore &rarr; Plan &rarr; Build &rarr; Validate with clear handoffs.</td></tr>
      <tr><td>5</td><td><strong>Manage by exception</strong></td><td>Agents work autonomously inside scope and escalate when they hit a real exception.</td></tr>
      <tr><td>6</td><td><strong>Focus on outputs</strong></td><td>Every task defines its <code>output</code> before work begins.</td></tr>
      <tr><td>7</td><td><strong>Tailor to context</strong></td><td>Profiles adapt rules and knowledge to the task at hand.</td></tr>
    </tbody>
  </table>

  <h2>Work Breakdown Structures</h2>
  <p>A Work Breakdown Structure decomposes a deliverable into smaller, manageable components. It tells you <em>what</em> needs to be done before you decide <em>in what order</em> to do it.</p>

  <pre><code>Feature: User Authentication
&#x251C;&#x2500;&#x2500; 1. Design
&#x2502;   &#x251C;&#x2500;&#x2500; 1.1 API contract
&#x2502;   &#x2514;&#x2500;&#x2500; 1.2 Database schema
&#x251C;&#x2500;&#x2500; 2. Implement
&#x2502;   &#x251C;&#x2500;&#x2500; 2.1 Auth handler
&#x2502;   &#x251C;&#x2500;&#x2500; 2.2 Token service
&#x2502;   &#x2514;&#x2500;&#x2500; 2.3 Middleware
&#x251C;&#x2500;&#x2500; 3. Test
&#x2502;   &#x251C;&#x2500;&#x2500; 3.1 Unit tests
&#x2502;   &#x2514;&#x2500;&#x2500; 3.2 Integration tests
&#x2514;&#x2500;&#x2500; 4. Review
    &#x2514;&#x2500;&#x2500; 4.1 Security audit</code></pre>

  <h3>From WBS to DAG</h3>
  <p>The WBS becomes a DAG when you add dependencies. The WBS answers &ldquo;what are all the pieces?&rdquo; The DAG answers &ldquo;what can run in parallel, and what must wait?&rdquo;</p>

  <pre><code>WBS leaf nodes                    DAG tasks
&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;                   &#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;
1.1 API contract        &#x2500;&#x2500;&#x2500;&rarr;     t1  engineer      (wave 0)
1.2 Database schema     &#x2500;&#x2500;&#x2500;&rarr;     t2  engineer      (wave 0)
2.1 Auth handler        &#x2500;&#x2500;&#x2500;&rarr;     t3  engineer      (wave 1, depends t1, t2)
2.2 Token service       &#x2500;&#x2500;&#x2500;&rarr;     t4  engineer      (wave 1, depends t1)
2.3 Middleware          &#x2500;&#x2500;&#x2500;&rarr;     t5  engineer      (wave 1, depends t3, t4)
3.1 Unit tests          &#x2500;&#x2500;&#x2500;&rarr;     t6  engineer      (wave 2, depends t3, t4, t5)
3.2 Integration tests   &#x2500;&#x2500;&#x2500;&rarr;     t7  engineer      (wave 2, depends t3, t4, t5)
4.1 Security audit      &#x2500;&#x2500;&#x2500;&rarr;     t8  judge         (wave 3, depends t6, t7)</code></pre>

  <p>The Planner performs this transformation: decompose, assign, sequence, and hand the result to the dispatcher.</p>

  <h2>The Planner as project manager</h2>
  <table>
    <thead>
      <tr><th>PM responsibility</th><th>Planner equivalent</th></tr>
    </thead>
    <tbody>
      <tr><td>Scope decomposition</td><td>Breaks a feature into atomic tasks</td></tr>
      <tr><td>Resource assignment</td><td>Assigns an agent type to each task</td></tr>
      <tr><td>Sequencing</td><td>Defines <code>depends_on</code> relationships</td></tr>
      <tr><td>Schedule optimization</td><td>Dispatcher computes execution waves for parallelism</td></tr>
      <tr><td>Risk identification</td><td>Conflicts, missing work, and bad dependency structure</td></tr>
      <tr><td>Progress tracking</td><td>Wave-by-wave execution with reports and summaries</td></tr>
    </tbody>
  </table>

  <h3>The 100% rule</h3>
  <p>The most important WBS principle is the 100% rule: the decomposition must capture the full scope. In Rune terms, every real change should be accounted for by some task. If files or deliverables fall outside the DAG, the plan is incomplete.</p>

  <h3>The 8/80 rule</h3>
  <p>Traditional WBS guidance says a work package should be neither too small nor too large. The Rune equivalent is similar: each task should be large enough to justify dispatching an agent, but small enough for one agent to finish without swallowing the whole project.</p>

  <h2>Critical path and parallelism</h2>
  <p>The critical path is the longest chain of dependent tasks through the DAG. It determines the minimum wall time. No amount of parallelism can shorten work that sits on the critical path.</p>

  <pre><code>DAG with 8 tasks:

Wave 0:  t1, t2           (parallel)
Wave 1:  t3, t4           (parallel, depend on wave 0)
Wave 2:  t5               (depends on t3, t4)
Wave 3:  t6, t7           (parallel, depend on t5)
Wave 4:  t8               (depends on t6, t7)

Critical path: t1 &rarr; t3 &rarr; t5 &rarr; t6 &rarr; t8
</code></pre>

  <h3>Optimizing the DAG</h3>
  <ul>
    <li><strong>Minimize dependencies.</strong> Only add them when a task genuinely needs the output.</li>
    <li><strong>Front-load independent work.</strong> Put as much true parallelism as possible into early waves.</li>
    <li><strong>Separate reading from writing.</strong> Explore is mostly parallel; Build is where dependencies tighten.</li>
    <li><strong>Review tasks go last.</strong> Validation is a gate, not a background activity.</li>
  </ul>

  <h2>When the analogy breaks down</h2>
  <table>
    <thead>
      <tr><th>Project management</th><th>DAG dispatch</th></tr>
    </thead>
    <tbody>
      <tr><td>Tasks take hours to weeks</td><td>Tasks take seconds to minutes</td></tr>
      <tr><td>Resources are humans with judgment</td><td>Resources are models working within scoped prompts</td></tr>
      <tr><td>Communication is rich and continuous</td><td>Communication is compressed into summaries between waves</td></tr>
      <tr><td>Replanning is expensive</td><td>Replanning is relatively cheap</td></tr>
      <tr><td>Scope creep is common</td><td>Scope is constrained by the plan unless explicitly changed</td></tr>
    </tbody>
  </table>

  <h2>Next steps</h2>
  <div class="card-grid">
    <button class="card" data-section="operating-guides"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Operating Guides</h4><p>Return to the wider Rune operating model</p></button>
    <button class="card" data-section="dag-dispatch"><span class="emoji" aria-hidden="true">&#x1F500;</span><h4>DAG Dispatch</h4><p>Context squeezing and parallel execution</p></button>
    <button class="card" data-section="token-economics"><span class="emoji" aria-hidden="true">&#x1F4B0;</span><h4>Token Economics</h4><p>Cost tracking and context budgets</p></button>
    <button class="card" data-section="four-phase-model"><span class="emoji" aria-hidden="true">&#x1F3AF;</span><h4>Four-Phase Model</h4><p>The full workflow</p></button>
  </div>
</section>
"""


def section_references() -> str:
    return f"""\
<section class="section" id="reference-overview">
{page_nav([("home", "Home"), "Reference"])}
  <h1>&#x1F4DA; Reference</h1>
  <p class="subtitle">Appendix pages for external sources, shared terms, and full-site lookup.</p>

  <p>Use this lane when you want neutral lookup material rather than guidance. The pages here support the rest of the docs: they define terms, point to upstream concepts, and expose the full site structure without adding another operating model.</p>

  <h2>Use this lane</h2>
  <table>
    <thead>
      <tr><th>Page</th><th>Open it when</th></tr>
    </thead>
    <tbody>
      <tr><td><button data-section="references">References</button></td><td>You want the outside concepts and source material Rune builds on.</td></tr>
      <tr><td><button data-section="glossary">Glossary</button></td><td>You need a fast definition for a term used elsewhere in the docs.</td></tr>
      <tr><td><button data-section="sitemap">Sitemap</button></td><td>You want the full table of contents for the generated site.</td></tr>
    </tbody>
  </table>
</section>

<section class="section" id="references">
{page_nav([("home", "Home"), ("reference-overview", "Reference"), "References"])}
  <h1>&#x1F517; References</h1>
  <p class="subtitle">External sources and concepts that inform Rune&rsquo;s design.</p>

  <p>These are upstream ideas, formats, and public references that the docs mention elsewhere. Use them when you want the source concept, not Rune&rsquo;s interpretation of it.</p>
  <ul>
    <li><strong><a href="https://github.com/msitarzewski/agency-agents" target="_blank" rel="noopener">The Agency</a></strong>: A practical example of structured agent roles and clear specialist boundaries.</li>
    <li><strong><a href="https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f" target="_blank" rel="noopener">LLM Wiki Pattern</a></strong>: A simple pattern for keeping reusable knowledge in markdown instead of repeating it in every session.</li>
    <li><strong><a href="https://github.com/joelparkerhenderson/architecture-decision-record" target="_blank" rel="noopener">ADRs</a></strong>: A common way to record important technical decisions, context, and tradeoffs.</li>
    <li><strong><a href="https://en.wikipedia.org/wiki/Directed_acyclic_graph" target="_blank" rel="noopener">Directed Acyclic Graph</a></strong>: Rune uses DAGs to represent task dependencies, compute execution waves, and keep parallel work explicit.</li>
    <li><strong><a href="https://en.wikipedia.org/wiki/Work_breakdown_structure" target="_blank" rel="noopener">Work Breakdown Structure</a></strong>: A basic planning method for splitting large work into smaller parts before execution order is added.</li>
    <li><strong><a href="https://en.wikipedia.org/wiki/Levenshtein_distance" target="_blank" rel="noopener">Levenshtein Distance</a></strong>: A simple example of distance between two text states. It is a useful way to think about Rune&rsquo;s idea of <strong>Knowledge Distance</strong>: how far the current context is from the context the task actually needs.</li>
  </ul>
</section>

"""


def section_glossary() -> str:
    return f"""\
<section class="section" id="glossary">
{page_nav([("home", "Home"), ("reference-overview", "Reference"), "Glossary"])}
  <h1>&#x1F4D6; Glossary</h1>
  <p>Key terms used throughout this documentation, organized by category.</p>

  <nav class="gloss-legend" aria-label="Glossary categories">
    <button data-scroll-to="gloss-ai" class="gloss-badge gloss-ai">AI Foundations</button>
    <button data-scroll-to="gloss-kit" class="gloss-badge gloss-kit">Toolkit Architecture</button>
    <button data-scroll-to="gloss-exec" class="gloss-badge gloss-exec">Execution &amp; Dispatch</button>
    <button data-scroll-to="gloss-know" class="gloss-badge gloss-know">Knowledge &amp; Context</button>
  </nav>

  <h2 id="gloss-ai" class="gloss-section-heading">AI Foundations</h2>
  <table>
    <thead><tr><th>Term</th><th>Definition</th></tr></thead>
    <tbody>
      <tr class="gloss-row gloss-ai"><td><strong>Agent&rsquo;s working memory</strong></td><td>The text the agent can see at one time. Rules, instructions, and conversation history all share this fixed space.</td></tr>
      <tr class="gloss-row gloss-ai"><td><strong>Context window</strong></td><td>The maximum number of <a href="https://en.wikipedia.org/wiki/Lexical_analysis#Token" target="_blank" rel="noopener">tokens</a> an LLM can process in a single request. Typical sizes range from 128K to 1M tokens.</td></tr>
      <tr class="gloss-row gloss-ai"><td><strong>LLM</strong></td><td><a href="https://en.wikipedia.org/wiki/Large_language_model" target="_blank" rel="noopener">Large Language Model</a>. A neural network trained on text that generates responses from a prompt and its current context.</td></tr>
      <tr class="gloss-row gloss-ai"><td><strong>MCP</strong></td><td><a href="https://modelcontextprotocol.io/" target="_blank" rel="noopener">Model Context Protocol</a>. A standard for connecting models to external tools and data sources.</td></tr>
      <tr class="gloss-row gloss-ai"><td><strong>Token</strong></td><td>The smallest unit of text an LLM processes. Roughly four characters or three quarters of a word. You pay per token.</td></tr>
    </tbody>
  </table>

  <h2 id="gloss-kit" class="gloss-section-heading">Toolkit Architecture</h2>
  <table>
    <thead><tr><th>Term</th><th>Definition</th></tr></thead>
    <tbody>
      <tr class="gloss-row gloss-kit"><td><strong>Agent</strong></td><td>A markdown file with YAML frontmatter and a system prompt. Rune loads the full prompt only when the agent is actually invoked.</td></tr>
      <tr class="gloss-row gloss-kit"><td><strong>Hook</strong></td><td>A script that intercepts lifecycle events before or after tool execution. Rune uses hooks for safety checks, workflow discipline, and automatic formatting.</td></tr>
      <tr class="gloss-row gloss-kit"><td><strong>Knowledge Manager (KM)</strong></td><td>The core agent responsible for ingesting raw material and distilling it into reusable rules, profiles, and guidance.</td></tr>
      <tr class="gloss-row gloss-kit"><td><strong>Profile</strong></td><td>A named set of rules and resources that load into context together. Switching profiles changes what the team knows without changing the agents themselves.</td></tr>
      <tr class="gloss-row gloss-kit"><td><strong>Rule</strong></td><td>A structured markdown file in <code>.claude/rules/</code> containing conventions, patterns, and architectural guidance that agents are expected to follow.</td></tr>
      <tr class="gloss-row gloss-kit"><td><strong>Skill</strong></td><td>A slash-command workflow that launches a structured task pattern on demand. Skills cost zero context until you invoke them.</td></tr>
    </tbody>
  </table>

  <h2 id="gloss-exec" class="gloss-section-heading">Execution &amp; Dispatch</h2>
  <table>
    <thead><tr><th>Term</th><th>Definition</th></tr></thead>
    <tbody>
      <tr class="gloss-row gloss-exec"><td><strong>DAG</strong></td><td><a href="https://en.wikipedia.org/wiki/Directed_acyclic_graph" target="_blank" rel="noopener">Directed Acyclic Graph</a>. A dependency graph where tasks point to prerequisites. Rune uses DAGs to determine execution order and parallel waves.</td></tr>
      <tr class="gloss-row gloss-exec"><td><strong>Dispatching</strong></td><td>Sending a task to an agent and waiting for the result. In Rune, dispatching follows the task plan and hands compact summaries between waves.</td></tr>
      <tr class="gloss-row gloss-exec"><td><strong>Subagent</strong></td><td>An agent dispatched to perform one scoped task. It gets a fresh context window and returns a short result to the parent workflow.</td></tr>
      <tr class="gloss-row gloss-exec"><td><strong>Topological sort</strong></td><td><a href="https://en.wikipedia.org/wiki/Topological_sorting" target="_blank" rel="noopener">Algorithm</a> that orders a DAG so every task appears after its dependencies. This is how execution waves are computed.</td></tr>
      <tr class="gloss-row gloss-exec"><td><strong>Wave</strong></td><td>A set of tasks with no mutual dependencies that can run in parallel. Wave 0 runs first; later waves wait for earlier dependencies to finish.</td></tr>
    </tbody>
  </table>

  <h2 id="gloss-know" class="gloss-section-heading">Knowledge &amp; Context</h2>
  <table>
    <thead><tr><th>Term</th><th>Definition</th></tr></thead>
    <tbody>
      <tr class="gloss-row gloss-know"><td><strong>ADR</strong></td><td><a href="https://en.wikipedia.org/wiki/Architectural_decision" target="_blank" rel="noopener">Architectural Decision Record</a>. A short document that captures a design decision, the context around it, and its consequences.</td></tr>
      <tr class="gloss-row gloss-know"><td><strong>Context compression</strong></td><td>Reducing a large amount of information to a compact summary before passing it to the next agent or wave. This keeps working memory from filling up.</td></tr>
      <tr class="gloss-row gloss-know"><td><strong>Distillation</strong></td><td>The process of compressing raw material into structured, model-friendly rules. It removes fluff and preserves the parts that change decisions.</td></tr>
      <tr class="gloss-row gloss-know"><td><strong>Knowledge distance</strong></td><td>The gap between what an agent currently knows and what it needs to know to answer well. Close the gap by supplying context, not by endlessly rephrasing the prompt.</td></tr>
    </tbody>
  </table>
</section>
"""


def section_sitemap(
    total_agents: int,
    total_skills: int,
    total_rules: int,
) -> str:
    return f"""\
<section class="section" id="sitemap">
{page_nav([("home", "Home"), ("reference-overview", "Reference"), "Sitemap"])}
  <h1>&#x1F30D; Sitemap</h1>
  <p>All pages in this documentation, organized by section.</p>

  <h3>Getting Started</h3>
  <ul>
    <li><button data-section="home">Home</button> &mdash; Overview, stats, and learning path</li>
    <li><button data-section="quick-start">Quick Start</button> &mdash; Install, configure, and verify Rune</li>
    <li><button data-section="talk">Talk to Your Team</button> &mdash; Natural-language interaction patterns</li>
  </ul>

  <h3>The Core Concept</h3>
  <ul>
    <li><button data-section="four-phase-model">Four-Phase Model</button> &mdash; Overview of the full workflow</li>
    <li><button data-section="phase-1-explore">Phase 1: Explore</button> &mdash; Gather context before acting</li>
    <li><button data-section="phase-2-plan">Phase 2: Plan</button> &mdash; Decompose work into a DAG</li>
    <li><button data-section="phase-3-build">Phase 3: Build</button> &mdash; Execute the plan in parallel waves</li>
    <li><button data-section="phase-4-validate">Phase 4: Validate</button> &mdash; Review and verification gate</li>
    <li><button data-section="profiles">Profiles</button> &mdash; Load the rules and resources the task needs</li>
    <li><button data-section="dag-dispatch">DAG Dispatch</button> &mdash; Run work in dependency waves</li>
  </ul>

  <h3>Rune Agency</h3>
  <ul>
    <li><button data-section="agents">Agents</button> &mdash; Agent catalog ({total_agents} agents)</li>
    <li><button data-section="agent-onboarding">Onboarding an Agent</button> &mdash; Recruit or write new specialists</li>
    <li><button data-section="skills">Skills</button> &mdash; Structured slash-command workflows ({total_skills} skills)</li>
    <li><button data-section="rules-catalog">Rules</button> &mdash; Shared knowledge library ({total_rules} rules)</li>
  </ul>

  <h3>Manual Pages</h3>
  <ul>
    <li><button data-section="rune-cheatsheet">Quick Reference</button> &mdash; Fast lookup companion to RUNE(1)</li>
    <li><button data-section="rune-man-1">RUNE(1)</button> &mdash; Main command reference for the rune CLI</li>
    <li><button data-section="rune-cli-top">Top-Level Commands</button> &mdash; Setup, demo, and reset</li>
    <li><button data-section="rune-cli-profile">Profile Commands</button> &mdash; Apply, list, and budget profiles</li>
    <li><button data-section="rune-cli-resource">Resource Commands</button> &mdash; Inspect agents, rules, and skills</li>
    <li><button data-section="rune-cli-system">System Commands</button> &mdash; Verify, validate, and generate the site</li>
    <li><button data-section="rune-cli-mcp">MCP Commands</button> &mdash; Manage Model Context Protocol servers</li>
    <li><button data-section="rune-man-env">Environment &amp; Files</button> &mdash; Exit codes and environment variables</li>
    <li><button data-section="rune-man-profiles">RUNE-PROFILES(5)</button> &mdash; Profile reference</li>
    <li><button data-section="rune-man-tools">RUNE-TOOLS(7)</button> &mdash; Optional system tools</li>
  </ul>

  <h3>Operating Guides</h3>
  <ul>
    <li><button data-section="operating-guides">Operating Guides</button> &mdash; Overview of Rune&rsquo;s advanced operating model</li>
    <li><button data-section="knowledge-pipeline">Knowledge Pipeline</button> &mdash; Turn raw material into reusable rules</li>
    <li><button data-section="token-economics">Token Economics</button> &mdash; Cost tracking, context budgets, and lean profiles</li>
    <li><button data-section="prompting">Knowledge Distance</button> &mdash; Close context gaps before you rewrite prompts</li>
    <li><button data-section="markdown-management">Documentation Structure</button> &mdash; Plans, ADRs, and context hygiene</li>
    <li><button data-section="project-management">Planning for DAGs</button> &mdash; Translate project scope into execution waves</li>
  </ul>

  <h3>Hooks</h3>
  <ul>
    <li><button data-section="hooks-overview">Overview</button> &mdash; What hooks are and how to read this lane</li>
    <li><button data-section="hook-safety-check">Safety Check</button> &mdash; Blocks destructive command patterns</li>
    <li><button data-section="hook-auto-lint">Auto-Lint</button> &mdash; Runs formatters after file writes</li>
    <li><button data-section="hook-stage-complete">Stage Complete</button> &mdash; Suggests the next workflow step</li>
    <li><button data-section="hook-context-awareness">Context Awareness</button> &mdash; Warns when context pressure is high</li>
    <li><button data-section="hook-done-criteria">Done Criteria</button> &mdash; Reminds the agent to verify before stopping</li>
    <li><button data-section="hook-plan-mode-rules">Plan Mode Rules</button> &mdash; Reinforces planning discipline</li>
    <li><button data-section="hook-session-discipline">Session Discipline</button> &mdash; Keeps workflow state in view</li>
  </ul>

  <h3>Reference</h3>
  <ul>
    <li><button data-section="reference-overview">Overview</button> &mdash; Appendix landing page for sources, terms, and lookup</li>
    <li><button data-section="references">References</button> &mdash; External concepts Rune builds on</li>
    <li><button data-section="glossary">Glossary</button> &mdash; Key terms and definitions</li>
    <li><button data-section="sitemap">Sitemap</button> &mdash; This page</li>
  </ul>
</section>
"""


def build_reference(
    total_rules: int,
    total_agents: int,
    total_skills: int,
) -> str:
    return (
        section_references()
        + section_glossary()
        + section_sitemap(total_agents, total_skills, total_rules)
    )
