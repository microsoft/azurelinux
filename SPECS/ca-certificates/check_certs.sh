#!/bin/perl

sub adjust {
   my $newLine = $_[0];
   my @neg = @{$_[1]};
   my @pos = @{$_[2]};
   my $found = 0;
   my @newneg = ();

   foreach my $cline (@neg) {
	if ($cline eq $newLine) {
	   $found = 1;
	} else {
            push(@newneg ,$cline );
	}
   }
   if (! $found ) {
 	push(@pos, $newLine);
   }
   @neg=@newneg;
}

sub removeLine {
   my $newLine = $_[0];
   my @neg = @{$_[1]};
   my $found = 0;
   my @newneg = ();

   foreach my $cline (@neg) {
        if ($found) {
            push(@newneg ,$cline );
	} elsif ($cline eq $newLine) {
	   $found = 1;
	} else {
            push(@newneg ,$cline );
	}
   }
   return @newneg;
}

sub filter {
   my @list = @{$_[0]};
   my $string = $_[1];
   my @filteredList = ();
   foreach my $cline (@list) {
	if ($cline =~ m/$string/) {
            push(@filteredList ,$cline );
	}
   }
   return @filteredList;
}

sub lineExists {
   my $newLine = $_[0];
   my @neg = @{$_[1]};

   foreach my $cline (@neg) {
	if ($cline eq $newLine) {
           return 1;
	}
   }
   return 0;
}

sub lineExists {
   my $newLine = $_[0];
   my @neg = @{$_[1]};

   foreach my $cline (@neg) {
	if ($cline eq $newLine) {
           return 1;
	}
   }
   return 0;
}

sub printeach {
   my @args = @{$_[0]};
   foreach my $arg (@args) {
	chomp $arg;
	print "    $arg\n";
    }
}

open my $handle, "git diff certdata.txt|";
my @diff_lines = <$handle>;
close $handle;
my @adds = ();
my @subs = ();
foreach my $line (@diff_lines) {
    $type = substr $line,0,1;
    $lline = substr $line,1;
    if ($type eq "+") {
          if (lineExists($lline, \@subs)) {
               @subs = removeLine($lline,\@subs);
          } else {
               push(@adds, $lline);
          }
    };
    if ($type eq "-") {
          if (lineExists($lline, \@adds)) {
                @adds = removeLine($lline,\@adds);
          } else {
                push(@subs, $lline);
          }
    };
}

my @tmp = filter(\@subs, "# Certificate");
if (@tmp) {
    print "   Removing: \n";
    printeach(\@tmp);
}
my @tmp = filter(\@adds, "# Certificate");
if (@tmp) {
    print "   Adding: \n";
    printeach(\@tmp);
}
