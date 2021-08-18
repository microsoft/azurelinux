
TESTOBJ=../fillup
REF=./REFERENCE
OUT=./OUT
DIF=./DIFFERENCE


all:	Test1 Test2 Test3 Test4 Test5 Test6 Test7 Test8 Bugzilla
	@echo ""
	@echo "If subdirectory $(DIF) is empty the test has been successful"
	@echo ""
	ls -al $(DIF)
	@echo ""


Test1:	Test100 Test101 Test102 Test103 Test104
Test2:  Test200 Test201
Test3:  Test300 Test301
Test4:  Test400 Test401 Test402 Test403
Test5:  Test500 Test501 Test510 Test511 Test512 Test513 Test514
Test6:  Test600
Test7:  Test700 Test701 Test702
Test8:  Test800 Test801 Test802

Bugzilla: TestBugzilla24540 TestBugzilla30279


Test100: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1 4 7 10 13 trailer
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t authors.base authors.add authors.outfile
	-diff $(REF)/Test100.txt authors.outfile > TestDifference.txt
	./Evaluate 100
	@echo "---------------------------"

Test101: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1 4 7 10 13 trailer
	cp authors.text ./authors.outfile
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t authors.base authors.add 
	-diff $(REF)/Test101.txt authors.base > TestDifference.txt
	./Evaluate 101
	-diff $(REF)/Test101.txt authors.outfile > TestDifference.txt
	./Evaluate 101
	@echo "---------------------------"

Test102: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 4 7 10 trailer
	mv authors.text ./authors.base
	./CreateAuthors 2 8 14
	mv authors.text ./authors.add
	./CreateAuthors 4 7 10 trailer 2 14 
	$(TESTOBJ) -t authors.base authors.add authors.outfile
	cat authors.outfile empty > authors.tmp
	-diff authors.text authors.tmp > TestDifference.txt
	./Evaluate 102
	-diff $(REF)/Test102.txt authors.outfile > TestDifference.txt
	./Evaluate 102
	@echo "---------------------------"

Test103: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 4 7 10 trailer
	mv authors.text ./authors.base
	./CreateAuthors 2 8 14
	mv authors.text ./authors.add
	./CreateAuthors 4 7 10 trailer 2 14 
	$(TESTOBJ) -t authors.base authors.add
	cat authors.base empty > authors.tmp
	-diff authors.text authors.tmp > TestDifference.txt
	./Evaluate 103
	-diff $(REF)/Test103.txt authors.base > TestDifference.txt
	./Evaluate 103
	@echo "---------------------------"

Test104: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 4 7 10 trailer
	mv authors.text ./authors.base
	./CreateAuthors 2 8 14
	mv authors.text ./authors.add
	./CreateAuthors 4 7 10 trailer 2 14 
	$(TESTOBJ) -t --maintain --quiet authors.base authors.add
	cat authors.base empty > authors.tmp
	-diff authors.text authors.tmp > TestDifference.txt
	./Evaluate 104
	-diff $(REF)/Test104.txt authors.base > TestDifference.txt
	./Evaluate 104
	@echo "---------------------------"

Test200: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1 4 7 trailer
	mv authors.text ./authors.base
	./CreateAuthors 5 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t -x authors.base authors.add authors.outfile
	-diff $(REF)/Test200.txt authors.outfile > TestDifference.txt
	./Evaluate 200
	@echo "---------------------------"

Test201: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1-HEADER 4 7 trailer
	mv authors.text ./authors.base
	./CreateAuthors 5 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t -x authors.base authors.add authors.outfile
	-diff $(REF)/Test201.txt authors.outfile > TestDifference.txt
	./Evaluate 201
	@echo "---------------------------"

Test300: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1 4 7 trailer
	mv authors.text ./authors.base
	./CreateAuthors 5 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t -i authors.base authors.add authors.outfile
	-diff $(REF)/Test300.txt authors.outfile > TestDifference.txt
	./Evaluate 300
	@echo "---------------------------"

Test301: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1-HEADER 4 7 trailer
	mv authors.text ./authors.base
	./CreateAuthors 6 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t -i authors.base authors.add authors.outfile
	-diff $(REF)/Test301.txt authors.outfile > TestDifference.txt
	./Evaluate 301
	@echo "---------------------------"

Test400: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1 4 7 10 13 trailer
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t -r authors.base authors.add authors.outfile
	-diff $(REF)/Test400.txt authors.outfile > TestDifference.txt
	./Evaluate 400
	-diff $(REF)/Test400.newtxt authors.base.new > TestDifference.txt
	./Evaluate 400
	@echo "---------------------------"

