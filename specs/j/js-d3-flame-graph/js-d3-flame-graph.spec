# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         pkgname d3-flame-graph
%global         github https://github.com/spiermar/d3-flame-graph

Name:           js-d3-flame-graph
Version:        4.0.7
Release: 12%{?dist}
Summary:        A D3.js plugin that produces flame graphs

BuildArch:      noarch

License:        Apache-2.0
URL:            %{github}

Source0:        %{github}/archive/%{version}/%{pkgname}-%{version}.tar.gz
# Note: In case there were no changes to this tarball, the NVR of this tarball
# lags behind the NVR of this package.
Source1:        js-d3-flame-graph-vendor-%{version}-1.tar.xz
Source2:        Makefile
Source3:        list_bundled_nodejs_packages.py

Patch1:         001-remove-unused-frontend-crypto-and-patch-md4.patch

BuildRequires:  web-assets-devel
BuildRequires:  nodejs

%if 0%{?fedora}
Requires:       web-assets-filesystem
%endif

# Bundled npm packages
Provides: bundled(npm(babel-preset-env)) = 1.7.0
Provides: bundled(npm(clean-webpack-plugin)) = 3.0.0
Provides: bundled(npm(copy-webpack-plugin)) = 5.1.1
Provides: bundled(npm(css-loader)) = 3.5.2
Provides: bundled(npm(d3-array)) = 2.4.0
Provides: bundled(npm(d3-dispatch)) = 1.0.6
Provides: bundled(npm(d3-ease)) = 1.0.6
Provides: bundled(npm(d3-format)) = 1.4.4
Provides: bundled(npm(d3-hierarchy)) = 1.1.9
Provides: bundled(npm(d3-scale)) = 3.2.1
Provides: bundled(npm(d3-selection)) = 1.4.1
Provides: bundled(npm(d3-transition)) = 1.3.2
Provides: bundled(npm(eslint)) = 6.8.0
Provides: bundled(npm(eslint-config-standard)) = 14.1.1
Provides: bundled(npm(eslint-loader)) = 4.0.0
Provides: bundled(npm(eslint-plugin-import)) = 2.20.2
Provides: bundled(npm(eslint-plugin-node)) = 11.1.0
Provides: bundled(npm(eslint-plugin-promise)) = 4.2.1
Provides: bundled(npm(eslint-plugin-standard)) = 4.0.1
Provides: bundled(npm(html-webpack-plugin)) = 4.2.0
Provides: bundled(npm(jest)) = 25.4.0
Provides: bundled(npm(prettier)) = 2.0.4
Provides: bundled(npm(script-ext-html-webpack-plugin)) = 2.1.4
Provides: bundled(npm(style-loader)) = 1.1.4
Provides: bundled(npm(terser-webpack-plugin)) = 1.4.3
Provides: bundled(npm(webpack)) = 4.42.1
Provides: bundled(npm(webpack-cli)) = 3.3.11
Provides: bundled(npm(webpack-dev-server)) = 3.10.3

%description
A D3.js plugin that produces flame graphs from hierarchical data.


%package doc
Summary: Documentation and example files for js-d3-flame-graph

%description doc
Documentation and example files for js-d3-flame-graph.


%prep
%setup -q -T -D -b 0 -n %{pkgname}-%{version}
%setup -q -T -D -b 1 -n %{pkgname}-%{version}

%patch -P1 -p1


%build
./node_modules/.bin/webpack --mode production


%install
install -d -m 755 %{buildroot}/%{_datadir}/%{pkgname}
mv dist/templates/* %{buildroot}/%{_datadir}/%{pkgname}
rmdir dist/templates

install -d -m 755 %{buildroot}/%{_jsdir}/%{pkgname}
cp -a dist/* %{buildroot}/%{_jsdir}/%{pkgname}


%check
./node_modules/.bin/jest


%files
%{_jsdir}/%{pkgname}
%{_datadir}/%{pkgname}

%license LICENSE
%doc README.md


%files doc
%doc README.md examples


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Nathan Scott <nathans@redhat.com> - 4.0.7-5
- Switch to SPDX license string

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 01 2021 Andreas Gerstmayr <agerstmayr@redhat.com> - 4.0.7-1
- update to 4.0.7 tagged upstream community sources, see CHANGELOG

* Wed Sep 29 2021 Andreas Gerstmayr <agerstmayr@redhat.com> - 3.0.2-5
- change webpack hash function to sha256
- remove unused cryptographic implementations

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar 20 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 3.0.2-1
- initial version
