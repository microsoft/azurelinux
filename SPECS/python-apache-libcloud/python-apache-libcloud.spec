#
# spec file for package python-apache-libcloud
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%global _description \
Apache Libcloud is a standard Python library that abstracts away \
differences among multiple cloud provider APIs.
%global pypi_name apache-libcloud
Summary:        Abstraction over multiple cloud provider APIs
Name:           python-apache-libcloud
Version:        3.5.1
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://libcloud.apache.org
Source0:        https://github.com/apache/libcloud/archive/refs/tags/v%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
Patch1:         gce_image_projects.patch
Patch2:         ec2_create_node.patch
# PATCH-FIX-UPSTREAM https://github.com/Kami/libcloud/commit/e62bb28cdbd685203d44a9a4028f311ea155476c Use unittest.mock library from stdlib instead of using 3rd party mock dependency.
Patch3:         mock.patch
BuildRequires:  fdupes
BuildRequires:  libvirt-python3
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-lockfile
BuildRequires:  python3-lxml
BuildRequires:  python3-paramiko
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-requests-mock
BuildRequires:  python3-setuptools
Requires:       python3-lxml
Requires:       python3-requests
BuildArch:      noarch
%if %{with_check}
BuildRequires:  openssh-clients
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif

%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -p1 -n libcloud-%{version}
sed -i '/^#!/d' demos/gce_demo.py
chmod a-x demos/gce_demo.py
# Setup tests
cp libcloud/test/secrets.py-dist libcloud/test/secrets.py

%build
%py3_build

%install
%py3_install
find %{buildroot} -name '*.DS_Store' -delete
find %{buildroot} -name '*.json' -size 0 -delete
find %{buildroot} -name '*.pem' -size 0 -delete
rm -r %{buildroot}%{python3_sitelib}/libcloud/test
%fdupes %{buildroot}%{python3_sitelib}

%check
%{python3} -m pip install atomicwrites attrs pluggy pygments six more-itertools
# Skip OvhTests::test_list_nodes_invalid_region which tries to reach OVH servers
# Skip ShellOutSSHClientTests tests which attempt to ssh to localhost
# Skip test_key_file_non_pem_format_error since OpenSSH support is backported for SLE python-paramiko < 2.7.0
%pytest -k '(not test_consume_stderr_chunk_contains_part_of_multi_byte_utf8_character and not test_consume_stdout_chunk_contains_part_of_multi_byte_utf8_character and not test_consume_stdout_chunk_contains_non_utf8_character and not test_consume_stderr_chunk_contains_non_utf8_character and not ElasticContainerDriverTestCase and not test_connection_timeout_raised and not test_retry_on_all_default_retry_exception_classes)'

