Vendor:         Microsoft Corporation
Distribution:   Mariner
%{?nodejs_find_provides_and_requires}
%global npm_name nodemon

# Disable until dependencies are met
%global enable_tests 0

Name:          nodejs-%{npm_name}
Version:       2.0.3
Release:       4%{?dist}
Summary:       Simple monitor script for use during development of a node.js app
License:       MIT
URL:           https://github.com/remy/nodemon
Source0:       %{_mariner_sources_url}/%{npm_name}-v%{version}-bundled.tar.gz

BuildRequires: nodejs-devel
BuildRequires: nodejs-packaging

ExclusiveArch: %{nodejs_arches} noarch
BuildArch:     noarch

%if 0%{?enable_tests}
BuildRequires:  npm(async)
BuildRequires:  npm(coffee-script)
BuildRequires:  npm(husky)
BuildRequires:  npm(istanbul)
BuildRequires:  npm(jscs)
BuildRequires:  npm(mocha)
BuildRequires:  npm(proxyquire)
BuildRequires:  npm(semantic-release)
BuildRequires:  npm(should)
%endif

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
cp -pr doc bin lib package.json website node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}

mkdir -p %{buildroot}%{_bindir}
ln -sf %{nodejs_sitelib}/%{npm_name}/bin/nodemon.js %{buildroot}%{_bindir}/nodemon


#%%nodejs_symlink_deps

%if 0%{?enable_tests}
%check
%nodejs_symlink_deps --check
npm run test
%endif

%files
%license LICENSE
%doc CODE_OF_CONDUCT.md doc faq.md README.md
%{nodejs_sitelib}/%{npm_name}
%{_bindir}/nodemon

%changelog
* Mon May 15 2023 Olivia Crain <oliviacrain@microsoft.com> - 2.0.3-4
- Remove explicit build-time dependency on npm (provided by nodejs-devel)

* Tue Apr 26 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 2.0.3-3
- Updated source URL.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.3-2
- Initial CBL-Mariner import from CentOS 8 (license: MIT).

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
