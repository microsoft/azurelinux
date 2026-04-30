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

%bcond_without check

%global _description %{expand: 
Scikit-learn integrates machine learning algorithms in the tightly-knit 
scientific Python world, building upon numpy, scipy, and matplotlib. 
As a machine-learning module, it provides versatile tools for data mining 
and analysis in any field of science and engineering. It strives to be 
simple and efficient, accessible to everybody, and reusable 
in various contexts.}

Name: python-scikit-learn
Version: 1.7.2
Release: %autorelease
Summary: Machine learning in Python
# sklearn/externals/_arff.py is MIT
# sklearn/externals/_packaging is BSD-2-Clause
# sklearn/metrics/_scorer.py is BSD-2-Clause
# sklearn/datasets/images/china.jpg  is CC-BY-2.0
# sklearn/datasets/images/flower.jpg is CC-BY-2.0
# sklearn/utils/_pprint.py is PSF-2.0
License: BSD-3-Clause AND CC-BY-2.0 AND MIT AND BSD-2-Clause AND PSF-2.0

URL: http://scikit-learn.org/
Source0: %{pypi_source scikit_learn}

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: python3-devel
BuildRequires: %{py3_dist setuptools}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

%description %_description

%package -n python3-scikit-learn
Summary: %{summary}

# For a brief moment, this package was accidentally named this way
# The Obsoletes clears the upgrade path and can be removed when Rawhide is F44
Obsoletes: python3-scikit_learn < 1.5.2-2

%if %{with check}
BuildRequires: %{py3_dist pytest} >= 7.1.2
BuildRequires: %{py3_dist joblib} >= 1.2.0
BuildRequires: %{py3_dist threadpoolctl} >= 2.0.0
%endif

%{?python_provide:%python_provide python3-sklearn}

%description -n python3-scikit-learn
%_description

%prep
%autosetup -n scikit_learn-%{version} -p1
sed -i -e 's|numpy>=2,<2.3.0|numpy|' pyproject.toml
# EPEL 10 has Cython 3.0.9, and the only reason Cython 3.0.10
# is required upstream is for Windows, see
# https://github.com/scikit-learn/scikit-learn/pull/28743
sed -i -e 's|Cython>=3.0.10|Cython>=3.0.9|' pyproject.toml
sed -i -e 's|CYTHON_MIN_VERSION = "3.0.10"|CYTHON_MIN_VERSION = "3.0.9"|' sklearn/_min_dependencies.py
find sklearn/metrics/_dist_metrics.pyx.tp -type f | xargs sed -i 's/cdef inline {{INPUT_DTYPE_t}} rdist/cdef {{INPUT_DTYPE_t}} rdist/g'

%generate_buildrequires
# Some tests packages not in Fedora
%pyproject_buildrequires -p

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files sklearn

%check
%if %{with check}
export PYTHONDONTWRITEBYTECODE=1
export PYTEST_ADDOPTS='-p no:cacheprovider'
pushd %{buildroot}%{python3_sitearch}
  pytest  \
  --deselect "sklearn/datasets/tests/test_openml.py::test_fetch_openml_verify_checksum[True-liac-arff]" \
  --deselect "sklearn/datasets/tests/test_openml.py::test_fetch_openml_verify_checksum[False-liac-arff]" \
  --deselect "sklearn/datasets/tests/test_openml.py::test_fetch_openml_verify_checksum[True-pandas]" \
  --deselect "sklearn/datasets/tests/test_openml.py::test_fetch_openml_verify_checksum[False-pandas]" \
  --deselect "sklearn/covariance/tests/test_covariance.py" \
  --deselect "sklearn/covariance/tests/test_robust_covariance.py" \
  --deselect "sklearn/linear_model/tests/test_bayes.py::test_toy_ard_object" \
  --deselect "sklearn/linear_model/tests/test_bayes.py::test_ard_accuracy_on_easy_problem[42-10-100]" \
  --deselect "sklearn/linear_model/tests/test_bayes.py::test_ard_accuracy_on_easy_problem[42-100-10]" \
