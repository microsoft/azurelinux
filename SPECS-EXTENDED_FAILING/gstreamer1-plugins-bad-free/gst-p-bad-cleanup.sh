#!/bin/sh

# Process a gst-plugins-bad tarball to remove
# unwanted GStreamer plugins.
#
# See https://bugzilla.redhat.com/show_bug.cgi?id=532470
# for details
#
# Bastien Nocera <bnocera@redhat.com> - 2010
#

SOURCE="$1"
NEW_SOURCE=`echo $SOURCE | sed 's/bad-/bad-free-/'`
DIRECTORY=`echo $SOURCE | sed 's/\.tar\.xz//'`

ALLOWED="
aacparse
accurip
adpcmdec
adpcmenc
aiff
aiffparse
amrparse
asfmux
audiobuffersplit
audiofxbad
audiolatency
audiomixer
audiomixmatrix
audioparsers
audiovisualizers
autoconvert
bayer
camerabin
camerabin2
cdxaparse
coloreffects
colorspace
compositor
dataurisrc
dccp
debugutils
dtmf
faceoverlay
festival
fieldanalysis
freeverb
freeze
frei0r
gaudieffects
gdp
geometrictransform
h264parse
hdvparse
hls
id3tag
inter
interlace
invtelecine
ivfparse
ivtc
jpegformat
jp2kdecimator
legacyresample
librfb
liveadder
midi
mve
mpegdemux
mpeg4videoparse
mpegpsmux
mpegtsdemux
mpegtsmux
mpegvideoparse
mxf
netsim
nsf
nuvdemux
onvif
patchdetect
pcapparse
pnm
proxy
qtmux
rawparse
removesilence
rtp
rtpmux
rtpvp8
scaletempo
sdi
sdp
segmentclip
selector
smooth
speed
stereo
subenc
timecode
tta
valve
videofilters
videoframe_audiolevel
videomaxrate
videomeasure
videoparsers
videosignal
vmnc
yadif
y4m
"

NOT_ALLOWED="
dvbsuboverlay
dvdspu
real
siren
"

error()
{
	MESSAGE=$1
	echo $MESSAGE
	exit 1
}

check_allowed()
{
	MODULE=$1
	for i in $ALLOWED ; do
		if test x$MODULE = x$i ; then
			return 0;
		fi
	done
	# Ignore errors coming from ext/ directory
	# they require external libraries so are ineffective anyway
	return 1;
}

check_not_allowed()
{
	MODULE=$1
	for i in $NOT_ALLOWED ; do
		if test x$MODULE = x$i ; then
			return 0;
		fi
	done
	return 1;
}

rm -rf $DIRECTORY
tar xJf $SOURCE || error "Cannot unpack $SOURCE"
pushd $DIRECTORY > /dev/null || error "Cannot open directory \"$DIRECTORY\""

unknown=""
for subdir in gst ext sys; do
	for dir in $subdir/* ; do
		# Don't touch non-directories
		if ! [ -d $dir ] ; then
			continue;
		fi
		MODULE=`basename $dir`
		if ( check_not_allowed $MODULE ) ; then
			echo "**** Removing $MODULE ****"
			echo "Removing directory $dir"
			rm -r $dir || error "Cannot remove $dir"
			if grep -q "AG_GST_CHECK_PLUGIN($MODULE)" configure.ac ; then
				echo "Removing element check for $MODULE"
				grep -v "AG_GST_CHECK_PLUGIN($MODULE)" configure.ac > configure.ac.new && mv configure.ac.new configure.ac
			fi
			echo "Removing Makefile generation for $MODULE"
			grep -v "$dir/Makefile" configure.ac > configure.ac.new && mv configure.ac.new configure.ac
			# Urgh
			if test $MODULE = real ; then
				grep -v "AG_GST_DISABLE_PLUGIN(real)" configure.ac > configure.ac.new && mv configure.ac.new configure.ac
			fi
			echo "Removing documentation for $MODULE"
			if grep -q "$MODULE" docs/plugins/Makefile.am ; then
				grep -v $dir docs/plugins/Makefile.am > docs/plugins/Makefile.am.new && mv docs/plugins/Makefile.am.new docs/plugins/Makefile.am
			fi
			echo
		elif test $subdir = ext  || test $subdir = sys; then
			# Ignore library or system non-blacklisted plugins
			continue;
		elif ! ( check_allowed $MODULE ) ; then
			echo "Unknown module in $dir"
			unknown="$unknown $dir"
		fi
	done
done

echo

if test "x$unknown" != "x"; then
  echo -n "Aborting due to unkown modules: "
  echo "$unknown" | sed "s/ /\n  /g"
  exit 1
fi

#autoreconf
NOCONFIGURE=1 \
./autogen.sh

popd > /dev/null

tar cJf $NEW_SOURCE $DIRECTORY
echo "$NEW_SOURCE is ready to use"

