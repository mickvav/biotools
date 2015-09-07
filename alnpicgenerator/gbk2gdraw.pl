#!/usr/bin/perl

open (FD,"<".$ARGV[0]) or die "Can't open ".$ARGV[0]."\n";
$shift=$ARGV[1];
$percm=$ARGV[2];
print "nucleospercm=$percm\n";
while(<FD>) {
   if(/^     (\w*)\s+(complement\(|)(\d+)\.\.(\d+)(\)|)/) {
        $operator=$1;
        if($2 eq 'complement(') {
          $direction='r';
        } else {
          $direction='f';
        };
        $start=$3;
        $end=$4;
   }
   if(/^                     \/organism="(.*)"/) {
          if($operator eq 'source') {
            print "kind \"$1\" 3.0\n";
          };
        };

   if(/^                     \/locus_tag="(.*)"/) {
        if($operator eq 'gene') {
          print "start=".($start-$shift)."\n";
          if ($direction eq 'r') { print 'r' };
          print "gene \"$1\" ".($end-$start)." white\n";
        };
        
   };
};
