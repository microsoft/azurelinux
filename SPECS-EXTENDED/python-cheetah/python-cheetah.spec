Name:           python-cheetah
Version:        3.2.6.post1
Release:        12%{?dist}
Summary:        Template engine and code generator

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://cheetahtemplate.org/
Source:         https://github.com/CheetahTemplate3/cheetah3/archive/%{version}/Cheetah3-%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Instead of playing Whac-A-Mole and adding more and more basepythons,
# e.g. in https://github.com/CheetahTemplate3/cheetah3/commit/6be6bc10a4,
# we let tox do the right thing by not setting any:
Patch:          tox-no-basepython.patch
Patch1:         cheetah3-3.2.6.post1-protect-cgi.patch
Patch2:         cheetah3-3.2.6.post1-loadTestsFromModule.patch
Patch3:         cheetah3-3.2.6.post1-typeerror.patch
Patch4:         cheetah3-3.2.6.post1-framelocalsproxy.patch
Patch5:         cheetah3-3.2.6.post1-parse_qs.patch

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

# for tests
%if 0%{?with_check}
BuildRequires:  python3-tox
BuildRequires:  python3-pluggy
BuildRequires:  python3-py
BuildRequires:  python3-filelock
BuildRequires:  python3-toml
BuildRequires:  python3-six
BuildRequires:  python3-tox-current-env
%endif

%global _description %{expand:
Cheetah3 is a free and open source template engine and code generation tool.
It can be used standalone or combined with other tools and frameworks.  Web
development is its principle use, but Cheetah is very flexible and is also
being used to generate C++ game code, Java, SQL, form emails and even Python
code.}

%description %{_description}

%package -n python3-cheetah
Summary:        %{summary}

%description -n python3-cheetah %{_description}

%prep
%autosetup -p1 -n cheetah3-%{version}

# remove upper bound on markdown test dependency
sed -e 's|, < 3.2||' -i tox.ini

# remove unnecessary shebang lines to silence rpmlint
find Cheetah -type f -name '*.py' -print0 | xargs -0 sed -i -e '1 {/^#!/d}'

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files Cheetah

%check
# changing this in %%prep would cause an rpmlint error (rpm-buildroot-usage),
# so do it here instead
sed -e 's|{envsitepackagesdir}|%{buildroot}%{python3_sitearch}|' -i tox.ini
%tox

%files -n python3-cheetah -f %{pyproject_files}
%doc ANNOUNCE.rst README.rst TODO BUGS
%{_bindir}/cheetah*

%changelog
* Thu Feb 13 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 3.2.6.post1-12
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified
- Added additional dependencies for successful build and test

* Wed Oct 30 2024 Mike Bonnet <mikeb@redhat.com> - 3.2.6.post1-11
- Backport fix from upstream to support Python 3.13+ (protect import of cgi module)
- Backport fix for running tests under Python 3.13+ (use unittest.defaultTestLoader.loadTestsFromModule)
- Backport fix that silences a TypeError
- Backport fix for a mapping test
- Backport fix to remove use of dropped cgi module

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.6.post1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.2.6.post1-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.6.post1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.6.post1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.6.post1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.2.6.post1-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.6.post1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.6.post1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.2.6.post1-2
- Rebuilt for Python 3.11

* Thu Apr 07 2022 Carl George <carl@george.computer> - 3.2.6.post1-1
- Update to 3.2.6.post1
- Convert to pyproject macros

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.2.4-7
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.2.4-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Patrik Novotný <panovotn@redhat.com> - 3.2.4-2
- Remove python2 package

* Mon Nov 18 2019 Patrik Novotný <panovotn@redhat.com> - 3.2.4-1
- Rebase to upstream release 3.2.4

* Tue Sep 17 2019 Nicolas Chauvet <kwizart@gmail.com> - 3.2.3-2
- Keep python2 despite python2-markdown is missing

* Tue Sep 17 2019 Nicolas Chauvet <kwizart@gmail.com> - 3.2.3-1
- Update to 3.2.3
- Don't own python_sitearch - rhbz#1672098

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 mskalick@redhat.com - 3.1.0-5
- Remove python2 tests - was calling python3 subprocesses internally

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-4
- Rebuilt for Python 3.7

