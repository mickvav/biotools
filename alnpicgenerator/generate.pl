#!/usr/bin/perl

#
# Generates tex from text input
#

#print '\begin{pspicture}';
print '\documentclass{article}

\usepackage[usenames,dvipsnames]{pstricks}
\usepackage{epsfig}
\usepackage{pst-grad}
\usepackage{pst-plot}
\usepackage{pst-node} 
\begin{document}
\pagestyle{empty}
';


$RE_Real='\d+\.?\d*';
$RE_gene='[^"]*';
$RE_kind='[^"]*';
$RE_skip='[^"]*';
$kind_y=0;
$gene_x=0;
$params{'genearrowstyle'}="linewidth=0.04,fillstyle=solid";
$params{'skipstyle'}="linewidth=0.04,fillstyle=solid,fillcolor=white";
$params{'connlinestyle'}="linewidth=0.04";
$params{'arrowheight'}="0.4";
$params{'arrowtipx'}="0.1";
$params{'geneskipx'}="0.1";
$params{'geneskipy'}="0.1";
$params{'kindskipx'}="0.3";
$params{'angle'}="45";
$params{'kindtype'}='emph';
$params{'genetype'}='textsf';
$params{'linkstyle'}='linewidth=0,linecolor=lightgray,fillstyle=solid,fillcolor=lightgray';
$params{'linkskipy'}='0.1';
$params{'linkshiftx'}='0.4';
$params{'skipspacex'}="0.2";
$params{'skipspacey'}="0.1";
$params{'skipsizey'}="0.6";
$params{'skiptype'}='textsf';
$params{'nucleospercm'}='1000';
$output='';

$colordefined{'white'}=1;
$colordefined{'black'}=1;
$colordefined{'gray'}=1;
$colordefined{'lightgray'}=1;
$colordefined{'darkgray'}=1;

while(<>) {
  chomp;
  s/_/\\_/g;
  if(/^defcolor (\w+) (\d+) (\d+) (\d+)$/) {
     $output .= "\\definecolor{$1}{rgb}{0.$2,0.$3,0.$4}\n";
     $colordefined{$1}=1;
  };
  if(/^kind "($RE_kind)" ($RE_Real)/) {
     $kind_y-=$2;
     $kind_name=$1;
     $gene_x=0;
     $output .= '\rput[br]('.$gene_x.','.$kind_y.'){\\'.$params{'kindtype'}.'{'.$kind_name."}}\n";
     $gene_x+=$params{'kindskipx'};
     $last_x=$gene_x;
  };
  if(/^gene "($RE_gene)" ($RE_Real) (\w+)/) {
     if($colordefined{$3}) {
       $width=$2/$params{'nucleospercm'};
       $x1=$gene_x;
       $x2=$gene_x+$width-$params{'arrowtipx'}*$width;
       $x3=$gene_x+$width;
       $y1=$kind_y;
       $y2=$kind_y+$params{'arrowheight'};
       $y3=$kind_y+$params{'arrowheight'}/2;
       $y4=$kind_y+$params{'arrowheight'}+$params{'geneskipy'};

       $genecoords{$1}{'x1'}=$x1;
       $genecoords{$1}{'x2'}=$x2;
       $genecoords{$1}{'x3'}=$x3;
       $genecoords{$1}{'y1'}=$y1;
       $genecoords{$1}{'y2'}=$y2;
       $genecoords{$1}{'y3'}=$y3;
       $output.="\\psline[".$params{'connlinestyle'}."]($last_x,$y3)($x1,$y3)\n";
       $last_x=$x3;
       $output.= "\\pspolygon[".$params{'genearrowstyle'}.",fillcolor=$3]($x1,$y1)($x1,$y2)($x2,$y2)($x3,$y3)($x2,$y1)\n";
       $output.= "\\rput[br]{-".$params{'angle'}."}($x2,$y2){\\".$params{'genetype'}."{$1}}\n";
       $gene_x+=$width+$params{'geneskipx'};
     } else {
       print STDERR "Color $3 not defined for $1 of $kind_name, $1 skiped!\n";
     };
  };
  if(/^rgene "($RE_gene)" ($RE_Real) (\w+)/) {
     if($colordefined{$3}) {
       $width=$2/$params{'nucleospercm'};
       $x1=$gene_x+$width;
       $x2=$gene_x+$params{'arrowtipx'}*$width;
       $x3=$gene_x;
       $x4=$gene_x+$width-$params{'arrowtipx'}*$width;
       $y1=$kind_y;
       $y2=$kind_y+$params{'arrowheight'};
       $y3=$kind_y+$params{'arrowheight'}/2;
       $y4=$kind_y+$params{'arrowheight'}+$params{'geneskipy'};
       $genecoords{$1}{'x1'}=$x1;
       $genecoords{$1}{'x2'}=$x2;
       $genecoords{$1}{'x3'}=$x3;
       $genecoords{$1}{'y1'}=$y1;
       $genecoords{$1}{'y2'}=$y2;
       $genecoords{$1}{'y3'}=$y3;
       $output.="\\psline[".$params{'connlinestyle'}."]($last_x,$y3)($x3,$y3)\n";
       $last_x=$x1;
       $output.= "\\pspolygon[".$params{'genearrowstyle'}.",fillcolor=$3]($x1,$y1)($x1,$y2)($x2,$y2)($x3,$y3)($x2,$y1)\n";
       $output.= "\\rput[br]{-".$params{'angle'}."}($x4,$y4){\\".$params{'genetype'}."{$1}}\n";
       $gene_x+=$width+$params{'geneskipx'};
     } else {
       print STDERR "Color $3 not defined for $1 of $kind_name, $1 skiped!\n";
     };
  };

  if(/^link "($RE_gene)" "($RE_gene)"/) {
    if(defined($genecoords{$1}) and defined($genecoords{$2})) {
       $x1=$genecoords{$1}{'x1'}+$params{'linkshiftx'};
       $x2=$genecoords{$1}{'x2'}+$params{'linkshiftx'};
       $y1=$genecoords{$1}{'y1'}-$params{'linkskipy'};
       $x3=$genecoords{$2}{'x1'}+$params{'linkshiftx'};
       $x4=$genecoords{$2}{'x2'}+$params{'linkshiftx'};
       $y2=$genecoords{$2}{'y2'}+$params{'linkskipy'};
       
       $output="%link from $1 to $2\n\\pspolygon[".$params{'linkstyle'}.']'.
          "($x1,$y1)($x2,$y1)($x4,$y2)($x3,$y2)\n"
          .$output;
    };
  };
  if(/^skip "($RE_skip)" ($RE_Real)/) {
       $width=$2;
       $x1=$gene_x+$params{'skipspacex'};
       $x2=$x1+$width;
       $x3=($x1+$x2)/2.0;
       $gene_x=$x2+$params{'skipspacex'};
       $y1=$kind_y;
       $y2=$kind_y+$params{'skipsizey'};
       $y3=$y2+$params{'skipspacey'}; 
       $output.="\\pspolygon[".$params{'skipstyle'}.']'.
             "($x1,$y2)($x2,$y2)($x3,$y1)\n";
       $output.= "\\rput[b]($x3,$y3){\\".$params{'skiptype'}."{$1}}\n";
  };
  if(/^(\w+)=(.*)$/) {
    $params{$1}=$2;
    if("$1" eq "start") {
      $gene_x=$2/$params{'nucleospercm'};
    };
  };
  
};
print $output."\n\\end{document}";
