
TESTOBJ=../fillup
STUBS=../STUBS
REF=./REFERENCE
OUT=./OUT
DIF=./DIFFERENCE

Test:	fillup io-files Test1 Test2
	@echo ""
	@echo "If subdirectory $(DIF) is empty the test has been successful"
	@echo ""
	ls -al $(DIF)
	@echo ""

Test1:	Test100

Test2:	Test201 Test202 Test203 Test204 Test205 Test206 Test207 Test208 Test209 Test210 \
	Test211 Test212 Test213 Test214 Test215 Test216 Test217 Test218 Test219 \
	Test231 Test232 Test233 Test234 Test235 Test236 Test237 Test238 Test239 Test240 \
	Test241 Test242 Test243 Test244 Test245 Test246 Test247 Test248 Test249 \
	Test250

Test100: 
	@echo "---------------------------"
	$(TESTOBJ) infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test100.txt
	-diff $(REF)/Test100.txt Test.txt > TestDifference.txt
	./Evaluate 100
	rm -f Test.txt
	@echo "---------------------------"

Test201: 
	@echo "---------------------------"
	$(TESTOBJ) -h infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test201.txt
	-diff $(REF)/Test201.txt Test.txt > TestDifference.txt
	./Evaluate 201
	rm -f Test.txt
	@echo "---------------------------"

Test202: 
	@echo "---------------------------"
	$(TESTOBJ) -a -e infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test202.txt
	-diff $(REF)/Test202.txt Test.txt > TestDifference.txt
	./Evaluate 202
	rm -f Test.txt
	@echo "---------------------------"

Test203: 
	@echo "---------------------------"
	$(TESTOBJ) -a -q infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test203.txt
	-diff $(REF)/Test203.txt Test.txt > TestDifference.txt
	./Evaluate 203
	rm -f Test.txt
	@echo "---------------------------"

Test204: 
	@echo "---------------------------"
	$(TESTOBJ) -a -s infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test204.txt
	-diff $(REF)/Test204.txt Test.txt > TestDifference.txt
	./Evaluate 204
	rm -f Test.txt
	@echo "---------------------------"

Test205: 
	@echo "---------------------------"
	$(TESTOBJ) -a -t infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test205.txt
	-diff $(REF)/Test205.txt Test.txt > TestDifference.txt
	./Evaluate 205
	rm -f Test.txt
	@echo "---------------------------"

Test206: 
	@echo "---------------------------"
	$(TESTOBJ) -a -v infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test206.txt
	-diff $(REF)/Test206.txt Test.txt > TestDifference.txt
	./Evaluate 206
	rm -f Test.txt
	@echo "---------------------------"

Test207: 
	@echo "---------------------------"
	$(TESTOBJ) -V infile addfile outfile 2> Test.txt
	cat Test.txt | grep -v "compiled" > $(OUT)/Test207.txt
	-diff $(REF)/Test207.txt $(OUT)/Test207.txt > TestDifference.txt
	./Evaluate 207
	rm -f Test.txt
	@echo "---------------------------"

Test208: 
	@echo "---------------------------"
	$(TESTOBJ) -a -c "##;" infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test208.txt
	-diff $(REF)/Test208.txt Test.txt > TestDifference.txt
	./Evaluate 208
	rm -f Test.txt
	@echo "---------------------------"

Test209: 
	@echo "---------------------------"
	$(TESTOBJ) -a -d ":" infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test209.txt
	-diff $(REF)/Test209.txt Test.txt > TestDifference.txt
	./Evaluate 209
	rm -f Test.txt
	@echo "---------------------------"

Test210: 
	@echo "---------------------------"
	$(TESTOBJ) -a -n 20 infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test210.txt
	-diff $(REF)/Test210.txt Test.txt > TestDifference.txt
	./Evaluate 210
	rm -f Test.txt
	@echo "---------------------------"

Test211: 
	@echo "---------------------------"
	$(TESTOBJ) -a -p infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test211.txt
	-diff $(REF)/Test211.txt Test.txt > TestDifference.txt
	./Evaluate 211
	rm -f Test.txt
	@echo "---------------------------"

