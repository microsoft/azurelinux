#
# spec file for package golang-packaging
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           golang-packaging
Version:        15.0.17
Release:        1%{?dist}
Summary:        A toolchain to help packaging golang
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Golang
URL:            https://github.com/openSUSE/%{name}
#Source0:       https://github.com/openSUSE/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  rpm
BuildRequires:  xz
Requires:       go
BuildArch:      noarch

%description
A toolchain to help packaging golang, written in bash.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/rpm/
mkdir -p %{buildroot}%{_libdir}/rpm/

install -m0755 golang.prov %{buildroot}%{_libdir}/rpm/
install -m0755 golang.req %{buildroot}%{_libdir}/rpm/
install -m0755 golang.sh %{buildroot}%{_libdir}/rpm/
install -m0644 macros.go %{buildroot}%{_sysconfdir}/rpm/

%files
%defattr(-,root,root)
%doc README.md CHANGELOG
%license COPYING
%{_libdir}/rpm/golang.prov
%{_libdir}/rpm/golang.req
%{_libdir}/rpm/golang.sh
%config %{_sysconfdir}/rpm/macros.go

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 15.0.17-1
- Auto-upgrade to 15.0.17 - Azure Linux 3.0 - package upgrades

* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 15.0.15-2
- Switching to using a single digit for the 'Release' tag.

* Thu Jun 10 2021 Henry Li <lihl@microsoft.com>  15.0.15-1.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License Verified
- Remove distro condition checks that do not apply for CBL-Mariner
- Fix Source0 URL

* Fri Nov 13 2020 jkowalczyk@suse.com
- Update to version 15.0.15:
  * Only create directories that do not yet exist
  * filelelist can try to access source_dir independently

* Wed Nov 11 2020 jkowalczyk@suse.com
- Update to version 15.0.14:
  * Ensure to touch $RPM_BUILD_ROOT only in the various install phases
  * Add support for riscv64

* Fri May 29 2020 jkowalczyk@suse.com
- Update to version 15.0.13:
  * Preserve modification time of source files
- Mark COPYING as %%license on suse_version > 1500

* Sat Nov 16 2019 jkowalczyk@suse.com
- Update to version 15.0.12:
  * Drop ppc64-nopie.patch
  * golang.sh: integrate ppc64-nopie.patch -buildmode=pie only on ppc64
  * golang.sh: avoid excessive "rpm --eval..." calls
  * Install Bazel files in src directory
  * Replace rpmdev-vercmp by "sort -V" to remove rpmdev-vercmp dependency
  * Remove s build flag no longer supported in go 1.10 boo#776058
  * Packaging: improve _service tar_scm declarations add _servicedata

* Wed Jun 13 2018 jmassaguerpla@suse.com
- We don't need to require rpmdev, because we updated to 15.0.11
  to remove that requirement. I missed to remove the req from
  the spec file.

* Tue Jun 12 2018 msuchanek@suse.com
- fix ppc64 (be) build. No pie baking support there.
  + ppc64-nopie.patch

* Mon Jun 11 2018 opensuse-packaging@opensuse.org
- Update to version 15.0.11:
  * Replace rpmdev-vercmp by "sort -V" to remove rpmdev-vercmp dependency

* Thu May 31 2018 opensuse-packaging@opensuse.org
- Update to version 15.0.10:
  * update changelog to v15.0.10
  * This flag does not exist for go 1.10 because this is an extra flag that openSUSE was adding into the go packages in order to fix
  * Revert "only add the s flag if go is less than 1.10"
  * only add the s flag if go is less than 1.10
  * Revert "Pass linker flag via ldflags"
  * update changelog: add 15.0.9 version
  * Pass linker flag via ldflags
  * Bump version 15.0.8
  * Fix the handling of quoted extra args
  * bump version to v15.0.7
- Add Requires rpmdev-tools as this is used to compare versions in the
  golang.sh script

* Tue May 29 2018 opensuse-packaging@opensuse.org
- Update to version 15.0.9:
  * Pass linker flag via ldflags

* Mon Feb 12 2018 opensuse-packaging@opensuse.org
- Update to version 15.0.8:
  * Fix Requires/Provides issue with split packages
  * Remove unused variables
  * Bump version to v15.0.5
  * *: always use -buildmode=pie
  * bump version to v15.0.6
  * fix changelog
  * golang.sh: Fix arch for aarch64
  * bump version to v15.0.7
  * Fix the handling of quoted extra args
  * Bump version 15.0.8

