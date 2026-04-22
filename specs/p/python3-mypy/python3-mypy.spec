# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python3-mypy
Version:        1.18.2
Release: 2%{?dist}
Summary:        A static type checker for Python
%{?python_provide:%python_provide python3-mypy}

# The files under lib-python and lib-typing/3.2 are Python-licensed, but this
# package does not include those files
# mypy/typeshed is ASL 2.0
License:        MIT and Apache-2.0 
URL:            https://github.com/python/mypy
Source0:        https://github.com/python/mypy/archive/v%{version}/mypy-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-typing-extensions
BuildRequires:  (python3-tomli if python3 < 3.11)
BuildRequires:  python3-pathspec
Requires:  python3-typing-extensions

# Remove for f38+
Obsoletes: python-typeshed < 1:0.1-1
Provides: python-typeshed = 1:0.1-0.20191011git2

# Needed to generate the man pages
BuildRequires:  help2man
BuildRequires:  python3dist(mypy-extensions)

BuildArch:      noarch

%description
Mypy is an optional static type checker for Python.  You can add type
hints to your Python programs using the upcoming standard for type
annotations introduced in Python 3.5 beta 1 (PEP 484), and use mypy to
type check them statically. Find bugs in your programs without even
running them!

%prep
%autosetup -n mypy-%{version} -p1
rm -vrf *.egg-info/

%build
%py3_build

%install
%py3_install

# Generate man pages
mkdir -p %{buildroot}%{_mandir}/man1
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    help2man --no-info --version-string 'mypy %{version}-dev' \
        --no-discard-stderr -o %{buildroot}%{_mandir}/man1/mypy.1 \
        %{buildroot}%{_bindir}/mypy

PYTHONPATH=%{buildroot}%{python3_sitelib} \
    help2man --no-info --version-string 'mypy stubgen %{version}-dev' \
        --no-discard-stderr -o %{buildroot}%{_mandir}/man1/stubgen.1 \
        %{buildroot}%{_bindir}/stubgen

%pre
# Remove for f38+
%pretrans -p <lua>
path = "%{python3_sitelib}/mypy/typeshed"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/mypy
%{python3_sitelib}/mypy-*.egg-info
%{python3_sitelib}/mypyc
%{_bindir}/mypy
%{_bindir}/mypyc
%{_bindir}/dmypy
%{_bindir}/stubgen
%{_bindir}/stubtest
%{_mandir}/man1/mypy.1*
%{_mandir}/man1/stubgen.1*

%changelog
* Fri Sep 19 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.18.2-1
- 1.18.2

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.18.1-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Sep 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.18.1-1
- 1.18.1

* Fri Aug 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.17.1-3
- BuildRequire pathspec to fix man pages.

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.17.1-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 31 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.17.1-1
- 1.17.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.17.0-1
- 1.17.0

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.16.0-2
- Rebuilt for Python 3.14

* Thu May 29 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.16.0-1
- 1.16.0

* Wed Feb 05 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.15.0-1
- 1.15.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.14.1-1
- 1.14.1

* Fri Dec 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.14.0-1
- 1.14.0

* Thu Oct 24 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.13.0-1
- 1.13.0

* Mon Oct 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.12.1-1
- 1.12.1

* Tue Oct 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.12.0-1
- 1.12.0

* Mon Aug 26 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.11.2-1
- 1.11.2

* Wed Jul 31 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.11.1-1
- 1.11.1

* Mon Jul 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.11.0-1
- 1.11.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.10.1-1
- 1.10.1

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.10.0-2
- Rebuilt for Python 3.13

* Thu Apr 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.10.0-1
- 1.10.0

* Tue Mar 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.9.0-1
- 1.9.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.8.0-1
- 1.8.0

* Mon Nov 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.7.1-1
- 1.7.1

* Mon Nov 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.7.0-1
- 1.7.0

* Mon Oct 23 2023 Miro Hrončok <mhroncok@redhat.com> - 1.6.1-2
- Drop a redundant BuildRequires python3dist(typed-ast)

* Thu Oct 19 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.6.1-1
- 1.6.1

* Tue Oct 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.6.0-1
- 1.6.0