Test212: 
	@echo "---------------------------"
	$(TESTOBJ) -a -g infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test212.txt
	-diff $(REF)/Test212.txt Test.txt > TestDifference.txt
	./Evaluate 212
	rm -f Test.txt
	@echo "---------------------------"

Test213: 
	@echo "---------------------------"
	$(TESTOBJ) -a -m infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test213.txt
	-diff $(REF)/Test213.txt Test.txt > TestDifference.txt
	./Evaluate 213
	rm -f Test.txt
	@echo "---------------------------"

Test214: 
	@echo "---------------------------"
	$(TESTOBJ) -a -x infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test214.txt
	-diff $(REF)/Test214.txt Test.txt > TestDifference.txt
	./Evaluate 214
	rm -f Test.txt
	@echo "---------------------------"

Test215: 
	@echo "---------------------------"
	$(TESTOBJ) -a -r infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test215.txt
	-diff $(REF)/Test215.txt Test.txt > TestDifference.txt
	./Evaluate 215
	rm -f Test.txt
	@echo "---------------------------"

Test216: 
	@echo "---------------------------"
	$(TESTOBJ) -a infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test216.txt
	-diff $(REF)/Test216.txt Test.txt > TestDifference.txt
	./Evaluate 216
	rm -f Test.txt
	@echo "---------------------------"

Test217: 
	@echo "---------------------------"
	$(TESTOBJ) -a -l "\"" infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test217.txt
	-diff $(REF)/Test217.txt Test.txt > TestDifference.txt
	./Evaluate 217
	rm -f Test.txt
	@echo "---------------------------"

Test218: 
	@echo "---------------------------"
	$(TESTOBJ) -a -f "DontChangeTheseVariables.Info" infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test218.txt
	-diff $(REF)/Test218.txt Test.txt > TestDifference.txt
	./Evaluate 218
	rm -f Test.txt
	@echo "---------------------------"

Test219: 
	@echo "---------------------------"
	$(TESTOBJ) -a -i infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test219.txt
	-diff $(REF)/Test219.txt Test.txt > TestDifference.txt
	./Evaluate 219
	rm -f Test.txt
	@echo "---------------------------"


Test231: 
	@echo "---------------------------"
	$(TESTOBJ) --help infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test231.txt
	-diff $(REF)/Test231.txt Test.txt > TestDifference.txt
	./Evaluate 231
	rm -f Test.txt
	@echo "---------------------------"

Test232: 
	@echo "---------------------------"
	$(TESTOBJ) -a --ignoreeof infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test232.txt
	-diff $(REF)/Test232.txt Test.txt > TestDifference.txt
	./Evaluate 232
	rm -f Test.txt
	@echo "---------------------------"

Test233: 
	@echo "---------------------------"
	$(TESTOBJ) -a --quiet infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test233.txt
	-diff $(REF)/Test233.txt Test.txt > TestDifference.txt
	./Evaluate 233
	rm -f Test.txt
	@echo "---------------------------"

Test234: 
	@echo "---------------------------"
	$(TESTOBJ) --arguments --suppress infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test234.txt
	-diff $(REF)/Test234.txt Test.txt > TestDifference.txt
	./Evaluate 234
	rm -f Test.txt
	@echo "---------------------------"

Test235: 
	@echo "---------------------------"
	$(TESTOBJ) -a --trailing infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test235.txt
	-diff $(REF)/Test235.txt Test.txt > TestDifference.txt
	./Evaluate 235
	rm -f Test.txt
	@echo "---------------------------"

Test236: 
	@echo "---------------------------"
	$(TESTOBJ) --arguments --verbose infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test236.txt
	-diff $(REF)/Test236.txt Test.txt > TestDifference.txt
	./Evaluate 236
	rm -f Test.txt
	@echo "---------------------------"

Test237: 
	@echo "---------------------------"
	$(TESTOBJ) --version infile addfile outfile 2> Test.txt
	cat Test.txt | grep -v "compiled" > $(OUT)/Test237.txt
	-diff $(REF)/Test237.txt $(OUT)/Test237.txt > TestDifference.txt
	./Evaluate 237
	rm -f Test.txt
	@echo "---------------------------"

