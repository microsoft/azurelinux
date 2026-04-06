#!/bin/perl
use warnings;
use strict;

use Test::More tests => 1;
use Storable;

use Exception::Base
    'MyException', => {
        message => 'Validation error',
        has     => [ qw(class errors) ],
        string_attributes => [ 'message', 'class', 'errors' ]
    };
eval {
    MyException->throw(
            class  => __PACKAGE__,
            errors => ["error 1", "error 2", "error 3"]
        );
};

my $exception = $@;
my $saved_errors = Storable::dclone($exception->errors());
$exception->to_string();
is_deeply($exception->errors(), $saved_errors, "to_string() does not modify errors() value");
