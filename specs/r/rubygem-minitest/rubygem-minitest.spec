# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from minitest-1.4.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name minitest

Name: rubygem-%{gem_name}
Version: 5.25.5
Release: 102%{?dist}
Summary: minitest provides a complete suite of testing facilities
# README.rdoc
# SPDX confirmed
License: MIT
URL: https://github.com/seattlerb/minitest
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(hoe)
BuildArch: noarch

%description
minitest provides a complete suite of testing facilities supporting
TDD, BDD, mocking, and benchmarking.

minitest/unit is a small and incredibly fast unit testing framework.
It provides a rich set of assertions to make your tests clean and
readable.

minitest/spec is a functionally complete spec engine. It hooks onto
minitest/unit and seamlessly bridges test assertions over to spec
expectations.

minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner. Now you can assert that your newb
co-worker doesn't replace your linear algorithm with an exponential
one!

minitest/mock by Steven Baker, is a beautifully tiny mock (and stub)
object framework.

minitest/pride shows pride in testing and adds coloring to your test
output. I guess it is an example of how to write IO pipes too. :P
minitest/unit is meant to have a clean implementation for language
implementors that need a minimal set of methods to bootstrap a working
test suite. For example, there is no magic involved for test-case
discovery.

minitest doesn't reinvent anything that ruby already provides, like:
classes, modules, inheritance, methods. This means you only have to
learn ruby to use minitest and all of your regular OO practices like
extract-method refactorings still apply.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

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
	.autotest \
	Manifest.txt \
	Rakefile \
	test/ \
	%{nil}
popd

%check
LANG=C.UTF-8
LC_ALL=C.utf8
pushd .%{gem_instdir}

ruby -Ilib:test -e 'Dir.glob "./test/minitest/test_*.rb", &method(:require)'

popd

%files
%license %{gem_instdir}/README.rdoc
%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.rdoc
%{gem_instdir}/design_rationale.rb

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.25.5-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 13 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.25.5-100
- 5.25.5

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.25.4-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.25.4-100
- 5.25.4

* Wed Nov 20 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.25.1-101
- Upstream patch to suppress warning when redefining object_id in ruby34

* Sat Aug 17 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.25.0-100
- 5.25.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.24.1-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 30 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.24.1-100
- 5.24.1

* Fri Jun 21 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.24.0-100
- 5.24.0

* Wed May 22 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.23.1-100
- 5.23.1

* Thu May 16 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.23.0-100
- 5.23.0

* Fri Mar 15 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.22.3-100
- 5.22.3

* Thu Feb 08 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.22.2-100
- 5.22.2

* Tue Feb 06 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.22.0-100
- 5.22.0

* Sun Jan 28 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.21.2-100
- 5.21.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.21.1-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.21.1-200
- 5.21.1

* Thu Sep 14 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.20.0-200
- 5.20.0

* Fri Jul 28 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.19.0-200
- 5.19.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.18.1-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.18.1-200
- 5.18.1

* Sun Mar  5 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.18.0-200
- 5.18.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.17.0-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  1 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.17.0-200
- 5.17.0

* Thu Aug 18 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.16.3-200
- 5.16.3

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.16.2-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul  9 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.16.2-200
- 5.16.2

* Tue Jun 21 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.16.1-200
- 5.16.1

* Sun Jun 19 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.16.0-200
- 5.16.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.0-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 22 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.15.0-200
- 5.15.0

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.4-201
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Feb 28 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.14.4-200
- 5.14.4

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.3-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.14.3-200
- 5.14.3

* Thu Sep 10 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.14.2-200
- 5.14.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.1-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.14.1-200
- 5.14.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.0-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.14.0-200
- 5.14.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-204
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.11.3-202
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun  4 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.11.3-200
- 5.11.3
- Bump release number

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.11.1-100
- 5.11.1

* Fri Jul 28 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.10.3-100
- 5.10.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.2-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.10.2-100
- 5.10.2

* Sat May  6 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.10.1-100
- 5.10.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 28 2016 Greg Hellings <greg.hellings@gmail.com> - 5.8.5-1
- Update to minitest 5.8.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.4-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.8.4-100
- 5.8.4
- Exclude some files

* Wed Oct 21 2015 Vít Ondruch <vondruch@redhat.com> - 5.8.1-1
- Update to minitest 5.8.1.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 01 2014 Vít Ondruch <vondruch@redhat.com> - 5.3.1-1
- Update to minitest 5.3.1.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Josef Stribny <jstribny@redhat.com> - 4.7.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to minitest 4.7.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.10.1-1
- 2.10.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 10 2011 Vít Ondruch <vondruch@redhat.com> - 1.6.0-3
- Removed Rake circular dependency.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0-1
- Update to 1.6.0 (#586505)
- Patch0 removed

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-3
- Drop Requires on hoe, only used by Rakefile (#538303).
- Move Rakefile to -doc (#538303).

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-2
- Better Source (#538303).
- More standard permissions on files.

* Tue Nov 17 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-1
- Initial package
