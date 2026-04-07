from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    import questionary
    from rich.console import Console
    from rich.table import Table
except ImportError as e:
    print(f'Missing dependency: {e.name}')
    print('Run this via the rune CLI: rune setup')
    sys.exit(1)

from .. import settings, setup_core as core
from .._common import flatten_section as _flat

console = Console()
BACK = object()
_SELECT_HINT = '(arrow keys to move, <enter> to confirm, <esc> to go back)'
_CHECKBOX_HINT = '(arrow keys to move, <space> to select, <a> to toggle all, <esc> to go back)'


def _abort(msg: str = 'Aborted.') -> None:
    """Print an abort message and exit."""
    console.print(f'\n[yellow]{msg}[/]')
    sys.exit(1)


def _ask_with_back(question: questionary.Question) -> object:
    """Run a prompt with escape returning BACK."""
    app = question.application

    @app.key_bindings.add('escape', eager=True)
    def _handle_back(event):
        event.app.exit(result=BACK)

    try:
        return question.unsafe_ask()
    except KeyboardInterrupt:
        _abort()


def _ask_no_back(question: questionary.Question) -> object:
    """Run a prompt without escape handling."""
    try:
        result = question.unsafe_ask()
    except KeyboardInterrupt:
        _abort()
    return result


def prompt_entry_point(state: core.CurrentState) -> str:
    """Ask the user how they would like to start the setup."""
    if state.status == 'none':
        choices = [
            questionary.Choice('Start from a profile', value='profile'),
            questionary.Choice('Build from scratch', value='scratch'),
        ]
        msg = 'How would you like to set up?'
    else:
        if state.status == 'profile':
            console.print(f'  Current: profile [bold cyan]{state.profile_name}[/bold cyan]\n')
        choices = [
            questionary.Choice('Modify current setup', value='modify'),
            questionary.Choice('Start over from a profile', value='profile'),
            questionary.Choice('Start over from scratch', value='scratch'),
        ]
        msg = 'What would you like to do?'
    return _ask_no_back(questionary.select(msg, choices=choices))


def prompt_profile_selection(profiles: dict[str, str]) -> str | object:
    """Ask the user to select a profile."""
    choices = [
        questionary.Choice(f'{name}  —  {desc}' if desc else name, value=name)
        for name, desc in profiles.items()
    ]
    return _ask_with_back(questionary.select('Select a profile:', choices=choices, instruction=_SELECT_HINT))


def prompt_agents(available: core.AvailableContent, preselected: dict[str, list[str]]) -> dict[str, list[str]] | object:
    """Ask the user to select agents for the profile."""
    if not available.agents:
        return {}
    pre = set(_flat(preselected))
    choices = []
    for category, names in sorted(available.agents.items()):
        for name in names:
            short = name.split('/', 1)[1] if '/' in name else name
            choices.append(questionary.Choice(f'[{category}] {short}', value=(category, name), checked=name in pre))
    console.print('\n[bold]Agents[/bold]')
    answer = _ask_with_back(questionary.checkbox('Select agents:', choices=choices, instruction=_CHECKBOX_HINT))
    if answer is BACK:
        return BACK
    result: dict[str, list[str]] = {}
    for category, name in answer:
        result.setdefault(category, []).append(name)
    return result


def prompt_rules(available: core.AvailableContent, preselected: dict[str, list[str]]) -> dict[str, list[str]] | object:
    """Ask the user to select rules for the profile."""
    if not available.rules:
        return {}
    pre = set(_flat(preselected))
    choices = []
    for category, names in sorted(available.rules.items()):
        for name in names:
            short = name.split('/', 1)[1] if '/' in name else name
            choices.append(questionary.Choice(f'[{category}] {short}', value=(category, name), checked=name in pre))
    console.print('\n[bold]Rules[/bold]')
    answer = _ask_with_back(questionary.checkbox('Select rules:', choices=choices, instruction=_CHECKBOX_HINT))
    if answer is BACK:
        return BACK
    result: dict[str, list[str]] = {}
    for category, name in answer:
        result.setdefault(category, []).append(name)
    return result


def _prompt_list_section(items: list[str], label: str, prompt: str, preselected: list[str]) -> list[str] | object:
    """Generic checkbox prompt for a flat list of strings."""
    if not items:
        return preselected
    pre = set(preselected)
    choices = [questionary.Choice(name, checked=name in pre) for name in items]
    console.print(f'\n[bold]{label}[/bold]')
    answer = _ask_with_back(questionary.checkbox(prompt, choices=choices, instruction=_CHECKBOX_HINT))
    return answer


