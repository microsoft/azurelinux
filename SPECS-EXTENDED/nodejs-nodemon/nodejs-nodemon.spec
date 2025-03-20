Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%{?nodejs_find_provides_and_requires}
%global npm_name nodemon

# Disable until dependencies are bundled
%global enable_tests 0

Name:          nodejs-%{npm_name}
Version:       3.1.4
Release:       3%{?dist}
Summary:       Simple monitor script for use during development of a node.js app
License:       ISC AND MIT
URL:           https://github.com/remy/nodemon
#Source0:       %{npm_name}-v%{version}-bundled.tar.gz
Source0:       https://github.com/remy/nodemon/archive/refs/tags/v3.1.4.tar.gz#/%{npm_name}-v%{version}-bundled.tar.gz
BuildRequires: nodejs-devel
BuildRequires: nodejs-packaging
BuildRequires: npm

ExclusiveArch: %{nodejs_arches} noarch
BuildArch:     noarch

%description
Simple monitor script for use during development of a node.js app.

For use during development of a node.js based application.

nodemon will watch the files in the directory in which nodemon
was started, and if any files change, nodemon will automatically
restart your node application.

nodemon does not require any changes to your code or method of
development. nodemon simply wraps your node application and keeps
an eye on any files that have changed. Remember that nodemon is a
replacement wrapper for node, think of it as replacing the word "node"
on the command line when you run your script.

%prep
%setup -q -n %{npm_name}-%{version}

%build

# nothing to do
# tarball is bundled in --production mode, so no need to prune

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pr doc bin lib package.json website %{buildroot}%{nodejs_sitelib}/%{npm_name}

mkdir -p %{buildroot}%{_bindir}
ln -sf %{nodejs_sitelib}/%{npm_name}/bin/nodemon.js %{buildroot}%{_bindir}/nodemon


#%%nodejs_symlink_deps

%if 0%{?enable_tests}
%check
%nodejs_symlink_deps --check
npm run test
%endif

%files
%doc CODE_OF_CONDUCT.md doc faq.md README.md
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/nodemon

%changelog
* Fri Mar 19 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 3.1.4-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Jan Staněk <jstanek@redhat.com> - 3.1.4-1
- Update to version 3.1.4 (rhbz#2290334)

* Fri May 31 2024 Jan Staněk <jstanek@redhat.com> - 3.1.2-1
- Update to version 3.1.2 (rhbz#2284031)

* Tue May 28 2024 Jan Staněk <jstanek@redhat.com> - 3.1.1-1
- Update to 3.1.1 (rhbz#2283282)

* Mon Mar 18 2024 Honza Horak <hhorak@redhat.com> - 3.1.0-1
- update to 3.1.0

* Fri Feb 09 2024 Honza Horak <hhorak@redhat.com> - 3.0.3-2
- SPDX conversion

* Fri Feb 09 2024 Honza Horak <hhorak@redhat.com> - 3.0.3-1
- update to version 3.0.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 11 2023 Jan Staněk <jstanek@redhat.com> - 3.0.1-1
- update to version 3.0.1

* Wed Aug 09 2023 Honza Horak <hhorak@redhat.com> - 2.0.3-9
- Let nodemon work with any Node.js version
  Resolves: #2230317

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 01 2020 Honza Horak <hhorak@redhat.com> - 2.0.3-1
- Update to 2.0.3

* Mon Aug 13 2018 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.18.3-1
- Resolves: #1615413
- Updated
- bundled

* Mon Jul 03 2017 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.11.0-2
- rh-nodejs8 rebuild

* Mon Oct 31 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.11.0-1
- Updated with script

* Sun Feb 14 2016 Zuzana Svetlikova <zsvetlik@redhat.com> - 1.8.1-6
- rebuilt

* Wed Jan 06 2016 Tomas Hrcka <thrcka@redhat.com> - 1.8.1-5
- Enable scl macros

* Thu Dec 17 2015 Troy Dawson <tdawson@redhat.com> - 1.8.1-2
- Fix dependencies

* Wed Dec 16 2015 Troy Dawson <tdawson@redhat.com> - 1.8.1-1
- Initial package
