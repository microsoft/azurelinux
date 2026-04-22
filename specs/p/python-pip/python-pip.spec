## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 19;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The original RHEL N+1 content set is defined by (build)dependencies
# of the packages in Fedora ELN. Hence we disable tests here
# to prevent pulling many unwanted packages in.
%bcond tests %{defined fedora}
# Whether to build the manual pages (useful for bootstrapping Sphinx)
%bcond man 1

%global srcname pip
%global base_version 25.1.1
%global upstream_version %{base_version}%{?prerel}
%global python_wheel_name %{srcname}-%{upstream_version}-py3-none-any.whl

Name:           python-%{srcname}
Version:        %{base_version}%{?prerel:~%{prerel}}
Release:        %autorelease
Summary:        A tool for installing and managing Python packages

# We bundle a lot of libraries with pip, which itself is under MIT license.
# Here is the list of the libraries with corresponding licenses:

# certifi: MPL-2.0
# CacheControl: Apache-2.0
# dependency-groups: MIT
# distlib: Python-2.0.1
# distro: Apache-2.0
# idna: BSD-3-Clause
# msgpack: Apache-2.0
# packaging: Apache-2.0 OR BSD-2-Clause
# platformdirs: MIT
# pygments: BSD-2-Clause
# pyproject-hooks: MIT
# requests: Apache-2.0
# resolvelib: ISC
# rich: MIT
# setuptools: MIT
# truststore: MIT
# tomli: MIT
# tomli-w: MIT
# typing-extensions: Python-2.0.1
# urllib3: MIT

License:        MIT AND Python-2.0.1 AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MPL-2.0 AND (Apache-2.0 OR BSD-2-Clause)
URL:            https://pip.pypa.io/
Source0:        https://github.com/pypa/pip/archive/%{upstream_version}/%{srcname}-%{upstream_version}.tar.gz

# The following sources are wheels used only for tests.
# They are not bundled in the built package and do not contribute to the overall license.
# They are pre-built but only contain text files, rebuilding them in %%build has very little benefit.

# setuptools.whl
# We cannot use RPM-packaged python-setuptools-wheel because upstream pins to <80.
# See https://github.com/pypa/pip/pull/13357 for rationale.
Source1:        https://files.pythonhosted.org/packages/0d/6d/b4752b044bf94cb802d88a888dc7d288baaf77d7910b7dedda74b5ceea0c/setuptools-79.0.1-py3-none-any.whl

# wheel.whl
# We cannot use RPM-packaged python-wheel-wheel because we intent to drop that package in wheel 0.46+.
# That version of wheel has runtime dependencies and is generally useless as a standalone wheel.
# See https://github.com/pypa/pip/pull/13382 as an attempt to drop the requirement from pip tests.
Source2:        https://files.pythonhosted.org/packages/0b/2c/87f3254fd8ffd29e4c02732eee68a83a1d3c346ae39bc6822dcbcb697f2b/wheel-0.45.1-py3-none-any.whl

# coverage.whl
# There is no RPM-packaged python-coverage-wheel, the package is archful.
# Upstream uses this to measure coverage, which we don't.
# This is a dummy placeholder package that only contains empty coverage.process_startup().
# That way, we don't need to patch the usage out of conftest.py.
Source3:        coverage-0-py3-none-any.whl

BuildArch:      noarch

%if %{with tests}
BuildRequires:  /usr/bin/git
BuildRequires:  /usr/bin/hg
BuildRequires:  /usr/bin/bzr
BuildRequires:  /usr/bin/svn
BuildRequires:  python%{python3_pkgversion}-pytest-xdist
%endif

%if %{with man}
# docs/requirements.txt contains many sphinx extensions
# however, we only build the manual pages thanks to
# https://github.com/pypa/pip/pull/13168
# We also always use the "main" Sphinx, not python%%{python3_pkgversion}-sphinx
BuildRequires:  python3-sphinx
%endif

# Prevent removing of the system packages installed under /usr/lib
# when pip install -U is executed.
# https://bugzilla.redhat.com/show_bug.cgi?id=1550368#c24
# Could be replaced with https://www.python.org/dev/peps/pep-0668/
Patch:          remove-existing-dist-only-if-path-conflicts.patch

# Use the system level root certificate instead of the one bundled in certifi
# https://bugzilla.redhat.com/show_bug.cgi?id=1655253
# The same patch is a part of the RPM-packaged python-certifi
Patch:          dummy-certifi.patch

