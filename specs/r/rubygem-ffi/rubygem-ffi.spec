# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name ffi

Name: rubygem-%{gem_name}
Version: 1.17.0
Release: 5%{?dist}
Summary: FFI Extensions for Ruby
License: BSD-3-Clause
URL: https://github.com/ffi/ffi/wiki
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/ffi/ffi.git --no-checkout
# cd ffi && git archive -v -o ffi-1.17.0-spec.txz v1.17.0 spec/
Source1: %{gem_name}-%{version}-spec.txz
# Fix test suite `Aborted (core dumped)` on ppc64le/s390x
# https://bugzilla.redhat.com/show_bug.cgi?id=2313598
# https://github.com/ffi/ffi/pull/1124
Patch0: rubygem-ffi-1.17.0-Ensure-GC-ing-closures-before-fork.patch
BuildRequires: make
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
# Compiler is required for build of gem binary extension.
# https://fedoraproject.org/wiki/Packaging:C_and_C++#BuildRequires_and_Requires
BuildRequires: gcc
BuildRequires: libffi-devel
BuildRequires: rubygem(rspec) >= 3
BuildRequires: rubygem(bigdecimal)

%description
Ruby-FFI is a ruby extension for programmatically loading dynamic
libraries, binding functions within them, and calling those functions
from Ruby code. Moreover, a Ruby-FFI extension works without changes
on Ruby and JRuby. Discover why should you write your next extension
using Ruby-FFI here[http://wiki.github.com/ffi/ffi/why-use-ffi].

%package doc
Summary: Documentation for %{name}
# The spec/ are MIT licensed.
License: BSD-3-Clause AND MIT
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n  %{gem_name}-%{version} -b 1

pushd %{builddir}
%patch 0 -p1
popd

%build
# Create the gem as gem install only works on a gem file
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
ln -s %{_builddir}/spec spec

# Build the test library with Fedora build options.
pushd spec/ffi/fixtures
make JFLAGS="%{optflags}"
popd

RUBYOPT="-I$(dirs +1)%{gem_extdir_mri}" rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/COPYING
%license %{gem_instdir}/LICENSE
%license %{gem_instdir}/LICENSE.SPECS
%{gem_libdir}
%{gem_instdir}/sig
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/samples
%{gem_instdir}/ffi.gemspec
%{gem_instdir}/rakelib

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Vít Ondruch <vondruch@redhat.com> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Thu Sep 19 2024 Vít Ondruch <vondruch@redhat.com> - 1.17.0-1
- Update to Ruby-FFI 1.17.0
  Resolves: rhbz#2240411

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.15.5-12
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 1.15.5-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Vít Ondruch <vondruch@redhat.com> - 1.15.5-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 27 2022 Vít Ondruch <vondruch@redhat.com> - 1.15.5-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Thu Jan 27 2022 Vít Ondruch <vondruch@redhat.com> - 1.15.5-2
- Disable fork spec broken by recent libffi.
- Re-enable long double test fixed by FFI 1.15.5.

* Thu Jan 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.15.5-2
- F-36: rebuild against ruby31

* Tue Jan 18 2022 Pavel Valena <pvalena@redhat.com> - 1.15.5-1
- Update to ffi 1.15.5.
  Resolves: rhbz#2038923

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 1.15.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Mon Sep 13 2021 Pavel Valena <pvalena@redhat.com> - 1.15.4-1
- Update to ffi 1.15.4.
  Resolves: rhbz#1909309

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Vít Ondruch <vondruch@redhat.com> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Thu Dec 03 2020 Vít Ondruch <vondruch@redhat.com> - 1.13.1-1
- Disable long double test failing on i686.

* Thu Nov 12 22:57:22 CET 2020 Pavel Valena <pvalena@redhat.com> - 1.13.1-1
- Update to ffi 1.13.1.
  Resolves: rhbz#1797215

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Pavel Valena <pvalena@redhat.com> - 1.12.1-1
- Update to ffi 1.12.1.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pavel Valena <pvalena@redhat.com> - 1.10.0-1
- Update to FFI 1.10.0.

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 1.9.23-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 Vít Ondruch <vondruch@redhat.com> - 1.9.23-1
- Update to FFI 1.9.23.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.9.18-6
- Rebuilt for switch to libxcrypt

* Tue Jan 09 2018 Vít Ondruch <vondruch@redhat.com> - 1.9.18-5
- Re-enable rdoc generation.

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.18-4
- F-28: rebuild for ruby25
- Disabling rdoc generation for now to avoid segfault

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 31 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.18-1
- 1.9.18

* Fri Feb 10 2017 Jun Aruga <jaruga@redhat.com> - 1.9.14-3
- Suppress deprecated Fixnum warnings on Ruby 2.4.0.

* Tue Jan 10 2017 Vít Ondruch <vondruch@redhat.com> - 1.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Tue Jan 03 2017 Vít Ondruch <vondruch@redhat.com> - 1.9.14-1
- Update to FFI 1.9.14.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Vít Ondruch <vondruch@redhat.com> - 1.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Sat Oct  3 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.10-1
- 1.9.10

* Mon Jul 20 2015 Vít Ondruch <vondruch@redhat.com> - 1.9.3-7
- Fix dangling symlinks in -debuginfo package.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.9.3-5
- fixed to build on aarch64

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3-4
- Rebuild for ruby 2.2 again

* Thu Jan 15 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.3-3
- Rebuild for ruby 2.2
- Use rspec2 for now

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 05 2014 Dominic Cleal <dcleal@redhat.com> - 1.9.3-1
- Update to FFI 1.9.3

* Sat May  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0-4
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Vít Ondruch <vondruch@redhat.com> - 1.4.0-2
- Use %%{gem_extdir_mri} instead of %%{gem_extdir}.

* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.4.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to FFI 1.4.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.9-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 14 2011 Bryan Kearney <bkearney@redhat.com> - 1.0.9-2
- Fixed the License, it is actually LGPL

* Mon Jun 13 2011 Bryan Kearney <bkearney@redhat.com> - 1.0.9-1
- Bring in 1.0.9 from upstream.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 10 2010 Bryan Kearney <bkearney@redhat.com> - 0.6.2-1
- Power PC fixes from upstream which were found testing 0.6.2

* Mon Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.6.2-1
- Pull in 0.6.2 from upstream

* Mon Feb 22 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-3
- Final updates based on package review

* Tue Feb 16 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-2
- Updates Based on code review comments

* Mon Feb 15 2010 Bryan Kearney <bkearney@redhat.com> - 0.5.4-1
- Initial specfile
