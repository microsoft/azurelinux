# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global qt_module qtspeech

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

%global examples 1

%bcond flite 0%{?fedora}

Summary: Qt6 - Speech component
Name:    qt6-%{qt_module}
Version: 6.10.2
Release: 1%{?dist}

# Code can be either LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only
# See e.g. src/plugins/speechdispatcher or src/tts
# Examples are under BSD-3-Clause
License: (GPL-2.0-only OR LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0) AND BSD-3-Clause
Url:     http://www.qt.io
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtmultimedia-devel >= %{version}
BuildRequires: qt6-qtdeclarative-devel >= %{version}
BuildRequires: speech-dispatcher-devel >= 0.8
%if %{with flite}
BuildRequires: flite-devel
%endif

BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}

%if %{with flite}
Recommends:    (%{name}-flite%{?_isa} = %{version}-%{release} if flite)
%endif
Recommends:    (%{name}-speechd%{?_isa} = %{version}-%{release} if speech-dispatcher)

%description
The module enables a Qt application to support accessibility features
such as text-to-speech, which is useful for end-users who are visually
challenged or cannot access the application for whatever reason. The
most common use case where text-to-speech comes in handy is when the
end-user is driving and cannot attend the incoming messages on the phone.
In such a scenario, the messaging application can read out the incoming
message. Qt Serial Port provides the basic functionality, which includes
configuring, I/O operations, getting and setting the control signals of
the RS-232 pinouts.

%if %{with flite}
%package flite
Summary: Festival Lite text-to-speech engine for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description flite
%{summary}.
%endif

%package speechd
Summary: Speech Dispatcher text-to-speech engine for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description speechd
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%if %{with flite}
Requires: qt6-qtspeech-flite
%endif
Requires: qt6-qtspeech-speechd
%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1


%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%files
%license LICENSES/GPL* LICENSES/LGPL* LICENSES/BSD*
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%{_qt6_libdir}/libQt6TextToSpeech.so.6{,.*}
%dir %{_qt6_plugindir}/texttospeech
%{_qt6_plugindir}/texttospeech/libqtexttospeech_mock.so
%dir %{_qt6_qmldir}/QtTextToSpeech
%{_qt6_qmldir}/QtTextToSpeech/*
%dir %{_qt6_libdir}/cmake/Qt6TextToSpeech

%if %{with flite}
%files flite
%{_qt6_plugindir}/texttospeech/libqtexttospeech_flite.so
%{_qt6_libdir}/cmake/Qt6TextToSpeech/Qt6QTextToSpeechFlitePlugin*.cmake
%endif

%files speechd
%{_qt6_plugindir}/texttospeech/libqtexttospeech_speechd.so
%{_qt6_libdir}/cmake/Qt6TextToSpeech/Qt6QTextToSpeechSpeechdPlugin*.cmake

%files devel
%dir %{_qt6_headerdir}/QtTextToSpeech
%{_qt6_headerdir}/QtTextToSpeech/*
%{_qt6_libdir}/libQt6TextToSpeech.so
%{_qt6_libdir}/libQt6TextToSpeech.prl
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6TextToSpeech
%dir %{_qt6_libdir}/cmake/Qt6TextToSpeechPrivate
%{_qt6_libdir}/cmake/Qt6TextToSpeech/*.cmake
%{_qt6_libdir}/cmake/Qt6TextToSpeechPrivate/*.cmake
%{_qt6_libdir}/pkgconfig/Qt6TextToSpeech.pc
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_texttospeech*.pri
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/qt6/metatypes/*.json

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

%changelog
* Mon Feb 09 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Thu Sep 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Thu Aug 28 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Wed Mar 26 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0~rc-2
- Make -devel to require -flite and -speechd plugins

* Mon Mar 24 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0~rc-1
- 6.9.0 RC

* Fri Jan 31 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-1
- 6.8.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-2
- Move Software Bill of Materials from -devel

* Thu Nov 28 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-1
- 6.8.1

* Fri Oct 11 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Tue Oct 10 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Wed Aug 09 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.2-3
- Separate flite and speechd subpackages

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 21 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-3
- Rebuild for qtbase private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-2
- Rebuild for qtbase private API version change

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Tue Apr 04 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Mon Feb 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- Initial package