%files -n python3-%{pypi_name}
%license LICENSE
%doc CHANGES.rst README.rst demos/ example_*.py
%{python3_sitelib}/*

%changelog
* Thu Jul 07 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.5.1-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag)
- Adding as run dependency for package cassandra medusa.
- License verified

* Fri May 13 2022 Markéta Machová <mmachova@suse.com>
- update to 3.5.1
  * Support for Python 3.5 which has been EOL for more than a year now has been removed.
  * [EC2] Add support for new ap-east-1 region.
  * [OpenStack] OpenStack: Move floating IP functions to use network service instead of nova.
  * [OpenStack] Avoid raising exception if ip is not found.
  * [GCE] Allow credentials argument which is provided to the driver constructor.
  * [Local Storage] Objects returned by the list_container_objects() method are now returned sorted in the ascending order based on the object name.
  * Also run unit tests under Python 3.10 + Pyjion on CI/CD.
- added upstream patch mock.patch and drop mock requirement
- rebase all other patches

* Thu Dec  9 2021 pgajdos@suse.com
- pytest-runner is not required for build

* Mon Nov 15 2021 Andreas Stieger <andreas.stieger@gmx.de>
- update to 3.4.1:
  * fix a regresion preventing installation under Python 3.5
  * revert requests minimum version required

* Sun Nov 14 2021 Andreas Stieger <andreas.stieger@gmx.de>
- update to 3.4.0:
  * Improvements and more flexibility in the failed HTTP requests
    retrying code
  * Various improvements to the Equinix Metal compute driver
  * Improvements and updates to the Outscale, Vultr, CloudSigma and
    OpenStack compute drivers
  * Support for authenticating via API tokens to the CloudFlare DNS
    driver
  * Support for using external cache for OpenStack auth tokens
- add upstream signing key and validate source signature

* Mon Feb  1 2021 Pablo Suárez Hernández <pablo.suarezhernandez@suse.com>
- Skip "OvhTests::test_list_nodes_invalid_region" compute test when building
  RPM package since this tests requires internet connection.

* Fri Jan 29 2021 Pablo Suárez Hernández <pablo.suarezhernandez@suse.com>
- Update to 3.3.1:
  * Compute
    + [EC2] Fix a regression introduced in v3.3.0 which would break EC2 driver for some regions because the driver would incorrectly try to use signature version 2 for all the regions whereas some newer regions require signature version 4 to be used.
    If you are unable to upgrade, you can use the following workaround, as long as you only use code which supports / works with authentication signature algorithm version 4:
    import libcloud.common.aws
    libcloud.common.aws.DEFAULT_SIGNATURE_VERSION = "4"
    [#] Instantiate affected driver here...
    Reported by @olegrtecno. (GITHUB-1545, GITHUB-1546)
    + [EC2] Allow user to override which signature algorithm version is used for authentication by passing signature_version keyword argument to the EC2 driver constructor. (GITHUB-1546)
  * Storage
    + [Google Cloud Storage] Fix a bug and make sure we also correctly handle scenario in get_object() method when the object size is returned in x-goog-stored-content-length and not content-length header. @RunOrVeith. (GITHUB-1544, GITHUB-1547)
    + [Google Cloud Storage] Update get_object() method and ensure object.size attribute is an integer and not a string. This way it’s consistent with list_objects() method. (GITHUB-1547)

* Fri Jan 29 2021 Pablo Suárez Hernández <pablo.suarezhernandez@suse.com>
- Update to 3.3.0:
  * Common
    + Fix a bug which would cause some prepared requests with empty bodies to be chunked which would cause some of the provider APIs such as OpenStack to return HTTP 400 errors. (GITHUB-1487, GITHUB-1488) [Michael Spagon - @mspagon]
    + Optimize various code imports (remove unnecessary imports, make some lazy, etc.), so now importing most of the modules is around ~20-40%% faster (~70 vs ~140 ms) and in some cases such as EC2 driver even more.
    + Now majority of the import time is spent in importing requests library. (GITHUB-1519) [Tomaz Muraus]
    + libcloud.pricing.get_size_price() function has been updated so it only caches pricing data in memory for the requested drivers.
    + Advertise Python 3.9 support in setup.py.
  * Compute
    + [GCE] Fix ex_set_image_labels method using incorrect API path. (GITHUB-1485) [Poul Petersen - @petersen-poul]
    + [OpenStack] Fix error setting ex_force_XXX_url without setting ex_force_base_url. (GITHUB-1492) [Miguel Caballer - @micafer]
    + [EC2] Update supported EC2 regions and instance sizes and add support for eu-north-1 region. (GITHUB-1486) [Arturo Noha - @r2ronoha]
    + [Ovh] Add support for multiple regions to the driver. User can select a region (location) by passing location argument to the driver constructor (e.g. location=ca). (GITHUB-1494) [Dan Hunsaker - @danhunsaker]
    + [GCE] Add support for creating nodes without a service account associated with them. Now when an empty list is passed for ex_service_accounts argument, VM will be created without service account attached.
    + [VSphere] Add new VMware VSphere driver which utilizes pyvmomi library and works under Python 3.
    + [OpenStack] Enable to get Quota Set detail. (GITHUB-1495) [Miguel Caballer - @micafer]
    + [OpenStack] Add ex_get_size_extra_specs function to OpenStack driver. (GITHUB-1517) [Miguel Caballer - @micafer]
    + [OpenStack] Enable to get Neutron Quota details in OpenStack driver. (GITHUB-1514) [Miguel Caballer - @micafer]
    + [DigitalOcean] _node_node method now ensures image and size attributes are also set correctly and populated on the Node object. (GITHUB-1507, GITHUB-1508) [@sergerdn]
    + [Vultr] Make sure private_ips attribute on the Node object is correctly populated when listing nodes. Also add additional values to the node.extra dictionary. (GITHUB-1506) [@sergerdn]
    + [EC2] Optimize EC2 driver imports and move all the large constant files to separate modules in libcloud/compute/constants/ec2_*.py files.
    + [Packet / Equinix Metal] Packet driver has been renamed to Equinix Metal. If your code uses Packet.net driver, you need to update it as per example in Upgrade Notes documentation section. (GITHUB-1511) [Dimitris Galanis - @dimgal1]
    + [OutScale] Add various extension methods to the driver. For information on available extenion methods, please refer to the driver documentation. (GITHUB-1499) [@tgn-outscale]
    + [Linode] Add support for Linode’s API v4. (GITHUB-1504) [Dimitris Galanis - @dimgal1]
  * Storage
    + Deprecated lockfile library which is used by the Local Storage driver has been replaced with fasteners library. [Tomaz Muraus - @Kami]
    + [S3] Add support for us-gov-east-1 region. (GITHUB-1509, GITHUB-1510) [Andy Spohn - @spohnan]
    + [DigitalOcean Spaces] Add support for sfo2 regon. (GITHUB-1525) [Cristian Rasch - @cristianrasch]
    + [MinIO] Add new driver for MinIO object storage (https://min.io). (GITHUB-1528, GITHUB-1454) [Tomaz Muraus - @Kami]
    + [S3] Update S3 and other drivers which are based on the S3 one (Google Storage, RGW, MinIO) to correctly throw ContainerAlreadyExistsError if container creation fails because container with this name already exists.
    + Add new libcloud.common.base.ALLOW_PATH_DOUBLE_SLASHES module level variable.
  * DNS
    + [Common] Fix a bug with the header value returned by the export_zone_to_bind_format method containing an invalid timestamp (value for the minute part of the timestamp was wrong and contained month number instead of the minutes value). (GITHUB-1500) [Tomaz Muraus - @Kami]
    + [CloudFlare DNS] Add support for creating SSHFP records. (GITHUB-1512, GITHUB-1513) [Will Hughes - @insertjokehere]
    + [DigitalOcean] Update driver and make sure request data is sent as part of HTTP request body on POST and PUT operations (previously it was sent as part of query params). (GITHUB-1505) [Andrew Starr-Bochicchio - @andrewsomething]
    + [AuroraDNS] Throw correct exception on 403 authorization failed API error. (GITHUB-1521, GITHUB-1522) [Freek Dijkstra - @macfreek]
    + [Linode] Add support for Linode’s API v4. (GITHUB-1504) [Dimitris Galanis - @dimgal1]
    + [CloudFlare] Update driver so it correctly throws RecordAlreadyExists error on various error responses which represent this error. [Tomaz Muraus - @Kami]

* Tue Nov  3 2020 Pablo Suárez Hernández <pablo.suarezhernandez@suse.com>
- Fix bcond macros on SPEC file to properly manage Python 2 and Python 3 builds.

* Fri Oct 30 2020 Pablo Suárez Hernández <pablo.suarezhernandez@suse.com>
- Skip conflictive 'ParamikoSSHClientTests.test_key_file_non_pem_format_error' test
  since our SLE python-paramiko package already has OpenSSH support on version < 2.7.0

* Fri Oct 30 2020 Pablo Suárez Hernández <pablo.suarezhernandez@suse.com>
- Add pyOpenSSL as build dependency to allow tests to pass on SLE15 family

* Wed Oct 28 2020 Pablo Suárez Hernández <pablo.suarezhernandez@suse.com>
- Do not build Python2 subpackage since 3.2.0 does not support Python2
- Adjust skipped SSH unit tests when paramiko <= 2.7.0
- Add:
  * skip-some-tests-for-older-paramiko-versions.patch

* Wed Oct 21 2020 Steve Kowalik <steven.kowalik@suse.com>
- Update to 3.2.0:
  * [OpenStack] Add ex_get_network() to the OpenStack driver to make it possible to retrieve a single network by using the ID.
  * [OpenStack] Fix pagination in the list_images() method and make sure method returns all the images, even if the result is spread across multiple pages.
  * [GCE] Add script for scraping GCE pricing data and improve price addition in _to_node_size method. (GITHUB-1468) [Eis D. Zaster - @Eis-D-Z]
  * [AWS EC2] Update script for scraping AWS EC2 pricing and update EC2 pricing data. (GITHUB-1469) [Eis D. Zaster - @Eis-D-Z]
  * [Deployment] Add new wait_period argument to the deploy_node method and default it to 5 seconds.
  * [Azure ARM] Add script for scraping Azure ARM instance pricing data. (GITHUB-1470) [Eis D. Zaster - @Eis-D-Z]
  * [Deployment] Make FileDeployment class much faster and more efficient when working with large files or when running multiple FileDeployment steps on a single node.
  * [Deployment] Add __repr__() and __str__() methods to all the Deployment classes. [Tomaz Muraus - @Kami]
  * [Deployment] New keep_alive and use_compression arguments have been added to the ParamikoSSHClient class constructor.
  * [Deployment] Update ParamikoSSHClient.put() method so it returns a correct path when commands are being executed on a Windows machine.
  * [Outscale] Add a new driver for the Outscale provider. Existing Outscale driver utilizes the EC2 compatible API and this one utilizes native Outscale API. (GITHUB-1476) [Tio Gobin - @tgn-outscale]
  * [KubeVirt] Add new methods for managing services which allows users to expose ports for the VMs (ex_list_services, ex_create_service, ex_delete_service). (GITHUB-1478) [Eis D. Zaster - @Eis-D-Z]
  * [LXD] Add new methods for managing network and storage pool capabilities and include other improvements in some of the existing methods. (GITHUB-1477) [Eis D. Zaster - @Eis-D-Z]
  * [DigitalOcean] Add location argument to the list_sizes() method.
  * Fix deploy_node() so an exception is not thrown if any of the output (stdout / stderr) produced by the deployment script contains a non-valid utf-8 character.
  * Add new timeout argument to ScriptDeployment and ScriptFileDeployment class constructor.
  * [GiG G8] Fix retry functionality when creating port forwards and add support for automatically refresing the JWT auth token inside the connection class if it's about to expire in 60 seconds or less. (GITHUB-1465) [Jo De Boeck - @grimpy]
  * [Azure ARM] Update create_node so an exception is thrown if user passes ex_use_managed_disks=False, but doesn't provide a value for the ex_storage_account argument. (GITHUB-1448) [@antoinebourayne]
  * [AWS S3] Make sure driver works correctly for objects with ~ in the name.
  * [CloudFlare] Update driver to include the whole error chain the thrown exception message field.
  * [Gandi Live] Don't throw if extra['rrset_ttl'] argument is not passed to the create_record method. (GITHUB-1463) [Tomaz Muraus]

* Wed May 27 2020 Steve Kowalik <steven.kowalik@suse.com>
- Update to v3.0.0:
  * Make sure auth_user_info variable on the OpenStack identify connection class is populated when using auth version 3.x_password and 3.x_oidc_access_token.
  * [OpenStack] Update OpenStack identity driver so a custom project can be selected using domain_name keyword argument containing a project id.
  * [GCE] Update create_node() method so it throws an exception if node location can't be inferred and location is not specified by the user ( either by passing datacenter constructor argument or by passing location argument to the method).
  * [GCE] Update ex_get_disktype method so it works if zone argument is not set. (GITHUB-1443) [Tomaz Muraus]
  * [GiG G8] Add new driver for GiG G8 provider (https://gig.tech/). (GITHUB-1437) [Jo De Boeck - @grimpy]
  * [OpenStack] Fix auto assignment of volume device when using device name auto in the attach_volume method. (GITHUB-1444) [Joshua Hesketh - @jhesketh]
  * [Kamatera] Add new driver for Kamatera provider (https://www.kamatera.com). (GITHUB-1442) [Ori Hoch - @OriHoch]
  * Add new download_object_range and download_object_range_as_stream methods for downloading part of the object content (aka range downloads) to the base storage API.
  * [Google Storage] Update the driver so it supports service account HMAC credentials.
  * [Kubernetes] Add support for the client certificate and static token based authentication to the driver. (GITHUB-1421) [Tomaz Muraus]
  * Add support for Ed25519 private keys for deploy_node() functionality when using paramiko >= 2.2.0. (GITHUB-1445) [Tomaz Muraus - @Kami]
  * Fix deploy_node() so it correctly propagates an exception is a private key which is used is password protected, but no password is specified.
  * Allow user to specify password for encrypted keys by passing ssh_key_password argument to the deploy_node() method.
  * Fix deploy_node() method so we don't retry on fatal SSHCommandTimeoutError exception (exception which is thrown when a command which is running on remote host times out). (GITHUB-1445) [Tomaz Muraus - @Kami]
  * Add new stdout and stderr attribute to SSHCommandTimeoutError class.
  * [OpenStack] Fix auto assignment of volume device when using device name auto in the attach_volume method. (GITHUB-1444) [Joshua Hesketh - @jhesketh]
- Refresh patches gce_image_projects.patch and ec2_create_node.patch.

* Thu Mar 12 2020 Tomáš Chvátal <tchvatal@suse.com>
- Fix build without python2

* Thu Mar  5 2020 Niels Abspoel <aboe76@gmail.com>
- update to 2.8.1
  for the changelog see:
  https://libcloud.readthedocs.io/en/stable/changelog.html#changes-in-apache-libcloud-v2-8-1

* Fri Feb 21 2020 Sean Marlow <sean.marlow@suse.com>
- Add gce_image_projects.patch to update the current list of SUSE
  image projects in GCE.

* Thu Feb 20 2020 James Fehlig <jfehlig@suse.com>
- Stop building for python2

* Thu Jan 16 2020 Marketa Calabkova <mcalabkova@suse.com>
- update to 2.8.0
  * Distribution now includes py.typed file which signals mypy that
    this package contains type annotations
  * Fix get_driver() bug / regression not working if the provider
    argument was a string and not a Provider ENUM.

* Fri Dec 13 2019 Thomas Bechtold <tbechtold@suse.com>
- update to 2.7.0:
  - Test code with Python 3.8 and advertise that we also support Python 3.8.
  - [OpenStack] Fix OpenStack project scoped token authentication. The driver
    constructors now accept ``ex_tenant_domain_id`` argument which tells
    authentication service which domain id to use for the scoped authentication
    token. (GITHUB-1367)
  - Introduce type annotations for the base compute API methods. This means you
    can now leverage mypy to type check (with some limitations) your code which
    utilizes Libcloud compute API standard API methods.
  - [Azure ARM] Fix ``attach_volume`` method and allow maximum of 64 disks to be
    added when LUN is not specified. Previously there was a bug and only a
    maximum of 63 disks could be added.
  - New ``start_node`` and ``stop_node`` methods have been added to the base
    Libcloud compute API NodeDriver class.
  - [GCE] Add new ``ex_set_volume_labels`` method for managing volume labels to
    the driver.
  - [EC2] Add support for new ``inf1.*`` instance types.
  - [S3] Update S3 driver so a single driver class can be used for different
    regions.
  - [S3] Add missing ``eu-north-1`` region to the S3 driver. (GITHUB-1370)
  - [S3] Add missing regions (eu-west-3, ap-northeast-3, me-south-1) to the driver.
  - [S3] Update the driver to throw more user-friendly error message if user is
    using driver for a region X, but trying to upload / download object to / from
    a region Y.

* Wed Sep 18 2019 Tomáš Chvátal <tchvatal@suse.com>
- Update to 2.6.0:
  * Many various cloud fixes and tweaks for future python releases
  * See CHANGES.rst

* Thu May 16 2019 ranand@suse.com
- Skip failing ElasticContainerDriverTestCase, with invalid URL

* Mon Feb 25 2019 John Vandenberg <jayvdb@gmail.com>
- Activate test suite, deselecting one set of tests which ssh to localhost
- Remove image_projects.patch merged upstream
- Add Suggests for optional dependencies paramiko, lockfile, libvirt-python
  and pysphere
- Add example code to %%doc
- Update to v2.4.0
  * Refuse installation with Python 2.6 and Python 3.3
  * Support Python 3.7
  * Cleanup various Python files
  * Allow running tests with http_proxy set
  * Common
    + Document openstack_connection_kwargs method
    + Handle missing user email in OpenStackIdentityUser
  * Compute
    + [ARM] Support OS disk size definition on node creation
    + [Digital Ocean] Support floating IPs
    + [Digital Ocean] Support attach/detach for floating IPs
    + [Digital Ocean] Add ex_get_node_details
    + [Digital Ocean] Add tags extra attribute to create_node
    + [Dimension Data] Fix IndexError in list_images
    + [EC2] Add AWS eu-west-3 (Paris) region
    + [EC2] Add description to ex_authorize_security_group_ingress
    + [EC2] Added script to automatically get EC2 instance sizes
    + [EC2] Update instance sizes
    + [EC2] Accept tags when create a snapshot
    + [GCE] Expand Firewall options coverage
    + [GCE] Expand network and subnetwork options coverage
    + [GCE] Extend ex_create_address to allow internal ip creation
    + [GCE] Allow shared VPC in managed instance group creation
    + [GCE] Support disk_size parameter for boot disk when creating instance
    + [GCE] Update public image projects list
    + [GCE] Fix _find_zone_or_region for >500 instances
    + [GCE] Allow routing_mode=None in ex_create_network
    + [OpenStack] Implement Glance Image API v2
    + [OpenStack] Fix spelling in ex_files description
    + [OpenStack v2] Allow listing image members
    + [OpenStack v2] Allow creating and accepting image members
    + [OpenStack v2] Fix image members methods
    + [OpenStack] Fix API doc for delete_floating_ip
    + [OpenStack] Implement port attaching/detaching
    + [OpenStack] Add methods for getting and creating ports
    + [OpenStack] Add get_user method
    + [OpenStack] Add ex_list_subnets to OpenStack_2_NodeDriver
    + [OpenStack] The OpenStack_2_NodeDriver uses two connections
    + [OpenStack] The OpenStack_2_NodeDriver /v2.0/networks instead of /os-networks
    + [Scaleway] New Scaleway driver
    + [Scaleway] Update Scaleway default API host
  * DNS
    + [Google Cloud DNS] Document driver instantiation
  * Storage
    + Update docstring for storage provider class
    + [Azure Blob Storage] Allow filtering lists by prefix
    + [Azure Blob Storage] Update driver documentation
    + [Azure Blob Storage] Fix upload/download streams
    + [Azure Blob Storage] Fix PageBlob headers
    + [S3] Guess s3 upload content type
    + [S3] Add Amazon S3 (cn-northwest-1) Storage Driver
  * Other
    + Fixed spelling in 2.0 changes documentation

* Fri Sep 28 2018 Sean Marlow <sean.marlow@suse.com>
- Add ec2_create_node.patch to allow for instance type strings
  in create_node method.

* Tue Aug 14 2018 sean.marlow@suse.com
- Cleanup RPM warnings.
- Add image_projects.patch with updated list of latest image
  projects.

* Wed Jun  6 2018 jengelh@inai.de
- Use noun phrase in summary.

* Thu May 10 2018 toddrme2178@gmail.com
- Make sure ssl is available

* Wed May  2 2018 tchvatal@suse.com
- Version update to 2.3.0:
  * For the changes see CHANGES.rst as it is too long
  * many various bugfixes
- Drop no longer applying patch fix-backports-usage.patch

* Sat Sep 30 2017 mc@suse.com
- fix build on SLE12 by using python-backports
- reduce warnings

* Tue May 16 2017 jmatejek@suse.com
- convert to singlespec
- update requires
- update source url

* Sun Apr 30 2017 aboe76@gmail.com
- Updated to apache libcloud 2.0.0
  for the changelog see:
  https://github.com/apache/libcloud/blob/trunk/CHANGES.rst#changes-in-apache-libcloud-200

* Tue Oct 18 2016 aboe76@gmail.com
- Updated to apache libcloud 1.3.0
  for the changelog see:
  https://github.com/apache/libcloud/blob/trunk/CHANGES.rst#changes-in-apache-libcloud-130

* Wed Jan 20 2016 aboe76@gmail.com
- Updated to apache libcloud 0.20.1
- General:
  - Introduction of container based drivers for Docker, Rkt and Container-as-a-service providers
    (LIBCLOUD-781, GITHUB-666) [Anthony Shaw]
  - Introduce a new libcloud.backup API for Backup as a Service projects and products.
    (GITHUB-621) [Anthony Shaw]
  - Also retry failed HTTP(s) requests upon transient “read operation timed out” SSL error.
    (GITHUB-556, LIBCLOUD-728) [Scott Kruger]
  - Throw a more user-friendly exception if a client fails to establish SSL / TLS connection
    with a server because of an unsupported SSL / TLS version. (GITHUB-682) [Tomaz Muraus]
- Compute:
  - Add ap-northeast-2 region to EC2 driver (South Korea) (GITHUB-681) [Anthony Shaw]
  - Added Added volume type to EC2 volume extra to EC2 driver. (GITHUB-680) [Gennadiy Stas]
  - Add LazyObject class that provides lazy-loading, see GCELicense for usage (LIBCLOUD-786,
    GITHUB-665) [Scott Crunkleton]
  - Added t2.nano instance type to EC2 Compute driver (GITHUB-663) [Anthony Shaw]
  - Support for passing the image ID as a string instead of an instance of image when creating
    nodes in Dimension Data driver. (GITHUB-664) [Anthony Shaw]
- DNS:
  - Add support for ‘health checks’ in Aurora DNS driver (GITHUB-672) [Wido den Hollander]
  - Make sure ttl attribute is correctly parsed and added to the Record extra dictionary.
    (GITHUB-675) [Wido den Hollander]
  - Improve unit tests of Aurora DNS driver (GITHUB-679) [Wido den Hollander]

* Thu Dec 17 2015 aboe76@gmail.com
- Updated to apache libcloud 0.20.0
  - new requirement: python-backports.ssl_match_hostname
  for the changelog see:
  https://libcloud.readthedocs.org/en/latest/changelog.html#changes-with-apache-libcloud-0-20-0

* Sun Nov  1 2015 aboe76@gmail.com
- Updated to apache libcloud 0.19.0
  for the changelog see:
  https://github.com/apache/libcloud/blob/trunk/CHANGES.rst#changes-with-apache-libcloud-0190

* Thu Aug 13 2015 aboe76@gmail.com
- Updated to apache libcloud 0.18.0
  for the changelog see:
  https://github.com/apache/libcloud/blob/v0.18.0/CHANGES.rst#changes-with-apache-libcloud-0180

* Wed Feb 18 2015 aboe76@gmail.com
- Updated to Apache Libcloud 0.17.0
- skipped 0.16.0 but the changes are listed here also.
- General:
  - Use match_hostname function from backports.ssl_match_hostname package to verify the SSL certificate hostname instead of relying on our own logic. (GITHUB-374) [Alex Gaynor]
  - Add new OpenStackIdentity_3_0_Connection class for working with OpenStack Identity (Keystone) service API v3. [Tomaz Muraus]
  - Add support for prettifying JSON or XML response body which is printed to a file like object when using LIBCLOUD_DEBUG environment variable. This option can be enabled by setting LIBCLOUD_DEBUG_PRETTY_PRINT_RESPONSE environment variable. [Tomaz Muraus]
  - Add support for using an HTTP proxy for outgoing HTTP and HTTPS requests. [Tomaz Muraus, Philip Kershaw]
- Compute:
  - GCE driver updated to include ex_stop_node() and ex_start_node() methods. (GITHUB-442) [Eric Johnson]
  - GCE driver now raises ResourceNotFoundError when the specified image is not found in any image project. Previously, this would return None but now raises the not-found exception instead. This fixes a bug where returning None caused ex_delete_image to raise an AttributeError. (GITHUB-441) [Eric Johnson]
  - GCE driver update to support JSON format Service Account files and a PY3 fix from Siim Põder for LIBCLOUD-627. (LIBCLOUD-627, LIBCLOUD-657, GITHUB-438) [Eric Johnson]
  - GCE driver fixed for missing param on ex_add_access_config. (GITHUB-435) [Peter Mooshammer]
  - GCE driver support for HTTP load-balancer resources. (LIBCLOUD-605, GITHUB-429) [Lee Verberne]
  - GCE driver updated to make better use of GCEDiskTypes. (GITHUB-428) [Eric Johnson]
  - GCE driver list_images() now returns all non-deprecated images by default. (LIBCLOUD-602, GITHUB-423) [Eric Johnson]
  - Improve GCE API coverage for create_node(). (GITHUB-419) [Eric Johnson]
  - GCE Licenses added to the GCE driver. (GITHUB-420) [Eric Johnson]
  - GCE Projects support common instance metadata and usage export buckets. (GITHUB-409) [Eric Johnson]
  - Improvements to TargetPool resource in GCE driver. (GITHUB-414) [Eric Johnson]
  - Adding TargetInstances resource to GCE driver. (GITHUB-393) [Eric Johnson]
  - Adding DiskTypes resource to GCE driver. (GITHUB-391) [Eric Johnson]
  - Fix boot disk auto_delete in GCE driver. (GITHUB-412) [Igor Bogomazov]
  - Add Routes to GCE driver. (GITHUB-410) [Eric Johnson]
  - Add missing ubuntu-os-cloud images to the GCE driver. (LIBCLOUD-632, GITHUB-385) [Borja Martin]
  - Add new us-east-2 and us-east-3 region to the Joyent driver. (GITHUB-386) [ZuluPro]
  - Add missing t2. instance types to the us-west-1 region in the EC2 driver. (GITHUB-388) [Matt Lehman]
  - Add option to expunge VM on destroy in CloudStack driver. (GITHUB-382) [Roeland Kuipers]
  - Add extra attribute in list_images for CloudStack driver. (GITHUB-389) [Loic Lambiel]
  - Add ex_security_group_ids argument to the create_node method in the EC2 driver. This way users can launch VPC nodes with security groups. (GITHUB-373) [Itxaka Serrano]
  - Add description argument to GCE Network. (GITHUB-397) [Eric Johnson]
  - GCE: Improve MachineType (size) coverage of GCE API. (GITHUB-396) [Eric Johnson]
  - GCE: Improved Images coverage. (GITHUB-395) [Eric Johnson]
  - GCE: Support for global IP addresses. (GITHUB-390, GITHUB-394) [Eric Johnson]
  - GCE: Add missing snapshot attributes. (GITHUB-401) [Eric Johnson]
  - AWS: Set proper disk size in c3.X instance types. (GITHUB-405) [Itxaka Serrano]
  - Fix a bug with handling of the ex_keyname argument in the Softlayer driver. (GITHUB-416, LIBCLOUD-647) [Dustin Oberloh]
  - Update CloudSigma region list (remove Las Vegas, NV region and add new San Jose, CA and Miami, FL region). (GITHUB-417) [Viktor Petersson]
  - Add ex_get_node method to the Joyent driver. (GITHUB-421) [ZuluPro]
  - Add support for placement group management to the EC2 driver. (GITHUB-418) [Mikhail Ovsyannikov]
  - Add new tok02 region to the Softlayer driver. (GITHUB-436, LIBCLOUD-656) [Dustin Oberloh]
  - Add new Honolulu, HI endpoint to the CloudSigma driver. (GITHUB-439) [Stephen D. Spencer]
  - Fix a bug with config_drive attribute in the OpenStack driver. New versions of OpenStack now return a boolean and not a string. (GITHUB-433) [quilombo]
  - Add support for Abiquo API v3.x, remove support for now obsolete API v2.x. (GITHUB-433, LIBCLOUD-652) [David Freedman]
  - Allow rootdisksize parameter in create_node CloudStack driver (GITHUB-440, LIBCLOUD-658) [Loic Lambiel]
  - Fix an issue with LIBCLOUD_DEBUG not working correctly with the Linode driver. [Tomaz Muraus, Juan Carlos Moreno] (LIBCLOUD-598, GITHUB-342)
  - Add new driver for VMware vSphere (http://www.vmware.com/products/vsphere/) based clouds. [Tomaz Muraus]
  - Add two new default node states - NodeState.SUSPENDED and NodeState.ERROR. [Tomaz Muraus]
  - Fix to join networks properly in deploy_node in the CloudStack driver. (LIBCLOUD-593, GITUHB-336) [Atsushi Sasaki]
  - Create CloudStackFirewallRule class and corresponding methods. (LIBCLOUD-594, GITHUB-337) [Atsushi Sasaki]
  - Add support for SSD disks to Google Compute driver. (GITHUB-339) [Eric Johnson]
  - Add utility get_regions and get_service_names methods to the OpenStackServiceCatalog class. [Andrew Mann, Tomaz Muraus]
  - Fix a bug in ex_get_console_output in the EC2 driver which would cause an exception to be thrown if there was no console output for a particular node.
    Reported by Chris DeRamus. [Tomaz Muraus]
  - Add ip_address parameter in CloudStack driver create_node method. (GITHUB-346) [Roeland Kuipers]
  - Fix ParamikoSSHClient.run and deploy_node method to work correctly under Python 3. (GITHUB-347) [Eddy Reyes]
  - Update OpenStack driver to map more node states to states recognized by Libcloud. [Chris DeRamus]
  - Fix a bug with ex_metadata argument handling in the Google Compute Engine driver create_node method. (LIBCLOUD-544, GITHUB-349, GITHUB-353) [Raphael Theberge]
  - Add SSH key pair management methods to the Softlayer driver. (GITHUB-321, GITHUB-354) [Itxaka Serrano]
  - Correctly categorize node IP addresses into public and private when dealing with OpenStack floating IPs. [Andrew Mann]
  - Add new t2 instance types to the EC2 driver. [Tomaz Muraus]
  - Add support for Amazon GovCloud to the EC2 driver (us-gov-west-1 region). [Chris DeRamus]
  - Allow user to pass "gp2" for "ex_volume_type" argument to the create_volume method in the EC2 driver.
    Reported by Xavier Barbosa. [Tomaz Muraus, Xavier Barbosa]
  - Add new driver for ProfitBricks provider. (LIBCLOUD-589, GITHUB-352) [Matt Baldwin]
  - Various improvements and bugs fixes in the GCE driver. For a list, see https://github.com/apache/libcloud/pull/360/commits (GITHUB-360) [Evgeny Egorochkin]
  - Allow user to specify virtualization type when registering an EC2 image by passing virtualization_type argument to the ex_register_image method. (GITHUB-361) [Andy Grimm]
  - Add ex_create_image method to the GCE driver. (GITHUB-358, LIBCLOUD-611) [Katriel Traum]
  - Add some methods to CloudStack driver: create_volume_snapshot, list_snapshots, destroy_volume_snapshot create_snapshot_template, ex_list_os_types) (GITHUB-363, LIBCLOUD-616) [Oleg Suharev]
  - Added VPC support and Egress Firewall rule support fo CloudStack (GITHUB-363) [Jeroen de Korte]
  - Add additional attributes to the extra dictionary of OpenStack StorageVolume object. (GITHUB-366) [Gertjan Oude Lohuis]
  - Fix create_volume method in the OpenStack driver to return a created volume object (instance of StorageVolume) on success, instead of a boolean indicating operation success. (GITHUB-365) [Gertjan Oude Lohuis]
  - Add optional project parameters for ex_list_networks() to CloudStack driver (GITHUB-367, LIBCLOUD-615) [Rene Moser]
  - CLOUDSTACK: option to start VM in a STOPPED state (GITHUB-368) [Roeland Kuipers]
  - Support "config_drive" in the OpenStack driver. Allow users to pass ex_config_drive argument to the create_node and ex_rebuild_node method. (GITHUB-370) [Nirmal Ranganathan]
  - Add support for service scopes to the create_node method in the GCE driver. (LIBCLOUD-578, GITHUB-373) [Eric Johnson]
  - Update GCE driver to allow for authentication with internal metadata service. (LIBCLOUD-625, LIBCLOUD-276, GITHUB-276) [Eric Johnson]
  - Fix a bug in Elasticstack node creation method where it would raise exceptions because of missing data in a response, and also fix pulling the IP from the proper data item. (GITHUB-325) [Michael Bennett]
  - Fix a bug which prevented user to connect and instantiate multiple EC2 driver instances for different regions at the same time. (GITHUB-325) [Michael Bennett]
  - Add methods in CloudStack driver to manage mutiple nics per vm. (GITHUB-369) [Roeland Kuipers]
  - Implements VPC network ACLs for CloudStack driver. (GITHUB-371) [Jeroen de Korte]
- Storage:
  - Allow user to pass headers argument to the upload_object and upload_object_via_stream method.
    This way user can specify CORS headers with the drivers which support that. (GITHUB-403, GITHUB-404) [Peter Schmidt]
  - Fix upload_object_via_stream so it works correctly under Python 3.x if user manually passes an iterator to the method.
    Also improve how reading a file in chunks works with drivers which support chunked encoding - always try to fill a chunk with CHUNK_SIZE bytes instead of directly streaming the chunk which iterator returns.
    Previously, if iterator returned 1 byte in one iteration, we would directly send this as a single chunk to the API. (GITHUB-408, LIBCLOUD-639) [Peter Schmidt]
  - Fix a bug with CDN requests in the CloudFiles driver. [Tomaz Muraus]
  - Fix a bug with not being able to specify meta_data / tags when uploading an object using Google Storage driver. (LIBCLOUD-612, GITHUB-356) [Stefan Friesel]
- Loadbalancer:
  - Updates to CloudStack driver. (GITHUB-434) [Jeroen de Korte]
  - Allow user to specify session affinity algorithm in the GCE driver by passing ex_session_affinity argument to the create_balancer method. (LIBCLOUD-595, GITHUB-341) [Lee Verberne, Eric Johnson]
- DNS:
  - New driver for Softlayer DNS service. (GITHUB-413, LIBCLOUD-640) [Vanč Levstik]
  - Fix a bug with ex_create_multi_value_record method in the Route53 driver only returning a single record. (GITHUB-431, LIBCLOUD-650) [Itxaka Serrano]
  - Various fixes in the Google DNS driver. (GITHUB-378) [Franck Cuny]

* Mon Jul 21 2014 aboe76@gmail.com
- Updated to Apache Libcloud 0.15.1
- Compute:
  - Allow user to limit a list of subnets which are returned by passing subnet_ids and filters argument to the ex_list_subnets
    method in the EC2 driver. (LIBCLOUD-571, GITHUB-306) [Lior Goikhburg]
  - Allow user to limit a list of internet gateways which are returned by passing gateway_ids and filters argument to the
    ex_list_internet_gateways method in the EC2 driver. (LIBCLOUD-572, GITHUB-307) [Lior Goikhburg]
  - Allow user to filter which nodes are returned by passing ex_filters argument to the list_nodes method in the EC2 driver.
    (LIBCLOUD-580, GITHUB-320) [Lior Goikhburg]
  - Add network_association_id to ex_list_public_ips and CloudstackAddress object (GITHUB-327) [Roeland Kuipers]
  - Allow user to specify admin password by passing ex_admin_pass argument to the create_node method in the Openstack driver.
    (GITHUB-315) [Marcus Devich]
  - Fix a possible race condition in deploy_node which would occur if node is online and can be accessed via SSH, but the
    SSH key we want to use hasn’t been installed yet.
    Previously, we would immediately throw if we can connect, but the SSH key hasn’t been installed yet. (GITHUB-331) [David Gay]
    Propagate an exception in deploy_node method if user specified an invalid path to the private key file. Previously
    this exception was silently swallowed and ignored. [Tomaz Muraus]
- DNS:
  - Include a better message in the exception which is thrown when a request in the Rackspace driver ends up in an ERROR state. [Tomaz Muraus]

* Wed Jun 25 2014 aboe76@gmail.com
- Updated to Apache LibCloud 0.15.0
- Package:
  - New requirement python-lxml
- general:
  - Use lxml library (if available) for parsing XML. This should substantially reduce parsing time and memory usage for large XML responses (e.g. retrieving all the available images in the EC2 driver). [Andrew Mann]
  - Use –head flag instead of -X HEAD when logging curl lines for HEAD requests in debug mode.
    Reported by Brian Metzler. (LIBCLOUD-552) [Tomaz Muraus]
  - Fix Python 3 compatibility bugs in the following functions:
  - import_key_pair_from_string in the EC2 driver
  - publickey._to_md5_fingerprint
  - publickey.get_pubkey_ssh2_fingerprint
    (GITHUB-301) [Csaba Hoch]
  - Update CA_CERTS_PATH to also look for CA cert bundle which comes with openssl Homebrew formula on OS x (/usr/local/etc/openssl/cert.pem). (GITHUB-309) [Pedro Romano]
  - Update Google drivers to allow simultaneous authornization for all the supported Google Services. (GITHUB-302) [Eric Johnson]
- Compute:
  - Fix create_key_pair method which was not returning private key. (LIBCLOUD-566) [Sebastien Goasguen]
  - Map “Stopped” node state in the CloudStack driver to NodeState.STOPPED instead of NodeState.TERMINATED, “Stopping” to NodeState.PENDING instead of NodeState.TERMINATED and “Expunging” to NodeState.PENDING instead of NodeState.TERMINATED. (GITHUB-246) [Chris DeRamus, Tomaz Muraus]
  - Add ex_create_tags and ex_delete_tags method to the CloudStack driver. (LIBCLOUD-514, GITHUB-248) [Chris DeRamus]
  - Add new G2 instances to the EC2 driver. [Tomaz Muraus]
  - Add support for multiple API versions to the Eucalyptus driver and allows user to pass “api_version” argument to the driver constructor. (LIBCLOUD-516, GITHUB-249) [Chris DeRamus]
  - Map “Powered Off” state in the vCloud driver from “TERMINATED” to “STOPPED”. (GITHUB-251) [Ash Berlin]
  - Add ex_rename_node method to the DigitalOcean driver. (GITHUB-252) [Rahul Ranjan]
  - Improve error parsing in the DigitalOcean driver.
    Reported by Deni Bertovic. [Tomaz Muraus]
  - Add extension methods for the VPC internet gateway management to the EC2 driver. (LIBCLOUD-525, GITHUB-255) [Chris DeRamus]
  - Add CloudStackProject class to the CloudStack driver and add option to select project and disk offering on node creation. (LIBCLOUD-526, GITHUB-257) [Jim Divine]
  - Fix IP address handling in the OpenStack driver. (LIBCLOUD-503, GITHUB-235) [Markos Gogoulos]
  - Ad new ex_delete_image and ex_deprecate_image method to the GCE driver. (GITHUB-260) [Franck Cuny]
  - Ad new ex_copy_image method to the GCE driver. (GITHUB-258) [Franck Cuny]
  - Ad new ex_set_volume_auto_delete method to the GCE driver. (GITHUB-264) [Franck Cuny]
  - Add ex_revoke_security_group_ingress method to the CloudStack driver. [Chris DeRamus, Tomaz Muraus]
  - Allow user to pass ex_ebs_optimized argument to the create_node method in the EC2 driver. (GITHUB-272) [zerthimon]
  - Add “deprecated” attribute to the Node object in the Google Compute Engine driver. (GITHUB-276) [Chris / bassdread]
  - Update Softlayer driver to use “fullyQualifiedDomainName” instead of “hostname” attribute for the node name. (GITHUB-280) [RoelVanNyen]
  - Allow user to specify target tags using target_tags attribute when creating a firewall rule in the GCE driver. (GITHUB-278) [zerthimon]
  - Add new standard API for image management and initial implementation for the EC2 and Rackspace driver. (GITHUB-277) [Matt Lehman]
  - Allow user to specify “displayname” attribute when creating a CloudStack node by passing “ex_displayname” argument to the method.
  - Also allow “name” argument to be empty (None). This way CloudStack automatically uses Node’s UUID for the name. (GITHUB-289) [Jeff Moody]
  - Deprecate “key” argument in the SSHClient class in favor of new “key_files” argument.
  - Also add a new “key_material” argument. This argument can contain raw string version of a private key.
    Note 1: “key_files” and “key_material” arguments are mutually exclusive. Note 2: “key_material” argument is not supported in the ShellOutSSHClient.
    Use node id attribute instead of the name for the “lconfig” label in the Linode driver. This way the label is never longer than 48 characters. (GITHUB-287) [earthgecko]
  - Add a new driver for Outscale SAS and Outscale INC cloud (http://www.outscale.com). (GITHUB-285, GITHUB-293, LIBCLOUD-536, LIBCLOUD-553) [Benoit Canet]
  - Add new driver for HP Public Cloud (Helion) available via Provider.HPCLOUD constant. [Tomaz Muraus]
  - Allow user to specify availability zone when creating an OpenStack node by passing “ex_availability_zone” argument to the create_node method. Note: This will only work if the OpenStack installation is running availability zones extension. (GITHUB-295, LIBCLOUD-555) [syndicut]
  - Allow user to pass filters to ex_list_networks method in the EC2 driver. (GITHUB-294) [zerthimon]
  - Allow user to retrieve container images using ex_get_image method in the Google Compute Engine driver. (GITHUB-299, LIBCLOUD-562) [Magnus Andersson]
  - Add new driver for Kili public cloud (http://kili.io/) [Tomaz Muraus]
  - Add “timeout” argument to the ParamikoSSHClient.run method. If this argument is specified and the command passed to run method doesn’t finish in the defined timeout, SSHCommandTimeoutError is throw and the connection to the remote server is closed.
    Note #1: If timed out happens, this functionality doesn’t guarantee that the underlying command will be stopped / killed. The way it works it simply closes a connect to the remote server. [Tomaz Muraus]
    Note #2: “timeout” argument is only available in the Paramiko SSH client.
  - Make “cidrs_ips” argument in the ex_authorize_security_group_egress method in the EC2 driver mandatory. (GITHUB-301) [Csaba Hoch]
  - Add extension methods for manging floating IPs (ex_get_floating_ip, ex_create_floating_ip, ex_delete_floating_ip) to the Openstack 1.1 driver. (GITHUB-301) [Csaba Hoch]
  - Fix bug in RimuHosting driver which caused driver not to work when the provider returned compressed (gzip’ed) response. (LIBCLOUD-569, GITHUB-303) [amastracci]
  - Fix issue with overwriting the server memory values in the RimuHosting driver. (GUTHUB-308) [Dustin Oberloh]
  - Add ex_all_tenants argument to the list_nodes method in the OpenStack driver. (GITHUB-312) [LIBCLOUD-575, Zak Estrada]
  - Add support for network management for advanced zones (ex_list_network_offerings, ex_create_network, ex_delete_network) in the CloudStack driver. (GITHUB-316) [Roeland Kuipers]
  - Add extension methods for routes and route table management to the EC2 driver (ex_list_route_tables, ex_create_route_table, ex_delete_route_table, ex_associate_route_table, ex_dissociate_route_table, ex_replace_route_table_association, ex_create_route, ex_delete_route, ex_replace_route) (LIBCLOUD-574, GITHUB-313) [Lior Goikhburg]
  - Fix ex_list_snapshots for HP Helion OpenStack based driver. [Tomaz Muraus]
  - Allow user to specify volume type and number of IOPS when creating a new volume in the EC2 driver by passing ex_volume_type and ex_iops argument to the create_volume method. [Tomaz Muraus]
  - Fix ex_unpause_node method in the OpenStack driver. (GITHUB-317) [Pablo Orduña]
  - Allow user to launch EC2 node in a specific VPC subnet by passing ex_subnet argument to the create_node method. (GITHUB-318) [Lior Goikhburg]
- Storage:
  - Fix container name encoding in the iterate_container_objects and get_container_cdn_url method in the CloudFiles driver. Previously, those methods would throw an exception if user passed in a container name which contained a whitespace.
    Reported by Brian Metzler. (LIBCLOUD-552) [Tomaz MUraus]
  - Fix a bug in the OpenStack Swift driver which prevented the driver to work with installations where region names in the service catalog werent upper case. (LIBCLOUD-576, GITHUB-311) [Zak Estrada]
- Load Balancer:
  - Add extension methods for policy managagement to the ELB driver. (LIBCLOUD-522, GITHUB-253) [Rahul Ranjan]
- DNS:
  - Fix update_record method in the Route56 driver so it works correctly for records with multiple values. [Tomaz Muraus]
  - Add ex_create_multi_value_record method to the Route53 driver which allows user to create a record with multiple values with a single call. [Tomaz Muraus]
  - Add new driver for Google DNS. (GITHUB-269) [Franck Cuny]

* Sun Feb  9 2014 aboe76@gmail.com
- Changes with Apache Libcloud 0.14.1
- Compute:
  - Add new m3.medium and m3.large instance information to the EC2 driver. [Tomaz Muraus]
  - Add a new driver for CloudSigma API v2.0. [Tomaz Muraus]
  - Add “volume_id” attribute to the Node “extra” dictionary in the EC2 driver. Also fix the value of the “device” extra attribute in the StorageVolume object. (LIBCLOUD-501) [Oleg Suharev]
  - Add the following extension methods to the OpenStack driver: ex_pause_node, ex_unpause_node, ex_suspend_node, ex_resume_node. (LIBCLOUD-505, GITHUB-238) [Chris DeRamus]
  - Add ex_limits method to the CloudStack driver. (LIBCLOUD-507, GITHUB-240) [Chris DeRamus]
  - Add “extra” dictionary to the CloudStackNode object and include more attributes in the “extra” dictionary of the network and volume object. (LIBCLOUD-506, GITHUB-239) [Chris DeRamus]
  - Add ex_register_image method to the EC2 driver. (LIBCLOUD-508, GITHUB-241) [Chris DeRamus]
  - Add methods for managing volume snapshots to the OpenStack driver. (LIBCLOUD-512, GITHUB-245) [Chris DeRamus]
- Load Balancer:
  - Fix a bug in the ex_targetpool_add_node and ex_targetpool_remove_node method in the GCE driver. [Rick Wright]
- Storage:
  - Allow user to use an internal endpoint in the CloudFiles driver by passing “use_internal_url” argument to the driver constructor. (GITHUB-229, GITHUB-231) [John Obelenus]
- DNS:
  - Add PTR to the supported record types in the Rackspace driver. [Tomaz Muraus]
  - Fix Zerigo driver to set Record.name attribute for records which refer to the bare domain to “None” instead of an empty string. [Tomaz Muraus]
  - For consistency with other drivers, update Rackspace driver to set Record.name attribute for the records which refer to the bare domain to “None” instead of setting them to FQDN. [Tomaz Muraus]
  - Update Rackspace driver to support paginating through zones and records. (GITHUB-230) [Roy Wellington]
  - Update Route53 driver so it supports handling records with multiple values (e.g. MX). (LIBCLOUD-504, GITHUB-237) [Chris DeRamus]
  - Update Route53 driver to better handle SRV records. [Tomaz Muraus]
  - Update Route53 driver, make sure “ttl” attribute in the Record extra dictionary is always an int. [Tomaz Muraus]

* Sat Jan 25 2014 aboe76@gmail.com
- Big release 0.14.0
- General:
  - If the file exists, read pricing data from ~/.libcloud/pricing.json by default.
  If the file doesn’t exist, fall back to the old behavior and use pricing data
    which is bundled with the release. [Tomaz Muraus]
  - Add libcloud.pricing.download_pricing_file function for downloading and
    updating the pricing file. [Tomaz Muraus]
  - Fix libcloud.utils.py3.urlquote so it works with unicode strings
    under Python 2. (LIBCLOUD-429) [Michael Farrell]
- Compute:
  - Refactor Rackspace driver classes and make them easier to use.
    Now there are two Rackspace provider constants - Provider.RACKSPACE which represents
    new next-gen OpenStack servers and Provider.RACKSPACE_FIRST_GEN
    which represents old first-gen cloud servers.
    Note: This change is backward incompatible.
    For more information on those changes and how to update your code,
    please visit “Upgrade Notes” documentation page - http://s.apache.org/lc0140un [Tomaz Muraus]
  - Deprecate the following EC2 provider constants:
    EC2_US_EAST, EC2_EU, EC2_EU_WEST, EC2_AP_SOUTHEAST,
    EC2_AP_NORTHEAST, EC2_US_WEST_OREGON, EC2_SA_EAST,
    EC2_SA_EAST and replace it with a new EC2 constant.
    Driver referenced by this new constant now takes a “region” argument which
    dictates to which region to connect.
    Note: Deprecated constants will continue to work until the next major release.
    For more information on those changes and how to update your code,
    please visit “Upgrade Notes” documentation page - http://s.apache.org/lc0140un [Tomaz Muraus]
  - Add support for volume related functions to OpenNebula driver. (LIBCLOUD-354) [Emanuele Rocca]
  - Add methods for managing storage volumes to the OpenStack driver. (LIBCLOUD-353) [Bernard Kerckenaere]
  - Add new driver for Google Compute Engine (LIBCLOUD-266, LIBCLOUD-386) [Rick Wright]
  - Fix create_node “features” metadata and update affected drivers. (LIBCLOUD-367) [John Carr]
  - Update EC2 driver to accept the auth kwarg (it will accept NodeAuthSSH objects and
    automatically import a public key that is not already uploaded to the EC2 keyring).
    (Follow on from LIBCLOUD-367). [John Carr]
  - Unify extension argument names for assigning a node to security groups in EC2 and OpenStack driver.
    Argument in the EC2 driver has been renamed from ex_securitygroup to ex_security_groups.
    For backward compatibility reasons, old argument will continue to work until the next major release.
    (LIBCLOUD-375) [Tomaz Muraus]
  - Add ex_import_keypair_from_string and ex_import_keypair method to the CloudStack driver.
    (LIBCLOUD-380) [Sebastien Goasguen]
  - Add support for managing floating IP addresses to the OpenStack driver. (LIBCLOUD-382) [Ivan Kusalic]
  - Add extension methods for handling port forwarding to the CloudStack driver,
    rename CloudStackForwardingRule class to CloudStackIPForwardingRule. (LIBCLOUD-348, LIBCLOUD-381) [sebastien goasguen]
  - Hook up deploy_node functionality in the CloudStack driver and unify extension arguments
    for handling security groups. (LIBCLOUD-388) [sebastien goasguen]
  - Allow user to pass “args” argument to the ScriptDeployment and ScriptFileDeployment class.
    This argument tells which command line arguments get passed to the ScriptDeployment script. (LIBCLOUD-394)
    Note: This change is backward incompatible.
    For more information on how this affects your code and how to update it,
    visit “Upgrade Notes” documentation page - http://s.apache.org/lc0140un [Tomaz Muraus]
  - Allow user to specify IAM profile to use when creating an EC2 node. (LIBCLOUD-403) [Xavier Barbosa]
  - Add support for keypair management to the OpenStack driver. (LIBCLOUD-392) [L. Schaub]
  - Allow user to specify disk partitioning mode using ex_disk_config argument in the OpenStack based drivers.
    (LIBCLOUD-402) [Brian Curtin]
  - Add new driver for NephoScale provider (http://nephoscale.com/). (LIBCLOUD-404) [Markos Gogoulos]
  - Update network related extension methods so they work correctly with both, OpenStack and Rackspace driver.
    (LIBCLOUD-368) [Tomaz Muraus]
  - Add tests for networking functionality in the OpenStack and Rackspace driver. [Tomaz Muraus]
  - Allow user to pass all supported extension arguments to ex_rebuild_server method in the OpenStack driver.
    (LIBCLOUD-408) [Dave King]
  - Add pricing information for Rackspace Cloud Sydney region. [Tomaz Muraus]
  - Update EC2 instance type map and pricing data. High Storage instances are now also available in
    Sydney and Singapore region. [Tomaz Muraus]
  - Add new methods for managing storage volumes and snapshots to the EC2 driver (list_volumes,
    list_snapshots, destroy_volume_snapshot, create_volume_snapshot) (LIBCLOUD-409) [Oleg Suharev]
  - Add the following new extension methods to EC2 driver: ex_destroy_image, ex_modify_instance_attributes,
    ex_delete_keypair. (LIBCLOUD-409) [Oleg Suharev]
  - Allow user to specify a port range when creating a port forwarding rule. (LIBCLOUD-409) [Oleg Suharev]
  - Align Joyent driver with other drivers and deprecate “location” argument in the driver constructor
    in favor of “region” argument.
    Note: Deprecated argument will continue to work until the next major release. [Tomaz Muraus]
  - Deprecate the following ElasticHosts provider constants:
    ELASTICHOSTS_UK1, ELASTICHOSTS_UK2, ELASTICHOSTS_US1, ELASTICHOSTS_US2, ELASTICHOSTS_US3,
    ELASTICHOSTS_CA1, ELASTICHOSTS_AU1, ELASTICHOSTS_CN1 and replace it with a new ELASTICHOSTS constant.
    Driver referenced by this new constant now takes a “region” argument which dictates to which region to connect.
    Note: Deprecated constants will continue to work until the next major release. For more information on those changes and
    how to update your code, please visit “Upgrade Notes”
    documentation page - http://s.apache.org/lc0140un (LIBCLOUD-383) [Michael Bennett, Tomaz Muraus]
  - Add log statements to our ParamikoSSHClient wrapper. This should make debugging deployment issues easier.
    (LIBCLOUD-414) [Tomaz Muraus]
  - Add new “NodeState.STOPPED” node state. Update HostVirual and EC2 driver to also recognize this new state.
    (LIBCLOUD-296) [Jayy Vis]
  - Add new Hong Kong endpoint to Rackspace driver. [Brian Curtin]
  - Fix ex_delete_keypair method in the EC2 driver. (LIBCLOUD-415) [Oleg Suharev]
  - Add the following new extension methods for elastic IP management to the EC2 driver:
    ex_allocate_address, ex_disassociate_address, ex_release_address. (LIBCLOUD-417) [Patrick Armstrong]
  - For consistency and accuracy, rename “ex_associate_addresses” method in the EC2 driver to
    “ex_associate_address_with_node”.
    Note: Old method will continue to work until the next major release. [Tomaz Muraus]
  - Add new driver for CloudFrames (http://www.cloudfounders.com/CloudFrames) provider. (LIBCLOUD-358) [Bernard Kerckenaere]
  - Update default kernel versions which are used when creating a Linode server.
    Old default kernel versions:
    x86 - 2.6.18.8-x86_64-linode1
    x86_64 - 2.6.39.1-linode34
    New default kernel versions:
    x86 - 3.9.3-x86-linode52
    x86_64 - 3.9.3-x86_64-linode33
    (LIBCLOUD-424) [Tomaz Muraus, Jon Chen]
  - Disable cache busting functionality in the OpenStack and Rackspace next-gen driver and enable it
    only for Rackspace first-gen driver. [Tomaz Muraus]
  - Update Google Compute Engine driver to v1beta16. [Rick Wright]
  - Modify auth_url variable in the OpenStack drivers so it works more like users would expect it to.
    Previously path specified in the auth_url was ignored and only protocol, hostname and port were used.
    Now user can provide a full url for the auth_url variable and the path provided in the url is also used.
    [DaeMyung Kang, Tomaz Muraus]
  - Allow user to associate arbitrary key/value pairs with a node by passing “ex_metadata” argument
    (dictionary) to create_node method in the EC2 driver. Those values are associated with a node using
    tags functionality. (LIBCLOUD-395) [Ivan Kusalic]
  - Add “ex_get_metadata” method to EC2 and OpenStack driver. This method reads metadata dictionary
    from the Node object. (LIBCLOUD-395) [Ivan Kusalic]
  - Multiple improvements in the Softlayer driver:
  - Map “INITIATING” node state to NodeState.PENDING
  - If node is launching remap “halted” state to “pending”
  - Add more node sizes
  - Add ex_stop_node and ex_start_node method
  - Update tests response fixtures
    (LIBCLOUD-416) [Markos Gogoulos]
  - Modify list_sizes method in the KT UCloud driver to work, even if the item doesn’t have ‘diskofferingid’
    attribute. (LIBCLOUD-435) [DaeMyung Kang]
  - Add new c3 instance types to the EC2 driver. [Tomaz Muraus]
  - Fix an issue with the ex_list_keypairs and ex_list_security_groups method in the CloudStack driver
    which caused an exception to be thrown if the API returned no keypairs / security groups.
    (LIBCLOUD-438) [Carlos Reategui, Tomaz Muraus]
  - Fix a bug in the OpenStack based drivers with not correctly checking if the auth token has expired
    before re-using it. (LIBCLOUD-428)
    Reported by Michael Farrell. [Tomaz Muraus, Michael Farrell]
- Storage
  - Deprecate CLOUDFILES_US and CLOUDFILES_UK provider constant and replace it with a new CLOUDFILES constant.
    Driver referenced by this new constant takes a “region” keyword argument which can be one
    of ‘ord’, ‘dfw’, ‘iad’, ‘syd’, ‘lon’.
    Note: Deprecated constants will continue to work until the next major release.
    For more information on this change, please visit “Upgrade Notes”
    documentation section - http://s.apache.org/lc0140un [Tomaz Muraus]
  - Allow users to filter objects starting with a prefix by passing ex_prefix argument to the list_
    container_objects method in the S3, Google Storage and CloudFiles driver. (LIBCLOUD-369) [Stefan Friesel]
  - Fix an issue with mutating connectionCls.host attribute in the Azure driver. This bug prevented user
    from having multiple Azure drivers with different keys instantiated at the same time. (LIBCLOUD-399) [Olivier Grisel]
  - Add a new driver for KT UCloud based on the OpenStack Swift driver. (LIBCLOUD-431). [DaeMyung Kang]
- Load Balancer:
  - Deprecate RACKSPACE_US and RACKSPACE_UK provider constant and replace it with a new RACKSPACE constant.
    Driver referenced by this new constant takes a “region” keyword argument which can be one of the
    following: ‘ord’, ‘dfw’, ‘iad’, ‘syd’, ‘lon’.
    Note: Deprecated constants will continue to work until the next major release.
    For more information on this change, please visit “Upgrade Notes”
    documentation section - http://s.apache.org/lc0140un [Tomaz Muraus]
  - Add new driver for Google Compute Engine (LIBCLOUD-386) [Rick Wright]
  - Add new Hong Kong endpoint to Rackspace driver. [Brian Curtin]
- DNS:
  - Deprecate RACKSPACE_US and RACKSPACE_UK provider constant and replace it with a new RACKSPACE constant.
    Driver referenced by this new constant takes a “region” keyword argument which can be one of the
    following: ‘us’, ‘uk’.
    Note: Deprecated constants will continue to work until the next major release.
    For more information on this change, please visit “Upgrade Notes”
    documentation section - http://s.apache.org/lc0140un [Tomaz Muraus]
  - Use string instead of integer for RecordType ENUM value.
    Note: If you directly use an integer instead of RecordType ENUM class you need to update your code to
    use the RecordType ENUM otherwise the code won’t work. For more information on how to do that,
    see “Upgrade Notes” documentation section - http://s.apache.org/lc0140un [Tomaz Muraus]
  - Add “export_zone_to_bind_format” and export_zone_to_bind_zone_file method which allows users to
    export Libcloud Zone to BIND zone format. (LIBCLOUD-398) [Tomaz Muraus]
  - Update issue with inexistent zone / record handling in the get_zone and get_record
    method in the Linode driver. Those issues were related to changes in the Linode API. (LIBCLOUD-425) [Jon Chen]

* Thu Jan  2 2014 aboe76@gmail.com
- Updated to 0.13.3 (bnc#857209)
- Security fix release, for destroying nodes on digitalOcean
  'data_scrub' method is always invoked

* Thu Oct 24 2013 speilicke@suse.com
- Require python-setuptools instead of distribute (upstreams merged)

* Sun Sep 22 2013 aboe76@gmail.com
- Updated to 0.13.2
- General:
  - Don't sent Content-Length: 0 header with POST and PUT request if "raw"
    mode is used. This fixes a regression which could cause broken behavior
    in some storage driver when uploading a file from disk.
- Compute:
  - Added Ubuntu Linux 12.04 image to ElasticHost driver image list.
  (LIBCLOUD-364)
  - Update ElasticHosts driver to store drive UUID in the node 'extra' field.
  (LIBCLOUD-357)
- Storage:
  - Store last_modified timestamp in the Object extra dictionary in the S3
    driver. (LIBCLOUD-373)
- Load Balancer:
  - Expose CloudStack driver directly through the Provider.CLOUDSTACK
    constant.
- DNS:
  - Modify Zerigo driver to include record TTL in the record 'extra' attribute
    if a record has a TTL set.
  - Modify values in the Record 'extra' dictionary attribute in the Zerigo DNS
    driver to be set to None instead of an empty string ('') if a value for
    the provided key is not set.

* Thu Sep  5 2013 aboe76@gmail.com
- Updated to 0.13.1
- General Changes:
  - Fix a regression introduced in 0.13.0 and make sure to include
    Content-Length 0 with PUT and POST requests.
- Compute Changes:
  - Fix a bug in the ElasticHosts driver and check for right HTTP status
    code when determining drive imaging success.
  - Update Opsource driver to include node public ip address (if available).
- Storage Chagnes:
  - Fix a regression with calling encode_container_name instead of
    encode_object_name on object name in get_object method.
  - Ensure that AWS S3 multipart upload works for small iterators.

* Mon Jul  1 2013 aboe76@gmail.com
- Updated to 0.13.0
- General changes:
  - Add homebrew curl-ca-bundle path to CA_CERTS_PATH.
  - Modify OpenStackAuthConnection and change auth_token_expires attribute to
    be a datetime object instead of a string.
  - Modify OpenStackAuthConnection to support re-using of the existing auth
    token if it's still valid instead of re-authenticating on every
    authenticate() call.
  - Modify base Connection class to not send Content-Length header if body is
    not provided.
  - Add the new error class ProviderError and modify InvalidCredsError to
    inherit from it.
- compute changes:
  - Fix destroy_node method in the experimental libvirt driver.
  - Add ex_start_node method to the Joyent driver.
  - Fix Python 3 compatibility issue in the ScriptFileDeployment class.
  - Add ex_set_metadata_entry and ex_get_metadata method to the VCloud driver.
  - Various improvements and bug-fixes in the VCloud driver.
  - Add ex_set_metadata_entry and ex_get_metadata method to the VCloud driver.
  - Modify list_sizes method in the OpenStack driver to include
    OpenStackNodeSize object which includes 'vcpus' attribute which holds
    a number of virtual CPUs for this size.
  - For consistency rename "ex_describe_keypairs" method in the EC2 driver to
    "ex_describe_keypair".
  - Modify "ex_describe_keypair" method to return key fingerprint in the
    return value.
  - Populate private_ips attribute in the CloudStack drive when returning
    a Node object from the create_node method.
  - Allow user to pass extra arguments via "extra_args" argument which are
    then passed to the "deployVirtualMachine" call in the CloudStack driver
    create_node method.
  - Update Gandi driver to handle new billing model.
  - Fix a bug in the Linode driver and remove extra newline which is added
    when generating a random root password in create_node.
  - Add extension methods for managing keypairs to the CloudStack driver.
  - Add extension methods for managing security groups to the CloudStack
    driver.
  - Add extension methods for starting and stoping the node to the
    CloudStack driver.
  - Fix old _wait_until_running method.
  - Fix a bug in the GoGrid driver get_uuid method.
  - Various bug fixes and improvements in the HostVirtual driver.
  - Fix a bug with deploy_node not respecting 'timeout' kwarg.
  - Modify create_node method in CloudStack driver to return an instance of
    CloudStackNode and add a new "expunging" node state.
  - Update API endpoint hostnames in the ElasticHost driver and use hostnames
    which return a valid SSL certificate.
  - Add a driver for Rackspace's new datacenter in Sydney, Australia.
  - Add ex_list_networks method and missing tests for list_templates to the
    CloudStack driver.
  - Correctly throw InvalidCredsError if user passes invalid credentials to
    the DigitalOcean driver.
- storage changes:
  - Fix an issue with double encoding the container name in the CloudFiles
    driver upload_object method.
    Also properly encode container and object name used in the HTTP request
    in the get_container and get_object method.
- load balancer changes:
  - Add ex_list_current_usage method to the Rackspace driver.

* Tue May  7 2013 aboe76@gmail.com
- Updated to 0.12.4
- Fix a regression in Softlayer driver caused by the xmlrpclib changes.
- Allow user to pass alternate ssh usernames to deploy_node
- Fix a bug in EC2 list_locations method - 'name' attribute didn't contain a
  the right value.
- Add new ScriptFileDeployment deployment class which reads deploy script from
  file.
- Add support for API version 5.1 to the vCloud driver and accept any value
  which is a multiple of four for ex_vm_memory kwarg in create_node method.
- Fix a regression with removed ex_force_service_region constructor kwarg in
  the CloudFiles driver.

* Mon Apr 15 2013 aboe76@gmail.com
- Updated to 0.12.3
- Fix Python 3.x related regressions
- Fix a regression introduced with recent xmlrpiclib changes which broke all
  the Gandi.net drivers
- Improve deploy code to work correctly if the ssh user doesn't have access
  to the /root directory.
- Improve public and private IP address handling in OpenStack 1.1 driver.
- Add new driver for DigitalOcean provider
- Fix a regression in ParamikoSSHClient
- Allow user to specify 'priority' extra argument when creating a MX or SRV
  record.

* Tue Feb 19 2013 aboe76@gmail.com
- updated to 0.12.1
- Changes with Apache Libcloud 0.12.1:
  - Deprecate LazyList method of iteration over large paginated collections
    and use a new, more efficient generator based approach which doesn't
    require the iterator to be pre-exhausted and buffering all of the values
    in memory.
    Existing list_* methods which previously used LazyList class are
    preserving the old behavior and new iterate_* methods which use a new
    generator based approach have been added. (LIBCLOUD-254)
    [Mahendra M]
  - Replace old ENUM style provider constants and replace them with a string
    version.
    This change allows users to dynamically register new drivers using a new
    set_driver method. (LIBCLOUD-255)
    [Mahendra M]
  - Allow user to explicitly specify which CA file is used for verifying
    the server certificate by setting 'SSL_CERT_FILE' environment variable.
    Note: When this variable is specified, the specified path is the only
    CA file which is used to verifying the server certificate. (LIBCLOUD-283)
    [Tomaz Muraus, Erinn Looney-Triggs]
  - Add a common module (libcloud.common.xmlrpc) for handling XML-RPC
    requests using Libcloud http layer.
    Also refactor existing drivers which use xmlrpclib directly (VCL, Gandi,
    Softlayer) to use this module.
    This change allows drivers to support LIBCLOUD_DEBUG and SSL certificate
    validation functionality. Previously they have bypassed Libcloud http
    layer so this functionality was not available. (LIBCLOUD-288)
    [John Carr]
  - Fix string interpolation bug in __repr__ methods in the IBM SCE driver.
    (LIBCLOUD-242)
    [Tomaz Muraus]
  - Fix test failures which happened in Python 3.3 due to:
  - hash randomization
  - changes in xml.etree module
  - changes in xmlrpc module
    (LIBCLOUD-245)
    [Tomaz Muraus]
  - Improvements and additions in vCloud driver:
  - Expose generic query method (ex_query)
  - Provide functionality to get and set control access for vApps. This way
    created vApps can be shared between users/groups or everyone.
    (LIBCLOUD-251)
    [Michal Galet]
  - Update EC2 pricing data to reflect new, lower prices -
    http://aws.typepad.com/aws/2012/10/new-ec2-second-generation-standard-instances-and-price-reductions-1.html
    [Tomaz Muraus]
  - Update EC2 instance size to reflect new m3 instance types. Also refactor
    the code to make it easier to maintain.
    [Tomaz Muraus]
  - Add a new driver for HostVirtual (http://www.vr.org) provider.
    (LIBCLOUD-249)
    [Dinesh Bhoopathy]
  - Fix a bug where a numeric instead of a string value was used for the
    content-length header in VCloud driver. (LIBCLOUD-256)
    [Brian DeGeeter, Tomaz Muraus]
  - Add a new driver for new Asia Pacific (Sydney) EC2 region.
    [Tomaz Muraus]
  - Add support for managing security groups to the OpenStack driver. This
    patch adds the following extension methods:
  - ex_list_security_groups, ex_get_node_security_groups methods
  - ex_create_security_group, ex_delete_security_group
  - ex_create_security_group_rule, ex_delete_security_group_rule
    (LIBCLOUD-253)
    [L. Schaub]
  - Modify ElasticStack driver class to pass 'vnc auto' instead of
    'vnc:ip auto' argument to the API when creating a server.
    It looks like 'vnc:ip' has been replaced with 'vnc'.
    [Rick Copeland, Tomaz Muraus]
  - Add new EC2 instance type - High Storage Eight Extra Large Instance
    (hs1.8xlarge).
    [Tomaz Muraus]
  - Map 'shutting-down' node state in EC2 driver to UNKNOWN. Previously
    it was mapped to TERMINATED. (LIBCLOUD-280)
    Note: This change is backward incompatible which means you need to update
    your code if you rely on the old behavior.
    [Tomaz Muraus, Marcin Kuzminski]
  - Change _wait_until_running method so it supports waiting on multiple nodes
    and make it public (wait_until_running). (LIBCLOUD-274)
    [Nick Bailey]
  - Add new EC2 instance type - High Memory Cluster Eight Extra Large.
    (cr1.8xlarge).
    [Tomaz Muraus]
  - Add new driver for Abiquo provider - http://www.abiquo.com (LIBCLOUD-250).
    [Jaume Devesa]
  - Allow user to pass 'ex_blockdevicemappings' kwarg to the EC2 driver
    'create_node' method. (LIBCLOUD-282)
    [Joe Miller, Tomaz Muraus]
  - Improve error handling in the Brightbox driver.
    [Tomaz Muraus]
  - Fix the ScriptDeployment step to work correctly if user provides a
    relative path for the script argument. (LIBCLOUD-278)
    [Jaume Devesa]
  - Fix Softlayer driver and make sure all the code is up to date and works
    with the latest version of the actual Softlayer deployment (v3).
    (LIBCLOUD-287)
    [Kevin McDonald]
  - Update EC2 driver, m3 instance types are now available in all the regions
    except Brazil.
    Also update pricing to reflect new (decreased) prices.
    [Tomaz Muraus]
  - Minor improvements in the HostVirtual driver and add new ex_get_node and
    ex_build_node extension method. (LIBCLOUD-249)
    [Dinesh Bhoopathy]
  - Add ex_destroy_image method to IBM SCE driver. (LIBCLOUD-291)
    [Perry Zou]
  - Add the following new regions to the ElasticHosts driver: sjc-c, syd-v,
    hkg-e. (LIBCLOUD-293)
    [Tomaz Muraus]
  - Fix create_node in OpenStack driver to work correctly if 'adminPass'
    attribute is not present in the response.
    [Gavin McCance, Tomaz Muraus]
  - Allow users to filter images returned by the list_images method in the EC2
    driver by providing ex_image_ids argument. (LIBCLOUD-294)
    [Chris Psaltis, Joseph Hall]
  - Add support for OpenNebula 3.8. (LIBCLOUD-295)
    [Guillaume ZITTA]
  - Add a new local storage driver.
    (LIBCLOUD-252, LIBCLOUD-258, LIBCLOUD-265, LIBCLOUD-273)
    [Mahendra M]
  - Fix a bug which caused the connection to not be closed when using Python
    2.6 and calling get_object on an object which doesn't exist in the S3
    driver. (LIBCLOUD-257)
    [John Carr]
  - Add a new generator based method for listing / iterating over the
    containers (iterate_containers). (LIBCLOUD-261)
    [Mahendra M]
  - Add ex_purge_object_from_cdn method to the CloudFiles driver.
    (LIBCLOUD-267)
    [Tomaz Muraus]
  - Support for multipart uploads and other improvements in the S3 driver
    so it can more easily be re-used with other implementations (e.g. Google
    Storage, etc.).
    Also default to a multipart upload when using upload_object_via_stream.
    This methods is more efficient compared to old approach because it only
    requires buffering a single multipart chunk (5 MB) in memory.
    (LIBCLOUD-269)
    [Mahendra M]
  - Add new driver for Windows Azure Storage with support for block and page
    blobs. (LIBCLOUD-80)
    [Mahendra M]
  - Update 'if type' checks in the update_record methods to behave correctly
    if users passes in RecordType.A with a value of 0 - if type is not None.
    (LIBCLOUD-247)
    [Tomaz Muraus]
  - New driver for HostVirtual provider (www.vr.org). (LIBCLOUD-249)
    [Dinesh Bhoopathy]
  - Finish Amazon Route53 driver. (LIBCLOUD-132)
    [John Carr]
  - Add new driver for Gandi provider (https://www.gandi.net). (LIBCLOUD-281)
    [John Carr]
  - Add new driver for AWS Elastic Load Balancing service. (LIBCLOUD-169)
    [John Carr]

* Wed Jan 30 2013 aboe76@gmail.com
- Updated spec file copyright to Suse

* Mon Jan 28 2013 toddrme2178@gmail.com
- Cleanup spec file
- Fix rpmlint errors
- Rename package to match spec file

* Tue Jan 22 2013 aboe76@gmail.com
- initial upload version 0.11.4
