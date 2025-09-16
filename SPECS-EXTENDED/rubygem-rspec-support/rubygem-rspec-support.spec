Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global	gem_name	rspec-support

%global	mainver	3.13.1
%undefine	prever

%global	need_bootstrap_set	0

%undefine __brp_mangle_shebangs

Name:		rubygem-%{gem_name}
Version:	%{mainver}
Release:	3%{?dist}

Summary:	Common functionality to Rspec series
# SPDX confirmed
License:	MIT
URL:		https://github.com/rspec/rspec-support
Source0:	https://github.com/rspec/rspec-support/archive/refs/tags/v%{version}.tar.gz#/rubygem-%{gem_name}-%{version}.tar.gz
# tweak regex for search path
Patch100:	rubygem-rspec-support-3.2.1-callerfilter-searchpath-regex.patch

#BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
%if %{without bootstrap}
BuildRequires:	rubygem(rspec)
BuildRequires:	rubygem(thread_order)
BuildRequires:	rubygem(bigdecimal)
# spec/rspec/support/spec/shell_out_spec.rb -> lib/rspec/support/spec/library_wide_checks.rb
# -> rake (%%check)
BuildRequires:	rubygem(rake)
BuildRequires:	git
%endif

BuildArch:		noarch

%description
`RSpec::Support` provides common functionality to `RSpec::Core`,
`RSpec::Expectations` and `RSpec::Mocks`. It is considered
suitable for internal use only at this time.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}

%global	version_orig	%{version}
%global	version	%{version_orig}%{?prever}

%prep
%autosetup -n %{gem_name}-%{version} -p1

%build
# UTF-8 is needed
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%check
LANG=C.UTF-8

# Test failure needs investigation...
FAILFILE=()
FAILTEST=()
%if 0
FAILFILE+=("spec/rspec/support/differ_spec.rb")
FAILTEST+=("copes with encoded strings")
%endif

for ((i = 0; i < ${#FAILFILE[@]}; i++)) {
	sed -i \
		-e "\@${FAILTEST[$i]}@s|do$|, :broken => true do|" \
		${FAILFILE[$i]}
}

ruby -rrubygems -Ilib/ -S rspec spec/ || \
	ruby -rrubygems -Ilib/ -S rspec --tag ~broken

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/LICENSE.md
%doc	%{gem_instdir}/Changelog.md
%doc	%{gem_instdir}/README.md

%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}

%changelog
* Fri Jan 17 2025 Archana Shettigar <v-shettigara@microsoft.com> - 3.13.1-3
- Initial Azure Linux import from Fedora 41 (license: MIT).
- Switch to build from .tar.gz
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 25 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.13.1-1
- 3.13.1

* Fri Feb 09 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.13.0-1
- 3.13.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul  1 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.1-1
- 3.12.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Dec 11 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.0-3
- Backport upstrem patch for pending broken test with ruby >= 3.1.3

* Fri Dec  2 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.0-2
- Pull upstream patch (under review) for ruby filer deadlock treatment

* Thu Oct 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.12.0-1
- 3.12.0

* Thu Sep 15 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.11.1-1
- 3.11.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Feb 10 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.11.0-1
- 3.11.0

* Sat Jan 29 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.3-2
- BR: rubygem(rake) for %%check

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.3-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov  4 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.3-1
- 3.10.3

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb  1 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.2-1
- 3.10.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 29 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.1-1
- 3.10.1

* Fri Dec 11 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.0-1
- Enable tests again

* Fri Dec 11 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.10.0-0.1
- 3.10.0
- Once disable test for bootstrap

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.3-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May  3 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.3-1
- 3.9.3


* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.2-1
- 3.9.2

* Mon Dec 30 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.1-1
- 3.9.1

* Tue Dec 10 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.0-2
- Enable tests again

* Tue Dec 10 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.9.0-0.1
- 3.9.0
- Once disable test for bootstrap

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.2-1
- 3.8.2

* Tue Feb  5 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.0-2
- Backport upstream patch for ruby 2.6 changes

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 13 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.0-1
- Enable tests again

* Wed Dec 12 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.8.0-0.1
- 3.8.0
- Once disable test for bootstrap

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.7.1-1.2
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb  9 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.1-1
- 3.7.1

* Mon Nov 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.0-1
- Enable tests again

* Mon Nov 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.7.0-0.1
- 3.7.0
- Once disable tests

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat May  6 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.0-1
- Enable tests again

* Sat May  6 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.6.0-0.1
- 3.6.0
- Once disable tests

* Tue Feb 21 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-3
- Always use full tar.gz for installed files and
  keep using gem file for gem spec (ref: bug 1425220)

* Fri Feb 03 2017 Jun Aruga <jaruga@redhat.com> - 3.5.0-2
- Fix for Ruby 2.4.0 compatibility.

* Sun Jul 24 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-1
- Enable tests again

* Sat Jul 23 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.5.0-0.1
- 3.5.0
- Once disable tests

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-2
- Enable tests again

* Tue Dec  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-1
- 3.4.1
- Once disable tests

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.0-2
- Enable tests again

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.0-1
- 3.3.0
- Once disable tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.2-1
- 3.2.2

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-2
- Enable tests again

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-1
- 3.2.1
- Once disable tests

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-3
- Enable tests again

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-2
- Retry

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-1
- 3.1.2
- Once disable tests

* Fri Aug 15 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.4-1
- 3.0.4

* Thu Aug 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.3-1
- 3.0.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-0.4.beta2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.0.0-0.4.beta1
- 3.0.0 beta 2

* Mon Feb 10 2014 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.0.0-0.2.beta1
- Modify Provides EVR

* Mon Feb 03 2014 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.0.0-0.1.beta1
- Initial package
