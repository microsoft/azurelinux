%global srcname breathe
%global _description \
Breathe is an extension to reStructuredText and Sphinx to be able to read and \
render the Doxygen xml output.
Summary:        Adds support for Doxygen xml output to reStructuredText and Sphinx
Name:           python-%{srcname}
Version:        4.35.0
Release:        13%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/michaeljones/breathe
Source0:        %{URL}/archive/v%{version}.tar.gz#/breathe-%{version}.tar.gz
Source1:        %{URL}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz.sig
Source2:        https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x8aed58021feacdd5f27ba0e6a72f627716ea9d96#./vermware.key
# Patch1 first hunk was truncated
Patch1:         https://github.com/breathe-doc/breathe/pull/956.patch
# Patch2 is a better fix of first hunk of Path1
Patch2:         https://github.com/breathe-doc/breathe/pull/964.patch
BuildRequires:  %{py3_dist Jinja2} >= 2.7.3
BuildRequires:  %{py3_dist MarkupSafe} >= 0.23
BuildRequires:  %{py3_dist Pygments} >= 1.6
BuildRequires:  %{py3_dist docutils} >= 0.12
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist six} >= 1.9
BuildRequires:  doxygen
# NOTE: git is only needed because part of the build process checks if it's in
# a git repo
BuildRequires:  git
BuildRequires:  gnupg2
BuildRequires:  make
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildArch:      noarch

# Set the name of the documentation directory
%global _docdir_fmt %{name}

# This is buildroot only in RHEL, and building the docs pulls in unwanted dependencies
#%bcond doc %{undefined rhel}

BuildRequires:  %{py3_dist Sphinx} > 5.0.0
#%if %{with doc}
#BuildRequires:  %{py3_dist furo}
#BuildRequires:  %{py3_dist sphinx-copybutton}
#%endif

%description %{_description}

