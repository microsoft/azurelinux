# unannotation.awk: filter to remove annotations in dictionaries.
#
# Copyright (C) 2001, 2002 SKK Development Team <skk@ring.gr.jp>
#
# Maintainer: SKK Development Team <skk@ring.gr.jp>
#
# This file is part of Daredevil SKK.
#
# Daredevil SKK is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2, or
# (at your option) any later version.
#
# Daredevil SKK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Daredevil SKK, see the file COPYING.  If not, write to
# the Free Software Foundation Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301, USA.

BEGIN{
    print ";; -*- text -*-";
    ctime = myctime(0);
    this = ARGV[1];
    if (match(this, "\.annotated$") != 0){
	this = substr(this, 1, RSTART - 1);
    } else
	this = this ".unannotated";
    printf(";; %s was generated automatically by unannotation.awk at %s\n",
	   this, ctime);
    #getline modeindicator
    #if (match(modeindicator, /;; -*- text -*-/) != 0){
    #    print modeindicator;
    #}
}
#$0 !~ /"^;; -\*- text -\*-\n"/{
{
    if (match($0, /^;/) == 0) {
	gsub(";[^/]*/", "/");
	if (DEQUOTE && $0 ~ /\\073/) {
	    $0 = dequote($0);
	}
    }
    print;
}
function myctime(ts,    format) {
    format = "%a %b %e %H:%M:%S %Y";
    if (ts == 0)
	ts = systime();         # use current time as default
    return strftime(format, ts);
}
# convert '\073' to ';' and strip '(concat "...")'.
# example: 'smile /(concat "^_^\073\073")/:-)/' to 'smile /^_^;;/:-)/'
# @param s string to convert
# @return converted string
function dequote(s) {
    ret = "";
    n = split(s, a, "/");
    for (i = 1; i < n; i++) {
	if (a[i] ~ /^\(concat ".*\\073.*"\)$/) {	# \073 = ';'
	    gsub(/\\073/, ";", a[i]);
	    if (a[i] !~ /\\/) {	# no other quote
		a[i] = gensub(/^\(concat "(.*)"\)$/, "\\1", "g", a[i]);
	    }
	}
	ret = ret a[i] "/";
    }
    return ret;
}
# end of unannotation.awk.
