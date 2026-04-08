# Generate OUTPUT_FORMAT line for .so files from the system linker output.
# Imported from glibc/Makerules.

/ld.*[ 	]-E[BL]/b f
/collect.*[ 	]-E[BL]/b f
/OUTPUT_FORMAT[^)]*$/{N
s/\n[	 ]*/ /
}
t o
: o
s/^.*OUTPUT_FORMAT(\([^,]*\), \1, \1).*$/OUTPUT_FORMAT(\1)/
t q
s/^.*OUTPUT_FORMAT(\([^,]*\), \([^,]*\), \([^,]*\)).*$/\1,\2,\3/
t s
s/^.*OUTPUT_FORMAT(\([^,)]*\).*$)/OUTPUT_FORMAT(\1)/
t q
d
: s
s/"//g
G
s/\n//
s/^\([^,]*\),\([^,]*\),\([^,]*\),B/OUTPUT_FORMAT(\2)/p
s/^\([^,]*\),\([^,]*\),\([^,]*\),L/OUTPUT_FORMAT(\3)/p
s/^\([^,]*\),\([^,]*\),\([^,]*\)/OUTPUT_FORMAT(\1)/p
/,/s|^|*** BUG in libc/scripts/output-format.sed *** |p
q
: q
s/"//g
p
q
: f
s/^.*[ 	]-E\([BL]\)[ 	].*$/,\1/
t h
s/^.*[ 	]-E\([BL]\)$/,\1/
t h
d
: h
h
