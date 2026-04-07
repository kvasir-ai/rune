"""Demo command showcasing the Four Phase Model."""

from __future__ import annotations

import time
from dataclasses import dataclass

import click
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.tree import Tree


REQUEST = '"plan a REST API for user management"'
INTRO_DELAY = 0.4
STEP_DELAY = 0.3
SUMMARY_STEP_DELAY = 0.25
SECTION_SETTLE_DELAY = 1.0
FINAL_READOUT_DELAY = 1.5
TREE_PANEL_WIDTH = 68


@dataclass(frozen=True)
class PhaseSpec:
    """One phase in the guided demo flow."""

    emoji: str
    title: str
    style: str
    spinner: str
    goal: str
    framing: str
    artifact_in: str
    artifact_out: str
    agents: tuple[str, ...]
    actions: tuple[str, ...]
    skills: tuple[str, ...]
    build_waves: tuple[tuple[str, ...], ...] = ()


PHASES: tuple[PhaseSpec, ...] = (
    PhaseSpec(
        emoji="🔍",
        title="Phase 1: Explore",
        style="cyan",
        spinner="dots",
        goal="Read the codebase before writing anything",
        framing="Understand the problem first. Dispatch read-only agents in parallel and return short summaries.",
        artifact_in="Vague request",
        artifact_out="Context summary",
        agents=("Developer (Haiku)", "Researcher (Haiku)", "Security (Haiku)", "Tester (Haiku)"),
        actions=(
            "Read the existing API structure",
            "Check dependencies and compliance constraints",
            "Return distilled findings for the planner",
        ),
        skills=("/km-explore",),
    ),
    PhaseSpec(
        emoji="📐",
        title="Phase 2: Plan",
        style="magenta",
        spinner="line",
        goal="Decompose work into small, parallelizable tasks",
        framing="The Planner turns the exploration summary into a DAG with owners, dependencies, and outputs.",
        artifact_in="Context summary",
        artifact_out="PLAN.md",
        agents=("Planner (Opus)",),
        actions=(
            "Break the work into atomic tasks",
            "Annotate dependencies and owners",
            "Write the execution plan artifact",
        ),
        skills=("/write-plan",),
    ),
    PhaseSpec(
        emoji="🔨",
        title="Phase 3: Build",
        style="yellow",
        spinner="bouncingBar",
        goal="Execute the plan wave by wave",
        framing="The dispatcher groups independent tasks into waves and injects short summaries into downstream work.",
        artifact_in="PLAN.md",
        artifact_out="Wave summaries",
        agents=("Engineer (Sonnet)", "Tester (Haiku)"),
        actions=(
            "Dispatch Wave 0 in parallel",
            "Inject summaries into dependent tasks",
        ),
        skills=("/rune", "/tw-draft-pr"),
        build_waves=(
            (
                "Wave 0 · Engineer designs the API contract",
                "Wave 0 · Engineer designs the database schema",
            ),
            (
                "Wave 1 · Engineer implements handlers",
                "Wave 1 · Tester writes tests",
            ),
        ),
    ),
    PhaseSpec(
        emoji="✅",
        title="Phase 4: Validate",
        style="green",
        spinner="arc",
        goal="Verify output before shipping",
        framing="The Judge checks correctness, safety, completeness, and the edge cases the builder may have missed.",
        artifact_in="Wave summaries",
        artifact_out="Approval verdict",
        agents=("Judge (Opus)", "Engineer (Sonnet · Review Mode)"),
        actions=(
            "Review correctness, safety, and completeness",
            "Check edge cases and missing tests",
            "Approve or send changes back",
        ),
        skills=("/judge", "/judge-audit", "/judge-panel 3"),
    ),
)


def _sleep(delay: float, animated: bool, fast: bool) -> None:
    """Sleep only when animation is enabled."""

    if not animated:
        return
    multiplier = 0.45 if fast else 1.0
    time.sleep(delay * multiplier)