Test238: 
	@echo "---------------------------"
	$(TESTOBJ) -a --char "##;" infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test238.txt
	-diff $(REF)/Test238.txt Test.txt > TestDifference.txt
	./Evaluate 238
	rm -f Test.txt
	@echo "---------------------------"

Test239: 
	@echo "---------------------------"
	$(TESTOBJ) -a --delim ":" infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test239.txt
	-diff $(REF)/Test239.txt Test.txt > TestDifference.txt
	./Evaluate 239
	rm -f Test.txt
	@echo "---------------------------"

Test240: 
	@echo "---------------------------"
	$(TESTOBJ) -a --num 20 infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test240.txt
	-diff $(REF)/Test240.txt Test.txt > TestDifference.txt
	./Evaluate 240
	rm -f Test.txt
	@echo "---------------------------"

Test241: 
	@echo "---------------------------"
	$(TESTOBJ) -a --put infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test241.txt
	-diff $(REF)/Test241.txt Test.txt > TestDifference.txt
	./Evaluate 241
	rm -f Test.txt
	@echo "---------------------------"

Test242: 
	@echo "---------------------------"
	$(TESTOBJ) -a --get infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test242.txt
	-diff $(REF)/Test242.txt Test.txt > TestDifference.txt
	./Evaluate 242
	rm -f Test.txt
	@echo "---------------------------"

Test243: 
	@echo "---------------------------"
	$(TESTOBJ) -a --maintain infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test243.txt
	-diff $(REF)/Test243.txt Test.txt > TestDifference.txt
	./Evaluate 243
	rm -f Test.txt
	@echo "---------------------------"

Test244: 
	@echo "---------------------------"
	$(TESTOBJ) -a --exchange infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test244.txt
	-diff $(REF)/Test244.txt Test.txt > TestDifference.txt
	./Evaluate 244
	rm -f Test.txt
	@echo "---------------------------"

Test245: 
	@echo "---------------------------"
	$(TESTOBJ) -a --remove infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test245.txt
	-diff $(REF)/Test245.txt Test.txt > TestDifference.txt
	./Evaluate 245
	rm -f Test.txt
	@echo "---------------------------"

Test246: 
	@echo "---------------------------"
	$(TESTOBJ) --arguments infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test246.txt
	-diff $(REF)/Test246.txt Test.txt > TestDifference.txt
	./Evaluate 246
	rm -f Test.txt
	@echo "---------------------------"

Test247: 
	@echo "---------------------------"
	$(TESTOBJ) --arguments --quote "\"" infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test247.txt
	-diff $(REF)/Test247.txt Test.txt > TestDifference.txt
	./Evaluate 247
	rm -f Test.txt
	@echo "---------------------------"

Test248: 
	@echo "---------------------------"
	$(TESTOBJ) --arguments --forbidden "DontChangeTheseVariables.Info" infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test248.txt
	-diff $(REF)/Test248.txt Test.txt > TestDifference.txt
	./Evaluate 248
	rm -f Test.txt
	@echo "---------------------------"

Test249: 
	@echo "---------------------------"
	$(TESTOBJ) --arguments --ignoreDefinites infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test249.txt
	-diff $(REF)/Test249.txt Test.txt > TestDifference.txt
	./Evaluate 249
	rm -f Test.txt
	@echo "---------------------------"


Test250: 
	@echo "---------------------------"
	$(TESTOBJ) --arguments -n 40 --char "###" -t --remove \
                   infile addfile outfile 2> Test.txt
	cp Test.txt $(OUT)/Test250.txt
	-diff $(REF)/Test250.txt Test.txt > TestDifference.txt
	./Evaluate 250
	rm -f Test.txt
	@echo "---------------------------"




fillup: 
	make -C ../../SRC clean
	make -C ../../SRC all
	mv ../../BIN/fillup $(TESTOBJ)

io-files:
	echo " " > infile
	echo " " > addfile

clean:
	rm -rf DIFFERENCE/*
	rm -rf infile addfile outfile infile.new

