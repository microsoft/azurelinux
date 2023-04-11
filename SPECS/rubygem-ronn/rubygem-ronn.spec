%global debug_package %{nil}
%global gem_name ronn
# Missing BR rubygem(contest), necessary for running the test suite in %%check.
Summary:        Manual authoring tool
Name:           rubygem-%{gem_name}
Version:        0.7.3
Release:        18%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rtomayko/ronn
Source0:        https://github.com/rtomayko/ronn/archive/refs/tags/%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  rubygems-devel
Requires:       rubygem(hpricot)
Requires:       rubygem(rdiscount)
Requires:       rubygem(mustache)
Requires:       rubygems
Requires:       groff-base
Requires:       ruby(release)

%description
Ronn builds manuals. It converts simple, human readable text files to
roff for terminal display, and also to HTML for the web.

The source format includes all of Markdown but has a more rigid structure and
syntax extensions for features commonly found in man pages (definition lists,
link notation, etc.). The ronn-format(7) manual page defines the format in
detail.

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
Documentation for %{name}

%prep
%setup -q -n  %{gem_name}-%{version}

%build
gem build %{gem_name}
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
chmod -x %{buildroot}%{gem_instdir}/lib/%{gem_name}.rb

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

# Man pages.
install -D -m 0644 %{buildroot}%{gem_instdir}/man/%{gem_name}.1 %{buildroot}/%{_mandir}/man1/%{gem_name}.1
install -D -m 0644 %{buildroot}%{gem_instdir}/man/%{gem_name}-format.7 %{buildroot}/%{_mandir}/man7/%{gem_name}-format.7

rm -rf %{buildroot}%{gem_instdir}/{INSTALLING,Rakefile,test,man,ronn.gemspec,config.ru}

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/[A-Z]*
%{gem_instdir}/bin
%{gem_libdir}
%{gem_cache}
%{gem_spec}
%{_bindir}/%{gem_name}
%{_mandir}/man1/%{gem_name}.1*
%{_mandir}/man7/%{gem_name}-format.7*

%files doc
%{gem_docdir}

%changelog
* Wed Sep 28 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.7.3-18
- Cleanup SPEC file and move to SPECS directory from Extended.

* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.7.3-17
- License verified
- Build from .tar.gz source.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.3-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 4 2013 Ricky Elrod <codeblock@fedoraproject.org> 0.7.3-4
- Add groff-base Requires.
- Nuke a Requires of the base package from the -doc subpackage.
- Fix Requires for F18-, make it be >= 1.9.1.

* Fri Apr 5 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.3-3
- Fix Requires so the package works on F18- and F19+.
- Fix what is marked as doc.
- Remove some extra files from the gem_instdir which are only needed for building.

* Wed Apr 3 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.3-2
- Move things into a doc subpackage.
- Fix BuildRequires.
- Document why the test suite isn't running.
- Make some things that don't need to be installed, not install.
- Mark some files as doc files.

* Wed Apr 3 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.3-1
- Initial build.
