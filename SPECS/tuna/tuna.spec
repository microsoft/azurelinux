# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond oscilloscope %{undefined rhel}

Name: tuna
Version: 0.20
Release: 2%{?dist}
License: GPL-2.0-only AND LGPL-2.1-only
Summary: Application tuning GUI & command line utility
Source: https://www.kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.xz
URL: https://rt.wiki.kernel.org/index.php/Tuna
BuildArch: noarch
BuildRequires: python3-devel, gettext
BuildRequires: pyproject-rpm-macros
BuildRequires: python3-pip
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
Requires: python3-linux-procfs >= 0.6
# This really should be a Suggests...
# Requires: python-inet_diag

# Patches

%description
Provides interface for changing scheduler and IRQ tunables, at whole CPU and at
per thread/IRQ level. Allows isolating CPUs for use by a specific application
and moving threads and interrupts to a CPU by just dragging and dropping them.
Operations can be done on CPU sockets, understanding CPU topology.

Can be used as a command line utility without requiring the GUI libraries to be
installed.

%if %{with oscilloscope}
%package -n oscilloscope
Summary: Generic graphical signal plotting tool
Requires: python3-matplotlib-gtk3
Requires: python3-numpy
Requires: python3-cairocffi
Requires: gobject-introspection
Requires: tuna = %{version}-%{release}

%description -n oscilloscope
Plots stream of values read from standard input on the screen together with
statistics and a histogram.

Allows to instantly see how a signal generator, such as cyclictest, signaltest
or even ping, reacts when, for instance, its scheduling policy or real time
priority is changed, be it using tuna or plain chrt & taskset.
%endif

%prep
%autosetup -v -p1
# Delete setup.py so pyproject.toml build doesn't use it
rm -f setup.py
# Prepare tuna script for installation (save to a separate location to avoid directory conflict)
cp -p tuna-cmd.py %{_builddir}/tuna-script
# Compress man page
gzip -c docs/tuna.8 > %{_builddir}/tuna.8.gz

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files tuna
# Install the tuna script
install -D -m 0755 %{_builddir}/tuna-script %{buildroot}%{_bindir}/tuna
# Install the compressed man page
install -D -m 0644 %{_builddir}/tuna.8.gz %{buildroot}%{_mandir}/man8/tuna.8.gz

mkdir -p %{buildroot}/%{_sysconfdir}/tuna/
mkdir -p %{buildroot}/%{_datadir}/tuna/help/kthreads
mkdir -p %{buildroot}/%{_datadir}/polkit-1/actions/
install -p -m644 tuna/tuna_gui.glade %{buildroot}/%{_datadir}/tuna/
install -p -m644 help/kthreads/* %{buildroot}/%{_datadir}/tuna/help/kthreads/
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

%files -f %{name}.lang -f %{pyproject_files}
%doc ChangeLog
%{_bindir}/tuna
%{_datadir}/tuna/
%{_mandir}/man8/tuna.8.gz
%{_sysconfdir}/tuna.conf
%{_sysconfdir}/tuna/*
%{_datadir}/polkit-1/actions/org.tuna.policy

%if %{with oscilloscope}
%files -n oscilloscope
%{_bindir}/oscilloscope
%doc docs/oscilloscope+tuna.html
%doc docs/oscilloscope+tuna.pdf
%endif

%changelog
* Tue Nov 04 2025 John Kacur <jkacur@redhat.com> - 0.20-2
- Add python3-pip, python3-setuptools, python3-wheel BuildRequires
- Delete setup.py in %%prep so pyproject.toml build is used
- Compress man page during %%prep similar to rteval
- Install tuna script and compressed man page explicitly

* Mon Oct 27 2025 John Kacur <jkacur@redhat.com> - 0.20-1
- Update to upstream version 0.20
- Convert to pyproject-rpm-macros for modern Python packaging
- Add pyproject.toml for modern Python packaging
- Remove all patches (now included in upstream 0.20)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.19-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.19-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.19-10
- Rebuilt for Python 3.14

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.19-7
- Rebuilt for Python 3.13

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 02 2023 John Kacur <jkacur@redhat.com> - 0.19-5
- Convert to SPDX licenses and use this in the specfile too

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.19-3
- Disable oscilloscope in RHEL builds
- Remove obsolete dependencies

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.19-2
- Rebuilt for Python 3.12

* Thu Feb 16 2023 John Kacur <jkacur@redhat.com> - 0.19-1
- Use setuptools and sysconfig instead of distutils in setup.py
- Update to 0.19 upstream

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 12 2022 Federico Pellegrin <fede@evolware.org> - 0.18-1
- update to 0.18, remove now merged patch

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.17-3
- Rebuilt for Python 3.11

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Federico Pellegrin <fede@evolware.org> - 0.17-1
- update to 0.17 (various fixes and cleanups)

* Fri Aug 20 2021 Federico Pellegrin <fede@evolware.org> - 0.16-1
- update to 0.16 (contains Gtk3 support)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.14.1-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-2
- Rebuilt for Python 3.9

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
