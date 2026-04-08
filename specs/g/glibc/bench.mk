objpfx = $(prefix)/$(ver)/usr/libexec/glibc-benchtests/

bench-math := acos acosh asin asinh atan atanh cos cosh exp exp2 ffs ffsll \
	      log log2 modf pow rint sin sincos sinh sqrt tan tanh

bench-pthread := pthread_once

bench := $(bench-math) $(bench-pthread)

run-bench := $(prefix)/$(ver)/lib64/ld-linux-x86-64.so.2 --library-path $(prefix)/$(ver)/lib64 $${run}

# String function benchmarks.
string-bench := bcopy bzero memccpy memchr memcmp memcpy memmem memmove \
		mempcpy memset rawmemchr stpcpy stpncpy strcasecmp strcasestr \
		strcat strchr strchrnul strcmp strcpy strcspn strlen \
		strncasecmp strncat strncmp strncpy strnlen strpbrk strrchr \
		strspn strstr strcpy_chk stpcpy_chk memrchr strsep strtok
string-bench-all := $(string-bench)

stdlib-bench := strtod

benchset := $(string-bench-all) $(stdlib-bench)

bench-malloc := malloc-thread

binaries-bench := $(addprefix $(objpfx)bench-,$(bench))
binaries-benchset := $(addprefix $(objpfx)bench-,$(benchset))
binaries-bench-malloc := $(addprefix $(objpfx)bench-,$(bench-malloc))

DETAILED_OPT :=

ifdef DETAILED
	DETAILED_OPT := -d
endif

bench: bench-set bench-func bench-malloc

bench-set: $(binaries-benchset)
	for run in $^; do \
	  outfile=$(prefix)/$$(basename $${run}.$(ver).out); \
	  echo "Running $${run}"; \
	  $(run-bench) > $${outfile}.tmp; \
	  mv $${outfile}{.tmp,}; \
	done

bench-malloc: $(binaries-bench-malloc)
	run=$(objpfx)bench-malloc-thread; \
	outfile=$(prefix)/$$(basename $${run}.$(ver).out); \
	for thr in 1 8 16 32; do \
	  echo "Running $${run} $${thr}"; \
	  $(run-bench) $${thr} > $${outfile}.tmp; \
	  mv $${outfile}{.tmp,}; \
	done

# Build and execute the benchmark functions.  This target generates JSON
# formatted bench.out.  Each of the programs produce independent JSON output,
# so one could even execute them individually and process it using any JSON
# capable language or tool.
bench-func: $(binaries-bench)
	{ echo "{\"timing_type\": \"hp-timing\","; \
	echo " \"functions\": {"; \
	for run in $^; do \
	  if ! [ "x$${run}" = "x$<" ]; then \
	    echo ","; \
	  fi; \
	  echo "Running $${run}" >&2; \
	  $(run-bench) $(DETAILED_OPT); \
	done; \
	echo; \
	echo " }"; \
	echo "}"; } > $(prefix)/bench.$(ver).out-tmp; \
	if [ -f $(prefix)/bench.$(ver).out ]; then \
	  mv -f $(prefix)/bench.$(ver).out{,.old}; \
	fi; \
	mv -f $(prefix)/bench.$(ver).out{-tmp,}
#	scripts/validate_benchout.py bench.out \
#		scripts/benchout.schema.json