def _render_progress(current_index: int) -> Text:
    """Render a compact phase progress strip."""

    progress = Text("Workflow Progress  ", style="bold white")
    for index, phase in enumerate(PHASES):
        if index < current_index:
            progress.append("● ", style="bold green")
            progress.append(phase.title.replace("Phase ", ""), style="dim")
        elif index == current_index:
            progress.append("▶ ", style=f"bold {phase.style}")
            progress.append(phase.title.replace("Phase ", ""), style=f"bold {phase.style}")
        else:
            progress.append("○ ", style="dim")
            progress.append(phase.title.replace("Phase ", ""), style="dim")
        if index != len(PHASES) - 1:
            progress.append("  ")
    return progress


def _tree_item_style(index: int, revealed_count: int, active_index: int | None, phase_style: str) -> str:
    """Return the style for a tree item based on reveal progress."""

    if revealed_count <= 0 or index >= revealed_count:
        return "dim"
    if active_index is not None and index == active_index:
        return f"bold black on {phase_style}"
    return f"bold {phase_style}"


def _wave_item_count(phase: PhaseSpec) -> int:
    """Count the total number of build-wave items in a phase."""

    return sum(len(wave) for wave in phase.build_waves)


def _phase_reveal_total(phase: PhaseSpec) -> int:
    """Count the total number of reveal steps in a phase."""

    return len(phase.agents) + (_wave_item_count(phase) if phase.build_waves else len(phase.actions))


def _progress_step_style(
    step_index: int,
    revealed_steps: int,
    active_step: int | None,
    phase_style: str,
    complete: bool,
) -> str:
    """Return the style for one project-progress segment."""

    if step_index >= revealed_steps:
        return "dim"
    if active_step is not None and step_index == active_step:
        return f"bold black on {phase_style}"
    return "bold green" if complete else f"bold {phase_style}"


