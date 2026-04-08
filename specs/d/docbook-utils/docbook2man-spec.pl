=head1 NAME

docbook2man-spec.pl - convert DocBook RefEntries to Unix manpages

=head1 SYNOPSIS

The sgmlspl script from the SGMLSpm Perl module must be used to run
this script.  Use it like this:

nsgmls some-docbook-document.sgml | sgmlspl docbook2man-spec.pl

See man page or included DocBook documentation for details.

=head1 DESCRIPTION

This is a sgmlspl spec file that produces Unix-style
man pages from DocBook RefEntry markup.

=head1 COPYRIGHT

Copyright (C) 1998-2001 Steve Cheng <stevecheng@users.sourceforge.net>

Copyright (C) 1999 Thomas Lockhart <lockhart@alumni.caltech.edu>

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation; either version 2, or (at your option) any later
version.

You should have received a copy of the GNU General Public License along with
this program; see the file COPYING.  If not, please write to the Free
Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.

=cut

# $Id: docbook2man-spec.pl,v 1.11 2010/10/04 10:23:31 ovasik Exp $

use SGMLS;			# Use the SGMLS package.
use SGMLS::Output;		# Use stack-based output.
use SGMLS::Refs;


########################################################################
# SGMLSPL script produced automatically by the script sgmlspl.pl
#
# Document Type: any, but processes only RefEntries
# Edited by: me :)
########################################################################


$write_manpages = 0;
$blank_xrefs = 0;

$default_sect = "1";
$default_date = `date "+%d %B %Y"`;
$cite_numeral_only = 1;

while (@ARGV) {
	my $arg = shift @ARGV;
	if ($arg eq "--section") {
		$default_sect = shift @ARGV || die "$arg requires an argument\n";
	} elsif ($arg eq "--date") {
		$default_date = shift @ARGV || die "$arg requires an argument\n";
	} elsif ($arg eq "--lowercase") {
		$lowercase_names = 1;
	} elsif ($arg eq "--preserve-case") {
		$lowercase_names = 0;
	} elsif ($arg eq "--cite-numeral-only") {
		$cite_numeral_only = 1;
	} elsif ($arg eq "--nocite-numeral-only") {
		$cite_numeral_only = 0;
	} elsif ($arg eq "--help") {
		print "Usage: $0",
			" [ --section <label> ]",
			" [ --date <string> ]",
			" [ --lowercase | --preserve-case ]",
			" [ --cite-numeral-only | --nocite-numeral-only ]",
			"\n";
		exit;
	} else {
		die "unrecognized switch $arg; try $0 --help\n";
	}
}

sgml('start', sub { 
	push_output('nul');
	$raw_cdata = 1;			# Makes it a bit faster.
	
	# Links file
	open(LINKSFILE, ">manpage.links");

	$Refs = new SGMLS::Refs("manpage.refs", "manpage.log");
});
sgml('end', sub {
	close(LINKSFILE);

	# Explicitly invoke destructor,
	# otherwise cache file may not get written!
	# Thomas Lockhart, 1999-08-03, perl-5.004, RedHat5.2
	undef $Refs;

	if($blank_xrefs) {
		warn "Warning: output contains unresolved XRefs\n";
	}
});


########################################################################
#
# Output helpers 
#
########################################################################

# Remove leading and trailing blanks.

