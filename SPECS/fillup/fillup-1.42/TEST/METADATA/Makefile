
TESTOBJ=../fillup
REF=./REFERENCE
OUT=./OUT
DIF=./DIFFERENCE


all:	Test1 Test2 Test3 Test4 Bugzilla
	@echo ""
	@echo "If subdirectory $(DIF) is empty the test has been successful"
	@echo ""
	ls -al $(DIF)
	@echo ""

special: TestBugzilla29212

Test1:	Test100 
Test2:  Test200 Test201 Test220
Test3:	Test300 Test301 Test302
Test4:  Test400 Test401 Test402
Bugzilla: TestBugzilla25119 TestBugzilla29212

Test100: fillup
	@echo "---------------------------"
	echo " " > basefile
	echo "#" >> basefile
	echo "GAMBIT=NO_GAMBIT" >> basefile
	echo " " >> basefile
	@echo "---------------------------"
	echo " " > addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "## Description: a variation of Queens gambit accepted" >> addfile
	echo "## Type:        forced line, if black holds the pawn on c4" >> addfile
	echo "## Default:     with initiative for white" >> addfile
	echo "#" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	echo " " >> addfile
	$(TESTOBJ) -t basefile addfile outfile
	-diff $(REF)/Test100.txt outfile > TestDifference.txt
	./Evaluate 100
	@echo "---------------------------"

Test200: fillup
	@echo "---------------------------"
	echo " " > basefile
	echo "## Description: D15 of encyclopaedia" >> basefile
	echo "## Type:        pawn on c4 is additional piece" >> basefile
	echo "#" >> basefile
	echo "GAMBIT=NO_GAMBIT" >> basefile
	echo " " >> basefile
	@echo "---------------------------"
	echo " " > addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "## Description: a variation of Queens gambit accepted" >> addfile
	echo "## Type:        forced line, if black holds the pawn on c4" >> addfile
	echo "## Default:     with initiative for white" >> addfile
	echo "#" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	echo " " >> addfile
	$(TESTOBJ) -t basefile addfile outfile
	-diff $(REF)/Test200.txt outfile > TestDifference.txt
	./Evaluate 200
	@echo "---------------------------"

Test201: fillup
	@echo "---------------------------"
	echo " " > basefile
	echo "## Description: D15 of encyclopaedia" >> basefile
	echo "## Type:        pawn on c4 is additional piece" >> basefile
	echo "#" >> basefile
	echo "GAMBIT=NO_GAMBIT" >> basefile
	echo " " >> basefile
	@echo "---------------------------"
	echo " " > addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "## Default:     with initiative for white" >> addfile
	echo "#" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	echo " " >> addfile
	$(TESTOBJ) -t basefile addfile outfile
	-diff $(REF)/Test201.txt outfile > TestDifference.txt
	./Evaluate 201
	@echo "---------------------------"

Test220: fillup
	@echo "---------------------------"
	echo " " > basefile
	echo "## Description: D15 of encyclopaedia" >> basefile
	echo "## Description: To avoid the Geller Gambit white normally plays" >> basefile
	echo "##            : the normal move 5.a4. This guarantees the recapture" >> basefile
	echo "##              of the gambited pawn on c4 at the cost of a tempo." >> basefile
	echo "## Type:        pawn on c4 is additional piece" >> basefile
	echo "## Description: Occupying centre immediately or gambiting a pawn" >> basefile
	echo "#" >> basefile
	echo "GAMBIT=NO_GAMBIT" >> basefile
	echo " " >> basefile
	@echo "---------------------------"
	echo " " > addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "## Default:     with initiative for white" >> addfile
	echo "#" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	echo " " >> addfile
	$(TESTOBJ) -t basefile addfile outfile
	-diff $(REF)/Test220.txt outfile > TestDifference.txt
	./Evaluate 220
	@echo "---------------------------"

Test300: fillup
	@echo "---------------------------"
	echo " " > basefile
	echo "#" >> basefile
	echo "## Description: D15 of encyclopaedia" >> basefile
	echo "## Type:        pawn on c4 is additional piece" >> basefile
	echo "GAMBIT=NO_GAMBIT" >> basefile
	echo " " >> basefile
	@echo "---------------------------"
	echo " " > addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "## Description: a variation of Queens gambit accepted" >> addfile
	echo "## Type:        forced line, if black holds the pawn on c4" >> addfile
	echo "## Default:     with initiative for white" >> addfile
	echo "#" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	echo " " >> addfile
	$(TESTOBJ) -t basefile addfile outfile
	-diff $(REF)/Test300.txt outfile > TestDifference.txt
	./Evaluate 300
	@echo "---------------------------"