def prompt_skills(available: core.AvailableContent, preselected: list[str]) -> list[str] | object:
    """Ask the user to select skills for the profile."""
    if not available.skills:
        return preselected
    pre = set(preselected)
    by_category: dict[str, list[str]] = {}
    for name in available.skills:
        cat = name.split('/', 1)[0] if '/' in name else 'general'
        by_category.setdefault(cat, []).append(name)
    choices = []
    for category in sorted(by_category):
        for name in by_category[category]:
            short = name.split('/', 1)[1] if '/' in name else name
            choices.append(questionary.Choice(f'[{category}] {short}', value=name, checked=name in pre))
    console.print('\n[bold]Skills[/bold]')
    answer = _ask_with_back(questionary.checkbox('Select skills:', choices=choices, instruction=_CHECKBOX_HINT))
    return answer if answer is BACK else list(answer)


def prompt_hooks(available: core.AvailableContent, preselected: list[str]) -> list[str] | object:
    """Ask the user to select hooks for the profile."""
    res = _prompt_list_section(available.hooks, 'Hooks', 'Select hooks:', preselected)
    return res if res is BACK else list(res)


def prompt_mcps(available: core.AvailableContent, preselected: list[str]) -> list[str] | object:
    """Ask the user to select MCP servers for the profile."""
    res = _prompt_list_section(available.mcps, 'MCPs', 'Select MCPs:', preselected)
    return res if res is BACK else list(res)


def _default_install_dir() -> Path:
    """Return the default install target for the wizard."""
    if (Path.cwd() / '.rune' / 'current-profile').exists():
        return settings.PROJECT_DIR or (Path.cwd() / '.claude')
    if settings.PROJECT_DIR:
        return settings.PROJECT_DIR
    return settings.CLAUDE_DIR


def prompt_install_target(current: Path) -> Path | object:
    """Ask where Claude Code resources should be installed."""
    project_dir = settings.PROJECT_DIR or (Path.cwd() / '.claude')
    choices = [
        questionary.Choice(
            f'Project ({project_dir})',
            value=project_dir,
            checked=current == project_dir,
        ),
        questionary.Choice(
            f'Global ({settings.CLAUDE_DIR})',
            value=settings.CLAUDE_DIR,
            checked=current == settings.CLAUDE_DIR,
        ),
    ]
    console.print('\n[bold]Install Target[/bold]')
    if settings.PROJECT_DIR:
        console.print(f'[dim]RUNE_PROJECT_DIR is set to {settings.PROJECT_DIR}[/dim]')
    return _ask_with_back(
        questionary.select(
            'Where should Rune install Claude Code resources?',
            choices=choices,
            instruction=_SELECT_HINT,
        )
    )


def prompt_confirmation(selections: core.Selections, base: core.Selections | None, install_dir: Path) -> str:
    """Ask the user to confirm the setup summary and choose apply mode."""
    render_summary(selections, base, install_dir)
    choices = [
        questionary.Choice('Apply (safe — keeps unmanaged resources)', value='apply'),
        questionary.Choice('Apply with full control (removes unmanaged resources)', value='full'),
        questionary.Choice('Cancel', value='cancel'),
    ]
    answer = _ask_with_back(
        questionary.select(
            'How to proceed?',
            choices=choices,
            instruction=_SELECT_HINT,
        )
    )
    if answer is BACK:
        return 'back'
    if answer == 'full':
        unmanaged = core.list_unmanaged(install_dir, selections) if install_dir.is_dir() else {}
        console.print(
            '\n[bold red]WARNING:[/bold red] '
            'This will remove unmanaged Claude Code resources from the selected install target.'
        )
        if unmanaged:
            console.print('\n  The following unmanaged resources will be removed:')
            for section, files in sorted(unmanaged.items()):
                for filename in files:
                    console.print(f'    {section}/  {filename}')
        confirm = questionary.confirm('Proceed with full control?', default=False).ask()
        if confirm is None:
            _abort()
        if not confirm:
            return 'back'
    return answer


