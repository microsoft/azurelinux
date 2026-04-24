# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global debug_package %{nil}
%global npm_name yarn

%{?nodejs_find_provides_and_requires}

%global enable_tests 1

# don't require bundled modules
%global __requires_exclude_from ^(%{nodejs_sitelib}/yarn/lib/.*|%{nodejs_sitelib}/yarn/bin/yarn(|\\.cmd|\\.ps1|pkg.*))$

%global bundledate 20260126

Name:           yarnpkg
Version:        1.22.22
Release: 17%{?dist}
Summary:        Fast, reliable, and secure dependency management.
License:        BSD-2-Clause
URL:            https://github.com/yarnpkg/yarn
# we need tarball with node_modules
Source0:        %{name}-v%{version}-bundled-%{bundledate}.tar.gz
Source1:        yarnpkg-tarball.sh

# These are applied by yarnpkg-tarball.sh
# yarn-update-jest.prebundle.patch
# yarn-no-commitizen.prebundle.patch
# yarn-no-eslint.prebundle.patch

Patch0:         CVE-2023-26136.patch
Patch1:         CVE-2022-37599.patch
Patch2:         CVE-2024-4067.patch
# https://github.com/yarnpkg/yarn/commit/97731871e674bf93bcbf29e9d3258da8685f3076.patch
Patch3:         CVE-2025-8262.patch
# https://github.com/form-data/form-data/commit/3d1723080e6577a66f17f163ecd345a21d8d0fd0
Patch4:         CVE-2025-8263.patch

ExclusiveArch:  %{nodejs_arches}

BuildRequires:  nodejs-packaging
%if 0%{?fedora}
BuildRequires:  %{_bindir}/npm
%else
BuildRequires:  npm
%endif

%description
Fast, reliable, and secure dependency management.


%prep
%autosetup -p1 -n %{npm_name}-%{version}


%build
# use build script
npm run build


%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}

cp -pr package.json lib bin node_modules \
    %{buildroot}%{nodejs_sitelib}/%{npm_name}

mkdir -p %{buildroot}%{_bindir}
ln -sfr %{buildroot}%{nodejs_sitelib}/%{npm_name}/bin/yarn.js %{buildroot}%{_bindir}/yarnpkg
ln -sfr %{buildroot}%{nodejs_sitelib}/%{npm_name}/bin/yarn.js %{buildroot}%{_bindir}/yarn

# Fix the shebang in yarn.js because brp-mangle-shebangs fails to detect this properly (rhbz#1998924)
sed -e "s|^#!/usr/bin/env node$|#!/usr/bin/node|" \
    -i %{buildroot}%{nodejs_sitelib}/%{npm_name}/bin/yarn.js

# Remove executable bits from bundled dependency tests
find %{buildroot}%{nodejs_sitelib}/%{npm_name}/node_modules \
    -ipath '*/test/*' -type f -executable \
    -exec chmod -x '{}' +


%if 0%{?enable_tests}
%check
%nodejs_symlink_deps --check
if [[ $(%{buildroot}%{_bindir}/yarnpkg --version) == %{version} ]] ; then echo PASS; else echo FAIL && exit 1; fi
if [[ $(%{buildroot}%{_bindir}/yarn --version) == %{version} ]] ; then echo PASS; else echo FAIL && exit 1; fi
%endif


%files
%doc README.md
%license LICENSE
%{_bindir}/yarnpkg
%{_bindir}/yarn
%{nodejs_sitelib}/%{npm_name}/


%changelog
* Tue Jan 27 2026 Sandro Mani <manisandro@gmail.com> - 1.22.22-16
- Refresh bundle, fixes CVE-2025-13465

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.22-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Dec 03 2025 Sandro Mani <manisandro@gmail.com> - 1.22.22-14
- Bump release

* Wed Dec 03 2025 Sandro Mani <manisandro@gmail.com> - 1.22.22-13
- Refresh bundle, fixes CVE-2025-64756

* Tue Sep 30 2025 Sandro Mani <manisandro@gmail.com> - 1.22.22-12
- Regenerate bundle, fixes CVE-2025-59343
- Patch out eslint and commitizen devDependencies to reduce dependencies

* Wed Jul 30 2025 Sandro Mani <manisandro@gmail.com> - 1.22.22-11
- Refresh bundle
- Drop patches obsoleted by new bundle
- Add yarn-update-jest.prebundle.patch to update jest and avoid some vulerable dependencies
- Apply fixes for CVE-2025-8262 and CVE-2025-8263

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.22-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 24 2025 Sandro Mani <manisandro@gmail.com> - 1.22.22-9
- Add CVE-2025-6545_6547.prebundle.patch and regenerate bundle. Fixes CVE-2025-6545 and CVE-2025-6547.

