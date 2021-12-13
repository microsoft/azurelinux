Vendor:         Microsoft Corporation
Distribution:   Mariner

Summary: GUI test tool and automation framework
Name: dogtail
Version: 0.9.11
Release: 8%{?dist}
License: GPLv2
URL: https://gitlab.com/dogtail/dogtail/
Source0: https://gitlab.com/dogtail/dogtail/raw/released/%{name}-%{version}.tar.gz
BuildArch: noarch

%global _description\
GUI test tool and automation framework that uses assistive technologies to\
communicate with desktop applications.

%description %_description

%package -n python3-dogtail
Summary: GUI test tool and automation framework - python3 installation
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires: python3-pyatspi
Requires: python3-gobject
Requires: python3-cairo
Requires: xorg-x11-xinit
Requires: hicolor-icon-theme

%description -n python3-dogtail
GUI test tool and automation framework that uses assistive technologies to
communicate with desktop applications.

%package -n python3-dogtail-scripts
Summary: Sniff and other scripts for use with Dogtail framework
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: desktop-file-utils
Requires: python3-pyatspi
Requires: python3-gobject
Requires: python3-cairo
Requires: xorg-x11-xinit
Requires: hicolor-icon-theme
Requires: python3-dogtail >= 0.9.11

%description -n python3-dogtail-scripts
GUI test tool and automation framework that uses assistive technologies to
communicate with desktop applications. This subpackage contains Sniff,
the a11y exploration tool as well dogtail-run-headless scripts to start
session to run tests in.


%prep
%setup -q -n %{name}-%{version}


%build

%{__python3} setup.py build

%install
%{__python3} ./setup.py install -O2 --root=$RPM_BUILD_ROOT --record=%{name}.files
rm -rf $RPM_BUILD_ROOT/%{_docdir}/dogtail
rm -rf $RPM_BUILD_ROOT/%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info

find examples -type f -exec chmod 0644 \{\} \;
desktop-file-install $RPM_BUILD_ROOT/%{_datadir}/applications/sniff.desktop \
  --dir=$RPM_BUILD_ROOT/%{_datadir}/applications \

%files -n python3-dogtail
%{python3_sitelib}/dogtail/
%{_datadir}/dogtail/
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%doc COPYING
%doc README
%doc NEWS

