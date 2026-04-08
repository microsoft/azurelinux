# less initialization script (csh)

# All less.*sh files should have the same semantics!

# In case you are curious, the test for non-emptiness is not as easy as in
# Bourne shell.  This "eval" construct is probably inspired by Stack
# Overflow question 13343392.
if ( $?LESSOPEN && { eval 'test ! -z "$LESSOPEN"' } ) then
    :
else
    if ( -x /usr/bin/lesspipe.sh ) then
        # The '||' here is intentional, see rhbz#1254837.
        setenv LESSOPEN "||/usr/bin/lesspipe.sh %s"
    endif
endif
