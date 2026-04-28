#!/bin/bash

NODE_BIN="$1"
PARENT_TEST_FOLDER="$2"
TEST_LIST_FILE="$3"

# At most 10 min per test
TIMEOUT_DURATION=600
# Exit code
FINAL_RESULT=0
ARCH=$(uname -m)
PARARALLEL_TEST_RERUN=""
echo "Started test run:"
# Run the list of test
while IFS= read -r test_line; do
  # ignore commented lines
  if [[ "$test_line" =~ ^# ]]; then
    continue
  fi
  # If test has specified ARCH which it should be skipped
  # Extract it
  TEST_PATH=$(echo "$test_line" | awk '{print $1}')
  IGNORE_ARCHES=$(echo "$test_line" |\
    awk '{for (i=2; i<=NF; i++) printf "%s ", $i; print ""}')

  # Skip test for specified ARCH
  for ARCH_IGNORE in $IGNORE_ARCHES; do
    if [[ "$ARCH_IGNORE" == "$ARCH" ]]; then
      echo "Skipping test, current arch is in ignore: $TEST_PATH ($ARCH_IGNORE)"
      continue 2
    fi
  done

  # Construct test path
  TEST_SCRIPT="$PARENT_TEST_FOLDER/$TEST_PATH"

  if [ ! -f "$TEST_SCRIPT" ]; then
    echo "Test script not found: $TEST_SCRIPT"
    continue
  fi

  TEST_OUTPUT=$(timeout "$TIMEOUT_DURATION" "$NODE_BIN" "$TEST_SCRIPT" 2>&1)
  TEST_RESULT=$?

  # Handle test result
  if [ $TEST_RESULT -ne 0 ]; then
    if [[ "$TEST_PATH" == */parallel/* ]]; then
      PARARALLEL_TEST_RERUN+="$TEST_SCRIPT"
      echo "Parallel test failed, marking for rerun: $TEST_SCRIPT"
      continue
    elif [ $TEST_RESULT -eq 124 ]; then
      echo "Test timed out: $TEST_SCRIPT"
    else
      echo "Test failed: $TEST_SCRIPT"
    fi
    FINAL_RESULT=1
    echo "Test failure message:"
    echo "$TEST_OUTPUT"
  fi
done < "$TEST_LIST_FILE"

if [ -n "$PARALLEL_TEST_RERUN" ]; then
  echo "Started rerun for parallel tests:"
  for RERUN_SCRIPT in $PARALLEL_TEST_RERUN; do
    TEST_OUTPUT=$(timeout "$TIMEOUT_DURATION" "$NODE_BIN" "$RERUN_SCRIPT" 2>&1)
    TEST_RESULT=$?
    if [ "$TEST_RESULT" -ne 0 ]; then
      if [ "$TEST_RESULT" -eq 124 ]; then
        echo "Rerun timed out: $RERUN_SCRIPT"
      else
        echo "Rerun failed: $RERUN_SCRIPT"
      fi
      FINAL_RESULT=1
      echo "Rerun failure message:"
      echo "$TEST_OUTPUT"
      echo "---"
    else
      echo "Rerun successful: $RERUN_SCRIPT"
    fi
  done
fi

if [ $FINAL_RESULT -eq 0 ]; then
    echo "All tests succesfully passed."
fi
exit $FINAL_RESULT
