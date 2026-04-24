# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global	gem_name	http-cookie

Name:		rubygem-%{gem_name}
Version:	1.1.0
Release: 2%{?dist}

Summary:	Ruby library to handle HTTP Cookies based on RFC 6265
License:	MIT
URL:		https://github.com/sparklemotion/http-cookie
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
%dnl Source0:	https://github.com/sparklemotion/%{gem_name}/archive/v%{version}.tar.gz/#/%{gem_name}-%{version}.tar.gz
Source1:	%{gem_name}-%{version}-additional.tar.gz
# Source1 is created by $ bash %%SOURCE2 %%version
Source2:	%{gem_name}-create-missing-files.sh

Requires:	ruby(release)
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
# %%check
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(domain_name)
BuildRequires:	rubygem(sqlite3)
Requires:	ruby(rubygems)
Requires:	rubygem(domain_name)

BuildArch:	noarch

%description
HTTP::Cookie is a Ruby library to handle HTTP Cookies based on RFC 6265.  It
has with security, standards compliance and compatibility in mind, to behave
just the same as today's major web browsers.  It has builtin support for the
legacy cookies.txt and the latest cookies.sqlite formats of Mozilla Firefox,
and its modular API makes it easy to add support for a new backend store.


%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n %{gem_name}-%{version} -b 1
mv ../%{gem_name}-%{version}.gemspec .

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# Clean up
rm -f %{buildroot}%{gem_cache}

%check
cp -a test/ .%{gem_instdir}
pushd .%{gem_instdir}
ruby -Ilib:test:. -e 'Dir.glob("test/test_*.rb").each {|f| require f}'
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/LICENSE.txt
%doc	%{gem_instdir}/README.md

%{gem_libdir}/
%{gem_spec}

%files doc
%doc	%{gem_docdir}/
%doc	%{gem_instdir}/CHANGELOG.md

%changelog
* Fri Oct 03 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.0-1
- 1.1.0

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.8-1
- 1.0.8

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.7-1
- 1.0.7

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 25 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.5-1
- 1.0.5

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.4-1
- 1.0.4

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 05 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.0.3-9
- Minor conditional fix for ELN

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 10 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.3-1
- 1.0.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.2-2
- Add BR: rubygem(sqlite3) for %%check (bug 1022827)

* Thu Oct 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.2-1
- Initial package
