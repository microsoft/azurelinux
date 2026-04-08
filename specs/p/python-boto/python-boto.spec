# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        A simple, lightweight interface to Amazon Web Services
Name:           python-boto
Version:        2.49.0
Release:        29%{?dist}
License:        MIT
URL:            https://github.com/boto/boto
Source0:        https://pypi.io/packages/source/b/boto/boto-%{version}.tar.gz
# Taken from sourcecode 2014-07-31
Source1:        boto-mit-license.txt

# Unbundle python-six
# https://github.com/boto/boto/pull/3086
Patch1:         boto-2.39.0-devendor.patch

# Add NAT gateway support
# https://github.com/boto/boto/pull/3472
Patch2:         boto-2.40.0-nat-gateway.patch

# Fix max_retry_delay config option
# https://github.com/boto/boto/pull/3506
# https://github.com/boto/boto/pull/3508
Patch4:         boto-2.40.0-retry-float.patch

# Add aws-exec-read to S3's canned ACL list
# https://github.com/boto/boto/pull/3332
Patch5:         boto-2.40.0-aws-exec-read.patch

# Add new instance attributes
# https://github.com/boto/boto/pull/3077
# https://github.com/boto/boto/pull/3131
Patch6:         boto-2.40.0-instance-attributes.patch

# Fix multi-VPC hosted zone parsing
# https://github.com/boto/boto/pull/2882
Patch7:         boto-2.40.0-multi-vpc-zone.patch

# Fix request logging for S3 requests
# https://github.com/boto/boto/issues/2722
# https://github.com/boto/boto/pull/2875
Patch8:         boto-2.40.0-s3-requestlog.patch

# Allow route53 health check resource paths to be none
# https://github.com/boto/boto/pull/2866
Patch9:         boto-2.40.0-route53-no-resourcepath.patch

# Add ModifySubnetAttribute support
# https://github.com/boto/boto/pull/3111
Patch10:        boto-2.45.0-modifysubnetattribute.patch

# tests: remove direct usages of mock in favor compat module
# https://fedoraproject.org/wiki/Changes/RemovePythonMockUsage
# https://github.com/boto/boto/pull/3952
Patch11:        remove-python-mock.patch

BuildRequires:  python3-devel
BuildRequires:  python3-six
# boto/plugin.py and boto/pyami/launch_ami.py uses imp
BuildRequires:  (python3-zombie-imp if python3 >= 3.12)
# test requires, but tests are commented out
# BuildRequires:  python3-httpretty
# BuildRequires:  python3-mock
# BuildRequires:  python3-nose
# BuildRequires:  python3-requests

BuildArch:      noarch


%description
Boto is a Python package that provides interfaces to Amazon Web Services.
It supports over thirty services, such as S3 (Simple Storage Service),
SQS (Simple Queue Service), and EC2 (Elastic Compute Cloud) via their
REST and Query APIs.  The goal of boto is to support the full breadth
and depth of Amazon Web Services.  In addition, boto provides support
for other public services such as Google Storage in addition to private
cloud systems like Eucalyptus, OpenStack and Open Nebula.


%package -n python3-boto
Summary:        A simple, lightweight interface to Amazon Web Services

Requires:       python3-requests
Requires:       python3-six
Requires:       python3-rsa
Requires:       (python3-zombie-imp if python3 >= 3.12)


%description -n python3-boto
Boto is a Python package that provides interfaces to Amazon Web Services.
It supports over thirty services, such as S3 (Simple Storage Service),
SQS (Simple Queue Service), and EC2 (Elastic Compute Cloud) via their
REST and Query APIs.  The goal of boto is to support the full breadth
and depth of Amazon Web Services.  In addition, boto provides support
for other public services such as Google Storage in addition to private
cloud systems like Eucalyptus, OpenStack and Open Nebula.


%prep
%autosetup -p1 -n boto-%{version}

#rm -r boto/vendored

