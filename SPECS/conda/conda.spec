Summary:        Cross-platform, Python-agnostic binary package manager
Name:           conda
Version:        24.1.2
Release:        2%{?dist}
License:        BSD-3-Clause AND Apache-2.0
# The conda code is BSD-3-Clause
# adapters/ftp.py is Apache-2.0
URL:            http://conda.pydata.org/docs/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/conda/conda/archive/%{version}/%{name}-%{version}.tar.gz
# bash completion script moved to a separate project
Source1:        https://raw.githubusercontent.com/tartansandal/conda-bash-completion/1.7/conda
Patch0:         conda_sys_prefix.patch
# Use main entry point for conda and re-add conda-env entry point, no need to run conda init
Patch1:         0001-Use-main-entry-point-for-conda-and-re-add-conda-env-.patch
# Use system cpuinfo
Patch3:         conda-cpuinfo.patch

Patch10004:     0004-Do-not-try-to-run-usr-bin-python.patch
Patch10005:     0005-Fix-failing-tests-in-test_api.py.patch
Patch10006:     0006-shell-assume-shell-plugins-are-in-etc.patch

BuildArch:      noarch

BuildRequires:  pkgconfig(bash-completion)
%global bash_completionsdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null || echo '/etc/bash_completion.d')
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec
BuildRequires:  python3-pip
BuildRequires:  python3-pluggy
%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-trove-classifiers
BuildRequires:  sed

Requires:       python%{python3_pkgversion}-conda = %{version}-%{release}

%?python_enable_dependency_generator


%global _description %{expand:
Conda is a cross-platform, Python-agnostic binary package manager. It
is the package manager used by Anaconda installations, but it may be
used for other systems as well. Conda makes environments first-class
citizens, making it easy to create independent environments even for
C libraries. Conda is written entirely in Python.

The Fedora conda base environment is special.  Unlike a standard
anaconda install base environment it is essentially read-only.  You
can only use conda to create and manage new environments.}


%description %_description

%global _py3_reqs \
        python%{python3_pkgversion}-cpuinfo \
        python%{python3_pkgversion}-conda-package-handling >= 1.3.0 \
        python%{python3_pkgversion}-cytoolz >= 0.8.2 \
        python%{python3_pkgversion}-distro >= 1.0.4 \
        python%{python3_pkgversion}-frozendict >= 1.2 \
        python%{python3_pkgversion}-pycosat >= 0.6.3 \
        python%{python3_pkgversion}-pyOpenSSL >= 16.2.0 \
        python%{python3_pkgversion}-PyYAML \
        python%{python3_pkgversion}-requests >= 2.18.4 \
        python%{python3_pkgversion}-ruamel-yaml >= 0.11.14 \
        python%{python3_pkgversion}-tqdm >= 4.22.0 \
        python%{python3_pkgversion}-urllib3 >= 1.19.1
%global py3_reqs %(c="%_py3_reqs"; echo "$c" | xargs)

%package tests
Summary:        conda tests

%description tests
Data for conda tests.  Set CONDA_TEST_DATA_DIR to
%{_datadir}/conda/tests/data.

%package -n python%{python3_pkgversion}-conda
Summary:        %{summary}

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools_scm
BuildRequires:  %py3_reqs

# For tests
BuildRequires:  python3
%if 0%{?with_check}
BuildRequires:  python%{python3_pkgversion}-jsonpatch
BuildRequires:  python%{python3_pkgversion}-pytest-mock
BuildRequires:  python%{python3_pkgversion}-responses
%endif

Requires:       %py3_reqs
# Some versions in conda/_vendor/vendor.txt
Provides:       bundled(python%{python3_pkgversion}-appdirs) = 1.2.0
Provides:       bundled(python%{python3_pkgversion}-auxlib) = 0.0.43
Provides:       bundled(python%{python3_pkgversion}-boltons) = 21.0.0

%{?python_provide:%python_provide python%{python3_pkgversion}-conda}

%description -n python%{python3_pkgversion}-conda %_description

%prep
%autosetup -p1

# Do not restrict upper bound of ruamel-yaml
sed -i -e '/ruamel.yaml/s/,<[0-9.]*//' pyproject.toml

# pytest-split/xdoctest not packaged, store-duration not needed
sed -i -e '/splitting-algorithm/d' -e '/store-durations/d' -e '/xdoctest/d' pyproject.toml

