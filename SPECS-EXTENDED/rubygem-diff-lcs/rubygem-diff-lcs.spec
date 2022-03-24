%global debug_package %{nil}
%global gem_name diff-lcs
Vendor:         Microsoft Corporation
Distribution:   Mariner
# %%check section needs rspec-expectations, however rspec-expectations depends
# on diff-lcs.
%{!?_with_bootstrap: %global bootstrap 0}

Name: rubygem-%{gem_name}
Version: 1.3
Release: 10%{?dist}
Summary: Provide a list of changes between two sequenced collections
License: GPLv2+ or Artistic or MIT
URL: https://github.com/halostatue/diff-lcs
Source0: https://github.com/halostatue/diff-lcs/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires: rubygems-devel
%if ! 0%{?bootstrap}
BuildRequires: rubygem(rspec)
%endif
BuildRequires: ruby(release)
BuildArch: noarch

%description
Diff::LCS computes the difference between two Enumerable sequences using the
McIlroy-Hunt longest common subsequence (LCS) algorithm. It includes utilities
to create a simple HTML diff output format and a standard diff-like tool.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install %{gem_name}-%{version}.gem
mkdir -p %{buildroot}%{gem_dir}
cp -a /%{gem_dir}/bin %{buildroot}%{gem_dir}/
cp -a /%{gem_dir}/build_info %{buildroot}%{gem_dir}/gems/
cp -a /%{gem_dir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gem_dir}/
cp -a /%{gem_dir}/doc/%{gem_name}-%{version} %{buildroot}%{gem_dir}/
cp -a /%{gem_dir}/extensions %{buildroot}%{gem_dir}/gems/
cp -a /%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gem_dir}/
cp -a /%{gem_dir}/gems/%{gem_name}-%{version} %{buildroot}%{gem_dir}/gems/

%check
pushd .%{gem_instdir}
rspec spec
popd

%files
%dir %{gem_instdir}
/usr/lib/ruby/gems/bin/htmldiff
/usr/lib/ruby/gems/bin/ldiff
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/License.md
%{gem_instdir}/bin
%license %{gem_instdir}/docs
%{gem_libdir}
%{gem_dir}/%{gem_name}-%{version}
%{gem_dir}/%{gem_name}-%{version}.gem
%{gem_dir}/%{gem_name}-%{version}.gemspec

%files doc
%doc %{gem_instdir}/Code-of-Conduct.md
%doc %{gem_instdir}/Contributing.md
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/Manifest.txt
%{gem_instdir}/autotest
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.3-10
- Build from .tar.gz source.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Vít Ondruch <vondruch@redhat.com> - 1.3-1
- Update to diff-lcs 1.3.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 28 2015 Josef Stribny <jstribny@redhat.com> - 1.2.5-4
- Fix FTBFS: change the way the specs are run

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 19 2015 Vít Ondruch <vondruch@redhat.com> - 1.2.5-2
- Fix test suite for RSpec 3.x comaptibility.

* Tue Jul 01 2014 Julian Dunn <jdunn@aquezada.com> - 1.2.5-1
- Update to 1.2.5 (bz#902240)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 06 2014 Josef Stribny <jstribny@redhat.com> - 1.1.3-4
- Fix licensing

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.3-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Change the dependency to rubygem(rspec).
- Add bootstrap code.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.3-1
- Update to diff-lcs 1.1.3.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-7
- Rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.2-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.2-2
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.2-1
- Package generated by gem2rpm
- Strip useless shebangs
- Fix up License
