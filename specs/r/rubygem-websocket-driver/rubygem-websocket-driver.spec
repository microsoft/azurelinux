# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from websocket-driver-0.3.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name websocket-driver

Name: rubygem-%{gem_name}
Version: 0.7.5
Release: 16%{?dist}
Summary: WebSocket protocol handler with pluggable I/O
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License: Apache-2.0
URL: http://github.com/faye/websocket-driver-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone --no-checkout https://github.com/faye/websocket-driver-ruby.git
# cd websocket-driver-ruby && git archive -v -o websocket-driver-ruby-0.7.5-tests.txz 0.7.5 spec/
Source1: websocket-driver-ruby-%{version}-tests.txz
# Use port 80 explicitly in tests
# https://github.com/faye/websocket-driver-ruby/pull/88
Patch0: rubygem-websocket-driver-0.7.5-Use-port-80-explicitly-in-tests.patch

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
# Compiler is required for build of gem binary extension.
# https://fedoraproject.org/wiki/Packaging:C_and_C++#BuildRequires_and_Requires
BuildRequires: gcc
BuildRequires: rubygem(base64)
BuildRequires: rubygem(websocket-extensions)
BuildRequires: rubygem(rspec)

%description
This module provides a complete implementation of the WebSocket protocols that
can be hooked up to any TCP library. It aims to simplify things by decoupling
the protocol details from the I/O layer, such that users only need to implement
code to stream data in and out of it without needing to know anything about how
the protocol actually works. Think of it as a complete WebSocket system with
pluggable I/O.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

%check
pushd .%{gem_instdir}

# Copy tests into place (patch does not work with symlinks)
cp -r %{_builddir}/spec .

cat %{PATCH0} | patch -p1

# Bundler
sed -i '/bundler/ s/^/#/' spec/spec_helper.rb

rspec -I$(dirs +1)%{gem_extdir_mri} spec
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%license %{gem_instdir}/LICENSE.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Vít Ondruch <vondruch@redhat.com> - 0.7.5-14
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Sun Nov 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.7.5-13
- Add BR: rubygem(base64) explicitly for ruby34

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 0.7.5-12
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 0.7.5-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Vít Ondruch <vondruch@redhat.com> - 0.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.7.5-4
- F-36: rebuild against ruby31

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Pavel Valena <pvalena@redhat.com> - 0.7.5-1
- Update to websocket-driver 0.7.5.
  Resolves: rhbz#1971168

* Tue May 25 2021 Pavel Valena <pvalena@redhat.com> - 0.7.4-1
- Update to websocket-driver 0.7.4.
  Resolves: rhbz#1964178

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Vít Ondruch <vondruch@redhat.com> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Sat Aug 22 03:35:41 GMT 2020 Pavel Valena <pvalena@redhat.com> - 0.7.3-1
- Update to websocket-driver 0.7.3.
  Resolves: rhbz#1490664

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.5-11
- F-32: rebuild against ruby27

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 0.6.5-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.6.5-5
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.5-4
- F-28: rebuild for ruby25

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 07 2017 Vít Ondruch <vondruch@redhat.com> - 0.6.5-1
- Update to websocket-driver 0.6.5.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Pavel Valena <pvalena@redhat.com> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Thu Jul 07 2016 Jun Aruga <jaruga@redhat.com> - 0.6.4-1
- Update to websocket-driver 0.6.4.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Pavel Valena <pvalena@redhat.com> - 0.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3
- Correct attributes for websocket_mask.so

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 18 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.3.4-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Jul 15 2014 Josef Stribny <jstribny@redhat.com> - 0.3.4-1
- Initial package
