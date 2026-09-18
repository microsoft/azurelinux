# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from msgpack-0.5.9.gem by gem2rpm -*- rpm-spec -*-
%global gem_name msgpack

Name: rubygem-%{gem_name}
Version: 1.7.2
Release: 5%{?dist}
Summary: MessagePack, a binary-based efficient data interchange format
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License: Apache-2.0
URL: http://msgpack.org/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# The msgpack gem doesn't ship with the test suite.
# You may check it out like so:
# git clone --no-checkout https://github.com/msgpack/msgpack-ruby
# git -C msgpack-ruby archive -v -o msgpack-1.7.2-spec.txz v1.7.2 spec/
Source1: %{gem_name}-%{version}-spec.txz
# https://github.com/msgpack/msgpack-ruby/commit/0737d2e8edbda1520d97ef1851efa4c2d57b469b
# support ruby3.4 formatting change
Patch0:  msgpack-1.7.2-ruby34-format.patch

BuildRequires: gcc
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires:  rubygem(rspec)
# BuildRequires: rubygem(rake-compiler) < 0.9
# BuildRequires: rubygem(json) < 2
# BuildRequires: rubygem(yard) < 0.9

%description
MessagePack is a binary-based efficient object serialization library. It
enables to exchange structured objects between many languages like JSON. But
unlike JSON, it is very fast and small.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1
(
cd %{builddir}/spec
%patch -P0 -p2
)

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -ar .%{gem_extdir_mri}/{gem.build_complete,%{gem_name}} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

# Disable the test suite for ppc64le
# https://github.com/msgpack/msgpack-ruby/issues/265
%ifnarch ppc64le
%check
pushd .%{gem_instdir}
ln -s %{builddir}/spec spec
rm -rf spec/jruby
rspec -Ilib -I%{buildroot}%{gem_extdir_mri} spec
popd
%endif

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/ChangeLog
%doc %{gem_instdir}/README.md
%{gem_instdir}/msgpack.gemspec

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Vít Ondruch <vondruch@redhat.com> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Thu Nov 14 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.2-2
- Backport upstream fix for ruby34 formating change

* Thu Sep 12 2024 Pavel Valena <pvalena@redhat.com> - 1.7.2-1
- Update to msgpack 1.7.2.
  Resolves: rhbz#2054672
  Resolves: rhbz#2301253

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.4.4-9
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 1.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.4-3
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Feb 06 2022 Pavel Valena <pvalena@redhat.com> - 1.4.4-1
- Update to msgpack 1.4.4.
  Resolves: rhbz#1533462

* Wed Jan 26 2022 Vít Ondruch <vondruch@redhat.com> - 1.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Vít Ondruch <vondruch@redhat.com> - 1.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Wed Aug 05 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.1.0-13
- Minor conditional fixes for ELN

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.0-11
- F-32: rebuild against ruby27

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Mon Aug 13 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.0-7
- Add C compiler as BR

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.1.0-4
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.0-3
- F-28: rebuild for ruby25

* Fri Jul 21 2017 Sandro Bonazzola <sbonazzo@redhat.com> - 1.1.0-2
- Re-applied changes lost during rebase

* Thu Jun 29 2017 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1
- version 1.1.0

* Thu Jan 19 2017 Sandro Bonazzola <sbonazzo@redhat.com> - 0.5.12-2
- Rebuilding adding ppc64le arch

* Fri Sep 16 2016 Rich Megginson <rmeggins@redhat.com> - 0.5.12-1
- update to 0.5.12

* Mon Jan 05 2015 Graeme Gillies <ggillies@redhat.com> - 0.5.11-1
- Initial package
