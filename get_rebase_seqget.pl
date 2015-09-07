#!/usr/bin/perl
#
#  For each enzyme in stdin, goes to http://rebase.neb.com/cgi-bin/seqget?$enzname
#   and parses result.
#
use LWP::Simple;
use Data::Dumper;
use HTML::TreeBuilder;


while(<>) {
chomp;
$seq=$_;
print STDERR "Getting list $seq:\n";

my $page = get "http://rebase.neb.com/cgi-bin/seqget?$seq";

print $page;
print STDERR "Ok, got it.\n";
#print $page;
my $tree = HTML::TreeBuilder->new_from_content($page);

print STDERR "Tree generated\n";
#my $tree = HTML::TreeBuilder->new_from_file("metadata.html");
my $gbnref = $tree->look_down('_tag','b', sub { return $_[0]->as_text=~/^Genbank Notes:*/; });
if(defined( $gbnref )) {
my $gbntable = $gbnref->parent->parent->parent->parent;
my $dataline = $gbntable->content->[1]->content->[0]->content->[0]->as_text;
#print $dataline;

my $ststop = $tree->look_down('_tag','b', sub { return $_[0]->as_text=~/^BP start\/stop*/; });
my $gbntable = $ststop->parent->parent->parent->parent;

my $datarow = $gbntable->content->[2];
#print Dumper($gbntable);
#exit(0);
my @list=();
for($i=0;$i<9;$i++) {
  if(defined($datarow->content->[$i])) {
     $list[$i]=$datarow->content->[$i]->as_text;
  } else {
     $list[$i]="";
  };
};
print  $seq."\t".$dataline."\t".join("\t",@list)."\n";
} else {
print $seq."\t"."not found"."\n";
}
};


sub parse_td_table($) {
   $i=0;
   my $result;
   $result->{'nrows'}=0;
   $result->{'ncols'}=0;
   if(defined($_[0])){
   my @rows = $_[0]->content_list;
   foreach my $row (@rows) {
       if($row->tag eq 'tr'){ 
          my @cols = $row->content_list;
          $j=0;
          foreach my $col (@cols) {
            if($col->tag eq 'td') {
               $result->{'data'}->{$i}->{$j}=$col->as_text;
               $j++;
            };
          };
          if($j>$result->{'ncols'}) { $result->{'ncols'}=$j;};
          $i++;
       };
   };
   if($i>$result->{'nrows'}) { $result->{'nrows'}=$i;};
   };
   return $result;
};

sub parse_orfs_table($) {
   my @rows = $_[0]->content_list;
   
   $i=0;
   my $result;
   $result->{'nrows'}=0;
   $result->{'ncols'}=0;
   $type="";
   $section="";
   foreach my $row (@rows) {
       if($row->tag eq 'tr'){ 
          my @cols = $row->content_list;
          $j=0;
          foreach my $col (@cols) {
            if(($col->tag eq 'th') and ($col->attr('class') eq "repo_ttype")) {
               $type=$col->as_text;
            };
            if(($col->tag eq 'td') and ($col->attr('class') eq "repo_orfs_td") and ($col->attr('colspan') eq '5')) {
               
               if($possiblesections{$col->as_text} == 1) {
                  $section=$col->as_text;
               };
            } elsif ($col->tag eq 'td') {
               $result->{'data'}->{$i}->{$j}=$col->as_text;
               $result->{'data'}->{$i}->{"type"}=$type;
               $result->{'data'}->{$i}->{"section"}=$section;
               $j++;
            };

            
          };
          if($j>$result->{'ncols'}) { $result->{'ncols'}=$j;};
          $i++;
       };
   };
   if($i>$result->{'nrows'}) { $result->{'nrows'}=$i;};
   return $result;
};




