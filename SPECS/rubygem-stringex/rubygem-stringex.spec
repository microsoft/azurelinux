%global gem_name stringex

Name:           rubygem-%{gem_name}
Summary:        Useful extensions to Ruby's String class
Version:        2.8.6
Release:        6%{?dist}
# SPDX confirmed
License:        MIT

URL:            http://github.com/rsl/stringex
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildArch:      noarch

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby

BuildRequires:  rubygem(activerecord)
BuildRequires:  rubygem(i18n)
BuildRequires:  rubygem(RedCloth)
BuildRequires:  rubygem(sqlite3)
BuildRequires:  rubygem(test-unit)

%description
Some [hopefully] useful extensions to Ruby's String class. Stringex is made up
of three libraries: ActsAsUrl [permalink solution with better character
translation], Unidecoder [Unicode to ASCII transliteration], and
StringExtensions [miscellaneous helper methods for the String class].


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}

BuildArch:      noarch

%description    doc
Documentation for %{name}.


%prep
%setup -q -n %{gem_name}-%{version}

# Relax unstable time-dependent test strictness
sed -i test/performance/localization_performance_test.rb \
	-e 's|allowed_difference = 25|allowed_difference = 99|'

%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -rf \
	Gemfile \
	Rakefile \
	stringex.gemspec \
	test/ \
	%{nil}
popd

%check
pushd .%{gem_instdir}
ruby -I'lib:test' -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd


%files
%license %{gem_instdir}/MIT-LICENSE

%dir %{gem_instdir}
%{gem_instdir}/VERSION
%{gem_instdir}/init.rb
%{gem_instdir}/locales

%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Thu Apr 17 2025 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.8.6-6
- Initial CBL-Mariner import from Fedora 42 (license: MIT).

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 20 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8.6-1
- 2.8.6
- SPDX confirmed

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 11 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8.5-10
- Workaround for test failure with ruby3.2 wrt remove_method failure

* Fri Aug 12 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8.5-9
- Relax unstable time-dependent test strictness

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Feb 14 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8.5-5
- Patch to make test suite compatible with rails 6.1.x

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 26 2019 Fabio Valentini <decathorpe@gmail.com> - 2.8.5-1
- Initial package