* Wed Jun 04 2025 Sandro Mani <manisandro@gmail.com> - 1.22.22-8
- Refresh bundle tarball for CVE-2025-48387

* Fri Mar 28 2025 Sandro Mani <manisandro@gmail.com> - 1.22.22-7
- Fix CVE-2024-12905

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 15 2024 Sandro Mani <manisandro@gmail.com> - 1.22.22-5
- Update bundled ws (CVE-2024-37890)

* Thu Oct 10 2024 Sandro Mani <manisandro@gmail.com> - 1.22.22-4
- Update bundled elliptic (CVE-2024-48949)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Sandro Mani <manisandro@gmail.com> - 1.22.22-2
- Backport patch for CVE-2024-4067

* Sat Mar 09 2024 Sandro Mani <manisandro@gmail.com> - 1.22.22-1
- Update to 1.22.22

* Mon Feb 19 2024 Sandro Mani <manisandro@gmail.com> - 1.22.21-2
- Backport patches for CVE-2022-37599, CVE-2023-26136, CVE-2023-46234

* Fri Feb 16 2024 Sandro Mani <manisandro@gmail.com> - 1.22.21-1
- Update to 1.22.21

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 03 2023 Sandro Mani <manisandro@gmail.com> - 1.22.19-6
- Rebuild (nodejs20)

* Tue Mar 21 2023 Sandro Mani <manisandro@gmail.com> - 1.22.19-5
- Add patch for CVE-2022-38900, proper fixes for CVE-2021-43138, CVE-2022-3517,
  CVE-2020-7677

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Sandro Mani <manisandro@gmail.com> - 1.22.19-3
- Add patches for CVE-2021-43138, CVE-2022-3517, CVE-2020-7677

* Tue Jan 03 2023 Sandro Mani <manisandro@gmail.com> - 1.22.19-2
- Backport fix for CVE-2021-35065 for bundled glob-parent

* Thu Dec 15 2022 Sandro Mani <manisandro@gmail.com> - 1.22.19-1
- Update to 1.22.19

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 23 2021 zsvetlik@redhat.com - 1.22.17-1
- Update to latest upstream release
- use --force in yarnpkg-tarball.sh to workaround dependency conflincts

* Mon Aug 30 2021 Neal Gompa <ngompa@fedoraproject.org> - 1.22.10-4
- Work around broken brp-mangle-shebangs behavior (see RHBZ#1998924)
- Fix broken macro variable for legacy "nodejs-yarn" binary name (RHBZ#1904279)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 09 2020 zsvetlik@redhat.com - 1.22.10-1
- Update to 1.22.10
- Resolves: RHBZ#1816262, RHBZ#1851876
- Long resolved CVEs, just not mentioned in changelog

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Neal Gompa <ngompa13@gmail.com> - 1.22.4-2
- Ensure Obsoletes + Provides stanza takes effect
- Fix broken author identity in changelog entries

* Tue Apr 14 2020 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.22.4-1
- Rename to yarnpkg, remove symlink-deps macro
- Update to 1.22.4

* Mon Jan 27 2020 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.21.1-1
- Resolves: RHBZ#1627748, #1687099, #1788329
- Update to 1.21.1
- Provides /usr/bin/yarn
- Resolves CVE-2019-10773

* Thu Dec 05 2019 Neal Gompa <ngompa@datto.com> - 1.13.0-4
- Rename nodejs-yarn binary package to yarnpkg (similar to other distros)
- Use nodejs macros consistently throughout spec
- Make the tests fail the build if the tests fail

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 13 2019 Jan Staněk <jstanek@redhat.com> - 1.13.0-2
- Remove executable bits from bundled tests
- Related: rhbz#1674073

* Thu Feb 07 2019 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.13.0-1
- Update

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.9.2-1
- Update to 1.9.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 24 2018 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Wed May 09 2018 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.6.0-1
- Rebase, rebuild with new packaging

* Wed Mar 21 2018 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.5.1-2
- Add requires_exclude_from macro
- rename nodejs-yarnpkg to yarn

* Wed Mar 21 2018 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.5.1-1
- Rebase

* Tue Jan 30 2018 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.4.1-1
- rebase
- package from GH, build with npm

* Tue Dec 05 2017 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.3.2-2
- Add fedora readme so users are able to find renamed commands
- change source url
- rename license according to guidelines

* Mon Nov 27 2017 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.3.2-1
- Initial build
