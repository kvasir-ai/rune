.DEFAULT_GOAL := help

.PHONY: \
  help \
  configure-claude configure-opencode configure-peon \
  use-profile current-profile list-profiles show-profile \
  list-mcps mcp-status enable-mcp disable-mcp \
  list-agents list-rules list-skills \
  verify validate reset list-tools \
  list-peon-profiles \
  _configure

RUN := uv run

# ──────────────────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────────────────

CLAUDE_DIR   := $(HOME)/.claude
OPENCODE_DIR := $(HOME)/.config/opencode
SRC          := $(CURDIR)/src
CLAUDE_SRC   := $(CURDIR)/platforms/claude
OPENCODE_SRC := $(CURDIR)/platforms/opencode

# ──────────────────────────────────────────────────────────────────────────────
# Recipe fragments  (Make logic evaluated inline, not shell commands)
# ──────────────────────────────────────────────────────────────────────────────

# Resolve PROFILE: use supplied value, or fall back to the active profile
define resolve_profile
$(eval PROFILE := $(or $(PROFILE),$(shell $(RUN) $(CURDIR)/scripts/resource-manager.py profile current $(CURDIR))))
endef

# Fail early when PROFILE is not set, printing available choices
define guard_profile
@[ -n "$(PROFILE)" ] || { echo "Error: PROFILE is required."; $(MAKE) --no-print-directory list-profiles; exit 1; }
endef

# Fail early when MCP is not set, printing available choices
define guard_mcp
@[ -n "$(MCP)" ] || { echo "Error: MCP is required."; $(MAKE) --no-print-directory list-mcps; exit 1; }
endef

# ──────────────────────────────────────────────────────────────────────────────

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"} \
	  /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } \
	  /^[a-zA-Z_-]+:.*##/ { printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2 }' \
	  $(MAKEFILE_LIST)

##@ Configuration

configure-claude: ## Apply profile to Claude Code   [PROFILE=<name>]
	$(resolve_profile)
	@if command -v claude >/dev/null 2>&1 || [ -d $(CLAUDE_DIR) ]; then \
		echo "==> Configuring Claude Code with profile: $(PROFILE)"; \
		$(MAKE) --no-print-directory _configure PLATFORM=claude PROFILE=$(PROFILE); \
	else \
		echo "==> Skipping Claude Code (not installed)"; \
	fi

configure-opencode: ## Apply profile to OpenCode   [PROFILE=<name>]
	$(resolve_profile)
	@if command -v opencode >/dev/null 2>&1 || [ -d $(OPENCODE_DIR) ]; then \
		echo "==> Configuring OpenCode with profile: $(PROFILE)"; \
		$(MAKE) --no-print-directory _configure PLATFORM=opencode PROFILE=$(PROFILE); \
	else \
		echo "==> Skipping OpenCode (not installed)"; \
	fi

configure-peon: ## Configure peon-ping model-pack rotation (requires peon-ping installed)   [PEON_PROFILES=warcraft,redalert,...]
	@test -f "$$HOME/.claude/hooks/peon-ping/peon.sh" || { \
		echo "✗ peon-ping is not installed."; \
		echo "  Run: make install-tool-peon-ping"; \
		exit 1; \
	}
	@if grep -qi microsoft /proc/version 2>/dev/null; then \
		if ! grep -q 'export PLATFORM=linux' "$$HOME/.bashrc" 2>/dev/null; then \
			echo "==> WSL2 detected — setting PLATFORM=linux in ~/.bashrc for WSLg audio"; \
			echo 'export PLATFORM=linux' >> "$$HOME/.bashrc"; \
		fi; \
		export PLATFORM=linux; \
	fi
	@if [ -f $(CURDIR)/tools/peon-ping/configure_claude.py ]; then \
		echo "==> Configuring peon-ping for Claude Code"; \
		PEON_PROFILES="$(PEON_PROFILES)" $(RUN) $(CURDIR)/tools/peon-ping/configure_claude.py; \
	else \
		echo "  – skipping Claude Code (configure_claude.py not found)"; \
	fi
	@if command -v opencode >/dev/null 2>&1 || [ -d $(OPENCODE_DIR) ]; then \
		if [ -f $(CURDIR)/tools/peon-ping/configure_opencode.py ]; then \
			echo "==> Configuring peon-ping for OpenCode"; \
			$(RUN) $(CURDIR)/tools/peon-ping/configure_opencode.py; \
		else \
			echo "  – skipping OpenCode (configure_opencode.py not found)"; \
		fi; \
	else \
		echo "==> Skipping OpenCode (not installed)"; \
	fi

