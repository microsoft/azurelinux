Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: tuna
Version: 0.19
Release: 1%{?dist}
License: GPLv2
Summary: Application tuning GUI & command line utility
Source: https://git.kernel.org/pub/scm/utils/%{name}/%{name}.git/snapshot/%{name}-%{version}.tar.gz
URL: https://rt.wiki.kernel.org/index.php/Tuna
BuildArch: noarch
BuildRequires: python3-devel, gettext
Requires: python3-ethtool
Requires: python3-linux-procfs >= 0.6
Requires: python3-schedutils >= 0.6
# This really should be a Suggests...
# Requires: python-inet_diag

%description
Provides interface for changing scheduler and IRQ tunables, at whole CPU and at
per thread/IRQ level. Allows isolating CPUs for use by a specific application
and moving threads and interrupts to a CPU by just dragging and dropping them.
Operations can be done on CPU sockets, understanding CPU topology.

Can be used as a command line utility without requiring the GUI libraries to be
installed.

%prep
%setup -q

%build
%py3_build
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" tuna/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" tuna-cmd.py

%install
rm -rf %{buildroot}
%py3_install
mkdir -p %{buildroot}/%{_sysconfdir}/tuna/
mkdir -p %{buildroot}/{%{_bindir},%{_datadir}/tuna/help/kthreads,%{_mandir}/man8}
mkdir -p %{buildroot}/%{_datadir}/polkit-1/actions/
install -p -m644 tuna/tuna_gui.glade %{buildroot}/%{_datadir}/tuna/
install -p -m755 tuna-cmd.py %{buildroot}/%{_bindir}/tuna
install -p -m644 help/kthreads/* %{buildroot}/%{_datadir}/tuna/help/kthreads/
install -p -m644 docs/tuna.8 %{buildroot}/%{_mandir}/man8/
install -p -m644 etc/tuna/example.conf %{buildroot}/%{_sysconfdir}/tuna/
install -p -m644 etc/tuna.conf %{buildroot}/%{_sysconfdir}/
install -p -m644 org.tuna.policy %{buildroot}/%{_datadir}/polkit-1/actions/

# l10n-ed message catalogues
for lng in `cat po/LINGUAS`; do
        po=po/"$lng.po"
        mkdir -p %{buildroot}/%{_datadir}/locale/${lng}/LC_MESSAGES
        msgfmt $po -o %{buildroot}/%{_datadir}/locale/${lng}/LC_MESSAGES/%{name}.mo
done

%find_lang %name

%files -f %{name}.lang
%doc ChangeLog
%{python3_sitelib}/*.egg-info
%{_bindir}/tuna
%{_datadir}/tuna/
%{python3_sitelib}/tuna/
%{_mandir}/man8/tuna.8*
%{_sysconfdir}/tuna.conf
%{_sysconfdir}/tuna/*
%{_datadir}/polkit-1/actions/org.tuna.policy

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.19-1
- Auto-upgrade to 0.19 - Azure Linux 3.0 - package upgrades

* Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.1-4
- Fixing invalid source URL.

* Thu Jan 27 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.14.1-3
- Move to SPECS
- Remove oscilloscope subpackage
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu May 21 2020 Jiri Kastner <jkastner@fedoraproject.org> - 0.14.1
- update to 0.14.1
- fixes RHBZ#1773339

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14-4
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Jiri Kastner <jkastner@fedoraproject.org> - 0.14-3
- upload patch

* Tue Feb 12 2019 Jiri Kastner <jkastner@fedoraproject.org> - 0.14-2
- oscilloscope gtk3 patch

* Tue Feb 12 2019 Jiri Kastner <jkastner@fedoraproject.org> - 0.14-1
- update to 0.14
- switch to python3

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.13.1-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 29 2017 Lubomir Rintel <lkundrak@v3.sk> - 0.13.1-4
- Add a missing dependency for oscilloscope

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Jiri Kastner <jkastner@redhat.com> - 0.13.1-1
- new version

* Mon Sep 26 2016 Dominik Mierzejewski <rpm@greysector.net> - 0.12-5
- rebuilt for matplotlib-2.0.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 10 2014 Jiri Kastner <jkastner@redhat.com> - 0.12-1
- new upstream release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jul 29 2013 Jiri Kastner <jkastner@redhat.com> - 0.11.1-1
- New upstream release

* Tue Jun 11 2013 Jiri Kastner <jkastner@redhat.com> - 0.11-2
- changed dependencies from python-numeric to numpy
- merged spec changes from upstream

* Thu Jun  6 2013 Jiri Kastner <jkastner@redhat.com> - 0.11-1
- New upstream release

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 01 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Sep 03 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.9.1-1
- New upstream release

* Wed Aug 26 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.9-3
- Rewrite the oscilloscope package summary
- Remove the shebang in tuna/oscilloscope.py

* Mon Aug 17 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.9-2
- Use install -p
- Add BuildRequires for gettext

* Fri Jul 10 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.9-1
- Fedora package reviewing changes: introduce ChangeLog file
