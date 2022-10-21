%global debug_package %{nil}
%global gem_name metaclass
Summary:        Adds a metaclass method to all Ruby objects
Name:           rubygem-%{gem_name}
Version:        0.0.4
Release:        16%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/floehopper/metaclass/
Source0:        https://github.com/floehopper/metaclass/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
# Make the test suite support MiniTest 5.x.
# https://github.com/floehopper/metaclass/commit/cff40cbace639d3b66d7913d99e74e56f91905b8
Patch0:         rubygem-metaclass-0.0.4-Move-to-Minitest-5.patch
Patch1:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby
BuildRequires:  rubygem(minitest)
BuildArch:      noarch
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Adds a metaclass method to all Ruby objects

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%check
# test_helper.rb currently references bundler, so it is easier to avoid
# its usage at all.
ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Jul 19 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.0.4-16
- Add provides, add missing files, remove doc package

* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.0.4-15
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.0.4-14
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-13
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Vít Ondruch <vondruch@redhat.com> - 0.0.1-1
- Update to metaclass 0.0.4.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.0.1-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 18 2012 Vít Ondruch <vondruch@redhat.com> - 0.0.1-5
- Build for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.1-3
- Move README.md into -doc subpackage and properly mark.

* Tue Oct 04 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.1-2
- Clarified license.

* Mon Oct 03 2011 Vít Ondruch <vondruch@redhat.com> - 0.0.1-1
- Initial package
