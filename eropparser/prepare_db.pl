#!/usr/bin/perl

foreach $file (glob("data/*.sequences")) {
  print "Working with $file\n";
  open(FD, "<$file");
  open(FO, ">$file.fasta");
  while(<FD>) {
    chomp;
    if(/^(\S+)\s+(\S.*)/){
    ($name,$orig_sequence) = ($1,$2) ;
    $sequence= $orig_sequence;
    $sequence=~s/\s*[a-z+ -]*([A-Z]+)[a-z+-]*\s*/$1/;
    if($sequence=~/-/) { 
      print "Buggy sequence: $sequence\n";
      print "Origin: $orig_sequence Name:$name\n";
    }
    else {
      print FO ">$name $orig_sequence\n$sequence\n";
    };
    } else {
      print "Buggy line: $_\n";
    };
  };
  close(FO);
  close(FD);
  $empire= $file;
  $empire=~s/(.*)\.sequences/$1/;

  system("formatdb -t $empire -i $file.fasta -p T -o T -n $empire ");
};