sub StripString
{
	my $str = shift;

	$str = $1 if ($str =~ m#^\s*(\S.*)#);
	$str = $1 if ($str =~ m#^(.*\S)\s*$#);

	return $str;
}

# Generate a good file name, for given manpage title and manvolnum
# (cdata content).
# Cleanup whitespace and convert to lower case if required.

sub FileInfo
{
	my $title = StripString(shift);
	my $volnum = StripString(shift);

	$title = lc $title if $lowercase_names;

	$title =~ tr/ /_/;
	$volnum =~ tr/ /_/;

	my $sectcite = $volnum;
	# The 'package name' part of the section should
	# not be used when citing it.
	if ($cite_numeral_only) {
		$sectcite = $1 if ($volnum =~ /^([0-9]+)/);
	}
	
	return ("$title.$volnum", "$title($sectcite)");
}

# Our own version of sgml() and output() to allow simple string output
# to play well with roff's stupid whitespace rules. 

sub man_sgml
{
	if(ref($_[1]) eq 'CODE') {
		return &sgml;
	}
	
	my $s = $_[1];
	$s =~ s/\\/\\\\/g;
	$s =~ s/'/\\'/g;

	sgml($_[0], eval("sub { man_output '$s' }"));
}

sub man_output
{
	if($separator eq 'full') {
		output "\n" unless $newline_last++;
		output ".PP\n";
		$separator = '';
	}
	
	$_ = shift;
	if(s/^\n//) {
		output "\n" unless $newline_last++;
	}
	return if $_ eq '';
	
	output $_;

	if(@_) {
		output @_;
		$newline_last = (pop(@_) =~ /\n$/);
	} else {
		$newline_last = ($_ =~ /\n$/)
	}
}

# Fold lines into one, quote some characters
sub fold_string
{
	$_ = shift;
	
	s/\\/\\\\/g;
	s/"/""/g;

	# Change tabs and newlines to spaces
	# The newlines will be swallowed later while trimming
	tr/[\t\n]/  /;

	# Trim whitespace from beginning and end.
	s/^ +//;
	s/ +$//;

	return $_;
}
	
sub save_cdata()
{
	$raw_cdata++;
	push_output('string');
}

sub bold_on()
{
	# If the last font is also bold, don't change anything.
	# Basically this is to just get more readable man output.
	if($fontstack[$#fontstack] ne 'bold') {
		if(!$raw_cdata) {
			output '\fB';
			#$newline_last = 0;
		}
	}
	push(@fontstack, 'bold');
}

sub italic_on()
{
	# If the last font is also italic, don't change anything.
	if($fontstack[$#fontstack] ne 'italic') {
		if(!$raw_cdata) {
			output '\fI';
			#$newline_last = 0;
		}
	}
	push(@fontstack, 'italic');
}

sub font_off()
{
	my $thisfont = pop(@fontstack);
	my $lastfont = $fontstack[$#fontstack];
	
	# Only output font change if it is different
	if($thisfont ne $lastfont) {
		if($raw_cdata)			{ return; }
		elsif($lastfont eq 'bold') 	{ output '\fB'; }
		elsif($lastfont eq 'italic')	{ output '\fI'; }
		else				{ output '\fR'; }
	
		#$newline_last = 0;
	}
}


########################################################################
#
# Manpage management
#
########################################################################

sgml('<REFENTRY>', sub { 
	# This will be overwritten at end of REFMETA, when we know the name of the page.
	pop_output();
	
	$write_manpages = 1;		# Currently writing manpage.
	
	$nocollapse_whitespace = 0;	# Current whitespace collapse counter.
	$newline_last = 1;		# At beginning of line?
		# Just a bit of warning, you will see this variable manipulated
		# manually a lot.  It makes the code harder to follow but it
		# saves you from having to worry about collapsing at the end of
		# parse, stopping at verbatims, etc.
	$raw_cdata = 0;                 # Instructs certain output functions to
					# leave CDATA alone, so we can assign
					# it to a string and process it, etc.
	@fontstack = ();		# Fonts being activated.
	
	$list_nestlevel = 0;		# Indent certain nested content.

	# Separator to use between 'elements' in the content of a
	# paragraph (usually).  This makes sure that PCDATA after a list
	# in a PARA gets a break in between and not become part of the
	# last listitem.  Note that we can't do it after the list ends,
	# because often the list ends the paragraph and we'll get an
	# extra break.  Anything that changes the separator status from
	# the default should also save its last state in the parent
	# element's ext, but I'm not going to explain further.  It's a
	# gross hack and almost guaranteed to fail in unforseen cases.
	# The only way to avoid all this is to use a tree/grove model, which
	# we're _not_ doing.
	$separator = '';
	
	$manpage_title = '';		# Needed for indexing.
	$manpage_sect = '';
	@manpage_names = ();
	
	$manpage_misc = '';

	# check refentry's language
	if(defined($_[0]->attribute('LANG')->value)) {
	  $manpage_lang = $_[0]->attribute('LANG')->value;
	}
	else {
	  $manpage_lang = '';
	}
});
sgml('</REFENTRY>', sub {
	if(!$newline_last) {
		output "\n";
	}
	
	$raw_cdata = 1;
	push_output('nul');

	$write_manpages = 0;
});

sgml('</REFMETA>', sub {
	my ($filename, $citation) = 
		FileInfo($manpage_title, $manpage_sect || $default_sect);

	push_output('file', $filename);

	output <<'_END_BANNER';
.\" auto-generated by docbook2man-spec from docbook-utils package
_END_BANNER

	my $manpage_date = $_[0]->parent->ext->{'date'} || $default_date;

	output '.TH "';

	# If the title is not mixed-case, convention says to
	# uppercase the whole title.  (The canonical title is
	# lowercase.)
	if($manpage_title =~ /[A-Z]/) {
		output fold_string($manpage_title);
	} else {
		output uc(fold_string($manpage_title));
	}
	
	output  '" "', fold_string($manpage_sect), 
		'" "', fold_string($manpage_date),
		'" "', $manpage_misc, 
		'" "', $manpage_manual, 
		"\"\n";

	$newline_last = 1;

	# References to this RefEntry.
	if(defined($_[0]->parent->attribute('ID')->value)) {
		my $id = $_[0]->parent->attribute('ID')->value;

		# Append XREFLABEL content to citations.
		if(defined($_[0]->parent->attribute('XREFLABEL')->value)) {
			$citation = $_[0]->parent->attribute('XREFLABEL')->value .
					' [' . $citation . ']';
		}

		$Refs->put("refentry:$id", $citation);
	}
});

sgml('<REFENTRYTITLE>', sub { 
	if($_[0]->in('REFMETA')) { 
		save_cdata();
	} else { 
		# Manpage citations are in bold.
		bold_on();
	}
});
sgml('</REFENTRYTITLE>', sub { 
	if($_[0]->in('REFMETA')) {
		$raw_cdata--;
		$manpage_title = pop_output();
	}
	else { font_off(); }

	if (defined($_[0]->attribute('ID')->value)) {
		my $id = $_[0]->attribute('ID')->value;
		$Refs->put("refentrytitle:$id", $manpage_title);
	}
});

sgml('<MANVOLNUM>', sub { 
	if($_[0]->in('REFMETA')) { 
		save_cdata();	
	} else {
		# Manpage citations use ().
		output '(';
	}
});
sgml('</MANVOLNUM>', sub { 
	if($_[0]->in('REFMETA')) {
		$raw_cdata--;
		$manpage_sect = pop_output();
	}
	else { output ')' }
});

sgml('<REFMISCINFO>', \&save_cdata);
sgml('</REFMISCINFO>', sub { 
	$raw_cdata--;
	$manpage_misc = fold_string(pop_output());
});


# NAME section
#man_sgml('<REFNAMEDIV>', "\n.SH NAME\n");
man_sgml('<REFNAMEDIV>', sub {
	my %text = { fr=>'NOM', es=>'NOMBRE', pl=>'NAZWA' };
	
	if(defined $text{lc($manpage_lang)})
	{
		man_output "\n.SH " . $text{lc($manpage_lang)} . "\n";
	} elsif(defined $_[0]->attribute('LANG') and
		defined $text{lc($_[0]->attribute('LANG')->value)})
	{
		man_output "\n.SH " . $text{lc($_[0]->attribute('LANG'))} . "\n";
	} else {
		man_output "\n.SH NAME\n";
	}
});

sgml('<REFNAME>', \&save_cdata);
sgml('</REFNAME>', sub { 
	$raw_cdata--;
	push(@manpage_names, pop_output());
});

sgml('<REFPURPOSE>', \&save_cdata);
sgml('</REFPURPOSE>', sub { 
	$raw_cdata--;
	my $manpage_purpose = fold_string(pop_output());
	
	for(my $i = 0; $i < $#manpage_names; $i++) {
		output fold_string($manpage_names[$i]), ', ';
	}

	output fold_string($manpage_names[$#manpage_names]);
	output " \\- $manpage_purpose\n";

	$newline_last = 1;

	foreach(@manpage_names) {
		# Don't link to itself
		if($_ ne $manpage_title) {
			print LINKSFILE "$manpage_title.$manpage_sect	$_.$manpage_sect\n";
		}
	}
});
	
man_sgml('<REFCLASS>', "\n.sp\n");

#RefDescriptor


########################################################################
#
# SYNOPSIS section and synopses
#
########################################################################

#man_sgml('<REFSYNOPSISDIV>', "\n.SH SYNOPSIS\n");
man_sgml('<REFSYNOPSISDIV>', sub {
	   if ($manpage_lang eq "pl") { man_output "\n.SH SK£ADNIA\n"; }
	   # waits for another languages
	   #elsif ($manpage_lang eq "xx") { man_output "\n.SH xxxxxxx\n"; } 
	   else { man_output "\n.SH SYNOPSIS\n"; }
});   

man_sgml('</REFSYNOPSISDIV>', "\n");

## FIXME! Must be made into block elements!!
#sgml('<FUNCSYNOPSIS>', \&bold_on);
#sgml('</FUNCSYNOPSIS>', \&font_off);
#sgml('<CMDSYNOPSIS>', \&bold_on);
#sgml('</CMDSYNOPSIS>', \&font_off);

man_sgml('<FUNCSYNOPSIS>', sub {
	man_output("\n.nf\n");
	bold_on();
});
man_sgml('</FUNCSYNOPSIS>', sub {
	man_output("\n.fi");
	font_off();
});

man_sgml('<CMDSYNOPSIS>', "\n.sp\n");
man_sgml('</CMDSYNOPSIS>', "\n");

man_sgml('<FUNCPROTOTYPE>', "\n.sp\n");

# Arguments to functions.  This is C convention.
#man_sgml('<PARAMDEF>', '(');
#man_sgml('</PARAMDEF>', ");\n");
#man_sgml('<VOID>', "(void);\n");
sub paramdef
{
	if($_[0]->parent->ext->{'inparams'}) {
		output ', ';
	} else {
		output ' (';
		$_[0]->parent->ext->{'inparams'} = 1;
	}
}
man_sgml('<PARAMDEF>', \&paramdef);
man_sgml('</FUNCPROTOTYPE>', ");\n");
man_sgml('<VOID>', "(void");
man_sgml('<VARARGS>', "(...");


sub arg_start
{
	# my $choice = $_[0]->attribute('CHOICE')->value;

	# The content model for CmdSynopsis doesn't include #PCDATA,
	# so we won't see any of the whitespace in the source file,
	# so we have to add it after each component.
	man_output ' ';

	if($_[0]->attribute('CHOICE')->value =~ /opt/i) {
		man_output '[ ';
	}
	bold_on();
}
sub arg_end
{
	font_off();
	if($_[0]->attribute('REP')->value =~ /^Repeat/i) {
		italic_on();
		man_output '...';
		font_off();
	}
	if($_[0]->attribute('CHOICE')->value =~ /opt/i) {
		man_output ' ] ';
	}
}

sgml('<ARG>', \&arg_start);
sgml('</ARG>', \&arg_end);
sgml('<GROUP>', \&arg_start);
sgml('</GROUP>', \&arg_end);

sgml('<OPTION>', \&bold_on);
sgml('</OPTION>', \&font_off);

# FIXME: This is one _blank_ line.
man_sgml('<SBR>', "\n\n");


########################################################################
#
# General sections
#
########################################################################

# The name of the section is handled by TITLE.  This just sets
# up the roff markup.
man_sgml('<REFSECT1>', sub { $separator = ''; man_output "\n.SH "});
man_sgml('<REFSECT2>', sub { $separator = ''; man_output "\n.SS "});
man_sgml('<REFSECT3>', sub { $separator = ''; man_output "\n.SS "});


########################################################################
#
# Titles, metadata.
#
########################################################################

sgml('<TITLE>', sub {
	if($_[0]->in('REFERENCE') or $_[0]->in('BOOK')) {
		$write_manpages = 1;
	}
	save_cdata();
});
sgml('</TITLE>', sub {
	my ($element, $event) = @_;
	my $title = fold_string(pop_output());
	$raw_cdata--;
	
	if($element->in('REFERENCE') or $element->in('BOOK')) {
		# We use TITLE of enclosing Reference or Book as manual name
		$manpage_manual = $title;
		$write_manpages = 0;
	}
	elsif(exists $element->parent->ext->{'title'}) {
		# By far the easiest case.  Just fold the string as
		# above, and then set the parent element's variable.
		$_[0]->parent->ext->{'title'} = $title;
	}
	else {
		# If the parent element's handlers are lazy, 
		# output the folded string for them :)
		# We assume they want uppercase and a newline.
		man_output '"', uc($title), "\"\n";
	}

	if (defined($element->attribute('ID')->value)) {
		my $id = $_[0]->attribute('ID')->value;
		$Refs->put("title:$id", $title);
	}

	my ($filename, $citation) =
		FileInfo($manpage_title, $manpage_sect || $default_sect);
	my $parentid = $element->parent->attribute('ID')->value;
	if ($parentid and ($element->in('REFSECT1') or $element->in('REFSECT2') or $element->in('REFSECT3'))) {
		$Refs->put("refsect:$parentid", "$citation");
	}
});

sgml('<ATTRIBUTION>', sub { 
	if($_[0]->in('BLOCKQUOTE')) {
		push_output('string');
	}
});
sgml('</ATTRIBUTION>', sub { 
	if($_[0]->in('BLOCKQUOTE')) {
		$_[0]->parent->ext->{'attribution'} = pop_output(); 
	} else {
		# For an Epigraph.
		man_output "\n\n";
	}
});

sgml('<DATE>', sub {
      save_cdata();
});
sgml('</DATE>', sub {
      $_[0]->parent->parent->ext->{'date'} = fold_string(pop_output());
      $raw_cdata--;
});

sub ignore_content { push_output 'nul'; }
sub restore_content { pop_output(); }

sgml('<DOCINFO>', \&ignore_content);
sgml('</DOCINFO>', \&restore_content);
sgml('<REFSYNOPSISDIVINFO>', \&ignore_content);
sgml('</REFSYNOPSISDIVINFO>', \&restore_content);
sgml('<REFSECT1INFO>', \&ignore_content);
sgml('</REFSECT1INFO>', \&restore_content);
sgml('<REFSECT2INFO>', \&ignore_content);
sgml('</REFSECT2INFO>', \&restore_content);
sgml('<REFSECT3INFO>', \&ignore_content);
sgml('</REFSECT3INFO>', \&restore_content);

sgml('<INDEXTERM>', \&ignore_content);
sgml('</INDEXTERM>', \&restore_content);

sgml('<AUTHORBLURB>', \&ignore_content);
sgml('</AUTHORBLURB>', \&restore_content);


########################################################################
#
# Set bold on enclosed content 
#
########################################################################

sgml('<APPLICATION>', \&bold_on);
sgml('</APPLICATION>', \&font_off);

sgml('<CLASSNAME>', \&bold_on);		sgml('</CLASSNAME>', \&font_off);
sgml('<STRUCTNAME>', \&bold_on);	sgml('</STRUCTNAME>', \&font_off);
sgml('<STRUCTFIELD>', \&bold_on);	sgml('</STRUCTFIELD>', \&font_off);
sgml('<SYMBOL>', \&bold_on);		sgml('</SYMBOL>', \&font_off);
sgml('<TYPE>', \&bold_on);		sgml('</TYPE>', \&font_off);

sgml('<ENVAR>', \&bold_on);	sgml('</ENVAR>', \&font_off);

sgml('<FUNCTION>', \&bold_on);	sgml('</FUNCTION>', \&font_off);

sgml('<EMPHASIS>', \&bold_on);	sgml('</EMPHASIS>', \&font_off);

sgml('<ERRORNAME>', \&bold_on);	sgml('</ERRORNAME>', \&font_off);
# ERRORTYPE

sgml('<COMMAND>', \&bold_on);	sgml('</COMMAND>', \&font_off);

sgml('<GUIBUTTON>', \&bold_on);	sgml('</GUIBUTTON>', \&font_off);
sgml('<GUIICON>', \&bold_on);	sgml('</GUIICON>', \&font_off);
# GUILABEL
# GUIMENU
# GUIMENUITEM
# GUISUBMENU
# MENUCHOICE

sgml('<ACCEL>', \&bold_on);	sgml('</ACCEL>', \&font_off);
# KEYCODE
# SHORTCUT


sgml('<KEYCOMBO>', sub {
	$separator = 'none';
	$_[0]->ext->{'separator'} = 'none';
});
sgml('</KEYCOMBO>', sub { $separator = $_[0]->parent->ext->{'separator'}; });

sub _keycombo {
	if($_[0]->in('KEYCOMBO')) {
		if($separator eq 'none') { $separator = '' }
		else { man_output "+"; }
	}
	bold_on();
}
sgml('<KEYCAP>', \&_keycombo);	sgml('</KEYCAP>', \&font_off);
sgml('<KEYSYM>', \&_keycombo);	sgml('</KEYSYM>', \&font_off);
sgml('<MOUSEBUTTON>', \&_keycombo);	sgml('</MOUSEBUTTON>', \&font_off);


sgml('<USERINPUT>', \&bold_on);	sgml('</USERINPUT>', \&font_off);

sgml('<INTERFACEDEFINITION>', \&bold_on);
sgml('</INTERFACEDEFINITION>', \&font_off);

# May need to look at the CLASS
sgml('<SYSTEMITEM>', \&bold_on);
sgml('</SYSTEMITEM>', \&font_off);


########################################################################
#
# Set italic on enclosed content 
#
########################################################################

sgml('<FIRSTTERM>', \&italic_on);	sgml('</FIRSTTERM>', \&font_off);

sgml('<FILENAME>', \&italic_on);	sgml('</FILENAME>', \&font_off);
sgml('<PARAMETER>', \&italic_on);	sgml('</PARAMETER>', \&font_off);
sgml('<PROPERTY>', \&italic_on);	sgml('</PROPERTY>', \&font_off);

sgml('<REPLACEABLE>', sub {
	italic_on();
	if($_[0]->in('TOKEN')) {
		# When tokenizing, follow more 'intuitive' convention
		output "<";
	}
});
sgml('</REPLACEABLE>', sub {
	if($_[0]->in('TOKEN')) {
		output ">";
	}
	font_off();
});

sgml('<CITETITLE>', \&italic_on);	sgml('</CITETITLE>', \&font_off);
sgml('<FOREIGNPHRASE>', \&italic_on);	sgml('</FOREIGNPHRASE>', \&font_off);

sgml('<LINEANNOTATION>', \&italic_on);	sgml('</LINEANNOTATION>', \&font_off);


########################################################################
#
# Other 'inline' elements 
#
########################################################################

man_sgml('<EMAIL>', '<');
man_sgml('</EMAIL>', '>');
man_sgml('<OPTIONAL>', '[');
man_sgml('</OPTIONAL>', ']');

man_sgml('</TRADEMARK>', "\\u\\s-2TM\\s+2\\d");

man_sgml('<COMMENT>', "[Comment: ");
man_sgml('</COMMENT>', "]");

man_sgml('<QUOTE>', "``");
man_sgml('</QUOTE>', "''");

#man_sgml('<LITERAL>', '"');
#man_sgml('</LITERAL>', '"');
# There doesn't seem to be a good way to represent LITERAL in -man
# ComputerOutput, SGMLTag, Markup are the same thing.

# These create spaces between content in special elements
# without PCDATA content.
man_sgml('</HONORIFIC>', " ");
man_sgml('</FIRSTNAME>', " ");
man_sgml('</SURNAME>', " ");
man_sgml('</LINEAGE>', " ");
man_sgml('</OTHERNAME>', " ");

man_sgml('<AFFILIATION>', "(");
man_sgml('</AFFILIATION>', ") ");
man_sgml('<CONTRIB>', "(");
man_sgml('</CONTRIB>', ") ");

man_sgml('</STREET>', " ");
man_sgml('</POB>', " ");
man_sgml('</POSTCODE>', " ");
man_sgml('</CITY>', " ");
man_sgml('</STATE>', " ");
man_sgml('</COUNTRY>', " ");
man_sgml('</PHONE>', " ");
man_sgml('</FAX>', " ");
man_sgml('</OTHERADDRESS>', " ");

man_sgml('</ALT>', ": ");
man_sgml('<GRAPHIC>', " [GRAPHIC] ");

# No special presentation:

# AUTHORINITIALS

# ABBREV
# ACTION
# ACRONYM
# CITATION
# PHRASE
# QUOTE
# WORDASWORD

# PROMPT
# RETURNVALUE
# TOKEN

# DATABASE
# HARDWARE
# INTERFACE
# MEDIALABEL


########################################################################
#
# Paragraph and paragraph-like elements 
#
########################################################################

sub para_start {
	if($separator eq '' or $separator eq 'full') {
		$separator = '';
		man_output "\n.PP\n";
	} elsif($separator eq 'blank') { 
		man_output "\n\n";
	} elsif($separator eq 'none' ) {
		$_[0]->parent->ext->{'separator'} = 'blank';
		$separator = 'blank';
	}
}
# Actually applies to a few other block elements as well
sub para_end {
	$separator = $_[0]->parent->ext->{'separator'};
	man_output "\n";
}

sgml('<PARA>', \&para_start);
sgml('</PARA>', \&para_end);
sgml('<SIMPARA>', \&para_start);
sgml('</SIMPARA>', \&para_end);

# Nothing special, except maybe FIXME set nobreak.
sgml('<INFORMALEXAMPLE>', \&para_start);
sgml('</INFORMALEXAMPLE>', \&para_end);


########################################################################
#
# Blocks using SS sections
#
########################################################################

# FIXME: We need to consider the effects of SS
# in a hanging tag :(

# Complete with the optional-title dilemma (again).
sgml('<ABSTRACT>', sub {
	$_[0]->ext->{'title'} = 'ABSTRACT';
	output "\n" unless $newline_last++;
	push_output('string');
});
sgml('</ABSTRACT>', sub {
	my $content = pop_output();
	
	# As ABSTRACT is never on the same level as RefSect1,
	# this leaves us with only .SS in terms of -man macros.
	output ".SS \"", uc($_[0]->ext->{'title'}), "\"\n";

	output $content;
	output "\n" unless $newline_last++;
});



# Ah, I needed a break.  Example always has a title.
sgml('<EXAMPLE>', sub { $separator = ''; man_output "\n.SS "});
sgml('</EXAMPLE>', \&para_end);

# Same with sidebar.
sgml('<SIDEBAR>', sub { $separator = ''; man_output "\n.SS "});
sgml('</SIDEBAR>', \&para_end);

sgml('<FORMALPARA>', sub { $separator = ''; man_output "\n.SS "});
sgml('</FORMALPARA>', \&para_end);

sgml('<FIGURE>', sub { $separator = ''; man_output "\n.SS "});
sgml('</FIGURE>', \&para_end);



# NO title.
sgml('<HIGHLIGHTS>', sub { $separator = ''; man_output "\n.SS HIGHLIGHTS\n"});
sgml('</HIGHLIGHTS>', \&para_end);


########################################################################
#
# Indented 'Block' elements 
#
########################################################################

sub indent_block_start
{
	$separator = '';
	man_output "\n.sp\n.RS\n";
}
sub indent_block_end
{
	$separator = $_[0]->parent->ext->{'separator'};
	man_output "\n.RE\n.sp\n";
}

sgml('<ADDRESS>', sub {
	&indent_block_start;
	if($_[0]->attribute('FORMAT')->type eq 'NOTATION'
	   and $_[0]->attribute('FORMAT')->value->name eq 'LINESPECIFIC') {
		&verbatim_start;
	}
});
sgml('</ADDRESS>', sub {
	if($_[0]->attribute('FORMAT')->type eq 'NOTATION'
	   and $_[0]->attribute('FORMAT')->value->name eq 'LINESPECIFIC') {
		&verbatim_end;
	}
	&indent_block_end;
});
	
# This element is almost like an admonition (below),
# only the default title is blank :)

sgml('<BLOCKQUOTE>', sub { 
	$_[0]->ext->{'title'} = ''; 
	&indent_block_start;
	push_output('string');
});
sgml('</BLOCKQUOTE>', sub {
	my $content = pop_output();

	if($_[0]->ext->{'title'}) {
		output ".B \"", $_[0]->ext->{'title'}, ":\"\n";
	}
	
	output $content;

	if($_[0]->ext->{'attribution'}) {
		man_output "\n\n                -- ",
				$_[0]->ext->{'attribution'}, "\n";
	}
	
	&indent_block_end;
});

# Set off admonitions from the rest of the text by indenting.
# FIXME: Need to check if this works inside paragraphs, not enclosing them.
sub admonition_end {
	my $content = pop_output();

	# When the admonition is only one paragraph,
	# it looks nicer if the title was inline.
	my $num_para;
	while ($content =~ /^\.PP/gm) { $num_para++ }
	if($num_para==1) {
		$content =~ s/^\.PP\n//;
	}
	
	output ".B \"" . $_[0]->ext->{'title'} . ":\"\n";
	output $content;
	
	&indent_block_end;
}

sgml('<NOTE>', sub {
	# We can't see right now whether or not there is a TITLE
	# element, so we have to save the output now and add it back
	# at the end of this admonition.
	$_[0]->ext->{'title'} = 'Note';
	
	&indent_block_start;
	
	push_output('string');
});
sgml('</NOTE>', \&admonition_end);

# Same as above.
sgml('<WARNING>', sub { 
	$_[0]->ext->{'title'} = 'Warning'; 
	&indent_block_start;
	push_output('string');
});
sgml('</WARNING>', \&admonition_end);

sgml('<TIP>', sub {
	$_[0]->ext->{'title'} = 'Tip';
	&indent_block_start;
	push_output('string');
});
sgml('</TIP>', \&admonition_end);
sgml('<CAUTION>', sub {
	$_[0]->ext->{'title'} = 'Caution';
	&indent_block_start;
	push_output('string');
});
sgml('</CAUTION>', \&admonition_end);

sgml('<IMPORTANT>', sub {
	$_[0]->ext->{'title'} = 'Important';
	&indent_block_start;
	push_output('string');
});
sgml('</IMPORTANT>', \&admonition_end);


########################################################################
#
# Verbatim displays. 
#
########################################################################

sub verbatim_start {
	$separator = '';
	man_output "\n.sp\n";
	man_output "\n.nf\n" unless $nocollapse_whitespace++;
}

sub verbatim_end {
	man_output "\n.sp\n";
	man_output "\n.fi\n" unless --$nocollapse_whitespace;
	$separator = $_[0]->parent->ext->{'separator'};
}

sgml('<PROGRAMLISTING>', \&verbatim_start); 
sgml('</PROGRAMLISTING>', \&verbatim_end);

sgml('<SCREEN>', \&verbatim_start); 
sgml('</SCREEN>', \&verbatim_end);

sgml('<LITERALLAYOUT>', \&verbatim_start); 
sgml('</LITERALLAYOUT>', \&verbatim_end);

sgml('<SYNOPSIS>', sub {
	my $format = $_[0]->attribute('FORMAT');

	if($format->type eq 'NOTATION'
	   and $format->value->name eq 'LINESPECIFIC')
	{
		&verbatim_start;
	} else {
		$separator = '';
		man_output "\n.sp\n";
	}
});

sgml('</SYNOPSIS>', sub {
	my $format = $_[0]->attribute('FORMAT');
	
	if($format->type eq 'NOTATION'
	   and $format->value->name eq 'LINESPECIFIC')
	{
		&verbatim_end;
	} else {
		man_output "\n";
		$_[0]->parent->ext->{'separator'} = 'full';
		$separator = 'full';
	}
});


########################################################################
#
# Lists
#
########################################################################

# Indent nested lists.
sub list_start {
	man_output "\n.RS\n" if $list_nestlevel++;
}
sub list_end {
	man_output "\n.RE\n" if --$list_nestlevel;
	$_[0]->parent->ext->{'separator'} = 'full';
	$separator = 'full';
}

sgml('<VARIABLELIST>', \&list_start);
sgml('</VARIABLELIST>', \&list_end);
sgml('<ITEMIZEDLIST>', \&list_start);
sgml('</ITEMIZEDLIST>', \&list_end);
sgml('<ORDEREDLIST>', sub { 
	&list_start;
	$_[0]->ext->{'count'} = 1;
});
sgml('</ORDEREDLIST>', \&list_end);
		
# Output content on one line, bolded.
sgml('<TERM>', sub { 
	man_output "\n.TP\n";
	bold_on();
	push_output('string');
});
sgml('</TERM>', sub { 
	my $term = StripString(pop_output());
	$term =~ tr/\n/ /;
	output $term;
	font_off();
	output "\n";
	$newline_last = 1;
});
	
sgml('<LISTITEM>', sub {
	# A bulleted list.
	if($_[0]->in('ITEMIZEDLIST')) {
		man_output "\n.TP 0.2i\n\\(bu\n";
	}

	# Need numbers.
	# Assume Arabic numeration for now.
	elsif($_[0]->in('ORDEREDLIST')) {
		man_output "\n.IP ", $_[0]->parent->ext->{'count'}++, ". \n";
	}
	
	$_[0]->ext->{'separator'} = 'none';
	$separator = 'none';
});

sgml('<SIMPLELIST>', sub {
	$_[0]->ext->{'first_member'} = 1;
});
sgml('<MEMBER>', sub {
	my $parent = $_[0]->parent;
	
	if($parent->attribute('TYPE')->value =~ /Inline/i) {
		if($parent->ext->{'first_member'}) {
			# If this is the first member don't put any commas
			$parent->ext->{'first_member'} = 0;
		} else {
			man_output ", ";
		}

	# We don't really have Horiz rendering, so it's the same
	# as Vert.
	} else {
		man_output "\n\n";
	}
});

# We implement Procedures as indent and lists

sgml('<PROCEDURE>', sub {
	$_[0]->ext->{'count'} = 1;
	&indent_block_start;
});
sgml('</PROCEDURE>', sub {
	&indent_block_end;
	$_[0]->parent->ext->{'separator'} = 'full';
	$separator = 'full';
});

sgml('<STEP>', sub {
	man_output "\n.IP ", $_[0]->parent->ext->{'count'}++, ". \n";
	$_[0]->ext->{'separator'} = 'none';
	$separator = 'none';
});


########################################################################
#
# Linkage, cross references
#
########################################################################

# Print the URL
sgml('</ULINK>', sub {
	man_output ' <URL:', $_[0]->attribute('URL')->value, '>';
});

# If cross reference target is a RefEntry, 
# output CiteRefEntry-style references.
sgml('<XREF>', sub {
	my $id = $_[0]->attribute('LINKEND')->value;

	my $manref = $Refs->get("refentry:$id") || $Refs->get("refsect:$id");
	if(!defined $manref) {
		$blank_xrefs++ if $write_manpages;
		man_output "[XRef to $id]";
		return;
	}

	# Limited ENDTERM support.
	if(defined $_[0]->attribute('ENDTERM')->value) {
		my $endterm = $_[0]->attribute('ENDTERM')->value;
		my $content = $Refs->get("title:$endterm") ||
				$Refs->get("refentrytitle:$endterm");
		man_output $content, ' [';
	}

	# This also displays the XREFLABEL (as bold)...
	# It's not worth the bother to fix it though, there
	# are better tools for this.
	my ($title, $sect) = ($manref =~ /(.*)(\(.*\))/);
	bold_on();
	man_output $title;
	font_off();
	man_output $sect;

	if(defined $_[0]->attribute('ENDTERM')->value) {
		man_output ']';
	}
});

# Anchor

########################################################################
#
# SDATA 
#
########################################################################

man_sgml('|[lt    ]|', '<');
man_sgml('|[equals]|', '=');
man_sgml('|[gt    ]|', '>');
man_sgml('|[plus  ]|', '\(pl');
man_sgml('|[dollar]|', '$');
man_sgml('|[num   ]|', '#');
man_sgml('|[percnt]|', '%');
man_sgml('|[amp   ]|', '&');
man_sgml('|[commat]|', '@');
man_sgml('|[lsqb  ]|', '[');
man_sgml('|[bsol  ]|', '\e');
man_sgml('|[rsqb  ]|', ']');
man_sgml('|[lcub  ]|', '{');
man_sgml('|[verbar]|', '\(or');
man_sgml('|[rcub  ]|', '}');
man_sgml('|[excl  ]|', '!');
man_sgml('|[quot  ]|', '"');
man_sgml('|[apos  ]|', '\\&\'');
man_sgml('|[lpar  ]|', '(');
man_sgml('|[rpar  ]|', ')');
man_sgml('|[comma ]|', ',');
man_sgml('|[lowbar]|', '_');
man_sgml('|[period]|', '.');
man_sgml('|[sol   ]|', '/');
man_sgml('|[colon ]|', ':');
man_sgml('|[semi  ]|', ';');
man_sgml('|[quest ]|', '?');
man_sgml('|[grave ]|', '`');
man_sgml('|[tilde ]|', '~');
man_sgml('|[half  ]|', '\(12');
man_sgml('|[frac12]|', '\(12');
man_sgml('|[frac14]|', '\(14');
man_sgml('|[frac34]|', '\(34');
man_sgml('|[frac18]|', '1/8');
man_sgml('|[frac38]|', '3/8');
man_sgml('|[frac58]|', '5/8');
man_sgml('|[frac78]|', '7/8');
man_sgml('|[sup1  ]|', '\u1\l');
man_sgml('|[sup2  ]|', '\u2\l');
man_sgml('|[sup3  ]|', '\u3\l');
man_sgml('|[plusmn]|', '\(+-');
man_sgml('|[divide]|', '\(di');
man_sgml('|[times ]|', '\(ti');
man_sgml('|[pound ]|', '#');
man_sgml('|[cent  ]|', '\(ct');
man_sgml('|[yen   ]|', 'yen');
man_sgml('|[ast   ]|', '*');
man_sgml('|[horbar]|', '_');
man_sgml('|[micro ]|', '\(*m');
man_sgml('|[ohm   ]|', '\(*W');
man_sgml('|[deg   ]|', '\(de');
man_sgml('|[sect  ]|', '\(sc');
man_sgml('|[larr  ]|', '\(<-');
man_sgml('|[rarr  ]|', '\(->');
man_sgml('|[uarr  ]|', '\(ua');
man_sgml('|[darr  ]|', '\(da');
man_sgml('|[copy  ]|', '\(co');
man_sgml('|[reg   ]|', '\(rg');
man_sgml('|[trade ]|', '\(tm');
man_sgml('|[brvbar]|', '|');
man_sgml('|[not   ]|', '\(no');
man_sgml('|[hyphen]|', '\-');
man_sgml('|[laquo ]|', '<<');
man_sgml('|[raquo ]|', '>>');
man_sgml('|[lsquo ]|', '`');
man_sgml('|[rsquo ]|', '\&\'');
man_sgml('|[ldquo ]|', '"');
man_sgml('|[rdquo ]|', '"');
man_sgml('|[nbsp  ]|', '\ ');
man_sgml('|[shy   ]|', '\%');
man_sgml('|[emsp  ]|', '\ \ ');
man_sgml('|[ensp  ]|', '\ ');
man_sgml('|[emsp3 ]|', '\ ');
man_sgml('|[emsp4 ]|', '\ ');
man_sgml('|[numsp ]|', '\0');
man_sgml('|[puncsp]|', '\|');
man_sgml('|[thinsp]|', '\!');
man_sgml('|[hairsp]|', '\\^');
man_sgml('|[mdash ]|', '\(em');
man_sgml('|[ndash ]|', '-');
man_sgml('|[dash  ]|', '-');
man_sgml('|[blank ]|', '\ ');
man_sgml('|[hellip]|', '\&...');
man_sgml('|[nldr  ]|', '\&..');
man_sgml('|[frac13]|', '1/3');
man_sgml('|[frac23]|', '2/3');
man_sgml('|[frac15]|', '1/5');
man_sgml('|[frac25]|', '2/5');
man_sgml('|[frac35]|', '3/5');
man_sgml('|[frac45]|', '4/5');
man_sgml('|[frac16]|', '1/6');
man_sgml('|[frac56]|', '5/6');
man_sgml('|[cir   ]|', '\(ci');
man_sgml('|[squ   ]|', '\(sq');
man_sgml('|[star  ]|', '\(**');
man_sgml('|[bull  ]|', '\(bu');
man_sgml('|[dagger]|', '\(dg');
man_sgml('|[Dagger]|', '\(dd');
man_sgml('|[caret ]|', '\^');
man_sgml('|[lsquor]|', '`');
man_sgml('|[ldquor]|', '``');
man_sgml('|[fflig ]|', '\(ff');
man_sgml('|[filig ]|', '\(fi');
man_sgml('|[ffilig]|', '\(Fi');
man_sgml('|[ffllig]|', '\(Fl');
man_sgml('|[fllig ]|', '\(fl');
man_sgml('|[rdquor]|', '\&\'\'');
man_sgml('|[rsquor]|', '\&\'');
man_sgml('|[vellip]|', '\&...');
man_sgml('|[aacute]|', '\(a\'');
man_sgml('|[Aacute]|', '\(A\'');
man_sgml('|[acirc ]|', '\(a^');
man_sgml('|[Acirc ]|', '\(A^');
man_sgml('|[agrave]|', '\(a`');
man_sgml('|[Agrave]|', '\(A`');
man_sgml('|[auml  ]|', '\(a:');
man_sgml('|[aelig ]|', '\(ae');
man_sgml('|[AElig ]|', '\(AE');
man_sgml('|[eacute]|', '\(e\'');
man_sgml('|[Eacute]|', '\(E\'');
man_sgml('|[egrave]|', '\(e`');
man_sgml('|[Egrave]|', '\(E`');
man_sgml('|[iacute]|', '\(i\'');
man_sgml('|[Iacute]|', '\(I\'');
man_sgml('|[igrave]|', '\(i`');
man_sgml('|[Igrave]|', '\(I`');
man_sgml('|[ntilde]|', '\(n~');
man_sgml('|[Ntilde]|', '\(N~');
man_sgml('|[oacute]|', '\(o\'');
man_sgml('|[Oacute]|', '\(O\'');
man_sgml('|[ograve]|', '\(o`');
man_sgml('|[Ograve]|', '\(O`');
man_sgml('|[oslash]|', '\(o/');
man_sgml('|[Oslash]|', '\(O/');
man_sgml('|[szlig ]|', '\(ss');
man_sgml('|[thorn ]|', '\(th');
man_sgml('|[uacute]|', '\(u\'');
man_sgml('|[Uacute]|', '\(U\'');
man_sgml('|[ugrave]|', '\(u`');
man_sgml('|[Ugrave]|', '\(U`');
man_sgml('|[aogon ]|', '\(ao');
man_sgml('|[agr   ]|', '\(*a');
man_sgml('|[Agr   ]|', '\(*A');
man_sgml('|[bgr   ]|', '\(*b');
man_sgml('|[Bgr   ]|', '\(*B');
man_sgml('|[ggr   ]|', '\(*g');
man_sgml('|[Ggr   ]|', '\(*G');
man_sgml('|[dgr   ]|', '\(*d');
man_sgml('|[Dgr   ]|', '\(*D');
man_sgml('|[egr   ]|', '\(*e');
man_sgml('|[Egr   ]|', '\(*E');
man_sgml('|[zgr   ]|', '\(*z');
man_sgml('|[Zgr   ]|', '\(*Z');
man_sgml('|[eegr  ]|', '\(*y');
man_sgml('|[EEgr  ]|', '\(*Y');
man_sgml('|[thgr  ]|', '\(*h');
man_sgml('|[THgr  ]|', '\(*H');
man_sgml('|[igr   ]|', '\(*i');
man_sgml('|[Igr   ]|', '\(*I');
man_sgml('|[kgr   ]|', '\(*k');
man_sgml('|[Kgr   ]|', '\(*K');
man_sgml('|[lgr   ]|', '\(*l');
man_sgml('|[Lgr   ]|', '\(*L');
man_sgml('|[mgr   ]|', '\(*m');
man_sgml('|[Mgr   ]|', '\(*M');
man_sgml('|[ngr   ]|', '\(*n');
man_sgml('|[Ngr   ]|', '\(*N');
man_sgml('|[xgr   ]|', '\(*c');
man_sgml('|[Xgr   ]|', '\(*C');
man_sgml('|[ogr   ]|', '\(*o');
man_sgml('|[Ogr   ]|', '\(*O');
man_sgml('|[pgr   ]|', '\(*p');
man_sgml('|[Pgr   ]|', '\(*P');
man_sgml('|[rgr   ]|', '\(*r');
man_sgml('|[Rgr   ]|', '\(*R');
man_sgml('|[sgr   ]|', '\(*s');
man_sgml('|[Sgr   ]|', '\(*S');
man_sgml('|[sfgr  ]|', '\(ts');
man_sgml('|[tgr   ]|', '\(*t');
man_sgml('|[Tgr   ]|', '\(*T');
man_sgml('|[ugr   ]|', '\(*u');
man_sgml('|[Ugr   ]|', '\(*U');
man_sgml('|[phgr  ]|', '\(*f');
man_sgml('|[PHgr  ]|', '\(*F');
man_sgml('|[khgr  ]|', '\(*x');
man_sgml('|[KHgr  ]|', '\(*X');
man_sgml('|[psgr  ]|', '\(*q');
man_sgml('|[PSgr  ]|', '\(*Q');
man_sgml('|[ohgr  ]|', '\(*w');
man_sgml('|[OHgr  ]|', '\(*W');
man_sgml('|[alpha ]|', '\(*a');
man_sgml('|[beta  ]|', '\(*b');
man_sgml('|[gamma ]|', '\(*g');
man_sgml('|[Gamma ]|', '\(*G');
man_sgml('|[delta ]|', '\(*d');
man_sgml('|[Delta ]|', '\(*D');
man_sgml('|[epsi  ]|', '\(*e');
man_sgml('|[epsis ]|', '\(*e');
man_sgml('|[zeta  ]|', '\(*z');
man_sgml('|[eta   ]|', '\(*y');
man_sgml('|[thetas]|', '\(*h');
man_sgml('|[Theta ]|', '\(*H');
man_sgml('|[iota  ]|', '\(*i');
man_sgml('|[kappa ]|', '\(*k');
man_sgml('|[lambda]|', '\(*l');
man_sgml('|[Lambda]|', '\(*L');
man_sgml('|[mu    ]|', '\(*m');
man_sgml('|[nu    ]|', '\(*n');
man_sgml('|[xi    ]|', '\(*c');
man_sgml('|[Xi    ]|', '\(*C');
man_sgml('|[pi    ]|', '\(*p');
man_sgml('|[Pi    ]|', '\(*P');
man_sgml('|[rho   ]|', '\(*r');
man_sgml('|[sigma ]|', '\(*s');
man_sgml('|[Sigma ]|', '\(*S');
man_sgml('|[tau   ]|', '\(*t');
man_sgml('|[upsi  ]|', '\(*u');
man_sgml('|[Upsi  ]|', '\(*U');
man_sgml('|[phis  ]|', '\(*f');
man_sgml('|[Phi   ]|', '\(*F');
man_sgml('|[chi   ]|', '\(*x');
man_sgml('|[psi   ]|', '\(*q');
man_sgml('|[Psi   ]|', '\(*X');
man_sgml('|[omega ]|', '\(*w');
man_sgml('|[Omega ]|', '\(*W');
man_sgml('|[ap    ]|', '\(ap');
man_sgml('|[equiv ]|', '\(==');
man_sgml('|[ge    ]|', '\(>=');
man_sgml('|[infin ]|', '\(if');
man_sgml('|[isin  ]|', '\(sb');
man_sgml('|[le    ]|', '\(<=');
man_sgml('|[minus ]|', '\(mi');
man_sgml('|[ne    ]|', '\(!=');
man_sgml('|[prop  ]|', '\(pt');
man_sgml('|[square]|', '\(sq');
man_sgml('|[sub   ]|', '\(sb');
man_sgml('|[sube  ]|', '\(ib');
man_sgml('|[sup   ]|', '\(sp');
man_sgml('|[supe  ]|', '\(ip');
man_sgml('|[acute ]|', '\&\'');
man_sgml('|[breve ]|', '\(be');
man_sgml('|[caron ]|', '\(hc');
man_sgml('|[cedil ]|', '\(cd');
man_sgml('|[dot   ]|', '\(dt');
man_sgml('|[macr  ]|', '\(ma');
man_sgml('|[ogon  ]|', '\(og');
man_sgml('|[ring  ]|', '\(ri');
man_sgml('|[uml   ]|', '\(..');

sgml('sdata',sub {
	my ($element, $event) = @_;
	my ($file, $line) = ($event->file, $event->line);
	man_output "|[", $_[0], "]|";
	warn "Warning: unrecognized SDATA '$_[0]'"
	     . ($file && $line ? " in $file on line $line" : "")
	     . ": please add definition to docbook2man-spec.pl\n";
});

#
# Default handlers (uncomment these if needed).  Right now, these are set
# up to gag on any unrecognised elements, sdata, processing-instructions,
# or entities.
#
# sgml('start_element',sub { die "Unknown element: " . $_[0]->name; });
# sgml('end_element','');

# This is for weeding out and escaping certain characters.
# This looks like it's inefficient since it's done on every line, but
# in reality, SGMLSpm and sgmlspl parsing ESIS takes _much_ longer.

sgml('cdata', sub
{ 
	if(!$write_manpages) { return; }
	elsif($raw_cdata) { output $_[0]; return; }

	if($separator eq 'full') {
		output "\n" unless $newline_last++;
		output ".PP\n";
		$separator = '';
	}
	
	# Escape backslashes
	$_[0] =~ s/\\/\\\\/g;

  # Escape dots and single quotes in column 1
	$_[0] =~ s/^[ \t]*\./\\\&\./;
	$_[0] =~ s/^[ \t]*\'/\\\&\'/;


	# In non-'pre'-type elements:
	if(!$nocollapse_whitespace) {
		# Change tabs to spaces
		$_[0] =~ tr/\t / /s;

		# Do not allow indents at beginning of line
		# groff chokes on that.
		if($newline_last) { 
			$_[0] =~ s/^ //;

			# If the line is all blank, don't do anything.
			if($_[0] eq '') { return; }
			
			$_[0] =~ s/^\./\\\&\./;
	
			# Argh... roff doesn't like ' for some unknown reason 
			$_[0] =~ s/^\'/\\\&\'/;
		}
	}

	$newline_last = 0;

	output $_[0];
});


# When in whitespace-collapsing mode, we disallow consecutive newlines.

sgml('re', sub
{
	if($nocollapse_whitespace || !$newline_last) {
		output "\n";
	}

	$newline_last = 1;
});

sgml('pi', sub {});
sgml('entity',sub { die "Unknown external entity: " . $_[0]->name; });
sgml('start_subdoc',sub { die "Unknown subdoc entity: " . $_[0]->name; });
sgml('end_subdoc',sub{});
sgml('conforming',sub{});

1;

