Vendor:         Microsoft Corporation
Distribution:   Mariner
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:           nodejs-packaging
Version:        25
Release:        2%{?dist}
Summary:        RPM Macros and Utilities for Node.js Packaging
BuildArch:      noarch
License:        MIT
URL:            https://fedoraproject.org/wiki/Node.js/Packagers
Source0:        https://releases.pagure.org/%{name}/%{name}-fedora-%{version}.tar.xz
ExclusiveArch:  %{nodejs_arches} noarch

BuildRequires:  python3

Requires:       redhat-rpm-config

%description
This package contains RPM macros and other utilities useful for packaging
Node.js modules and applications in RPM-based distributions.


%prep
%autosetup -p 1 -n %{name}-fedora-%{version}


%build
#nothing to do


%install
install -Dpm0644 macros.nodejs %{buildroot}%{macrosdir}/macros.nodejs
install -Dpm0644 nodejs.attr %{buildroot}%{_rpmconfigdir}/fileattrs/nodejs.attr
install -pm0755 nodejs.prov %{buildroot}%{_rpmconfigdir}/nodejs.prov
install -pm0755 nodejs.req %{buildroot}%{_rpmconfigdir}/nodejs.req
install -pm0755 nodejs-symlink-deps %{buildroot}%{_rpmconfigdir}/nodejs-symlink-deps
install -pm0755 nodejs-fixdep %{buildroot}%{_rpmconfigdir}/nodejs-fixdep
install -pm0755 nodejs-setversion %{buildroot}%{_rpmconfigdir}/nodejs-setversion
install -Dpm0644 multiver_modules %{buildroot}%{_datadir}/node/multiver_modules


%check
./test/run


%files
%license LICENSE
%{macrosdir}/macros.nodejs
%{_rpmconfigdir}/fileattrs/nodejs*.attr
%{_rpmconfigdir}/nodejs*
%{_datadir}/node/multiver_modules


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 25-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Wed Sep 02 2020 Stephen Gallagher <sgallagh@redhat.com> - 25-1
- Fix incorrect bundled library detection for Requires

* Tue Sep 01 2020 Stephen Gallagher <sgallagh@redhat.com> - 24-1
- Check node_modules_prod for bundled dependencies

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Stephen Gallagher <sgallagh@redhat.com> - 23-3
- Drop Requires: nodejs(engine)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Tom Hughes <tom@compton.nu> - 23-1
- Ensure nodejs(engine) is required for packages with no dependencies

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul  2 2019 Tom Hughes <tom@compton.nu> - 22-1
- Refactor nodejs.req in more idiomatic Python
- Treat only external dependency links as un-bundled

* Mon Jun 10 2019 Tom Hughes <tom@compton.nu> - 21-1
- Refactor nodejs.prov in more idiomatic Python

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan  5 2019 Tom Hughes <tom@compton.nu> - 20-1
- Fix handling of ^ dependencies for multiversion modules

* Thu Jan  3 2019 Tom Hughes <tom@compton.nu> - 18-1
- Handle =, >= and <= dependencies for multiversion modules

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May  3 2018 Tom Hughes <tom@compton.nu> - 17-1
- Fix version comparators with a space after the operator

* Tue May  1 2018 Tom Hughes <tom@compton.nu> - 16-1
- Rewrite nodejs.req to better match npm versioning rules
- Add tests for nodejs.req and nodejs.prov

* Mon Apr 30 2018 Tom Hughes <tom@compton.nu> - 15-1
- Fix caret dependency ranges

* Thu Apr 12 2018 Tom Hughes <tom@compton.nu> - 14-1
- Only match top level modules for requires and provides generation

* Wed Feb 28 2018 Tom Hughes <tom@compton.nu> - 13-1
- Add %%nodejs_setversion macro

* Fri Feb 23 2018 Tom Hughes <tom@compton.nu> - 12-1
- Port to python 3

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 13 2018 Tom Hughes <tom@compton.nu> - 11-1
- nodesjs.req: use boolean with for range dependencies

* Tue Sep 12 2017 Stephen Gallagher <sgallagh@redhat.com> - 10-1
- Release v10
- Automatically generate Provides for bundled npm dependencies

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 21 2017 Tom Hughes <tom@compton.nu> - 9-3
- switch source URL to pagure

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb  2 2016 Tom Hughes <tom@compton.nu> - 9-1
- nodejs-fixdep: stop --move erroring on missing dependency types

* Sun Jan 31 2016 Tom Hughes <tom@compton.nu> - 8-1
- nodejs-fixdep: add --move option
- nodejs-symlink-deps: add --optional option
- req: generate suggests for optional dependencies

* Mon Nov 16 2015 Tom Hughes <tom@compton.nu> - 7-5
- nodejs-symlink-deps: handle caret in versions

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar  4 2015 Ville Skyttä <ville.skytta@iki.fi> - 7-3
- Install macros in %%{_rpmconfidir}/macros.d where available (#1074279)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 7-1
- nodejs-symlink-deps: fix regression preventing multiply versioned modules from
  being symlinked correctly

* Sat May 24 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 6-1
- nodejs-fixdep: use real option parsing
- nodejs-fixdep: support modifying optionalDependencies and devDependencies
- req: support the caret operator
- nodejs-symlink-deps: add --force option
- nodejs-symlink-deps: add --build alias for --check
- nodejs-fixdep: support converting to caret dependencies
- nodejs-fixdep: support non-dictionary dependency properties
- multiver_modules: add nan

* Mon Jul 29 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 4-1
- handle cases where the symlink target exists gracefully

* Wed Jul 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3-1
- dependencies and engines can be lists or strings too
- handle unversioned dependencies on multiply versioned modules correctly
  (RHBZ#982798)
- restrict to compatible arches

* Fri Jun 21 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2-1
- move multiple version list to /usr/share/node
- bump nodejs Requires to 0.10.12
- add Requires: redhat-rpm-config

* Thu Jun 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1-1
- initial package