# Don't warn the user about pip._internal.main() entrypoint
# In Fedora, we use that in ensurepip and users cannot do anything about it,
# this warning is juts moot. Also, the warning breaks CPython test suite.
Patch:          nowarn-pip._internal.main.patch

# Adjust path_to_url et al. to produce the same results on Python 3.14+
# https://github.com/pypa/pip/pull/13423
Patch:          python3.14-file-urls.patch

# https://fedoraproject.org/wiki/Changes/dropingOfCertPemFile
# https://github.com/sethmlarson/truststore/pull/183
Patch:          truststore-pem-path.patch

# Patch for the bundled urllib3 for CVE-2025-50181
# Redirects are not disabled when retries are disabled on PoolManager instantiation
# Upstream fix: https://github.com/urllib3/urllib3/commit/f05b1329126d5be6de501f9d1e3e36738bc08857
Patch:          urllib3-CVE-2025-50181.patch

# Remove -s from Python shebang - ensure that packages installed with pip
# to user locations are seen by pip itself
%undefine _py3_shebang_s

%description
pip is a package management system used to install and manage software packages
written in Python. Many packages can be found in the Python Package Index
(PyPI). pip is a recursive acronym that can stand for either "Pip Installs
Packages" or "Pip Installs Python".



# Virtual provides for the packages bundled by pip.
# You can generate it with:
# %%{_rpmconfigdir}/pythonbundles.py --namespace 'python%%{1}dist' src/pip/_vendor/vendor.txt
%global bundled() %{expand:
Provides: bundled(python%{1}dist(cachecontrol)) = 0.14.2
Provides: bundled(python%{1}dist(certifi)) = 2025.1.31
Provides: bundled(python%{1}dist(dependency-groups)) = 1.3.1
Provides: bundled(python%{1}dist(distlib)) = 0.3.9
Provides: bundled(python%{1}dist(distro)) = 1.9
Provides: bundled(python%{1}dist(idna)) = 3.10
Provides: bundled(python%{1}dist(msgpack)) = 1.1
Provides: bundled(python%{1}dist(packaging)) = 25
Provides: bundled(python%{1}dist(platformdirs)) = 4.3.7
Provides: bundled(python%{1}dist(pygments)) = 2.19.1
Provides: bundled(python%{1}dist(pyproject-hooks)) = 1.2
Provides: bundled(python%{1}dist(requests)) = 2.32.3
Provides: bundled(python%{1}dist(resolvelib)) = 1.1
Provides: bundled(python%{1}dist(rich)) = 14
Provides: bundled(python%{1}dist(setuptools)) = 70.3
Provides: bundled(python%{1}dist(tomli)) = 2.2.1
Provides: bundled(python%{1}dist(tomli-w)) = 1.2
Provides: bundled(python%{1}dist(truststore)) = 0.10.1
Provides: bundled(python%{1}dist(typing-extensions)) = 4.13.2
Provides: bundled(python%{1}dist(urllib3)) = 1.26.20
}

# Some manylinux1 wheels need libcrypt.so.1.
# Manylinux1, a common (as of 2019) platform tag for binary wheels, relies
# on a glibc version that included ancient crypto functions, which were
# moved to libxcrypt and then removed in:
#  https://fedoraproject.org/wiki/Changes/FullyRemoveDeprecatedAndUnsafeFunctionsFromLibcrypt
# The manylinux1 standard assumed glibc would keep ABI compatibility,
# but that's only the case if libcrypt.so.1 (libxcrypt-compat) is around.
# This should be solved in the next manylinux standard (but it may be
# a long time until manylinux1 is phased out).
# See: https://github.com/pypa/manylinux/issues/305
# Note that manylinux is only applicable to x86 (both 32 and 64 bits)
# As of Python 3.12, we no longer use this,
# see https://discuss.python.org/t/29455/
# However, we keep it around for previous Python versions that use the wheel package.
%global crypt_compat_recommends() %{expand:
Recommends: (libcrypt.so.1()(64bit) if python%{1}(x86-64))
Recommends: (libcrypt.so.1 if python%{1}(x86-32))
}



%package -n python%{python3_pkgversion}-%{srcname}
Summary:        A tool for installing and managing Python3 packages

