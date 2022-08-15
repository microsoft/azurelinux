#!/bin/bash

function usage() { 
    echo "Place a new dummy spec" 
    echo "n : name of new package (ex. cowz)" 
    echo "s : sleep duration in seconds for %build step (ex. 2)"
    exit 1 
}

while getopts "n:s:" OPTIONS; do
  case "${OPTIONS}" in
    n ) NAME=$OPTARG ;;
    s ) SLEEP_DUR=$OPTARG ;;
    * ) usage 
        ;;
  esac
done

if [[ -z $NAME ]]; then
    echo "Missing -n"
    usage
fi

if [[ -z $SLEEP_DUR ]]; then
    echo "Setting SLEEP_DUR=1 by default"
    SLEEP_DUR=1
fi

cp -r cowz $NAME 
sed -i "s/Name:\x20*cowz/Name:           ${NAME}/g" ${NAME}/cowz.spec
sed -i "s/sleep 2/sleep ${SLEEP_DUR}/g" ${NAME}/cowz.spec
mv ${NAME}/cowz.spec ${NAME}/${NAME}.spec
mv ${NAME}/cowz.signatures.json ${NAME}/${NAME}.signatures.json
code ${NAME}/${NAME}.spec