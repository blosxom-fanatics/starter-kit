#!/usr/local/bin/perl

# Blosxom
# Author: Rael Dornfest <rael@oreilly.com>
# Version: 2.0
# Home/Docs/Licensing: http://www.raelity.org/apps/blosxom/

package blosxom;

eval { require './config.cgi'; };
die "Failed to load configuration file.\n$@" if $@;

use vars qw! $version $blog_title $blog_description $blog_language $datadir $url %template $template $depth $num_entries $file_extension $default_flavour $static_or_dynamic $plugin_dir $plugin_state_dir @plugins %plugins $static_dir $static_password @static_flavours $static_entries $path_info $path_info_yr $path_info_mo $path_info_da $path_info_mo_num $flavour $static_or_dynamic %month2num @num2month $interpolate $entries $output $header $show_future_entries %files %indexes %others !;

use strict;
use FileHandle;
use File::Find;
use File::stat;
use Time::localtime;
use CGI qw/:standard :netscape/;

$version = "2.0";

my $fh = new FileHandle;

%month2num = (nil=>'00', Jan=>'01', Feb=>'02', Mar=>'03', Apr=>'04', May=>'05', Jun=>'06', Jul=>'07', Aug=>'08', Sep=>'09', Oct=>'10', Nov=>'11', Dec=>'12');
@num2month = sort { $month2num{$a} <=> $month2num{$b} } keys %month2num;

# Use the stated preferred URL or figure it out automatically
$url ||= url();
$url =~ s/^included:/http:/; # Fix for Server Side Includes (SSI)
$url =~ s!/$!!;

# Drop ending any / from dir settings
$datadir =~ s!/$!!; $plugin_dir =~ s!/$!!; $static_dir =~ s!/$!!;
  
# Fix depth to take into account datadir's path
$depth and $depth += ($datadir =~ tr[/][]) - 1;

# Global variable to be used in head/foot.{flavour} templates
$path_info = '';

$static_or_dynamic = (!$ENV{GATEWAY_INTERFACE} and param('-password') and $static_password and param('-password') eq $static_password) ? 'static' : 'dynamic';
$static_or_dynamic eq 'dynamic' and param(-name=>'-quiet', -value=>1);

# Path Info Magic
# Take a gander at HTTP's PATH_INFO for optional blog name, archive yr/mo/day
my @path_info = split m{/}, path_info() || param('path'); 
shift @path_info;

while ($path_info[0] and $path_info[0] =~ /^[a-zA-Z].*$/ and $path_info[0] !~ /(.*)\.(.*)/) { $path_info .= '/' . shift @path_info; }

# Flavour specified by ?flav={flav} or index.{flav}
$flavour = '';