* Wed Aug 30 2017 thipp@suse.de
- Update to version 15.0.7:
  * *: always use -buildmode=pie
  * fix changelog
  * golang.sh: Fix arch for aarch64

* Wed Jun 28 2017 thipp@suse.de
- Update to version 15.0.5:
  * set correct modifier if no arguments are provided
  * Remove duplicates when finding Requires
  * fix GOPATH and macros
  * Fix Provides and Requires for some builds
  * Fix Requires/Provides issue with split packages
  * Remove unused variables

* Wed Jun  7 2017 thipp@suse.de
- Update to version 15.0.4:
  * Handle extra_flags for build/test correctly
  * set correct modifier if no arguments are provided
  * Remove duplicates when finding Requires
  * fix GOPATH and macros
  * Fix Provides and Requires for some builds

* Thu Jun  1 2017 thipp@suse.de
- fix GOPATH for Provides and Requires

* Wed May 24 2017 thipp@suse.de
- Fix all %%go_*dir macros

* Tue May 23 2017 thipp@suse.de
- fix GOPATH issue

* Sun May 21 2017 jmassaguerpla@suse.com
- fix gopath after updating go to 1.8. With go 1.8, there is no more
  /usr/share/go/contrib but /usr/share/go/1.8/contrib
  gopath.patch: contains the fix

* Wed Mar 29 2017 thipp@suse.de
- Update to version 15.0.3:
  * Remove duplicates when finding Requires
  * bump version to v15.0.3

* Wed Mar 22 2017 thipp@suse.de
- Update to version 15.0.2:
  * set correct modifier if no arguments are provided
  * bump version to v15.0.2

* Tue Mar 14 2017 thipp@suse.de
- Update to version 15.0.1:
  * Handle extra_flags for build/test correctly
  * bump version to v15.0.1

* Wed Feb 15 2017 thipp@suse.de
- Update to version 15.0.0:
  * [SLE11]some commands need time to finish, immediate close will get wrong status, so use timeout 30s
  * [SLE]ditch named group in regexp in golang.req, the oniguruma in ruby 1.8.7 doesn't support named group
  * fix a typo in cli.rb
  * increate timeout to 300s or go install can't finish
  * Remove runtime dependency for Go API
  * simplify rpmsysinfo.rb
  * release 14.9.1
  * Added go_nostrip macro
  * Refactor using plain bash
  * small fixes

* Fri Jul 22 2016 tboerger@suse.com
- Added refactoring.patch while trying new code base
- Dropped the sed for static architecture detection
- Updated files list to reflect new file structure

* Fri Jul  8 2016 i@marguerite.su
- can't be noarch. we detected %%%%go_arch at build time. it has to be
  architecture-dependent, or it'll be published randomly with one
  from i586/x86_64, whose content (/etc/rpm/macros.go) is unique.

* Tue Jun 21 2016 tboerger@suse.com
- Update to version 14.9.2:
  + [SLE11]some commands need time to finish, immediate close will get wrong status, so use timeout 30s
  + [SLE]ditch named group in regexp in golang.req, the oniguruma in ruby 1.8.7 doesn't support named group
  + fix a typo in cli.rb
  + increate timeout to 300s or go install can't finish
  + Remove runtime dependency for Go API
  + simplify rpmsysinfo.rb
  + release 14.9.1
  + Added go_nostrip macro

* Wed Jun  8 2016 i@marguerite.su
- Update to version 14.9.1:
  * simplify rpmsysinfo.rb: don't guess variables'
    values can be passed in by RPM environment
    variables. use RbConfig to get libdir.
  * support s390x architecture

* Sun Apr 17 2016 mpluskal@suse.com
- Update service
  * use xz for compression
  * change from disabled to localonly
- Update spec file to actually use tarball generated by _service
- Drop useless _servicedata

* Fri Apr 15 2016 tboerger@suse.com
- Switched to service based package updates
- Update to version 14.9.0:
  * do not hardcode go version
  * fix encoding problem in rpmsysinfo.rb
  * [SLE11]some commands need time to finish, immediate close will get wrong status, so use timeout 30s
  * [SLE]ditch named group in regexp in golang.req, the oniguruma in ruby 1.8.7 doesn't support named group
  * fix a typo in cli.rb
  * increate timeout to 300s or go install can't finish
  * Remove runtime dependency for Go API