%files -n python3-dogtail-scripts
%{_bindir}/*
%{_datadir}/applications/*
%doc COPYING
%doc README
%doc NEWS


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.11-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.11-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.11-5
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.11-2
- Subpackage python2-dogtail has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Nov 12 2018 Vitezslav Humpa <vhumpa@redhat.com> - 0.9.11-1
- Update to upstream version 0.9.11

* Mon Jul 16 2018 Vitezslav Humpa <vhumpa@redhat.com> - 0.9.10-1
- Update to upstream version 0.9.10

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.9-11
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.9.9-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Troy Dawson <tdawson@redhat.com> - 0.9.9-8
- Update conditional

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.9-7
- Python 2 binary package renamed to python2-dogtail
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.9-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Vitezslav Humpa <vhumpa@redhat.com> - 0.9.9-1
- Update to upstream version 0.9.9
- Upstream now supports Python 3, built as python3-dogtail sub-package

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 08 2014 David King <amigadave@amigadave.com> - 0.9.0-3
- Depend on hicolor-icon-theme for icon directory ownership (#1171906)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Vitezslav Humpa <vhumpa@redhat.com> - 0.9.0-1
- Update to upstream version 0.9.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 9 2013 Vitezslav Humpa <vhumpa@redhat.com> - 0.8.2-1
- Update to upstream version 0.8.2

* Sat Feb 23 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.8.1-5
- drop unversioned obsolete

* Sat Feb 23 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.8.1-4
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 18 2012 Vitezslav Humpa <vhumpa@redhat.com> - 0.8.1-2
- Respin

* Tue Oct 16 2012 Vitezslav Humpa <vhumpa@redhat.com> - 0.8.1-1
- New upstream release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-2
- respin

* Thu May 31 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-1
- Update to 0.8.0 Final
- New upstream release

* Mon Apr 16 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-0.5.beta5
- Update to 0.8.0 beta 5

* Mon Apr 02 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-0.2.beta2
- Update to 0.8.0 beta 2

* Mon Mar 19 2012 Jaroslav Reznik <jreznik@redhat.com> - 0.8.0-0.1.beta1
- Update to 0.8.0 beta 1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Oct 08 2009 Zack Cerza <zcerza@redhat.com> - 0.7.0-1
- New upstream release.
- Drop Requires on xorg-x11-server-Xvfb.
- Update URL and Source0.
- Ship NEWS file.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.90-4.401
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.90-3.401
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.90-2.401
- Rebuild for Python 2.6

* Tue Aug 12 2008 Zack Cerza <zcerza@redhat.com> - 0.6.90-1.401
- New upstream snapshot.
- Require python-imaging

* Tue Aug 12 2008 Zack Cerza <zcerza@redhat.com> - 0.6.90-1.381.2
- Really fix license tag.

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.90-1.381.1
- fix license tag

* Thu Jan 31 2008 Zack Cerza <zcerza@redhat.com> - 0.6.90-1.381
- New upstream snapshot.
- Obsolete pyspi; Require at-spi-python.
- Require pygtk2-libglade.
- Don't ship the .egg-info file.

* Wed Jan  3 2007 Zack Cerza <zcerza@redhat.com> - 0.6.1-1
- New upstream release.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.6.0-2
- build for python 2.5
- BR python-devel

* Wed Sep 13 2006 Zack Cerza <zcerza@redhat.com> - 0.6.0-1
- New upstream release.
- Add Requires for xorg-x11-xinit.
- Add Requires for gnome-python2-gconf.
- Bump pyspi Requires.
- Remove upstreamed patches.

* Fri Aug 18 2006 Zack Cerza <zcerza@redhat.com> - 0.5.2-3
- Add Requires for xorg-x11-xinit. Closes: #203189.

* Fri Aug 11 2006 Zack Cerza <zcerza@redhat.com> - 0.5.2-2
- Added headless-gconf.patch to use the python gconf bindings.
- Added desktop-file-categories.patch to put sniff and dogtail-recorder under
  the 'Programming' menu.

* Tue Aug 01 2006 Zack Cerza <zcerza@redhat.com> - 0.5.2-1
- New upstream release.
- Update Requires from Xvfb to xorg-x11-server-Xvfb.
- Bump pyspi Requires.
- Remove ImageMagick Requires.
- Escape post-macro in changelog-macro.

* Mon Apr 17 2006 Zack Cerza <zcerza@redhat.com> - 0.5.1-3
- Fix the URL field.

* Tue Mar 21 2006 Zack Cerza <zcerza@redhat.com> - 0.5.1-2
- Fix URL and Source0 fields.
- Fix desktop-file-utils magic; use desktop-file-install.

* Fri Feb 24 2006 Zack Cerza <zcerza@redhat.com> - 0.5.1-1
- Remove BuildRequires on at-spi-devel. Added one on python.
- Use macros instead of absolute paths.
- Touch _datadir/icons/hicolor/ before running gtk-update-icon-cache.
- Require and use desktop-file-utils.
- postun = post.
- Shorten BuildArchitectures to BuildArch. The former worked, but even vim's
  hilighting hated it.
- Put each *Requires on a separate line.
- Remove __os_install_post definition.
- Use Fedora Extras BuildRoot.
- Instead of _libdir, which kills the build if it's /usr/lib64, use a
  python macro to define python_sitelib and use that.
- Remove the executable bit on the examples in install scriptlet.
- Remove call to /bin/rm in post scriptlet.
- Use dist in Release.

* Fri Feb 17 2006 Zack Cerza <zcerza@redhat.com> - 0.5.0-2
- It looks like xorg-x11-Xvfb changed names. Require 'Xvfb' instead.
- Remove Requires on python-elementtree, since RHEL4 didn't have it. The
  functionality it provides is probably never used anyway, and will most likely
  be removed in the future.
- Don't run gtk-update-icon-cache if it doesn't exist.

* Fri Feb  3 2006 Zack Cerza <zcerza@redhat.com> - 0.5.0-1
- New upstream release.
- Added missing BuildRequires on at-spi-devel.
- Added Requires on pyspi >= 0.5.3.
- Added Requires on rpm-python, pygtk2, ImageMagick, xorg-x11-Xvfb,
  python-elementtree.
- Moved documentation (including examples) to the correct place.
- Make sure /usr/share/doc/dogtail is removed.
- Added 'gtk-update-icon-cache' to %%post.

* Mon Oct 24 2005 Zack Cerza <zcerza@redhat.com> - 0.4.3-1
- New upstream release.

* Sat Oct  8 2005 Jeremy Katz <katzj@redhat.com> - 0.4.2-1
- Initial build.
