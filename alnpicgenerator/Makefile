all::
	perl generate.pl < testinput.txt > testout.tex
	latex test.tex
	dvips test.dvi -o test.ps
	gv test.ps
TypeII_SRMS.ps:: TypeII_SRMS.txt generate.pl
	perl generate.pl < TypeII_SRMS.txt > TypeII_SRMS.tex
	latex TypeII_SRMS.tex
	dvips TypeII_SRMS.dvi -o TypeII_SRMS.ps
	gv TypeII_SRMS.ps 