# delete interpreter line, the user can always call the file
# explicitly as python3 /usr/lib/python3.6/site-packages/conda/_vendor/appdirs.py
# or so.
sed -r -i '1 {/#![/]usr[/]bin[/]env/d}' conda/_vendor/appdirs.py

# Use Fedora's cpuinfo since it supports more arches
rm -r conda/_vendor/cpuinfo
sed -i -e '/^dependencies = /a\ \ "py-cpuinfo",' pyproject.toml

# Use system versions
rm -r conda/_vendor/{distro.py,frozendict}
find conda -name \*.py | xargs sed -i -e 's/^\( *\)from .*_vendor\.\(\(distro\|frozendict\).*\) import/\1from \2 import/'
sed -i -e '/^dependencies = /a\ \ "distro",' pyproject.toml
sed -i -e '/^dependencies = /a\ \ "frozendict",' pyproject.toml

# Unpackaged - use vendored version
sed -i -e '/"boltons *>/d' pyproject.toml

# Unpackaged - really only applicable for macOS/Windows?
sed -i -e '/"truststore *>/d' pyproject.toml

%ifnarch x86_64
# Tests on non-x86_64
cp -a tests/data/conda_format_repo/{linux-64,%{python3_platform}}
sed -i -e s/linux-64/%{python3_platform}/ tests/data/conda_format_repo/%{python3_platform}/*json
%endif

# Do not run coverage in pytest
sed -i -e '/"--cov/d' pyproject.toml

%generate_buildrequires
# When not testing, we don't need runtime dependencies.
# Normally, we would still BuildRequire them to not accidentally build an uninstallable package,
# but there is a runtime dependency loop with python3-conda-libmamba-solver.
%pyproject_buildrequires %{!?with_check:-R}

%build
%pyproject_wheel

%install
%pyproject_install
%py3_shebang_fix %{buildroot}%{python3_sitelib}/conda/shell/bin/conda
%pyproject_save_files conda*

mkdir -p %{buildroot}%{_sysconfdir}/conda/condarc.d
mkdir -p %{buildroot}%{_datadir}/conda/condarc.d
cat >%{buildroot}%{_datadir}/conda/condarc.d/defaults.yaml <<EOF
pkgs_dirs:
 - /var/cache/conda/pkgs
 - ~/.conda/pkgs
EOF

mv %{buildroot}%{python3_sitelib}/tests %{buildroot}%{_datadir}/conda/
cp -rp tests/data %{buildroot}%{_datadir}/conda/tests/

mkdir -p %{buildroot}%{_localstatedir}/cache/conda/pkgs/cache

# install does not create the directory on EL7
install -m 0644 -Dt %{buildroot}/etc/profile.d/ conda/shell/etc/profile.d/conda.{sh,csh}
sed -r -i -e '1i [ -z "$CONDA_EXE" ] && CONDA_EXE=%{_bindir}/conda' \
          -e '/PATH=.*condabin/s|PATH=|[ -d $(dirname "$CONDA_EXE")/condabin ] \&\& PATH=|' %{buildroot}/etc/profile.d/conda.sh
sed -r -i -e '1i set _CONDA_EXE=%{_bindir}/conda\nset _CONDA_ROOT=' \
          -e 's/CONDA_PFX=.*/CONDA_PFX=/' %{buildroot}/etc/profile.d/conda.csh
install -m 0644 -Dt %{buildroot}%{_datadir}/fish/vendor_conf.d/ conda/shell/etc/fish/conf.d/conda.fish
sed -r -i -e '1i set -gx CONDA_EXE "/usr/bin/conda"\nset _CONDA_ROOT "/usr"\nset _CONDA_EXE "/usr/bin/conda"\nset -gx CONDA_PYTHON_EXE "/usr/bin/python3"' \
          %{buildroot}%{_datadir}/fish/vendor_conf.d/conda.fish

# Install bash completion script
install -m 0644 -Dt %{buildroot}%{bash_completionsdir}/ %SOURCE1

%check
%if 0%{?with_check}
pip3 install archspec iniconfig flask pytest-xprocess zstandard conda-package-streaming flaky pytest-timeout
export PATH=%{buildroot}%{_bindir}:$PATH
PYTHONPATH=%{buildroot}%{python3_sitelib} conda info

