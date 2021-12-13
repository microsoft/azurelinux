Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           fros
Version:        1.1
Release:        23%{?dist}
Summary:        Universal screencasting frontend with pluggable support for various backends

%global commit 30275a07dab7891b9f31ff115743f67d757c7c1a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

License:        GPLv2+
URL:            https://github.com/mozeq/fros
# this url is wrong, because github doesn't offer a space for downloadable archives :(
Source:         https://github.com/mozeq/fros/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

# git format-patch %%{commit} --topo-order -N -M;
#Patch0001:      0001-Update-the-spec-file-and-release-1.1.patch
# upstream pull request: https://github.com/mozeq/fros/pull/12
Patch0002:      0002-Specify-prototypes-for-used-X11-C-functions.patch
#Patch0003:      0003-Add-Makefile-rules-for-building-rpm-from-local-repos.patch
Patch0004:      0004-Switch-to-XDG_CURRENT_DESKTOP.patch
Patch0005:      0005-Ensure-that-the-right-version-of-Gtk-gets-loaded.patch
Patch0006:      0006-Delay-initialization-of-GNOME-Screencast-D-Bus-proxy.patch
Patch0007:      0007-Add-a-sanity-check-to-recordmydestkop-plugin.patch

BuildArch:      noarch

# '%%autosetup -S git' -> git
BuildRequires: git

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-gobject

%description
Universal screencasting frontend with pluggable support for various backends.
The goal is to provide an unified access to as many screencasting backends as
possible while still keeping the same user interface so the user experience
while across various desktops and screencasting programs is seamless.

%package recordmydesktop
Summary: fros plugin for screencasting using recordmydesktop as a backend
Requires: %{name} = %{version}-%{release}

%description recordmydesktop
fros plugin for screencasting using recordmydesktop as a backend

%package gnome
Summary: fros plugin for screencasting using Gnome3 integrated screencaster
Requires: %{name} = %{version}-%{release}

%description gnome
fros plugin for screencasting using Gnome3 integrated screencaster

%prep
# If you need to use '--exclude' update __scm_apply_git_am as follows (don't
# forget to remove the second % from all macros):
#(see /usr/lib/rpm/macros for more details)
#%%define __scm_apply_git_am(qp:m:) %%{__git} am --exclude Makefile  %%{-q} %%{-p:-p%%{-p*}}
# I am using "git_am" because "git" does not allow to create a new file within
# a patch because the scm "git" uses "git apply && git commit"
%autosetup -n %{name}-%{commit} -S git_am

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
%{__python3} setup.py test


%files
%doc README COPYING
%dir %{python3_sitelib}/pyfros
%{python3_sitelib}/pyfros/*.py*
%dir %{python3_sitelib}/pyfros/__pycache__
%{python3_sitelib}/pyfros/__pycache__/*.cpython-%{python3_version_nodots}.*py*
%dir %{python3_sitelib}/pyfros/plugins
%{python3_sitelib}/pyfros/plugins/__init__.*
%{python3_sitelib}/pyfros/plugins/const.*
%dir %{python3_sitelib}/pyfros/plugins/__pycache__
%{python3_sitelib}/pyfros/plugins/__pycache__/__init__.cpython-%{python3_version_nodots}*.py*
%{python3_sitelib}/pyfros/plugins/__pycache__/const.cpython-%{python3_version_nodots}*.py*
# fros-1.0-py2.7.egg-info
%dir %{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info/*
%{_bindir}/fros
%{_mandir}/man1/%{name}.1*

%files recordmydesktop
%{python3_sitelib}/pyfros/plugins/*recordmydesktop.*
%{python3_sitelib}/pyfros/plugins/__pycache__/*recordmydesktop.cpython-%{python3_version_nodots}.*py*

%files gnome
%{python3_sitelib}/pyfros/plugins/*gnome.*
%{python3_sitelib}/pyfros/plugins/__pycache__/*gnome.cpython-%{python3_version_nodots}.*py*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1-21
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1-20
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1-16
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Mat Booth <mat.booth@redhat.com> - 1.1-14
- Remove hard requirement on retired package 'recordmydesktop'
  rhbz#1509900

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1-11
- Rebuild for Python 3.6

* Thu Dec 15 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1-10
- Own all the bytecompiled files

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 1.1-7
- Rebuilt for Python3.5 rebuild

* Mon Aug 24 2015 Jakub Filak <jfilak@redhat.com> - 1.1-6
- Add recordmydesktop to BRs of the plugin
- Add a sanity check to 'recordmydestkop' plugin
- Delay initialization of GNOME Screencast D-Bus proxy

* Mon Aug 24 2015 Jakub Filak <jfilak@redhat.com> - 1.1-5
- switch to XDG_CURRENT_DESKTOP
- get rid of PyGIWarning: "Gtk was imported without ..."
- Resolves: #1194976

* Wed Jul 29 2015 Jakub Filak <jfilak@redhat.com> - 1.1-4
- specify X11 C functions prototypes
- move byte compiled plugin files to plugin packages
- Resolves: #1244261

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Jakub Filak <jfilak@redhat.com> 1.1-2
- add a Require for GObject
- Related: #1230420

* Tue Jan 27 2015 Jakub Filak <jfilak@redhat.com> 1.1-1
- switch to Python3
- Resolves: #1125200

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug  6 2013 Jiri Moskovcak <jmoskovc@redhat.com> 1.0-4
-  check if X is available rhbz#920206
- Resolves: #920206

* Tue Aug  6 2013 Jiri Moskovcak <jmoskovc@redhat.com> 1.0-3
- fixed exception when no plugin is installed rhbz#993619

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Jiri Moskovcak <jmoskovc@redhat.com> 1.0-1
- initial rpm
