#!/usr/local/bin/perl

# This script based on:
# http://www.hyuki.com/netserv/google.html

use strict;

use CGI qw(:standard);

my $q   = &uri_escape(param('q'));
my $key = &uri_escape(param('key'));

print "Location: http://www.google.com/search?q=$q+$key&ie=UTF-8\n\n";

exit;

sub uri_escape {
  my $str = shift;

  $str =~ s/([^\w ])/sprintf("%%%02X", ord($1))/eg;
  $str =~ tr/ /+/;

  return $str;
}