cp -p %{SOURCE1} .


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%install
%pyproject_install
rm -f $RPM_BUILD_ROOT/%{_bindir}/*


%check
#%{__python3} tests/test.py default
%py3_check_import boto


%files -n python3-boto
%license boto-mit-license.txt
%{python3_sitelib}/boto*


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.49.0-29
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.49.0-28
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.49.0-26
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 11 2024 Miro Hrončok <mhroncok@redhat.com> - 2.49.0-24
- Remove unused test BuildRequires
- https://fedoraproject.org/wiki/Changes/DeprecateNose
- Run a very basic import check during the build

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.49.0-22
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Maxwell G <maxwell@gtmx.me> - 2.49.0-19
- Remove python3-mock dependency

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Miro Hrončok <mhroncok@redhat.com> - 2.49.0-17
- Require python3-zombie-imp on runtime

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.49.0-16
- Rebuilt for Python 3.12

* Fri Mar 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.49.0-15
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 2.49.0-12
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.49.0-9
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 2.49.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.49.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 24 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.49.0-3
- Disable tests.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.49.0-2
- Rebuilt for Python 3.8

* Tue Aug 13 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.49.0-1
- 2.49.0

* Tue Aug 13 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.45.0-13
- Drop python 2.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.45.0-9
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.45.0-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 01 2017 Troy Dawson <tdawson@redhat.com> - 2.45.0-6
- Update spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.45.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Garrett Holmstrom <gholms@fedoraproject.org> - 2.45.0-3
- Added support for ModifySubnetAttribute

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.45.0-2
- Rebuild for Python 3.6

* Thu Dec 15 2016 Jon Ciesla <limburgher@gmail.com> - 2.45.0-1
- 2.40.0.

* Fri Dec  9 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.44.0-1
- Updated to 2.44.0 (RH #1403362)

* Tue Oct 25 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.43.0-1
- Updated to 2.43.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul  5 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.41.0-1
- Updated to 2.41.0

* Tue Jun 21 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.40.0-2
- Cleaned up spec file
- Added NAT gateway support
- Fixed sigv4 protocol selection
- Fixed max_retry_delay config option
- Added aws-exec-read to S3's canned ACL list
- Added new instance attributes
- Fixed multi-VPC hosted zone parsing
- Fixed request logging for S3 requests
- Allowed route53 health check resource paths to be none

* Mon May 23 2016 Jon Ciesla <limburgher@gmail.com> - 2.40.0-1
- 2.40.0.
- Kinesis patch upstreamed.

* Fri Jan 29 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.39.0-1
- Updated to 2.39.0 (RH #1300424)
- Switched to systemwide copy of python-six on el7
- Enabled unit tests on el7
- Renamed python-boto to python2-boto to comply with current python
  packaging standards

* Mon Nov 30 2015 Ryan S. Brown <sb@ryansb.com> - 2.38.0-5
- Add patch for unittest failure https://github.com/boto/boto/pull/3412

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  9 2015 Garrett Holmstrom <gholms@fedoraproject.org> - 2.38.0-2
- Fixed ImportErrors on RHEL 7 (RH #1229863)

* Fri Apr 10 2015 Garrett Holmstrom <gholms@fedoraproject.org> - 2.38.0-1
- Updated to 2.38.0
- Added BuildRequires for python-six
- Made sample executables doc files in F23

* Wed Apr  8 2015 Garrett Holmstrom <gholms@fedoraproject.org> - 2.37.0-1
- Updated to 2.37.0 (RH #1180861)
- Dropped executables in F23
- Unbundled python-six (boto #3086)
- Enabled unit tests on Fedora (RH #1072946)

* Sun Nov  9 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.34.0-4
- Fixed python3 requires

* Fri Nov  7 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.34.0-3
- Re-fix executables (RH #1152444)

* Fri Nov  7 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.34.0-2
- Added missing python-requests and python-rsa dependencies
- Disabled unit tests due to rawhide/F21 python regression (RH #1161166:c4)

* Fri Nov  7 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.34.0-1
- Updated to 2.34.0 (RH #1072925, RH #1072928, RH #1161229)
- Made executables point to python2 (RH #1152444)
- Enabled unit tests on Fedora (RH #1072946)

* Thu Aug 21 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.32.1-1
- Updated to 2.32.1 (RH #1126056, RH #1132348)
- Added python3-boto (RH #1024363)
- Added (but did not enable) unit tests (RH #1072946, RH #1072923)

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 2.27.0-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 21 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.27.0-1
- Updated to 2.27.0

* Wed Feb 12 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.25.0-2
- Fixed roboto parameter type conversion (boto #2094, RH #1064550)

* Mon Feb 10 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.25.0-1
- Updated to 2.25.0
- This update makes s3.get_bucket use HEAD instead of GET

* Mon Jan 20 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.23.0-1
- Updated to 2.23.0
- Fixed auth for anonymous S3 requests (boto #1988)

* Thu Sep 26 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.13.3-1
- Updated to 2.13.3
- Note that this version changes register_image's virtualization_type parameter
- Fixed auto-scaling PropagateAtLaunch parsing (#1011682)

* Mon Jul 29 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.9.9-2
- Re-fixed autoscaling policy parsing (boto #1538)

* Thu Jul 25 2013 Orion Poplawski <orion@cora.nwra.com> - 2.9.9-1
- Update to 2.9.9

* Fri Jun 21 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.9.6-2
- Rebuilt after merge

* Fri Jun 21 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.9.6-1
- Updated to 2.9.6
- Fixed autoscaling policy parsing (boto #1538)

* Thu May  9 2013 Orion Poplawski <orion@cora.nwra.com> - 2.9.2-1
- Update to 2.9.2 (bug #948714)
- Spec cleanup

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.5.2-3
- Fixed parsing of current/previous instance state data (boto #881)

* Wed Nov 21 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 2.6.0-2
- Updated to 2.6.0 (#876517)
- Note that this version enables SSL cert verification by default.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 2.5.2-1
- Updated to 2.5.2
- Fixed failure when metadata is empty (#838076)

* Thu Jun 14 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 2.5.1-1
- Updated to 2.5.1 (last-minute upstream bugfix)

* Wed Jun 13 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 2.5.0-1
- Updated to 2.5.0 (#828912)

* Wed Mar 21 2012 Robert Scheck <robert@fedoraproject.org> 2.3.0-1
- Upgrade to 2.3.0 (#786301 #c10)

* Tue Mar 13 2012 Robert Scheck <robert@fedoraproject.org> 2.2.2-1
- Upgrade to 2.2.2 (#786301, thanks to Bobby Powers)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 15 2011 Robert Scheck <robert@fedoraproject.org> 2.0-1
- Upgrade to 2.0 (#723088)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9b-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Robert Scheck <robert@fedoraproject.org> 1.9b-6
- Added a patch for python 2.4 support (#656446, #661233)

* Thu Dec 02 2010 Lubomir Rintel <lubo.rintel@gooddata.com> 1.9b-5
- Apply a patch for python 2.7 support (#659248)

* Thu Nov 18 2010 Robert Scheck <robert@fedoraproject.org> 1.9b-4
- Added patch to fix parameter of build_list_params() (#647005)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.9b-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Feb 09 2010 Robert Scheck <robert@fedoraproject.org> 1.9b-2
- Backported upstream patch for image registration (#561216)

* Sat Jan 09 2010 Robert Scheck <robert@fedoraproject.org> 1.9b-1
- Upgrade to 1.9b

* Fri Jul 24 2009 Robert Scheck <robert@fedoraproject.org> 1.8d-1
- Upgrade to 1.8d (#513560)

* Wed Jun 03 2009 Luke Macken <lmacken@redhat.com> 1.7a-2
- Add python-setuptools-devel to our build requirements, for egg-info

* Thu Apr 16 2009 Robert Scheck <robert@fedoraproject.org> 1.7a-1
- Upgrade to 1.7a

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1.5c-2
- Rebuild against rpm 4.6

* Sun Dec 07 2008 Robert Scheck <robert@fedoraproject.org> 1.5c-1
- Upgrade to 1.5c

* Fri Dec 05 2008 Jeremy Katz <katzj@redhat.com> 1.2a-2
- Rebuild for python 2.6

* Wed May 07 2008 Robert Scheck <robert@fedoraproject.org> 1.2a-1
- Upgrade to 1.2a

* Sat Feb 09 2008 Robert Scheck <robert@fedoraproject.org> 1.0a-1
- Upgrade to 1.0a

* Sat Dec 08 2007 Robert Scheck <robert@fedoraproject.org> 0.9d-1
- Upgrade to 0.9d

* Thu Aug 30 2007 Robert Scheck <robert@fedoraproject.org> 0.9b-1
- Upgrade to 0.9b
- Initial spec file for Fedora and Red Hat Enterprise Linux
