Vendor:         Microsoft Corporation
Distribution:   Mariner
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           lv2
Version:        1.16.0
Release:        4%{?dist}
Summary:        Audio Plugin Standard

# lv2specgen template.html is CC-AT-SA
License:        ISC
URL:            http://lv2plug.in
Source:         http://lv2plug.in/spec/lv2-%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libsndfile-devel
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-pygments
Buildrequires:  python3-rdflib
Buildrequires:  asciidoc

# this package replaces lv2core 
Provides:       lv2core = 6.0-4
Obsoletes:      lv2core < 6.0-4
Provides:       lv2-ui = 2.4-5
Obsoletes:      lv2-ui < 2.4-5

%description
LV2 is a standard for plugins and matching host applications, mainly
targeted at audio processing and generation.  

There are a large number of open source and free software synthesis
packages in use or development at this time. This API ('LV2') attempts
to give programmers the ability to write simple 'plugin' audio
processors in C/C++ and link them dynamically ('plug') into a range of
these packages ('hosts').  It should be possible for any host and any
plugin to communicate completely through this interface.

LV2 is a successor to LADSPA, created to address the limitations of
LADSPA which many hosts have outgrown.

%package        devel
Summary:        API for the LV2 Audio Plugin Standard

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-rdflib
Provides:       lv2core-devel = 6.0-4
Obsoletes:      lv2core-devel < 6.0-4
Provides:       lv2-ui-devel = 2.4-5
Obsoletes:      lv2-ui-devel < 2.4-5

%description    devel
lv2-devel contains the lv2.h header file and headers for all of the
LV2 specification extensions and bundles.

Definitive technical documentation on LV2 plug-ins for both the host
and plug-in is contained within copious comments within the lv2.h
header file.

%package        doc
Summary:        Documentation for the LV2 Audio Plugin Standard
BuildArch:      noarch
Obsoletes:      %{name}-docs < 1.6.0-2
Provides:       %{name}-docs = %{version}-%{release}

%description    doc
Documentation for the LV2 plugin API.

%package        example-plugins
Summary:        Examples of the LV2 Audio Plugin Standard

%description    example-plugins
Example LV2 audio plugins

%prep
%setup -q
# Fix wrong interpreter in lv2specgen.py
sed -i '1s|^#!.*|#!%{__python3}|' lv2specgen/lv2specgen.py

%build

%set_build_flags
%{__python3} waf configure -vv --prefix=%{_prefix} --libdir=%{_libdir} \
  --docs --docdir=%{_pkgdocdir} --lv2dir=%{_libdir}/lv2
%{__python3} waf -vv %{?_smp_mflags}

%install
DESTDIR=%buildroot %{__python3} waf -vv install
mv %{buildroot}%{_pkgdocdir}/%{name}/lv2plug.in/* %{buildroot}%{_pkgdocdir}
find %{buildroot}%{_pkgdocdir} -type d -empty | xargs rmdir
for f in COPYING NEWS README.md build/plugins/book.{txt,html} ; do
    install -p -m0644 $f %{buildroot}%{_pkgdocdir}
done

%files
# don't include doc files via %%doc here (bz 913540)
%dir %{_pkgdocdir}
%{_pkgdocdir}/COPYING
%{_pkgdocdir}/NEWS
%{_pkgdocdir}/README.md
%{_libdir}/%{name}/

%exclude %{_libdir}/%{name}/*/*.[ch]
%exclude %{_libdir}/%{name}/eg-*

%files devel
%{_bindir}/lv2specgen.py
%{_bindir}/lv2_validate
%{_datadir}/lv2specgen
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/%{name}/*/*.[hc]
%{_libdir}/pkgconfig/%{name}.pc

%exclude %{_libdir}/%{name}/eg-*

%files example-plugins
%{_libdir}/%{name}/eg-*

%files doc
%{_pkgdocdir}/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 23 2019 Guido Aulisi <guido.aulisi@gmail.com> - 1.16.0-1
- Update to 1.16.0
- Use python3
- Some spec cleanup

* Tue Feb 19 2019 Guido Aulisi <guido.aulisi@gmail.com> - 1.14.0-9
- Add missing dependency in devel package

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jul 15 2018 Guido Aulisi <guido.aulisi@gmail.com> - 1.14.0-7
- Fix FTBFS due to the move of /usr/bin/python into a separate package

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.14.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 27 2017 Guido Aulisi <guido.aulisi@gmail.com> - 1.14.0-2
- Fix wrong interpreter in lv2specgen.py

* Mon Mar 13 2017 Guido Aulisi <guido.aulisi@gmail.com> - 1.14.0-1
- Update to 1.14.0
- Move examples to the example-plugins subpackage
- Provide debuginfo for the examples
- Use hardened LDFLAGS
- Enable syntax highlighting in doc subpackage
- Remove deprecated Groups tags

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 16 2016 Brendan Jones <brendan.jones.it@gmail.com> - 1.12.0-1
- Update to 1.12.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Aug 19 2014 Brendan Jones <brendan.jones.it@gmail.com> 1.10.0-2
- Ad miising libsndfile

* Tue Aug 19 2014 Brendan Jones <brendan.jones.it@gmail.com> 1.10.0-1
- Update to 1.10.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 09 2014 Brendan Jones <brendan.jones.it@gmail.com> 1.8.0-1
- Upstream maintenance release
- Add example plugins

* Sun Sep 22 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.0-2
- Don't duplicate -doc package contents in base package (#913540).
- Define and use %%_pkgdocdir as suggested by the Unversioned Docdirs
  change for Fedora 20 (#993908).
- Pass --docdir= to waf.
- Use Group Documentation in -doc subpackage.
- Rename -docs package to -doc as recommended in the guidelines.
- The documentation subpackage does not need the base package.

* Fri Aug 23 2013 Brendan Jones <brendan.jones.it@gmail.com> 1.6.0-1
- Update to 1.6.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 1.4.0-1
- New upstream release 

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 20 2012 Brendan Jones <brendan.jones.it@gmail.com> 1.2.0-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Brendan Jones <brendan.jones.it@gmail.com> 1.0.0-7
- Remove date from doxygen footers

* Sat Apr 21 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-6
- Re-suppress debuginfo

* Sat Apr 21 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-5
- libsndfile no longer required

* Sat Apr 21 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-4
- remove examples 

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-3
- dd libsndfile BR

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-2
- Remove debuginfo supression, correct changelog

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-1
- Created

