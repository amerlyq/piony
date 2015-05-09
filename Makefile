NM := piony
PR := ./$(NM).py
PRF := /tmp/$(NM).prof
PY3 := python3

# Ignore all real files with names of targets.
TARGS := $(shell sed -n 's/^\([-a-z]\+\):.*/\1/p' Makefile|sort -u|xargs)
.PHONY: $(TARGS)

### DEFAULTS ###
# USAGE: make dbg A="[a,b]"
all: test debug
dbg: idbg
test: test-exec
style: style-lint
prf: prf-dot

# --- MAIN ---
debug: ARGS += -V k
debug-all: ARGS += -V a
app:  PYARGS := -O $(PYARGS)

# --- DEBUGGING ---
udbg: PYARGS += -m pudb.run
idbg: PYARGS += -m ipdb
vdbg: PYARGS += -S ~/pkg/Komodo-PythonRemoteDebugging/pydbgp -d localhost:9000
# py3_dbgp
dasm: PYARGS += -m dis

# --- PROFILING ---
# PYARGS += -O -m timeit -n 10
# python -m timeit -s 'text = "sample string"; char = "g"'  'char in text'
time: PY3 := time -v $(PY3)
time: app
time-client:
	time bash -c "for i in {1..10}; do time $(PR); echo; done"
trace: PYARGS := -O -m trace --count -C
trace: app
profile: PYARGS += -O -m cProfile $(PRFARGS)
# [-o output_file] [-s sort_order:{line, calls, pcalls, cumulative, cumtime, time, tottime, name } ]

prf-cli prf-gui prf-dot: PRFARGS += -o $(PRF)
prf-cli: PRFARGS += -s cumulative
prf-cli: profile
	@$(PY3) -c "import pstats;pstats.Stats('$(PRF)').strip_dirs().sort_stats('cumulative').print_stats()" | vim -R -
#   https://docs.python.org/3.4/library/profile.html#instant-user-s-manual
prf-gui: profile
	@pyprof2calltree -i $(PRF) -k
prf-dot: profile
	@gprof2dot -f pstats $(PRF) | dot -Tpng -o $(PRF:.prof=.png) && sxiv $(PRF:.prof=.png)
prf-mem-total:
	@mprof run -T 0.01 -C --python $(PY3) $(PR) && mprof plot
# -s <time> -- for statistics, -t 0/1 -- trace threads, -f callgrind/text -- format
prf-line-total:
	@pprofile -f callgrind --out $(PRF) --threads 1 $(PR) && kcachegrind $(PRF)

# For both -mem and -line you need to put decorator @profile on line before
# functions you are insterested in. They are undefined, so remove them after testing.
prf-mem: PYARGS += -m memory_profiler
prf-line:
	@kernprof -v -l $(PR)

## {-u -- unbuffered output for vim's :make}
debug debug-all app udbg idbg vdbg dasm profile prf-mem:
	$(PY3) -u $(PYARGS) $(PR) $(ARGS) $(A)


### TEST ###
# {-s -- turns off capture output, !dbgrs may need!}
test-dbg: MODARGS += --capture=no
test-lst: MODARGS += --collect-only

test-dbg test-lst: test-exec
test-exec: export PYTHONPATH += .
test-exec:
	@py.test $(MODARGS)  # python3 -m pytest my_file_test.py


### STYLE ###
style-lint: export PYTHONPATH += .
style-lint:
	@pylint --reports=no --output-format=parseable \
		--extension-pkg-whitelist=PyQt5 \
		--disable=C0111,C0103,W0613 $(NM)
# W0232,E1101

style-pep:  MODARGS += --first --statistics
style-more: MODARGS += --show-source --show-pep8
style-pep style-more:
	@pep8 $(PEP8)


### SETUP ###
keys:
	xbindkeys -mk


### USAGE ###
# ALT: {-B -- don't write .pyc}
clean:
	find . -name "*.pyc" -exec rm {} \;
deploy:
	@./scripts/deploy
log:
	@./scripts/show-changelog
help:
	@echo "Use one of those targets: $(TARGS)"
