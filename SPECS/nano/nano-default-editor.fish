# Ensure GNU nano is set as EDITOR if it isn't already set
# This is set as a universal variable so that any other definition
# by the user would win
# Cf. https://fishshell.com/docs/current/index.html#variables-scope

if ! set -q EDITOR;
	set -x EDITOR /usr/bin/nano
end
