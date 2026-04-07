"""Operating Guides sections: advanced Rune operating-model documentation."""
from __future__ import annotations

from .core_concept import (
    section_knowledge_pipeline,
    section_prompting,
    section_token_economics,
)
from .reference import (
    section_markdown_management,
    section_project_management,
)
from .shared import page_nav


def section_operating_guides() -> str:
    return """\
<section class="section" id="operating-guides">
{nav}
  <h1>&#x1F9ED; Operating Guides</h1>
  <p class="subtitle">Advanced guides for how Rune stays lean, teachable, and scalable after the core workflow already makes sense.</p>

  <p>These pages explain the operating model behind Rune rather than the installation path or the basic four phases. Read them when you want the reasoning behind the system: how knowledge becomes rules, how context stays focused, how cost stays visible, and how planning turns into execution waves.</p>

  <h2>Use this lane</h2>
  <table>
    <thead>
      <tr><th>Guide</th><th>Read it when</th></tr>
    </thead>
    <tbody>
      <tr><td><button data-section="knowledge-pipeline">Knowledge Pipeline</button></td><td>You want Rune to learn something reusable instead of repeating context dumps.</td></tr>
      <tr><td><button data-section="prompting">Knowledge Distance</button></td><td>The model is under-informed and you need to decide between more context, distillation, or a narrower task.</td></tr>
      <tr><td><button data-section="token-economics">Token Economics</button></td><td>You need to control budget, profile size, or model mix across a real workflow.</td></tr>
      <tr><td><button data-section="markdown-management">Documentation Structure</button></td><td>You want plans, ADRs, and other docs to act like durable context instead of dead files.</td></tr>
      <tr><td><button data-section="project-management">Planning for DAGs</button></td><td>You need to translate project scope into explicit tasks, dependencies, and execution waves.</td></tr>
    </tbody>
  </table>

  <h2>Guides</h2>
  <div class="card-grid">
    <button class="card" data-section="knowledge-pipeline"><span class="emoji" aria-hidden="true">&#x1F4E5;</span><h4>Knowledge Pipeline</h4><p>Turn raw material into durable rules</p></button>
    <button class="card" data-section="prompting"><span class="emoji" aria-hidden="true">&#x1F9ED;</span><h4>Knowledge Distance</h4><p>Know when to add context, distill, or split the work</p></button>
    <button class="card" data-section="token-economics"><span class="emoji" aria-hidden="true">&#x1F4B0;</span><h4>Token Economics</h4><p>Control cost, context budgets, and model mix</p></button>
    <button class="card" data-section="markdown-management"><span class="emoji" aria-hidden="true">&#x1F4C4;</span><h4>Documentation Structure</h4><p>Keep plans, ADRs, and docs easy to navigate</p></button>
    <button class="card" data-section="project-management"><span class="emoji" aria-hidden="true">&#x1F4CB;</span><h4>Planning for DAGs</h4><p>Translate project scope into runnable execution waves</p></button>
  </div>
</section>
""".format(nav=page_nav([("home", "Home"), "Operating Guides"], 4))


def build_operating_guides(total_rules: int) -> str:
    return (
        section_operating_guides()
        + section_knowledge_pipeline(total_rules)
        + section_prompting()
        + section_token_economics()
        + section_markdown_management(total_rules)
        + section_project_management()
    )
