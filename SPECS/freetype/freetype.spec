Summary:        software font engine.
Name:           freetype
Version:        2.13.2
Release:        1%{?dist}
License:        BSD/GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.freetype.org/
Source0:        https://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.gz
Source1:        https://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.gz
BuildRequires:  brotli-devel
BuildRequires:  bzip2-devel
BuildRequires:  gcc
BuildRequires:  libpng-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  zlib-devel

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.

%package        devel
Summary:        Header and development files
Requires:       freetype = %{version}-%{release}

%description	devel
The freetype-devel package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-devel if you want to develop programs which will use
FreeType.

%prep
%autosetup -p1

%build
./configure                  \
	--prefix=%{_prefix}      \
	--with-harfbuzz=no       \
	--disable-static         \
    --with-zlib=yes          \
    --with-bzip2=yes         \
    --with-png=yes           \
	--enable-freetype-config \
	--with-brotli=yes
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -name '*.a' -delete

mkdir -p %{buildroot}%{_datadir}/licenses/freetype
cp LICENSE.TXT %{buildroot}%{_datadir}/licenses/freetype
cp -r docs/* %{buildroot}%{_datadir}/licenses/freetype

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license docs/LICENSE.TXT
%{_libdir}/*.so*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_bindir}/freetype-config

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.2-1
- Auto-upgrade to 2.13.2 - Azure Linux 3.0 - package upgrades

* Mon May 08 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-1
- Auto-upgrade to 2.13.0 - to fix CVE-2023-2004

* Wed Aug 10 2022 Muhammad Falak <mwani@microsoft.com> - 2.12.1-1
- Bump verison to address CVE-2022-27405

* Mon May 16 2022 Chris Co <chrco@microsoft.com> - 2.11.1-2
- Address CVE-2022-27404
- Fix lint

* Tue Feb 08 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.11.1-1
- Update source to 2.11.1
- Add freetype-docs source (2.11.1), same license
- Manually copy over docs (make install doesn't handle it for us?)
- License verified

* Thu Mar 25 2021 Henry Li <lihl@microsoft.com> - 2.9.1-5
- Add enable-fretype-config to configuration
- Add /usr/bin/freetype-config to freetype-devel

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.9.1-4
- Added %%license line automatically

* Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.9.1-3
- Rename freetype2 to freetype.
- Update URL.
- Remove sha1 macro.
- Update Source0.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.9.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 12 2018 Sujay G <gsujay@vmware.com> 2.9.1-1
- version bump to 2.9.1

* Thu Jun 14 2018 Tapas Kundu <tkundu@vmware.com> 2.7.1-4
- CVE-2018-6942

* Mon May 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.1-3
- CVE-2017-8287

* Fri Apr 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.1-2
- CVE-2017-7857, CVE-2017-7858 and CVE-2017-7864

* Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.7.1-1
- Initial version
