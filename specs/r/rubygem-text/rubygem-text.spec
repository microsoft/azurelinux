# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global	gem_name	text

Name:		rubygem-%{gem_name}
Version:	1.3.1
Release:	22%{?dist}
Summary:	Collection of text algorithms

# SPDX confirmed
License:	MIT
URL:		http://github.com/threedaymonk/text
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
# Check
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(csv)
Requires:	ruby(release)
Requires:	ruby(rubygems)

BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
A collection of text algorithms: Levenshtein, Soundex, Metaphone, Double
Metaphone, Figlet, Porter Stemming


%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n %{gem_name}-%{version}
mv ../%{gem_name}-%{version}.gemspec .

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -rf \
	Rakefile \
	test/ \
	%{nil}
popd

%check
pushd .%{gem_instdir}
ruby -Ilib:test:. -e 'gem "minitest" ; Dir.glob("test/*_test.rb").each{|f| require f}'
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/README.rdoc
%license	%{gem_instdir}/COPYING.txt

%{gem_libdir}/
%{gem_spec}

%files doc
%doc	%{gem_docdir}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-20
- Add BR: rubygem(csv) explicitly for ruby34

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 23 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-16
- Use minitest5 for test
- Cleanup spec file

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-1
- 1.3.1

* Fri Jun 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.0-1
- 1.3.0

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.3-4
- Force to use minitest ver4 for now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.3-2
- Include license text

* Wed Aug 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.3-1
- 1.2.3

* Sun Aug 25 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.2-1
- Initial package
