1,/<iso_639_entries/b

# on each new iso-code process the current one
\!\(<iso_639_entry\|</iso_639_entries>\)!{
    x
    s/^$//
    # we are on the first iso-code--nothing to process here
    t
    # process and write to output
    s/\s\+/ /g
    s/<iso_639_entry//
    s!/\s*>!!
    # use '%' as a separator of parsed and unparsed input
    s/\(.*\)iso_639_2T_code="\([^"]\+\)"\(.*\)/\2 % \1 \3/
    s/\([^%]\+\)%\(.*\)iso_639_2B_code="\([^"]\+\)"\(.*\)/\1\t\3 % \2 \4/
    #  clear subst. memory for the next t
    t clear
    :clear
    s/\([^%]\+\)%\(.*\)iso_639_1_code="\([^"]\+\)"\(.*\)/\1\t\3 % \2 \4/
    t name
    # no 639-1 code--write xx
    s/%/\tXX %/
    :name
    s/\([^%]\+\)%\(.*\)name="\([^"]\+\)"\(.*\)/\1\t\3/
    s/ \t/\t/g
    p
    b
    :noout
}

H
