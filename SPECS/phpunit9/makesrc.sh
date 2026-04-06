#!/bin/bash

NAME=$(basename $PWD)
DATE=$(sed    -n '/^%global gh_date/{s/.* //;p}'    $NAME.spec)
OWNER=$(sed   -n '/^%global gh_owner/{s/.* //;p}'   $NAME.spec)
PROJECT=$(sed -n '/^%global gh_project/{s/.* //;p}' $NAME.spec)
VERSION=$(sed -n '/^%global upstream_version/{s/.* //;p}' $NAME.spec)
COMMIT=$(sed  -n '/^%global gh_commit/{s/.* //;p}'  $NAME.spec)
SHORT=${COMMIT:0:7}

DATE=$(date -d "$DATE -4 days" +%Y-%m-%d)

if [ -f $NAME-$VERSION-$SHORT.tgz ]; then
	echo "$NAME-$VERSION-$SHORT.tgz already there"
else
	echo -e "\nCreate git snapshot\nName=$NAME, Owner=$OWNER, Project=$PROJECT, Version=$VERSION, Date=$DATE\n"

	echo "Cloning..."
	rm -rf $PROJECT-$COMMIT
	git clone https://github.com/$OWNER/$PROJECT.git $PROJECT-$COMMIT || exit 1

	echo "Getting commit..."
	pushd $PROJECT-$COMMIT
		git checkout $COMMIT || exit 1
		cp composer.json ../composer.json
	popd

	echo "Archiving..."
	tar czf $NAME-$VERSION-$SHORT.tgz --exclude-vcs --exclude tools $PROJECT-$COMMIT

	echo "Cleaning..."
	rm -rf $PROJECT-$COMMIT

	echo "Done."
fi