%package -n     python%{python3_pkgversion}-%{srcname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Summary:        %{summary}
License:        BSD-3-Clause
Requires:       doxygen >= 1.8.4
Requires:       python%{python3_pkgversion}-six

%description -n python%{python3_pkgversion}-%{srcname} %{_description}

%package        doc
Summary:        Documentation files for %{srcname}
# tinyxml uses zlib license
License:        BSD-3-Clause AND Zlib

%description    doc
This package contains documentation for developer documentation for %{srcname}.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{srcname}-%{version} -p1

%build
%py3_build
# %if %{with doc}
# Build the documentation
# Remove -W (turn warnings into errors) from SPHINXOPTS to fix the build for f39
# %make_build SPHINXOPTS="-v -E" DOXYGEN=$(which doxygen) PYTHONPATH=$(pwd) html
# Remove temporary build files
# rm documentation/build/html/.buildinfo
# %endif

%install
%py3_install

%check
%make_build dev-test

%files -n python%{python3_pkgversion}-%{srcname}
%doc README.rst
%{_bindir}/breathe-apidoc
%{python3_sitelib}/*
%license LICENSE

# %if %{with doc}
# %files doc
# %doc documentation/build/html
# %license LICENSE
# %endif

%changelog
* Fri Oct 18 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 4.35.0-13
- Integrating the spec into Azure Linux
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.35.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 4.35.0-11
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.35.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.35.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Sérgio M. Basto <sergio@serjux.com> - 4.35.0-8
- Fix for Sphinx 7.2 compatlble with older Sphinx

* Thu Jan 11 2024 Sérgio M. Basto <sergio@serjux.com> - 4.35.0-7
- Fix the build for f39 and rawhide

* Fri Aug 04 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 4.35.0-6
- migrated to SPDX license

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.35.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 4.35.0-4
- Rebuilt for Python 3.12

* Thu Apr 20 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 4.35.0-3
- Do not build docs in RHEL builds

* Fri Apr 07 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.35.0-2
- Add gpg source verification back

* Thu Mar 30 2023 Karolina Surma <ksurma@redhat.com> - 4.35.0-1
- Update to 4.35.0 (resolves rhbz#2179094)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.34.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 09 2022 Karolina Surma <ksurma@redhat.com> - 4.34.0-5
- Backport upstream patch to enable successful build with Sphinx 5.3+

* Mon Sep 19 2022 Tom Rix <trix@redhat.com> - 4.34.0-4
- Use any version of sphinx on RHEL

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 12 2021 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.30.0-1
- New upstream release 4.30.0
- Fixes rhbz#1955833

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.29.1-2
- Rebuilt for Python 3.10

* Sat Apr 24 2021 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.29.1-1
- New upstream release 4.29.1
- Fixes rhbz#1953104

* Thu Apr 15 2021 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.29.0-1
- New upstream release 4.29.0
- Fixes rhbz#1944821

* Wed Mar 10 2021 Charalampos Stratakis <cstratak@redhat.com> - 4.27.0-2
- Fix an IndexError when generating toctree (rhbz#1930910)

* Tue Feb 16 2021 Charalampos Stratakis <cstratak@redhat.com> - 4.27.0-1
- New upstream release 4.27.0 (rhbz#1918566, rhbz#1929448)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Charalampos Stratakis <cstratak@redhat.com> - 4.26.0-1
- New upstream release 4.26.0 (rhbz#1914147)

* Sun Dec 20 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.25.1-1
- New upstream release 4.25.1 (rhbz#1908213)

* Mon Dec  7 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.24.1-1
- New upstream release 4.24.1 (rhbz#1903366)

* Mon Nov 16 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.24.0-1
- New upstream release 4.24.0 (rhbz#1897984)

* Tue Nov  3 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.23.0-1
- New upstream release 4.23.0 (rhbz#1889874)

* Thu Oct  1 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.22.1-1
- New upstream release 4.22.1 (rhbz#1880753)

* Thu Oct  1 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.22.0-1
- New upstream release 4.22.0 (rhbz#1880753)

* Sun Sep 13 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.21.0-1
- New upstream release 4.21.0 (rhbz#1878050)

* Thu Aug 20 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.20.0-1
- New upstream release 4.20.0 (rhbz#1870404)

* Thu Aug 20 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.19.2-3
- Add patch to add support for sphinx 3.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  9 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.19.2-1
- New upstream release 4.19.2 (rhbz#1821614, rhbz#1823718)

* Mon Jun  8 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.19.1-1
- New upstream release 4.19.1 (rhbz#1821614, rhbz#1823718)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.14.2-2
- Rebuilt for Python 3.9

* Tue May  5 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.18.0-1
- New upstream release 4.18.0 (rhbz#1821614, rhbz#1823718)

* Thu Apr 23 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.16.0-1
- New upstream release 4.16.0 (rhbz#1821614, rhbz#1823718)

* Wed Apr 15 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.15.0-1
- New upstream release 4.15.0

* Wed Apr  8 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.14.2-1
- New upstream release 4.14.2

* Sun Feb  2 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.14.1-1
- New upstream release 4.14.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.14.0-1
- New upstream release 4.14.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.13.1-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 28 2019 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.13.1-1
- New upstream release 4.13.1
- Enable test run in %%check

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.13.0.post0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.0.post0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Dan Čermák <dan.cermak@cgc-instruments.com> - 4.13.0.post0-1
- New upstream release 4.13.0.post0

* Mon Mar 18 2019 Miro Hrončok <mhroncok@redhat.com> - 4.7.3-7
- Subpackage python2-breathe has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.7.3-4
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.7.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 24 2017 Dave Johansen <davejohansen@gmail.com> - 4.7.3-1
- Upstream update

* Tue Aug 22 2017 Dave Johansen <davejohansen@gmail.com> - 4.7.2-1
- Upstream update

* Wed Aug 16 2017 Dave Johansen <davejohansen@gmail.com> - 4.7.1-1
- Upstream update

* Wed Aug 09 2017 Dave Johansen <davejohansen@gmail.com> - 4.7.0-1
- Upstream update

* Sat Aug 05 2017 Dave Johansen <davejohansen@gmail.com> - 4.6.0-3
- Fix for node without parent

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Miro Hrončok <mhroncok@redhat.com> - 4.6.0-1
- Upstream update

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Miro Hrončok <mhroncok@redhat.com> - 4.4.0-2
- Rebuild for Python 3.6

* Mon Dec 19 2016 Dave Johansen <davejohansen@gmail.com> - 4.4.0-1
- Upstream release

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri May 13 2016 Dave Johansen <davejohansen@gmail.com> - 4.2.0-3
- Fix for Python 3

* Sun Apr 10 2016 Orion Poplawski <orion@cora.nwra.com> - 4.2.0-2
- Fix BR/Rs

* Wed Apr 06 2016 Dave Johansen <davejohansen@gmail.com> - 4.2.0-1
- Initial RPM release
## END: Generated by rpmautospec
