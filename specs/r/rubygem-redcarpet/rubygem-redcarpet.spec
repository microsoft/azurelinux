# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name redcarpet

Name:		rubygem-%{gem_name}
Version:	3.6.1
Release: 3%{?dist}

Summary:	A fast, safe and extensible Markdown to (X)HTML parser
# SPDX confirmed
License:	MIT
URL:		http://github.com/vmg/redcarpet
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:	%{gem_name}-%{version}-test-missing-files.tar.gz
# Source1 is created by $ bash %%SOURCE2 %%version
Source2:	%{gem_name}-create-missing-test-files.sh

BuildRequires:	gcc
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	ruby-devel
BuildRequires:	rubygem(test-unit)

%description
A fast, safe and extensible Markdown to (X)HTML parser.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1
cp -p ../%{gem_name}-%{version}.gemspec .

%build
gem build ./%{gem_name}-%{version}.gemspec
%gem_install

# https://github.com/vmg/redcarpet/pull/503
chmod a-x .%{gem_instdir}/ext/redcarpet/html.c

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_bindir}/redcarpet

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} \
	%{buildroot}%{gem_extdir_mri}/

# cleanups
pushd %{buildroot}%{gem_instdir}
# Prevent dangling symlink in -debuginfo.
rm -rf \
	Gemfile \
	Rakefile \
	ext/ \
	test/ \
	%{gem_name}.gemspec \
	%{nil}
popd
rm -f %{buildroot}%{gem_cache}

%check
cp -a test/ .%{gem_instdir}/

pushd .%{gem_instdir}
env \
	RUBYOPT=-Ilib:$(dirs +1)%{gem_extdir_mri}:test \
	ruby -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/COPYING
%doc	%{gem_instdir}/README.markdown

%{_bindir}/redcarpet

%{gem_instdir}/bin
%{gem_libdir}
%{gem_extdir_mri}

%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/CHANGELOG.md
%{gem_instdir}/CONTRIBUTING.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Feb 27 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.1-1
- 3.6.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.0-7
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.0-4
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 30 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.0-2
- 3.6.0
- License changed to MIT (SPDX confimred)
- CVE-2020-26298 is fixed in this version

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-24
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-22
- F-36: rebuild against ruby31
- modernize spec file, especially move %%gem_install to %%build
  to fix FTBFS with package_notes

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Vít Ondruch <vondruch@redhat.com> - 3.3.2-18
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-15
- F-32: rebuild against ruby27

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 3.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 3.3.2-9
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-8
- F-28: rebuild for ruby25

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Vít Ondruch <vondruch@redhat.com> - 3.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Vít Ondruch <vondruch@redhat.com> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Wed Jul 08 2015 Vít Ondruch <vondruch@redhat.com> - 3.3.2-1
- Update to Redcarpet 3.3.2.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 2.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Josef Stribny <jstribny@redhat.com> - 2.1.1-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-4
- Removing conditionals

* Mon May 21 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-3
- Adding newer rdoc build requires to fix rpmdiff issue

* Fri May 18 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-2
- Cleaning up spec to remove patch and rake testing dependency

* Thu Apr 26 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-1
- Initial package
