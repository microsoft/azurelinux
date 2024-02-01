Summary:        Compact text-to-speech synthesizer
Name:           espeak-ng
Version:        1.51.1
Release:        1%{?dist}
# Apache2 license applies only to Android APK code- does not apply here
# BSD license applies only to Windows code- does not apply here
License:        GPLv3 AND Unicode
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/espeak-ng/espeak-ng
Source0:        https://github.com/%{name}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz#/%{name}-%{version}.tgz
Patch0:         espeak-ng-1.51-CVE-2023-49990-4.patch
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pcaudiolib-devel
BuildRequires:  pkg-config
BuildRequires:  which
Requires:       pcaudiolib

%description
The eSpeak NG is a compact open source software text-to-speech synthesizer for Linux.

%package devel
Summary:        Libraries and header files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Libraries and header files for %{name}

%package vim
Summary:        Vim syntax highlighting for espeak-ng data files
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description vim
%{summary}.

%prep
%autosetup -p1
# Remove unused files to make sure we've got the License tag right
rm -rf src/include/compat/endian.h src/compat/getopt.c android/

%build
./autogen.sh
%configure --without-sonic
%make_build src/espeak-ng src/speak-ng
%make_build

%install
%make_install
rm -vf %{buildroot}%{_libdir}/libespeak-ng-test.so*
rm -vf %{buildroot}%{_libdir}/*.{a,la}
# Remove files conflicting with espeak
rm -vf %{buildroot}%{_bindir}/{speak,espeak}
rm -vrf %{buildroot}%{_includedir}/espeak
# Move Vim files
mv %{buildroot}%{_datadir}/vim/addons %{buildroot}%{_datadir}/vim/vimfiles
rm -vrf %{buildroot}%{_datadir}/vim/registry

%check
%make_build check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%license COPYING
%license COPYING.APACHE
%license COPYING.BSD2
%license COPYING.UCD
%doc README.md
%doc CHANGELOG.md
%{_bindir}/speak-ng
%{_bindir}/espeak-ng
%{_libdir}/libespeak-ng.so.1
%{_libdir}/libespeak-ng.so.1.*
%{_datadir}/espeak-ng-data

%files devel
%{_libdir}/pkgconfig/espeak-ng.pc
%{_libdir}/libespeak-ng.so
%{_includedir}/espeak-ng

%files vim
%{_datadir}/vim/vimfiles/ftdetect/espeakfiletype.vim
%{_datadir}/vim/vimfiles/syntax/espeaklist.vim
%{_datadir}/vim/vimfiles/syntax/espeakrules.vim

%changelog
* Wed Jan 31 2024 Sumedh Sharma <sumsharma@microsoft.com> - 1.51.1-1
- Bump package version to 1.51.1
- move vim specific builds to sub-package 'vim'
- remove unneeded patch files

* Mon May 10 2021 Thomas Crain <thcrain@microsoft.com> - 1.50-3
- Rename "Mr serious" voice to "Mr_serious"

* Fri Mar 05 2021 Thomas Crain <thcrain@microsoft.com> - 1.50-2
- Add tests-fix-greek-letter-variants.patch to address failing test
- Adjust tests-newline-fixes.patch to account for new patch

* Fri Feb 05 2021 Thomas Crain <thcrain@microsoft.com> - 1.50-1
- Original version for CBL-Mariner (license: MIT)
- License verified