Test301: fillup
	@echo "---------------------------"
	echo " " > basefile
	echo "#########################################################" >> basefile
	echo "#" >> basefile
	echo "# This is an example of a multiple defined variable but " >> basefile
	echo "# metadata information is not included at first appearence." >> basefile
	echo "# Therefore correct metadata will be seen as part of comment" >> basefile
	echo "#" >> basefile
	echo "########################################################" >> basefile
	echo "GAMBIT=QUEENS_GAMBIT_ACCEPTED" >> basefile
	echo " " >> basefile
	echo "#" >> basefile
	echo "## Description: D15 of encyclopaedia" >> basefile
	echo "## Type:        pawn on c4 is additional piece" >> basefile
	echo "GAMBIT=NO_GAMBIT" >> basefile
	echo " " >> basefile
	@echo "---------------------------"
	echo " " > addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "## Description: a variation of Queens gambit accepted" >> addfile
	echo "## Type:        forced line, if black holds the pawn on c4" >> addfile
	echo "## Default:     with initiative for white" >> addfile
	echo "#" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	echo " " >> addfile
	$(TESTOBJ) -t basefile addfile outfile
	-diff $(REF)/Test301.txt outfile > TestDifference.txt
	./Evaluate 301
	@echo "---------------------------"


Test302: fillup
	@echo "---------------------------"
	echo " " > basefile
	echo "#########################################################" >> basefile
	echo "#" >> basefile
	echo "# This is an example of a multiple defined variable but " >> basefile
	echo "# metadata information is not included at first appearence." >> basefile
	echo "# Therefore correct metadata will be seen as part of comment" >> basefile
	echo "#" >> basefile
	echo "########################################################" >> basefile
	echo "GAMBIT=QUEENS_GAMBIT_ACCEPTED" >> basefile
	echo " " >> basefile
	echo "#" >> basefile
	echo "## Description: D15 of encyclopaedia" >> basefile
	echo "## Type:        pawn on c4 is additional piece" >> basefile
	echo "GAMBIT=NO_GAMBIT" >> basefile
	echo " " >> basefile
	@echo "---------------------------"
	echo " " > addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "## Description: a variation of Queens gambit accepted" >> addfile
	echo "## Type:        forced line, if black holds the pawn on c4" >> addfile
	echo "## Default:     with initiative for white" >> addfile
	echo "#" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	echo " " >> addfile
	$(TESTOBJ) -t -logfile ./logfile -variable GAMBIT basefile addfile outfile
	-diff $(REF)/Test302.txt outfile > TestDifference.txt
	-diff $(REF)/Test302.logfile logfile >> TestDifference.txt
	./Evaluate 302
	echo "logging calls normally the watchdog - ignore this at this place"
	@echo "---------------------------"


Test400: fillup
	@echo "---------------------------"
	echo "##" > basefile
	echo "GAMBIT=QUEENS_GAMBIT_ACCEPTED" >> basefile
	@echo "---------------------------"
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" > addfile
	echo "##" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	@echo "---------------------------"
	@echo "Bug report dated 2003-02-17:"
	@echo "Consuming white spaces beetween '##' and metadata information is"
	@echo "replaced by consuming only blanks and tabs."
	$(TESTOBJ) -q basefile addfile outfile
	-diff outfile $(REF)/Test400.txt > TestDifference.txt
	./Evaluate 400
	@echo "---------------------------"


Test401: fillup
	@echo "---------------------------"
	echo "" > basefile
	echo "  	  " > basefile
	echo "" > basefile
	echo "##" >> basefile
	echo "GAMBIT=QUEENS_GAMBIT_ACCEPTED" >> basefile
	@echo "---------------------------"
	echo "" > addfile
	echo "  	  " >> addfile
	echo "" >> addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "##" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	@echo "---------------------------"
	@echo "Bug report dated 2003-02-17:"
	@echo "Same testcase as Test400, but with white space prefixes"
	$(TESTOBJ) -q basefile addfile
	-diff basefile $(REF)/Test401.txt > TestDifference.txt
	./Evaluate 401
	@echo "---------------------------"


