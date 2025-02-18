#!/usr/bin/perl
use strict;
use warnings;

use Carp;
use Encode;

# small script for Blowfish encryption and decryption

# The key for the blowfish encoding/decoding below
my $privateString = '123456789012345678901234567890123456789012';

my $teststring = "Testtext";

my $encoded = encodeBlowfish($teststring);
my $decoded = decodeBlowfish($encoded);
print "original: $teststring\n";
print "encoded:  $encoded\n";
print "decoded:  $decoded\n";

#
# Encode a string using blowfish with a private key.
#
sub encodeBlowfish
{
   my($string) = @_;

   my $cipher = undef;
   eval
   {
      require Crypt::CBC;
      my $key = pack('H*', $privateString);

      my $params = { 'key' => $key, 'cipher' => 'Blowfish', 'header' => 'randomiv'};

      $cipher = new Crypt::CBC($params);
   };
   if ($@)
   {
      warn("*********** $@\n");
   }

   my $enc = undef;
   if (defined($cipher))
   {
      if (Encode::is_utf8($string))
      {
         #
         # workaround Blowfish problem with utf8-flag
         #
         Encode::_utf8_off($string);
      }

      $enc = $cipher->encrypt_hex($string);
   }

   return $enc;
}


#
# Decode a string using blowfish with a private key.
#
sub decodeBlowfish
{
   my($string) = @_;

   return undef if (!defined($string)); # filter empty strings for Blowfish
   return '' if ($string eq '');

   my $cipher = undef;
   eval
   {
      require Crypt::CBC;
      my $key = pack('H*', $privateString);

      my $params = { 'key' => $key, 'cipher' => 'Blowfish', 'header' => 'randomiv'};

      $cipher = new Crypt::CBC($params);
   };

   my $enc = undef;
   if (defined($cipher))
   {
      $enc = $cipher->decrypt_hex($string);
   }

   return $enc;
}
