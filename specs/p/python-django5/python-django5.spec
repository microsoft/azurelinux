## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Main Django, i.e. whether this is the main Django version in the distribution
# that owns /usr/bin/django-admin and other unique paths
# based on Python packaging, see e.g. python3.13
%if 0%{?fedora} >= 42 && 0%{?fedora} < 44
%bcond main_django 1
%else
%bcond main_django 0
%endif

%if 0%{?python3_version_nodots} >= 314
# some tests currently fail
%bcond all_tests 0
%else
%bcond all_tests 1
%endif

%if %{defined fedora} && 0%{?fedora} == 42
%bcond old_setuptools 1
%else
%bcond old_setuptools 0
%endif

Version:        5.2.11
%global major_ver %(echo %{version} | cut -d. -f1)
Name:           python-django%{major_ver}

Release:        %autorelease
Summary:        A high-level Python Web framework

# Django: BSD-3-Clause
# Bundled Python code: PSF-2.0
# Font Awesome font: OFL-1.1
# Font Awesome icons: MIT
# jquery, select2, xregexp: MIT
# gis/gdal: BSD-3-Clause
# gis/geos: BSD-3-Clause
License:        BSD-3-Clause AND PSF-2.0 AND MIT AND OFL-1.1
URL:            https://www.djangoproject.com/
Source:         %{pypi_source django}
Source:         %{name}.rpmlintrc

# conditional patches: >= 1000
# test_strip_tags() failing with Python 3.14
# https://code.djangoproject.com/ticket/36499
#
# also test_parsing_errors()
# https://code.djangoproject.com/ticket/36515
# ======================================================================
# FAIL: test_parsing_errors (test_utils.tests.HTMLEqualTests.test_parsing_errors)
# ----------------------------------------------------------------------
# AssertionError: &lt; div&gt; != <div>
# - &lt; div&gt;   
# + <div>
Patch1000:      django-py314-skip-failing-tests.diff
# setuptools 77 is only needed to support the new license metadata
Patch1001:      django-allow-setuptools-ge-69.diff
# This allows to build the package without tests, e.g. when bootstrapping new Python version
%bcond tests    1

BuildArch:      noarch

