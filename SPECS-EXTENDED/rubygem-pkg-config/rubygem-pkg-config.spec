# Generated from pkg-config-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global	gem_name	pkg-config

%undefine	__brp_mangle_shebangs

Summary:	A pkg-config implementation by Ruby
Name:		rubygem-%{gem_name}
Version:	1.5.7
Release:	2%{?dist}
# SPDX confirmed
License:	LGPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:		https://github.com/rcairo/pkg-config

Source0:	https://github.com/ruby-gnome/%{gem_name}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Observe test failure on test_cflags test_cflags_only_I
# with pkgconf 1.4.2
Patch0:		rubygem-pkg-config-1.4.4-cflags-result-sort.patch

Requires:	ruby(release)
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
# For %%check
BuildRequires:	rubygem(test-unit)
# mkmf.rb requires ruby-devel
BuildRequires:	ruby-devel
BuildRequires:	cairo-devel
Requires:	rubygems
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
This gem contains a pkg-config implementation by Ruby

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}
%gem_install

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}/%{gem_dir}/

pushd %{buildroot}%{gem_instdir}
rm -rf \
	Gemfile \
	Rakefile \
	test/ \
	%{nil}
popd
rm -f %{buildroot}%{gem_cache}

%check
pushd .%{gem_instdir}
ruby test/run-test.rb
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/NEWS.md
%license	%{gem_instdir}/README.rdoc
%license	%{gem_instdir}/LGPL-2.1
%{gem_libdir}/

%{gem_spec}

%files	doc
%{gem_docdir}

%changelog
* Fri Dec 20 2024 Akhila Guruju <v-guakhila@microsoft.com> - 1.5.7-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Oct 25 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.7-1
- 1.5.7

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 19 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.6-1
- 1.5.6

* Tue Sep  5 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.5-1
- 1.5.5

* Thu Aug 31 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.3-1
- 1.5.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.2-1
- 1.5.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 30 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.1-1
- 1.5.1

* Sun Jul 31 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.9-1
- 1.4.9

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.7-1
- 1.4.7

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 19 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.6-1
- 1.4.6

* Fri Feb  5 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.5-1
- 1.4.5

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 23 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.4-1
- 1.4.4

* Tue Aug 11 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.2-1
- 1.4.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Feb 13 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.1-1
- 1.4.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 10 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0-1
- 1.4.0

* Tue Oct 15 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.9-1
- 1.3.9

* Sat Aug 17 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.8-1
- 1.3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr  5 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.7-1
- 1.3.7

* Tue Feb 19 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.4-1
- 1.3.4

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.2-1
- 1.3.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May  2 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-1
- 1.3.1
- Again restore cflags-result-sort.patch due to test failure for
  test_cflags_only_I

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.9-1
- 1.2.9

* Wed Nov  8 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.8-1
- 1.2.8

* Mon Aug 28 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.7-1
- 1.2.7

* Mon Aug 14 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.6-1
- 1.2.6

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 30 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.3-1
- 1.2.3

* Mon May 29 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.2-1
- 1.2.2

* Thu May  4 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.0-1
- 1.2.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 Orion Poplawski <orion@cora.nwra.com> - 1.1.7-3
- Fixup conditionals for EPEL7
- Drop %%defattr()

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan  6 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.7-1
- 1.1.7

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.6-1
- 1.1.6

* Thu Jun 26 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.5-3
- Fix build failure

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 31 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.5-1
- 1.1.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.4-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.4-1
- 1.1.4

* Thu Aug  2 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.3-3
- Fix test failure on test_cflags, test_cflags_only_I with
  recent pkgconfig

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.3-1
- 1.1.3

* Sun Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-3
- F-17: rebuild against ruby 1.9

* Sun Jan 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org>
- Fix test failure with new png

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- F-17: Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 17 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-1
- 1.1.2

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.7-2
- F-15 mass rebuild

* Thu Oct  7 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.7-1
- 1.0.7

* Thu Sep 23 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.6-2
- Add R: rubygems

* Thu Sep 23 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.6-1
- 1.0.6

* Fri Sep 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.3-1
- Initial package
