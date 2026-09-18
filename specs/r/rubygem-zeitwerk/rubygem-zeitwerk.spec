# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from zeitwerk-2.1.10.gem by gem2rpm -*- rpm-spec -*-
%global gem_name zeitwerk

Name: rubygem-%{gem_name}
Version: 2.6.6
Release: 7%{?dist}
Summary: Efficient and thread-safe constant autoloader
License: MIT
URL: https://github.com/fxn/zeitwerk
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Test suite is not included in packaged gem
# git clone https://github.com/fxn/zeitwerk.git --no-checkout
# cd zeitwerk && git archive -v -o zeitwerk-2.6.6-tests.txz v2.6.6 test
Source2: %{gem_name}-%{version}-tests.txz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Zeitwerk implements constant autoloading with Ruby semantics. Each gem
and application may have their own independent autoloader, with its own
configuration, inflector, and logger. Supports autoloading, preloading,
reloading, and eager loading.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b2

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/test .

# focus gem is not needed for tests
sed -i '/require..minitest.focus./ s/^/#/' test/test_helper.rb
# Remove minitest-reporters. It does not provide any additional value while
# it blows up the dependency chain.
sed -i '/require..minitest.reporters./ s/^/#/' test/test_helper.rb
sed -i '/Minitest::Reporters/ s/^/#/' test/test_helper.rb

# Skip failing test
# https://github.com/fxn/zeitwerk/issues/202
sed -i '/returns true for a file in a descendant of an ignored directory/ a \
  skip' test/lib/zeitwerk/test_ignore.rb

ruby -Itest:lib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%license %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.6.6-1
- 2.6.6
  - ruby3.2 needs at least 2.6.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Feb 06 2022 Pavel Valena <pvalena@redhat.com> - 2.5.4-1
- Update to zeitwerk 2.5.4.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 07 2021 Vít Ondruch <vondruch@redhat.com> - 2.4.2-3
- Drop `BR: rubygem(minitest-reporters)`.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 10:16:11 CET 2020 Pavel Valena <pvalena@redhat.com> - 2.4.2-1
- Update to zeitwerk 2.4.2.

* Fri Oct 30 19:47:19 CET 2020 Pavel Valena <pvalena@redhat.com> - 2.4.1-1
- Update to zeitwerk 2.4.1.

* Wed Aug 19 16:28:46 GMT 2020 Pavel Valena <pvalena@redhat.com> - 2.4.0-1
- Update to zeitwerk 2.4.0.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 21 2020 Pavel Valena <pvalena@redhat.com> - 2.3.0-1
- Update to zeitwerk 2.3.0.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Pavel Valena <pvalena@redhat.com> - 2.2.1-1
- Update to zeitwerk 2.2.1.

* Tue Sep 24 2019 Pavel Valena <pvalena@redhat.com> - 2.1.10-1
- Initial package
