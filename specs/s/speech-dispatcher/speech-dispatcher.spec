# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel} > 9
%global festival_backend 0
%else
%global festival_backend 1
%endif

Name:          speech-dispatcher
Version:       0.12.1
Release: 6%{?dist}
Summary:       To provide a high-level device independent layer for speech synthesis

# Almost all files are under GPL-2.0-or-later, however
# src/c/clients/spdsend/spdsend.h is licensed under GPLv2,
# which makes %%_bindir/spdsend GPLv2.
License:       GPL-2.0-or-later AND LGPL-2.1-only OR LGPL-2.0-only
URL:           http://devel.freebsoft.org/speechd
Source0:       https://github.com/brailcom/speechd/releases/download/%{version}/speech-dispatcher-%{version}.tar.gz
Source1:       http://www.freebsoft.org/pub/projects/sound-icons/sound-icons-0.1.tar.gz

Patch1:        0001-Remove-pyxdg-dependency.patch
#Patch2:        4ba45da405fe8dba5ed56725d20a388d6d0269a4.patch
#Patch3:        de9588a29ed6deda8ced1bab98abccebfe1ee788.patch

BuildRequires: alsa-lib-devel
BuildRequires: desktop-file-utils
BuildRequires: dotconf-devel
BuildRequires: espeak-ng-devel
%if 0%{?fedora} || 0%{?rhel} < 10
BuildRequires: flite-devel >= 2.0
%endif
BuildRequires: gcc
BuildRequires: gcc-c++
Buildrequires: glib2-devel
BuildRequires: help2man
Buildrequires: intltool
Buildrequires: libao-devel
Buildrequires: libtool-ltdl-devel
Buildrequires: libsndfile-devel
BuildRequires: make
Buildrequires: pulseaudio-libs-devel
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: systemd-rpm-macros
BuildRequires: texinfo
BuildRequires: systemd-devel

Requires:      %{name}-espeak-ng%{?_isa} = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Obsoletes:     speech-dispatcher-baratinoo < 0.9.1
Obsoletes:     speech-dispatcher-kali < 0.9.1

%description
* Common interface to different TTS engines
* Handling concurrent synthesis requests – requests may come
  asynchronously from multiple sources within an application
  and/or from more different applications.
* Subsequent serialization, resolution of conflicts and
  priorities of incoming requests
* Context switching – state is maintained for each client
  connection independently, event for connections from
  within one application.
* High-level client interfaces for popular programming languages
* Common sound output handling – audio playback is handled by
  Speech Dispatcher rather than the TTS engine, since most engines
  have limited sound output capabilities.

%package        libs
Summary:        Development files for %{name}
License:        GPL-2.0-or-later
# split out of main package
Conflicts:      %{name} < 0.11.5-4

%description    libs
The %{name}-libs package contains runtime libraries for applications
that use %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
License:        GPL-2.0-or-later

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:        Documentation for speech-dispatcher
License:        GPL-2.0-or-later
Requires:       %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
speechd documentation

%package utils
Summary:        Various utilities for speech-dispatcher
License:        GPL-2.0-or-later
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       python3-speechd = %{version}-%{release}
Requires:       pulseaudio-utils

%description utils
Various utilities for speechd

%package espeak-ng
Summary:        Speech Dispatcher espeak-ng module
Requires:       %{name}%{_isa} = %{version}-%{release}

%description espeak-ng
This package contains the espeak-ng output module for Speech Dispatcher.

%if %{festival_backend}
%package festival
Summary:        Speech Dispatcher festival module
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       festival-freebsoft-utils

%description festival
This package contains the festival output module for Speech Dispatcher.
%endif

%if 0%{?fedora} || 0%{?rhel} < 10
%package flite
Summary:        Speech Dispatcher flite module
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       flite%{?_isa} >= 2.0

%description flite
This package contains the flite output module for Speech Dispatcher.
%endif

%package -n python3-speechd
Summary:        Python 3 Client API for speech-dispatcher
License:        GPL-2.0-or-later

%description -n python3-speechd
Python 3 module for speech-dispatcher

%prep
%autosetup -p1

tar xf %{SOURCE1}

%build
%configure --disable-static \
	--with-alsa --with-pulse --with-libao \
	--with-espeak-ng \
%if 0%{?fedora} || 0%{?rhel} < 10
	--with-flite \
%endif
	--without-oss --without-nas --without-espeak \
	--with-kali=no --with-baratinoo=no --with-ibmtts=no --with-voxin=no \
	--sysconfdir=%{_sysconfdir} --with-default-audio-method=pulse \
	--with-module-bindir=%{_libdir}/speech-dispatcher-modules/ \
	--with-systemdsystemunitdir=%{_unitdir} \
	--with-systemduserunitdir=%{_prefix}/lib/systemd/user/

%make_build

%install
%make_install

