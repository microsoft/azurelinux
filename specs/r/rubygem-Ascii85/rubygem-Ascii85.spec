# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name Ascii85

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 12%{?dist}
Summary: Ascii85 encoder/decoder
License: MIT
URL: https://github.com/DataWraith/ascii85gem/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
#retrieved from http://rubyforge.org/tracker/index.php?func=detail&aid=29377&group_id=7826&atid=30313
Source1: ascii85.1.pod.tgz 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildRequires: %{_bindir}/pod2man
BuildArch: noarch

%description
Ascii85 provides methods to encode/decode Adobe's binary-to-text encoding of
the same name.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n  %{gem_name}-%{version} -b 1

%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install

pod2man --center "" --release "" --name ASCII85 --utf8 --section=1 ../ascii85.1.pod ../ascii85.1

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

mv %{buildroot}%{gem_instdir}/{History.txt,README.md} ./
rm -rf %{buildroot}%{gem_instdir}/.travis.yml

install -D -m 644 ../ascii85.1 %{buildroot}%{_mandir}/man1/ascii85.1

sed -i 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|' %{buildroot}%{gem_instdir}/bin/ascii85

%check
pushd .%{gem_instdir}
ruby -e 'Dir.glob "./spec/**/*_spec.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/ascii85
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{_mandir}/man1/ascii85.1*

%files doc
%doc History.txt README.md
%doc %{gem_docdir}
%{gem_instdir}/Ascii85.gemspec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Vít Ondruch <vondruch@redhat.com> - 1.1.0-1
- Update to Ascii85 1.1.0.
  Resolves: rhbz#1538845

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Vít Ondruch <vondruch@redhat.com> - 1.0.2-10
- Spec file cleanup.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Miroslav Suchý <msuchy@redhat.com> - 1.0.2-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 09 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.2-1
- 874854 - rebase to Ascii85-1.0.2.gem (msuchy@redhat.com)

* Fri Aug 24 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-7
- add rubygem to BR (msuchy@redhat.com)

* Fri Aug 24 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-6
- do not run test on rhel, where is no rspec (msuchy@redhat.com)

* Fri Aug 24 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-5
- 850469 - in BR do s/perl/pod2man/ (msuchy@redhat.com)
- 850469 - set man generation flags (msuchy@redhat.com)

* Thu Aug 23 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-4
- 850469 do not delete %%{gem_instdir}/bin (msuchy@redhat.com)
- 850469 - pass -KU option better way (msuchy@redhat.com)
- 850469 - edit test suite (msuchy@redhat.com)
- add rspec to BR (msuchy@redhat.com)

* Tue Aug 21 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-3
- add ascii85.1.pod.tgz (msuchy@redhat.com)

* Tue Aug 21 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-2
- tune spec for Fedora (msuchy@redhat.com)

* Tue Aug 21 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-1
- new package built with tito

