Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:       cldr-emoji-annotation
Version:    37.0_13.0_0_1
Release:    2%{?dist}
# Annotation files are in Unicode license
Summary:    Emoji annotation files in CLDR
License:    LGPLv2+ and Unicode
URL:        https://github.com/fujiwarat/cldr-emoji-annotation
Source0:    https://github.com/fujiwarat/cldr-emoji-annotation/releases/download/%{version}/%{name}-%{version}.tar.gz
#Patch0:     %%{name}-HEAD.patch
BuildRequires: autoconf
BuildRequires: automake
BuildArch:  noarch

%description
This package provides the emoji annotation file by language in CLDR.

%package devel
Summary:    Files for development using cldr-annotations
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig
BuildArch:  noarch

%description devel
This package contains the pkg-config files for development
when building programs that use cldr-annotations.


%prep
%autosetup

%build
#autoreconf -v -i
autoreconf -v -i
%configure
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install INSTALL="install -p"

%files
%doc AUTHORS README
%license unicode-license.txt
%{_datadir}/unicode/

%files devel
%{_datadir}/pkgconfig/*.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 37.0_13.0_0_1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jun 26 2020 Takao Fujiwara <tfujiwar@gmail.com> - 37.0_13.0_0_1-1
- Integrated Emoji 13.0 CLDR 37.0

* Wed Apr 22 2020 Takao Fujiwara <tfujiwar@gmail.com> - 36.12.120200305_0-1
- Integrated Emoji 12.1 CLDR 36.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 36.12.120191002_0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 25 2019 Takao Fujiwara <tfujiwar@gmail.com> - 36.12.120191002_0-1
- Integrated Emoji 12.1 CLDR 36

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 35.12.14971_0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 04 2019 Takao Fujiwara <tfujiwar@gmail.com> - 35.12.14971_0-1
- Integrated release-35

* Tue Feb 26 2019 Takao Fujiwara <tfujiwar@gmail.com> - 34.12.14891_0-1
- Integrated release-35-alpha2

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 33.1.0_0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 33.1.0_0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Takao Fujiwara <tfujiwar@gmail.com> - 33.1.0_0-1
- Integrated release 33-1

* Wed Jun 20 2018 Takao Fujiwara <tfujiwar@gmail.com> - 33.0.0_2-1
- Changed COPYING

* Thu Apr 12 2018 Takao Fujiwara <tfujiwar@gmail.com> - 33.0.0_1-1
- Integrated release 33

* Fri Mar 09 2018 Takao Fujiwara <tfujiwar@gmail.com> - 32.90.0_1-2
- Removed gcc dependency

* Wed Mar 07 2018 Takao Fujiwara <tfujiwar@gmail.com> - 32.90.0_1-1
- Integrated release-33-alpha

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 32.0.0_1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Takao Fujiwara <tfujiwar@gmail.com> - 32.0.0_1-1
- Integrated release 32

* Thu Sep 28 2017 Takao Fujiwara <tfujiwar@gmail.com> - 31.90.0_1-1
- Integrated release-32-alpha

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 31.0.1_1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 21 2017 Takao Fujiwara <tfujiwar@gmail.com> - 31.0.1_1-1
- Integrated release-31.0.1

* Wed Mar 22 2017 Takao Fujiwara <tfujiwar@gmail.com> - 31.0.0_1-1
- Integrated release-31

* Mon Mar 06 2017 Takao Fujiwara <tfujiwar@gmail.com> - 30.0.3_2-1
- Initial implementation
