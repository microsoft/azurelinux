# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from regexp_parser-1.7.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name regexp_parser

Name: rubygem-%{gem_name}
Version: 2.5.0
Release: 7%{?dist}
Summary: Scanner, lexer, parser for ruby's regular expressions
License: MIT
URL: https://github.com/ammar/regexp_parser
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/ammar/regexp_parser.git && cd regexp_parser \
# git archive -v -o regexp_parser-2.5.0-specs.tar.gz v2.5.0 spec/
Source1: %{gem_name}-%{version}-specs.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.0.0
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(regexp_property_values)
BuildArch: noarch

%description
A library for tokenizing, lexing, and parsing Ruby regular expressions.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/



%check
pushd .%{gem_instdir}
ln -s %{_builddir}/spec spec

# We don't have 'ice_nine' in Fedora anymore.
sed -i '/ice_nine/ s/^/#/' spec/spec_helper.rb
sed -i -r '/IceNine/ s/IceNine.deep_freeze\((.*)\)/\1/' spec/expression/to_s_spec.rb

rspec spec
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/regexp_parser.gemspec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 08 2022 Vít Ondruch <vondruch@redhat.com> - 2.5.0-1
- Update to regexp_parser 2.5.0.
  Resolves: rhbz#2113702

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 12:24:11 CET 2020 Pavel Valena <pvalena@redhat.com> - 2.0.0-1
- Update to regexp_parser 2.0.0.

* Fri Oct 30 15:34:19 CET 2020 Pavel Valena <pvalena@redhat.com> - 1.8.2-1
- Update to regexp_parser 1.8.2.

* Tue May 26 2020 Pavel Valena <pvalena@redhat.com> - 1.7.1-1
- Initial package