%global _description %{expand:
Django is a high-level Python Web framework that encourages rapid
development and a clean, pragmatic design. It focuses on automating as
much as possible and adhering to the DRY (Don't Repeat Yourself)
principle.}

%description %_description


%if %{with main_django}
%global pkgname python3-django
%else
%global pkgname python3-django%{major_ver}
%endif

%package -n %{pkgname}-bash-completion
Summary:        Bash completion files for Django
BuildRequires:  bash-completion
Requires:       bash-completion

# Make sure this replaces any other Django bash-completion package
Provides:       python-django-bash-completion-impl
Conflicts:      python-django-bash-completion-impl

%description -n %{pkgname}-bash-completion
This package contains the Bash completion files form Django high-level
Python Web framework.


%package -n %{pkgname}-doc
Summary:        Documentation for Django
# Font Awesome: CC-BY-4.0, OFL-1.1, MIT
License:        BSD-3-Clause AND CC-BY-4.0 AND OFL-1.1 AND MIT
Suggests:       %{pkgname} = %{version}-%{release}
BuildRequires:  make

# Make sure this replaces any other Django doc package
Provides:       python-django-doc-impl
Conflicts:      python-django-doc-impl

%description -n %{pkgname}-doc
This package contains the documentation for the Django high-level
Python Web framework.


%package -n %{pkgname}
Summary:        A high-level Python Web framework

Recommends:     (%{pkgname}-bash-completion = %{version}-%{release} if bash-completion)

BuildRequires:  python3-devel
BuildRequires:  python3-asgiref

# see django/contrib/admin/static/admin/js/vendor/
Provides:       bundled(jquery) = 3.6.4
Provides:       bundled(select2) = 4.0.13
Provides:       bundled(xregexp) = 3.2.0

# Make sure this replaces any other Django package
Provides:       python-django-impl
Conflicts:      python-django-impl

%description -n %{pkgname} %_description

%prep
%autosetup -N -n django-%{version}
%autopatch -p1 -M 999
%if %{without all_tests}
%autopatch -p1 1000
%endif
%if %{with old_setuptools}
%autopatch -p1 1001
%endif

# hard-code python3 in django-admin
pushd django
for file in conf/project_template/manage.py-tpl ; do
    sed -i "s/\/env python/\/python3/" $file ;
done
popd

# Use non optimised psycopg for tests
# Not available in Fedora
sed -i 's/psycopg\[binary\]>=3\.1\.8/psycopg>=3.1.8/' tests/requirements/postgres.txt

# Remove unnecessary test BRs
sed -i '/^pywatchman\b/d' tests/requirements/py3.txt
sed -i '/^tzdata$/d' tests/requirements/py3.txt

# Remove deps on code checkers/linters
sed -i '/^black\b/d' tests/requirements/py3.txt
sed -i '/^black\b/d' docs/requirements.txt
sed -i '/^blacken-docs\b/d' docs/requirements.txt

%generate_buildrequires
%pyproject_buildrequires -r %{?with_tests:tests/requirements/{py3,postgres,mysql,oracle}.txt} docs/requirements.txt

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files django

# build documentation
(cd docs && mkdir djangohtml && mkdir -p _build/{doctrees,html} && make html)
mkdir -p %{buildroot}%{_docdir}/python3-django-doc
cp -ar docs/_build/html/* %{buildroot}%{_docdir}/python3-django-doc/

# install man pages (for the main executable only)
mkdir -p %{buildroot}%{_mandir}/man1/
cp -p docs/man/* %{buildroot}%{_mandir}/man1/

# install bash completion script
mkdir -p %{buildroot}%{bash_completions_dir}
install -m 0644 -p extras/django_bash_completion \
  %{buildroot}%{bash_completions_dir}/django-admin

for file in manage.py ; do
   ln -s django-admin.py %{buildroot}%{bash_completions_dir}/$file
done

# remove .po files
find %{buildroot} -name "*.po" | xargs rm -f
sed -i '/.po$/d' %{pyproject_files}

%check
# many contrib modules assume a configured app, "Requested setting INSTALLED_APPS..."
# the rest needs optional dependencies
%{pyproject_check_import \
    -e 'django.contrib.*' \
    -e 'django.core.serializers.pyyaml' \
    -e 'django.db.backends.mysql*' \
    -e 'django.db.backends.oracle*' \
    -e 'django.db.backends.postgresql*'}

%if %{with tests}
cd %{_builddir}/django-%{version}
export PYTHONPATH=$(pwd)
cd tests

%{python3} runtests.py --settings=test_sqlite --verbosity=2
%endif

%files -n %{pkgname}-bash-completion
%{bash_completions_dir}/*

%files -n %{pkgname}-doc
%doc %{_docdir}/python3-django-doc/*
%license LICENSE
%license %{_docdir}/python3-django-doc/_static/fontawesome/LICENSE.txt

%files -n %{pkgname} -f %{pyproject_files}
%doc AUTHORS README.rst
%doc %{python3_sitelib}/django/contrib/admin/static/admin/img/README.txt
%license %{python3_sitelib}/django/contrib/admin/static/admin/css/vendor/select2/LICENSE-SELECT2.md
%license %{python3_sitelib}/django/contrib/admin/static/admin/img/LICENSE
%license %{python3_sitelib}/django/contrib/admin/static/admin/js/vendor/jquery/LICENSE.txt
%license %{python3_sitelib}/django/contrib/admin/static/admin/js/vendor/select2/LICENSE.md
%license %{python3_sitelib}/django/contrib/admin/static/admin/js/vendor/xregexp/LICENSE.txt
%license %{python3_sitelib}/django/contrib/gis/gdal/LICENSE
%license %{python3_sitelib}/django/contrib/gis/geos/LICENSE
%{_bindir}/django-admin
%{_mandir}/man1/django-admin.1*


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 5.2.11-2
- test: add initial lock files

* Thu Feb 19 2026 Michel Lind <salimma@fedoraproject.org> - 5.2.11-1
- Update to version 5.2.11; Resolves: RHBZ#2427483
- `python-django5` is now the alternate `python3-django5` on Fedora 44+,
  `python3-django` is now Django 6.x
- Fixes CVE-2025-13473: Username enumeration through timing difference in
  mod_wsgi authentication handler
- Fixes CVE-2025-14550: Potential denial-of-service vulnerability via
  repeated headers when using ASGI
- Fixes CVE-2026-1207: Potential SQL injection via raster lookups on
  PostGIS
- Fixes CVE-2026-1285: Potential denial-of-service vulnerability in
  django.utils.text.Truncator HTML methods
- Fixes CVE-2026-1287: Potential SQL injection in column aliases via
  control characters
- Fixes CVE-2026-1312: Potential SQL injection via QuerySet.order_by and
  FilteredRelation
- Fixed a bug in Django 5.2 where data exceeding max_length was silently
  truncated by QuerySet.bulk_create() on PostgreSQL
- Fixed a bug where management command colorized help (introduced in Python
  3.14) ignored the --no-color option and the DJANGO_COLORS setting

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 08 2025 Michel Lind <salimma@fedoraproject.org> - 5.2.9-1
- Update to version 5.2.9
- Fixes CVE-2025-13372: Potential SQL injection in FilteredRelation column
  aliases on PostgreSQL
- Fixes CVE-2025-64460: Potential denial-of-service vulnerability in XML
  Deserializer
- Fixes CVE-2025-64459: Potential SQL injection via _connector keyword
  argument (5.2.8)
- Fixes CVE-2025-59681: Potential SQL injection in QuerySet.annotate(),
  alias(), aggregate(), and extra() on MySQL and MariaDB (5.2.7)
- Fixes CVE-2025-59682: Potential partial directory-traversal via
  archive.extract() (5.2.7)
- Fixes CVE-2025-57833: Potential SQL injection in FilteredRelation column
  aliases (5.2.6)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.2.4-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.2.4-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Michel Lind <salimma@fedoraproject.org> - 5.2.4-1
- Update to version 5.2.4
- Skip test_strip_tags and test_parsing_errors on Python 3.14; Fixes:
  RHBZ#2374042

* Mon Jul 21 2025 Python Maint <python-maint@redhat.com> - 5.2.2-3
- Unbootstrap for Python 3.14

* Wed Jun 18 2025 Python Maint <python-maint@redhat.com> - 5.2.2-2
- Bootstrap for Python 3.14.0b3 bytecode

* Mon Jun 09 2025 Michel Lind <salimma@fedoraproject.org> - 5.2.2-1
- Update to 5.2.2
- Fixes CVE-2025-32873: Denial-of-service possibility in strip_tags()
- Fixes CVE-2025-48432: Potential log injection via unescaped request path

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.1.8-4
- Bootstrap for Python 3.14

* Mon May 26 2025 Karolina Surma <ksurma@redhat.com> - 5.1.8-3
- Enable compatibility with Python 3.14+

* Wed May 14 2025 Lumir Balhar <lbalhar@redhat.com> - 5.1.8-2
- Remove upper limit from setuptools version

* Fri Apr 04 2025 Michel Lind <salimma@fedoraproject.org> - 5.1.8-1
- Update to 5.1.8
- On Windows, this fixes CVE-2025-27556. Mentioning for compleness
- Fixes a regression in Django 5.1.7 affecting
  LogEntryManager.log_actions() - #36234
- Remove legacy symlinks

* Wed Mar 19 2025 Tomáš Hrnčiar <thrnciar@redhat.com> - 5.1.7-2
- Adjust patch to allow setuptools <77

* Sat Mar 08 2025 Michel Lind <salimma@fedoraproject.org> - 5.1.7-1
- Update to version 5.1.7; Fixes: RHBZ#2350881
- Fix for CVE-2025-26699: Potential denial-of-service vulnerability in
  django.utils.text.wrap()

* Sat Feb 15 2025 Michel Lind <salimma@fedoraproject.org> - 5.1.6-1
- Initial package; Resolves: RHBZ#2345877
## END: Generated by rpmautospec
