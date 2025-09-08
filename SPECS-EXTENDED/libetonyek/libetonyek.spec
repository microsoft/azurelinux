Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global apiversion 0.1

Name: libetonyek
Version: 0.1.12
Release: 2%{?dist}
Summary: A library for import of Apple iWork documents

License: MPL-2.0
URL: http://wiki.documentfoundation.org/DLP/Libraries/libetonyek
Source: https://dev-www.libreoffice.org/src/%{name}/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: glm-devel
BuildRequires: gperf
BuildRequires: help2man
BuildRequires: make
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(liblangtag)
BuildRequires: pkgconfig(librevenge-0.0)
BuildRequires: pkgconfig(librevenge-generators-0.0)
BuildRequires: pkgconfig(librevenge-stream-0.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(mdds-2.1)
BuildRequires: pkgconfig(zlib)

%description
%{name} is library for import of Apple iWork documents. It supports
documents created by any version of Keynote, Pages or Numbers.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: Documentation of %{name} API
BuildArch: noarch

%description doc
The %{name}-doc package contains documentation files for %{name}.

%package tools
Summary: Tools to transform Apple iWork documents into other formats
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform Apple iWork documents into other formats. Currently
supported: CSV, HTML, SVG, text, and raw.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror --with-mdds=2.1
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
%make_build

%install
%make_install
rm -f %{buildroot}/%{_libdir}/*.la
# we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

# generate and install man pages
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in key2raw key2text key2xhtml numbers2csv numbers2raw numbers2text pages2html pages2raw pages2text; do
    help2man -N -S '%{name} %{version}' -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 key2*.1 numbers2*.1 pages2*.1 %{buildroot}/%{_mandir}/man1

%ldconfig_scriptlets

%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
if ! %make_build check; then
    cat src/test/*.log
    exit 1
fi

%files
%doc AUTHORS FEATURES.md NEWS README.md
%license COPYING
%{_libdir}/%{name}-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files doc
%license COPYING
%doc docs/doxygen/html

%files tools
%{_bindir}/key2raw
%{_bindir}/key2text
%{_bindir}/key2xhtml
%{_bindir}/numbers2csv
%{_bindir}/numbers2raw
%{_bindir}/numbers2text
%{_bindir}/pages2html
%{_bindir}/pages2raw
%{_bindir}/pages2text
%{_mandir}/man1/key2raw.1*
%{_mandir}/man1/key2text.1*
%{_mandir}/man1/key2xhtml.1*
%{_mandir}/man1/numbers2csv.1*
%{_mandir}/man1/numbers2raw.1*
%{_mandir}/man1/numbers2text.1*
%{_mandir}/man1/pages2html.1*
%{_mandir}/man1/pages2raw.1*
%{_mandir}/man1/pages2text.1*

%changelog
* Wed May 07 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.1.12-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Sun Dec 22 2024 David Tardon <dtardon@redhat.com> - 0.1.12-1
- Update to 0.1.12

* Sun Dec 22 2024 David Tardon <dtardon@redhat.com> - 0.1.10-1
- Revert "Update to latest git snapshot"

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.11~20230802.git9c3a8cb-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.11~20230802.git9c3a8cb-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.11~20230802.git9c3a8cb-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 24 2023 Mattia Verga <mattia.verga@proton.me> - 0.1.11~20230802.git9c3a8cb-3
- Change mdds req also in configure parameters

* Thu Aug 24 2023 Mattia Verga <mattia.verga@proton.me> - 0.1.11~20230802.git9c3a8cb-2
- Fix mdds version requirement

* Thu Aug 24 2023 Mattia Verga <mattia.verga@proton.me> - 0.1.11~20230802.git9c3a8cb-1
- Update to latest git snapshot

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 David Tardon <dtardon@redhat.com> - 0.1.10-5
- Convert license to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 18 2021 David Tardon <dtardon@redhat.com> - 0.1.10-1
- new upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 0.1.9-8
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Thu Jun 04 2020 David Tardon <dtardon@redhat.com> - 0.1.9-7
- fix build with latest boost

* Thu Feb 06 2020 Caolán McNamara <caolanm@redhat.com> - 0.1.9-6
- add fix for contemporary glm

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 0.1.9-2
- Rebuilt for Boost 1.69

* Sat Dec 29 2018 David Tardon <dtardon@redhat.com> - 0.1.9-1
- new upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 22 2018 David Tardon <dtardon@redhat.com> - 0.1.8-1
- new upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 0.1.7-2
- Rebuilt for Boost 1.66

* Mon Oct 23 2017 David Tardon <dtardon@redhat.com> - 0.1.7-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 0.1.6-8
- Rebuilt for Boost 1.64

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.1.6-5
- Rebuilt for Boost 1.63

* Sun Feb 14 2016 David Tardon <dtardon@redhat.com> - 0.1.6-4
- switch to mdds 1.x

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.1.6-2
- Rebuilt for Boost 1.60

* Wed Jan 13 2016 David Tardon <dtardon@redhat.com> - 0.1.6-1
- new upstream release

* Thu Dec 03 2015 David Tardon <dtardon@redhat.com> - 0.1.5-1
- new upstream release

* Wed Nov 18 2015 David Tardon <dtardon@redhat.com> - 0.1.4-1
- new upstream release

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.1.3-4
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.1.3-2
- rebuild for Boost 1.58

* Wed Jun 24 2015 David Tardon <dtardon@redhat.com> - 0.1.3-1
- new upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 David Tardon <dtardon@redhat.com> - 0.1.2-3
- fix output of shapes

* Tue May 26 2015 David Tardon <dtardon@redhat.com> - 0.1.2-2
- fix some problems found by coverity

* Wed May 20 2015 David Tardon <dtardon@redhat.com> - 0.1.2-1
- new upstream release

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.1.1-5
- Rebuilt for GCC 5 C++11 ABI change

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.1.1-4
- Rebuild for boost 1.57.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 David Tardon <dtardon@redhat.com> - 0.1.1-1
- new upstream release

* Thu May 29 2014 David Tardon <dtardon@redhat.com> - 0.1.0-2
- fix detection of Keynote 3 documents

* Mon May 26 2014 David Tardon <dtardon@redhat.com> - 0.1.0-1
- new upstream release

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.0.4-3
- Rebuild for boost 1.55.0

* Mon May 05 2014 Jaromir Capik <jcapik@redhat.com> - 0.0.4-2
- fixing FTBFS on ppc64le

* Tue Apr 15 2014 David Tardon <dtardon@redhat.com> - 0.0.4-1
- new upstream release

* Wed Apr 09 2014 David Tardon <dtardon@redhat.com> - 0.0.3-2
- generate man pages

* Fri Dec 06 2013 David Tardon <dtardon@redhat.com> - 0.0.3-1
- new release

* Wed Dec 04 2013 David Tardon <dtardon@redhat.com> - 0.0.2-1
- new release

* Mon Nov 04 2013 David Tardon <dtardon@redhat.com> - 0.0.1-1
- new release

* Wed Oct 30 2013 David Tardon <dtardon@redhat.com> 0.0.0-1
- initial import

