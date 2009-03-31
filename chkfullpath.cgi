#!/usr/local/bin/perl

use strict;

use CGI qw(:standard);

my $cgi_path = $ENV{'SCRIPT_FILENAME'};
$cgi_path =~ s!\\!/!g;
$cgi_path =~ s!/[^/]*?$!!;

print header(-type => "text/html");
print <<"_HTML_";
<html>
  <head>
  <title>chkfullpath.cgi</title>
  </head>
  <body>
    <h1>chkfullpath.cgi</h1>
    <p>The full-path of this directory is:</p>
    <pre>$cgi_path</pre>
    <p>Set this string to value of <code>\$basedir</code> in config.cgi.</p>
  </body>
</html>
_HTML_

exit;
