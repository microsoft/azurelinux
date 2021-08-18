
TESTOBJ=../fillup
REF=./REFERENCE
OUT=./OUT
DIF=./DIFFERENCE


all:	Test1 Test2 Test3 Test4
	@echo ""
	@echo "If subdirectory $(DIF) is empty the test has been successful"
	@echo ""
	ls -al $(DIF)
	@echo ""


	
Test1:	Test100 Test110 Test120 Test121 Test130 Test131
Test2:  Test200 Test210 Test220 Test221 Test230 Test231
Test3:  Test300 Test310 Test320 Test321 Test330 Test331
Test4:                  Test420 Test421



Test100: fillup
# 	option -m 
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) basefile addfile outfile
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test100.txt > TestDifference.txt
	./Evaluate 100


Test110: fillup
# 	option -x 
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -x basefile addfile outfile
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test110.txt > TestDifference.txt
	./Evaluate 110


Test120: fillup
# 	option -m -r
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -m -r basefile addfile outfile
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test120.txt > TestDifference.txt
	./Evaluate 120
	-diff basefile.new $(REF)/Test120.newtxt > TestDifference.txt
	./Evaluate 120


Test121: fillup
# 	option -m -r
#       same test case as 120, but option -t added
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -m -r -t basefile addfile outfile
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test121.txt > TestDifference.txt
	./Evaluate 121
	-diff basefile.new $(REF)/Test121.newtxt > TestDifference.txt
	./Evaluate 121


Test130: fillup
# 	option -x -r
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -x -r basefile addfile outfile
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test130.txt > TestDifference.txt
	./Evaluate 130
	-diff basefile.new $(REF)/Test130.newtxt > TestDifference.txt
	./Evaluate 130


Test131: fillup
# 	option -x -r
#       same test case as 130, but option -t added
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -x -r -t basefile addfile outfile
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test131.txt > TestDifference.txt
	./Evaluate 131
	-diff basefile.new $(REF)/Test131.newtxt > TestDifference.txt
	./Evaluate 131



Test200: fillup
# 	option -m, but observed variable isn't first in file
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) basefile addfile outfile
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test200.txt > TestDifference.txt
	./Evaluate 200


Test210: fillup
# 	option -x, but observed variable isn't first in file
#	an existing trailer of basefile remains
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -x -t basefile addfile outfile
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test210.txt > TestDifference.txt
	./Evaluate 210


Test220: fillup
# 	option -m -r, but observed variable isn't first in file
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCompleteVariableBlock basefile LANGUAGE foo
	@echo "" >> basefile
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -m -r basefile addfile outfile
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test220.txt > TestDifference.txt
	./Evaluate 220
	-diff basefile.new $(REF)/Test220.newtxt > TestDifference.txt
	./Evaluate 220


Test221: fillup
# 	option -m -r, but observed variable isn't first in file
#       same test case as 220, but option -t added
# catched watchdog exception for fillup-1.22
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -m -r -t basefile addfile outfile 2> TestStderr.txt
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test221.txt > TestDifference.txt
	./Evaluate 221
	-diff basefile.new $(REF)/Test221.newtxt > TestDifference.txt
	./Evaluate 221
	./CheckForException 221


Test230: fillup
# 	option -x -r, but observed variable isn't first in file
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -x -r basefile addfile outfile
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test230.txt > TestDifference.txt
	./Evaluate 230
	-diff basefile.new $(REF)/Test230.newtxt > TestDifference.txt
	./Evaluate 230


Test231: fillup
# 	option -x -r, but observed variable isn't first in file
#       same test case as 230, but option -t added
# catched watchdog exception for fillup-1.22
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -x -r -t basefile addfile outfile 2> TestStderr.txt
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test231.txt > TestDifference.txt
	./Evaluate 231
	-diff basefile.new $(REF)/Test231.newtxt > TestDifference.txt
	./Evaluate 231
	./CheckForException 231



Test300: fillup
# 	option -m, but observed variable isn't first in file
#       metadata inserted
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	echo "" >> addfile
	./CreateMetaData addfile Path /tmp
	./CreateMetaData addfile Description "temporary files are located there"
	./CreateMetaData addfile Type "not specified"
	./CreateMetaData addfile Default none
	./CreateAssignmentBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) basefile addfile outfile
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test300.txt > TestDifference.txt
	./Evaluate 300


