# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           lv2
Version:        1.18.10
Release: 4%{?dist}
Summary:        Audio Plugin Standard

# lv2specgen template.html is CC-AT-SA
License:        ISC
URL:            https://lv2plug.in
Source:         https://lv2plug.in/spec/lv2-%{version}.tar.xz
Patch0:         %{name}-no-gtk2.patch

BuildRequires:  asciidoc
Buildrequires:  cairo-devel >= 1.8.10
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  libsndfile-devel
BuildRequires:  meson
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  python3-pygments
Buildrequires:  python3-rdflib
Buildrequires:  python3-markdown
Buildrequires:  python3-lxml

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
Requires:       python3-markdown

%description    devel
lv2-devel contains the lv2.h header file and headers for all of the
LV2 specification extensions and bundles.

Definitive technical documentation on LV2 plug-ins for both the host
and plug-in is contained within copious comments within the lv2.h
header file.

%package        doc
Summary:        Documentation for the LV2 Audio Plugin Standard
BuildArch:      noarch

%description    doc
Documentation for the LV2 plugin API.

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
  -D docs=enabled \
  -D old_headers=true \
  -D tests=disabled

%meson_build

%install
%meson_install

# Let RPM pick docs in the files section
rm -fr %{buildroot}%{_docdir}/%{name}

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

%files doc
%doc %{_vpath_builddir}/doc/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 23 2024 Simone Caronni <negativo17@gmail.com> - 1.18.10-1
- Update to 1.18.10.
- Delete very old macro and provides/obsoletes definitions. We don't have any
  of those versions anymore in any non-EOL release.
- Trim changelog.
- Drop examples that require GTK2.
- Remove %pretrans lua scriptlet, required only when going from el8 to el9.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 30 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.8-4
- Fix pretrans lua script error for first installation (not upgrade)
  (#2131236)

* Fri Sep 23 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.18.8-3
- Remove all symlinks in previous -devel subpackage in %%pre_trans
  to ensure update transaction (#2123422)

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
