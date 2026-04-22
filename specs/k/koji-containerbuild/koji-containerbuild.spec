# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

%global module koji_containerbuild

%global owner release-engineering
%global project koji-containerbuild

%global commit 1.0.1
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           %{project}
Version:        1.0.1
Release: 15%{?dist}
Summary:        Koji support for building layered container images

# Automatically converted from old format: LGPLv2 - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2
URL:            https://github.com/%{owner}/%{project}
Source0:        https://github.com/%{owner}/%{project}/archive/%{commit}/%{project}-%{commit}.tar.gz
BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires: python3-setuptools

%description
Koji support for building layered container images


%package hub
# Automatically converted from old format: LGPLv2 - review is highly recommended.
License:    LicenseRef-Callaway-LGPLv2
Summary:    Hub plugin that extend Koji to build layered container images
Requires:   koji-containerbuild
Requires:   koji-hub

%description hub
Hub plugin that extend Koji to support building layered container images


%package builder
# Automatically converted from old format: LGPLv2 - review is highly recommended.
License:    LicenseRef-Callaway-LGPLv2
Summary:    Builder plugin that extend Koji to build layered container images
Requires:   koji-builder
Requires:   koji-containerbuild
Requires:   osbs-client
Requires:   python3-urlgrabber
Requires:   python3-dockerfile-parse
Requires:   python3-jsonschema

%description builder
Builder plugin that extend Koji to communicate with OpenShift build system and
build layered container images.

%package -n python3-%{name}-cli
# Automatically converted from old format: LGPLv2 - review is highly recommended.
License:    LicenseRef-Callaway-LGPLv2
Summary:    CLI that communicates with Koji to control building layered container images
Requires:   python%{python3_pkgversion}-koji >= 1.13

%description -n python3-%{name}-cli
Builder plugin that extend Koji to communicate with OpenShift build system and
build layered container images.

%prep
%setup -qn %{name}-%{commit}

%build
%{__python3} setup.py build


%install
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT%{_prefix}/lib/koji-hub-plugins
%{__install} -p -m 0644 %{module}/plugins/hub_containerbuild.py $RPM_BUILD_ROOT%{_prefix}/lib/koji-hub-plugins/hub_containerbuild.py
%{__install} -d $RPM_BUILD_ROOT%{_prefix}/lib/koji-builder-plugins
%{__install} -p -m 0644 %{module}/plugins/builder_containerbuild.py $RPM_BUILD_ROOT%{_prefix}/lib/koji-builder-plugins/builder_containerbuild.py
%{__install} -d $RPM_BUILD_ROOT%{python3_sitelib}/koji_cli_plugins
%{__install} -p -m 0644 %{module}/plugins/cli_containerbuild.py $RPM_BUILD_ROOT%{python3_sitelib}/koji_cli_plugins/cli_containerbuild.py


