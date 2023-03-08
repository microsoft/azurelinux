Summary:        software font engine.
Name:           freetype
Version:        2.12.1
Release:        2%{?dist}
License:        BSD WITH advertising OR GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.freetype.org/
Source0:        https://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  libtool
BuildRequires:  zlib-devel

%description
FreeType is a software font engine that is designed to be small, efficient, highly customizable, and portable while capable of producing high-quality output (glyph images). It can be used in graphics libraries, display servers, font conversion tools, text image generation tools, and many other products as well.

%package   devel
Summary:        Header and development files
Requires:       freetype = %{version}-%{release}

%description   devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
./configure \
   --prefix=%{_prefix} \
   --with-harfbuzz=no
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -name '*.a' -delete

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE.TXT docs/FTL.TXT docs/GPLv2.TXT
%{_libdir}/*.so*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Feb 28 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 2.12.1-2
- Bump release number due to harfbuzz upgrade to fix CVE-2023-25193.

* Thu Aug 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.12.1-1
- Updating to version 2.12.1 to address CVEs: 2022-27405 and 2022-27406.

* Mon May 16 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.11.1-2
- Add patch to address CVE-2022-27404.

* Mon Mar 07 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.11.1-1
- Updating to version 2.11.1 to address CVE-2020-15999.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.9.1-4
- Added %%license line automatically

* Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.9.1-3
- Rename freetype2 to freetype.
- Update URL.
- Remove sha1 macro.
- Update Source0.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.9.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 12 2018 Sujay G <gsujay@vmware.com> - 2.9.1-1
- version bump to 2.9.1

* Thu Jun 14 2018 Tapas Kundu <tkundu@vmware.com> - 2.7.1-4
- CVE-2018-6942

* Mon May 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.7.1-3
- CVE-2017-8287

* Fri Apr 28 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.7.1-2
- CVE-2017-7857, CVE-2017-7858 and CVE-2017-7864

* Fri Nov 11 2016 Dheeraj Shetty <dheerajs@vmware.com> - 2.7.1-1
- Initial version
