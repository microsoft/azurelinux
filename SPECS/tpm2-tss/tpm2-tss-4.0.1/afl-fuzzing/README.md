 # Usage of AFL Fuzzing for IMA and system events.

* afl++ has to be be installed.
* AFL Fuzzing can be started with the following scripts:
  ```
  $ ./afl-fuzzing/fuzz-system.sh
  $ ./afl-fuzzing/fuzz-ima.sh
  ```
* The results and the files leading to crashes are stored in findings-{ima,system}
* The tests are not integrated into the CI because of the long
  run time
* If crashes are detected the unit tests can be used for debugging
  with the crash file in findings-system/crashes or finding-ima/crashes:
  ```
  $ ./test/unit/fapi-{ima,sysem}-fuzzing <crash-file>
  ```