install -p -m 0644 sound-icons-0.1/* %{buildroot}%{_datadir}/sounds/%{name}/

%find_lang speech-dispatcher

#Remove %{_infodir}/dir file
rm -f %{buildroot}%{_infodir}/dir

find %{buildroot} -name '*.la' -delete

# Move the config files from /usr/share to /etc
mkdir -p %{buildroot}%{_sysconfdir}/speech-dispatcher/clients
mkdir -p %{buildroot}%{_sysconfdir}/speech-dispatcher/modules
mv %{buildroot}%{_datadir}/speech-dispatcher/conf/speechd.conf %{buildroot}%{_sysconfdir}/speech-dispatcher/
mv %{buildroot}%{_datadir}/speech-dispatcher/conf/clients/* %{buildroot}%{_sysconfdir}/speech-dispatcher/clients
mv %{buildroot}%{_datadir}/speech-dispatcher/conf/modules/* %{buildroot}%{_sysconfdir}/speech-dispatcher/modules

# Create log dir
mkdir -p -m 0700 %{buildroot}%{_localstatedir}/log/speech-dispatcher/

# Verify the desktop files
desktop-file-validate %{buildroot}/%{_datadir}/speech-dispatcher/conf/desktop/speechd.desktop

# enable pulseaudio as default with a fallback to alsa
sed 's/# AudioOutputMethod "pulse,alsa"/AudioOutputMethod "pulse,alsa"/' %{buildroot}%{_sysconfdir}/speech-dispatcher/speechd.conf

# explicitly enable espeak-ng module, othervise it falls back to espeak-ng-mbrola and it has bad pronunciation
sed -i 's/#AddModule "espeak-ng"                "sd_espeak-ng" "espeak-ng.conf"/AddModule "espeak-ng"                "sd_espeak-ng" "espeak-ng.conf"/' %{buildroot}%{_sysconfdir}/speech-dispatcher/speechd.conf



# Remove Festival related files if needed, we can't disable their generation by any other means (e. g. configure option).
# And if not done, we're getting an error about installed but unpackaged files.
%if %{festival_backend} == 0
rm %{buildroot}%{_sysconfdir}/speech-dispatcher/modules/festival.conf
rm %{buildroot}%{_libdir}/speech-dispatcher-modules/sd_festival
%endif

%post 
%systemd_post speech-dispatcherd.service

%postun
%systemd_postun_with_restart speech-dispatcherd.service

%preun
%systemd_preun speech-dispatcherd.service

%files -f speech-dispatcher.lang
%license COPYING.LGPL
%doc NEWS README.md
%dir %{_sysconfdir}/speech-dispatcher/
%dir %{_sysconfdir}/speech-dispatcher/clients
%dir %{_sysconfdir}/speech-dispatcher/modules
%config(noreplace) %{_sysconfdir}/speech-dispatcher/speechd.conf
%config(noreplace) %{_sysconfdir}/speech-dispatcher/clients/*.conf
%config(noreplace) %{_sysconfdir}/speech-dispatcher/modules/*.conf
%exclude %{_sysconfdir}/speech-dispatcher/modules/espeak*.conf
%exclude %{_sysconfdir}/speech-dispatcher/modules/festival.conf
%exclude %{_sysconfdir}/speech-dispatcher/modules/flite.conf
%{_bindir}/speech-dispatcher
%{_datadir}/speech-dispatcher/
%dir %{_libdir}/speech-dispatcher-modules/
%{_libdir}/speech-dispatcher-modules/sd_cicero
%{_libdir}/speech-dispatcher-modules/sd_dummy
%{_libdir}/speech-dispatcher-modules/sd_generic
%{_libdir}/speech-dispatcher-modules/sd_openjtalk

%dir %{_libdir}/speech-dispatcher
%{_libdir}/speech-dispatcher/spd*.so
%{_datadir}/sounds/speech-dispatcher
%{_mandir}/man1/speech-dispatcher.1*
%dir %attr(0700, root, root) %{_localstatedir}/log/speech-dispatcher/
%{_unitdir}/speech-dispatcherd.service
%{_prefix}/lib/systemd/user/speech-dispatcher.service
%{_prefix}/lib/systemd/user/speech-dispatcher.socket

%files libs
%license COPYING.LGPL
%{_libdir}/libspeechd.so.2
%{_libdir}/libspeechd.so.2.6.0
%{_libdir}/libspeechd_module.so.0
%{_libdir}/libspeechd_module.so.0.0.0

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%{_infodir}/*

%files utils
%{_bindir}/spd-conf
%{_bindir}/spd-say
%{_bindir}/spdsend
%{_mandir}/man1/spd-conf.1*
%{_mandir}/man1/spd-say.1*

%files espeak-ng
%config(noreplace) %{_sysconfdir}/speech-dispatcher/modules/espeak-ng.conf
%{_libdir}/speech-dispatcher-modules/sd_espeak-ng
%{_libdir}/speech-dispatcher-modules/sd_espeak-ng-mbrola

%if %{festival_backend}
%files festival
%config(noreplace) %{_sysconfdir}/speech-dispatcher/modules/festival.conf
%{_libdir}/speech-dispatcher-modules/sd_festival
%endif

%if 0%{?fedora} || 0%{?rhel} < 10
%files flite
%config(noreplace) %{_sysconfdir}/speech-dispatcher/modules/flite.conf
%{_libdir}/speech-dispatcher-modules/sd_flite
%endif

%files -n python3-speechd
%{python3_sitearch}/speechd*

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.12.1-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.12.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.12.1-2
- Rebuilt for Python 3.14

* Wed May 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 0.12.1-1
- 0.12.1

* Thu Apr 24 2025 Vojtech Polasek <krecoun@gmail.com> - 0.12.0-2
- enable espeak-ng module by default

* Mon Feb 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 0.12.0-1
- 0.12.0

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 1 2024 Lukas Tyrychtr <ltyrycht@redhat.com>
- Conditionalize the festival subpackage, we're not shipping Festival in RHEL 10

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.11.5-6
- Rebuilt for Python 3.13

* Sun Apr 14 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.11.5-5
- Fix split -libs upgrades

* Thu Mar 21 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.11.5-4
- Split out libs and adjust dependencies

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.11.5-2
- Have utils require pulseaudio-utils as it's the default.

* Mon Aug 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.11.5-1
- 0.11.5

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.11.4-5
- Rebuilt for Python 3.12

* Fri May 12 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.11.4-4
- Disable flite in RHEL 10+ builds

* Tue Feb 28 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.11.4-3
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.11.4-1
- 0.11.4

* Mon Sep 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.11.3-1
- 0.11.3

* Mon Aug 29 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.11.2-1
- 0.11.2

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.11.1-3
- Rebuilt for Python 3.11

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.11.1-1
- 0.11.1

* Mon Dec 13 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.11.0-1
- 0.11.0

* Mon Oct 18 2021 Dominik Mierzejewski <rpm@greysector.net> - 0.10.2-7
- move the manual flite dependency to flite subpackage

* Wed Oct 06 2021 Dominik Mierzejewski <rpm@greysector.net> - 0.10.2-6
- Rebuilt for flite-2.2
- Added manual dependencies on flite 2.0+ for register_cmu_us_kal16 symbol

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.10.2-4
- Rebuilt for Python 3.10

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.2-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.2-1
- Update to 0.10.2

* Fri Sep 11 2020 Kalev Lember <klember@redhat.com> - 0.10.1-2
- Fix crash with python 3.9 (#1878276)

* Mon Aug 10 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.1-1
- Update to 0.10.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-7
- Rebuilt for Python 3.9

* Tue Feb 25 2020 Than Ngo <than@redhat.com> - 0.9.1-6
- Fixed FTBFS

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.1-1
- speech-dispatcher 0.9.1

* Tue Feb 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-4
- Remove obsolete scriptlets

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Kalev Lember <klember@redhat.com> - 0.9.0-2
- Split new baratinoo and kali modules out into separate subpackages
- Install man pages
- Update the source URL

* Sun Jan 27 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.0-1
- speech-dispatcher 0.9.0

* Fri Jul 20 2018 Bastien Nocera <bnocera@redhat.com> - 0.8.8-8
- speech-dispatcher-0.8.8-8
- Remove pyxdg dependency

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8.8-6
- Rebuilt for Python 3.7

* Thu Mar 08 2018 Ondřej Lysoněk <olysonek@redhat.com> - 0.8.8-5
- Make espeak-ng the default output module, drop the espeak output module

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Ondřej Lysoněk <olysonek@redhat.com> - 0.8.8-3
- Add support for espeak-ng, add speech-dispatcher-espeak-ng subpackage

* Thu Jan 25 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.8.8-2
- include translations, pkgconfig support (#1538715)
- own %%_datadir/speech-dispatcher (#1480893)

* Tue Nov  7 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.8-1
- 0.8.8

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.7-1
- 0.8.7

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.8.6-2
- Rebuild for Python 3.6

* Wed Dec  7 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.6-1
- 0.8.6

* Wed Aug 10 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.5-1
- 0.8.5

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 20 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.4-1
- 0.8.4

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.3-1
- 0.8.3

* Mon May 18 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-5
- Add missing libsndfile dependency to fix sound icon support

* Tue Apr 14 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-4
- Always install the espeak plugin

* Fri Mar 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-3
- Fix noarch docs Requires

* Fri Mar 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-2
- Use %%license
- Make packaging more modular (rhbz #799140)

* Fri Mar 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-1
- 0.8.2

* Mon Sep 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.1-1
- 0.8.1
- Split utils into sub package

* Fri Aug 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.1-0.1rc1
- 0.8.1 rc1
- Enable hardened build

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 0.8-11
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Mar 27 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-7
- Rebuild

* Fri Nov  1 2013 Matthias Clasen <mclasen@redhat.com> 0.8-6
- Avoid a crash in the festival module (#995639)

* Tue Aug 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-5
- Install clients as not longer installed by default (fixes RHBZ 996337)

* Sat Aug 10 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8-4
- include/install missing headers

* Wed Aug  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-3
- Drop libao and python2 bindings

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-1
- Update to 0.8 stable release
- Rename python package for consistency
- Add python3 bindings - fixes RHBZ 867958
- Update the systemd scriptlets to the macroized versions

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Bastien Nocera <bnocera@redhat.com> 0.7.1-9
- Move RPM hacks to source patches

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
