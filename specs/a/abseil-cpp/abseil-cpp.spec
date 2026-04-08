## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Installed library version
%global lib_version 2508.0.0

Name:           abseil-cpp
Version:        20250814.1
Release:        %autorelease
Summary:        C++ Common Libraries

# The entire source is Apache-2.0, except:
#   - The following files are LicenseRef-Fedora-Public-Domain:
#       absl/time/internal/cctz/src/tzfile.h
#         ** This file is in the public domain, so clarified as of
#         ** 1996-06-05 by Arthur David Olson.
#       absl/time/internal/cctz/testdata/zoneinfo/iso3166.tab
#         # This file is in the public domain, so clarified as of
#         # 2009-05-17 by Arthur David Olson.
#       absl/time/internal/cctz/testdata/zoneinfo/zone1970.tab
#         # This file is in the public domain.
#     Public-domain license text for these files was added to the
#     public-domain-text.txt file in fedora-license-data in commit
#     538bc87d5e3c1cb08e81d690ce4122e1273dc9cd
#     (https://gitlab.com/fedora/legal/fedora-license-data/-/merge_requests/205).
License:        Apache-2.0 AND LicenseRef-Fedora-Public-Domain
URL:            https://abseil.io
Source:         https://github.com/abseil/abseil-cpp/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
# The default make backend would work just as well; ninja is observably faster
BuildRequires:  ninja-build
BuildRequires:  gcc-c++

BuildRequires:  gmock-devel
BuildRequires:  gtest-devel

# The contents of absl/time/internal/cctz are derived from
# https://github.com/google/cctz (https://src.fedoraproject.org/rpms/cctz), but
# have been forked with Abseil-specific changes. It is not obvious from which
# particular version of CCTZ these sources are derived. Upstream was asked
# about a path to supporting a system copy as required by bundling guidelines:
#   Please comment on CCTZ bundling
#   https://github.com/abseil/abseil-cpp/discussions/1415
# They refused, for the time being, as follows:
#   “[…] we have no plans to change this decision, but we reserve the right to
#   change our minds.”
Provides:       bundled(cctz)

%ifarch s390x
# Symbolize.SymbolizeWithMultipleMaps fails in absl_symbolize_test on s390x
# with LTO
# https://github.com/abseil/abseil-cpp/issues/1133
%global _lto_cflags %{nil}
%endif

%description
Abseil is an open-source collection of C++ library code designed to augment
the C++ standard library. The Abseil library code is collected from
Google's own C++ code base, has been extensively tested and used in
production, and is the same code we depend on in our daily coding lives.

In some cases, Abseil provides pieces missing from the C++ standard; in
others, Abseil provides alternatives to the standard for special needs we've
found through usage in the Google code base. We denote those cases clearly
within the library code we provide you.

Abseil is not meant to be a competitor to the standard library; we've just
found that many of these utilities serve a purpose within our code base,
and we now want to provide those resources to the C++ community as a whole.

%package testing
Summary:        Libraries needed for running tests on the installed %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

Provides:       bundled(cctz)

%description testing
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-testing%{?_isa} = %{version}-%{release}

# Some of the headers from CCTZ are part of the -devel subpackage. See the
# corresponding virtual Provides in the base package for full details.
Provides:       bundled(cctz)

%description devel
Development headers for %{name}

%prep
%autosetup -p1 -S gendiff

%build
# ABSL_BUILD_TEST_HELPERS is needed to build libraries for the -testing
# subpackage when tests are not enabled. It is therefore redundant here, but we
# still supply it to be more explicit.
%cmake \
  -GNinja \
  -DABSL_USE_EXTERNAL_GOOGLETEST:BOOL=ON \
  -DABSL_FIND_GOOGLETEST:BOOL=ON \
  -DABSL_ENABLE_INSTALL:BOOL=ON \
  -DABSL_BUILD_TESTING:BOOL=ON \
  -DABSL_BUILD_TEST_HELPERS:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING=None \
  -DCMAKE_CXX_STANDARD:STRING=17
%cmake_build


%install
%cmake_install

%check
skips='^($.'
%ifarch ppc64le
# [Bug]: Flaky test failures in absl_failure_signal_handler_test on ppc64le in
# Fedora
# https://github.com/abseil/abseil-cpp/issues/1804
skips="${skips}|absl_failure_signal_handler_test"
# [Bug]: StackTrace.NestedSignal in absl_stacktrace_test fails on ppc64le since
# 20250184.0
# https://github.com/abseil/abseil-cpp/issues/1925
skips="${skips}|absl_stacktrace_test"
%endif
skips="${skips})$"

