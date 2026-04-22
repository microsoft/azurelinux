# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name pdf-reader

Name: rubygem-%{gem_name}
Version: 2.4.2
Release: 11%{?dist}
Summary: A library for accessing the content of PDF files
License: MIT
URL: https://github.com/yob/pdf-reader
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone --no-checkout https://github.com/yob/pdf-reader.git
# cd pdf-reader && git archive -v -o pdf-reader-2.4.2-spec.txz v2.4.2 spec/
Source1: pdf-reader-%{version}-spec.txz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.9.3
BuildRequires: rubygem(Ascii85)
BuildRequires: rubygem(afm)
BuildRequires: rubygem(hashery)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(ruby-rc4)
BuildRequires: rubygem(ttfunk)
BuildArch: noarch

%description
The PDF::Reader library implements a PDF parser conforming as much as possible
to the PDF specification from Adobe.

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

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

chmod a+x %{buildroot}%{gem_instdir}/examples/*.rb

%check
pushd .%{gem_instdir}
ln -s %{_builddir}/spec .

sed -i '/require.*bundler/ s/^/#/' spec/spec_helper.rb
sed -i '/Bundler.setup/ s/^/#/' spec/spec_helper.rb

rspec -r spec_helper spec
popd

%files
%dir %{gem_instdir}
%{_bindir}/pdf_*
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/TODO
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/examples

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Vít Ondruch <vondruch@redhat.com> - 2.4.2-1
- Update to pdf-reader 2.4.2.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 14 13:52:42 CEST 2020 Pavel Valena <pvalena@redhat.com> - 2.4.1-1
- Update to pdf-reader 2.4.1.
  Resolves: rhbz#1742349

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Vít Ondruch <vondruch@redhat.com> - 2.1.0-1
- Update to pdf-reader 2.1.0.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 16 2014 Josef Stribny <jstribny@redhat.com> 1.3.3.-6
- Skip specs that relies on test/unit

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 13 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.3-4
- require (and BR) ttfunk

* Tue Aug 13 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.3-3
- add BR of afm and hashery for tests

* Mon Aug 05 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.3-2
- fix tar file name

* Mon Aug 05 2013 Miroslav Suchý <msuchy@redhat.com> 1.3.3-1
- rebase to 1.3.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Miroslav Suchý <msuchy@redhat.com> - 1.1.1-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 05 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-6
- 850679 - add rubygem(minitest) to BR (msuchy@redhat.com)
- 850679 - include version in file name with spec tests (msuchy@redhat.com)

* Mon Sep 03 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-5
- 850679 - run test suite (msuchy@redhat.com)
- 850679 - flag examples as executables (msuchy@redhat.com)

* Thu Aug 23 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-4
- 850679 - add rubygems to BR (msuchy@redhat.com)
- 850679 - fix BR and do not remove %%{gem_instdir}/bin (msuchy@redhat.com)

* Wed Aug 22 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-3
- add runtime dependencies (msuchy@redhat.com)

* Wed Aug 22 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-2
- new package built with tito

* Tue Aug 21 2012 Miroslav Suchý <msuchy@redhat.com> 1.1.1-1
- new package built with tito