* Tue Apr  5 2016 i@marguerite.su
- update version 14.8.1
  * bugfix release
  * fix a typo in cli.rb
  * increate timeout to 300s, or go install can't
    finish itself sometimes

* Sun Apr  3 2016 i@marguerite.su
- update version 14.8
  * rpmsysinfo.rb: fix encoding problem in open()
  * cli.rb: ruby 1.8.7 doesn't support passing environment
    variables in popen(), some commands/tests need time to
    finish, an immediate io.close() will get us wrong
    exitstatus (broken pipe, code 13). so use 'timeout'
    module with a 30s and process.wait for them to quit
    successfully.
  * golang.req: the oniguruma in ruby 1.8.7 doesn't support
    named group in regexp. so ditch the named group used in
    go_get_version()

* Wed Feb 24 2016 i@marguerite.su
- update version 14.7
  * do not hardcode go version

* Fri Feb 12 2016 i@marguerite.su
- update version 14.6
  * Fix rbarch for Power architectures

* Fri Jan 22 2016 i@marguerite.su
- update version 14.5
  * fix a typo that prevent golang.req from running (fix #10)

* Fri Jan 22 2016 i@marguerite.su
- update version 14.4
  * fix #5 on golang.req

* Tue Jan 19 2016 i@marguerite.su
- update version 14.3
  * fix: command not found error for go test on SLE
  * fix #5 again: gsub importpath itself is not enough

* Mon Jan 11 2016 i@marguerite.su
- update version 14.2
  * golang.req: fix ' // indirect' comment in import

* Mon Jan 11 2016 i@marguerite.su
- update version 14.1
  * golang.prov fix: uniq! returns nil if everything is unique

* Tue Jan  5 2016 i@marguerite.su
- update version 14
  * if importpath has "test/example", it should survive (github#5)
  * merge macros.go from openSUSE's go here
  * add golang-macros.rb, replacement for the complicated
    macros in shell in macros.go
  * golang-macros.rb:
    + support build with fake build id
    + support build with custom tags (github#7)
    + support pass any -<arg>="a b c" or -<arg>=<value>
    to go install, shared build is possible now
    (not fully support, other macros need to be adapted)
    + --filelist, to generate filelist used in %%files
    section with excluding support
    + use IO.popen to break the build at the exact place
    it fails (github#6)

* Mon Jan  4 2016 i@marguerite.su
- update version 13
  * provides the importpath itself
  * fix regex not to check files like .golden in -source
  * filter "test/example" from Provides
  * split common stuff to a module golang/rpmsysinfo.rb
  * rewrite golang.req, now read from stdin RPM feeds,
    and check __.PKGDEF from .a files for "import"s. (github#3, github#4)

* Sun Jan  3 2016 i@marguerite.su
- update version 12
  * don't find provides/requires on -source, -debuginfo, -debugsource
    subpackages
  * add scripts to generate file lists.

* Sat Jan  2 2016 i@marguerite.su
- update version 11
  * fix for sles and openSUSE < 13.2

* Fri Sep  4 2015 i@marguerite.su
- update version 10
  * support all archtectures like ppc/arm

* Fri Aug 28 2015 i@marguerite.su
- update version 9
  * update golang(API) to 1.5

* Sun Aug  2 2015 i@marguerite.su
- update version 8
  * skip the last "/" in golang.prov, thanks to matwey

* Fri Jul 31 2015 i@marguerite.su
- udpate version 7
  * handle gopkg.in/* requirements

* Fri Jul 24 2015 i@marguerite.su
- update version 6
  * fix golang.req to not treat a sentence as importpath
  * fix golang.attr to correctly detect /usr/bin/*

* Wed Jul 22 2015 i@marguerite.su
- update version 5
  * if a sub-directory doesn't contain any *.go file, do not
    treat it as a Provides candidate.
  * add /usr/bin to golang.attr for go executes to be handled
    by golang-packaging

* Sun Jul 12 2015 i@marguerite.su
- update version 4
  * fix encoding error in golang-strip-builddep
  * add macros.go-extra, extra golang macros for packaging

* Sat Jul 11 2015 i@marguerite.su
- update version 3
  * skip *example*.go/*test*.go for Requires finding
  * support alias format (import xx "xxx") for importpath
  * add golang-strip-builddep, a tool to strip unneeded importpath
    from source codes

* Fri Jul 10 2015 i@marguerite.su
- update version 2
  * fix pkgname detection

* Sun Jul  5 2015 i@marguerite.su
- initial version 1
  * implemented provides
  * implemented requires