list-peon-profiles: ## List available peon-ping sound profiles
	@$(RUN) $(CURDIR)/tools/peon-ping/configure_claude.py --list-profiles

##@ Profiles

use-profile: ## Set active profile and reconfigure   PROFILE=<name>
	$(guard_profile)
	@$(RUN) $(CURDIR)/scripts/resource-manager.py profile use $(PROFILE) $(CURDIR)
	@$(MAKE) --no-print-directory configure-claude PROFILE=$(PROFILE)
	@$(MAKE) --no-print-directory configure-opencode PROFILE=$(PROFILE)

current-profile: ## Print the active profile name
	@$(RUN) $(CURDIR)/scripts/resource-manager.py profile current $(CURDIR)

list-profiles: ## List all available profiles
	@$(RUN) $(CURDIR)/scripts/resource-manager.py profile list $(CURDIR)

show-profile: ## Preview profile contents   PROFILE=<name>
	$(guard_profile)
	@$(RUN) $(CURDIR)/scripts/resource-manager.py profile show $(PROFILE) $(CURDIR)

##@ MCPs

list-mcps: ## List all available MCP server definitions
	@$(RUN) $(CURDIR)/scripts/mcp-manager.py list --curdir $(CURDIR)

mcp-status: ## Show MCP on/off status   [PROFILE=<name>]
	$(resolve_profile)
	@$(RUN) $(CURDIR)/scripts/mcp-manager.py status --profile $(PROFILE) --curdir $(CURDIR)

enable-mcp: ## Enable an MCP in a profile   MCP=<name> [PROFILE=<name>]
	$(guard_mcp)
	$(resolve_profile)
	@$(RUN) $(CURDIR)/scripts/mcp-manager.py enable $(MCP) --profile $(PROFILE) --curdir $(CURDIR)

disable-mcp: ## Disable an MCP in a profile   MCP=<name> [PROFILE=<name>]
	$(guard_mcp)
	$(resolve_profile)
	@$(RUN) $(CURDIR)/scripts/mcp-manager.py disable $(MCP) --profile $(PROFILE) --curdir $(CURDIR)

##@ Content

list-agents: ## List all available agents
	@find $(SRC)/agents -name "*.md" 2>/dev/null | xargs -I{} basename {} .md | sort

list-rules: ## List all available rules
	@find $(SRC)/rules -name "*.md" 2>/dev/null | xargs -I{} basename {} .md | sort