Test310: fillup
# 	option -x, but observed variable isn't first in file
#	an existing trailer of basefile remains
#       metadata replaced partially
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	echo "" >> basefile
	./CreateMetaData basefile Description "no temporary files"
	./CreateMetaData basefile Type "specified later"
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	echo "" >> basefile
	./CreateTrailingComment basefile 
	echo "" >> addfile
	./CreateMetaData addfile Path /tmp
	./CreateMetaData addfile Description "temporory files are located there"
	./CreateMetaData addfile Type "not specified"
	./CreateMetaData addfile Default none
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -x -t basefile addfile outfile
	# ./ShowFiles basefile addfile outfile
	-diff outfile $(REF)/Test310.txt > TestDifference.txt
	./Evaluate 310


Test320: fillup
# 	option -m -r, but observed variable isn't first in file
#       metadata replaced partially
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCompleteVariableBlock basefile LANGUAGE foo
	echo "" >> basefile
	./CreateMetaData basefile Description "no temporary files"
	./CreateMetaData basefile Type "specified later"
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	echo "" >> addfile
	./CreateMetaData addfile Path /tmp
	./CreateMetaData addfile Type "not specified"
	./CreateMetaData addfile Default none
	./CreateAssignmentBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -m -r basefile addfile outfile
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test320.txt > TestDifference.txt
	./Evaluate 320
	-diff basefile.new $(REF)/Test320.newtxt > TestDifference.txt
	./Evaluate 320


Test321: fillup
# 	option -m -r, but observed variable isn't first in file
#       same test case as 320, but option -t added
# catched watchdog exception for fillup-1.22
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -m -r -t basefile addfile outfile 2> TestStderr.txt
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test321.txt > TestDifference.txt
	./Evaluate 321
	-diff basefile.new $(REF)/Test321.newtxt > TestDifference.txt
	./Evaluate 321
	./CheckForException 321


Test330: fillup
# 	option -x -r, but observed variable isn't first in file
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -x -r basefile addfile outfile
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test330.txt > TestDifference.txt
	./Evaluate 330
	-diff basefile.new $(REF)/Test330.newtxt > TestDifference.txt
	./Evaluate 330


Test331: fillup
# 	option -x -r, but observed variable isn't first in file
#       same test case as 330, but option -t added
# catched watchdog exception for fillup-1.22
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile LANGUAGE foo
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateCompleteVariableBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -x -r -t basefile addfile outfile 2> TestStderr.txt
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test331.txt > TestDifference.txt
	./Evaluate 331
	-diff basefile.new $(REF)/Test331.newtxt > TestDifference.txt
	./Evaluate 331
	./CheckForException 331



Test420: fillup
# 	option -i -r, but observed variable isn't first in file
#       metadata replaced partially
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCompleteVariableBlock basefile LANGUAGE foo
	echo "" >> basefile
	./CreateMetaData basefile Description "no temporary files"
	./CreateMetaData basefile Type "specified later"
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	echo "" >> addfile
	./CreateMetaData addfile Path /tmp
	./CreateMetaData addfile Type "not specified"
	./CreateMetaData addfile Default none
	./CreateAssignmentBlock addfile PATH /local
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -r -i basefile addfile outfile
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test420.txt > TestDifference.txt
	./Evaluate 420
	-diff basefile.new $(REF)/Test420.newtxt > TestDifference.txt
	./Evaluate 420


Test421: fillup
# 	option -r -i, but observed variable is first in file
#       similar test case as 420, but option -t added
	rm -f basefile* addfile outfile
	./CreateHeader basefile
	./CreateCommentedVariableBlock basefile PATH /var/log
	./CreateAssignmentBlock basefile PATH /tmp
	./CreateTrailingComment basefile 
	./CreateHeader addfile
	./CreateVariableNameBlock addfile PATH
	./CreateTrailingComment addfile 
	# ./ShowFiles basefile addfile
	$(TESTOBJ) -i -r -t basefile addfile outfile 2> TestStderr.txt
	# ./ShowFiles basefile addfile outfile basefile.new
	-diff outfile $(REF)/Test421.txt > TestDifference.txt
	./Evaluate 421
	-diff basefile.new $(REF)/Test421.newtxt > TestDifference.txt
	./Evaluate 421
	./CheckForException 421






fillup:
	make -C ../../SRC clean
	make -C ../../SRC all
	mv ../../BIN/fillup $(TESTOBJ)

clean:
	rm -rf DIFFERENCE/*
	rm -f basefile* addfile outfile logfile TestStderr.txt


