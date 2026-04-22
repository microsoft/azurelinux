# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Allow building with multiple Python versions in EPEL
%{?el7:%bcond_without python3_other}

# Metadata for Python-related macros (i.e. %%pypi_source)
## Upstream package/project name
%global srcname bsddb3

## Description common to all version-specific subpackages
%global common_description %{expand:
This package contains Python wrappers for Berkeley DB, the Open Source embedded
database system. The Python wrappers allow you to store Python string objects of
any length.}

Name:           python-%{srcname}
Version:        6.2.9
Release: 24%{?dist}
Summary:        Python 3 bindings for Berkeley DB

License:        BSD-3-Clause
URL:            https://pypi.org/project/bsddb3
Source0:        %{pypi_source}

# This change satisfies the rpath check during the build
# Currently, both Python's and setuptools' bundled distutils are patched to work
# around this issue, so the package doesn't fail even without this patch.
# As both patches may be removed in the future and it's possible to fix the
# package directly, it's better to do it here.
Patch0:          dont-include-standard-paths-in-runtime-libdir.patch
Patch1:          TextTestResult.patch
Patch2:          threads.patch
BuildRequires:  gcc libdb-devel

%description    %{common_description}


# Mainline Python 3 subpackage
%global python3_name        %{expand:python%{python3_pkgversion}-%{srcname}}
%package -n     %{python3_name}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pip

%description -n %{python3_name} %{common_description}


# Alternative Python 3 subpackage
%if %{with python3_other}
%global python3_other_name  %{expand:python%{python3_other_pkgversion}-%{srcname}}
%package -n     %{python3_other_name}
Summary:        %{summary}
BuildRequires:  python%{python3_other_pkgversion}-devel
BuildRequires:  python%{python3_other_pkgversion}-setuptools

%description -n %{python3_other_name} %{common_description}
%endif


%prep
%autosetup -p1 -n %{srcname}-%{version}

#%%generate_buildrequires
#%%pyproject_buildrequires

%build
%pyproject_wheel
%{?with_python3_other:%py3_other_build}

%install
# Helper installation functions
fix_scripts_shebangs_and_permissions() {
    local -r py_binary="$1"
    local -r py_install_dir="$2"

    local -r WRONG_SHEBANG='#!/usr/bin/python|#!/usr/bin/env python[[:digit:]]*'
    local -r CORRECT_SHEBANG="#!${py_binary}"

    # Fix shebangs
    grep --recursive --files-with-matches --null --extended-regexp \
        --regexp="${WRONG_SHEBANG}" "${py_install_dir}" \
    | xargs --null -- sed --regexp-extended --in-place \
        --expression="s@${WRONG_SHEBANG}@${CORRECT_SHEBANG}@"

    # Set correct permissions on scripts
    grep --recursive --files-with-matches --null --extended-regexp \
        --regexp="${CORRECT_SHEBANG}" "${py_install_dir}" \
    | xargs --null -- chmod 0755

    # Recompile bytecode for changed files
    %{py_byte_compile "${py_binary}" "${py_install_dir}"}
}

# Latter builds override former ones
%if %{with python3_other}
%py3_other_install
fix_scripts_shebangs_and_permissions %{__python3_other} \
    %{buildroot}%{python3_other_sitearch}/%{srcname}
%endif

%pyproject_install 
fix_scripts_shebangs_and_permissions %{__python3} \
    %{buildroot}%{python3_sitearch}/%{srcname}

# Get rid of unneeded header
rm -f %{buildroot}%{_includedir}/python3.*/%{srcname}/bsddb.h


%check
%{__python3} test.py
%{?with_python3_other:%{__python3_other} test.py}

%files -n %{python3_name}
%doc ChangeLog PKG-INFO README.txt
%license LICENSE.txt
%{python3_sitearch}/bsddb3/
%{python3_sitearch}/bsddb3-%{version}.dist-info

%if %{with python3_other}
%files -n %{python3_other_name}
%doc ChangeLog PKG-INFO README.txt
%license LICENSE.txt
%{python3_other_sitearch}/bsddb3/
%{python3_other_sitearch}/bsddb3-%{version}-py%{python3_other_version}.egg-info
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 6.2.9-23
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 6.2.9-22
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 6.2.9-20
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 6.2.9-17
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 6.2.9-14
= Patch for Python 3.13

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 6.2.9-12
- Rebuilt for Python 3.12

* Thu Mar 02 2023 Gwyn Ciesla <gwync@protonmail.com> - 6.2.9-11
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 6.2.9-9
- BR setuptools.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 6.2.9-7
- Rebuilt for Python 3.11

* Fri Mar 04 2022 Karolina Surma <ksurma@redhat.com> - 6.2.9-6
- Satisfy the rpath check when using setuptools' bundled distutils

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 6.2.9-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 27 2020 Jan Staněk <jstanek@redhat.com> - 6.2.9-1
- Upgrade to version 6.2.9

* Fri Nov 20 2020 Jan Staněk <jstanek@redhat.com> - 6.2.8-1
- Upgrade to version 6.2.8

* Tue Oct 20 2020 Jan Staněk <jstanek@redhat.com> - 6.2.7-1
- Upgrade to version 6.2.7

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 6.2.6-10
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jan Staněk <jstanek@redhat.com> - 6.2.6-8
- Add patch for import compatibility with Python 3.9

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 6.2.6-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 6.2.6-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 03 2019 Jan Staněk <jstanek@redhat.com> - 6.2.6-3
- Restructure and rename package in order to enable EPEL builds

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Jan Staněk <jstanek@redhat.com> - 6.2.6-1
- Update to 6.2.6 (https://www.jcea.es/programacion/pybsddb.htm#bsddb3-6.2.6)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 6.2.5-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 11 2017 Jan Staněk <jstanek@redhat.com> - 6.2.5-3
- Apply the shebang fix to the right files.

* Tue Oct 10 2017 Jan Staněk <jstanek@redhat.com> - 6.2.5-2
- Fix generic python shebangs (https://pagure.io/packaging-committee/issue/698)

* Wed Oct 04 2017 Jan Stanek <jstanek@redhat.com> - 6.2.5-1
- Update to 6.2.5 (https://www.jcea.es/programacion/pybsddb.htm#bsddb3-6.2.5)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Jan Stanek <jstanek@redhat.com> - 6.2.4-1
- Update to version 6.2.4 (https://www.jcea.es/programacion/pybsddb.htm#bsddb3-6.2.4)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 6.2.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu May 05 2016 Jan Stanek <jstanek@redhat.com> - 6.2.0-1
- Update to version 6.2.0 (https://www.jcea.es/programacion/pybsddb.htm#bsddb3-6.2.0)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Jan Stanek <jstanek@redhat.com> - 6.1.1-1
- Update to version 6.1.1 (https://www.jcea.es/programacion/pybsddb.htm#bsddb3-6.1.1)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Dec 06 2013 Jan Stanek <jstanek@redhat.com> - 6.0.1-1
- Update to 6.0.1

* Mon Sep 23 2013 Jan Stanek <jstanek@redhat.com> - 6.0.0-1
- Initial package