def _render_ship(
    current_index: int,
    reveal_count: int,
    reveal_total: int,
    phase_style: str,
    ready: bool,
) -> RenderableType:
    """Render a Viking ship that is built across the four phases."""

    phase_allocations = (2, 2, 2, 3)
    completed_before = sum(phase_allocations[:current_index])
    current_allocation = phase_allocations[current_index]
    if ready:
        current_revealed = current_allocation
    elif reveal_count <= 0:
        current_revealed = 0
    else:
        current_revealed = max(1, (reveal_count * current_allocation + reveal_total - 1) // reveal_total)

    revealed_steps = completed_before + current_revealed
    active_step = None if ready or current_revealed == 0 else revealed_steps - 1
    complete = ready and current_index == len(PHASES) - 1

    def style(step_index: int) -> str:
        return _progress_step_style(step_index, revealed_steps, active_step, phase_style, complete)

    line_1 = Text("           ", no_wrap=True)
    line_1.append("~.", style=style(8))

    line_2 = Text("     ", no_wrap=True)
    line_2.append("`-...____", style=style(5))
    line_2.append("|", style=style(3))
    line_2.append("__...`.", style=style(5))
    line_2.append("     .   .", style=style(8))

    line_3 = Text("      ", no_wrap=True)
    line_3.append("\\   \\   \\   \\   \\", style=style(4))
    line_3.append("   (     )", style=style(8))

    line_4 = Text("       ", no_wrap=True)
    line_4.append(":   :   :   :   :", style=style(4))
    line_4.append("   `.oo'", style=style(8))

    line_5 = Text("       ", no_wrap=True)
    line_5.append("|   |   |   |   |", style=style(3))
    line_5.append("  ( (`-'", style=style(8))

    line_6 = Text(" .---.   ", no_wrap=True)
    line_6.append(";   ;   ;   ;   ;", style=style(2))
    line_6.append("   `.`.", style=style(7))

    line_7 = Text("", no_wrap=True)
    line_7.append("/", style=style(6))
    line_7.append(" .-._)", style=style(6))
    line_7.append(" /_.-\"\"\"\"|\"\"\"'-._/", style=style(1))
    line_7.append("      `.`.", style=style(7))

    line_8 = Text("", no_wrap=True)
    line_8.append("(", style=style(6))
    line_8.append(" (`._)", style=style(6))
    line_8.append(" .-.  .-. |.-.  .-.  .-.", style=style(2))
    line_8.append("   ) )", style=style(1))

    line_9 = Text(" ", no_wrap=True)
    line_9.append("\\", style=style(1))
    line_9.append(" `---", style=style(6))
    line_9.append("( o )( o )( o )( o )( o )", style=style(0))
    line_9.append("-' /", style=style(1))

    line_10 = Text("  ", no_wrap=True)
    line_10.append("`.", style=style(1))
    line_10.append("    `-'  `-'  `-'  `-'  `-'", style=style(0))
    line_10.append("  .'", style=style(1))

    ship = Group(
        line_1,
        line_2,
        line_3,
        line_4,
        line_5,
        line_6,
        line_7,
        line_8,
        line_9,
        line_10,
    )

    return Panel.fit(
        Align.center(ship),
        title="Project Progress",
        border_style=phase_style,
        box=box.ROUNDED,
    )


def _build_phase_tree(
    phase: PhaseSpec,
    revealed_agents: int,
    active_agent: int | None,
    revealed_actions: int,
    active_action: int | None,
    revealed_wave_items: int,
    active_wave_item: int | None,
) -> Tree:
    """Build the tree for a phase based on the visible reveal state."""

    tree = Tree(f"{phase.emoji} [bold {phase.style}]{phase.title}[/]")
    tree.add(f"[dim]{phase.framing}[/]")
    tree.add(f"[bold]Goal[/]: {phase.goal}")
    tree.add(f"[bold]Handoff[/]: {phase.artifact_in} [dim]->[/] {phase.artifact_out}")
    tree.add(f"[bold]What to say[/]: {'  '.join(phase.skills)}")

    agents_node = tree.add("🤖 [bold]Agents Active[/]")
    for index, agent in enumerate(phase.agents):
        agents_node.add(f"[{_tree_item_style(index, revealed_agents, active_agent, phase.style)}]{agent}[/]")

    if phase.build_waves:
        wave_node = tree.add("🌊 [bold]Wave Execution[/]")
        remaining_visible_items = revealed_wave_items
        wave_offset = 0
        for wave_index, wave_items in enumerate(phase.build_waves, start=0):
            label = "parallel" if len(wave_items) > 1 else "sequential"
            wave_visible_count = max(0, min(len(wave_items), remaining_visible_items))
            if wave_visible_count == 0:
                wave_style = "dim"
            elif active_wave_item is not None and wave_offset <= active_wave_item < wave_offset + len(wave_items):
                wave_style = f"bold black on {phase.style}"
            else:
                wave_style = f"bold {phase.style}"
            subnode = wave_node.add(f"[{wave_style}]Wave {wave_index}[/] [dim]({label})[/]")
            for item_index, item in enumerate(wave_items):
                global_index = wave_offset + item_index
                local_active = item_index if global_index == active_wave_item else None
                subnode.add(
                    f"[{_tree_item_style(item_index, wave_visible_count, local_active, phase.style)}]{item}[/]"
                )
            remaining_visible_items -= wave_visible_count
            wave_offset += len(wave_items)
    else:
        action_node = tree.add("⚡ [bold]Actions[/]")
        for index, action in enumerate(phase.actions):
            action_node.add(f"[{_tree_item_style(index, revealed_actions, active_action, phase.style)}]{action}[/]")

    return tree


def _render_phase_panel(
    phase: PhaseSpec,
    current_index: int,
    visible_agents: int,
    visible_actions: int,
    visible_wave_items: int,
    ready: bool,
) -> RenderableType:
    """Render the live phase panel with surrounding progress."""

    subtitle = "[dim]guided simulation[/]" if not ready else f"[bold {phase.style}]artifact ready[/]"
    if ready:
        revealed_agents = len(phase.agents)
        active_agent = None
        revealed_actions = len(phase.actions)
        active_action = None
        revealed_wave_items = _wave_item_count(phase)
        active_wave_item = None
        reveal_count = _phase_reveal_total(phase)
    elif phase.build_waves:
        revealed_agents = len(phase.agents) if visible_wave_items else visible_agents
        active_agent = visible_agents - 1 if visible_wave_items == 0 and visible_agents > 0 else None
        revealed_actions = 0
        active_action = None
        revealed_wave_items = visible_wave_items
        active_wave_item = visible_wave_items - 1 if visible_wave_items > 0 else None
        reveal_count = revealed_agents + revealed_wave_items
    else:
        revealed_agents = len(phase.agents) if visible_actions else visible_agents
        active_agent = visible_agents - 1 if visible_actions == 0 and visible_agents > 0 else None
        revealed_actions = visible_actions
        active_action = visible_actions - 1 if visible_actions > 0 else None
        revealed_wave_items = 0
        active_wave_item = None
        reveal_count = revealed_agents + revealed_actions

    body = Group(
        _render_progress(current_index),
        Text(""),
        Columns(
            [
                Panel(
                    _build_phase_tree(
                        phase,
                        revealed_agents,
                        active_agent,
                        revealed_actions,
                        active_action,
                        revealed_wave_items,
                        active_wave_item,
                    ),
                    border_style=phase.style,
                    subtitle=subtitle,
                    box=box.ROUNDED,
                    width=TREE_PANEL_WIDTH,
                ),
                Align.center(
                    _render_ship(
                        current_index=current_index,
                        reveal_count=reveal_count,
                        reveal_total=_phase_reveal_total(phase),
                        phase_style=phase.style,
                        ready=ready,
                    ),
                    vertical="middle",
                ),
            ],
            align="center",
            expand=False,
        ),
    )
    return Align.center(body)


def _render_summary_table(rows_visible: int) -> Table:
    """Render the final summary table with progressive row reveal."""

    rows = (
        ("1. Explore", "Researcher / KM", "Context Summary"),
        ("2. Plan", "Planner", "PLAN.md"),
        ("3. Build", "Engineer / Tester", "Wave summaries"),
        ("4. Validate", "Judge", "Approval Verdict"),
    )
    table = Table(title="Workflow Summary", box=box.ROUNDED, show_header=True, header_style="bold white")
    table.add_column("Phase", style="cyan")
    table.add_column("Primary Agent", style="green")
    table.add_column("Output Artifact", style="yellow")
    for row in rows[:rows_visible]:
        table.add_row(*row)
    return table


def _animate_phase(console: Console, phase: PhaseSpec, index: int, animated: bool, fast: bool) -> None:
    """Animate one phase reveal, or print the final static panel."""

    console.print(Rule(f"[bold {phase.style}]Stage {index + 1} of {len(PHASES)}[/]", style=phase.style))
    if animated:
        with console.status(
            f"[bold {phase.style}]Preparing {phase.title}[/] [dim]for {REQUEST}[/]",
            spinner=phase.spinner,
        ):
            _sleep(STEP_DELAY, animated=animated, fast=fast)

        with Live(
            _render_phase_panel(
                phase,
                current_index=index,
                visible_agents=0,
                visible_actions=0,
                visible_wave_items=0,
                ready=False,
            ),
            console=console,
            refresh_per_second=8,
            transient=True,
        ) as live:
            for agent_count in range(1, len(phase.agents) + 1):
                live.update(
                    _render_phase_panel(
                        phase,
                        current_index=index,
                        visible_agents=agent_count,
                        visible_actions=0,
                        visible_wave_items=0,
                        ready=False,
                    )
                )
                _sleep(STEP_DELAY, animated=animated, fast=fast)

            if phase.build_waves:
                for wave_item_count in range(1, _wave_item_count(phase) + 1):
                    live.update(
                        _render_phase_panel(
                            phase,
                            current_index=index,
                            visible_agents=len(phase.agents),
                            visible_actions=0,
                            visible_wave_items=wave_item_count,
                            ready=False,
                        )
                    )
                    _sleep(STEP_DELAY, animated=animated, fast=fast)
            else:
                for action_count in range(1, len(phase.actions) + 1):
                    live.update(
                        _render_phase_panel(
                            phase,
                            current_index=index,
                            visible_agents=len(phase.agents),
                            visible_actions=action_count,
                            visible_wave_items=0,
                            ready=False,
                        )
                    )
                    _sleep(STEP_DELAY, animated=animated, fast=fast)

            live.update(
                _render_phase_panel(
                    phase,
                    current_index=index,
                    visible_agents=len(phase.agents),
                    visible_actions=len(phase.actions),
                    visible_wave_items=_wave_item_count(phase),
                    ready=True,
                )
            )
            _sleep(STEP_DELAY, animated=animated, fast=fast)

    console.print(
        _render_phase_panel(
            phase,
            current_index=index,
            visible_agents=len(phase.agents),
            visible_actions=len(phase.actions),
            visible_wave_items=_wave_item_count(phase),
            ready=True,
        )
    )
    console.print(
        f"[dim]Artifact handoff:[/] [bold]{phase.artifact_out}[/] [dim]-> next phase[/]"
    )
    console.print()
    _sleep(SECTION_SETTLE_DELAY, animated=animated, fast=fast)


def _render_intro(console: Console, animated: bool, fast: bool) -> None:
    """Render the staged intro panel."""

    intro_text = Text(
        "The Four-Phase Model turns a vague request into verified output.\n"
        "Explore -> Plan -> Build -> Validate.\n\n"
        f"Request: {REQUEST}",
        justify="center",
        style="bold cyan",
    )
    console.print(
        Align.center(
            Panel(
                intro_text,
                title="[bold magenta]The Four-Phase Model[/]",
                subtitle="[dim]guided simulation[/]",
                box=box.DOUBLE,
            )
        )
    )
    if animated:
        with console.status("[bold cyan]Initializing the workflow timeline[/]", spinner="dots"):
            _sleep(INTRO_DELAY, animated=animated, fast=fast)
    console.print(
        Panel(
            "[bold white]Story arc[/]\n"
            "[cyan]Vague request[/] -> [magenta]Context summary[/] -> [yellow]PLAN.md[/] -> "
            "[yellow]Parallel waves[/] -> [green]Approval verdict[/]",
            border_style="bright_black",
            box=box.ROUNDED,
        )
    )
    console.print()
    _sleep(INTRO_DELAY, animated=animated, fast=fast)


def _render_summary(console: Console, animated: bool, fast: bool) -> None:
    """Render the final summary and next-step guidance."""

    console.print(Rule("[bold green]Final Readout[/]", style="green"))
    if animated:
        with Live(Align.center(_render_summary_table(0)), console=console, refresh_per_second=8, transient=True) as live:
            for visible_rows in range(1, len(PHASES) + 1):
                live.update(Align.center(_render_summary_table(visible_rows)))
                _sleep(SUMMARY_STEP_DELAY, animated=animated, fast=fast)

    console.print(Align.center(_render_summary_table(len(PHASES))))
    console.print()
    console.print(
        Panel(
            "[bold white]What just happened[/]\n"
            "Rune moved one request through the same Four-Phase Model shown in the docs: "
            "Explore, Plan, Build, Validate.\n\n"
            "[bold white]Try it next[/]\n"
            "1. [cyan]rune profile use explore[/]\n"
            "2. Ask your assistant: [magenta]explore this repo[/]\n"
            "3. Then use [yellow]/write-plan[/] and [yellow]/rune[/]",
            border_style="green",
            box=box.ROUNDED,
        )
    )
    _sleep(FINAL_READOUT_DELAY, animated=animated, fast=fast)


@click.command("demo")
@click.option("--fast", is_flag=True, help="Shorten delays while keeping the guided flow.")
@click.option("--no-animate", is_flag=True, help="Render the demo without live animation or pauses.")
def top_demo(fast: bool, no_animate: bool) -> None:
    """Show the Four Phase Model workflow demo."""

    console = Console()
    animated = console.is_terminal and not getattr(console, "is_dumb_terminal", False) and not no_animate

    _render_intro(console, animated=animated, fast=fast)
    for index, phase in enumerate(PHASES):
        _animate_phase(console, phase, index=index, animated=animated, fast=fast)
    _render_summary(console, animated=animated, fast=fast)