%files
%{python3_sitelib}/*
%doc docs AUTHORS README.rst
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?_licensedir:%global license %doc}
%endif
%license LICENSE

%files -n python%{python3_pkgversion}-%{name}-cli
%{python3_sitelib}/koji_cli_plugins

%files hub
%{_prefix}/lib/koji-hub-plugins/hub_containerbuild.py*

%files builder
%{_prefix}/lib/koji-builder-plugins/builder_containerbuild.py*


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.1-14
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.1-13
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.0.1-11
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.0.1-9
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.1-7
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.0.1-3
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 12 2022 Kevin Fenzi <kevin@scrye.com> - 1.0.1-1
- Update to 1.0.1. Fixes rhbz#2133987

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.16.0-2
- Rebuilt for Python 3.11

* Sun Apr 10 2022 Kevin Fenzi <kevin@scrye.com> - 0.16.0-1
- Update to 0.16.0. Fixes rhbz#2024390

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Sep 25 2021 Kevin Fenzi <kevin@scrye.com> - 0.13.0-1
- Upgrade to 0.13.0. Fixes rhbz#1819520

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.11.1-3
- Rebuilt for Python 3.10

* Mon Mar 29 2021 David Kirwan <dkirwan@redhat.com> - 0.11.1
- Update to the latest upstream v0.11.1

* Tue Mar 16 2021 David Kirwan <dkirwan@redhat.com> - 0.11.0
- Update to the latest upstream v0.11.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 27 2020 Clement Verna <cverna@fedoraproject.org> - 0.9.0
- Update to latest upstream

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.15-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 17 2019 Clement Verna <cverna@fedoraproject.org> - 0.7.15
- Update to latest upstream

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.13.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.13.1-4
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Clement Verna <cverna@fedoraproject.org> - 0.7.13.1-2
- Build the hub and builder using python3

* Fri May 17 2019 Clement Verna <cverna@fedoraproject.org> - 0.7.13.1-1
- Update to latest upstream

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Clement Verna <cverna@fedoraproject.org> - 0.7.9.1-2
- Make sure we use Python 2 dependency name

* Tue Jul 31 2018 Clement Verna <cverna@fedoraproject.org> - 0.7.9.1-1
- Update to latest upstream
- conditional install for py3
- make CLI proper koji plugin

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.7.7-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Clement Verna <cverna@fedoraproject.org> - 0.7.7-1
- Update to latest upstream
- Added dependency to python2-koji since koji package is now python3

* Fri Oct 06 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 0.7.5-1
- Update to latest upsteam

* Thu Aug 24 2017 Adam Miller <maxamillion@fedoraproject.org> - 0.7.3-1
- Update to latest upstream

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 06 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.6.6-3
- Conditionally fix epel7 python2 deps

* Tue Sep 06 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.6.6-2
- Fix python2 deps for packages that don't provide it yet

* Tue Sep 06 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.6.6-1
- Update to latest upstream
- Remove no longer needed patch for pycurl calls

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2.2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 18 2016 Adam Miller <maxamillion@fedoraproject.org> 0.6.3-1.2
- Switch all python deps to be explicitly python2

* Thu Jun 02 2016 Adam Miller <maxamillion@fedoraproject.org> 0.6.3-1.1
- Rebase popen patch on 0.6.3

* Thu Jun 02 2016 Brendan Reilly <breilly@redhat.com> 0.6.3-1
- Fix task result output (lucarval@redhat.com)
- Handle release parameter (lucarval@redhat.com)

* Wed May 25 2016 Brendan Reilly <breilly@redhat.com> 0.6.2-1
- supply koji_task_id to osbs-client's create_build() (twaugh@redhat.com)
- no need to warn about build result not being JSON (twaugh@redhat.com)
- Use component label in nvr check (vrutkovs@redhat.com)
- Don't check NVR for scratch builds and move nvr check closer to build object
  creation (vrutkovs@redhat.com)
- Don't start the build if package with this NVR already has been built
  (vrutkovs@redhat.com)
- Expose Koji CG build ID in CreateContainerTask (lucarval@redhat.com)

* Fri May 13 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.6.1-1.3
- Handle logs properly in popen patch

* Mon Apr 25 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.6.1-1.2
- Fix patch for popen osbs cmd to get correct json output

* Mon Apr 25 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.6.1-1.1
- Add patch for popen osbs, fix deps for builder

* Mon Apr 11 2016 Brendan Reilly <breilly@redhat.com> 0.6.1-1
- Reinstate _get_repositories() method (fixes #35) (twaugh@redhat.com)
- Add back in bits required for streaming logs (fixes #33) (twaugh@redhat.com)

* Thu Apr 07 2016 Brendan Reilly <breilly@redhat.com> 0.6.0-1
- remove un-necessary code for v2-only CG builds
  (maxamillion@fedoraproject.org)
- runBuilds: add debug for arches (dennis@ausil.us)
- runBuilds make label unique and be able to build archfully (dennis@ausil.us)
- Build process documentation - quick and dirty (pbabinca@redhat.com)

* Mon Mar 14 2016 Pavol Babincak <pbabinca@redhat.com> 0.5.7-1
- Updated docs how to create a release (pbabinca@redhat.com)
- add some post-install instructions (admiller@redhat.com)
- incorporated new osbs api for compression fix (breilly@redhat.com)

* Tue Mar 08 2016 Pavol Babincak <pbabinca@redhat.com> 0.5.6-1
- Backport spec file from Fedora (pbabinca@redhat.com)
- Include docs in MANIFEST.in (pbabinca@redhat.com)
- Use .md extension for build architecture (pbabinca@redhat.com)
- quickfix for downloads always being .tar (breilly@redhat.com)
- Channel override in CLI (pbabinca@redhat.com)
- Build process documentation - quick and dirty (pbabinca@redhat.com)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 04 2015 Pavol Babincak <pbabinca@redhat.com> 0.5.5-1
- Add README.rst to a release (pbabinca@redhat.com)
- Use %%global macro instead of %%define one (pbabinca@redhat.com)
- Require main package in subpackages to always install license file
  (pbabinca@redhat.com)
- Add license directives to subpackages (pbabinca@redhat.com)

* Thu Dec 03 2015 Pavol Babincak <pbabinca@redhat.com> 0.5.4-3
- Simplify inclusion of python modules to get proper owners
  (pbabinca@redhat.com)
- Explicit __python2 definitions on <=rhel6 (pbabinca@redhat.com)
- Explicit use of python2 and BuildRequires on python2-devel
  (pbabinca@redhat.com)
- %%defattr macro isn't needed anymore (pbabinca@redhat.com)
- Use %%license tag for license on RHEL && RHEL <= 6 (pbabinca@redhat.com)
- Fix permissions for CLI binary (pbabinca@redhat.com)
- Wrap package descriptions to make rpmlint happy (pbabinca@redhat.com)
- Replace Requires on osbs with osbs-client (pbabinca@redhat.com)
- Remove koji Requires from the base package (pbabinca@redhat.com)
- Replace koji-builder with koji dependency for cli subpackage
  (pbabinca@redhat.com)
- Specify how release tarballs are created (pbabinca@redhat.com)
- Use build system instead of buildsystem to make rpmlint happy
  (pbabinca@redhat.com)
- Fix name macro in URL (pbabinca@redhat.com)

* Fri Nov 20 2015 Pavol Babincak <pbabinca@redhat.com> 0.5.4-2
- fix spec paths, libdir evals to /usr/lib64/ on 64-bit build hosts which is
  the wrong path for koji plugins (admiller@redhat.com)

* Fri Nov 20 2015 Pavol Babincak <pbabinca@redhat.com> 0.5.4-1
- Reinit curl after fork to properly process incremental logs
  (pbabinca@redhat.com)
- Add support to new LABEL names and make architecture optional
  (pbabinca@redhat.com)
- Fix serious issue: check external rpms for *non*scratch builds
  (pbabinca@redhat.com)
- Catch errors raised by markExternalRPMs and raise it as koji.PostBuildError
  (pbabinca@redhat.com)
- Get list of rpms and repositories only for successful builds
  (pbabinca@redhat.com)
- Download image tarball only if build was successful (pbabinca@redhat.com)
- Log list of all rpms from osbs response as formatted rpm list
  (pbabinca@redhat.com)
- Refactor: get rpm packages to separate method (pbabinca@redhat.com)
- Refactor: get docker repositories to separate method (pbabinca@redhat.com)
- Fail only if build was successful and it haven't generated any tarball
  (pbabinca@redhat.com)
- Improve log write related exception messages (pbabinca@redhat.com)
- Raise ContainerError exceptions when something goes wrong with osbs logs
  (pbabinca@redhat.com)
- Pass branch and push_url from opts to osbs's create_build()
  (pbabinca@redhat.com)
- Uploader process check if child (which fetches logs) finished
  (pbabinca@redhat.com)
- Overall docs about build architecture (pbabinca@redhat.com)
- change log msg level to info (mikem@redhat.com)
- Properly handle empty repositories in osbs response (pbabinca@redhat.com)
- Wait between new connection/fetch logs (pbabinca@redhat.com)
- Use get_build_name() instead of build_id to get osbs build id
  (pbabinca@redhat.com)

* Tue Jul 14 2015 Pavol Babincak <pbabinca@redhat.com> 0.5.3-1
- List repositories in status message of buildContainer task
  (pbabinca@redhat.com)
- Print osbs build id in the error message about failed build
  (pbabinca@redhat.com)
- If not exactly one image was built leave fail to parent (pbabinca@redhat.com)
- Use DockerfileParser class from dockerfile_parse module for parsing
  (pbabinca@redhat.com)
- Download docker logs at the end of the build (pbabinca@redhat.com)
- Try fetch OSBS logs with follow and incrementally upload them
  (pbabinca@redhat.com)
- If final tarball cannot be downloaded log error and continue
  (pbabinca@redhat.com)
- Accept repo URLs in CLI and pass it in builder plugin to osbs
  (pbabinca@redhat.com)
- Improve error message when there were unexpected number of builds
  (pbabinca@redhat.com)
- Fix: correctly format string before passing to ContainerError
  (pbabinca@redhat.com)
- Fix formatting of README.rst (pbabinca@redhat.com)

* Mon Jun 15 2015 Pavol Babincak <pbabinca@redhat.com> 0.5.2-1
- Use BZComponent LABEL instead of Name (pbabinca@redhat.com)

* Fri Jun 12 2015 Pavol Babincak <pbabinca@redhat.com> 0.5.1-1
- Explicit string conversion before urlgrabber.urlgrab() and more logging
  (pbabinca@redhat.com)
- Explicitly set urlgrab ssl verify options which pycurl expects
  (pbabinca@redhat.com)

* Fri Jun 12 2015 Pavol Babincak <pbabinca@redhat.com> 0.5.0-1
- Read LABELs from Dockerfile (pbabinca@redhat.com)

* Fri Jun 12 2015 Pavol Babincak <pbabinca@redhat.com> 0.4.0-1
- Download container image via https (pbabinca@redhat.com)
- Tag package (image) after successful build if not scratch
  (pbabinca@redhat.com)

* Tue Jun 09 2015 Pavol Babincak <pbabinca@redhat.com> 0.3.1-1
- Add missing import imp (pbabinca@redhat.com)

* Mon Jun 08 2015 Pavol Babincak <pbabinca@redhat.com> 0.3.0-1
- Remove code which always overwrote release (pbabinca@redhat.com)
- Removed not used imports (pbabinca@redhat.com)
- Import kojipath from path set via variable not from inspection
  (pbabinca@redhat.com)
- More debug info: list rpm_packages (pbabinca@redhat.com)
- Mock image tarball as we don't get this from the buildsystem (yet)
  (pbabinca@redhat.com)
- Pull getting task options to separate method (pbabinca@redhat.com)
- Pull package (image) whitelist check into separate method
  (pbabinca@redhat.com)
- Reuse image tables and methods for container builds (pbabinca@redhat.com)
- Don't pass build_tag as separate argument to createContainer task
  (pbabinca@redhat.com)

* Wed Jun 03 2015 Pavol Babincak <pbabinca@redhat.com> 0.2.0-2
- Don't require python-distutils. distutils is part of python-libs pkg
  (pbabinca@redhat.com)

* Wed May 27 2015 Pavol Babincak <pbabinca@redhat.com> 0.2.0-1
- Explicitly list code which are hack around database constraints
  (pbabinca@redhat.com)
- refactor: remove not used code and move comment to better position
  (pbabinca@redhat.com)
- Get name from name of the basename repository for non-scratch builds
  (pbabinca@redhat.com)
- Extend SCM object with get_component() and get_git_uri() and use it
  (pbabinca@redhat.com)
- Use logger to write logs and not sys.stderr.write (pbabinca@redhat.com)
- Use container_archives not image_archives table (pbabinca@redhat.com)
- Use attributes of BuildResponse object to query responses
  (pbabinca@redhat.com)
- Connect to osbs logger to print more debug info via own logger
  (pbabinca@redhat.com)
- Improve rpm_packages listings (pbabinca@redhat.com)
- Support non-scratch builds with listing of the contents (pbabinca@redhat.com)
- builderplugin: import kojid binary as kojid module (pbabinca@redhat.com)
- builderplugin: Use single handler to OSBS object (pbabinca@redhat.com)

* Mon May 18 2015 Pavol Babincak <pbabinca@redhat.com> 0.1.2-1
- add BuildRoot tag (needed for rhel<6) (mikem@redhat.com)
- use alternate method to import kojihub (mikem@redhat.com)

* Wed May 13 2015 Pavol Babincak <pbabinca@redhat.com> 0.1.1-1
- Documentation for buildContainer task (pbabinca@redhat.com)
- In buildContainer task use "container" channel by default
  (pbabinca@redhat.com)

* Wed May 13 2015 Pavol Babincak <pbabinca@redhat.com> 0.1.0-2
- Bump Release instead of Version (pbabinca@redhat.com)
- Use BuildArch noarch (pbabinca@redhat.com)

* Mon May 04 2015 Pavol Babincak <pbabinca@redhat.com> 0.1.0-1
- first public release