def render_summary(selections: core.Selections, base: core.Selections | None, install_dir: Path) -> None:
    """Render a summary table of the proposed setup."""
    table = Table(title='Setup Summary', show_header=True, header_style='bold')
    table.add_column('Resource Type', style='cyan')
    table.add_column('Value', justify='right')
    table.add_column('Changes', style='dim')
    diff = core.diff_from_base(base, selections) if base else {}
    sections = [
        ('Agents', len(_flat(selections.agents)), 'agents'),
        ('Rules', len(_flat(selections.rules)), 'rules'),
        ('Skills', len(selections.skills), 'skills'),
        ('Hooks', len(selections.hooks), 'hooks'),
        ('MCPs', len(selections.mcps), 'mcps'),
    ]
    for label, count, key in sections:
        changes = ''
        if key in diff:
            added, removed = len(diff[key].get('added', [])), len(diff[key].get('removed', []))
            changes = ' '.join([f'[green]+{added}[/green]' if added else '', f'[red]-{removed}[/red]' if removed else '']).strip()
        table.add_row(label, str(count), changes)
    table.add_section()
    scope = 'project' if install_dir != settings.CLAUDE_DIR else 'global'
    table.add_row('Platform', 'Claude Code', '')
    table.add_row('Install target', scope, str(install_dir))
    if selections.based_on:
        table.add_row('Based on', selections.based_on, '')
    console.print(table)


def prompt_export(curdir: Path, selections: core.Selections, install_dir: Path) -> None:
    """Ask the user to save the current configuration as a profile."""
    console.print('\n[bold]Save as a named profile[/bold]')
    dest = _ask_no_back(
        questionary.select(
            'Where to save this profile?',
            choices=[
                questionary.Choice(
                    'Personal (.local-profile.yaml — private)',
                    value='local',
                ),
                questionary.Choice(
                    'Shared (profiles.yaml — committed)',
                    value='shared',
                ),
            ],
        )
    )
    name = questionary.text(
        'Profile name:',
        validate=lambda value: len(value.strip()) > 0 or 'Name cannot be empty',
    ).ask()
    if name is None:
        _abort()
    name = name.strip()
    shared_profiles = core._load_profiles_yaml(curdir)
    if dest == 'local':
        if name in shared_profiles:
            console.print(
                f'[dim]Note: shared profile "{name}" exists; '
                'local will take precedence.[/dim]'
            )
        desc = questionary.text('Description (optional):').ask()
        core.export_to_local_profile_yaml(curdir, name, (desc or '').strip(), selections)
    else:
        if name in shared_profiles:
            overwrite = questionary.confirm(
                f'Overwrite shared profile "{name}"?',
                default=False,
            ).ask()
            if overwrite is not True:
                return prompt_export(curdir, selections, install_dir)
        desc = questionary.text('Description (optional):').ask()
        core.export_to_profiles_yaml(curdir, name, (desc or '').strip(), selections)
    state_file = core.state_file_for_install_dir(install_dir)
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(name + '\n')
    console.print(f'[green]Saved profile "{name}"[/green]')


def prompt_tools(curdir: Path) -> None:
    """Ask the user to install discovered system tools."""
    tools = core.discover_tools(curdir)
    not_installed = [t for t in tools if not t.installed]
    if not not_installed:
        return
    required_missing = any(t.required for t in not_installed)
    prompt = 'Install missing system tools?' if required_missing else 'Install recommended system tools?'
    if questionary.confirm(prompt, default=required_missing).ask() is not True:
        return
    choices = []
    for tool in not_installed:
        prefix = 'required' if tool.required else 'optional'
        check_note = ' [custom check]' if tool.check else ''
        if tool.description:
            label = f'[{prefix}] {tool.name} ({tool.binary}){check_note} — {tool.description}'
        else:
            label = f'[{prefix}] {tool.name} ({tool.binary}){check_note}'
        choices.append(questionary.Choice(label, value=tool.name, checked=tool.required))
    selected = questionary.checkbox(
        'Select tools to install:',
        choices=choices,
        instruction=_CHECKBOX_HINT,
    ).ask()
    if selected is None:
        _abort()
    for tname in selected:
        console.print(f'\n[bold]Installing {tname}...[/bold]')
        script = curdir / 'tools' / tname / f'install-{tname}.sh'
        if script.exists():
            subprocess.run(['bash', str(script)], check=False)
        else:
            console.print(f'[yellow]Missing install script for {tname}[/yellow]')


