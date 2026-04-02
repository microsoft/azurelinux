# This spec file has been modified by azldev to include build configuration overlays. Version: v0.1.1-0.20260402002340-3dc8b8a0f4b6
# Do not edit manually; changes may be overwritten.

Summary: Dictionary of English words for the /usr/share/dict directory
Name: words
Version: 3.0
Release: %autorelease

# https://gitlab.com/fedora/legal/fedora-license-data/-/commit/1fe1c5769b177e00749a324557f6631a964770b1
License: LicenseRef-Fedora-Public-Domain

# Note that Moby Project officially does not exist any more. The most complete
# information about the project is in Wikipedia.
URL: https://en.wikipedia.org/wiki/Moby_Project
Source: https://web.archive.org/web/20060527013227/http://www.dcs.shef.ac.uk/research/ilash/Moby/mwords.tar.Z

BuildArch: noarch
BuildRequires: dos2unix
BuildRequires: grep

#428582 - linux.words contains misspelled word "flourescent"
#440146 - misspelled word in /usr/share/dict/words (architecure)
#457309 - contains both 'unnecessary' and 'unneccesary'
#1626689 - linux.words contains "half-embracinghalf-embracingly"
#1652919 - malformed entry in words file
#2294822 - Misspelled words in /usr/share/dict/words
Patch0: words-3.0-typos.patch
#470921 -"Barack" and "Obama" are not in /usr/share/dict/words
Patch1: words-3.0-presidents.patch

%description
The words file is a dictionary of English words for the
/usr/share/dict directory. Some programs use this database of
words to check spelling. Password checkers use it to look for bad
passwords.

%prep
%autosetup -p1 -n mwords

%build
dos2unix -o *; chmod a+r *
cat [1-9]*.??? | grep -E --invert-match "'s$" | grep -E "^[[:alnum:]'&!,./-]+$" | sort --ignore-case --dictionary-order | uniq > moby

cat <<EOF >license.txt
***
    The license in the readme.txt file is original and DEPRECATED
    license of The Moby lexicon project.
***

On June 1, 1996 Grady Ward announced that the fruits of
the Moby project were being placed in the public domain:

The Moby lexicon project is complete and has
been place into the public domain. Use, sell,
rework, excerpt and use in any way on any platform.

Placing this material on internal or public servers is
also encouraged. The compiler is not aware of any
export restrictions so freely distribute world-wide.

You can verify the public domain status by contacting

Grady Ward
3449 Martha Ct.
Arcata, CA  95521-4884

daedal@myrealbox.com
EOF

%install
install -D -m644 moby $RPM_BUILD_ROOT%{_datadir}/dict/linux.words
ln -sf linux.words $RPM_BUILD_ROOT%{_datadir}/dict/words

%files
%license license.txt
%doc readme.txt
%{_datadir}/dict/linux.words
%{_datadir}/dict/words

%changelog
%autochangelog
