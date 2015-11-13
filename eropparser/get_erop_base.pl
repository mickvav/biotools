#!/usr/bin/perl
#
#  For each enzyme in stdin, goes to http://rebase.neb.com/cgi-bin/seqget?$enzname
#   and parses result.
#
use LWP::Simple;
use Data::Dumper;


print STDERR "Getting list:\n";
if(! -d "data") { mkdir "data" };
for $empire ("bacterium", "animal", "fungus", "plant", "virus") {
 if (! -d "data/$empire") { mkdir "data/$empire"; };
my $page = get "http://erop.inbi.ras.ru/result1.php?Submit1=Submit+query&EROP_NMB_K=&PEP_NAME_K=&FAM_NAME_K=&ALL_KAR__K=&ALL_KGD__K=$empire&ALL_PHYL_K=&ALL_B_CL_K=&Organism=&SPECIES__K=&ALL_TISS_K=&SEQ_1____K=&AAR_SUM__K1=&AAR_SUM__K2=&M_W______K1=&M_W______K2=&PI_______K1=&PI_______K2=&FUNC_CL__K=&FUNCTION_K=&SEQ_REFA_V=&SEQ_REFT_V=&SEQ_REFJ_V=&YEAR_SEQ_V1=&YEAR_SEQ_V2=&COUNTRY__V=";

print STDERR "Ok, got it.\n";
#print $page;
#my $tree = HTML::TreeBuilder->new_from_content($page);

#print STDERR "Tree generated\n";
#my $tree = HTML::TreeBuilder->new_from_file("metadata.html");
my @matches= $page=~/result2[^"]*"/g;
print "Empire: $empire Matches: $#matches\n";
open(FH,">data/$empire.sequences");
for $match (@matches) {
  $pepname = $match=~s/.*PepName=([^&]+)&.*/$1/r;
  chop $match;
  print STDERR "$empire/$pepname\n";
  my $page1 = get "http://erop.inbi.ras.ru/$match";
  if($page1=~/<b>sequence<\/b><\/font><\/td>\s+<td[^>]*>(?:<font[^>]*>)([^<]*)(?:<\/font[^>]*>)<\/td>/s) {
     print FH "$pepname $1\n";
  };
  open(FD, ">data/$empire/$pepname");
  print FD $page1;
  close(FD);
};
close(FH);
};

