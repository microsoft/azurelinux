
testsequence: parameter replacement metadata getvariable shiftregister
	@echo ""
	@echo "If diff subdirectores are empty the test has been successful"
	@echo ""
	ls -al */DIFF*
	@echo ""
	@cat */DIFF*/*.txt 2>/dev/null || echo "done"


parameter:
	make -C PARAMETERS

replacement:
	make -C REPLACEMENT

metadata:
	make -C METADATA

getvariable:
	make -C GETVARIABLE

shiftregister:
	make -C FCSR

clean:
	rm -rf ./fillup
	make -C PARAMETERS clean
	make -C REPLACEMENT clean
	make -C METADATA clean
	make -C GETVARIABLE clean
	make -C FCSR clean

