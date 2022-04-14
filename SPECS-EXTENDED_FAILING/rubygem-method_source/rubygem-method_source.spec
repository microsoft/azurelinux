%global gem_name method_source
%global debug_package %{nil}
Summary: Retrieve the source code for a method
Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 4%{?dist}
License: MIT
URL: http://banisterfiend.wordpress.com
Source0: https://github.com/banister/method_source/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0: fix-gemspec.patch

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
Retrieve the source code for a method

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install %{gem_name}-%{version}.gem
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{gem_dir}/cache
cp -a /%{gem_dir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gem_dir}/cache/
cp -a /%{gem_dir}/doc/%{gem_name}-%{version} %{buildroot}%{gem_dir}/
cp -a /%{gem_dir}/extensions %{buildroot}%{gem_dir}/gems/
mkdir -p %{buildroot}%{gem_dir}/specifications
cp -a /%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gem_dir}/specifications/
cp -a /%{gem_dir}/gems/%{gem_name}-%{version} %{buildroot}%{gem_dir}/gems/

%check
pushd .%{gem_instdir}
rspec spec
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_dir}/%{gem_name}-%{version}

%files doc
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.markdown
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Rakefile
%{gem_instdir}/method_source.gemspec
%{gem_instdir}/spec

%changelog
* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.0-4
- License verified.
- Build from .tar.gz source.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 30 04:22:11 CET 2020 Pavel Valena <pvalena@redhat.com> - 1.0.0-1
- Update to method_source 1.0.0.
  Resolves: rhbz#1495844

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 14 2017 Jun Aruga <jaruga@redhat.com> - 0.8.2-5
- Fix Fixnum/Bignum deprecated warning for Ruby 2.4.0.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 24 2015 Vít Ondruch <vondruch@redhat.com> - 0.8.2-1
- Update to method_source 0.8.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 0.8.1-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to method_source 0.8.1.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 31 2012 Vít Ondruch <vondruch@redhat.com> - 0.8-1
- Update to method_source 0.8.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.7.1-2
- Mark LICENSE as a %%doc.

* Wed May 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.7.1-1
- Initial package