STEP_ENTRY, STEP_PROFILE, STEP_AGENTS, STEP_RULES, STEP_SKILLS, STEP_HOOKS, STEP_MCPS, STEP_INSTALL_TARGET, STEP_CONFIRM = range(9)


def _load_base_selection(curdir: Path, selections: core.Selections) -> core.Selections | None:
    """Load the base profile selection when the current selection derives from one."""
    if not selections.based_on:
        return None
    try:
        return core.load_profile(curdir, selections.based_on)
    except (ValueError, FileNotFoundError):
        return None


def _remove_unmanaged_resources(install_dir: Path, selections: core.Selections) -> None:
    """Remove unmanaged resources from the selected install target."""
    import shutil

    if not install_dir.is_dir():
        return

    for section, files in core.list_unmanaged(install_dir, selections).items():
        for filename in files:
            target = install_dir / section / filename
            if target.is_dir():
                shutil.rmtree(target)
            elif target.exists():
                target.unlink()
            console.print(f'  [red]Removed[/red] {section}/{filename}')


def run_setup_wizard(curdir: Path) -> None:
    """Run the interactive setup wizard."""
    try:
        if not sys.stdin.isatty():
            print('Interactive terminal required. For non-interactive use: rune profile use <name>')
            sys.exit(1)
        console.print('[bold]Rune setup wizard[/bold]\n')
        state, available = core.detect_current_state(curdir), core.discover(curdir)
        action, selections, prof_active, step = '', core.Selections(), False, STEP_ENTRY
        install_dir = _default_install_dir()
        while step <= STEP_CONFIRM:
            if step == STEP_ENTRY:
                action = prompt_entry_point(state)
                if action == 'modify':
                    selections = state.selections or core.Selections()
                    prof_active = False
                elif action == 'profile':
                    selections = core.Selections()
                    prof_active = True
                else:
                    selections = core.Selections()
                    prof_active = False
                step += 1
            elif step == STEP_PROFILE:
                if not prof_active:
                    step += 1
                    continue
                profs = core.list_profiles(curdir)
                if not profs:
                    console.print('[red]No profiles found[/red]')
                    sys.exit(1)
                res = prompt_profile_selection(profs)
                if res is BACK:
                    step = STEP_ENTRY
                else:
                    selections = core.load_profile(curdir, res)
                    step += 1
            elif step == STEP_AGENTS:
                res = prompt_agents(available, selections.agents)
                if res is BACK:
                    step = STEP_PROFILE if prof_active else STEP_ENTRY
                else:
                    selections.agents = res
                    step += 1
            elif step == STEP_RULES:
                res = prompt_rules(available, selections.rules)
                if res is BACK:
                    step = STEP_AGENTS
                else:
                    selections.rules = res
                    step += 1
            elif step == STEP_SKILLS:
                res = prompt_skills(available, selections.skills)
                if res is BACK:
                    step = STEP_RULES
                else:
                    selections.skills = res
                    step += 1
            elif step == STEP_HOOKS:
                res = prompt_hooks(available, selections.hooks)
                if res is BACK:
                    step = STEP_SKILLS
                else:
                    selections.hooks = res
                    step += 1
            elif step == STEP_MCPS:
                res = prompt_mcps(available, selections.mcps)
                if res is BACK:
                    step = STEP_HOOKS
                else:
                    selections.mcps = res
                    step += 1
            elif step == STEP_INSTALL_TARGET:
                res = prompt_install_target(install_dir)
                if res is BACK:
                    step = STEP_MCPS
                else:
                    install_dir = res
                    step += 1
            elif step == STEP_CONFIRM:
                base = _load_base_selection(curdir, selections)
                dec = prompt_confirmation(selections, base, install_dir)
                if dec == 'back':
                    step = STEP_INSTALL_TARGET
                elif dec == 'cancel':
                    _abort()
                else:
                    if dec == 'full':
                        _remove_unmanaged_resources(install_dir, selections)
                    console.print('\n[bold]Applying configuration...[/bold]')
                    core.apply(curdir, selections, ['claude'], claude_dir=install_dir)
                    console.print('[bold green]Done![/bold green]\n')
                    prompt_export(curdir, selections, install_dir)
                    prompt_tools(curdir)
                    console.print('\n[bold]Setup complete.[/bold]\nRun [cyan]rune system verify[/cyan] to check.')
                    break
    except KeyboardInterrupt:
        _abort()