if ( $path_info[$#path_info] =~ /(.+)\.(.+)$/ ) {
  $flavour = $2;
  $1 ne 'index' and $path_info .= "/$1.$2";
  pop @path_info;
} else {
  $flavour = param('flav') || $default_flavour;
}

# Fix XSS in flavour name (CVE-2008-2236)
$flavour = blosxom_html_escape($flavour);

sub blosxom_html_escape {
  my $string = shift;
  my %escape = (
    '<' => '&lt;',
    '>' => '&gt;',
    '&' => '&amp;',
    '"' => '&quot;',
    "'" => '&apos;'
  );
  my $escape_re = join '|' => keys %escape;
  $string =~ s/($escape_re)/$escape{$1}/g;
  $string;
}

# Strip spurious slashes
$path_info =~ s!(^/*)|(/*$)!!g;

# Date fiddling
($path_info_yr,$path_info_mo,$path_info_da) = @path_info;
$path_info_mo_num = $path_info_mo ? ( $path_info_mo =~ /\d{2}/ ? $path_info_mo : ($month2num{ucfirst(lc $path_info_mo)} || undef) ) : undef;

# Define standard template subroutine, plugin-overridable at Plugins: Template
$template = 
  sub {
    my ($path, $chunk, $flavour) = @_;

    do {
      return join '', <$fh> if $fh->open("< $datadir/$path/$chunk.$flavour");
    } while ($path =~ s/(\/*[^\/]*)$// and $1);

    return join '', ($template{$flavour}{$chunk} || $template{error}{$chunk} || '');
  };
# Bring in the templates
%template = ();
while (<DATA>) {
  last if /^(__END__)?$/;
  my($ct, $comp, $txt) = /^(\S+)\s(\S+)\s(.*)$/;
  $txt =~ s/\\n/\n/mg;
  $template{$ct}{$comp} = $txt;
}

# Plugins: Start
if ( $plugin_dir and opendir PLUGINS, $plugin_dir ) {
  foreach my $plugin ( grep { /^\w+$/ && -f "$plugin_dir/$_"  } sort readdir(PLUGINS) ) {
    my($plugin_name, $off) = $plugin =~ /^\d*(\w+?)(_?)$/;
    my $on_off = $off eq '_' ? -1 : 1;
    require "$plugin_dir/$plugin";
    $plugin_name->start() and ( $plugins{$plugin_name} = $on_off ) and push @plugins, $plugin_name;
  }
  closedir PLUGINS;
}

# Plugins: Template
# Allow for the first encountered plugin::template subroutine to override the
# default built-in template subroutine
my $tmp; foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('template') and defined($tmp = $plugin->template()) and $template = $tmp and last; }

# Provide backward compatibility for Blosxom < 2.0rc1 plug-ins
sub load_template {
  return &$template(@_);
}

# Define default find subroutine
$entries =
  sub {
    my(%files, %indexes, %others);
    find(
      sub {
        my $d; 
        my $curr_depth = $File::Find::dir =~ tr[/][]; 
        return if $depth and $curr_depth > $depth; 
     
        if ( 
          # a match
          $File::Find::name =~ m!^$datadir/(?:(.*)/)?(.+)\.$file_extension$!
          # not an index, .file, and is readable
          and $2 ne 'index' and $2 !~ /^\./ and (-r $File::Find::name)
        ) {

            # to show or not to show future entries
            ( 
              $show_future_entries
              or stat($File::Find::name)->mtime < time 
            )

              # add the file and its associated mtime to the list of files
              and $files{$File::Find::name} = stat($File::Find::name)->mtime

                # static rendering bits
                and (
                  param('-all') 
                  or !-f "$static_dir/$1/index." . $static_flavours[0]
                  or stat("$static_dir/$1/index." . $static_flavours[0])->mtime < stat($File::Find::name)->mtime
                )
                  and $indexes{$1} = 1
                    and $d = join('/', (nice_date($files{$File::Find::name}))[5,2,3])
  
                      and $indexes{$d} = $d
                        and $static_entries and $indexes{ ($1 ? "$1/" : '') . "$2.$file_extension" } = 1

            } 
            else {
              !-d $File::Find::name and -r $File::Find::name and $others{$File::Find::name} = stat($File::Find::name)->mtime
            }
      }, $datadir
    );

    return (\%files, \%indexes, \%others);
  };

# Plugins: Entries
# Allow for the first encountered plugin::entries subroutine to override the
# default built-in entries subroutine
my $tmp; foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('entries') and defined($tmp = $plugin->entries()) and $entries = $tmp and last; }

my ($files, $indexes, $others) = &$entries();
%files = %$files; %indexes = %$indexes; %others = ref $others ? %$others : ();

# Plugins: Filter
foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('filter') and $entries = $plugin->filter(\%files, \%others) }

# Static
if (!$ENV{GATEWAY_INTERFACE} and param('-password') and $static_password and param('-password') eq $static_password) {

  param('-quiet') or print "Blosxom is generating static index pages...\n";

  # Home Page and Directory Indexes
  my %done;
  foreach my $path ( sort keys %indexes) {
    my $p = '';
    foreach ( ('', split /\//, $path) ) {
      $p .= "/$_";
      $p =~ s!^/!!;
      $path_info = $p;
      $done{$p}++ and next;
      (-d "$static_dir/$p" or $p =~ /\.$file_extension$/) or mkdir "$static_dir/$p", 0755;
      foreach $flavour ( @static_flavours ) {
        my $content_type = (&$template($p,'content_type',$flavour));
        $content_type =~ s!\n.*!!s;
        my $fn = $p =~ m!^(.+)\.$file_extension$! ? $1 : "$p/index";
        param('-quiet') or print "$fn.$flavour\n";
        my $fh_w = new FileHandle "> $static_dir/$fn.$flavour" or die "Couldn't open $static_dir/$p for writing: $!";  
        $output = '';
        print $fh_w 
          $indexes{$path} == 1
            ? &generate('static', $p, '', $flavour, $content_type)
            : &generate('static', '', $p, $flavour, $content_type);
        $fh_w->close;
      }
    }
  }
}

# Dynamic
else {
  my $content_type = (&$template($path_info,'content_type',$flavour));
  $content_type =~ s!\n.*!!s;

  $header = {-type=>$content_type};

  print generate('dynamic', $path_info, "$path_info_yr/$path_info_mo_num/$path_info_da", $flavour, $content_type);
}

# Plugins: End
foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('end') and $entries = $plugin->end() }

# Generate 
sub generate {
  my($static_or_dynamic, $currentdir, $date, $flavour, $content_type) = @_;

  my %f = %files;

  # Plugins: Skip
  # Allow plugins to decide if we can cut short story generation
  my $skip; foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('skip') and defined($tmp = $plugin->skip()) and $skip = $tmp and last; }
  
  # Define default interpolation subroutine
  $interpolate = 
    sub {
      package blosxom;
      my $template = shift;
      $template =~ 
        s/(\$\w+(?:::)?\w*)/"defined $1 ? $1 : ''"/gee;
      return $template;
    };  

  unless (defined($skip) and $skip) {

    # Plugins: Interpolate
    # Allow for the first encountered plugin::interpolate subroutine to 
    # override the default built-in interpolate subroutine
    my $tmp; foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('interpolate') and defined($tmp = $plugin->interpolate()) and $interpolate = $tmp and last; }
        
    # Head
    my $head = (&$template($currentdir,'head',$flavour));
  
    # Plugins: Head
    foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('head') and $entries = $plugin->head($currentdir, \$head) }
  
    $head = &$interpolate($head);
  
    $output .= $head;
    
    # Stories
    my $curdate = '';
    my $ne = $num_entries;

    if ( $currentdir =~ /(.*?)([^\/]+)\.(.+)$/ and $2 ne 'index' ) {
      $currentdir = "$1$2.$file_extension";
      $files{"$datadir/$1$2.$file_extension"} and %f = ( "$datadir/$1$2.$file_extension" => $files{"$datadir/$1$2.$file_extension"} );
    } 
    else { 
      $currentdir =~ s!/index\..+$!!;
    }

    # Define a default sort subroutine
    my $sort = sub {
      my($files_ref) = @_;
      return sort { $files_ref->{$b} <=> $files_ref->{$a} } keys %$files_ref;
    };
  
    # Plugins: Sort
    # Allow for the first encountered plugin::sort subroutine to override the
    # default built-in sort subroutine
    my $tmp; foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('sort') and defined($tmp = $plugin->sort()) and $sort = $tmp and last; }
  
    foreach my $path_file ( &$sort(\%f, \%others) ) {
      last if $ne <= 0 && $date !~ /\d/;
      use vars qw/ $path $fn /;
      ($path,$fn) = $path_file =~ m!^$datadir/(?:(.*)/)?(.*)\.$file_extension!;
  
      # Only stories in the right hierarchy
      $path =~ /^$currentdir/ or $path_file eq "$datadir/$currentdir" or next;
  
      # Prepend a slash for use in templates only if a path exists
      $path &&= "/$path";

      # Date fiddling for by-{year,month,day} archive views
      use vars qw/ $dw $mo $mo_num $da $ti $yr $hr $min $hr12 $ampm /;
      ($dw,$mo,$mo_num,$da,$ti,$yr) = nice_date($files{"$path_file"});
      ($hr,$min) = split /:/, $ti;
      ($hr12, $ampm) = $hr >= 12 ? ($hr - 12,'pm') : ($hr, 'am'); 
      $hr12 =~ s/^0//; $hr12 == 0 and $hr12 = 12;
  
      # Only stories from the right date
      my($path_info_yr,$path_info_mo_num, $path_info_da) = split /\//, $date;
      next if $path_info_yr && $yr != $path_info_yr; last if $path_info_yr && $yr < $path_info_yr; 
      next if $path_info_mo_num && $mo ne $num2month[$path_info_mo_num];
      next if $path_info_da && $da != $path_info_da; last if $path_info_da && $da < $path_info_da; 
  
      # Date 
      my $date = (&$template($path,'date',$flavour));
      
      # Plugins: Date
      foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('date') and $entries = $plugin->date($currentdir, \$date, $files{$path_file}, $dw,$mo,$mo_num,$da,$ti,$yr) }
  
      $date = &$interpolate($date);
  
      $curdate ne $date and $curdate = $date and $output .= $date;
      
      use vars qw/ $title $body $raw /;
      if (-f "$path_file" && $fh->open("< $path_file")) {
        chomp($title = <$fh>);
        chomp($body = join '', <$fh>);
        $fh->close;
        $raw = "$title\n$body";
      }
      my $story = (&$template($path,'story',$flavour));
  
      # Plugins: Story
      foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('story') and $entries = $plugin->story($path, $fn, \$story, \$title, \$body) }
      
      if ($content_type =~ m{\Wxml$}) {
        # Escape <, >, and &, and to produce valid RSS
        my %escape = ('<'=>'&lt;', '>'=>'&gt;', '&'=>'&amp;', '"'=>'&quot;');  
        my $escape_re  = join '|' => keys %escape;
        $title =~ s/($escape_re)/$escape{$1}/g;
        $body =~ s/($escape_re)/$escape{$1}/g;
      }
  
      $story = &$interpolate($story);
    
      $output .= $story;
      $fh->close;
  
      $ne--;
    }
  
    # Foot
    my $foot = (&$template($currentdir,'foot',$flavour));
  
    # Plugins: Foot
    foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('foot') and $entries = $plugin->foot($currentdir, \$foot) }
  
    $foot = &$interpolate($foot);
    $output .= $foot;

    # Plugins: Last
    foreach my $plugin ( @plugins ) { $plugins{$plugin} > 0 and $plugin->can('last') and $entries = $plugin->last() }

  } # End skip

  # Finally, add the header, if any and running dynamically
  $static_or_dynamic eq 'dynamic' and $header and $output = header($header) . $output;
  
  $output;
}


sub nice_date {
  my($unixtime) = @_;
  
  my $c_time = ctime($unixtime);
  my($dw,$mo,$da,$ti,$yr) = ( $c_time =~ /(\w{3}) +(\w{3}) +(\d{1,2}) +(\d{2}:\d{2}):\d{2} +(\d{4})$/ );
  $da = sprintf("%02d", $da);
  my $mo_num = $month2num{$mo};
  
  return ($dw,$mo,$mo_num,$da,$ti,$yr);
}


# Default HTML and RSS template bits
__DATA__
html content_type text/html
html head <html>\n<head>\n<title>$blog_title</title>\n<link rel="alternate" type="application/rss+xml" title="RSS" href="$url/index.rss">\n</head>\n<body>\n<h1>$blog_title</h1>\n<p>$blog_description</p>\n
html story <h3><a name="$fn">$title</a></h3>\n$body\n<p>Posted at: $ti | Path: <a href="$url$path">$path</a> | <a href="$url$path/$fn.$default_flavour">Permanent link to this entry</a></p>\n
html date <h2>$yr/$mo_num/$da</h2>\n
html foot <address><a href="http://www.blosxom.com/"><img src="http://www.blosxom.com/images/pb_blosxom.gif" border="0"></a></address>\n</body>\n</html>\n
rss content_type text/xml
rss head <?xml version="1.0"?>\n<!-- name="generator" content="blosxom/$version" -->\n<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">\n<rss version="0.91">\n<channel>\n<title>$blog_title</title>\n<link>$url</link>\n<description>$blog_description</description>\n<language>$blog_language</language>\n
rss story <item>\n<title>$title</title>\n<link>$url$path$fn.$default_flavour</link>\n<description>$body</description>\n</item>\n
rss date \n
rss foot </channel>\n</rss>\n
error content_type text/html
error head <html>\n<head>\n<title>$blog_title</title>\n</head>\n<body>\n<h1>$blog_title</h1>\n<p>$blog_description</p>\n<p><em>Error: I'm afraid this is the first I've heard of a "$flavour" flavoured Blosxom. Try dropping the "/+$flavour" bit from the end of the URL.</em></p>\n
error story <h3><a name="$fn">$title</a></h3>\n$body\n<p>Posted at: $ti | Path: <a href="$url$path">$path</a> | <a href="$url$path/$fn.$default_flavour">Permanent link to this entry</a></p>\n
error date <h2>$yr/$mo_num/$da</h2>\n
error foot <address><a href="http://www.blosxom.com/"><img src="http://www.blosxom.com/images/pb_blosxom.gif" border="0"></a></address>\n</body>\n</html>\n
__END__
