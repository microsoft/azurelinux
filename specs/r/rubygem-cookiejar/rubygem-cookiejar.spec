# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name cookiejar	

Name: rubygem-%{gem_name}
Version: 0.3.3
Release: 20%{?dist}
Summary: Parsing and returning cookies in Ruby
# Automatically converted from old format: BSD - review is highly recommended.
License: LicenseRef-Callaway-BSD	
URL: https://github.com/dwaite/cookiejar
Source0: https://rubygems.org/gems/cookiejar-%{version}.gem
# Remove rspec-collection_matchers dependency.
# https://github.com/dwaite/cookiejar/pull/36
Patch0: rubygem-cookiejar-0.3.3-Remove-rspec-collection_matchers-dependency.patch
# https://github.com/dorianmariefr/cookiejar2/pull/2
Patch1: cookiejar2-pr2-fix-regexp-3rd-arg.patch
# Ref: https://github.com/ruby/uri/issues/125
# Use URI::RFC2396_Parser explicitly for ruby34 (uri 1.0.1)
Patch2: cookiejar-uri-1_0-use-rfc2396_regexp-explicitly.patch
BuildRequires: rubygem(rspec)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildArch: noarch

%description
The Ruby CookieJar is a library to help manage client-side cookies in pure
Ruby. It enables parsing and setting of cookie headers, alternating between
multiple 'jars' of cookies at one time (such as having a set of cookies for
each browser or thread), and supports persistence of the cookies in a JSON
string.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n %{gem_name}-%{version}

%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install


%check
pushd ./%{gem_instdir}
rspec -Ilib spec
popd	

%install

mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/contributors.json
%{gem_spec}
%license %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/%{gem_name}.gemspec
%exclude %{gem_instdir}/spec

%files doc
%{gem_docdir}  
%doc %{gem_instdir}/README.markdown
%{gem_instdir}/Rakefile
%{gem_instdir}/Gemfile

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 12 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.3.3-17
- Use URI::RFC2396_Parser explicitly for ruby34 (uri 1.0.1)

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.3.3-16
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 19 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.3.3-12
- Fix for Regexp.new 3rd argument deprecation (needed for ruby 3.3)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Pavel Valena <pvalena@redhat.com> - 0.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 05 2021 Vít Ondruch <vondruch@redhat.com> - 0.3.3-5
- Remove rspec-collection_matchers dependency.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Pavel Valena <pvalena@redhat.com> - 0.3.3-1
- Update to cookiejar 0.3.3.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild


* Tue Jun 24 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-5
- Updated to latest upstream release

* Wed May 28 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-4
- Added conditional for F19/F20

* Sat Mar 15 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-3
- Updated to comply with Fedora guidelines

* Thu Mar 6 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-2
- Updated as per the Fedora guidelines

* Sat Jan 11 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-1
- Initial package
