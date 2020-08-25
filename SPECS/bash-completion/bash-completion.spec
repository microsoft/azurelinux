# Expected failures in mock, hangs in koji
%bcond_with tests
# The *.py files we ship are not python scripts, #813651
%global _python_bytecompile_errors_terminate_build 0

Name:           bash-completion
Version:        2.8
Release:        4%{?dist}
# Epoch:          1
Summary:        Programmable completion for Bash
Group:          Applications/Shells
Vendor:         Microsoft Corporation
Distribution:   Mariner

License:        GPLv2+
URL:            https://github.com/scop/bash-completion
Source0:        https://github.com/scop/bash-completion/releases/download/%{version}/%{name}-%{version}.tar.xz
# https://bugzilla.redhat.com/677446, see also redefine_filedir comments
Patch0:         %{name}-1.99-noblacklist.patch

# Remove while rebasing to bash-completion-2.9
Patch1:         %{name}-2.9-override-completions.patch

BuildArch:      noarch
%if %{with tests}
BuildRequires:  dejagnu
BuildRequires:  screen
BuildRequires:  tcllib
%endif
# Needed for rfkill patch as it modifies Makefile.am
# It should be removed while rebasing to bash-completion-2.8
BuildRequires:  automake
Requires:       bash >= 4.1

%description
bash-completion is a collection of shell functions that take advantage
of the programmable completion feature of bash.

%prep
# %%autosetup -p1
%setup -q

%build
# Needed for rfkill patch as it modifies Makefile.am
# It should be removed while rebasing to bash-completion-2.8
autoreconf -fi -v
%configure
%make_build

cat <<EOF >redefine_filedir
# This is a copy of the _filedir function in bash_completion, included
# and (re)defined separately here because some versions of Adobe
# Reader, if installed, are known to override this function with an
# incompatible version, causing various problems.
#
# https://bugzilla.redhat.com/677446
# http://forums.adobe.com/thread/745833

EOF
sed -ne '/^_filedir\s*(/,/^}/p' bash_completion >>redefine_filedir


%install
%make_install
install -Dpm 644 redefine_filedir \
    %{buildroot}%{_sysconfdir}/bash_completion.d/redefine_filedir

# Updated completion shipped in cowsay package:
rm %{buildroot}%{_datadir}/bash-completion/completions/{cowsay,cowthink}


%check
# For some tests involving non-ASCII filenames
export LANG=en_US.UTF-8
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
%doc AUTHORS CHANGES CONTRIBUTING.md README.md
%doc doc/bash_completion.txt
%config(noreplace) %{_sysconfdir}/profile.d/bash_completion.sh
%{_sysconfdir}/bash_completion.d/
%{_datadir}/bash-completion/
%{_datadir}/cmake/
%{_datadir}/pkgconfig/bash-completion.pc


%changelog
* Tue Aug 25 2020 Andrew Phelps <anphel@microsoft.com> - 2.8-4
  Initial CBL-Mariner import from Fedora 29 (license: MIT)
  Remove Epoch

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
