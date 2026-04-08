# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from webrick-1.7.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name webrick

Name: rubygem-%{gem_name}
Version: 1.9.0
Release: 3%{?dist}
Summary: HTTP server toolkit
License: Ruby AND BSD-2-Clause
URL: https://github.com/ruby/webrick
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Test suite is not packaged with the gem, you may check out it like so:
# git clone --no-checkout https://github.com/ruby/webrick
# cd webrick && git archive -v -o webrick-1.9.0-tests.txz v1.9.0 test
Source1: %{gem_name}-%{version}-tests.txz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.4.0
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(test-unit-ruby-core)
BuildArch: noarch

%description
WEBrick is an HTTP server toolkit that can be configured as an HTTPS server, a
proxy server, and a virtual-host server.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Symlink the test suite.
ln -s %{_builddir}/test .

# Use --verbose to set $VERBOSE to true. `test_sni` in test/webrick/test_https.rb
# relies on output in $stderr from lib/webrick/ssl.rb that is only written there
# if $VERBOSE is true.
# https://github.com/ruby/webrick/pull/158
ruby --verbose           \
     -Ilib:test:test/lib \
     -rhelper            \
     -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/sig
%{gem_instdir}/webrick.gemspec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 21 2024 Jarek Prokop <jprokop@redhat.com> - 1.9.0-1
- Upgrade to webrick 1.9.0.
  Resolves: CVE-2024-47220

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 2020 Pavel Valena <pvalena@redhat.com> - 1.7.0-1
- Initial package
