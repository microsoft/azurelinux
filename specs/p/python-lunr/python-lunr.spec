# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-lunr
Version:        0.8.0
Release:        5%{?dist}
Summary:        A Python implementation of Lunr.js

License:        MIT
URL:            https://github.com/yeraydiazdiaz/lunr.py
BuildArch:      noarch
Source0:        %{pypi_source lunr}

BuildRequires:  python3-devel
# For tests
BuildRequires:  python3dist(pytest)


%description
This Python version of Lunr.js aims to bring the simple and powerful full text
search capabilities into Python guaranteeing results as close as the original
implementation as possible.


%package -n python3-lunr
Summary:        %{summary}

%description -n python3-lunr
This Python version of Lunr.js aims to bring the simple and powerful full text
search capabilities into Python guaranteeing results as close as the original
implementation as possible.


%pyproject_extras_subpkg -n python3-lunr languages


%generate_buildrequires
%pyproject_buildrequires -r -x languages


%prep
%autosetup -p1 -n lunr-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files lunr


%check
# test_reduces_words_to_their_stem requires missing tests/fixtures/stemming_vocab.json
# test_lunr_function_registers_nltk_stemmers_in_pipeline requires network
# test_lunr_registers_lun_stemmers_in_pipeline_if_language_is_en requires network
# test_search_stems_search_terms requires network
# test_search_stems_search_terms_for_both_languages requires network
%pytest -k "not test_reduces_words_to_their_stem and \
            not test_lunr_function_registers_nltk_stemmers_in_pipeline and \
            not test_lunr_registers_lun_stemmers_in_pipeline_if_language_is_en and \
            not test_search_stems_search_terms and \
            not test_search_stems_search_terms_for_both_languages and \
            not acceptance"


%files -n python3-lunr -f %{pyproject_files}
%doc README.md
%license LICENSE


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.8.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.8.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.8.0-2
- Rebuilt for Python 3.14

* Tue Mar 11 2025 Sandro Mani <manisandro@gmail.com> - 0.8.0-1
- Update to 0.8.0

* Sun Jan 26 2025 Romain Geissler <romain.geissler@amadeus.com> - 0.7.0.post1-7
- Remove deprecated mock dependency.

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0.post1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0.post1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.7.0.post1-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0.post1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0.post1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 12 2023 Sandro Mani <manisandro@gmail.com> - 0.7.0.post1-1
- Update to 0.7.0.post1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 0.6.2-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Python Maint <python-maint@redhat.com> - 0.6.2-2
- Rebuilt for Python 3.11

* Mon Feb 28 2022 Sandro Mani <manisandro@gmail.com> - 0.6.3-1
- Update to 0.6.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Sandro Mani <manisandro@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Wed Jan 05 2022 Sandro Mani <manisandro@gmail.com> - 0.6.0-4
- Modernize spec

* Fri Oct 08 2021 Sandro Mani <manisandro@gmail.com> - 0.6.0-3
- Remove nltk version constraint to fix FailsToInstall

* Mon Oct 04 2021 Sandro Mani <manisandro@gmail.com> - 0.6.0-2
- Rebuild to fix FailsToInstall

* Thu Sep 30 2021 Sandro Mani <manisandro@gmail.com> - 0.6.0-1
- Update to 0.6.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.5.8-6
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 0.5.8-3
- Add lunr[languages] subpackage

* Thu Jun 25 2020 Robin Lee <cheeselee@fedoraproject.org> - 0.5.8-2
- BR python3dist(setuptools)

* Fri Jun 12 2020 Qiyu Yan <yanqiyu01@gmail.com> - 0.5.8-1
- Update to 0.5.8

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.5.6-2
- Rebuilt for Python 3.9

* Sun Mar  8 2020 Robin Lee <cheeselee@fedoraproject.org> - 0.5.6-1
- Initial packaging