%ctest --exclude-regex "${skips}"

%files
%license LICENSE
%doc FAQ.md README.md UPGRADES.md
# All shared libraries except installed TESTONLY libraries; see the %%files
# list for the -testing subpackage for those.
%{_libdir}/libabsl_base.so.%{lib_version}
%{_libdir}/libabsl_city.so.%{lib_version}
%{_libdir}/libabsl_civil_time.so.%{lib_version}
%{_libdir}/libabsl_cord.so.%{lib_version}
%{_libdir}/libabsl_cord_internal.so.%{lib_version}
%{_libdir}/libabsl_cordz_functions.so.%{lib_version}
%{_libdir}/libabsl_cordz_handle.so.%{lib_version}
%{_libdir}/libabsl_cordz_info.so.%{lib_version}
%{_libdir}/libabsl_cordz_sample_token.so.%{lib_version}
%{_libdir}/libabsl_crc32c.so.%{lib_version}
%{_libdir}/libabsl_crc_cord_state.so.%{lib_version}
%{_libdir}/libabsl_crc_cpu_detect.so.%{lib_version}
%{_libdir}/libabsl_crc_internal.so.%{lib_version}
%{_libdir}/libabsl_debugging_internal.so.%{lib_version}
%{_libdir}/libabsl_decode_rust_punycode.so.%{lib_version}
%{_libdir}/libabsl_demangle_internal.so.%{lib_version}
%{_libdir}/libabsl_demangle_rust.so.%{lib_version}
%{_libdir}/libabsl_die_if_null.so.%{lib_version}
%{_libdir}/libabsl_examine_stack.so.%{lib_version}
%{_libdir}/libabsl_exponential_biased.so.%{lib_version}
%{_libdir}/libabsl_failure_signal_handler.so.%{lib_version}
%{_libdir}/libabsl_flags_commandlineflag.so.%{lib_version}
%{_libdir}/libabsl_flags_commandlineflag_internal.so.%{lib_version}
%{_libdir}/libabsl_flags_config.so.%{lib_version}
%{_libdir}/libabsl_flags_internal.so.%{lib_version}
%{_libdir}/libabsl_flags_marshalling.so.%{lib_version}
%{_libdir}/libabsl_flags_parse.so.%{lib_version}
%{_libdir}/libabsl_flags_private_handle_accessor.so.%{lib_version}
%{_libdir}/libabsl_flags_program_name.so.%{lib_version}
%{_libdir}/libabsl_flags_reflection.so.%{lib_version}
%{_libdir}/libabsl_flags_usage.so.%{lib_version}
%{_libdir}/libabsl_flags_usage_internal.so.%{lib_version}
%{_libdir}/libabsl_graphcycles_internal.so.%{lib_version}
%{_libdir}/libabsl_hash.so.%{lib_version}
%{_libdir}/libabsl_hashtablez_sampler.so.%{lib_version}
%{_libdir}/libabsl_hashtable_profiler.so.%{lib_version}
%{_libdir}/libabsl_int128.so.%{lib_version}
%{_libdir}/libabsl_kernel_timeout_internal.so.%{lib_version}
%{_libdir}/libabsl_leak_check.so.%{lib_version}
%{_libdir}/libabsl_log_entry.so.%{lib_version}
%{_libdir}/libabsl_log_flags.so.%{lib_version}
%{_libdir}/libabsl_log_globals.so.%{lib_version}
%{_libdir}/libabsl_log_initialize.so.%{lib_version}
%{_libdir}/libabsl_log_internal_check_op.so.%{lib_version}
%{_libdir}/libabsl_log_internal_conditions.so.%{lib_version}
%{_libdir}/libabsl_log_internal_fnmatch.so.%{lib_version}
%{_libdir}/libabsl_log_internal_format.so.%{lib_version}
%{_libdir}/libabsl_log_internal_globals.so.%{lib_version}
%{_libdir}/libabsl_log_internal_log_sink_set.so.%{lib_version}
%{_libdir}/libabsl_log_internal_message.so.%{lib_version}
%{_libdir}/libabsl_log_internal_nullguard.so.%{lib_version}
%{_libdir}/libabsl_log_internal_proto.so.%{lib_version}
%{_libdir}/libabsl_log_internal_structured_proto.so.%{lib_version}
%{_libdir}/libabsl_log_severity.so.%{lib_version}
%{_libdir}/libabsl_log_sink.so.%{lib_version}
%{_libdir}/libabsl_malloc_internal.so.%{lib_version}
%{_libdir}/libabsl_periodic_sampler.so.%{lib_version}
%{_libdir}/libabsl_poison.so.%{lib_version}
%{_libdir}/libabsl_profile_builder.so.%{lib_version}
%{_libdir}/libabsl_random_distributions.so.%{lib_version}
%{_libdir}/libabsl_random_internal_distribution_test_util.so.%{lib_version}
%{_libdir}/libabsl_random_internal_entropy_pool.so.%{lib_version}
%{_libdir}/libabsl_random_internal_platform.so.%{lib_version}
%{_libdir}/libabsl_random_internal_randen.so.%{lib_version}
%{_libdir}/libabsl_random_internal_randen_hwaes.so.%{lib_version}
%{_libdir}/libabsl_random_internal_randen_hwaes_impl.so.%{lib_version}
%{_libdir}/libabsl_random_internal_randen_slow.so.%{lib_version}
%{_libdir}/libabsl_random_internal_seed_material.so.%{lib_version}
%{_libdir}/libabsl_random_seed_gen_exception.so.%{lib_version}
%{_libdir}/libabsl_random_seed_sequences.so.%{lib_version}
%{_libdir}/libabsl_raw_hash_set.so.%{lib_version}
%{_libdir}/libabsl_raw_logging_internal.so.%{lib_version}
%{_libdir}/libabsl_scoped_set_env.so.%{lib_version}
%{_libdir}/libabsl_spinlock_wait.so.%{lib_version}
%{_libdir}/libabsl_stacktrace.so.%{lib_version}
%{_libdir}/libabsl_status.so.%{lib_version}
%{_libdir}/libabsl_statusor.so.%{lib_version}
%{_libdir}/libabsl_str_format_internal.so.%{lib_version}
%{_libdir}/libabsl_strerror.so.%{lib_version}
%{_libdir}/libabsl_strings.so.%{lib_version}
%{_libdir}/libabsl_strings_internal.so.%{lib_version}
%{_libdir}/libabsl_string_view.so.%{lib_version}
%{_libdir}/libabsl_symbolize.so.%{lib_version}
%{_libdir}/libabsl_synchronization.so.%{lib_version}
%{_libdir}/libabsl_throw_delegate.so.%{lib_version}
%{_libdir}/libabsl_time.so.%{lib_version}
%{_libdir}/libabsl_time_zone.so.%{lib_version}
%{_libdir}/libabsl_tracing_internal.so.%{lib_version}
%{_libdir}/libabsl_utf8_for_code_point.so.%{lib_version}
%{_libdir}/libabsl_vlog_config_internal.so.%{lib_version}

