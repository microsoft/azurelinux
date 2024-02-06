%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%bcond_with docs
Summary:        Audio Plugin Standard
Name:           lv2
Version:        1.18.8
Release:        3%{?dist}
# lv2specgen template.html is CC-AT-SA
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://lv2plug.in
Source:         https://lv2plug.in/spec/%{name}-%{version}.tar.xz
BuildRequires:  asciidoc
BuildRequires:  cairo-devel >= 1.8.10
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  libsndfile-devel
BuildRequires:  meson
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  python3-pygments
BuildRequires:  python3-rdflib
BuildRequires:  python3-markdown
BuildRequires:  python3-lxml
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
Requires:       python3-markdown
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

%if %{with docs}
%package        doc
Summary:        Documentation for the LV2 Audio Plugin Standard
Obsoletes:      %{name}-docs < 1.6.0-2
Provides:       %{name}-docs = %{version}-%{release}
BuildArch:      noarch

%description    doc
Documentation for the LV2 plugin API.
%endif

%package        example-plugins
Summary:        Examples of the LV2 Audio Plugin Standard
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    example-plugins
Example plugins for the LV2 Audio Plugin Standard.

%prep
%autosetup -p1
# Fix wrong interpreter in lv2specgen.py
sed -i '1s|^#!.*|#!%{__python3}|' lv2specgen/lv2specgen.py

%build
%meson \
%if %{with docs}
  -D docs=enabled \
%else
  -D docs=disabled \
%endif
  -D old_headers=true \
  -D tests=disabled

%meson_build

%install
%meson_install

# Let RPM pick docs in the files section
rm -fr %{buildroot}%{_docdir}/%{name}

%check
%meson_test

%files
%license COPYING
%doc NEWS README.md
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/atom.lv2
%{_libdir}/%{name}/buf-size.lv2
%{_libdir}/%{name}/core.lv2
%{_libdir}/%{name}/data-access.lv2
%{_libdir}/%{name}/dynmanifest.lv2
%{_libdir}/%{name}/event.lv2
%{_libdir}/%{name}/instance-access.lv2
%{_libdir}/%{name}/log.lv2
%{_libdir}/%{name}/midi.lv2
%{_libdir}/%{name}/morph.lv2
%{_libdir}/%{name}/options.lv2
%{_libdir}/%{name}/parameters.lv2
%{_libdir}/%{name}/patch.lv2
%{_libdir}/%{name}/port-groups.lv2
%{_libdir}/%{name}/port-props.lv2
%{_libdir}/%{name}/presets.lv2
%{_libdir}/%{name}/resize-port.lv2
%{_libdir}/%{name}/schemas.lv2
%{_libdir}/%{name}/state.lv2
%{_libdir}/%{name}/time.lv2
%{_libdir}/%{name}/ui.lv2
%{_libdir}/%{name}/units.lv2
%{_libdir}/%{name}/uri-map.lv2
%{_libdir}/%{name}/urid.lv2
%{_libdir}/%{name}/worker.lv2

%files devel
%{_bindir}/lv2specgen.py
%{_bindir}/lv2_validate
%{_datadir}/lv2specgen
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/lv2.h

%files example-plugins
%{_libdir}/%{name}/eg-amp.lv2
%{_libdir}/%{name}/eg-fifths.lv2
%{_libdir}/%{name}/eg-metro.lv2
%{_libdir}/%{name}/eg-midigate.lv2
%{_libdir}/%{name}/eg-params.lv2
%{_libdir}/%{name}/eg-sampler.lv2
%{_libdir}/%{name}/eg-scope.lv2

%if %{with docs}
%files doc
%doc %{_vpath_builddir}/doc/*
%endif

%changelog
* Thu Nov 24 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.18.8-3
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Disable subpackage docs.
- Disable check section with missing dependency on codespell
- License verified

* Sat Sep 17 2022 Guido Aulisi <guido.aulisi@gmail.com> - 1.18.8-2
- Readd old headers #2127286

* Tue Aug 30 2022 Simone Caronni <negativo17@gmail.com> - 1.18.8-1
- Update to 1.18.8, switch to Meson.
- Update docs installation.
- Drop gcc/python-devel build requirements.
- Avoid exclude directives in the files section so build ids are not duplicated.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 02 2022 Guido Aulisi <guido.aulisi@gmail.com> - 1.18.4-1
- Update to 1.18.4

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 08 2021 Guido Aulisi <guido.aulisi@gmail.com> - 1.18.2-1
- Update to 1.18.2
- Add BR gcc-c++

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 26 2020 Guido Aulisi <guido.aulisi@gmail.com> - 1.18.0-1
- Update to 1.18.0
- Add missing BR

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
- Remove deprecated Group tags

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 16 2016 Brendan Jones <brendan.jones.it@gmail.com> - 1.12.0-1
- Update to 1.12.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Aug 19 2014 Brendan Jones <brendan.jones.it@gmail.com> 1.10.0-2
- Add missing libsndfile

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