list-skills: ## List all available skills
	@ls -1d $(SRC)/skills/*/ 2>/dev/null | xargs -I{} basename {} | sort

##@ Verification

reset: ## Remove all deployed resources
	@echo ""
	@echo "  Will remove from $(CLAUDE_DIR)/:   agents/*.md  rules/*.md  skills/*  hooks/*.py  settings.json  statusline*"
	@echo "  Will remove from $(OPENCODE_DIR)/: agents/*.md  rules/*.md  skills/*  hooks/*.py  settings.json"
	@echo "  Will clean MCP keys from:          ~/.config/opencode/opencode.json (if present)"
	@echo "  Will remove:                       .current-profile"
	@echo ""
	@printf '  Type "delete" to confirm: ' && read ans && [ "$${ans}" = "delete" ] || { echo "  Aborted."; exit 1; }
	@find $(CLAUDE_DIR)/agents   -maxdepth 1 -name "*.md" -delete 2>/dev/null || true
	@find $(CLAUDE_DIR)/rules    -maxdepth 1 -name "*.md" -delete 2>/dev/null || true
	@find $(CLAUDE_DIR)/hooks    -maxdepth 1 -name "*.py" -delete 2>/dev/null || true
	@find $(CLAUDE_DIR)/skills   -maxdepth 1 -mindepth 1 -type d -exec rm -r {} + 2>/dev/null || true
	@rm -f $(CLAUDE_DIR)/settings.json $(CLAUDE_DIR)/statusline_command.py $(CLAUDE_DIR)/statusline.yaml 2>/dev/null || true
	@find $(OPENCODE_DIR)/agents -maxdepth 1 -name "*.md" -delete 2>/dev/null || true
	@find $(OPENCODE_DIR)/rules  -maxdepth 1 -name "*.md" -delete 2>/dev/null || true
	@find $(OPENCODE_DIR)/hooks  -maxdepth 1 -name "*.py" -delete 2>/dev/null || true
	@find $(OPENCODE_DIR)/skills -maxdepth 1 -mindepth 1 -type d -exec rm -r {} + 2>/dev/null || true
	@rm -f $(OPENCODE_DIR)/settings.json 2>/dev/null || true
	@if [ -f $(HOME)/.config/opencode/opencode.json ]; then \
		python3 -c "import json; p='$(HOME)/.config/opencode/opencode.json'; d=json.loads(open(p).read()); d.pop('mcp',None); open(p,'w').write(json.dumps(d,indent=2)+'\n')" 2>/dev/null && \
		echo "  ✓ Cleaned MCP keys from opencode.json" || true; \
	fi
	@rm -f $(CURDIR)/.current-profile 2>/dev/null || true
	@echo "  ✓ Reset complete — run 'make use-profile PROFILE=<name>' to redeploy"

verify: ## Check installed resources
	@ok=true; \
	echo "==> Verifying Claude Code setup"; \
	if [ -d $(CLAUDE_DIR) ]; then \
		[ -d $(CLAUDE_DIR)/agents ]                && echo "  ✓ agents/"               || { echo "  ✗ agents/ missing";               ok=false; }; \
		[ -d $(CLAUDE_DIR)/hooks ]                 && echo "  ✓ hooks/"                || { echo "  ✗ hooks/ missing";                ok=false; }; \
		[ -d $(CLAUDE_DIR)/rules ]                 && echo "  ✓ rules/"                || { echo "  ✗ rules/ missing";                ok=false; }; \
		[ -d $(CLAUDE_DIR)/skills ]                && echo "  ✓ skills/"               || { echo "  ✗ skills/ missing";               ok=false; }; \
		[ -f $(CLAUDE_DIR)/settings.json ]         && echo "  ✓ settings.json"         || { echo "  ✗ settings.json missing";         ok=false; }; \
		[ -f $(CLAUDE_DIR)/statusline_command.py ] && echo "  ✓ statusline_command.py" || echo "  – statusline_command.py not installed (optional)"; \
	else \
		echo "  – skipped ($(CLAUDE_DIR) does not exist)"; \
	fi; \
	echo "==> Verifying OpenCode setup"; \
	if [ -d $(OPENCODE_DIR) ]; then \
		[ -d $(OPENCODE_DIR)/agents ] && echo "  ✓ agents/" || { echo "  ✗ agents/ missing"; ok=false; }; \
		[ -d $(OPENCODE_DIR)/hooks ]  && echo "  ✓ hooks/"  || { echo "  ✗ hooks/ missing";  ok=false; }; \
		[ -d $(OPENCODE_DIR)/rules ]  && echo "  ✓ rules/"  || { echo "  ✗ rules/ missing";  ok=false; }; \
		[ -d $(OPENCODE_DIR)/skills ] && echo "  ✓ skills/" || { echo "  ✗ skills/ missing"; ok=false; }; \
	else \
		echo "  – skipped ($(OPENCODE_DIR) does not exist)"; \
	fi; \
	echo "==> Verifying tools"; \
	if command -v yq >/dev/null 2>&1; then \
		yq -r 'to_entries[] | .key + ":" + (.value.check // "") + ":" + .value.binary' $(CURDIR)/tools/registry.yaml | while IFS=: read -r name chk bin; do \
			if [ -n "$$chk" ]; then eval "$$chk" >/dev/null 2>&1 && echo "  ✓ $$name" || echo "  – $$name not installed (run 'make install-tool-$$name')"; \
			else command -v $$bin >/dev/null 2>&1 && echo "  ✓ $$name" || echo "  – $$name not installed (run 'make install-tool-$$name')"; fi; \
		done; \
	else \
		echo "  – yq not installed (run 'make install-tool-yq' to enable tool verification)"; \
	fi; \
	if [ "$$ok" = "true" ]; then echo "✓ All verified"; else echo "✗ Some items missing — run 'make use-profile PROFILE=<name>' to fix"; exit 1; fi

validate: ## Validate YAML files against JSON schemas
	@echo "==> Validating YAML against schemas"
	@$(RUN) $(CURDIR)/scripts/validate-schemas.py

##@ System Tools (optional, not managed by profiles)

install-tool-%: ## Install a system tool   install-tool-<name>
	@[ -f $(CURDIR)/tools/$*/install-$*.sh ] || { echo "✗ Unknown tool: $*"; exit 1; }
	@bash $(CURDIR)/tools/$*/install-$*.sh