* Mon Aug 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.5.1-1
- 1.5.1

* Fri Aug 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.5.0-1
- 1.5.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Python Maint <python-maint@redhat.com> - 1.4.1-2
- Rebuilt for Python 3.12

* Tue Jun 27 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.4.1-1
- 1.4.1

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 1.4.0-2
- Rebuilt for Python 3.12

* Wed Jun 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.4.0-1
- 1.4.0

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.3.0-2
- Rebuilt for Python 3.12

* Thu May 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.3.0-1
- 1.3.0

* Thu Apr 06 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.2.0-1
- 1.2.0

* Tue Mar 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.1.1-1
- 1.1.1

* Fri Mar 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.0.1-2
- migrated to SPDX license

* Tue Feb 21 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.0.1-1
- 1.0.1

* Tue Feb 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.0.0-1
- 1.0.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.991-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 20 2023 Miro Hrončok <mhroncok@redhat.com> - 0.991-2
- Conditionalize an unused build dependency on python3-tomli

* Tue Nov 15 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.991-1
- 0.991

* Wed Nov 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.990-1
- 0.990

* Tue Oct 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.982-1
- 0.982

* Tue Sep 27 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.981-1
- 0.981

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.971-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.971-1
- 0.971

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 0.961-2
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.961-1
- 0.961

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.960-2
- Rebuilt for Python 3.11

* Thu May 26 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.960-1
- 0.960

* Mon May 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.950-1
- 0.950

* Tue Apr 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.942-1
- 0.942

* Wed Mar 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.941-1
- 0.941

* Mon Mar 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.940-1
- 0.940

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.931-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.931-1
- 0.931

* Wed Dec 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.930-1
- 0.930

* Wed Dec 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.921-1
- 0.921

* Fri Dec 17 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.920-1
- 0.920

* Wed Sep 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.910-4
- Revert to bundled typeshed per typeshed upstream.

* Wed Aug 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.910-3
- BR python3-toml to fix man pages.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.910-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.910-1
- 0.910

* Fri Jun 11 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.902-1
- 0.902

* Wed Jun 09 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.901-1
- 0.901

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.812-2
- Rebuilt for Python 3.10

* Sat Feb 20 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.812-1
- 0.812

* Wed Feb 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.810-1
- 0.810

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.800-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.800-1
- 0.800

* Sat Oct 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.790-1
- 0.790

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.782-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.782-1
- 0.782

* Fri Jun 19 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.781-1
- 0.781

* Fri Jun 05 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.780-1
- 0.780

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.770-2
- Rebuilt for Python 3.9

* Tue Mar 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.770-1
- 0.770

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.761-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.761-1
- 0.761

* Wed Dec 18 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.760-1
- 0.760

* Mon Dec 02 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.750-1
- 0.750

* Mon Nov 11 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.740-2
- Require/BR python3-typing-extensions

* Thu Oct 17 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.740-1
- 0.740

* Tue Oct 08 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.730-2
- Fix typeshed.

* Thu Sep 26 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.730-1
- 0.730

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.720-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.720-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.720-1
- 0.720

* Mon Jun 24 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.711-1
- 0.711

* Wed Jun 19 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.710-1
- 0.710

* Wed Apr 17 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.701-1
- 0.701

* Wed Apr 03 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.700-1
- Update to 0.700

* Sat Feb 23 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.670-1
- Update to 0.670

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.620-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Matus Honek <mhonek@redhat.com> - 0.620-2
- Add BuildRequire to fix man page generation

* Fri Aug 10 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.620-1
- 0.620

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.600-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.600-2
- Rebuilt for Python 3.7

* Tue May 08 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.600-1
- 0.600

* Tue Mar 27 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.580-1
- 0.580

* Mon Mar 05 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.570-1
- 0.570

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.560-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Gwyn Ciesla <limburgher@gmail.com> - 0.560-2
- python3-psutil requires.

* Mon Dec 18 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.560-1
- 0.560

* Mon Nov 13 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.550-1
- 0.550

* Mon Oct 23 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.540-1
- 0.540

* Fri Oct 20 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.530-1
- 0.530

* Tue Sep 05 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.521-3
- Typeshed patch.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.521-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.521-1
- 0.521

