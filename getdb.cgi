#!/usr/bin/perl
use warnings;
use strict;
use Data::Dumper;
use File::Copy;
use DBI;
use JSON::XS;

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
#print "Opened database successfully\n";

#my $stmt = qq(SELECT * from stock;);
my $stmt = qq(SELECT column_name FROM information_schema.columns WHERE table_name = 'stock';);

my $sth = $dbh->prepare( $stmt );
my $rv = $sth->execute() or die $DBI::errstr;
if($rv < 0) {
   print $DBI::errstr;
}
#print "\{\n";

my $data;

while(my @row = $sth->fetchrow_array()) {
    $data->{$row[0]} = "";
#    print $row[0] . "\",\n";
}

#my $stmt = qq(SELECT  FROM information_schema.columns WHERE table_name = 'stock';);#

#my $sth = $dbh->prepare( $stmt );
#my $rv = $sth->execute() or die $DBI::errstr;


print encode_json($data);
#print "\}\n";
#print "Operation done successfully\n";
$dbh->disconnect();