%files testing
# TESTONLY libraries (that are actually installed):
# absl/base/CMakeLists.txt
%{_libdir}/libabsl_exception_safety_testing.so.%{lib_version}
%{_libdir}/libabsl_atomic_hook_test_helper.so.%{lib_version}
%{_libdir}/libabsl_spinlock_test_common.so.%{lib_version}
# absl/container/CMakeLists.txt
%{_libdir}/libabsl_test_instance_tracker.so.%{lib_version}
%{_libdir}/libabsl_hash_generator_testing.so.%{lib_version}
# absl/debugging/CMakeLists.txt
%{_libdir}/libabsl_stack_consumption.so.%{lib_version}
# absl/log/CMakeLists.txt
%{_libdir}/libabsl_log_internal_test_actions.so.%{lib_version}
%{_libdir}/libabsl_log_internal_test_helpers.so.%{lib_version}
%{_libdir}/libabsl_log_internal_test_matchers.so.%{lib_version}
%{_libdir}/libabsl_scoped_mock_log.so.%{lib_version}
# absl/status/CMakeLists.txt
%{_libdir}/libabsl_status_matchers.so.%{lib_version}
# absl/strings/CMakeLists.txt
%{_libdir}/libabsl_pow10_helper.so.%{lib_version}
# absl/synchronization/CMakeLists.txt
%{_libdir}/libabsl_per_thread_sem_test_common.so.%{lib_version}
# absl/time/CMakeLists.txt
%{_libdir}/libabsl_time_internal_test_util.so.%{lib_version}

