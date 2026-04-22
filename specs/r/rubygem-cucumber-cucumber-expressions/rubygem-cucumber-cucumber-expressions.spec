# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from cucumber-expressions-6.0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name cucumber-cucumber-expressions

Name: rubygem-%{gem_name}
Version: 17.1.0
Release: 5%{?dist}
Summary: A simpler alternative to Regular Expressions
License: MIT
URL: https://github.com/cucumber/cucumber-expressions
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Upstream removed LICENSE file from packages.
# https://github.com/cucumber/cucumber-expressions/issues/292
# Taken from:
# https://github.com/cucumber/cucumber-expressions/blob/v17.1.0/LICENSE
Source1: LICENSE
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: %{_bindir}/rspec
BuildRequires: rubygem(rspec-expectations)
BuildRequires: rubygem-bigdecimal
BuildArch: noarch

# Provides: can be removed in F36+2, i.e. F38
Provides: rubygem-cucumber-expressions = %{version}-%{release}
Obsoletes: rubygem-cucumber-expressions < 6.0.1-10

%description
Cucumber Expressions - a simpler alternative to Regular Expressions.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install

install -m 644 %{SOURCE1} .%{gem_instdir}/LICENSE

# The methods with question marks were replaced with attr_reader(s) in 17.0.0.
# They were getters already. To keep compatibility with cucumber v7.
# simply aliasing the methods on the correct place is enough.
# Related: https://github.com/cucumber/cucumber-expressions/pull/234
sed -i -e '/attr_reader :name, :type/ a    alias :prefer_for_regexp_match? :prefer_for_regexp_match' \
       -e '/attr_reader :name, :type/ a    alias :use_for_snippets? :use_for_snippets' \
          .%{gem_libdir}/cucumber/cucumber_expressions/parameter_type.rb

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
rspec spec
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%{gem_spec}

%exclude %{gem_instdir}/.*
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/VERSION
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/cucumber-cucumber-expressions.gemspec
%{gem_instdir}/spec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 17.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 17.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 17.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Mar 21 2024 Packit <hello@packit.dev> - 17.1.0-1
- Update to 17.1.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Jarek Prokop <jprokop@redhat.com> - 14.0.0-1
- Rename rubygem-cucumber-expressions to rubygem-cucumber-cucumber-expressions
- Upgrade rubygem-cucumber-cucumber-expressions

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018 jackorp <jar.prokop@volny.cz> - 6.0.1-1
- Initial package