Test401: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1-HEADER 4 7 10 13 trailer
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t -r authors.base authors.add authors.outfile
	-diff $(REF)/Test401.txt authors.outfile > TestDifference.txt
	./Evaluate 401
	-diff $(REF)/Test401.newtxt authors.base.new > TestDifference.txt
	./Evaluate 401
	@echo "---------------------------"

Test402: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors HEADER
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t -r authors.base authors.add authors.outfile
	-diff $(REF)/Test402.txt authors.outfile > TestDifference.txt
	./Evaluate 402
	-diff $(REF)/Test402.newtxt authors.base.new > TestDifference.txt
	./Evaluate 402
	@echo "---------------------------"

Test403: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors HEADER
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	mv authors.text ./authors.add
	$(TESTOBJ) -r -i authors.base authors.add authors.outfile
	-diff $(REF)/Test403.txt authors.outfile > TestDifference.txt
	./Evaluate 403
	-diff $(REF)/Test403.newtxt authors.base.new > TestDifference.txt
	./Evaluate 403
	@echo "---------------------------"

Test500: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1 4 7 10 13 trailer
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t -r -x authors.base authors.add authors.outfile
	-diff $(REF)/Test500.txt authors.outfile > TestDifference.txt
	./Evaluate 500
	-diff $(REF)/Test500.newtxt authors.base.new > TestDifference.txt
	./Evaluate 500
	@echo "---------------------------"

Test501: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1-HEADER 4 7 10 13 trailer
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	mv authors.text ./authors.add
	$(TESTOBJ) -t -r -x authors.base authors.add authors.outfile
	-diff $(REF)/Test501.txt authors.outfile > TestDifference.txt
	./Evaluate 501
	-diff $(REF)/Test501.newtxt authors.base.new > TestDifference.txt
	./Evaluate 501
	@echo "---------------------------"

Test510: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors HEADER HEADER
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	cat VBN-base >> ./authors.text
	mv authors.text ./authors.add
	$(TESTOBJ) -q -d = authors.base authors.add authors.outfile
	-diff $(REF)/Test510.txt authors.outfile > TestDifference.txt
	./Evaluate 510
	@echo "---------------------------"

Test511: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors HEADER HEADER
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	cat VBN-base >> ./authors.text
	mv authors.text ./authors.add
	$(TESTOBJ) authors.base authors.add 
	-diff $(REF)/Test511.txt authors.base > TestDifference.txt
	./Evaluate 511
	@echo "---------------------------"

Test512: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors HEADER HEADER
	cat VBN-base >> ./authors.text
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	cat VBN-add >> ./authors.text
	mv authors.text ./authors.add
	$(TESTOBJ) -m authors.base authors.add 
	-diff $(REF)/Test512.txt authors.base > TestDifference.txt
	./Evaluate 512
	@echo "---------------------------"

Test513: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors HEADER HEADER
	cat VBN-base >> ./authors.text
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	cat VBN-add >> ./authors.text
	mv authors.text ./authors.add
	$(TESTOBJ) -x authors.base authors.add 
	-diff $(REF)/Test513.txt authors.base > TestDifference.txt
	./Evaluate 513
	@echo "---------------------------"

Test514: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors HEADER HEADER
	cat VBN-base >> ./authors.text
	mv authors.text ./authors.base
	./CreateAuthors 2 14
	cat VBN-add >> ./authors.text
	mv authors.text ./authors.add
	$(TESTOBJ) -r authors.base authors.add authors.outfile
	-diff $(REF)/Test514.txt authors.base > TestDifference.txt
	./Evaluate 514
	@echo "---------------------------"


Test600: fillup
	@echo "---------------------------"
	rm -f authors.*
	./CreateAuthors 1 7 
	mv authors.text ./authors.base
	./CreateAuthors 5 13 trailer
	mv authors.text ./authors.add
	$(TESTOBJ) -r -i authors.base authors.add authors.outfile
	-diff $(REF)/Test600.txt authors.outfile > TestDifference.txt
	./Evaluate 600
	-diff $(REF)/Test600.newtxt authors.base.new > TestDifference.txt
	./Evaluate 600
	@echo "---------------------------"


