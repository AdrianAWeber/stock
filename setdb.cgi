#!/usr/bin/perl
use warnings;
use strict;
use Data::Dumper;
use File::Copy;
use DBI;
use JSON::XS;

my ($partnum,$amount,$place,$type,$value,$package,$price,$add,$new) = split('-',$ENV{'QUERY_STRING'});

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

$place = "" if !(defined $place);
$type = "" if !(defined $type);
$value = "" if !(defined $value);
$package = "" if !(defined $package);
$price = 0 if ($price == '');
$add = 0 if ($add == '');
$new = 0 if ($new == '');
#print $package."b\n";


#print "$partnum  $amount  $place  $type  $value  $package  $price\n";

#partnum='$partnum' AND
#print $place."\n";
my $stmt = qq(SELECT * FROM stock WHERE partnum='$partnum' AND place = '$place' AND value='$value' AND package='$package';);
#my $stmt = qq(INSERT INTO stock VALUES (DEFAULT,'$partnum',$amount,$place,'$type','$value','$package',$price););

my $sth = $dbh->prepare( $stmt );
my $rv = $sth->execute() or die print "$DBI::errstr\n";

if($rv < 0) {
   print $DBI::errstr;
}

my $oldamount=0;
my $add2id = -1;

while(my @row = $sth->fetchrow_array()) {
  print "ID: ".$row[0]."<br>";  
  $add2id = $row[0];
  $oldamount = $row[2];
}

if ($add > 0) {
  my $newamount = $oldamount + $amount ;
  print $newamount."<br>\n";
  $stmt = qq(UPDATE stock SET amount='$newamount' WHERE id = '$add2id';);
  $sth = $dbh->prepare( $stmt );
  $rv = $sth->execute() or die print "$DBI::errstr\n";

}

if ($new > 0) {
  $stmt = qq(INSERT INTO stock VALUES (DEFAULT,'$partnum',$amount,$place,'$type','$value','$package',$price););
  $sth = $dbh->prepare( $stmt );
  $rv = $sth->execute() or die print "$DBI::errstr\n";
}


$dbh->disconnect();