%if 0%{?el10}
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression(max_iter=5)-check_dont_overwrite_parameters]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression(max_iter=5)-check_f_contiguous_array_estimator]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression(max_iter=5)-check_regressors_no_decision_function]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression(max_iter=5)-check_methods_sample_order_invariance]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression(max_iter=5)-check_methods_subset_invariance]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression(max_iter=5)-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression(max_iter=5)-check_dict_unchanged]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ARDRegression(max_iter=5)-check_fit2d_predict1d]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[EllipticEnvelope()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[EmpiricalCovariance()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA(max_iter=5)-check_dont_overwrite_parameters]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA(max_iter=5)-check_methods_sample_order_invariance]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA(max_iter=5)-check_methods_subset_invariance]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA(max_iter=5)-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA(max_iter=5,n_components=1)-check_dict_unchanged]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[FastICA(max_iter=5)-check_fit2d_predict1d]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[KernelPCA()-check_fit2d_1sample]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[LedoitWolf()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[MinCovDet()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[OAS()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[RidgeCV()-check_fit2d_1sample]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[RidgeClassifierCV()-check_fit2d_1sample]" \
  --deselect "sklearn/tests/test_common.py::test_estimators[ShrunkCovariance()-check_fit2d_1feature]" \
  --deselect "sklearn/tests/test_common.py::test_check_inplace_ensure_writeable[ARDRegression(max_iter=5)]" \
%endif
  --deselect "sklearn/utils/tests/test_validation.py::test_check_is_fitted_with_attributes[list]" \
  --deselect "sklearn/utils/tests/test_validation.py::test_check_is_fitted" \
  --deselect "sklearn/cluster/tests/test_optics.py::test_warn_if_metric_bool_data_no_bool" \
  --deselect "sklearn/datasets/tests/test_openml.py::test_open_openml_url_retry_on_network_error" \
%ifarch ppc64le
  --deselect "sklearn/tests/test_calibration.py::test_calibrated_classifier_cv_zeros_sample_weights_equivalence[True-isotonic]" \
%endif
  sklearn
popd

%else
%py3_check_import sklearn
%endif

%files -n python3-scikit-learn -f %{pyproject_files}
%doc examples/
%license COPYING sklearn/svm/src/liblinear/COPYRIGHT

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.7.2-2
- test: add initial lock files

* Fri Sep 26 2025 Sergio Pascual <sergiopr@fedoraproject.org> - 1.7.2-1
- New upstream source 1.7.2

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.7.1-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.7.1-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 31 2025 Charalampos Stratakis <cstratak@redhat.com> - 1.7.1-1
- Update to 1.7.1
- Fixes: rhbz#2365349, rhbz#2377055

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.6.1-6
- Rebuilt for Python 3.14

* Thu May 29 2025 Karolina Surma <ksurma@redhat.com> - 1.6.1-4
- Skip more tests counting warnings - they are not reliable

* Thu Mar 13 2025 Romain Geissler <romain.geissler@amadeus.com> - 1.6.1-3
- Adapt test suite failures for EPEL 10.

* Thu Mar 13 2025 Romain Geissler <romain.geissler@amadeus.com> - 1.6.1-2
- Relax Cython requirement for EPEL 10.

* Thu Feb 27 2025 Sergio Pascual <sergiopr@fedoraproject.org> - 1.6.1-1
- New upstream version 1.6.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 19 2024 Orion Poplawski <orion@nwra.com> - 1.6.0-1
- Update to 1.6.0 (rhbz#2326488)

* Wed Nov 27 2024 Miroslav Suchý <msuchy@redhat.com> - 1.5.2-6
- Correct SPDX license

* Tue Nov 26 2024 Sergio Pascual <sergiopr@fedoraproject.org> - 1.5.2-5
- Review license to conform to spdx

* Mon Nov 18 2024 Miro Hrončok <miro@hroncok.cz> - 1.5.2-4
- Obsolete python3-scikit_learn

* Sat Nov 16 2024 Adam Williamson <awilliam@redhat.com> - 1.5.2-2
- Correct binary package name back to python3-scikit-learn

* Wed Nov 13 2024 Sergio Pascual <sergiopr@fedoraproject.org> - 1.5.2-1
- New upstream source 1.5.2

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.4.1.post1-5
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1.post1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.4.1.post1-3
- Rebuilt for Python 3.13

* Tue Mar 12 2024 Sergio Pascual <sergiopr@fedoraproject.org> - 1.4.1.post1-1
- Drop i686 arch

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Sep 30 2023 Sergio Pascual <sergiopr@fedoraproject.org> - 1.3.1-2
- Skip test faillure in i686

* Sat Sep 30 2023 Sergio Pascual <sergiopr@fedoraproject.org> - 1.3.1-1
- New upstream source (1.3.1)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 08 2023 Sergio Pascual <sergiopr@fedoraproject.org> - 1.3.0-1
- New upstream source (1.3.0)

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 1.2.2-2
- Rebuilt for Python 3.12

* Tue May 02 2023 Sergio Pascual <sergiopr@fedoraproject.org> - 1.2.2-1
- New upstream source (1.2.2)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 25 2022 Sergio Pascual <sergiopr@fedoraproject.org> - 1.1.2-1
- New upstream source (1.1.2)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul  3 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.2-4
- Kill failing tests on ppc64le for now

* Mon Jun 20 2022 Python Maint <python-maint@redhat.com> - 1.0.2-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 27 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 1.0.2-1
- New upstream source (1.0.2)

* Wed Oct 06 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 1.0-1
- New upstream source (1.0)

* Wed Aug 25 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.24.2-2
- Fix FTBFS (#1987890)
- Skip tests in armv7hl, collection causes core dumpep

* Mon Aug 23 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.24.2-1
- New upstream source (0.24.2)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 17 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.24.1-5
- Enabled testing

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.24.1-4
- Rebuilt for Python 3.10

* Tue Feb 16 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.24.1-3
- New upstream source (0.24.1)
- Disable testing (too long)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.24.0-1
- New upstream source (0.24.0)

* Wed Aug 26 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.23.2-1
- New upstream source (0.23.2)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 28 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.23.1-1
- New upstream source (0.23.1)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.23.0-3
- Rebuilt for Python 3.9

* Sun May 24 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.23.0-2
- Add missing dependency on threadpoolctl (bz #1836744)

* Sun May 17 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.23.0-1
- New upstream source (0.23.0)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 12 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.22.1
- New upstream source (0.22.1)

* Sat Jan 11 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.22-1
- New upstream source (0.22)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.21.3-2
- Rebuilt for Python 3.8

* Thu Aug 01 2019 Sergio Pascual <sergiopr@fedoraproject.org> - 0.21.3-1
- New upstream source (0.21.3)
- Add a patch to fix detection of openmp

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 15 2018 Miro Hrončok <mhroncok@redhat.com> - 0.19.1-6
- Subpackage python2-scikit-learn has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Jul 17 2018 Christian Dersch <lupinix@fedoraproject.org> - 0.19.1-5
- BuildRequires: gcc gcc-c++

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.19.1-3
- Rebuilt for Python 3.7
- Recythonize the .c/.cpp files to fix FTBFS on Python 3.7
- Use python2-Cython, not Cython

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 03 2017 Colin B. Macdonald <cbm@m.fsf.org> - 0.19.1-1
- New upstream (0.19.1)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Sergio Pascual <sergiopr@fedoraproject.org> - 0.18.1-1
- New upstream (0.18.1)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.18-3
- Rebuild for Python 3.6

* Sun Nov  6 2016 Orion Poplawski <orion@cora.nwra.com> - 0.18-2
- Rebuild for ppc64

* Thu Oct 27 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.18-1
- New upstream (0.18)
- Updatd patch blas-name
- Removed patch sklearn-np11 (already in upstream)

* Sat Oct 15 2016 Peter Robinson <pbrobinson@fedoraproject.org> - 0.17.1-6
- rebuilt for matplotlib-2.0.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Mar 30 2016 Björn Esser <fedora@besser82.io> - 0.17.1-4
- add Provides for python(2|3)-sklearn

* Wed Mar 30 2016 Björn Esser <fedora@besser82.io> - 0.17.1-3
- add proper Provides and Obsoletes

* Wed Mar 30 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.17.1-2.1
- Skip tests for the moment

* Tue Mar 29 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.17.1-2
- New upstream (0.17.1)
- Provide python2-scikit-learn
- Add patch for numpy1.11
- New style macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 25 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.17-1
- Update to latest version
- Force linking to atlas

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 09 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.16.1-1
- New upstream (0.16.1), bugfix

* Thu Apr 09 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.16.0-2
- Readd provides filter
- Increase joblib minimum version
- New upstream (0.16.0)

* Tue Sep 16 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.2-2
- Remove patch for broken test (fixed in scipy 0.14.1)

* Tue Sep 16 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.2-1
- New upstream (0.15.2), bugfix

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.1-1
- New upstream (0.15.1), bugfix

* Tue Jul 15 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.0-1
- New upstream (0.15.0), final

* Wed Jul 02 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.0-0.5.b2
- New upstream (0.15.0b2), beta release

* Tue Jun 24 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.0-0.4.b1
- Add COPYING to docs
- Spec cleanup

* Mon Jun 23 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.0-0.3.b1
- New upstream (0.15.0b1), beta release
- Add tarball
- Disable tests for the moment

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.14.1-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Jun 02 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.14.1-7
- Rerun Cython3 on broken files
- Disable tests for the moment

* Thu May 29 2014 Björn Esser <bjoern.esser@gmail.com> - 0.14.1-6
- rebuilt for Python3 3.4

* Wed Jan 15 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.14.1-5
- Enable checks
- Regenerate C files from patched cython code
- Use python2 style macros

* Sat Oct 26 2013 Björn Esser <bjoern.esser@gmail.com> - 0.14.1-4
- rebuilt for atlas-3.10.1-7

* Mon Sep 16 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.14.1-3
- Unbundle six

* Wed Sep 11 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.14.1-2
- Update cblas patch
- Update EVR to build with new numpy (1.8.0-0.3b2)

* Wed Aug 28 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.14.1-1
- New upstream source (0.14.1)
- Add python3 support
- Unbundle joblib and cblas

* Wed Jul 10 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.13.1-3
- Reorder buildrequires and requires
- Dropped doc, it does not build

* Tue Jun 25 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.13.1-2
- Changed package name
- Tests do not need recompile

* Thu Apr 18 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.13.1-1
- Initial spec file

## END: Generated by rpmautospec