BuildRequires:  python%{python3_pkgversion}-devel
# python3 bootstrap: this is rebuilt before the final build of python3, which
# adds the dependency on python3-rpm-generators, so we require it manually
# Note that the package prefix is always python3-, even if we build for 3.X
# The minimal version is for bundled provides verification script
BuildRequires:  python3-rpm-generators >= 11-8
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  bash-completion
BuildRequires:  ca-certificates
Requires:       ca-certificates

# Virtual provides for the packages bundled by pip:
%{bundled %{python3_pkgversion}}

Provides:       pip = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{srcname}
pip is a package management system used to install and manage software packages
written in Python. Many packages can be found in the Python Package Index
(PyPI). pip is a recursive acronym that can stand for either "Pip Installs
Packages" or "Pip Installs Python".


%package -n     %{python_wheel_pkg_prefix}-%{srcname}-wheel
Summary:        The pip wheel
Requires:       ca-certificates

# Virtual provides for the packages bundled by pip:
%{bundled %{python3_pkgversion}}

# This is only relevant for Pythons that are older than 3.12 and don't use their own bundled wheels
# It is also only relevant when this wheel is shared across multiple Pythons
%if "%{python_wheel_pkg_prefix}" == "python"
%{crypt_compat_recommends 3.11}
%{crypt_compat_recommends 3.10}
%{crypt_compat_recommends 3.9}
%endif

%description -n %{python_wheel_pkg_prefix}-%{srcname}-wheel
A Python wheel of pip to use with venv.

%prep
%autosetup -p1 -n %{srcname}-%{upstream_version}