# Integration tests generally require network, so skip them.

# TestJson.test_list does not recognize /usr as a conda environment
# These fail on koji with PackageNotFound errors likely due to network issues
# test_cli.py::TestRun.test_run_returns_int
# test_cli.py::TestRun.test_run_returns_nonzero_errorlevel
# test_cli.py::TestRun.test_run_returns_zero_errorlevel

# test_ProgressiveFetchExtract_prefers_conda_v2_format, test_subdir_data_prefers_conda_to_tar_bz2,
# test_use_only_tar_bz2 fail in F31 koji, but not with mock --enablerepo=local. Let's disable
# them for now.
# tests/env/test_create.py::test_create_update_remote_env_file requires network access
# tests/cli/test_conda_argparse.py::test_list_through_python_api does not recognize /usr as a conda environment
# tests/cli/test_main_{clean,info,list,list_reverse,rename}.py tests require network access
# tests/cli/test_main_notices.py::test_notices_appear_once_when_running_decorated_commands needs a conda_build fixture that we remove
# tests/cli/test_main_notices.py::test_notices_cannot_read_cache_files - TypeError: '<' not supported between instances of 'MagicMock' and 'int'
# tests/cli/test_main_run.py require /usr/bin/conda to be installed
# tests/cli/test_subcommands.py tests require network access
# tests/cli/test_subcommands.py::test_rename seems to need an active environment
# tests/test_misc.py::test_explicit_missing_cache_entries requires network access
# tests/core/test_initialize.py tries to unlink /usr/bin/python3 and fails when python is a release candidate
# tests/core/test_solve.py::test_cuda_fail_1 fails on non-x86_64
# tests/core/test_solve.py libmamba - some depsolving differences - TODO
# tests/core/test_solve.py libmamba - some depsolving differences - TODO
# tests/core/test_prefix_graph.py libmamba - some depsolving differences - TODO
# tests/trust/test_signature_verification.py requires conda_content_trust - not yet packaged
#
# tests skipped for missing presence of conda_libmamba_solver
# tests/test_solvers.py::TestLibMambaSolver
# tests/base/test_context.py::test_target_prefix \
# tests/cli/test_compare.py::test_compare_success \
# tests/cli/test_compare.py::test_compare_fail \
# tests/cli/test_main_notices.py::test_target_prefix \
# tests/core/test_package_cache_data.py::test_instantiating_package_cache_when_both_tar_bz2_and_conda_exist_read_only \
# tests/core/test_solve.py::test_solve_1[libmamba] \
# tests/core/test_solve.py::test_solve_msgs_exclude_vp[libmamba] \
# tests/core/test_solve.py::test_cuda_1[libmamba] \
# tests/core/test_solve.py::test_cuda_2[libmamba] \
# tests/core/test_solve.py::test_cuda_fail_2[libmamba] \
# tests/core/test_solve.py::test_cuda_constrain_absent[libmamba] \
# tests/core/test_solve.py::test_cuda_glibc_sat[libmamba] \
# tests/core/test_solve.py::test_update_prune_1[libmamba] \
# tests/core/test_solve.py::test_update_prune_4[libmamba] \
# tests/core/test_solve.py::test_update_prune_5[libmamba] \
# tests/core/test_solve.py::test_no_deps_1[libmamba] \
# tests/core/test_solve.py::test_only_deps_1[libmamba] \
# tests/core/test_solve.py::test_only_deps_2[libmamba] \
# tests/core/test_solve.py::test_update_all_1[libmamba] \
# tests/core/test_solve.py::test_unfreeze_when_required[libmamba] \
# tests/core/test_solve.py::test_auto_update_conda[libmamba] \
# tests/core/test_solve.py::test_explicit_conda_downgrade[libmamba] \
# tests/core/test_solve.py::test_aggressive_update_packages[libmamba] \
# tests/core/test_solve.py::test_update_deps_1[libmamba] \
# tests/core/test_solve.py::test_no_update_deps_1[libmamba] \
# tests/core/test_solve.py::test_force_reinstall_1[libmamba] \
# tests/core/test_solve.py::test_force_reinstall_2[libmamba] \
# tests/core/test_solve.py::test_channel_priority_churn_minimized[libmamba] \
# tests/core/test_solve.py::test_current_repodata_usage[libmamba] \
# tests/core/test_solve.py::test_current_repodata_fallback[libmamba] \
# tests/core/test_solve.py::test_downgrade_python_prevented_with_sane_message[libmamba] \
# tests/core/test_solve.py::test_packages_in_solution_change_already_newest[libmamba] \
# tests/core/test_solve.py::test_packages_in_solution_change_needs_update[libmamba] \
# tests/core/test_solve.py::test_packages_in_solution_change_constrained[libmamba] \
# tests/core/test_solve.py::test_determine_constricting_specs_conflicts[libmamba] \
# tests/core/test_solve.py::test_determine_constricting_specs_conflicts_upperbound[libmamba] \
# tests/core/test_solve.py::test_determine_constricting_specs_multi_conflicts[libmamba] \
# tests/core/test_solve.py::test_determine_constricting_specs_no_conflicts_upperbound_compound_depends[libmamba] \
# tests/core/test_solve.py::test_determine_constricting_specs_no_conflicts_version_star[libmamba] \
# tests/core/test_solve.py::test_determine_constricting_specs_no_conflicts_free[libmamba] \
# tests/core/test_solve.py::test_determine_constricting_specs_no_conflicts_no_upperbound[libmamba] \
# tests/models/test_prefix_graph.py::test_windows_sort_orders_1[libmamba] \
# tests/models/test_prefix_graph.py::test_sort_without_prep[libmamba] \