Test700: fillup
	@echo "---------------------------"
	rm -f authors.*
	cat HEADER HEADER > authors.text
	./Downsize 7 =
	./Comment "_0=NO_LONGER_USED_VALUE" >> authors.text
	./Upsize "_0=USED_VALUE" >> authors.text
	./Upsize "_1=\"Underscore_one\"" >> authors.text
	./Upsize "_2= Underscore_two" >> authors.text
	./Upsize "_3=\"Underscore_three\"" >> authors.text
	mv authors.text ./authors.base
	./Upsize "_0=\"\"" > authors.text
	./Upsize "_1=\"\"" >> authors.text
	./Upsize "_2=\"\"" >> authors.text
	./Upsize "_3=" >> authors.text
	mv authors.text ./authors.add
	rm -rf ./downsized
	$(TESTOBJ) -r -i authors.base authors.add authors.outfile
	-diff $(REF)/Test700.txt authors.outfile > TestDifference.txt
	./Evaluate 700
	-diff $(REF)/Test700.newtxt authors.base.new > TestDifference.txt
	./Evaluate 700
	@echo "---------------------------"

Test701: fillup
	@echo "---------------------------"
	rm -f authors.*
	cat HEADER HEADER > authors.text
	./Downsize 7 =
	./Comment "_0=NO_LONGER_USED_VALUE" >> authors.text
	./Upsize "_0=USED_VALUE" >> authors.text
	./Comment "_1=\"Underscore_one\"" >> authors.text
	./Comment "_2= Underscore_two" >> authors.text
	./Upsize "_3=\"Underscore_three\"" >> authors.text
	mv authors.text ./authors.base
	./Upsize "_0=\"\"" > authors.text
	./Upsize "_1=\"\"" >> authors.text
	./Upsize "_2=\"\"" >> authors.text
	./Upsize "_3=" >> authors.text
	mv authors.text ./authors.add
	rm -rf ./downsized
	$(TESTOBJ) -r -i authors.base authors.add authors.outfile
	-diff $(REF)/Test701.txt authors.outfile > TestDifference.txt
	./Evaluate 701
	-diff $(REF)/Test701.newtxt authors.base.new > TestDifference.txt
	./Evaluate 701
	@echo "---------------------------"

Test702: fillup
	@echo "---------------------------"
	rm -f authors.*
	cat HEADER HEADER > authors.text
	./Downsize 7 =
	./Comment "_0=NO_LONGER_USED_VALUE" >> authors.text
	./Upsize "_0=USED_VALUE" >> authors.text
	./Upsize "_1=\"Underscore_one\"" >> authors.text
	./Upsize "_2= Underscore_two" >> authors.text
	./Upsize "_3=\"Underscore_three\"" >> authors.text
	mv authors.text ./authors.base
	./Upsize "_0=\"\"" > authors.text
	./Upsize "_1=\"\"" >> authors.text
	./Upsize "_2=\"\"" >> authors.text
	./Upsize "_3=" >> authors.text
	mv authors.text ./authors.add
	rm -rf ./downsized
	$(TESTOBJ) -t -r -i -d = authors.base authors.add 
	-diff $(REF)/Test702.txt authors.base > TestDifference.txt
	./Evaluate 702
	-diff $(REF)/Test702.newtxt authors.base.new > TestDifference.txt
	./Evaluate 702
	@echo "---------------------------"


Test800: fillup
	@echo "---------------------------"
	rm -f authors.*
	cat HEADER HEADER > authors.text
	./Downsize 7 =
	./Comment "_0=NO_LONGER_USED_VALUE" >> authors.text
	./Upsize "_0=USED_VALUE" >> authors.text
	./Upsize "_1=\"Underscore_one\"" >> authors.text
	./Upsize "_0= OVERWRITTEN_VARIABLE" >> authors.text
	./Comment "= BASE_VARIABLE" >> authors.text
	./Upsize "= BASE_VARIABLE_VALUE" >> authors.text
	./Comment "= BASE_VARIABLE_POSTCOMMENT" >> authors.text
	mv authors.text ./authors.base
	./Upsize "_0=\"\"" > authors.text
	./Comment "_1=NO_LONGER_USED_VALUE" >> authors.text
	mv authors.text ./authors.add
	rm -rf ./downsized
	$(TESTOBJ) -r -i -m authors.base authors.add authors.outfile
	-diff $(REF)/Test800.txt authors.outfile > TestDifference.txt
	./Evaluate 800
	-diff $(REF)/Test800.newtxt authors.base.new > TestDifference.txt
	./Evaluate 800
	@echo "---------------------------"

