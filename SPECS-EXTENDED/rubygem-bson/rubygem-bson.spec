Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Generated from bson-1.3.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name bson

Name: rubygem-%{gem_name}
Version: 4.15.0
Release: 1%{?dist}
Summary: Ruby Implementation of the BSON specification
License: ASL 2.0
# Keep the URL, while different URL is used in the upstream gemspec file.
# Because there is a basic explanation about the bson
# that is a beneficial for Fedora user.
URL: https://bsonspec.org
Source0: https://github.com/mongodb/%{gem_name}-ruby/archive/refs/tags/v%{version}.tar.gz#/rubygem-%{gem_name}-%{version}.tar.gz
Requires: rubygem(bigdecimal)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: ruby-devel >= 2.3
BuildRequires: gcc
BuildRequires: rubygem(bigdecimal)
BuildRequires: rubygem(rspec)
# This package contains the binary extension originaly provided by bson_ext
# since F26 timeframe.
Provides: rubygem-bson_ext%{?_isa} = %{version}-%{release}
Provides: rubygem-bson_ext = %{version}-%{release}
Provides: rubygem(bson_ext) = %{version}-%{release}
Obsoletes: rubygem-bson_ext < 4.1.1-1

%description
A fully featured BSON specification implementation in Ruby.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{gem_name}-ruby-%{version}

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/
rm -rf $RPM_BUILD_ROOT%{gem_dir}/extensions/

%check
pushd .%{gem_instdir}
rspec -I$(dirs +1)%{gem_extdir_mri} spec
popd

%files
%dir %{gem_instdir}
%{gem_extdir_mri}
%license %{gem_instdir}/LICENSE
%{gem_instdir}/NOTICE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Mon Nov 28 2022 Muhammad Falak <mwani@microsoft.com> - 4.15.0-1
- Switch to building a tar.gz instead of a gem
- License verified

* Thu Mar 11 2021 Henry Li <lihl@microsoft.com> - 4.7.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove unnecessary files that won'be built

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Vít Ondruch <vondruch@redhat.com> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.7

* Fri Dec 20 2019 Jun Aruga <jaruga@redhat.com> - 4.7.0-1
- Update to bson 4.7.0.

* Tue Nov 19 2019 Jun Aruga <jaruga@redhat.com> - 4.6.0-1
- Update to bson 4.6.0.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 28 2019 Jun Aruga <jaruga@redhat.com> - 4.5.0-1
- Update to bson 4.5.0.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Vít Ondruch <vondruch@redhat.com> - 4.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Mon Jul 23 2018 Jun Aruga <jaruga@redhat.com> - 4.3.0-4
- Fix FTBFS (rhbz#1606164)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Jun Aruga <jaruga@redhat.com> - 4.3.0-1
- Update to bson 4.3.0.
- Remove Obsoletes (rhbz#1537219)

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 4.2.2-3
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Vít Ondruch <vondruch@redhat.com> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.5

* Mon Dec 18 2017 Jun Aruga <jaruga@redhat.com> - 4.2.2-1
- Update to bson 4.2.2.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Vít Ondruch <vondruch@redhat.com> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Wed Jan 04 2017 Vít Ondruch <vondruch@redhat.com> - 4.2.1-1
- Update to bson 4.2.1.

* Thu Dec 15 2016 Vít Ondruch <vondruch@redhat.com> - 4.2.0-2
- Add BigDecimal dependnecy.

* Thu Dec 15 2016 Vít Ondruch <vondruch@redhat.com> - 4.2.0-1
- Update to bson 4.2.0.

* Mon Dec 05 2016 Vít Ondruch <vondruch@redhat.com> - 4.1.1-2
- Fix build on PPC.

* Wed Aug 31 2016 Vít Ondruch <vondruch@redhat.com> - 4.1.1-1
- Update to bson 4.1.1.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 26 2014 Vít Ondruch <vondruch@redhat.com> - 1.10.2-1
- Update to bson 1.10.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 19 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.2-1
- Update to bson 1.9.2.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.4-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 08 2012 Vít Ondruch <vondruch@redhat.com> - 1.6.4-1
- Update to bson 1.6.4.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.4.0-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Vít Ondruch <vondruch@redhat.com> - 1.4.0-1
- Update to bson 1.4.0

* Wed May 25 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.1-1
- Initial package
