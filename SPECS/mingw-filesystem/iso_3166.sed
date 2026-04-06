1,/<iso_3166_entries/b

# on each new iso-code process the current one
\!\(<iso_3166_entry\|</iso_3166_entries>\)!{
    x
    s/^$//
    # we are on the first iso-code--nothing to process here
    t
    # process and write to output
    s/\s\+/ /g
    s/<iso_3166_entry//
    s!/\s*>!!
    # use '%' as a separator of parsed and unparsed input
    s/\(.*\)alpha_2_code="\([^"]\+\)"\(.*\)/\2 % \1 \3/
    s/\([^%]\+\)%\(.*\)alpha_3_code="\([^"]\+\)"\(.*\)/\1% \2 \4/
    #  clear subst. memory for the next t
    t clear
    :clear
    s/\([^%]\+\)%\(.*\)numeric_code="\([^"]\+\)"\(.*\)/\1% \2 \4/
    t name
    # no 3166 code--write xx
    s/%/\tXX %/
    :name
    s/\([^%]\+\)%\(.*\)name="\([^"]\+\)"\(.*\)/\1\t\3/
    s/ \t/\t/g
    p
    b
    :noout
}

H