Test801: fillup
	@echo "---------------------------"
	rm -f authors.*
	cat HEADER HEADER > authors.text
	./Downsize 7 =
	./Comment "_0=NO_LONGER_USED_VALUE" >> authors.text
	./Upsize "_0=USED_VALUE" >> authors.text
	./Upsize "_1=\"Underscore_one\"" >> authors.text
	./Upsize "_0= OVERWRITTEN_VARIABLE" >> authors.text
	./Comment "= BASE_VARIABLE" >> authors.text
	./Upsize "= BASE_VARIABLE_VALUE" >> authors.text
	./Comment "= BASE_VARIABLE_POSTCOMMENT" >> authors.text
	mv authors.text ./authors.base
	./Upsize "_1=\"\"" > authors.text
	./Comment "_0=NO_LONGER_USED_VALUE" >> authors.text
	mv authors.text ./authors.add
	rm -rf ./downsized
	$(TESTOBJ) -r -i authors.base authors.add authors.outfile
	-diff $(REF)/Test801.txt authors.outfile > TestDifference.txt
	./Evaluate 801
	-diff $(REF)/Test801.newtxt authors.base.new > TestDifference.txt
	./Evaluate 801
	@echo "---------------------------"



Test802: fillup
	@echo "---------------------------"
	rm -f authors.*
	cat HEADER HEADER > authors.text
	./Downsize 7 =
	./Comment "_0=NO_LONGER_USED_VALUE" >> authors.text
	./Upsize "_0=USED_VALUE" >> authors.text
	./Upsize "_1=\"Underscore_one\"" >> authors.text
	./Upsize "_0= OVERWRITTEN_VARIABLE" >> authors.text
	./Comment "= BASE_VARIABLE" >> authors.text
	./Upsize "= BASE_VARIABLE_VALUE" >> authors.text
	./Comment "= BASE_VARIABLE_POSTCOMMENT" >> authors.text
	mv authors.text ./authors.base
	./Comment "=\"\"" > authors.text
	./Upsize "=\"\"" >> authors.text
	mv authors.text ./authors.add
	rm -rf ./downsized
	$(TESTOBJ) -r -i -m authors.base authors.add authors.outfile
	-diff $(REF)/Test802.txt authors.outfile > TestDifference.txt
	./Evaluate 802
	-diff $(REF)/Test802.newtxt authors.base.new > TestDifference.txt
	./Evaluate 802
	@echo "---------------------------"




TestBugzilla23876: fillup
	@echo "---------------------------"
	echo "# header1" > basefile
	echo "" >> basefile
	echo "# abc" >> basefile
	echo "ABC='abc'" >> basefile
	echo "# header2" > addfile
	echo "" >> addfile
	echo "# abcd" >> addfile
	echo "ABCD='abcd'" >> addfile
	$(TESTOBJ) basefile addfile outfile
	-diff outfile $(REF)/TestBugzilla23876.txt > TestDifference.txt
	./Evaluate Bugzilla23876
	@echo "---------------------------"



TestBugzilla24540: fillup
	@echo "---------------------------"
	echo "# " > basefile
	echo "# this is the first comment" >> basefile
	echo "# " >> basefile
	echo "VAR_1=47" >> basefile
	echo "# " >> basefile
	echo "# this is the second comment" >> basefile
	echo "# " >> basefile
	echo "VAR_2=94" >> basefile
	echo "#" > addfile
	echo "VAR_1='true'" >> addfile
	echo "#" >> addfile
	echo "VAR_2" >> addfile
	$(TESTOBJ) -r -i basefile addfile outfile
	-diff outfile $(REF)/TestBugzilla24540.txt > TestDifference.txt
	./Evaluate Bugzilla24540
	-diff basefile.new $(REF)/TestBugzilla24540.new.txt > TestDifference.txt
	./Evaluate Bugzilla24540
	@echo "---------------------------"



TestBugzilla30279: fillup
	@echo "---------------------------"
	cp Bugzilla30279/basefile .
	cp Bugzilla30279/addfile .
	$(TESTOBJ) -q basefile addfile outfile
	-diff -B outfile basefile > TestDifference.txt
	./Evaluate Bugzilla30279
	@echo "---------------------------"




fillup: ;
	make -C ../../SRC clean
	make -C ../../SRC all
	mv ../../BIN/fillup $(TESTOBJ)

clean:
	rm -f authors.*
	rm -f addfile outfile basefile*
	rm -rf DIFFERENCE/*

