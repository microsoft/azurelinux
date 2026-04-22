# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global	gem_name	contracts

Name:		rubygem-%{gem_name}
Version:	0.17.3
Release: 2%{?dist}

Summary:	Contracts for Ruby
# SPDX confirmed
License:	BSD-2-Clause
URL:		http://egonschiele.github.io/contracts.ruby/
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	ruby
BuildRequires:	rubygem(rspec) >= 3
BuildArch:		noarch

%description
This library provides contracts for Ruby. Contracts let you clearly express
how your code behaves, and free you from writing tons of boilerplate,
defensive code.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}
mv ../%{gem_name}-%{version}.gemspec .

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -rf \
	.[^.]* \
	Gemfile \
	Rakefile \
	*gemspec \
	*yml \
	features/ \
	script/ \
	spec/ \
	%{nil}

%check
pushd .%{gem_instdir}
rspec spec/
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/LICENSE
%doc		%{gem_instdir}/CHANGELOG.markdown
%doc		%{gem_instdir}/README.md
%doc		%{gem_instdir}/TODO.markdown
%doc		%{gem_instdir}/TUTORIAL.md

%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_docdir}
# Keep this
%{gem_instdir}/benchmarks/

%changelog
* Tue Dec 30 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.17.3-1
- 0.17.3

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 26 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.17.2-2
- Workaround for ruby34 hash inspect format change

* Fri Oct 18 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.17.2-1
- 0.17.2

* Tue Oct 08 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.17.1-1
- 0.17.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 29 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.17-8
- SPDX migration

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct  4 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.17-5
- Fix for ruby3.2 wrt Fixnum removal

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May  8 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.17-1
- 0.17

* Sat May  1 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.16.1-1
- 0.16.1

* Sun Feb 28 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.16.0-11
- Add conditional for eln

* Sun Jan 31 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.16.0-10
- Backport some patches from the upstream
- Ruby 3.0: apply the upstream WIP patch for keyword separation

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May  5 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.16.0-1
- 0.16.0

* Fri Mar 17 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.15.0-1
- 0.15.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Sep 10 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.0-2
- Remove features/ directory from packaging

* Thu Aug 18 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.14.0-1
- Initial package
