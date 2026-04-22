#!/bin/sh
# Upstream documents: erl +sbtu +A1 -noinput -mode minimal -boot start_clean -s rebar3 main -extra "$@"
# We omit -mode minimal because lazy module loading causes failures
# when test suites expect standard OTP modules to be already initialized.
exec erl +sbtu +A1 -noinput -boot start_clean -s rebar3 main -extra "$@"