# this goes together with patch4
rm src/pip/_vendor/certifi/*.pem

# Remove windows executable binaries
rm -v src/pip/_vendor/distlib/*.exe
sed -i '/\.exe/d' pyproject.toml

# Remove unused test requirements
sed -Ei '/(pytest-(cov|xdist|rerunfailures)|proxy\.py)/d' tests/requirements.txt

%if %{with tests}
# tests expect wheels in here
mkdir tests/data/common_wheels
cp -a %{SOURCE1} %{SOURCE2} %{SOURCE3} tests/data/common_wheels
%endif


%if %{with tests}
%generate_buildrequires
# we only use this to generate test requires
# the "pyproject" part is explicitly disabled as it generates a requirement on pip
%pyproject_buildrequires -N tests/requirements.txt
%endif


%build
export PYTHONPATH=./src/
%pyproject_wheel

%if %{with man}
sphinx-build -t man -b man -d docs/build/doctrees/man -c docs/html docs/man docs/build/man
%endif


%install
export PYTHONPATH=./src/
%pyproject_install
%pyproject_save_files -l pip

# We'll install pip as pip3.X
# Later we'll provide symbolic links, manpage links and bashcompletion fixes for alternative names
%if "%{python3_pkgversion}" == "3"
%global alternate_names pip-%{python3_version} pip-3 pip3 pip
%else
%global alternate_names pip-%{python3_version}
%endif

# Provide symlinks to executables
mv %{buildroot}%{_bindir}/pip %{buildroot}%{_bindir}/pip%{python3_version}
rm %{buildroot}%{_bindir}/pip3
for pip in %{alternate_names}; do
ln -s ./pip%{python3_version} %{buildroot}%{_bindir}/$pip
done

%if %{with man}
pushd docs/build/man
install -d %{buildroot}%{_mandir}/man1
for MAN in *1; do
install -pm0644 $MAN %{buildroot}%{_mandir}/man1/${MAN/pip/pip%{python3_version}}
for pip in %{alternate_names}; do
echo ".so ${MAN/pip/pip%{python3_version}}" > %{buildroot}%{_mandir}/man1/${MAN/pip/$pip}
done
done
popd
%endif

mkdir -p %{buildroot}%{bash_completions_dir}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    %{buildroot}%{_bindir}/pip%{python3_version} completion --bash \
    > %{buildroot}%{bash_completions_dir}/pip%{python3_version}

# Make bash completion apply to all alternate names symlinks we install
sed -i -e "s/^\\(complete.*\\) pip%{python3_version}\$/\\1 pip%{python3_version} %{alternate_names}/" \
    -e s/_pip_completion/_pip%{python3_version_nodots}_completion/ \
    %{buildroot}%{bash_completions_dir}/pip%{python3_version}

mkdir -p %{buildroot}%{python_wheel_dir}
install -p %{_pyproject_wheeldir}/%{python_wheel_name} -t %{buildroot}%{python_wheel_dir}


%check
# Verify bundled provides are up to date
%{_rpmconfigdir}/pythonbundles.py src/pip/_vendor/vendor.txt --compare-with '%{bundled 3}'

# Verify no unwanted files are present in the package
grep "exe$" %{pyproject_files} && exit 1 || true
grep "pem$" %{pyproject_files} && exit 1 || true

# Verify we can at least run basic commands without crashing
%{py3_test_envvars} %{buildroot}%{_bindir}/pip%{python3_version} --help
%{py3_test_envvars} %{buildroot}%{_bindir}/pip%{python3_version} list
%{py3_test_envvars} %{buildroot}%{_bindir}/pip%{python3_version} show pip

%if %{with tests}
# Upstream tests
# bash completion tests only work from installed package
pytest_k='not completion'
# this clashes with our PYTHONPATH
pytest_k="$pytest_k and not environments_with_no_pip"
# this seems to require internet (despite no network marker)
# added in https://github.com/pypa/pip/pull/13378 TODO drop this in the next release
pytest_k="$pytest_k and not test_prompt_for_keyring_if_needed and not test_double_install_fail and not test_install_sdist_links and not test_lock_vcs and not test_lock_archive and not test_backend_sees_config_via_sdist"
# this cannot import breezy, TODO investigate
pytest_k="$pytest_k and not (functional and bazaar)"
# failures to investigate
pytest_k="$pytest_k and not test_all_fields and not test_report_mixed_not_found and not test_basic_show"  # "Editable project location" missing
pytest_k="$pytest_k and not test_basic_install_from_wheel"
pytest_k="$pytest_k and not test_check_unsupported"

%pytest -n auto -m 'not network' -k "$(echo $pytest_k)" \
    --ignore tests/functional/test_proxy.py  # no proxy.py in Fedora
%endif


%files -n python%{python3_pkgversion}-%{srcname} -f %{pyproject_files}
%doc README.rst
%if %{with man}
%if "%{python3_pkgversion}" == "3"
%{_mandir}/man1/pip{,3,-3}.1.*
%{_mandir}/man1/pip{,3,-3}-[^3]*.1.*
%endif
%{_mandir}/man1/pip{,-}%{python3_version}.1.*
%{_mandir}/man1/pip{,-}%{python3_version}-*.1.*
%endif
%if "%{python3_pkgversion}" == "3"
%{_bindir}/pip
%{_bindir}/pip3
%{_bindir}/pip-3
%endif
%{_bindir}/pip%{python3_version}
%{_bindir}/pip-%{python3_version}
%dir %{bash_completions_dir}
%{bash_completions_dir}/pip%{python3_version}


%files -n %{python_wheel_pkg_prefix}-%{srcname}-wheel
%license LICENSE.txt
# we own the dir for simplicity
%dir %{python_wheel_dir}/
%{python_wheel_dir}/%{python_wheel_name}

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 25.1.1-19
- Latest state for python-pip

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 25.1.1-18
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Sep 10 2025 Miro Hrončok <miro@hroncok.cz> - 25.1.1-17
- Security fix for the bundled urllib3 for CVE-2025-50181

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 25.1.1-16
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Miro Hrončok <miro@hroncok.cz> - 25.1.1-13
- Use /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem even in truststore
- https://fedoraproject.org/wiki/Changes/dropingOfCertPemFile
- Fixes: rhbz#2380441

* Tue Jul 08 2025 Miro Hrončok <miro@hroncok.cz> - 25.1.1-11
- Use /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
- https://fedoraproject.org/wiki/Changes/dropingOfCertPemFile

* Mon Jun 16 2025 Miro Hrončok <miro@hroncok.cz> - 25.1.1-5
- Rebuilt for Python 3.14
- Fix test failures
- Fixes: rhbz#2335909

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 25.1.1-4
- Bootstrap for Python 3.14

* Wed May 07 2025 Miro Hrončok <miro@hroncok.cz> - 25.1.1-3
- Run functional tests
- Drop test requirement of python-wheel-wheel
- Use pytest-xdist to run tests faster

* Mon May 05 2025 Miro Hrončok <miro@hroncok.cz> - 25.1.1-2
- Remove Recommends only related to unsupported Pythons

* Sat May 03 2025 Miro Hrončok <miro@hroncok.cz> - 25.1.1-1
- Update to 25.1.1
- Fixes: rhbz#2363801

* Sat May 03 2025 Miro Hrončok <miro@hroncok.cz> - 25.1-4
- Stop building the HTML documentation, only build manual pages
- Also build manual pages on RHEL
- The python-pip-doc package is gone but not Obsoleted, it has no
  dependencies

* Tue Apr 29 2025 Tomáš Hrnčiar <thrnciar@redhat.com> - 25.1-1
- Update to 25.1.0 (rhbz#2362438)

* Thu Feb 27 2025 Charalampos Stratakis <cstratak@redhat.com> - 25.0.1-1
- Update to 25.0.1
- Fixes: rhbz#2342135

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 07 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 24.3.1-1
- Update to 24.3.1
- Fixes: rhbz#2321997

* Fri Sep 06 2024 Karolina Surma <ksurma@redhat.com> - 24.2-2
- Verify no unwanted files are present in the package

* Tue Aug 06 2024 Miro Hrončok <miro@hroncok.cz> - 24.2-1
- Update to 24.2
- Fixes: rhbz#2296203

* Fri Jul 26 2024 Karolina Surma <ksurma@redhat.com> - 24.1.1-4
- CI: Prepare for Python 2 removal

* Fri Jul 26 2024 Karolina Surma <ksurma@redhat.com> - 24.1.1-3
- CI: Python 3.5 is gone from all Fedoras (removed in F35)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Karolina Surma <ksurma@redhat.com> - 24.1.1-1
- Update to 24.1.1

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 24.0-5
- Rebuilt for Python 3.13

* Thu Jun 06 2024 Python Maint <python-maint@redhat.com> - 24.0-4
- Bootstrap for Python 3.13

* Tue May 28 2024 Miro Hrončok <miro@hroncok.cz> - 24.0-3
- Fix tests with Python 3.13.0b1

* Thu Mar 07 2024 Miro Hrončok <miro@hroncok.cz> - 24.0-2
- CI: Add Python 3.13

* Wed Feb 28 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 24.0-1
- Update to 24.0

* Thu Jan 25 2024 Miro Hrončok <miro@hroncok.cz> - 23.3.2-1
- Update to 23.3.2

* Mon Jan 22 2024 Miro Hrončok <mhroncok@redhat.com> - 23.3.1-5
- Switched to autogenerated BuildRequires for test dependencies,
  which removed some that were no longer necessary

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Maxwell G <maxwell@gtmx.me> - 23.3.1-3
- Remove unused python3-mock dependency

* Wed Jan 03 2024 Maxwell G <maxwell@gtmx.me> - 23.3.1-2
- Remove weak dependency on python3-setuptools

* Thu Nov 16 2023 Petr Viktorin <pviktori@redhat.com> - 23.3.1-1
- Update to 23.3.1
Resolves: rhbz#2244306

* Fri Aug 04 2023 Miro Hrončok <mhroncok@redhat.com> - 23.2.1-1
- Update to 23.2.1
Resolves: rhbz#2223082

* Fri Aug 04 2023 Miro Hrončok <mhroncok@redhat.com> - 23.1.2-7
- Actually run the tests and build the docs when building this package

* Wed Jul 26 2023 Miro Hrončok <mhroncok@redhat.com> - 23.1.2-6
- Drop no-longer-needed custom changes to /usr/bin/pip*
- Stop Recommending libcrypt.so.1 on Python 3.12+
Resolves: rhbz#2150373

* Tue Jul 25 2023 Python Maint <python-maint@redhat.com> - 23.1.2-5
- Rebuilt for Python 3.12

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 20 2023 Python Maint <python-maint@redhat.com> - 23.1.2-3
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 23.1.2-2
- Bootstrap for Python 3.12

* Fri May 19 2023 Miro Hrončok <mhroncok@redhat.com> - 23.1.2-1
- Update to 23.1.2
Resolves: rhbz#2186979

* Mon Mar 27 2023 Karolina Surma <ksurma@redhat.com> - 23.0.1-2
- Fix compatibility with Sphinx 6+
Resolves: rhbz#2180479

* Mon Feb 20 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 23.0.1-1
- Update to 23.0.1
Resolves: rhbz#2165760

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 14 2022 Karolina Surma <ksurma@redhat.com> - 22.3.1-1
- Update to 22.3.1
Resolves: rhbz#2135044

* Mon Sep 05 2022 Python Maint <python-maint@redhat.com> - 22.2.2-2
- Fix crash when an empty dist-info/egg-info is present
Resolves: rhbz#2115001
- No longer use the rpm_install prefix to determine RPM-installed packages
Related: rhbz#2026979

* Wed Aug 03 2022 Charalampos Stratakis <cstratak@redhat.com> - 22.2.2-1
- Update to 22.2.2
Resolves: rhbz#2109468

* Fri Jul 22 2022 Charalampos Stratakis <cstratak@redhat.com> - 22.2-1
- Update to 22.2
Resolves: rhbz#2109468

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 22.0.4-4
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 22.0.4-3
- Bootstrap for Python 3.11

* Tue Apr 26 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 22.0.4-2
- Fallback to pep517 if setup.py is present and setuptools cannot be imported
- Fixes: rhbz#2020635

* Mon Mar 21 2022 Karolina Surma <ksurma@redhat.com> - 22.0.4-1
- Update to 22.0.4
Resolves: rhbz#2061262

* Wed Feb 16 2022 Lumír Balhar <lbalhar@redhat.com> - 22.0.3-1
- Update to 22.0.3
Resolves: rhbz#2048243

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 25 2021 Miro Hrončok <mhroncok@redhat.com> - 21.3.1-1
- Update to 21.3.1
- Resolves: rhbz#2016682

* Wed Oct 13 2021 Miro Hrončok <mhroncok@redhat.com> - 21.3-1
- Update to 21.3
- Resolves: rhbz#2013026
- Fix incomplete pip-updates in virtual environments

* Wed Oct 06 2021 Charalampos Stratakis <cstratak@redhat.com> - 21.2.3-4
- Remove bundled windows executables
- Resolves: rhbz#2005453

* Thu Sep 23 2021 Miro Hrončok <mhroncok@redhat.com> - 21.2.3-3
- Detect paths not to uninstall from via sysconfig's rpm_prefix install scheme

* Mon Aug 16 2021 Miro Hrončok <mhroncok@redhat.com> - 21.2.3-2
- Fix broken uninstallation by a bogus downstream patch

* Mon Aug 09 2021 Miro Hrončok <mhroncok@redhat.com> - 21.2.3-1
- Update to 21.2.3
- Resolves: rhbz#1985635

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Lumír Balhar <lbalhar@redhat.com> - 21.1.3-1
- Update to 21.1.3
Resolves: rhbz#1976449

* Mon Jun 07 2021 Karolina Surma <ksurma@redhat.com> - 21.1.2-1
- Update to 21.1.2
Resolves: rhbz#1963433

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 21.1.1-3
- Rebuilt for Python 3.10

* Tue Jun 01 2021 Python Maint <python-maint@redhat.com> - 21.1.1-2
- Bootstrap for Python 3.10

* Mon May 10 2021 Karolina Surma <ksurma@redhat.com> - 21.1.1-1
- Update to 21.1.1

* Sat Mar 13 2021 Miro Hrončok <mhroncok@redhat.com> - 21.0.1-2
- python-pip-wheel: Remove bundled provides and libcrypt recommends for Python 2
  (The wheel is Python 3 only for a while)

* Wed Feb 17 2021 Lumír Balhar <lbalhar@redhat.com> - 21.0.1-1
- Update to 21.0.1
Resolves: rhbz#1922592

* Tue Jan 26 2021 Lumír Balhar <lbalhar@redhat.com> - 21.0-1
- Update to 21.0 (#1919530)

* Thu Dec 17 2020 Petr Viktorin <pviktori@redhat.com> - 20.3.3-1
- Update to 20.3.3

* Mon Nov 30 2020 Miro Hrončok <mhroncok@redhat.com> - 20.3-1
- Update to 20.3
- Add support for PEP 600: Future manylinux Platform Tags
- New resolver
- Fixes: rhbz#1893470

* Mon Oct 19 2020 Lumír Balhar <lbalhar@redhat.com> - 20.2.4-1
- Update to 20.2.4 (#1889112)

* Wed Aug 05 2020 Tomas Orsava <torsava@redhat.com> - 20.2.2-1
- Update to 20.2.2 (#1838553)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Lumír Balhar <lbalhar@redhat.com> - 20.1.1-6
- Do not emit a warning about root privileges when --root is used

* Wed Jul 08 2020 Miro Hrončok <mhroncok@redhat.com> - 20.1.1-5
- Update bundled provides to match 20.1.1

* Tue Jun 16 2020 Lumír Balhar <lbalhar@redhat.com> - 20.1.1-4
- Deselect tests incompatible with the latest virtualenv

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 20.1.1-3
- Rebuilt for Python 3.9

* Thu May 21 2020 Miro Hrončok <mhroncok@redhat.com> - 20.1.1-2
- Bootstrap for Python 3.9

* Wed May 20 2020 Tomas Hrnciar <thrnciar@redhat.com> - 20.1.1-1
- Update to 20.1.1

* Wed Apr 29 2020 Tomas Hrnciar <thrnciar@redhat.com> - 20.1-1
- Update to 20.1

* Mon Apr 27 2020 Tomas Hrnciar <thrnciar@redhat.com> - 20.1~b1-1
- Update to 20.1~b1

* Wed Apr 15 2020 Miro Hrončok <mhroncok@redhat.com> - 20.0.2-4
- Only recommend setuptools, don't require them

* Fri Apr 10 2020 Miro Hrončok <mhroncok@redhat.com> - 20.0.2-3
- Allow setting $TMPDIR to $PWD/... during pip wheel (#1806625)

* Tue Mar 10 2020 Miro Hrončok <mhroncok@redhat.com> - 20.0.2-2
- Don't warn the user about pip._internal.main() entrypoint to fix ensurepip

* Mon Mar 02 2020 Miro Hrončok <mhroncok@redhat.com> - 20.0.2-1
- Update to 20.0.2 (#1793456)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 19.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 04 2019 Tomas Orsava <torsava@redhat.com> - 19.3.1-1
- Update to 19.3.1 (#1761508)
- Drop upstreamed patch that fixed expected output in test to not break with alpha/beta/rc Python versions

* Wed Oct 30 2019 Miro Hrončok <mhroncok@redhat.com> - 19.2.3-2
- Make /usr/bin/pip(3) work with user-installed pip 19.3+ (#1767212)

* Mon Sep 02 2019 Miro Hrončok <mhroncok@redhat.com> - 19.2.3-1
- Update to 19.2.3 (#1742230)
- Drop patch that should strip path prefixes from RECORD files, the paths are relative

* Wed Aug 21 2019 Petr Viktorin <pviktori@redhat.com> - 19.1.1-8
- Remove python2-pip
- Make pip bootstrap itself, rather than with an extra bootstrap RPM build

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1.1-7
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1.1-6
- Bootstrap for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1.1-5
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 19.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Petr Viktorin <pviktori@redhat.com> - 19.1.1-3
- Recommend libcrypt.so.1 for manylinux1 compatibility
- Make /usr/bin/pip Python 3

* Mon Jun 10 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1.1-2
- Fix root warning when pip is invoked via python -m pip
- Remove a redundant second WARNING prefix form the abovementioned warning

* Wed May 15 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1.1-1
- Update to 19.1.1 (#1706995)

* Thu Apr 25 2019 Miro Hrončok <mhroncok@redhat.com> - 19.1-1
- Update to 19.1 (#1702525)

* Wed Mar 06 2019 Miro Hrončok <mhroncok@redhat.com> - 19.0.3-1
- Update to 19.0.3 (#1679277)

* Wed Feb 13 2019 Miro Hrončok <mhroncok@redhat.com> - 19.0.2-1
- Update to 19.0.2 (#1668492)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Miro Hrončok <mhroncok@redhat.com> - 18.1-2
- Use the system level root certificate instead of the one bundled in certifi

* Thu Nov 22 2018 Miro Hrončok <mhroncok@redhat.com> - 18.1-1
- Update to 18.1 (#1652089)

* Tue Sep 18 2018 Victor Stinner <vstinner@redhat.com> - 18.0-4
- Prevent removing of the system packages installed under /usr/lib
  when pip install -U is executed. Original patch by Michal Cyprian.
  Resolves: rhbz#1550368.

* Wed Aug 08 2018 Miro Hrončok <mhroncok@redhat.com> - 18.0-3
- Create python-pip-wheel package with the wheel

* Tue Jul 31 2018 Miro Hrončok <mhroncok@redhat.com> - 18.0-2
- Remove redundant "Unicode" from License

* Mon Jul 23 2018 Marcel Plch <mplch@redhat.com> - 18.0-7
- Update to 18.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 9.0.3-5
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 9.0.3-4
- Bootstrap for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 9.0.3-3
- Bootstrap for Python 3.7

* Fri May 04 2018 Miro Hrončok <mhroncok@redhat.com> - 9.0.3-2
- Allow to import pip10's main from pip9's /usr/bin/pip
- Do not show the "new version of pip" warning outside of venv
Resolves: rhbz#1569488
Resolves: rhbz#1571650
Resolves: rhbz#1573755

* Thu Mar 29 2018 Charalampos Stratakis <cstratak@redhat.com> - 9.0.3-1
- Update to 9.0.3

* Wed Feb 21 2018 Lumír Balhar <lbalhar@redhat.com> - 9.0.1-16
- Include built HTML documentation (in the new -doc subpackage) and man page

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 04 2017 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-14
- Reintroduce the ipaddress module in the python3 subpackage.

* Mon Nov 20 2017 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-13
- Add virtual provides for the bundled libraries. (rhbz#1096912)

* Tue Aug 29 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-12
- Switch macros to bcond's and make Python 2 optional to facilitate building
  the Python 2 and Python 3 modules

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-10
- Modernized package descriptions
Resolves: rhbz#1452568

* Tue Mar 21 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-9
- Fix typo in the sudo pip warning

* Fri Mar 03 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-8
- Patch 1 update: No sudo pip warning in venv or virtualenv

* Thu Feb 23 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-7
- Patch 1 update: Customize the warning with the proper version of the pip
  command

* Tue Feb 14 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-6
- Added patch 1: Emit a warning when running with root privileges

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-4
- Provide symlinks to executables to comply with Fedora guidelines for Python
Resolves: rhbz#1406922

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-3
- Rebuild for Python 3.6 with wheel

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-2
- Rebuild for Python 3.6 without wheel

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 9.0.1-1
- Update to 9.0.1

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 8.1.2-5
- Enable EPEL Python 3 builds
- Use new python macros
- Cleanup spec

* Fri Aug 05 2016 Tomas Orsava <torsava@redhat.com> - 8.1.2-4
- Updated the test sources

* Fri Aug 05 2016 Tomas Orsava <torsava@redhat.com> - 8.1.2-3
- Moved python-pip into the python2-pip subpackage
- Added the python_provide macro

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 17 2016 Tomas Orsava <torsava@redhat.com> - 8.1.2-1
- Update to 8.1.2
- Moved to a new PyPI URL format
- Updated the prefix-stripping patch because of upstream changes in pip/wheel.py

* Mon Feb 22 2016 Slavek Kabrda <bkabrda@redhat.com> - 8.0.2-1
- Update to 8.0.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 7.1.0-3
- Rebuilt for Python3.5 rebuild
- With wheel set to 1

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 7.1.0-2
- Rebuilt for Python3.5 rebuild

* Wed Jul 01 2015 Slavek Kabrda <bkabrda@redhat.com> - 7.1.0-1
- Update to 7.1.0

* Tue Jun 30 2015 Ville Skyttä <ville.skytta@iki.fi> - 7.0.3-3
- Install bash completion
- Ship LICENSE.txt as %%license where available

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Matej Stuchlik <mstuchli@redhat.com> - 7.0.3-1
- Update to 7.0.3

* Fri Mar 06 2015 Matej Stuchlik <mstuchli@redhat.com> - 6.0.8-1
- Update to 6.0.8

* Thu Dec 18 2014 Slavek Kabrda <bkabrda@redhat.com> - 1.5.6-5
- Only enable tests on Fedora.

* Mon Dec 01 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-4
- Add tests
- Add patch skipping tests requiring Internet access

* Tue Nov 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-3
- Added patch for local dos with predictable temp dictionary names
  (http://seclists.org/oss-sec/2014/q4/655)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-3
- Disable build_wheel

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-2
- Rebuild as wheel for Python 3.4

* Mon Apr 07 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-1
- Updated to 1.5.4

* Mon Oct 14 2013 Tim Flink <tflink@fedoraproject.org> - 1.4.1-1
- Removed patch for CVE 2013-2099 as it has been included in the upstream 1.4.1 release
- Updated version to 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-4
- Fix for CVE 2013-2099

* Thu May 23 2013 Tim Flink <tflink@fedoraproject.org> - 1.3.1-3
- undo python2 executable rename to python-pip. fixes #958377
- fix summary to match upstream

* Mon May 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.1-2
- Fix main package Summary, it's for Python 2, not 3 (#877401)

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.3.1-1
- Update to 1.3.1, fix for CVE-2013-1888.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Fri Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file
* Thu Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package

## END: Generated by rpmautospec