uninstall-tool-%: ## Uninstall a system tool   uninstall-tool-<name>
	@[ -f $(CURDIR)/tools/$*/uninstall-$*.sh ] || { echo "✗ Unknown tool: $*"; exit 1; }
	@bash $(CURDIR)/tools/$*/uninstall-$*.sh

list-tools: ## List available system tools
	@echo "Available tools (install with 'make install-tool-<name>'):"
	@if command -v yq >/dev/null 2>&1; then \
		yq -r 'to_entries[] | .key + ":" + (.value.check // "") + ":" + .value.binary + ":" + .value.description' $(CURDIR)/tools/registry.yaml | while IFS=: read -r name chk bin desc; do \
			if [ -n "$$chk" ]; then eval "$$chk" >/dev/null 2>&1 && tag="[installed]" || tag="[not installed]"; \
			else command -v $$bin >/dev/null 2>&1 && tag="[installed]" || tag="[not installed]"; fi; \
			printf "  %-14s %-16s %s\n" "$$name" "$$tag" "$$desc"; \
		done; \
	else \
		echo "  – yq not installed (run 'make install-tool-yq' to enable tool listing)"; \
	fi

# ──────────────────────────────────────────────────────────────────────────────
# Internal — not shown in help
# ──────────────────────────────────────────────────────────────────────────────

_configure:
	@[ -n "$(PLATFORM)" ] || { echo "Usage: make _configure PLATFORM=claude|opencode PROFILE=<name>"; exit 1; }
	@[ -n "$(PROFILE)" ]  || { echo "Usage: make _configure PLATFORM=claude|opencode PROFILE=<name>"; exit 1; }
	@$(RUN) $(CURDIR)/scripts/resource-manager.py configure \
		--platform     $(PLATFORM)     \
		--profile      $(PROFILE)      \
		--curdir       $(CURDIR)       \
		--src          $(SRC)          \
		--claude-dir   $(CLAUDE_DIR)   \
		--opencode-dir $(OPENCODE_DIR) \
		--claude-src   $(CLAUDE_SRC)   \
		--opencode-src $(OPENCODE_SRC)
