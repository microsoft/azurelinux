# Generated from kramdown-1.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name kramdown

Name: rubygem-%{gem_name}
Version: 2.5.1
Release: 3%{?dist}
Summary: Fast, pure-Ruby Markdown-superset converter

# SPDX confirmed
License:	MIT
URL:		http://kramdown.gettalong.org
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(minitest) >= 5
BuildRequires:	rubygem(rexml)
BuildRequires:	rubygem(rouge) >= 3.26.0
BuildRequires:	rubygem(test-unit)
%if ! 0%{?rhel}
BuildRequires:	rubygem(stringex)
BuildRequires:	tidy
%endif
Requires:	ruby(release)
Requires:	ruby(rubygems)
BuildArch: noarch

Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
kramdown is yet-another-markdown-parser but fast, pure Ruby,
using a strict syntax definition and supporting several common extensions.

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

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
    %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Move man pages
mkdir -p %{buildroot}%{_mandir}/man1
mv %{buildroot}%{gem_instdir}/man/man1/kramdown.1 \
    %{buildroot}%{_mandir}/man1

# Cleanup
pushd %{buildroot}%{gem_instdir}
rm -rf \
    test/

%check
LANG=C.UTF-8

pushd .%{gem_instdir}

%if 0%{?rhel}
# Avoid unwanted stringex dependency
sed -i test/testcases/block/04_header/with_auto_ids.options \
       -e '\@transliterated_header_ids@s|true|false|'
sed -i \
       test/testcases/block/04_header/with_auto_ids.* \
       -e '\@[Tr]ransliterated@d'
%endif

sed -i.skip test/test_files.rb \
    -e "\@EXCLUDE_LATEX_FILES =@s|^\(.*\)$|\1 'test/testcases/block/04_header/with_auto_ids.text', #texlive 2022|"

export RUBYLIB=$(pwd)/lib
ruby -e 'Dir.glob "./test/test_*.rb", &method(:require)'

popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/COPYING
%doc	%{gem_instdir}/AUTHORS
%doc	%{gem_instdir}/CONTRIBUTERS
%doc	%{gem_instdir}/README.md
%doc	%{gem_instdir}/VERSION

%{_bindir}/kramdown
%{gem_instdir}/bin
%{_mandir}/man1/kramdown.1*

%{gem_libdir}/
%{gem_instdir}/data/

%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}

%changelog
* Thu Apr 17 2025 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.5.1-3
- Initial CBL-Mariner import from Fedora 42 (license: MIT).

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.5.1-1
- 2.5.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  8 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.4.0-5
- Skip one test failing with texlive 2022, due to perhaps font issue

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 30 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.4.0-3
- Remove previous workaround for rpm side change

* Tue Apr 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.4.0-2
- 2.4.0

* Sun Mar 20 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.2-1
- 2.3.2

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jul 25 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.1-3
- Rebuild for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.1-2
- Bump release

* Sun Mar 21 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.1-1
- 2.3.1

* Sun Mar 21 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.0-3
- Apply upstream fix for CVE-2021-28834 (rouge formatter namespace restriction)

* Tue Feb 16 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.0-2
- Use recent packaging style

* Mon Feb  1 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.3.0-1
- 2.3.0
- Speficy rouge version dependency for test suite

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.1-8
- Wrap rexml depedency with fedora release
- Add upstream patch for rouge change
- Add upstream patch to silence warnings from minitest

* Wed Jan 13 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.2.1-7
- Re-add rexml dependency

* Fri Oct  2 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.1-6
- Test suite now failing, rescuing now

* Tue Aug 11 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.1-5
- Release bump

* Mon Aug 10 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.1-4
- Backport upstream patch for CVE-2020-14001 (bug 1858395)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 21 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.1-2
- Remove explicit rexml runtime dependency (bug 1838185)

* Fri May  8 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.1-1
- 2.2.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Wed Sep 11 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.0-6
- Enable more tests

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew JÄ™drzejewski-Szmek <zbyszek@in.waw.pl> - 1.17.0-3
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun  4 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.17.0-1
- 1.17.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 31 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.16.2-1
- 1.16.2

* Thu Sep 14 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.0-1
- 1.15.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.0-1
- 1.14.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.2-1
- 1.13.2

* Sat Dec 31 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.1-1
- 1.13.1

* Wed Aug 17 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.0-1
- 1.12.0

* Thu May  5 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.1-1
- 1.11.1

* Sun Mar  6 2016 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.10.0-1
- 1.10.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct  4 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.0-1
- 1.9.0

* Mon Jul  6 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.0-1
- 1.8.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.0-1
- 1.7.0

* Sun Mar  1 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.0-1
- 1.6.0

* Fri Nov  7 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.0-1
- 1.5.0

* Mon Sep 22 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.2-1
- 1.4.2

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.1-1
- 1.4.1

* Fri Jun 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0-1
- 1.4.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.3-1
- 1.3.3

* Sat Feb 22 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.2-1
- 1.3.2

* Thu Jan 09 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-1
- 1.3.1

* Thu Dec 12 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.0-1
- 1.3.0

* Fri Nov 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.0-1
- Initial package
