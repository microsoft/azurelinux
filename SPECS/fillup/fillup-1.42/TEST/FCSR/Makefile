
TESTOBJ=../fillup
REF=./REFERENCE
OUT=./OUT
DIF=./DIFFERENCE


all:	./CreateBasefile ./CreateAddfile ./CreateOutfile ./CreateRemoved \
	nometadata Test833232 Test601270 Test447307 Test215341
	@echo ""
	@echo "If subdirectory $(DIF) is empty the test has been successful"
	@echo ""
	ls -al $(DIF)
	@echo ""

nometadata: Test0 Test1 Test2 Test3

Test0: fillup
	./CallSequence $(TESTOBJ) 0
	@echo "---------------------------"
	-diff -B outfile ref-outfile > TestDifference.txt
	./Evaluate 0
	@echo "---------------------------"

Test1: fillup
	./CallSequence $(TESTOBJ) 1 "-x"
	@echo "---------------------------"
	-diff -B outfile ref-outfile > TestDifference.txt
	./Evaluate 1
	@echo "---------------------------"

Test2: fillup
	./CallSequence $(TESTOBJ) 2 "-r"
	@echo "---------------------------"
	-diff -B outfile ref-outfile > TestDifference.txt
	./Evaluate 2
	-diff -B basefile.new ref-removed >> TestDifference.txt
	./Evaluate 2
	@echo "---------------------------"

Test3: fillup
	./CallSequence $(TESTOBJ) 3 "-x -r"
	@echo "---------------------------"
	-diff -B outfile ref-outfile > TestDifference.txt
	./Evaluate 3
	-diff -B basefile.new ref-removed >> TestDifference.txt
	./Evaluate 3
	@echo "---------------------------"


Test833232: fillup
	./CallSequence $(TESTOBJ) 833232 ""
	@echo "---------------------------"
	-diff -B outfile ref-outfile > TestDifference.txt
	./Evaluate 833232
	@echo "---------------------------"

Test601270: fillup
	./CallSequence $(TESTOBJ) 601270 "-r"
	@echo "---------------------------"
	-diff -B outfile ref-outfile > TestDifference.txt
	./Evaluate 601270
	-diff -B basefile.new ref-removed >> TestDifference.txt
	./Evaluate 601270
	@echo "---------------------------"

Test447307: fillup
	./CallSequence $(TESTOBJ) 447307 "-x -r"
	@echo "---------------------------"
	-diff -B outfile ref-outfile > TestDifference.txt
	./Evaluate 447307
	-diff -B basefile.new ref-removed >> TestDifference.txt
	./Evaluate 447307
	@echo "---------------------------"

Test215341: fillup
	./CallSequence $(TESTOBJ) 215341 "-x"
	@echo "---------------------------"
	-diff -B outfile ref-outfile > TestDifference.txt
	./Evaluate 215341
	@echo "---------------------------"




./CreateBasefile:
	gcc SRC/CreateBasefile.c -o ./CreateBasefile

./CreateAddfile:
	gcc SRC/CreateAddfile.c -o ./CreateAddfile

./CreateOutfile:
	gcc SRC/CreateOutfile.c -o ./CreateOutfile

./CreateRemoved:
	gcc SRC/CreateRemoved.c -o ./CreateRemoved


fillup:
	make -C ../../SRC clean
	make -C ../../SRC all
	mv ../../BIN/fillup $(TESTOBJ)

clean:
	rm -rf DIFFERENCE/*
	rm -f basefile basefile.new addfile outfile ref-outfile ref-removed
	rm -f Create*

