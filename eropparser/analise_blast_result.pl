#!/usr/bin/perl
if ($ARGV[0] =~ /^(--help)|(-h)$/) {
  print "Usage: analise_blast_result.pl file1.txt file2.txt ...
where files contain output of blast
use FILTER_OUT environment variable to filter out common substrings from ID's
";
  exit(0); 
};

if (defined($ENV{'FILTER_OUT'})) {
  $filter_out=$ENV{'FILTER_OUT'};
  
} else {
  $filter_out="CP009243.1_prot_BCGR_";
};
my $vhash;
my $shash;
while(<>) {
  chomp;
  if(/^# Query:\s+(\S+)\s+(\S+)/) { 
    $target=$1;
    $sequence=$2;
    $shash->{$target}=$sequence;
  };
  if(/^# Database:\s+(\S+)/) {
    $dbname=$1;
  };
  if(/^# (\d+)\s+hits found/) {
    $hits=$1;

  };
### assuming fields   query id, subject id, evalue, bit score

  if(/^([^#]\S*)\s+(\S+)\s+(\S+)\s+(\S+)/) {
    if(defined($evalue)) {
       $vhash->{$dbname}->{$qid}->{$sid}->{evalue}=$evalue;
       $vhash->{$dbname}->{$qid}->{$sid}->{bitscore}=$bitscore;
    };
    $qid=$1;
    $sid=$2;
    $evalue=$3;
    $bitscore=$4;
  };
   if(/^# BLAST/) {
     if($hits>0){
       $vhash->{$dbname}->{$qid}->{$sid}->{evalue}=$evalue;
       $vhash->{$dbname}->{$qid}->{$sid}->{bitscore}=$bitscore;
       $evalue=undef;
     };
   };
};
if(defined($evalue)) {
       $vhash->{$dbname}->{$qid}->{$sid}->{evalue}=$evalue;
       $vhash->{$dbname}->{$qid}->{$sid}->{bitscore}=$bitscore;
};

foreach $dbname (keys(%{$vhash})) {
  print "Results for database $dbname\n";
  print "Query\tSequence\tN\tID(evalue,bitscore)...\n";

  foreach $qid (keys(%{$vhash->{$dbname}})) {
    my @sids=keys(%{$vhash->{$dbname}->{$qid}});
    print $qid."\t".$shash->{$qid}."\t".($#sids+1);
    foreach $sid (@sids) {
      $hs=$vhash->{$dbname}->{$qid}->{$sid};
      $msid=$sid;
      $msid=~s/$filter_out//;
      print "\t".$msid.'('.$hs->{evalue}.','.$hs->{bitscore}.')';
    };
    print "\n";
  };
};
