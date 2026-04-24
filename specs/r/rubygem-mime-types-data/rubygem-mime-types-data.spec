# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from mime-types-data-3.2016.0521.gem by gem2rpm -*- rpm-spec -*-
%global gem_name mime-types-data

Name: rubygem-%{gem_name}
Version: 3.2023.0218.1
Release: 7%{?dist}
Summary: A registry for information about MIME media type definitions
License: MIT
URL: https://github.com/mime-types/mime-types-data/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch

%description
mime-types-data provides a registry for information about MIME media type
definitions. It can be used with the Ruby mime-types library or other software
to determine defined filename extensions for MIME types, or to use filename
extensions to look up the likely MIME type definitions.


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

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
# There is nothing to test, since this is just the data package.
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/Licence.md
%{gem_instdir}/data
%{gem_libdir}
%{gem_instdir}/types
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Code-of-Conduct.md
%doc %{gem_instdir}/Contributing.md
%doc %{gem_instdir}/History.md
%{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2023.0218.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2023.0218.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2023.0218.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2023.0218.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2023.0218.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 09 2023 Vít Ondruch <vondruch@redhat.com> - 3.2023.0218.1-1
- Update to mime-types-data 3.2023.0218.1.
  Resolves: rhbz#1928283

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2020.1104-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2020.1104-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2020.1104-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2020.1104-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2020.1104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 13 01:30:37 CET 2020 Pavel Valena <pvalena@redhat.com> - 3.2020.1104-1
- Update to mime-types-data 3.2020.1104.
  Resolves: rhbz#1827975

* Fri Oct 30 17:05:11 CET 2020 Pavel Valena <pvalena@redhat.com> - 3.2020.0512-1
- Update to mime-types-data 3.2020.0512.
  Resolves: rhbz#1827975

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2019.1009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 Pavel Valena <pvalena@redhat.com> - 3.2019.1009-1
- Update to mime-types-data 3.2019.1009.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2019.0331-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jul 23 2019 Pavel Valena <pvalena@redhat.com> - 3.2019.0331-1
- Update to mime-types-data 3.2019.0331.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2016.0521-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2016.0521-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2016.0521-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2016.0521-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2016.0521-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jun 30 2016 Vít Ondruch <vondruch@redhat.com> - 3.2016.0521-1
- Initial package
