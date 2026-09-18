#!/bin/bash

NAME=$(basename $PWD)
OWNER=$(sed   -n '/^%global gh_owner/{s/.* //;p}'   $NAME.spec)
PROJECT=$(sed -n '/^%global gh_project/{s/.* //;p}' $NAME.spec)
VERSION=$(sed -n '/^Version:/{s/.* //;p}'           $NAME.spec)

if [ -f $NAME-$VERSION.tgz ]; then
	echo "$NAME-$VERSION.tgz already there"
else
	echo -e "\nCreate git snapshot\nName=$NAME, Owner=$OWNER, Project=$PROJECT, Version=$VERSION	\n"

	echo "Cloning..."
	rm -rf $PROJECT-$VERSION
	git clone https://github.com/$OWNER/$PROJECT.git --depth 1 --branch v$VERSION $PROJECT-$VERSION || exit 1

	echo "Getting composer..."
	cp $PROJECT-$VERSION/composer.json composer.json

	echo "Archiving..."
	tar czf $NAME-$VERSION.tgz --exclude-vcs --exclude tools $PROJECT-$VERSION

	echo "Cleaning..."
	rm -rf $PROJECT-$VERSION

	echo "Done."
fi
