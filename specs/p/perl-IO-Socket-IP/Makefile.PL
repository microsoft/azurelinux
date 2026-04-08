use strict;
use warnings;

use ExtUtils::MakeMaker;

WriteMakefile(
    'NAME' => 'IO::Socket::IP',
    'VERSION_FROM' => 'lib/IO/Socket/IP.pm',
    'ABSTRACT_FROM' => 'lib/IO/Socket/IP.pm',
    'PREREQ_PM' => {
         'base' => '0',
         'Carp' => '0',
         'constant' => '0',
         'Errno' => '0',
         'IO::Socket' => 0,
         'POSIX' => '0',
         'Socket' => '1.97',
         'strict' => '0',
         'warnings' => '0',
    },
    'TEST_REQUIRES' => {
	 'perl' => '5.014',
         'IO::Socket::INET' => '0',
         'Test::More' => '0.88',
    },
    'INSTALLDIRS' => 'site',
);