%files devel
%{_includedir}/absl
%{_libdir}/libabsl_*.so
%{_libdir}/cmake/absl
%{_libdir}/pkgconfig/absl_*.pc

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 20250814.1-2
- Latest state for abseil-cpp

* Tue Sep 23 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250814.1-1
- Update to 20250814.1 (close RHBZ#2397466)

* Fri Aug 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250814.0-1
- Update to 20250814.0 (close RHBZ#2389295)

* Fri Aug 15 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250512.1-1
- Update to 20250512.1 (close RHBZ#2388710)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20250512.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu May 15 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250512.0-1
- Update to 20250512.0 (close RHBZ#2366373)

* Wed Mar 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250127.1-1
- Update to 20250127.1 (close RHBZ#2353223)

* Tue Feb 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20250127.0-1
- Update to 20250127.0 (close RHBZ#2343779)

* Fri Jan 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20240722.1-1
- Update to 20240722.1 (close RHBZ#2341808)

* Wed Jan 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20240722.0-5
- Rebuilt for gtest 1.15.2

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20240722.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20240722.0-3
- Patch for GCC 15 (fix RHBZ#2336266)

* Wed Jan 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 20240722.0-2
- Report and skip a test regression on ppc64le

* Sat Aug 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20240722.0-1
- Update to 20240722.0 (close RHBZ#2302537)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240116.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20240116.2-3
- Rebuilt with upstream patch for NegativeNaN test failure on riscv64

* Wed May 29 2024 David Abdurachmanov <davidlt@rivosinc.com> - 20240116.2-2
- Disable NegativeNaN test on riscv64

* Tue Apr 09 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20240116.2-1
- Update to 20240116.2 (close RHBZ#2274172)

* Wed Jan 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20240116.0-1
- Update to 20240116.0

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230802.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230802.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 31 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20230802.1-2
- Rebuild for gtest 1.14.0

* Wed Sep 20 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20230802.1-1
- Update to 20230802.1 (close RHBZ#2239814)

* Thu Aug 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20230802.0-1
- Update to 20230802.0 (Abseil LTS branch, Aug 2023): close RHBZ#2229015

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20230125.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 09 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20230125.3-1
- Update to 20230125.3 (close RHBZ#2193306)
- Split installed TESTONLY libraries into a -testing subpackage; explicitly
  list all installed shared libraries
- Explicitly enable the ABSL_BUILD_TEST_HELPERS CMake option

* Thu Mar 30 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20230125.2-1
- Update to 20230125.2 (close RHBZ#2182229)

* Thu Feb 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20230125.1-1
- Update to 20230125.1 (close RHBZ#2162638)

* Sat Jan 21 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 20220623.1-4
- Backport upstream commit 4eef161 for GCC 13

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20220623.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 02 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20220623.1-2
- Update to 20220623.1 (close RHBZ#2123181)

* Sat Aug 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20220623.0-1
- Update to 20220623.0 (close RHBZ#2101021)
- Update License to SPDX

* Fri Jul 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20211102.0-4
- Do not leak -maes -msse4.1 into pkgconfig (fix RHBZ#2108658)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211102.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20211102.0-2
- Disable LTO on s390x to work around test failure
- Skip SysinfoTest.NominalCPUFrequency on all architectures; it fails
  occasionally on aarch64, and upstream says we should not care

* Fri Feb 18 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20211102.0-1
- Update to 20211102.0 (close RHBZ#2019691)
- Drop --output-on-failure, already in %%ctest expansion
- On s390x, instead of ignoring all tests, skip only the single failing test
- Use ninja backend for CMake: speeds up build with no downsides
- Drop patch for armv7hl

* Mon Jan 31 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20210324.2-4
- Fix test failure (fix RHBZ#2045186)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210324.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210324.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Rich Mattes <richmattes@gmail.com> - 20210324.1-2
- Update to release 20210324.2
- Enable and run test suite

* Mon Mar 08 2021 Rich Mattes <richmattes@gmail.com> - 20200923.3-1
- Update to release 20200923.3

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200923.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 19 2020 Rich Mattes <richmattes@gmail.com> - 20200923.2-1
- Update to release 20200923.2
- Rebuild to fix tagging in koji (rhbz#1885561)

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200225.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200225.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 27 2020 Rich Mattes <richmattes@gmail.com> - 20200225.2-2
- Don't remove buildroot in install

* Sun May 24 2020 Rich Mattes <richmattes@gmail.com> - 20200225.2-1
- Initial package.

## END: Generated by rpmautospec
