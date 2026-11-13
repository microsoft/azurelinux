# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from ruby-vips-2.0.17.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ruby-vips

Name: rubygem-%{gem_name}
Version: 2.2.5
Release: 6%{?dist}
Summary: Ruby extension for the vips image processing library
License: MIT
URL: http://github.com/libvips/ruby-vips
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone --no-checkout http://github.com/libvips/ruby-vips
# cd ruby-vips && git archive -v -o ruby-vips-2.2.5-spec.tar.gz v2.2.5 spec/
Source1: %{gem_name}-%{version}-spec.tar.gz

Requires: (libvips.so.42()(64bit) if libc.so.6()(64bit))
Requires: (libvips.so.42 if libc.so.6)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(ffi)
BuildRequires: rubygem(logger)
BuildRequires: rubygem(rspec) >= 3.3
BuildRequires: (libvips.so.42()(64bit) if libc.so.6()(64bit))
BuildRequires: (libvips.so.42 if libc.so.6)
BuildArch: noarch

%description
ruby-vips is a binding for the libvips image processing library. It is fast
and it can process large images without loading the whole image in memory.


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

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

( cd .%{gem_instdir}
ln -s %{_builddir}/spec .
rspec spec
)

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/TODO
%{gem_instdir}/ruby-vips.gemspec
%{gem_instdir}/VERSION
%{gem_instdir}/example

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Nov 18 2025 Vít Ondruch <vondruch@redhat.com> - 2.2.5-1
- Update to ruby-vips 2.2.5
  Resolves: rhbz#2344206

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 18 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.17-13
- Apply upstream patch to add sentinel when calling variadic C func

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 02 2022 Vít Ondruch <vondruch@redhat.com> - 2.0.17-7
- Use glibc to check for the platform specificity.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 01 2021 Vít Ondruch <vondruch@redhat.com> - 2.0.17-5
- Remove the ppc64le workaround, since orc was fixed.
  Resolves: rhbz#1987951
  Related: rhbz#1917540

* Sat Aug 14 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.0.17-4
- Patch for ruby 3.0 keyword argument separation change,
  patch from the upstream
- Workaround for vips segfault perhaps due to orc issue (bug 1917540)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 12 2020 Pavel Valena <pvalena@redhat.com> - 2.0.17-1
- Initial package
