#!/usr/bin/perl
use warnings;
use strict;
use Data::Dumper;
use File::Copy;
use DBI;
use JSON::XS;

my ($id) = split('-',$ENV{'QUERY_STRING'});

  print "Cache-Control: no-cache, must-revalidate, max-age=1\r\n";
  print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\r\n";
#  print "Content-type: text/html\r\n\r\n";
  print "Content-type: text/html\r\n\r\n";

my $driver   = "Pg"; 
my $database = "stock";
my $dsn = "DBI:$driver:dbname = $database;host = 127.0.0.1;port = 5432";
my $userid = "postgres";
my $password = "\$postgres";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 })
   or die $DBI::errstr;




#print "$partnum  $amount  $place  $type  $value  $package  $price\n";
my $stmt = qq(DELETE FROM stock WHERE id=$id;);

my $sth = $dbh->prepare( $stmt );
my $rv = $sth->execute() or die print "$DBI::errstr\n";

if($rv < 0) {
   print $DBI::errstr;
}
print "deleted ID $id!\n";

$dbh->disconnect();