foreach $a (@as) {
	$orgname = $a->parent->as_text;
	$gn=$a->attr('name');
#	print $orgname."----".$gn."\n";
	$gi=$gn;
	$gi=~s/gn//;

        print STDERR "Geting data for $gi\n";

	my $spage = get "http://tools.neb.com/~vincze/genomes/summary.php?genome_id=".$gi;

        print STDERR "Ok, got it.\nBuilding tree\n";
        my $stree = HTML::TreeBuilder->new_from_content($spage);
        print STDERR "Done. Analising\n";
        $rebase_ref_no_tag =  $stree->look_down('_tag','p', sub {return $_[0]->as_text =~/REBASE ref #/;});
        $rebase_ref_no = $rebase_ref_no_tag->as_text;
        # $rebase_ref_no =~s/REBASE ref #\s*(\d+)\s*/\1/;
        
        $org_num_tag =  $stree->look_down('_tag','p', sub {return $_[0]->as_text =~/Org_num:/;});
        $org_num = $org_num_tag->as_text;
        
        $all_begin_tag = $stree->look_down('_tag','p', sub {return $_[0]->as_text =~/All begin/;});
        $all_begin =  $all_begin_tag->as_text;
  
        $all_begin =~s/\s*All begin\s*//;
        @all_begin_list = split(/,/,$all_begin);
        

        $repo_top_tag = $stree->look_down('_tag','table', sub {return $_[0]->attr('class')=~/repo_top/;});
        
        $repo_top_table = parse_td_table($repo_top_tag);
        if($repo_top_table->{'nrows'}==0) {
# 
#       No plasmids, no top table. Grr.
#
            $genebank_no_tag =  $stree->look_down('_tag','p', sub {return $_[0]->as_text =~/GenBank #:/;});
            if(defined($genebank_no_tag)) {
              $genebank_no = $genebank_no_tag->as_text;
              $genebank_no=~s/GenBank #:\s*//;              
            } else {
               $genebank_no="";
            };
        } else {
            $genebank_no="";
        };
       our %possiblesections=();
       our %sectionnumber=();
        for($i=0;$i<$repo_top_table->{'nrows'};$i++) {
          $sectname=$repo_top_table->{'data'}->{$i}->{'0'};
          $sectname=~s/:$//;
          $possiblesections{$sectname}=1;
          $sectionnumber{$sectname}=$i;
        }; 
        $orfs_table_tag =  $stree->look_down('_tag','table', sub {return $_[0]->attr('class')=~/repo_orfs/;});

        $orfs_table = parse_orfs_table($orfs_table_tag);
 
        for($i=0;$i<$orfs_table->{"nrows"};$i++) {
            $orf=$orfs_table->{"data"}->{$i}->{"0"};
            if($orf ne "") {
            $name=$orfs_table->{"data"}->{$i}->{"4"};
             
            print $name."\t";
            
            if($name=~/^(\w*)\.(.*\d)(\D+)$/) {
            $prefix=$1;
            $sysname=$2; 
            $suffix=$3;
            } elsif ($name=~/^(.*\d)(\D+)$/) {
            $prefix=""; 
            $sysname=$1;
            $suffix=$2;
            } else {
               $prefix=""; 
               $sysname="";
               $suffix="";         
            };
            $mostsimilar=$orfs_table->{"data"}->{$i}->{"2"};
            print $mostsimilar."\t";
            print $sysname."\t".$prefix."\t".$suffix."\t";
            $section=$orfs_table->{"data"}->{$i}->{"section"};
            if($#all_begin_list==0) {
              print $all_begin.$orf."\t";
            } else {
              print $all_begin_list[$sectionnumber{$section}-1].$orf."\t";
            };
            print $orfs_table->{"data"}->{$i}->{"type"}."\t";
            if(defined($sectionnumber{$section})) {
               print $repo_top_table->{"data"}->{$sectionnumber{$section}}->{"2"}."\t";
            } else {
               print $genebank_no."\t";
            };
            print $section."\t";
       #     print  $sectionnumber{$section}."\t";
            print $gi."\t";
            print $org_num."\n";
            };
        };       
#        print Dumper($orfs_table);
        
        $stree->delete;
};

$tree->delete;