* Tue Jun 12 2018 Lumír Balhar <lbalhar@redhat.com> - 3.1.0-3
- Fixed python2 conditions
- Removed usage of %%{py3dir}

* Wed Mar 28 2018 Marek Skalický <mskalick@redhat.com> - 3.1.0-2
- Use python3 shebang in binary files

* Tue Mar 20 2018 Marek Skalický <mskalick@redhat.com> - 3.1.0-1
- Rebase to latest upstream release

* Tue Feb 27 2018 Marek Skalický <mskalick@redhat.com> - 3.0.0-20
- Add missing BuildRequires: gcc/gcc-c++

* Thu Feb 22 2018 Marek Skalický <mskalick@redhat.com> - 3.0.0-19
- Add Cheetah egg-info for backward compatibility

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.4-17
- Python 2 binary package renamed to python2-cheetah
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-13
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 2.4.4-9
- fix license handling

* Mon Jul 21 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 2.4.4-8
- Since we're leaving out the dep on markdown in the rpm requirements we need
  to leave it out of egginfo as well otherwise pkg_resources using code breaks

* Thu Jun 19 2014 Matthew Miller <mattdm@fedoraproject.org> - 2.4.4-7
- remove python-markdown and python-pygments hard dependencies

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.4-1
- update to the 2.4.4 release

* Mon Oct 18 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.3-1
- update to the 2.4.3 release

* Mon Oct 18 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.2.1-3
- Fix compatibility with Python 2.7

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 24 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.2.1-1
- update to the 2.4.2.1 release

* Thu Jan 14 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.1-3
- remove unnecessary shebang lines to silence rpmlint

* Fri Jan  8 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.1-2
- fix Source url

* Mon Jan  4 2010 Mike Bonnet <mikeb@redhat.com> - 2.4.1-1
- update to the 2.4.1 release

* Tue Oct 20 2009 Mike Bonnet <mikeb@redhat.com> - 2.2.2-2
- backport significant improvements to utf-8/unicode handling from upstream

* Mon Sep 14 2009 Mike Bonnet <mikeb@redhat.com> - 2.2.2-1
- update to the 2.2.2 release
- add dependency on python-markdown for consistency with the egg-info

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun  5 2009 Mike Bonnet <mikeb@redhat.com> - 2.2.1-1
- update to the 2.2.1 release

* Mon May 18 2009 Mike Bonnet <mikeb@redhat.com> - 2.2.0-1
- update to the 2.2.0 release
- remove unneeded importHook() patch, it has been included upstream

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1-4
- Fix cheetah enough that it will pass its unittests on python-2.6.  This has
  actually been broken since py-2.5 and this fix is only a workaround.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.1-3
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.1-2
- Autorebuild for GCC 4.3

* Tue Dec  4 2007 Mike Bonnet <mikeb@redhat.com> - 2.0.1-1
- update to the 2.0.1 release

* Mon Oct 15 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-1
- update to the 2.0 release

* Tue Aug 21 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-0.7.rc8
- rebuild for F8

* Thu May  3 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-0.6.rc8
- bump release for rebuild

* Mon Apr 23 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-0.5.rc8
- update to 2.0rc8

* Mon Jan  8 2007 Mike Bonnet <mikeb@redhat.com> - 2.0-0.4.rc7
- use setuptools and install setuptools metadata

* Sun Dec 10 2006 Mike Bonnet <mikeb@redhat.com> - 2.0-0.3.rc7
- rebuild against python 2.5
- remove obsolete python-abi Requires:

* Mon Sep 11 2006 Mike Bonnet <mikeb@redhat.com> - 2.0-0.2.rc7
- un-%%ghost .pyo files

* Thu Jul 13 2006 Mike Bonnet <mikeb@redhat.com> - 2.0-0.1.rc7
- update to 2.0rc7
- change %%release format to conform to Extras packaging guidelines

* Sun May 21 2006 Mike Bonnet <mikeb@redhat.com> - 2.0-0.rc6.0
- update to 2.0rc6
- run the included test suite after install

* Thu Feb 16 2006 Mike Bonnet <mikeb@redhat.com> - 1.0-2
- Rebuild for Fedora Extras 5

* Wed Dec  7 2005 Mike Bonnet <mikeb@redhat.com> - 1.0-1
- Initial version
