# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Expected failures in mock, hangs in koji
%bcond_with tests
# The *.py files we ship are not python scripts, #813651
%global _python_bytecompile_errors_terminate_build 0
%define upstream_version 2.16.0

Name:           bash-completion
Version:        2.16
Release:        2%{?dist}
Epoch:          1
Summary:        Programmable completion for Bash

License:        GPL-2.0-or-later
URL:            https://github.com/scop/bash-completion
Source0:        https://github.com/scop/bash-completion/releases/download/%{upstream_version}/%{name}-%{upstream_version}.tar.xz

BuildArch:      noarch
%if %{with tests}
BuildRequires:  dejagnu
BuildRequires:  screen
BuildRequires:  tcllib
%endif
# Needed for rfkill patch as it modifies Makefile.am
# It should be removed while rebasing to bash-completion-2.8
BuildRequires:  automake
BuildRequires: make
Requires:       bash >= 4.1

%description
bash-completion is a collection of shell functions that take advantage
of the programmable completion feature of bash.

%package devel
Summary: Development files for %{name}
Requires: %{name} =  %{epoch}:%{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%autosetup -n %{name}-%{upstream_version} -p1

%build
# Needed for rfkill patch as it modifies Makefile.am
# It should be removed while rebasing to bash-completion-2.8
autoreconf -fi -v
%configure
%make_build

%install
%make_install

# Updated completion shipped in cowsay package:
rm %{buildroot}%{_datadir}/bash-completion/completions/{cowsay,cowthink}

# Bug 1819867 - conflict over the makepkg name with pacman
rm %{buildroot}%{_datadir}/bash-completion/completions/makepkg

# Bug 2088307 - Remove completions for prelink
rm %{buildroot}%{_datadir}/bash-completion/completions/prelink

# Bug 2188865 - Remove bash completions for javaws as it's not shipped with Fedora
rm %{buildroot}%{_datadir}/bash-completion/completions/javaws

%check
# For some tests involving non-ASCII filenames
export LANG=C.UTF-8
%if %{with tests}
# This stuff borrowed from dejagnu-1.4.4-17 (tests need a terminal)
tmpfile=$(mktemp)
screen -D -m sh -c '( make check ; echo $? ) >'$tmpfile
cat $tmpfile
result=$(tail -n 1 $tmpfile)
rm -f $tmpfile
exit $result
%else
make -C completions check
%endif


%files
%license COPYING
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md README.md
%doc doc/configuration.md doc/styleguide.md
%config(noreplace) %{_sysconfdir}/profile.d/bash_completion.sh
%{_sysconfdir}/bash_completion.d/000_bash_completion_compat.bash
%{_datadir}/bash-completion/

%files devel
%{_datadir}/cmake/
%{_datadir}/pkgconfig/bash-completion.pc

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 21 2025 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.16-1
- Update to version 2.16
  Resolves: #2328588

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 22 2024 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.13-1
- Update to version 2.13
  Resolves: #2273545

* Mon Mar 18 2024 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.12-1
- Update to version 2.12.0

* Thu Feb 15 2024 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.11-15
- Move development files in devel subpackage
  Resolves: #1457164

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.11-11
- Remove bash completions for javaws
  Resolves: #2188865

* Tue Apr 11 2023 Lukáš Zaoral <lzaoral@redhat.com> - 1:2.11-10
- migrate to SPDX license format

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu May 19 2022 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.11-7
- Remove completions for prelink
  Resolves: #2088307

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 Ville Skyttä <ville.skytta@iki.fi> - 1:2.11-5
- Revert back to upstream _filedir override avoidance

* Mon Nov 08 2021 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.11-4
- Avoid conflict with makepkg completions in pacman
  Resolves: #1819867

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  8 13:20:44 CET 2021 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.11-1
- Rebase to version 2.11
  Resolves: #1782254

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.8-5
- Add completion for rpm -q --licensefiles
  Resolves: #1578811

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.8-4
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Mon Aug 13 2018 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.8-3
- Document how to turn off default completions
  Resolves: #1575571

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.8-1
- Update to 2.8
  Resolves: #1561241

* Wed Mar 14 2018 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.7-4
- Do not use $MANPATH directly
  Resolves: #1495055

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 09 2017 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.7-2
- Rename rfkill function to avoid conflict with util-linux >= 2.31
  Resolves: #1494855

* Thu Oct 05 2017 Siteshwar Vashisht <svashisht@redhat.com> - 1:2.7-1
- Update to 2.7

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Ville Skyttä <ville.skytta@iki.fi> - 1:2.6-1
- Update to 2.6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb  4 2017 Ville Skyttä <ville.skytta@iki.fi> - 1:2.5-1
- Update to 2.5

* Fri Aug 12 2016 Ville Skyttä <ville.skytta@iki.fi> - 1:2.4-1
- Update to 2.4

* Mon Mar 28 2016 Ville Skyttä <ville.skytta@iki.fi> - 1:2.3-1
- Update to 2.3

* Thu Mar  3 2016 Ville Skyttä <ville.skytta@iki.fi> - 1:2.2-1
- Update to 2.2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1-9.20150513git1950590
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1-8.20150513git1950590
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-7.20150513git1950590
- Autogenerate redefine_filedir (fixes #1171396 in it too)

* Wed May 13 2015 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-6.20150513git1950590
- Update to current upstream git (fixes #1171396)
- Move pre-1.90 %%changelog entries to CHANGES.package.old

* Mon Nov 10 2014 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-6.20141110git52d8316
- Update to current upstream git (fixes #744406, #949479, #1090481, #1015935,
  #1132959, #1135489)
- Clean up no longer needed specfile conditionals
- Mark COPYING as %%license where applicable

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 17 2013 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-4
- Ship bash_completion.txt.
- Make profile.d scriptlet noreplace again.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  9 2013 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-2
- Don't install nmcli completion on F-18+ (#950071).

* Mon Apr  8 2013 Ville Skyttä <ville.skytta@iki.fi> - 1:2.1-1
- Update to 2.1 (fixes #860510, #906469, #912113, #919246, #928253).
- Don't ship completions included in util-linux 2.23-rc2 for F-19+.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:2.0-1
- Update to 2.0 (fixes #817902, #831835).
- Don't try to python-bytecompile our non-python *.py (#813651).

* Sun Jan  8 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:1.99-1
- Update to 1.99.

* Fri Nov  4 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:1.90-1
- Update to 1.90.
- Specfile cleanups.
- Move pre-1.2 %%changelog entries to CHANGES.package.old.
