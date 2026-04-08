# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global testspec_version 3.6.3
%define with_tests 0

Name:           sassc
Version:        3.6.2
Release:        12%{?dist}
Summary:        Wrapper around libsass to compile CSS stylesheet

License:        MIT
URL:            http://github.com/sass/sassc
Source0:        https://github.com/sass/sassc/archive/%{version}/%{name}-%{version}.tar.gz
# Test suite spec. According to this comment from an upstream dev, we should
# not use the release tags on the test spec:
# https://github.com/sass/libsass/issues/2258#issuecomment-268196004
# https://github.com/sass/sass-spec/archive/master.zip
# https://github.com/sass/sass-spec/archive/v%%{testspec_version}.tar.gz
Source1:        sass-spec-libsass-%{testspec_version}.tar.gz

BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  libsass-devel >= %{version}
BuildRequires:  gcc-c++
%if %{with_tests}
# For the test suite
BuildRequires:  ruby
%if 0%{?epel} && 0%{?epel} <= 7
BuildRequires:  rubygem-minitest5
%else
BuildRequires:  rubygem-hrx
BuildRequires:  rubygem-minitest
%endif
%endif

%description
SassC is a wrapper around libsass used to generate a useful command-line
application that can be installed and packaged for several operating systems.


%prep
%autosetup -a 1
mv sass-spec-libsass-%{testspec_version} sass-spec
autoreconf -fiv


%build
%configure
%make_build 


%install
%make_install

%if %{with_tests}
%check
rm sass-spec/spec/basic/12_pseudo_classes_and_elements.hrx
rm sass-spec/spec/basic/44_bem_selectors.hrx
rm sass-spec/spec/extend-tests/018_test_id_unification.hrx
rm sass-spec/spec/extend-tests/065_test_attribute_unification.hrx
rm sass-spec/spec/extend-tests/066_test_attribute_unification.hrx
rm sass-spec/spec/extend-tests/067_test_attribute_unification.hrx
rm sass-spec/spec/extend-tests/068_test_attribute_unification.hrx
rm sass-spec/spec/extend-tests/070_test_pseudo_unification.hrx
rm sass-spec/spec/extend-tests/071_test_pseudo_unification.hrx
rm sass-spec/spec/extend-tests/074_test_pseudo_unification.hrx
rm sass-spec/spec/extend-tests/087_test_negation_unification.hrx
rm sass-spec/spec/libsass-closed-issues/issue_2520.hrx
ruby sass-spec/sass-spec.rb -c ./%{name} --impl libsass sass-spec/spec
%endif

%files
%license LICENSE
%doc Readme.md
%{_bindir}/%{name}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 06 2023 Leigh Scott <leigh123linux@gmail.com> - 3.6.2-8
- Disable tests

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Leigh Scott <leigh123linux@gmail.com> - 3.6.2-2
- Use configure and enable tests

* Fri May 21 2021 Leigh Scott <leigh123linux@gmail.com> - 3.6.2-1
- Upgrade to 3.6.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Leigh Scott <leigh123linux@gmail.com> - 3.6.1-6
- Disable tests

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 06 2019 Leigh Scott <leigh123linux@googlemail.com> - 3.6.1-2
- Add build requires rubygem-hrx and enable tests for fedora

* Mon Dec 02 2019 Leigh Scott <leigh123linux@gmail.com> - 3.6.1-1
- Upgrade to 3.6.1, tests 3.6.3
- Disable tests they fail due to missing rubygem-hrx

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 19 2018 Kevin Fenzi <kevin@scrye.com> - 3.5.0-1
- Upgrade to 3.5.0, tests 3.5.4. 
- Fixes FTBFS.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Aurelien Bompard <abompard@fedoraproject.org> - 3.4.5-2
- Require the same libsass version

* Mon Jul 24 2017 Aurelien Bompard <abompard@fedoraproject.org> - 3.4.5-1
- Version 3.4.5: https://github.com/sass/sassc/releases/tag/3.4.5

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Aurelien Bompard <abompard@fedoraproject.org> - 3.4.1-1
- Version 3.4.1: https://github.com/sass/sassc/releases/tag/3.4.1

* Mon Dec 12 2016 Aurelien Bompard <abompard@fedoraproject.org> - 3.4.0-1
- Version 3.4.0: https://github.com/sass/sassc/releases/tag/3.4.0

* Tue Aug 23 2016 Aurelien Bompard <abompard@fedoraproject.org> - 3.3.6-1
- initial package