%pytest -vv -m "not integration" \
    --deselect=tests/test_cli.py::TestJson::test_list \
    --deselect=tests/test_cli.py::test_run_returns_int \
    --deselect=tests/test_cli.py::test_run_returns_nonzero_errorlevel \
    --deselect=tests/test_cli.py::test_run_returns_zero_errorlevel \
    --deselect=tests/test_cli.py::test_run_readonly_env \
	--ignore=tests/test_create.py \
    --deselect=tests/test_misc.py::test_explicit_missing_cache_entries \
    --ignore=tests/env/specs/test_binstar.py \
    --deselect=tests/env/test_create.py::test_create_update_remote_env_file \
    --deselect='tests/cli/test_common.py::test_is_active_prefix[active_prefix-True]' \
    --deselect=tests/cli/test_config.py::test_conda_config_describe \
    --deselect=tests/cli/test_config.py::test_conda_config_validate \
    --deselect=tests/cli/test_config.py::test_conda_config_validate_sslverify_truststore \
    --deselect=tests/cli/test_conda_argparse.py::test_list_through_python_api \
    --deselect=tests/cli/test_main_clean.py \
    --deselect=tests/cli/test_main_info.py::test_info_python_output \
    --deselect=tests/cli/test_main_info.py::test_info_conda_json \
    --deselect=tests/cli/test_main_list.py::test_list \
    --deselect=tests/cli/test_main_list.py::test_list_reverse \
    --deselect=tests/cli/test_main_notices.py::test_notices_appear_once_when_running_decorated_commands \
    --deselect=tests/cli/test_main_notices.py::test_notices_cannot_read_cache_files \
    --deselect=tests/cli/test_main_remove.py::test_remove_all \
    --deselect=tests/cli/test_main_remove.py::test_remove_all_keep_env \
    --deselect=tests/cli/test_main_rename.py \
    --deselect=tests/cli/test_main_run.py \
    --deselect=tests/cli/test_subcommands.py::test_create[libmamba] \
    --deselect=tests/cli/test_subcommands.py::test_env_create \
    --deselect=tests/cli/test_subcommands.py::test_env_update \
    --deselect=tests/cli/test_subcommands.py::test_init \
    --deselect=tests/cli/test_subcommands.py::test_install \
    --deselect=tests/cli/test_subcommands.py::test_list \
    --deselect=tests/cli/test_subcommands.py::test_notices \
    --deselect=tests/cli/test_subcommands.py::test_remove_all_json[remove] \
    --deselect=tests/cli/test_subcommands.py::test_remove_all_json[uninstall] \
    --deselect=tests/cli/test_subcommands.py::test_rename \
    --deselect=tests/cli/test_subcommands.py::test_run \
    --deselect=tests/cli/test_subcommands.py::test_search \
    --deselect=tests/cli/test_subcommands.py::test_update[libmamba-update] \
    --deselect=tests/cli/test_subcommands.py::test_update[libmamba-upgrade] \
    --deselect=tests/cli/test_subcommands.py::test_update[update] \
    --deselect=tests/cli/test_subcommands.py::test_update[upgrade] \
    --deselect=tests/core/test_package_cache_data.py::test_ProgressiveFetchExtract_prefers_conda_v2_format \
    --deselect=tests/core/test_subdir_data.py::test_subdir_data_prefers_conda_to_tar_bz2 \
    --deselect=tests/core/test_subdir_data.py::test_use_only_tar_bz2 \
    --deselect=tests/core/test_initialize.py \
    --deselect=tests/core/test_solve.py::test_cuda_fail_1 \
    --deselect=tests/core/test_solve.py::test_conda_downgrade[libmamba] \
    --deselect=tests/core/test_solve.py::test_python2_update[libmamba] \
    --deselect=tests/core/test_solve.py::test_update_deps_2[libmamba] \
    --deselect=tests/core/test_solve.py::test_fast_update_with_update_modifier_not_set[libmamba] \
    --deselect=tests/core/test_solve.py::test_timestamps_1[libmamba] \
    --deselect=tests/core/test_solve.py::test_remove_with_constrained_dependencies[libmamba] \
    --deselect=tests/gateways/test_jlap.py::test_download_and_hash \
    --deselect=tests/gateways/test_jlap.py::test_jlap_fetch_ssl[True] \
    --deselect=tests/gateways/test_jlap.py::test_jlap_fetch_ssl[False] \
    --deselect=tests/test_plan.py::test_pinned_specs_conda_meta_pinned \
    --deselect=tests/test_plan.py::test_pinned_specs_condarc \
    --deselect=tests/test_plan.py::test_pinned_specs_all \
    --deselect=tests/cli/test_subcommands.py::test_compare[libmamba] \
    --deselect=tests/cli/test_subcommands.py::test_package[libmamba] \
    --deselect=tests/cli/test_subcommands.py::test_remove[libmamba-remove] \
    --deselect=tests/cli/test_subcommands.py::test_remove[libmamba-uninstall] \
    --deselect=tests/cli/test_subcommands.py::test_remove_all_json[libmamba-remove] \
    --deselect=tests/cli/test_subcommands.py::test_remove_all_json[libmamba-uninstall] \
    --deselect=tests/cli/test_subcommands.py::test_remove_all_json[classic-remove] \
    --deselect=tests/cli/test_subcommands.py::test_remove_all_json[classic-uninstall] \
    --deselect=tests/cli/test_subcommands.py::test_update[classic-update] \
    --deselect=tests/cli/test_subcommands.py::test_update[classic-upgrade] \
    --deselect=tests/cli/test_subcommands.py::test_env_remove[libmamba] \
    --deselect=tests/cli/test_subcommands.py::test_env_config_vars[libmamba] \
    --deselect=tests/core/test_subdir_data.py::test_subdir_data_coverage \
    --deselect=tests/models/test_prefix_graph.py::test_prefix_graph_1[libmamba] \
    --deselect=tests/models/test_prefix_graph.py::test_prefix_graph_2[libmamba] \
    --deselect=tests/models/test_prefix_graph.py::test_remove_youngest_descendant_nodes_with_specs[libmamba] \
    --deselect=tests/models/test_prefix_graph.py::test_deep_cyclical_dependency[libmamba] \
    --deselect=tests/plugins/test_pre_solves.py::test_pre_solve_invoked \
    --deselect=tests/plugins/test_post_solves.py::test_post_solve_action_raises_exception \
    --deselect=tests/plugins/test_post_solves.py::test_post_solve_invoked \
    --deselect=tests/plugins/subcommands/doctor/test_cli.py::test_conda_doctor_with_test_environment \
    --deselect=tests/core/test_prefix_data.py::test_get_environment_env_vars \
    --deselect=tests/core/test_prefix_data.py::test_set_unset_environment_env_vars \
    --deselect=tests/core/test_prefix_data.py::test_set_unset_environment_env_vars_no_exist \
    --ignore=tests/trust \
	--deselect=tests/test_solvers.py::TestLibMambaSolver \
	--deselect=tests/base/test_context.py::test_target_prefix \
	--deselect=tests/cli/test_compare.py::test_compare_success \
	--deselect=tests/cli/test_compare.py::test_compare_fail \
	--deselect=tests/cli/test_main_notices.py::test_target_prefix \
	--deselect=tests/core/test_package_cache_data.py::test_instantiating_package_cache_when_both_tar_bz2_and_conda_exist_read_only \
	--deselect=tests/core/test_solve.py::test_solve_1[libmamba] \
	--deselect=tests/core/test_solve.py::test_solve_msgs_exclude_vp[libmamba] \
	--deselect=tests/core/test_solve.py::test_cuda_1[libmamba] \
	--deselect=tests/core/test_solve.py::test_cuda_2[libmamba] \
	--deselect=tests/core/test_solve.py::test_cuda_fail_2[libmamba] \
	--deselect=tests/core/test_solve.py::test_cuda_constrain_absent[libmamba] \
	--deselect=tests/core/test_solve.py::test_cuda_glibc_sat[libmamba] \
	--deselect=tests/core/test_solve.py::test_update_prune_1[libmamba] \
	--deselect=tests/core/test_solve.py::test_update_prune_4[libmamba] \
	--deselect=tests/core/test_solve.py::test_update_prune_5[libmamba] \
	--deselect=tests/core/test_solve.py::test_no_deps_1[libmamba] \
	--deselect=tests/core/test_solve.py::test_only_deps_1[libmamba] \
	--deselect=tests/core/test_solve.py::test_only_deps_2[libmamba] \
	--deselect=tests/core/test_solve.py::test_update_all_1[libmamba] \
	--deselect=tests/core/test_solve.py::test_unfreeze_when_required[libmamba] \
	--deselect=tests/core/test_solve.py::test_auto_update_conda[libmamba] \
	--deselect=tests/core/test_solve.py::test_explicit_conda_downgrade[libmamba] \
	--deselect=tests/core/test_solve.py::test_aggressive_update_packages[libmamba] \
	--deselect=tests/core/test_solve.py::test_update_deps_1[libmamba] \
	--deselect=tests/core/test_solve.py::test_no_update_deps_1[libmamba] \
	--deselect=tests/core/test_solve.py::test_force_reinstall_1[libmamba] \
	--deselect=tests/core/test_solve.py::test_force_reinstall_2[libmamba] \
	--deselect=tests/core/test_solve.py::test_channel_priority_churn_minimized[libmamba] \
	--deselect=tests/core/test_solve.py::test_current_repodata_usage[libmamba] \
	--deselect=tests/core/test_solve.py::test_current_repodata_fallback[libmamba] \
	--deselect=tests/core/test_solve.py::test_downgrade_python_prevented_with_sane_message[libmamba] \
	--deselect=tests/core/test_solve.py::test_packages_in_solution_change_already_newest[libmamba] \
	--deselect=tests/core/test_solve.py::test_packages_in_solution_change_needs_update[libmamba] \
	--deselect=tests/core/test_solve.py::test_packages_in_solution_change_constrained[libmamba] \
	--deselect=tests/core/test_solve.py::test_determine_constricting_specs_conflicts[libmamba] \
	--deselect=tests/core/test_solve.py::test_determine_constricting_specs_conflicts_upperbound[libmamba] \
	--deselect=tests/core/test_solve.py::test_determine_constricting_specs_multi_conflicts[libmamba] \
	--deselect=tests/core/test_solve.py::test_determine_constricting_specs_no_conflicts_upperbound_compound_depends[libmamba] \
	--deselect=tests/core/test_solve.py::test_determine_constricting_specs_no_conflicts_version_star[libmamba] \
	--deselect=tests/core/test_solve.py::test_determine_constricting_specs_no_conflicts_free[libmamba] \
	--deselect=tests/core/test_solve.py::test_determine_constricting_specs_no_conflicts_no_upperbound[libmamba] \
	--deselect=tests/models/test_prefix_graph.py::test_windows_sort_orders_1[libmamba] \
	--deselect=tests/models/test_prefix_graph.py::test_sort_without_prep[libmamba] \
	--deselect=tests/gateways/test_subprocess.py::test_subprocess_call_with_capture_output[libmamba] \
	--deselect=tests/gateways/test_subprocess.py::test_subprocess_call_without_capture_output[libmamba] \
	--deselect=tests/gateways/test_delete.py::test_auto_remove_file[libmamba] \
	--deselect=tests/gateways/test_delete.py::test_auto_remove_file_to_trash[libmamba] \
	--deselect=tests/gateways/test_permissions.py::test_make_writable[libmamba] \
	--deselect=tests/gateways/test_permissions.py::test_recursive_file_to_trash[libmamba] \
	--deselect=tests/gateways/test_permissions.py::test_make_executable[libmamba] \
    conda tests
