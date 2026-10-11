# Manim animations. Run `make` for usage.
#
#   src/<subject>/<lesson>.py                 sources, e.g. src/inf/zaklady_pythonu.py
#   renders/<subject>/<lesson>/<quality>/     finished videos & stills (gitignored)
#   build/                                    Manim caches: TeX, partial movies (gitignored)
#   templates/scene.py                        skeleton for `make new`

SHELL := /bin/bash
.DEFAULT_GOAL := help

# --- Arguments ---------------------------------------------------------------
# FILE    src/inf/zaklady_pythonu.py, inf/zaklady_pythonu or just zaklady_pythonu
#         (src/ and .py optional); defaults to the most recently edited animation
# SCENE   scene class(es) to render; empty = every scene in FILE
# Q       l=480p15 m=720p30 h=1080p60 p=1440p60 k=2160p60
# FORMAT  mov | mp4 | gif | webm
# ARGS    extra manim flags, e.g. ARGS="-n 3,5" (only animations 3-5)
FILE   ?=
SCENE  ?=
Q      ?= k
FORMAT ?= mov
ARGS   ?=

MANIM   ?= manim
OPEN    ?= $(if $(filter Darwin,$(shell uname -s)),open,xdg-open)
SRC_DIR := src
RENDERS := renders
BUILD   := build
STAMP   := $(BUILD)/.stamp

# Every .py under src/ defining a Scene subclass.
# (Regex lives in a variable: make would count its paren inside $(shell ...).)
SCENE_RE   := ^class +([A-Za-z_][A-Za-z0-9_]*) *\(.*Scene
ANIMATIONS := $(shell find $(SRC_DIR) -name '*.py' -not -path '*/.*' \
                -exec grep -lE '$(SCENE_RE)' {} + 2>/dev/null | sort)
LATEST := $(if $(ANIMATIONS),$(shell ls -t $(ANIMATIONS) | head -n1))

# FILE relative to src/ (src/inf/x.py, inf/x.py and inf/x all give inf/x.py)
FILE_PY := $(patsubst $(SRC_DIR)/%,%,$(FILE:.py=).py)
NEW_PY  := $(SRC_DIR)/$(FILE_PY)
ifeq ($(strip $(FILE)),)
  ANIM := $(LATEST)
else
  ANIM := $(or $(wildcard $(SRC_DIR)/$(FILE_PY)),$(filter %/$(notdir $(FILE_PY)),$(ANIMATIONS)))
endif
# Output paths mirror src/ without the src/ prefix.
SUBJECT := $(patsubst %/,%,$(dir $(patsubst $(SRC_DIR)/%,%,$(ANIM))))
LESSON  := $(basename $(notdir $(ANIM)))
OUTDIR  := $(RENDERS)/$(SUBJECT)/$(LESSON)

# Recursive (=) so target-specific Q/FORMAT (see preview) apply.
RUN_MANIM = $(MANIM) render -q$(Q) --media_dir $(RENDERS)/$(SUBJECT) $(if $(SCENE),,-a) $(ARGS)
# Open every video/still written to OUTDIR since $(STAMP) was touched.
OPEN_NEW = files=$$(find $(OUTDIR) -type f -newer $(STAMP) -not -path '*/sections/*' \
             \( -name '*.mov' -o -name '*.mp4' -o -name '*.gif' -o -name '*.webm' -o -name '*.png' \)); \
           [ -n "$$files" ] || { echo "Nothing new in $(OUTDIR)" >&2; exit 1; }; \
           for f in $$files; do echo "open $$f"; $(OPEN) "$$f"; done

.PHONY: help list render open preview still all new clean clean-all _check _stamp

help: ## Show this help
	@echo "Usage: make <target> [FILE=inf/zaklady_pythonu] [SCENE=FunctionsAsPrograms] [Q=l|m|h|p|k] [FORMAT=mov|mp4|gif|webm] [ARGS=...]"
	@echo
	@awk -F ':.*## ' '/^[a-z][a-z-]*:.*## /{printf "  %-10s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo
	@echo "Defaults: Q=$(Q) FORMAT=$(FORMAT), FILE = last edited animation ($(or $(LATEST),none))"
	@echo "Output:   $(RENDERS)/<subject>/<lesson>/<quality>/<Scene>.<ext>"

list: ## List animations and their scenes (* = default FILE)
	@for f in $(ANIMATIONS); do \
	  [ "$$f" = "$(LATEST)" ] && m='*' || m=' '; \
	  echo "$$m $$f"; \
	  sed -nE 's/$(SCENE_RE).*/      \1/p' "$$f"; \
	done

render: _check ## Render FILE [SCENE] at quality Q
	$(RUN_MANIM) --format=$(FORMAT) $(ANIM) $(SCENE)

open: _check _stamp ## Render, then open the result
	$(RUN_MANIM) --format=$(FORMAT) $(ANIM) $(SCENE)
	@$(OPEN_NEW)

preview: Q = l
preview: FORMAT = mp4
preview: open ## Quick low-quality render (Q=l, mp4), then open

still: _check _stamp ## Render only the last frame as PNG, then open
	$(RUN_MANIM) -s $(ANIM) $(SCENE)
	@$(OPEN_NEW)

all: ## Render every scene of every animation at quality Q
	@for f in $(ANIMATIONS); do $(MAKE) --no-print-directory render FILE=$$f SCENE= || exit 1; done

new: ## Create src/FILE from the template (SCENE defaults to the CamelCased file name)
	@$(if $(strip $(FILE)),,$(error Usage: make new FILE=<subject>/<lesson>.py [SCENE=Name]))
	@test ! -e $(NEW_PY) || { echo "$(NEW_PY) already exists" >&2; exit 1; }
	@mkdir -p $(dir $(NEW_PY))
	@scene=$(or $(SCENE),$$(basename $(NEW_PY) .py | perl -pe 's/(?:^|_)(\w)/\U$$1/g')); \
	  sed "s/__SCENE__/$$scene/g" templates/scene.py > $(NEW_PY) && \
	  echo "Created $(NEW_PY) (scene $$scene). Try: make preview FILE=$(FILE_PY)"

clean: ## Remove Manim caches (build/, __pycache__)
	rm -rf $(BUILD)
	find . -path './.*' -prune -o -type d -name __pycache__ -prune -exec rm -rf {} +

clean-all: clean ## Also remove every render
	rm -rf $(RENDERS)

_check:
	@$(if $(ANIM),,$(error No animation matches FILE='$(FILE)'; see `make list`))
	@$(if $(word 2,$(ANIM)),$(error FILE='$(FILE)' is ambiguous: $(ANIM)))
	@$(if $(filter l m h p k,$(Q)),,$(error Q must be one of l m h p k, got '$(Q)'))
	@echo "▶ $(ANIM)$(if $(SCENE), [$(SCENE)]) Q=$(Q)$(if $(strip $(FILE)),, (last edited))"

_stamp:
	@mkdir -p $(BUILD) && touch $(STAMP)
