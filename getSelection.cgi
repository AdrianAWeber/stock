#!/usr/bin/perl
use warnings;
use strict;
use Data::Dumper;
use File::Copy;
use DBI;
use JSON::XS;

## getSelection.cgi?value-R
## getSelection.cgi?types

my @args = split('-',$ENV{'QUERY_STRING'});

  print "Cache-Control: no-cache, must-revalidate, max-age=1\r\n";
  print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\r\n";
#  print "Content-type: text/html\r\n\r\n";
  print "Content-type: application/json\r\n\r\n";

my $driver   = "Pg"; 
my $database = "stock";
my $dsn = "DBI:$driver:dbname = $database;host = 127.0.0.1;port = 5432";
my $userid = "postgres";
my $password = "\$postgres";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 })
   or die $DBI::errstr;

my $Sel = "";
my $type = "";
$Sel = $args[0];
$type = $args[1];
my $stmt;
if ($Sel eq "type") {
  $stmt = qq(SELECT DISTINCT type FROM typeValue;);
} elsif ($Sel eq "value" && $type ne ""){
  $stmt = qq(SELECT * FROM typeValue WHERE type='$type';);
}

my $sth = $dbh->prepare( $stmt );
my $rv = $sth->execute() or die $DBI::errstr;
if($rv < 0) {
   print $DBI::errstr;
}

my $data;

while(my @row = $sth->fetchrow_array()) {
  if ($Sel eq "type") {
    $data->{$row[0]} = "$row[0]";
  } elsif ($Sel eq "value" && $type ne ""){
     $data->{$row[2]} = $row[1];
  }
}

#my $stmt = qq(SELECT  FROM information_schema.columns WHERE table_name = 'stock';);#

#my $sth = $dbh->prepare( $stmt );
#my $rv = $sth->execute() or die $DBI::errstr;


print encode_json($data);
#print "\}\n";
#print "Operation done successfully\n";
$dbh->disconnect();