%endif

%files
%{_sysconfdir}/conda/
%{_bindir}/conda
%{_bindir}/conda-env
%{bash_completionsdir}/conda
# TODO - better ownership for fish/vendor_conf.d
%dir %{_datadir}/fish/vendor_conf.d
%{_datadir}/fish/vendor_conf.d/conda.fish
/etc/profile.d/conda.sh
/etc/profile.d/conda.csh

%files tests
%{_datadir}/conda/tests/

%files -n python%{python3_pkgversion}-conda -f %pyproject_files
%doc CHANGELOG.md README.md
%doc %{python3_sitelib}/conda-%{version}.dist-info/licenses/AUTHORS.md
%license %{python3_sitelib}/conda-%{version}.dist-info/licenses/LICENSE
%{_localstatedir}/cache/conda/
%dir %{_datadir}/conda/
%{_datadir}/conda/condarc.d/

%changelog
* Fri Jun 14 2024 Sam Meluch <sammeluch@microsoft.com> - 24.1.2-2
- Add pytest and pip install archspec to fix package tests

* Mon Apr 22 2024 Andrew Phelps <anphel@microsoft.com> - 24.1.2-1
- Upgrade to version 24.1.2 referencing Fedora 40 (license: MIT)

* Fri Jan 28 2022 Rachel Menge <rachelmenge@microsoft.com> - 4.11.0-1
- Update source to 4.11.0

* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 4.10.1-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Thu Apr 15 2021 Orion Poplawski <orion@nwra.com> - 4.10.1-1
- Update to 4.10.1

* Fri Apr 02 2021 Orion Poplawski <orion@nwra.com> - 4.10.0-1
- Update to 4.10.0

* Tue Jan 26 2021 Orion Poplawski <orion@nwra.com> - 4.9.2-3
- Add patch to support python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 11 2020 Orion Poplawski <orion@nwra.com> - 4.9.2-1
- Update to 4.9.2

* Tue Oct 27 2020 Orion Poplawski <orion@nwra.com> - 4.9.1-1
- Update to 4.9.1

* Sun Oct 18 2020 Orion Poplawski <orion@nwra.com> - 4.9.0-1
- Update to 4.9.0

* Mon Sep 21 2020 Orion Poplawski <orion@nwra.com> - 4.8.5-2
- Add note to description about base environment

* Mon Sep 14 2020 Orion Poplawski <orion@nwra.com> - 4.8.5-1
- Update to 4.8.5
- Install conda.fish (bz#1878306)

* Sat Aug 08 2020 Orion Poplawski <orion@nwra.com> - 4.8.4-1
- Update to 4.8.4

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.3-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.8.3-2
- Rebuilt for Python 3.9

* Sun Mar 15 2020 Orion Poplawski <orion@nwra.com> - 4.8.3-1
- Update to 4.8.3

* Tue Feb  4 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.8.2-2
- Fix import for python3.9 compatiblity (#1797691)

* Tue Jan 28 2020 Orion Poplawski <orion@nwra.com> - 4.8.2-1
- Update to 4.8.2 (#1785658)
- Obtain bash completion file from github - tartansandal/conda-bash-completion

* Mon Jan 20 2020 Orion Poplawski <orion@nwra.com> - 4.8.0-2
- Install bash completion file (bz#1791068)

* Sat Dec 14 2019 Orion Poplawski <orion@nwra.com> - 4.8.0-1
- Update to 4.8.0
- Make "conda shell.bash hook" work (bz#1737165)
- Unbundle more libraries

* Sat Sep 14 2019 Orion Poplawski <orion@nwra.com> - 4.7.12-1
- Update to 4.7.12

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.7.11-2
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Orion Poplawski <orion@nwra.com> - 4.7.11-1
- Update to 4.7.11
- Use system py-cpuinfo

* Fri Aug 16 2019 Orion Poplawski <orion@nwra.com> - 4.7.10-2
- Cleanup requires some (drop crypto, yaml; add pyOpenSSL; 
  add versions for requests and ruamel-yaml

* Sat Aug  3 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.7.10-1
- Fix 'conda shell.* hook' invocations (#1737165)

* Wed Jul 31 2019 Orion Poplawski <orion@nwra.com> - 4.7.10-1
- Update to 4.7.10

* Mon Jul 29 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.7.6-1
- Update to latest version (#1678578)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Orion Poplawski <orion@nwra.com> - 4.7.2-1
- Update to 4.7.2

* Sun Jun  9 2019 Orion Poplawski <orion@nwra.com> - 4.7.1-1
- Update to 4.7.1

* Tue Apr 16 2019 Orion Poplawski <orion@nwra.com> - 4.6.13-1
- Update to 4.6.13

* Thu Apr  4 2019 Orion Poplawski <orion@nwra.com> - 4.6.11-1
- Update to 4.6.11

* Tue Apr  2 2019 Orion Poplawski <orion@nwra.com> - 4.6.9-2
- Fix conda profile scripts
- Do not build for python2 on EPEL
- Ignore test failures on EPEL7

* Sat Mar 30 2019 Orion Poplawski <orion@nwra.com> - 4.6.9-1
- Update to 4.6.9

* Wed Feb 13 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.6.5-1
- Update to latest upstream version (#1668145)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 31 2018 Orion Poplawski <orion@nwra.com> - 4.5.12-1
- Update to 4.5.12

* Mon Dec 31 2018 Orion Poplawski <orion@nwra.com> - 4.5.11-2
- EPEL7 compatability

* Fri Sep 21 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.5.11-1
- Update to latest stable version (#1570217)
- Disable python2 subpackage on F30+

* Fri Jul 13 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.4.11-4
- Pull in python[23]-cytoolz to replace bundled toolz

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.4.11-3
- Rebuilt for Python 3.7

* Wed Apr 18 2018 Orion Poplawski <orion@nwra.com> - 4.4.11-2
- Set _CONDA_ROOT in /etc/profile.d/conda.csh
- Fix python2 requires
- Require pycosat >= 0.6.3

* Sat Apr 14 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.4.11-1
- Update to latest upstream version in the 4.4.x branch (#1544046)

* Wed Feb  7 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.4.9-1
- Update to v4.4.9 (#1542874)
- conda-activate binary rpm is retired. The new way to activate the environment
  is to say 'conda activate'. See
  https://github.com/conda/conda/releases/tag/4.4.0 for more information.

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.3.24-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.3.24-3
- Install just one version of the executables (python 2 or 3)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.3.24-2
- Add all licenses to the License tag
- Add Provides: bundled(...) for all the "vendored" dependencies
- Update descriptions and simplify the spec file a bit
- Move condarc.d directory under /usr/share/conda

* Thu Aug  3 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.3.24-1
- Update to latest version
- Switch /usr/bin/conda to python3

* Thu Jul 21 2016 Orion Poplawski <orion@cora.nwra.com> - 4.1.6-1
- Update to 4.1.6

* Thu Dec 31 2015 Orion Poplawski <orion@cora.nwra.com> - 3.19.0-1
- Update to 3.19.0

* Thu Dec 31 2015 Orion Poplawski <orion@cora.nwra.com> - 3.18.8-2
- Add python 3 version

* Mon Dec 7 2015 Orion Poplawski <orion@cora.nwra.com> - 3.18.8-1
- Update to 3.18.8

* Thu Sep 24 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-6
- Do not create broken symlinks if activate/deactivate are not installed
- Do not create /usr/conda-meta to prevent accidental installs into system

* Thu Sep 24 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-5
- Non-bootstrap build

* Wed Sep 23 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-4
- Add patch to support rootless mode
- Require python-crypto
- Create /usr/conda-meta, /usr/.condarc, /var/cache/conda

* Tue Sep 22 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-3
- Require python-requests, python-yaml

* Tue Sep 22 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-2
- Add patch to allow overriding pkgs_dirs in .condarc

* Mon Sep 21 2015 Orion Poplawski <orion@cora.nwra.com> - 3.17.0-1
- Initial package