* Tue Jul 11 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.520-1
- 0.520

* Sun Jun 11 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.511-2
- Add python3-typed_ast Requires.

* Fri Jun 09 2017 Gwyn Ciesla <limburgher@gmail.com> - 0.511-1
- New upstream.

* Sat May 13 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.4.6-4
- Add dist tag back to Release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.6-2
- Rebuild for Python 3.6

* Mon Dec 19 2016 CAI Qian <caiqian@redhat.com> - 0.4.6-1
- Update to mypy 0.4.6

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.4.3-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 18 2016 David Shea <dshea@redhat.com> - 0.4.3-1
- Update to mypy 0.4.3

* Mon Jun 13 2016 David Shea <dshea@redhat.com> - 0.4.2-1
- Update to mypy 0.4.2

* Thu May 19 2016 David Shea <dshea@redhat.com> - 0.4.1-2
- Fix build issues

* Tue May 17 2016 David Shea <dshea@redhat.com> - 0.4.1-1
- Update to mypy 0.4.1

* Mon Feb 22 2016 David Shea <dshea@redhat.com> - 0.3.1-1
- Update to the first post-3.5 actual upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2.dev20160128git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 David Shea <dshea@redhat.com> - 0.2.0-1.dev20160128git
- Generalize yield statement function type
- Avoid crash on outrageous non-ASCII characters.
- No longer need to pin flake8 version.
- Find partial types anywhere in the stack. (removes local patch)
- Update license year range to 2016
- If a base class is Any, don't get default constructor signature from object.
- Simplify union types when determining type sameness
- Generator fixup
- Add line number to "__init__ must return None" error
- Fix empty yield error in unannotated functions
- Fix "except (E1, E2):" parsing in PY2.
- Don't crash if no source files were found in a directory or package.
- Fail without traceback when duplicate module name encountered.
- Fix subtype check between generic class and Callable
- Avoid crash on "x in y" where y has a partial type.
- Fix type inference issue with dict(x=[], y=[])
- Fix #1160 (bogus error message)
- Fix function definition within for statement

* Fri Jan 15 2016 David Shea <dshea@redhat.com> - 0.2.0-1.dev20160115git
- Fix the order in which builtins are loaded.
- Fix crash on undefined variable actual_types in check_argument_count (replaces local patch)
- Fixes for Generator support
- Fix crash in check_overlapping_op_methods
- Hopeful fix for #1002 (lxml trouble)
- No longer need to pin flake8 version.
- Find partial types anywhere in the stack. (not yet committed upstream)

* Mon Jan 11 2016 David Shea <dshea@redhat.com> - 0.2.0-1.dev20160111git
- Add support for more kinds of function redefinition
- Allow conditionally assigning None to a module
- Support conditionally defined nested functions
- Tighten argument type for Instance(erased=...) from Any to bool.
- Reformat a few messages so they are easier to find using grep.
- Update README.md to fix installation instructions for Python 3.5

* Thu Jan  7 2016 David Shea <dshea@redhat.com> - 0.2.0-1.dev20160104git.1
- Fix a bug in the discovery of the typeshed files

* Mon Jan  4 2016 David Shea <dshea@redhat.com> - 0.2.0-1.dev20160104git
- Don't check git submodule in subprocesses.
- Improve check for "# type: ignore".
- Add --pdb flag to drop into pdb upon fatal error.
- Don't report internal error when using a name that could not be imported.
- Write type-checking errors to stdout. Make usage() more complete.
- Avoid ever relying on a not-yet-initialized MRO
- When comparing template to actual arg types, stop at shortest.
- Be more clever about finding a Python 2 interpreter
- Basic support for partial 'None' types
- Handle multiple None initializers
- Remove redundant annotations
- Partial type improvements
- Allow assignments to function definitions
- Document --pdb option.
- Look for the keyword type in the right place.

* Mon Dec 21 2015 David Shea <dshea@redhat.com> - 0.2.0-1.dev20151220git
- Fix an internal error when updating a partial type from an outer scope

* Thu Dec 17 2015 David Shea <dshea@redhat.com> - 0.2.0-1.dev20151217git
- Initial package
