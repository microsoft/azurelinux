#!/bin/bash

NAME=$(basename $PWD)
OWNER=$(sed   -n '/^%global gh_owner/{s/.* //;p}'   $NAME.spec)
PROJECT=$(sed -n '/^%global gh_project/{s/.* //;p}' $NAME.spec)
VERSION=$(sed -n '/^Version:/{s/.* //;p}'           $NAME.spec)
COMMIT=$(sed  -n '/^%global gh_commit/{s/.* //;p}'  $NAME.spec)
SHORT=${COMMIT:0:7}

if [ -f $NAME-$VERSION-$SHORT.tgz ]; then
	echo Skip $NAME-$VERSION-$SHORT.tgz
else
	echo -e "\nCreate git snapshot\nName=$NAME, Owner=$OWNER, Project=$PROJECT, Version=$VERSION\n"

	echo "Cloning..."
	rm -rf $PROJECT-$COMMIT
	git clone https://github.com/$OWNER/$PROJECT.git $PROJECT-$COMMIT

	echo "Getting commit..."
	pushd $PROJECT-$COMMIT
		git checkout $COMMIT || exit 1
		cp composer.json ../composer.json
		rm build-abnfgen.sh
		rm tests/abnfgen-0.20.tar.gz
	popd

	echo "Archiving..."
	tar czf $NAME-$VERSION-$SHORT.tgz --exclude .git $PROJECT-$COMMIT

	echo "Cleaning..."
	rm -rf $PROJECT-$COMMIT

	echo "Done."
fi