Test402: fillup
	@echo "---------------------------"
	echo "" > basefile
	echo "  	  " > basefile
	echo "" > basefile
	echo "##" >> basefile
	echo "GAMBIT=QUEENS_GAMBIT_ACCEPTED" >> basefile
	@echo "---------------------------"
	echo "" > addfile
	echo "  	  " >> addfile
	echo "" >> addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "##" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	@echo "---------------------------"
	@echo "Bug report dated 2003-02-17:"
	@echo "Same testcase as Test401, but iterated"
	$(TESTOBJ) -q basefile addfile
	-diff basefile $(REF)/Test401.txt > TestDifference.txt
	./Evaluate 401
	echo "" > addfile
	echo "  	  " >> addfile
	echo "" >> addfile
	echo "## Path:        d2-d4/d7-d5/c2-c4/c7-c6/Ng1-f3/Ng8-f6/Nb1-c3/d5xc4/e2-e4" >> addfile
	echo "## (second iteration)" >> addfile
	echo "GAMBIT=GELLER_GAMBIT" >> addfile
	@echo "---------------------------"
	$(TESTOBJ) -q basefile addfile
	-diff basefile $(REF)/Test402.txt > TestDifference.txt
	./Evaluate 402




TestBugzilla25119: fillup
	rm -f basefile
	touch basefile
	@echo "---------------------------"
	echo "## Path:       Network/WWW/Apache" > addfile
	echo "## Default:    yes" >> addfile
	echo "## Type:       yesno" >> addfile
	echo "#" >> addfile
	echo "# enable the PHP module (yes|no)" >> addfile
	echo "#" >> addfile
	echo "HTTPD_SEC_MOD_PHP=yes" >> addfile
	@echo "---------------------------"
	$(TESTOBJ) basefile addfile outfile
	-diff outfile $(REF)/TestBugzilla25119.firstrun.txt > TestDifference.txt
	# outfile is identical to addfile
	./Evaluate Bugzilla25119
	@echo "---------------------------"
	mv outfile basefile
	touch basefile
	@echo "---------------------------"
	$(TESTOBJ) basefile addfile
	-diff basefile $(REF)/TestBugzilla25119.secondrun.txt > TestDifference.txt
	./Evaluate Bugzilla25119
	@echo "---------------------------"



TestBugzilla29212:
	echo "This is Test215341 from FCSR with an other order within metadata kewwords"
	echo "" > basefile
	echo "## Default: \"This is the value of metadata variable: D1dd111ddddd\"" >> basefile
	echo "## Path: \"This is the value of metadata variable: A1aa111aaaaa\"" >> basefile
	echo "## Command: \"This is the value of metadata variable: H1hh111hhhhh\"" >> basefile
	echo "## ServiceRestart: \"This is the value of metadata variable: G1gg111ggggg\"" >> basefile
	echo "#" >> basefile 
	echo "# This is a comment for automatically generated basefile" >> basefile
	echo "#" >> basefile 
	echo "TESTVARIABLE=ShiftRegister of basefile" >> basefile
	echo "" > addfile
	echo "## Command: \"This is the value of metadata variable: H2hh222hhhhh\"" >> addfile
	echo "## Config: \"This is the value of metadata variable: E2ee222eeeee\"" >> addfile
	echo "## Description: \"This is the value of metadata variable: B2bb222bbbbb\"" >> addfile
	echo "## Path: \"This is the value of metadata variable: A2aa222aaaaa\"" >> addfile
	echo "#" >> addfile 
	echo "# This is a comment for automatically generated addfile" >> addfile
	echo "#" >> addfile 
	echo "TESTVARIABLE=ShiftRegister of addfile" >> addfile
	@echo "---------------------------"
	$(TESTOBJ) basefile addfile outfile
	-diff outfile $(REF)/TestBugzilla29212.txt > TestDifference.txt
	./Evaluate Bugzilla29212
	@echo "---------------------------"



fillup:
	make -C ../../SRC clean
	make -C ../../SRC all
	mv ../../BIN/fillup $(TESTOBJ)

clean:
	rm -rf DIFFERENCE/*
	rm -f basefile addfile outfile logfile

