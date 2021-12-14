Vendor:         Microsoft Corporation
Distribution:   Mariner
%global gem_name liquid

Name:           rubygem-%{gem_name}
Summary:        Secure, non-evaling end user template engine
Version:        4.0.3
Release:        5%{?dist}
License:        MIT

URL:            http://www.liquidmarkup.org
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

# Disable running stack profiler in the test suite
Patch0:         00-test-unit-context-disable-stack-profiler.patch

# Remove shebang and executable bit from the test_helper.rb
Patch1:         01-test-helper-remove-shebang-and-executable-bit.patch

# Disable two tests that are broken with ruby 2.7
Patch2:         02-tests-integration-drop_test-disable-tests-broken-wit.patch

BuildArch:      noarch

BuildRequires:  ruby(release)
BuildRequires:  ruby >= 2.1.0
BuildRequires:  rubygems-devel >= 1.3.7

BuildRequires:  rubygem(bigdecimal)
BuildRequires:  rubygem(minitest)

Requires:       rubygem(bigdecimal)

%description
Liquid is a template engine which was written with very specific requirements:
* It has to have beautiful and simple markup. Template engines which don't
  produce good looking markup are no fun to use.
* It needs to be non evaling and secure. Liquid templates are made so that
  users can edit them. You don't want to run code on your server which your
  users wrote.
* It has to be stateless. Compile and render steps have to be separate so that
  the expensive parsing and compiling can be done once and later on you can
  just render it passing in a hash with local variables and objects.


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    doc
Documentation for %{name}.


%prep
%setup -q -n %{gem_name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
ruby -I"lib:test" -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd


%files
%license %{gem_instdir}/LICENSE

%dir %{gem_instdir}
%{gem_libdir}
%{gem_spec}

%exclude %{gem_cache}


%files doc
%doc %{gem_instdir}/History.md
%doc %{gem_instdir}/README.md

%doc %{gem_docdir}

%{gem_instdir}/test


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.0.3-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fabio Valentini <decathorpe@gmail.com> - 4.0.3-4
- Disable two tests that are broken with ruby 2.7.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Fabio Valentini <decathorpe@gmail.com> - 4.0.3-1
- Update to version 4.0.3.

* Sat Mar 09 2019 Fabio Valentini <decathorpe@gmail.com> - 4.0.2-1
- Update to version 4.0.2.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 09 2018 Fabio Valentini <decathorpe@gmail.com> - 4.0.1-1
- Update to version 4.0.1.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 07 2018 Fabio Valentini <decathorpe@gmail.com> - 4.0.0-1
- Update to version 4.0.0.
- Add BR: rubygem(spy) and run the test suite.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May 13 2016 Vít Ondruch <vondruch@redhat.com> - 3.0.1-4
- Explicitly specify dependency on rubygem(bigdecimal).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.1-1
- Update to latest upstream release (RHBZ #1186292)

* Wed Jan 07 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.0-2
- Add "Ruby" to License tag (RHBZ #1038274)
- Create a dummy "spy/integration" lib so we can run the tests during %%check
  (RHBZ #1038274)

* Wed Dec 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.0-1
- Update to latest upstream release
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Use %%license tag
- Unconditionally pass tests until rubygem-spy is available

* Wed Dec 04 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.6.0-1
- Initial package

