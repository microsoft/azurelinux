# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global min_osbuild_version 183
%global goipath         github.com/osbuild/image-builder

Version:        79.0.0

%gometa

%global common_description %{expand:
A local binary for building customized OS artifacts such as VM images and
OSTree commits. Uses osbuild under the hood.
}

Name:           image-builder
Release:        1%{?dist}
Summary:        An image building executable using osbuild
ExcludeArch:    i686

# Upstream license specification: Apache-2.0
# Others generated with:
#   $ go_vendor_license -C <UNPACKED ARCHIVE> report expression
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND CC-BY-SA-4.0 AND ISC AND MIT AND MPL-2.0 AND Unlicense

URL:            %{gourl}
Source0:        https://github.com/osbuild/image-builder/releases/download/v%{version}/image-builder-%{version}.tar.gz


BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires:  libvirt-devel
BuildRequires:  skopeo

# Build requirements of the `kerby/kerby` package
BuildRequires:  krb5-devel
# Build requirements of 'theproglottis/gpgme' package
BuildRequires:  gpgme-devel
BuildRequires:  libassuan-devel
# Build requirements of 'github.com/containers/storage' package
BuildRequires:  device-mapper-devel
BuildRequires:  libxcrypt-devel
%if 0%{?fedora}
# Build requirements of 'github.com/containers/storage' package
BuildRequires:  btrfs-progs-devel
# for _tmpfilesdir macro
BuildRequires:  systemd-rpm-macros
# DO NOT REMOVE the BUNDLE_START and BUNDLE_END markers as they are used by 'tools/rpm_spec_add_provides_bundle.sh' to generate the Provides: bundled list
# BUNDLE_START
Provides: bundled(golang(cel.dev/expr)) = 0.25.1
Provides: bundled(golang(cloud.google.com/go)) = 0.121.6
Provides: bundled(golang(cloud.google.com/go/auth)) = 0.16.5
Provides: bundled(golang(cloud.google.com/go/auth/oauth2adapt)) = 0.2.8
Provides: bundled(golang(cloud.google.com/go/compute)) = 1.45.0
Provides: bundled(golang(cloud.google.com/go/compute/metadata)) = 0.9.0
Provides: bundled(golang(cloud.google.com/go/iam)) = 1.5.2
Provides: bundled(golang(cloud.google.com/go/monitoring)) = 1.24.2
Provides: bundled(golang(cloud.google.com/go/storage)) = 1.56.1
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azcore)) = 1.21.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azidentity)) = 1.13.1
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/internal)) = 1.11.2
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/compute/armcompute/v5)) = 5.7.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/network/armnetwork/v7)) = 7.2.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/resources/armresources)) = 1.2.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/storage/armstorage)) = 1.8.1
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/storage/azblob)) = 1.6.4
Provides: bundled(golang(github.com/AzureAD/microsoft-authentication-library-for-go)) = 1.6.0
Provides: bundled(golang(github.com/BurntSushi/toml)) = 1.6.0
Provides: bundled(golang(github.com/GoogleCloudPlatform/opentelemetry-operations-go/detectors/gcp)) = 1.30.0
Provides: bundled(golang(github.com/GoogleCloudPlatform/opentelemetry-operations-go/exporter/metric)) = 0.53.0
Provides: bundled(golang(github.com/GoogleCloudPlatform/opentelemetry-operations-go/internal/resourcemapping)) = 0.53.0
Provides: bundled(golang(github.com/IBM/go-sdk-core/v5)) = 5.21.0
Provides: bundled(golang(github.com/IBM/ibm-cos-sdk-go)) = 1.12.3
Provides: bundled(golang(github.com/VividCortex/ewma)) = 1.2.0
Provides: bundled(golang(github.com/acarl005/stripansi)) = 5a71ef0
Provides: bundled(golang(github.com/asaskevich/govalidator)) = a9d515a
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2)) = 1.42.1
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream)) = 1.7.14
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/config)) = 1.32.29
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/credentials)) = 1.19.28
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/feature/ec2/imds)) = 1.18.30
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/feature/s3/transfermanager)) = 0.3.1
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/internal/configsources)) = 1.4.30
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/internal/endpoints/v2)) = 2.7.30
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/internal/v4a)) = 1.4.31
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/ec2)) = 1.316.0
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding)) = 1.13.13
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/checksum)) = 1.9.23
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/presigned-url)) = 1.13.30
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/s3shared)) = 1.19.31
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/s3)) = 1.105.0
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/signin)) = 1.4.0
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/sso)) = 1.32.0
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/ssooidc)) = 1.37.0
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/sts)) = 1.44.0
Provides: bundled(golang(github.com/aws/smithy-go)) = 1.27.3
Provides: bundled(golang(github.com/cespare/xxhash/v2)) = 2.3.0
Provides: bundled(golang(github.com/cheggaaa/pb/v3)) = 3.1.7
Provides: bundled(golang(github.com/cncf/xds/go)) = ee656c7
Provides: bundled(golang(github.com/containers/common)) = 0.64.2
Provides: bundled(golang(github.com/containers/image/v5)) = 5.36.2
Provides: bundled(golang(github.com/containers/libtrust)) = c1716e8
Provides: bundled(golang(github.com/containers/ocicrypt)) = 1.2.1
Provides: bundled(golang(github.com/containers/storage)) = 1.59.1
Provides: bundled(golang(github.com/coreos/go-semver)) = 0.3.1
Provides: bundled(golang(github.com/cpuguy83/go-md2man/v2)) = 2.0.6
Provides: bundled(golang(github.com/cyberphone/json-canonicalization)) = 19d51d7
Provides: bundled(golang(github.com/davecgh/go-spew)) = d8f796a
Provides: bundled(golang(github.com/distribution/reference)) = 0.6.0
Provides: bundled(golang(github.com/docker/distribution)) = 2.8.3+incompatible
Provides: bundled(golang(github.com/docker/docker)) = 28.3.2+incompatible
Provides: bundled(golang(github.com/docker/docker-credential-helpers)) = 0.9.3
Provides: bundled(golang(github.com/docker/go-connections)) = 0.5.0
Provides: bundled(golang(github.com/docker/go-units)) = 0.5.0
Provides: bundled(golang(github.com/dougm/pretty)) = add1dbc
Provides: bundled(golang(github.com/envoyproxy/go-control-plane/envoy)) = 1.36.0
Provides: bundled(golang(github.com/envoyproxy/protoc-gen-validate)) = 1.3.0
Provides: bundled(golang(github.com/fatih/color)) = 1.18.0
Provides: bundled(golang(github.com/felixge/httpsnoop)) = 1.0.4
Provides: bundled(golang(github.com/gabriel-vasile/mimetype)) = 1.4.8
Provides: bundled(golang(github.com/go-jose/go-jose/v4)) = 4.1.4
Provides: bundled(golang(github.com/go-logr/logr)) = 1.4.3
Provides: bundled(golang(github.com/go-logr/stdr)) = 1.2.2
Provides: bundled(golang(github.com/go-openapi/errors)) = 0.22.1
Provides: bundled(golang(github.com/go-openapi/strfmt)) = 0.23.0
Provides: bundled(golang(github.com/go-playground/locales)) = 0.14.1
Provides: bundled(golang(github.com/go-playground/universal-translator)) = 0.18.1
Provides: bundled(golang(github.com/go-playground/validator/v10)) = 10.26.0
Provides: bundled(golang(github.com/gobwas/glob)) = 0.2.3
Provides: bundled(golang(github.com/gocomply/scap)) = 0.1.3
Provides: bundled(golang(github.com/golang-jwt/jwt/v5)) = 5.3.0
Provides: bundled(golang(github.com/golang/protobuf)) = 1.5.4
Provides: bundled(golang(github.com/google/go-cmp)) = 0.7.0
Provides: bundled(golang(github.com/google/go-containerregistry)) = 0.20.3
Provides: bundled(golang(github.com/google/s2a-go)) = 0.1.9
Provides: bundled(golang(github.com/google/uuid)) = 1.6.0
Provides: bundled(golang(github.com/googleapis/enterprise-certificate-proxy)) = 0.3.6
Provides: bundled(golang(github.com/googleapis/gax-go/v2)) = 2.15.0
Provides: bundled(golang(github.com/gophercloud/gophercloud/v2)) = 2.10.0
Provides: bundled(golang(github.com/gorilla/mux)) = 1.8.1
Provides: bundled(golang(github.com/hashicorp/errwrap)) = 1.1.0
Provides: bundled(golang(github.com/hashicorp/go-cleanhttp)) = 0.5.2
Provides: bundled(golang(github.com/hashicorp/go-multierror)) = 1.1.1
Provides: bundled(golang(github.com/hashicorp/go-retryablehttp)) = 0.7.8
Provides: bundled(golang(github.com/hashicorp/go-version)) = 1.9.0
Provides: bundled(golang(github.com/inconshreveable/mousetrap)) = 1.1.0
Provides: bundled(golang(github.com/jmespath/go-jmespath)) = b0104c8
Provides: bundled(golang(github.com/json-iterator/go)) = 1.1.12
Provides: bundled(golang(github.com/klauspost/compress)) = 1.18.0
Provides: bundled(golang(github.com/klauspost/pgzip)) = 1.2.6
Provides: bundled(golang(github.com/kolo/xmlrpc)) = a4b6fa1
Provides: bundled(golang(github.com/kr/text)) = 0.2.0
Provides: bundled(golang(github.com/kylelemons/godebug)) = 1.1.0
Provides: bundled(golang(github.com/leodido/go-urn)) = 1.4.0
Provides: bundled(golang(github.com/letsencrypt/boulder)) = de9c061
Provides: bundled(golang(github.com/mattn/go-colorable)) = 0.1.14
Provides: bundled(golang(github.com/mattn/go-isatty)) = 0.0.22
Provides: bundled(golang(github.com/mattn/go-runewidth)) = 0.0.16
Provides: bundled(golang(github.com/mattn/go-sqlite3)) = 1.14.28
Provides: bundled(golang(github.com/miekg/pkcs11)) = 1.1.1
Provides: bundled(golang(github.com/mitchellh/mapstructure)) = 1.5.0
Provides: bundled(golang(github.com/moby/sys/capability)) = 0.4.0
Provides: bundled(golang(github.com/moby/sys/mountinfo)) = 0.7.2
Provides: bundled(golang(github.com/moby/sys/user)) = 0.4.0
Provides: bundled(golang(github.com/modern-go/concurrent)) = bacd9c7
Provides: bundled(golang(github.com/modern-go/reflect2)) = 1.0.2
Provides: bundled(golang(github.com/oklog/ulid)) = 1.3.1
Provides: bundled(golang(github.com/opencontainers/go-digest)) = 1.0.0
Provides: bundled(golang(github.com/opencontainers/image-spec)) = 1.1.1
Provides: bundled(golang(github.com/opencontainers/runtime-spec)) = 1.2.1
Provides: bundled(golang(github.com/oracle/oci-go-sdk/v54)) = 54.0.0
Provides: bundled(golang(github.com/osbuild/blueprint)) = 1.32.0
Provides: bundled(golang(github.com/pkg/browser)) = 5ac0b6a
Provides: bundled(golang(github.com/planetscale/vtprotobuf)) = 0393e58
Provides: bundled(golang(github.com/pmezard/go-difflib)) = 5d4384e
Provides: bundled(golang(github.com/proglottis/gpgme)) = 0.1.4
Provides: bundled(golang(github.com/rivo/uniseg)) = 0.4.7
Provides: bundled(golang(github.com/russross/blackfriday/v2)) = 2.1.0
Provides: bundled(golang(github.com/secure-systems-lab/go-securesystemslib)) = 0.9.0
Provides: bundled(golang(github.com/sigstore/fulcio)) = 1.6.6
Provides: bundled(golang(github.com/sigstore/protobuf-specs)) = 0.4.1
Provides: bundled(golang(github.com/sigstore/sigstore)) = 1.9.5
Provides: bundled(golang(github.com/sirupsen/logrus)) = 1.9.4
Provides: bundled(golang(github.com/smallstep/pkcs7)) = 0.1.1
Provides: bundled(golang(github.com/sony/gobreaker)) = dd874f9
Provides: bundled(golang(github.com/spf13/cobra)) = 1.10.2
Provides: bundled(golang(github.com/spf13/pflag)) = 1.0.10
Provides: bundled(golang(github.com/spiffe/go-spiffe/v2)) = 2.6.0
Provides: bundled(golang(github.com/stefanberger/go-pkcs11uri)) = 7828495
Provides: bundled(golang(github.com/stretchr/testify)) = 1.11.1
Provides: bundled(golang(github.com/supakeen/yamlplus)) = 1.1.0
Provides: bundled(golang(github.com/titanous/rocacheck)) = afe7314
Provides: bundled(golang(github.com/ubccr/kerby)) = 412be7b
Provides: bundled(golang(github.com/ulikunitz/xz)) = 0.5.15
Provides: bundled(golang(github.com/vbatts/tar-split)) = 0.12.1
Provides: bundled(golang(github.com/vbauerster/mpb/v8)) = 8.10.2
Provides: bundled(golang(github.com/vmware/govmomi)) = 0.52.0
Provides: bundled(golang(go.mongodb.org/mongo-driver)) = 1.17.2
Provides: bundled(golang(go.opentelemetry.io/auto/sdk)) = 1.2.1
Provides: bundled(golang(go.opentelemetry.io/contrib/detectors/gcp)) = 1.39.0
Provides: bundled(golang(go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc)) = 0.61.0
Provides: bundled(golang(go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp)) = 0.61.0
Provides: bundled(golang(go.opentelemetry.io/otel)) = 1.39.0
Provides: bundled(golang(go.opentelemetry.io/otel/metric)) = 1.39.0
Provides: bundled(golang(go.opentelemetry.io/otel/sdk)) = 1.39.0
Provides: bundled(golang(go.opentelemetry.io/otel/sdk/metric)) = 1.39.0
Provides: bundled(golang(go.opentelemetry.io/otel/trace)) = 1.39.0
Provides: bundled(golang(go.yaml.in/yaml/v2)) = 2.4.2
Provides: bundled(golang(go.yaml.in/yaml/v3)) = 3.0.4
Provides: bundled(golang(golang.org/x/crypto)) = 0.47.0
Provides: bundled(golang(golang.org/x/exp)) = 7d7fa50
Provides: bundled(golang(golang.org/x/mod)) = 0.31.0
Provides: bundled(golang(golang.org/x/net)) = 0.49.0
Provides: bundled(golang(golang.org/x/oauth2)) = 0.35.0
Provides: bundled(golang(golang.org/x/sync)) = 0.19.0
Provides: bundled(golang(golang.org/x/sys)) = 0.41.0
Provides: bundled(golang(golang.org/x/term)) = 0.40.0
Provides: bundled(golang(golang.org/x/text)) = 0.33.0
Provides: bundled(golang(golang.org/x/time)) = 0.12.0
Provides: bundled(golang(golang.org/x/tools)) = 0.40.0
Provides: bundled(golang(google.golang.org/api)) = 0.248.0
Provides: bundled(golang(google.golang.org/genproto)) = 513f239
Provides: bundled(golang(google.golang.org/genproto/googleapis/api)) = ff82c1b
Provides: bundled(golang(google.golang.org/genproto/googleapis/rpc)) = ff82c1b
Provides: bundled(golang(google.golang.org/grpc)) = 1.79.3
Provides: bundled(golang(google.golang.org/protobuf)) = 1.36.10
Provides: bundled(golang(gopkg.in/ini.v1)) = 1.67.3
Provides: bundled(golang(gopkg.in/yaml.v3)) = 3.0.1
Provides: bundled(golang(libvirt.org/go/libvirt)) = 1.12005.0
Provides: bundled(golang(sigs.k8s.io/yaml)) = 1.6.0
# BUNDLE_END
%endif

Requires:   osbuild >= %{min_osbuild_version}
Requires:   osbuild-ostree >= %{min_osbuild_version}
Requires:   osbuild-lvm2 >= %{min_osbuild_version}
Requires:   osbuild-luks2 >= %{min_osbuild_version}
Requires:   osbuild-depsolve-dnf >= %{min_osbuild_version}

%description
%{common_description}

%prep
%if 0%{?rhel}
%forgeautosetup -p1
%else
%goprep -k
%endif

%build
export GOFLAGS="-buildmode=pie"
%if 0%{?rhel}
GO_BUILD_PATH=$PWD/_build
install -m 0755 -vd $(dirname $GO_BUILD_PATH/src/%{goipath})
ln -fs $PWD $GO_BUILD_PATH/src/%{goipath}
cd $GO_BUILD_PATH/src/%{goipath}
install -m 0755 -vd _bin
export PATH=$PWD/_bin${PATH:+:$PATH}
export GOPATH=$GO_BUILD_PATH:%{gopath}
export GOFLAGS+=" -mod=vendor"
%endif

%if 0%{?fedora}
# Fedora disables Go modules by default, but we want to use them.
# Undefine the macro which disables it to use the default behavior.
%undefine gomodulesmode
%endif

# btrfs-progs-devel is not available on RHEL
%if 0%{?rhel}
GOTAGS="exclude_graphdriver_btrfs"
%endif

export LDFLAGS="${LDFLAGS} -X 'main.version=%{version}'"
%gobuild ${GOTAGS:+-tags=$GOTAGS} -o _bin/image-builder %{goipath}/cmd/image-builder

# Generate man pages
mkdir -p man/man1
_bin/image-builder doc man/man1/

%install
install -m 0755 -vd                                 %{buildroot}%{_bindir}
install -m 0755 -vp _bin/image-builder              %{buildroot}%{_bindir}/
# tmpfiles.d snippet
install -m 0755 -vd                                 %{buildroot}%{_tmpfilesdir}
install -m 0644 -vp data/tmpfiles.d/image-builder.conf %{buildroot}%{_tmpfilesdir}/image-builder.conf
install -m 0755 -vd                                 %{buildroot}%{_mandir}/man1
install -m 0644 -vp man/man1/image-builder*.1       %{buildroot}%{_mandir}/man1/
%check
export GOFLAGS="-buildmode=pie"
%if 0%{?rhel}
export GOFLAGS+=" -mod=vendor -tags=exclude_graphdriver_btrfs"
export GOPATH=$PWD/_build:%{gopath}
# cd inside GOPATH, otherwise go with GO111MODULE=off ignores vendor directory
cd $PWD/_build/src/%{goipath}
%gotest ./...
%else
%gocheck
%endif

%files
%license LICENSE
%doc README.md
%{_bindir}/image-builder
%{_tmpfilesdir}/image-builder.conf
%{_mandir}/man1/image-builder*.1*
%ghost %attr(0755, root, root) %dir /var/cache/image-builder

%changelog
* Thu Aug 20 2026 Packit <hello@packit.dev> - 79.0.0-1
Changes with 79.0.0
----------------
  - Fix the container resolver tests (#2602)
    - Author: Achilleas Koutsou, Reviewers: Florian Schüller, Sanne Raymaekers
  - Run privileged unit tests on gitlab (#2603)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Simon de Vlieger
  - Start container with repos support for legacy ISO only [HMS-11156] (#2582)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Simon de Vlieger
  - Update osbuild dependency commit ID (#2600)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Anna Vítová
  - Update snapshots to 20260816 (#2599)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Anna Vítová
  - anaconda_installer: platform build packages (#2589)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Sanne Raymaekers
  - distrodefs: Add aliases to Fedora for GCP (HMS-11182) (#2583)
    - Author: Tomáš Koscielniak, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - fedora: drop explicit `anaconda-widgets` (#2597)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Katerina Koukiou, Lukáš Zapletal
  - image-builder: reuse progress bars for upload (#2592)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Lukáš Zapletal, Simon de Vlieger
  - manifest: accept human-readable image sizes (#2571)
    - Author: tomatotomata, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - osbuild/rpm: implement generic env   (#2586)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Anna Vítová
  - ova: set os type and virtual hardware version (HMS-3248) (#2480)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - packit: enable riscv64 (#2595)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  - pkg/disk.yaml: add an option to not grow root (#2524)
    - Author: Jean-Baptiste Trystram, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - test: add GPG keys to Fedora 44 test repos (#2585)
    - Author: Achilleas Koutsou, Reviewers: Anna Vítová, Simon de Vlieger
  - test: mock host arch for package search (#2594)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal

— Somewhere on the Internet, 2026-08-20

* Mon Aug 10 2026 Packit <hello@packit.dev> - 78.0.0-1
Changes with 78.0.0
----------------
  - Simplify early manifest generation code and enable custom seeds for bootc-based images (#2565)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Simon de Vlieger
  - Update RHEL 9, 10 OCI image defs to add Oracle as cloud init datasource (#2559)
    - Author: src-up, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Update osbuild dependency commit ID (#2576)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Anna Vítová
  - Update snapshots to 20260719 (#2530)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Anna Vítová
  - ci: tag containers (#2575)
    - Author: Simon de Vlieger, Reviewers: Anna Vítová, Brian C. Lane
  - cmd/image-builder: drop `images` from version (#2573)
    - Author: Simon de Vlieger, Reviewers: Anna Vítová, Brian C. Lane
  - container: add SetAuthFilePath method to Resolver (#2580)
    - Author: Ondřej Budai, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - disk: align footer to grain by default (#2562)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Anna Vítová
  - disk: take the ESP size from the image type's partition table (RHEL-214147) (#2552)
    - Author: Lucas Garfield, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - distro/generic: pass subscription options to pxe-tar-xz images (HMS-11108) (#2564)
    - Author: Lucas Garfield, Reviewers: Achilleas Koutsou, Brian C. Lane
  - fedora: create 46 (#2546)
    - Author: Simon de Vlieger, Reviewers: Anna Vítová, Florian Schüller
  - imgtestlib: configure setuptools package discovery (#2563)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - test/imgtestlib: revert boot.py to old behaviour (#2579)
    - Author: Anna Vítová, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - test: remove iot-bootable-container image type (#2569)
    - Author: Anna Vítová, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2026-08-10

* Tue Jul 28 2026 Packit <hello@packit.dev> - 77.0.0-1
Changes with 77.0.0
----------------
  - Generate bootc-image-builder test jobs dynamically and enable all tests [HMS-11073] (#2539)
    - Author: Achilleas Koutsou, Reviewers: Anna Vítová, Simon de Vlieger
  - Refactor CLI setup (#2503)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Simon de Vlieger
  - Update osbuild dependency commit ID (#2555)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Anna Vítová
  - anaconda: rectify comment (#2548)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Anna Vítová, Lukáš Zapletal
  - bib: Replace logrus usage with olog (#2543)
    - Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - bib_legacy: Use functions from bootc (#2540)
    - Author: Brian C. Lane, Reviewers: Anna Vítová, Lukáš Zapletal, Simon de Vlieger
  - build(deps): bump actions/setup-python from 6 to 7 (#2556)
    - Author: dependabot, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - eln: enable `aarch64` for `gce` (HMS-11095) (#2558)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Brian C. Lane
  - github: enable building the bootc-image-builder container [HMS-11005] (#2549)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Simon de Vlieger
  - gitlab: remove setup-show option for pytest (#2551)
    - Author: Achilleas Koutsou, Reviewers: Anna Vítová, Brian C. Lane
  - manifest/raw_bootc: support subscription registration on first boot (HMS-10897) (#2528)
    - Author: Lucas Garfield, Reviewers: Brian C. Lane, Simon de Vlieger
  - pkg/koji/upload: session credentials to headers (#2550)
    - Author: Anna Vítová, Reviewers: Florian Schüller, Sanne Raymaekers

— Somewhere on the Internet, 2026-07-28

* Wed Jul 22 2026 Packit <hello@packit.dev> - 76.0.0-1
Changes with 76.0.0
----------------
  - Restore anaconda-iso/iso type to bootc-image-builder (#2527)
    - Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Update osbuild dependency commit ID (#2531)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Anna Vítová
  - anaconda: enable shell shenanigans for anaconda (#2544)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  - build(deps): bump actions/setup-go from 6 to 7 (#2532)
    - Author: dependabot, Reviewers: Achilleas Koutsou, Anna Vítová
  - eln: set runner to eln11 (#2535)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Anna Vítová
  - image-builder: distro detection for `build` and `manifest` (#2542)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Ondřej Budai

— Somewhere on the Internet, 2026-07-22

* Tue Jul 21 2026 Packit <hello@packit.dev> - 75.0.0-1
Changes with 75.0.0
----------------
  - Add hidden pkgsearch subcommand for querying available packages (HMS-11011) (#2515)
    - Author: Gianluca Zuccarelli, Reviewers: Sanne Raymaekers, Simon de Vlieger
  - Always use seed argument directly (#2516)
    - Author: Achilleas Koutsou, Reviewers: Sanne Raymaekers, Simon de Vlieger
  - Enable basic bootc-image-builder tests [HMS-10851] (#2467)
    - Author: Achilleas Koutsou, Reviewers: Anna Vítová, Tomáš Koscielniak
  - Enable image-builder container builds [HMS-10851] (#2497)
    - Author: Achilleas Koutsou, Reviewers: Florian Schüller, Simon de Vlieger
  - Fedora ISO Modernization (HMS-9965) (#2533)
    - Author: Simon de Vlieger, Reviewers: Anna Vítová, Sanne Raymaekers
  - Improve error message for pkgsearch with no packages (#2526)
    - Author: Gianluca Zuccarelli, Reviewers: Brian C. Lane, Lucas Garfield
  - README: update deprecated information in docs (#2498)
    - Author: Anna Vítová, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Run more bootc-image-builder tests in gitlab [HMS-10854] (#2520)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Tomáš Hozza
  - Update dependencies 2026-07-12 (#2513)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Anna Vítová
  - Update osbuild dependency commit ID (#2512)
    - Author: SchutzBot, Reviewers: Anna Vítová, Simon de Vlieger
  - Update snapshots to 20260705 (#2488)
    - Author: SchutzBot, Reviewers: Anna Vítová, Simon de Vlieger
  - bootc: support grub2 serial console customization (#2403)
    - Author: Jean-Baptiste Trystram, Reviewers: Brian C. Lane, Joel Capitao, Tomáš Hozza
  - build(deps): bump actions/checkout from 6 to 7 (#2452)
    - Author: dependabot, Reviewers: Anna Vítová, Simon de Vlieger
  - ci: enable allow-unsafe-pr-checkout in checkout/7 (#2523)
    - Author: Anna Vítová, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  - cmd/image-builder: mock simple integration tests (HMS-10857) (#2473)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Anna Vítová
  - disk: systemd-repart compatibility (#2510)
    - Author: Simon de Vlieger, Reviewers: Anna Vítová, Brian C. Lane
  - fedora: drop slirp4netns from the IoT image (#2478)
    - Author: Peter Robinson, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - image-builder: add hidden `--with-upload-result` option (#2521)
    - Author: Sanne Raymaekers, Reviewers: Brian C. Lane, Tomáš Hozza
  - pkg/disk: add XFS agcount option in `disk.yaml` (#2496)
    - Author: Jean-Baptiste Trystram, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - progress: add file progress (HMS-10977) (#2493)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Anna Vítová, Simon de Vlieger
  - test: fix build info cache path creation to use correct runner_distro (#2495)
    - Author: Achilleas Koutsou, Reviewers: Sanne Raymaekers, Simon de Vlieger
  - test: fix vm.py import error [HMS-11012] (#2522)
    - Author: Anna Vítová, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - test: go 1.27 compatibility (#2504)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Anna Vítová
  - test: mock cache dir (#2519)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Anna Vítová

— Somewhere on the Internet, 2026-07-21

* Wed Jul 08 2026 Packit <hello@packit.dev> - 74.0.0-1
Changes with 74.0.0
----------------
  - Test depsolvednf with dnf5 [HMS-10324] (#2475)
    - Author: Achilleas Koutsou, Reviewers: Simon de Vlieger, Tomáš Hozza
  - Update dependencies 2026-06-28 (#2472)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Update dependencies 2026-07-05 (#2490)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - depsolvednf: don't require solver.json in test (#2479)
    - Author: Achilleas Koutsou, Reviewers: Anna Vítová, Brian C. Lane
  - distro/eln: use dnf5 and update package lists (#2482)
    - Author: Yaakov Selkowitz, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - gen-manifest: optimize checksum calculation (#2382)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Tomáš Hozza
  - generic/bootc: allow disk.yaml to provide root filesystem type (#2405)
    - Author: Joel Capitao, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - github: remove osbuild-composer reverse dependency test (#2477)
    - Author: Achilleas Koutsou, Reviewers: Simon de Vlieger, Tomáš Hozza
  - image-builder/build: add json format option (#2484)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - manifest: add firstboot support (HMS-9187) (#1913)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Simon de Vlieger
  - many: plumb sdboot options (#2456)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Brian C. Lane
  - many: use `image-builder upload` in tests (HMS-10856) (#2476)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Brian C. Lane
  - partition_table: Make AlignUp clearer (#2419)
    - Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - pkg/rhsm: match subscription baseurls with wildcards (RHEL-36789) (#2460)
    - Author: Lucas Garfield, Reviewers: Achilleas Koutsou, Brian C. Lane, Lukáš Zapletal
  - progress: lock around sub progress (#2487)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  - workflows: Add a link to the osbuild-composer API unit test results (#2469)
    - Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - workflows: Update old images urls to image-builder (#2468)
    - Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2026-07-08

* Mon Jun 29 2026 Packit <hello@packit.dev> - 73.0.0-1
Changes with 73.0.0
----------------
  - Update dependencies 2026-06-21 (#2451)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - Update osbuild dependency commit ID (#2450)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - disk: check all partitions for boot partition requirement (#2459)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - github: drop the reverse dependency check with image-builder-cli (#2454)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Simon de Vlieger
  - imgtestlib: handle missing sources key in tests (#2447)
    - Author: Anna Vítová, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - osbuild: ddi mount (#2457)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - rhel-10: reintroduce minimal-raw-xz (#2465)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal

— Somewhere on the Internet, 2026-06-29

* Wed Jun 17 2026 Packit <hello@packit.dev> - 69-1
Changes with 69
----------------
  - deps: bump osbuild/images dependency (#548)
    - Author: SchutzBot, Reviewers: Nobody
  - deps: bump osbuild/images dependency (#551)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - deps: bump osbuild/images dependency (#552)
    - Author: SchutzBot, Reviewers: Simon de Vlieger
  - deps: images 0.273.0 (#549)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli, Lucas Garfield
  - main: `system` subcommand (#537)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Brian C. Lane

osbuild/images changes (v0.270.0 -> v0.274.0):

  - Add BootcRootFS pipeline and use it for bootc pxe-tar-xz (#2361)
    - Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Add Custom menus to X86 and PPC64 ISO bootloaders (#2394)
    - Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Test: stop testing EOL RHEL releases (#2415)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  - Update dependencies 2026-05-31 (#2391)
    - Author: SchutzBot, Reviewers: Anna Vítová, Lukáš Zapletal, Simon de Vlieger
  - Update dependencies 2026-06-07 (#2402)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Anna Vítová, Simon de Vlieger
  - config-list: narrow down the matrix (#2366)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - data/repositories: add PQC keys to rolling distros (#2411)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - deps: drop `golang.org/x/exp/slices` (#2399)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  - distro/eln: clean up part 1 (HMS-10764) (#2384)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - distro/eln: installers use erofs (HMS-10634) (#2398)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Brian C. Lane
  - fedora-42: eol (#2385)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Brian C. Lane
  - imgtestlib: support bootc-foundry image types (#2393)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - manifest: use boot root for fix bls (#2412)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli
  - many: copy boot files from build (#2410)
    - Author: Simon de Vlieger, Reviewers: Anna Vítová, Brian C. Lane
  - many: initial `systemd-boot` support (#2392)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - oscap: drop dead code (#2409)
    - Author: Simon de Vlieger, Reviewers: Gianluca Zuccarelli, Lukáš Zapletal
  - test/imgtestlib: boot test network installer on RHEL 10.2 (#2387)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Ondřej Budai, Tomáš Hozza

— Somewhere on the Internet, 2026-06-17

* Thu Jun 04 2026 Packit <hello@packit.dev> - 68-1
Changes with 68
----------------
  - Containerfile*: correct base image reference in tag (#531)
    - Author: Zephyr Lykos, Reviewers: Brian C. Lane, Tomáš Hozza
  - deps: bump osbuild/images dependency (#533)
    - Author: SchutzBot, Reviewers: Brian C. Lane, Simon de Vlieger
  - deps: bump osbuild/images dependency (#538)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - doc: mention additional requirements (#530)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - main: `--force-defs-dir` (#534)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - main: `bootc inspect` (#529)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - pr-best-practices: Update authentication scheme for Jira Cloud (HMS-10749) (#535)
    - Author: Florian Schüller, Reviewers: Lukáš Zapletal, Simon de Vlieger

osbuild/images changes (v0.267.0 -> v0.270.0):

  - Break down imgtestlib module and  use log sections (#2383)
    - Author: Achilleas Koutsou, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - CI: run tests on Fedora 44 (#2343)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Simon de Vlieger
  - Make EFIPartitionTable function public, move it into disk (#2354)
    - Author: Brian C. Lane, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - Repos: Add/update AlmaLinux repository definitions (#2376)
    - Author: Eduard Abdullin, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Update dependencies 2026-05-25 (#2368)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - bootc: assert non-nil kernel info (#2370)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal, Tomáš Hozza
  - cicd: run gobump per commit (#2352)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Simon de Vlieger
  - container: guess at mime type (#2372)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Lukáš Zapletal, Tomáš Hozza
  - depsolver: catch all errors from the child process (#2365)
    - Author: Ondřej Budai, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - distro/loader: expand installerConfig template by copying (HMS-10718) (#2373)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Lukáš Zapletal
  - distro: Make isoCustomizations usable by bootcImageType (#2360)
    - Author: Brian C. Lane, Reviewers: Simon de Vlieger, Tomáš Hozza
  - fedora: drop no_timer_check leftover (#2282)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Simon de Vlieger
  - gitlab: exit with error code when manifests fail to validate (#2374)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Lukáš Zapletal
  - install-dependencies: Add a note about it being used by image-builder-cli workflows (#2353)
    - Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger, Tomáš Hozza
  - loader: allow custom path (#2378)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Tomáš Hozza
  - many: fix non-determistic manifest generation (#2381)
    - Author: Ondřej Budai, Reviewers: Achilleas Koutsou, Simon de Vlieger, Tomáš Hozza
  - pr-best-practices: Update authentication scheme for Jira Cloud (HMS-10749) (#2386)
    - Author: Florian Schüller, Reviewers: Brian C. Lane, Lukáš Zapletal
  - stage/grub2: allow VFAT for boot fs (#2371)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Tomáš Hozza

— Somewhere on the Internet, 2026-06-04

* Mon May 25 2026 Packit <hello@packit.dev> - 66-1
Changes with 66
----------------
  - cmd: introduce profiling options (#516)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Simon de Vlieger
  - deps: bump osbuild/images dependency (#524)
    - Author: SchutzBot, Reviewers: Simon de Vlieger, Tomáš Hozza
  - packit: enable ELN (HMS-10701) (#521)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Tomáš Hozza

osbuild/images changes (v0.266.0 -> v0.267.0):

  - Add osbuild stages for mounting erofs and squashfs compressed filesystems (#2348)
    - Author: Brian C. Lane, Reviewers: Simon de Vlieger, Tomáš Hozza
  - arch: map OCI platform architecture to GOARCH (#2315)
    - Author: Zephyr Lykos, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - bootloaders: Move the iso bootloader setup into its own struct (#2347)
    - Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - container: resolve containers using skopeo [RHEL-56367] (#2346)
    - Author: Achilleas Koutsou, Reviewers: Gianluca Zuccarelli, Tomáš Hozza
  - fedora: Update IoT arm images with newer RPi dtbs (#2358)
    - Author: Peter Robinson, Reviewers: Achilleas Koutsou, Simon de Vlieger, Tomáš Koscielniak
  - many: upgrade deps with deprecated APIs (HMS-10702) (#2356)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2026-05-25

* Thu May 21 2026 Packit <hello@packit.dev> - 65-1
Changes with 65
----------------
  - deps: bump images to 0.266.0 (#520)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Tomáš Hozza
  - deps: bump osbuild/images dependency (#515)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - main: default to XDG cache directory for non-root users (#511)
    - Author: Guillermo N. Leiro Arroyo, Reviewers: Brian C. Lane, Lukáš Zapletal

osbuild/images changes (v0.262.0 -> v0.266.0):

  - Add bootc-foundry boot test infrastructure (HMS-10336) (#2335)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - Update RHEL 9 and 10 OCI image definitions [HMS-10328, HMS-10472] (#2333)
    - Author: Achilleas Koutsou, Reviewers: Simon Steinbeiß, Simon de Vlieger
  - Update osbuild dependency commit ID (#2321)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - Update osbuild dependency commit ID (#2328)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Update snapshots to 20260504 (#2323)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - boot-azure: switch machine type (#2344)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Sanne Raymaekers, Simon Steinbeiß
  - ci: include flatpaks (#2349)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Tomáš Hozza
  - ci: use f43 for cross-arch (#2322)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - defs/bootc: set XBOOTLDR GUID (#2325)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Tomáš Hozza
  - disk: partition table policies (#2330)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - distro/rhel-9: fix OCI partitioning (#2351)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Simon de Vlieger, Tomáš Hozza
  - experimental: use yamlplus (#2319)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - fedora: remove vc4 module blacklist from ostree kernel options (#2331)
    - Author: Paul Whalen, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - flatpak: use container resolver to resolve flatpak refs (#2334)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - import ELN (HMS-10620, HMS-10621, HMS-10623) (#2318)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - many: bootc sealed images (composefs, and bootloader) (HMS-10628) (#2326)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - pkg/bootc/resolver: handle missing 'bootc container inspect' (#2342)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - rhel: enable sshd service for WSL images (#2332)
    - Author: Simon Steinbeiß, Reviewers: Achilleas Koutsou, Sanne Raymaekers, Simon de Vlieger
  - schutzbot: update terraform commit ID (#2341)
    - Author: Achilleas Koutsou, Reviewers: Anna Vítová, Brian C. Lane
  - test: close filesystem/disk customization coverage gaps with osbuild-composer (#2329)
    - Author: Simon Steinbeiß, Reviewers: Achilleas Koutsou, Lukáš Zapletal, Simon de Vlieger

— Somewhere on the Internet, 2026-05-21

* Wed May 13 2026 Packit <hello@packit.dev> - 64-1
Changes with 64
----------------
  - cmd: drop "bootc is experimental" (#510)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - deps: bump osbuild/images dependency (#507)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - deps: update dependencies (w/o osbuild/images) (#508)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - doc: fix broken link (#509)
    - Author: Simon de Vlieger, Reviewers: Anna Vítová, Lukáš Zapletal
  - doc: introduce advanced bootc (#462)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Tomáš Hozza
  - docs: generate manpages (#504)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - main: hide `--use-librepo` (#513)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Tomáš Hozza
  - main: hide `--with-rpmlist` (#512)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Tomáš Hozza

— Somewhere on the Internet, 2026-05-13

* Wed Apr 29 2026 Packit <hello@packit.dev> - 63-1
Changes with 63
----------------
  - deps: bump images to 0.259.0 (#501)
    - Author: Anna Vítová, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - docs: update satellite info (#503)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Tomáš Hozza
  - main: `--version` -> `version` subcommand (#505)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - many: Generate rpmlist as an output of manifestgen (#502)
    - Author: Anna Vítová, Reviewers: Lukáš Zapletal, Simon de Vlieger

— Somewhere on the Internet, 2026-04-29

* Tue Apr 14 2026 Packit <hello@packit.dev> - 60-1
Changes with 60
----------------
  - Support --in-vm in image-builder (#485)
    - Author: Anna Vítová, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - deps: bump images to 0.258.0 (#495)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Anna Vítová

— Somewhere on the Internet, 2026-04-14

* Tue Apr 07 2026 Packit <hello@packit.dev> - 58-1
Changes with 58
----------------
  - deps: bump images to 0.256.0 (#491)
    - Author: Simon de Vlieger, Reviewers: Anna Vítová, Lukáš Zapletal

— Somewhere on the Internet, 2026-04-07

* Mon Apr 06 2026 Packit <hello@packit.dev> - 57-1
Changes with 57
----------------
  - deps: update `images` to 0.254.0 (#489)
    - Author: Simon de Vlieger, Reviewers: Anna Vítová, Lukáš Zapletal

— Somewhere on the Internet, 2026-04-06


* Tue Mar 24 2026 Packit <hello@packit.dev> - 55-1
Changes with 55
----------------
  - chore: bump dependencies via gobump (#460)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal
  - deps: bump images (#483)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Anna Vítová

— Somewhere on the Internet, 2026-03-24


* Fri Mar 13 2026 Packit <hello@packit.dev> - 53-1
Changes with 53
----------------
  - chore: bump dependencies via gobump (#475)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - cmd: allow specifying AWS credentials profile (#443)
    - Author: Jakub Kadlčík, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - deps: bump images to 0.248.0 (#479)
    - Author: Simon de Vlieger, Reviewers: Nobody
  - docs: update COPR command for RHEL (#477)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Simon de Vlieger
  - test: bump ISO timeout (#469)
    - Author: Lukáš Zapletal, Reviewers: Simon de Vlieger, Tomáš Hozza

— Somewhere on the Internet, 2026-03-13


* Thu Feb 19 2026 Packit <hello@packit.dev> - 51-1
Changes with 51
----------------
  - go.mod: update osbuild/images to v0.243.0 (#457)
    - Author: Achilleas Koutsou, Reviewers: Lukáš Zapletal, Simon de Vlieger

— Somewhere on the Internet, 2026-02-19


* Tue Feb 17 2026 Packit <hello@packit.dev> - 50-1
Changes with 50
----------------
  - SPEC: define default permissions for /var/cache/image-builder (#454)
    - Author: Tomáš Hozza, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - build(deps): bump actions/cache from 4 to 5 (#434)
    - Author: {}, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - deps: bump Go to 1.24.12 and use new Go functions (#452)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - go.mod: update osbuild/images to v0.240.0 (#456)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2026-02-17


* Wed Feb 04 2026 Packit <hello@packit.dev> - 48-1
Changes with 48
----------------
  - Add pxe-tar-xz to bib types and add boot tests for f43, stream9, and stream10 (#436)
    - Author: Brian C. Lane, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - Support rootless bootc-image-builder (#445)
    - Author: Alexander Larsson, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - chore: fix constant format string (#438)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - tests: Fix bootc pxe testing (#439)
    - Author: Brian C. Lane, Reviewers: Simon de Vlieger

— Somewhere on the Internet, 2026-02-04


* Fri Jan 16 2026 Packit <hello@packit.dev> - 47-1
Changes with 47
----------------
  - Revert "spec: Use gosource macro for Source0" (#433)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Tomáš Hozza

— Somewhere on the Internet, 2026-01-16


* Mon Jan 05 2026 Packit <hello@packit.dev> - 45-1
Changes with 45
----------------
  - deps: bump images to 0.231.0 (#425)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Lukáš Zapletal

— Somewhere on the Internet, 2026-01-05


* Wed Dec 24 2025 Packit <hello@packit.dev> - 44-1
Changes with 44
----------------
  - [RFC] main: print pretty json manifest (#414)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - bib: document details about  {,bib}cmd{ManifestFromCobra,Build} (#402)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - bib: fix anaconda-iso mTLS key extraction (#404)
    - Author: Michael Vogt, Reviewers: Brian C. Lane, Ondřej Budai
  - bib: small cleanups (#400)
    - Author: Michael Vogt, Reviewers: Simon de Vlieger, Tomáš Hozza
  - cmd: move `awscloudNewUploader` back into upload.go (#397)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - cmd: remove bibupload as it was never exposed to the public (#405)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - data: install tmpfiles.d/image-builder.conf to auto-clean cache (#418)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - main: error when image-builder is used to create anaconda-iso (#401)
    - Author: Michael Vogt, Reviewers: Brian C. Lane, Lukáš Zapletal
  - test: add rhel specific tests (#403)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Tomáš Hozza

— Somewhere on the Internet, 2025-12-24


* Wed Dec 10 2025 Packit <hello@packit.dev> - 43-1
Changes with 43
----------------
  - Containerfile: add subscription-manager (#390)
    - Author: Michael Vogt, Reviewers: Ondřej Budai, Simon de Vlieger
  - bib: drop inContainerOrUnknown() and use setup.IsContainer() (#395)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - chore: bump dependencies via gobump (#389)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - chore: bump dependencies via gobump (#394)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - cmd: make bootc-image-builder a multi-call binary of ibcli (HMS-9808) (#374)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Lukáš Zapletal, Simon de Vlieger, Tomáš Hozza
  - cmd: move the "upload" comand from bib here (#396)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Tomáš Hozza
  - deps: update images to 0.228.0 (#393)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Michael Vogt
  - docs: add a note about satellite (#385)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Simon de Vlieger
  - go.mod: move to images v0.226.0 (#384)
    - Author: Michael Vogt, Reviewers: Anna Vítová, Simon de Vlieger
  - main: add `{supported,required}` bp options to describe-image (#376)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - main: rename `data-dir` to `force-data-dir` (#386)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal
  - readme: new `--force-data-dir` (#387)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Michael Vogt
  - repos: force data is an override (#388)
    - Author: Simon de Vlieger, Reviewers: Michael Vogt, Tomáš Hozza
  - test: add test for subscribed content (#391)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Simon de Vlieger

— Somewhere on the Internet, 2025-12-10


* Wed Nov 26 2025 Packit <hello@packit.dev> - 42-1
Changes with 42
----------------
  - Fix release action (#368)
    - Author: Simon Steinbeiß, Reviewers: Achilleas Koutsou, Lukáš Zapletal, Michael Vogt
  - build(deps): bump actions/checkout from 5 to 6 (#381)
    - Author: dependabot[bot], Reviewers: Lukáš Zapletal, Simon de Vlieger
  - chore: bump dependencies via gobump (#382)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - ci: split gobump into two PRs (#371)
    - Author: Lukáš Zapletal, Reviewers: Michael Vogt, Simon de Vlieger
  - cmd: modify success message to include image path (#377)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Michael Vogt
  - doc/installation: mention RHEL 9.7 and 10.1 (#378)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Lukáš Zapletal, Tomáš Hozza
  - doc: additional information on `ostree` (HMS-9741) (#373)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Michael Vogt
  - doc: document `bootc` specifics (HMS-9740) (#375)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Michael Vogt, Tomáš Hozza
  - github: disable gomod updates with dependabot (#372)
    - Author: Achilleas Koutsou, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - go.mod: move to images v0.218 (#370)
    - Author: Michael Vogt, Reviewers: Sanne Raymaekers, Simon de Vlieger
  - go.mod: move to images v0.223 (#383)
    - Author: Ondřej Budai, Reviewers: Michael Vogt, Simon de Vlieger
  - main: add `--bootc-defaultfs` option (#324)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Lukáš Zapletal, Simon de Vlieger
  - many: metrics option for stage durations (#317)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2025-11-26


* Wed Nov 12 2025 Packit <hello@packit.dev> - 41-1
Changes with 41
----------------
  - Drop the need for --privileged for all subcommands except `build` (#361)
    - Author: Ondřej Budai, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - ci: add gobump action (#365)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger, Tomáš Hozza
  - main: add `--rpmmd-cache` options [HMS-9646] (#358)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - main: fix missing append of `repositories` when using --data-dirs (#360)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Brian C. Lane
  - many: update all refs to Fedora 43 (#362)
    - Author: Ondřej Budai, Reviewers: Achilleas Koutsou, Michael Vogt, Simon de Vlieger

— Somewhere on the Internet, 2025-11-12


* Wed Oct 29 2025 Packit <hello@packit.dev> - 40-1
Changes with 40
----------------
  - Allow setting custom tags when uploading to AWS (#327)
    - Author: Jakub Kadlčík, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - Support uploading to IBM Cloud (#338)
    - Author: Jakub Kadlčík, Reviewers: Michael Vogt, Simon de Vlieger
  - Support uploading to OpenStack (#337)
    - Author: Jakub Kadlčík, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - deps: switch yaml libraries (#354)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Michael Vogt
  - main: add support for bootc-installer image types (#341)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - progress: detect real terminal width for messages (#316)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Simon de Vlieger

— Somewhere on the Internet, 2025-10-29


* Wed Oct 15 2025 Packit <hello@packit.dev> - 39-1
Changes with 39
----------------
  - ci: consistent triggers for spec check (#346)
    - Author: Simon de Vlieger, Reviewers: Ondřej Budai, Tomáš Hozza
  - ci: split apart test cases (#331)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Michael Vogt
  - cmd/image-builder: adjust code to unified rpmmd.Package struct (HMS-9457) (#334)
    - Author: Tomáš Hozza, Reviewers: Brian C. Lane, Simon de Vlieger
  - deps: update images and blueprint (#345)
    - Author: Simon de Vlieger, Reviewers: Florian Schüller, Tomáš Hozza
  - main: add osbuild version to version command (#332)
    - Author: Lukáš Zapletal, Reviewers: Michael Vogt, Tomáš Hozza

— Somewhere on the Internet, 2025-10-15


* Mon Oct 06 2025 Packit <hello@packit.dev> - 38-1
Changes with 38
----------------
  - deps: bump images to 0.202.0 (#339)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Michael Vogt

— Somewhere on the Internet, 2025-10-06


* Wed Oct 01 2025 Packit <hello@packit.dev> - 37-1
Changes with 37
----------------
  - Support uploading to libvirt (#300)
    - Author: Jakub Kadlčík, Reviewers: Sanne Raymaekers, Simon de Vlieger
  - blueprintload: improve error message in Load (#333)
    - Author: Ondřej Budai, Reviewers: Michael Vogt, Simon de Vlieger, Tomáš Hozza
  - doc: mention CentOS (#336)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - go.mod: update to v0.197.0 (#326)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - main: add `--bootc-build-ref` option to set build container (#325)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - test: add missing test container cleanups (#330)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - test: check that we get the expected image types (HMS-9426) (#320)
    - Author: Michael Vogt, Reviewers: Sanne Raymaekers, Simon de Vlieger

— Somewhere on the Internet, 2025-10-01


* Wed Sep 24 2025 Packit <hello@packit.dev> - 36-1
Changes with 36
----------------
  - deps: update to images 0.195.0 (#318)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Tomáš Hozza
  - deps: upgrade images to v0.194 (#314)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - gitignore: add common image formats (#312)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - progress: split progress.go into command.go (#313)
    - Author: Lukáš Zapletal, Reviewers: Michael Vogt, Simon de Vlieger

— Somewhere on the Internet, 2025-09-24


* Fri Sep 19 2025 Packit <hello@packit.dev> - 35-1
Changes with 35
----------------
  - cmd/upload: add fedora ami to aws upload (HMS-9388) (#307)
    - Author: Gianluca Zuccarelli, Reviewers: Lukáš Zapletal, Michael Vogt
  - deps: update to images 0.193.0 (#308)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Michael Vogt
  - main: update to latest images API changes in imgfilter (#295)
    - Author: Michael Vogt, Reviewers: Simon de Vlieger, Tomáš Hozza

— Somewhere on the Internet, 2025-09-19


* Tue Sep 16 2025 Packit <hello@packit.dev> - 34-1
Changes with 34
----------------
  - Install openssl in cli container (#292)
    - Author: Justin Sherrill, Reviewers: Brian C. Lane, Michael Vogt
  - build(deps): bump actions/setup-python from 5 to 6 (#296)
    - Author: dependabot[bot], Reviewers: Achilleas Koutsou, Tomáš Hozza
  - deps: update to images 0.191.0 (#302)
    - Author: Simon de Vlieger, Reviewers: Michael Vogt, Tomáš Hozza
  - github: add CODEOWNERS (#291)
    - Author: Achilleas Koutsou, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - go.mod: update osbuild/images to 0.190.0 (dnfjson -> depsolvednf rename) (HMS-9366) (#301)
    - Author: Tomáš Hozza, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - go.mod: update to images v0.186.0 (#294)
    - Author: Michael Vogt, Reviewers: Ondřej Budai, Tomáš Hozza
  - image-builder: use `manifesttest` from `images` (#293)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Ondřej Budai
  - main: add support disk based bootc images via --bootc-ref  (HMS-8845) (#245)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Ondřej Budai, Simon de Vlieger

— Somewhere on the Internet, 2025-09-16


* Thu Aug 28 2025 Packit <hello@packit.dev> - 33-1
Changes with 33
----------------
  - deps: images 0.182.0 (#288)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli, Michael Vogt

— Somewhere on the Internet, 2025-08-28


* Tue Aug 19 2025 Packit <hello@packit.dev> - 31-1
Changes with 31
----------------
  - build(deps): bump actions/checkout from 3 to 5 (#278)
    - Author: dependabot[bot], Reviewers: Brian C. Lane, Simon de Vlieger
  - build(deps): bump github.com/docker/docker from 28.3.2+incompatible to 28.3.3+incompatible (#270)
    - Author: dependabot[bot], Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - image-builder: use manifest.{Build,Payload}Pipelines (#279)
    - Author: Michael Vogt, Reviewers: Brian C. Lane, Lukáš Zapletal, Simon de Vlieger, Tomáš Hozza
  - main: fix --extra-repos support when cross building (#281)
    - Author: Michael Vogt, Reviewers: Brian C. Lane, Lukáš Zapletal, Simon de Vlieger, Tomáš Hozza
  - setup: Fix a typo carried over from bib (#277)
    - Author: Brian C. Lane, Reviewers: Lukáš Zapletal, Michael Vogt

— Somewhere on the Internet, 2025-08-19


* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 30-2
- Rebuild for golang-1.25.0

* Mon Aug 11 2025 Packit <hello@packit.dev> - 30-1
Changes with 30
----------------
  - image-builder: move to latest images library (#272)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - image-builder: use `github.com/osbuild/blueprint` (#273)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli

— Somewhere on the Internet, 2025-08-11


* Fri Aug 01 2025 Packit <hello@packit.dev> - 29-1
Changes with 29
----------------
  - deps: fix images 0.168 (#266)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Lukáš Zapletal

— Somewhere on the Internet, 2025-08-01


* Thu Jul 31 2025 Packit <hello@packit.dev> - 28-1
Changes with 28
----------------
  - README.md: document `--ignore-warnings` (#254)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - ci/packit: remove EPEL release automation (#258)
    - Author: Simon de Vlieger, Reviewers: Ondřej Budai, Tomáš Hozza
  - ci: upgrade golangci-lint to 2.3.0 (#257)
    - Author: Lukáš Zapletal, Reviewers: Michael Vogt, Simon de Vlieger
  - deps: update `images` to 0.168 (HMS-8949, HMS-8922) (#262)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Michael Vogt, Tomáš Hozza
  - spec: fix up version number (#259)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Ondřej Budai, Tomáš Hozza

— Somewhere on the Internet, 2025-07-31


* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Packit <hello@packit.dev> - 27-1
Changes with 27
----------------
  - chore: set specfile version at build (#253)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Lukáš Zapletal

— Somewhere on the Internet, 2025-07-23


* Mon Jul 21 2025 Packit <hello@packit.dev> - 26-1
Changes with 26
----------------
  - deps: bump images to 0.164 (#252)
    - Author: Simon de Vlieger, Reviewers: Michael Vogt, Ondřej Budai
  - main: add `--ignore-warnings` cmdline option (#250)
    - Author: Michael Vogt, Reviewers: Lukáš Zapletal, Sanne Raymaekers, Simon de Vlieger
  - testutil: trivial cleanup/rename (#249)
    - Author: Michael Vogt, Reviewers: Ondřej Budai, Simon de Vlieger

— Somewhere on the Internet, 2025-07-21


* Wed Jul 16 2025 Packit <hello@packit.dev> - 25-1
Changes with 25
----------------
  - deps: update images to 0.162.0 (#247)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal, Michael Vogt, Ondřej Budai
  - main: `--version` includes git commit (#230)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Michael Vogt
  - packit: enable RHEL 10 builds (HMS-8829) (#246)
    - Author: Ondřej Budai, Reviewers: Florian Schüller, Sanne Raymaekers, Simon de Vlieger

— Somewhere on the Internet, 2025-07-16


* Mon Jul 14 2025 Packit <hello@packit.dev> - 24-1
Changes with 24
----------------
  - Always set rhsm.Facts when generating manifests (#239)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - doc/01-usage.md: avoid multiple h1 in one document (#235)
    - Author: Florian Schüller, Reviewers: Michael Vogt, Simon de Vlieger
  - doc/10-faq.md: add image types documentation (#236)
    - Author: Florian Schüller, Reviewers: Michael Vogt, Simon de Vlieger
  - docs: subscription basic info (#205)
    - Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Michael Vogt
  - readme: mention mount for container (#232)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane, Jelle van der Waa, Michael Vogt

— Somewhere on the Internet, 2025-07-09


* Wed Jun 25 2025 Packit <hello@packit.dev> - 23-1
Changes with 23
----------------
  - cmd/describe: ensure that all image types can be described (HMS-7044) (#231)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2025-06-25


* Sun Jun 22 2025 Packit <hello@packit.dev> - 22-1
Changes with 22
----------------
  - GHA: add the common-stale-action (#225)
    - Author: Tomáš Hozza, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - chore: bump `images` (#228)
    - Author: Simon de Vlieger, Reviewers: Tomáš Hozza

— Somewhere on the Internet, 2025-06-22


* Wed Jun 11 2025 Packit <hello@packit.dev> - 21-1
Changes with 21
----------------
  - image-builder: fix cross-arch uploading (#218)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - packit: rename epel9-next (#224)
    - Author: Simon de Vlieger, Reviewers: Lukáš Zapletal

— Somewhere on the Internet, 2025-06-11


* Fri May 30 2025 Packit <hello@packit.dev> - 20-1
Changes with 20
----------------
  - deps: update (#219)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou

— Somewhere on the Internet, 2025-05-30


* Wed May 14 2025 Packit <hello@packit.dev> - 19-1
Changes with 19
----------------
  - refactor: use standard logger instead of logrus (#214)
    - Author: Lukáš Zapletal, Reviewers: Michael Vogt

— Somewhere on the Internet, 2025-05-14


* Thu Apr 17 2025 Packit <hello@packit.dev> - 17-1
Changes with 17
----------------
  - deps: bump images (#207)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou

— Somewhere on the Internet, 2025-04-17


* Wed Apr 02 2025 Packit <hello@packit.dev> - 15-1
Changes with 15
----------------
  - README: document that cross building works (#168)
    - Author: Michael Vogt, Reviewers: Simon de Vlieger
  - Revert "blueprintload: enable strict checking for toml" (#174)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Michael Vogt
  - blueprintload: enable strict checking for toml (#163)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Brian C. Lane
  - go.mod: update to latest version of `github.com/osbuild/blueprint` (#172)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou
  - import: `progress` from `bootc-image-builder` (#179)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou
  - import: `setup`, `util`, `podmanutil` from `bootc-image-builder` (#178)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou
  - main: Add a --version flag to show the build version (#175)
    - Author: Brian C. Lane, Reviewers: Michael Vogt, Simon de Vlieger
  - main: allow seed setting (#176)
    - Author: Simon de Vlieger, Reviewers: Achilleas Koutsou, Michael Vogt
  - main: automatically cross build when --arch <foreign> is passed (#164)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - main: show output directory content after image build (#162)
    - Author: Michael Vogt, Reviewers: Brian C. Lane
  - main: tweak handling of --output-name to avoid adding double extensions (#161)
    - Author: Michael Vogt, Reviewers: Simon de Vlieger
  - main: tweak how ibcli determines if bootstraping is needed (#167)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou
  - many: move to use the new github.com/osbuild/blueprint module (HMS-5804) (#169)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou
  - progress: set --cache-max-size in osbuild (#182)
    - Author: Simon de Vlieger, Reviewers: Michael Vogt

— Somewhere on the Internet, 2025-04-02


* Fri Mar 14 2025 Packit <hello@packit.dev> - 14-1
Changes with 14
----------------
  - build(deps): bump github.com/cheggaaa/pb/v3 from 3.1.6 to 3.1.7 in the go-deps group (#147)
    - Author: dependabot[bot], Reviewers: Simon de Vlieger
  - doc: fix typo (#152)
    - Author: Simon de Vlieger, Reviewers: Michael Vogt
  - ibcli: add new --output-name flag and predictable default names (#158)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - main: fix creating output dir for `--with-buildlog` (#150)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - main: show "success" message with output dir when build finishes (#154)
    - Author: Michael Vogt, Reviewers: Simon de Vlieger
  - main: skip arch checks on`IMAGE_BUILDER_EXPERIMENTAL=bootstrap` (#155)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou
  - packit: enable epel-9 and epel-10 (#149)
    - Author: Simon de Vlieger, Reviewers: Michael Vogt, Ondřej Budai

— Somewhere on the Internet, 2025-03-14


* Wed Mar 05 2025 Packit <hello@packit.dev> - 13-1
Changes with 13
----------------
  - chore: bump deps (#146)
    - Author: Simon de Vlieger, Reviewers: Brian C. Lane
  - main: add build --with-buildlog (#106)
    - Author: Michael Vogt, Reviewers: Ondřej Budai, Simon de Vlieger
  - main: argument names (#138)
    - Author: Simon de Vlieger, Reviewers: Michael Vogt, Tomáš Hozza
  - more doc updates (#132)
    - Author: Simon de Vlieger, Reviewers: Michael Vogt
  - readme: update installation instructions (#143)
    - Author: Simon de Vlieger, Reviewers: Ondřej Budai

— Somewhere on the Internet, 2025-03-05


* Fri Feb 14 2025 Packit <hello@packit.dev> - 11-1
Changes with 11
----------------
  - describeimg: typo in describe output (#129)
    - Author: Simon de Vlieger, Reviewers: Michael Vogt
  - go.mod: update to get the latest `progress` fixes from `bib` (#127)
    - Author: Michael Vogt, Reviewers: Simon de Vlieger
  - main: add `-v,--verbose` switch that enables verbose build logging (#126)
    - Author: Michael Vogt, Reviewers: Ondřej Budai
  - main: add add `--force-repo` flag (#134)
    - Author: Michael Vogt, Reviewers: Simon de Vlieger, Tomáš Hozza
  - main: add new `--extra-repo` flag (#113)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Tomáš Hozza
  - main: add new upload command (#119)
    - Author: Michael Vogt, Reviewers: Tomáš Hozza
  - main: update for new reporegistry.New() api (c.f. pr#1179) (#128)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou

— Somewhere on the Internet, 2025-02-14


* Wed Feb 05 2025 Packit <hello@packit.dev> - 10-1
Changes with 10
----------------
  - main: fix auto-detected distro that is non-visible, tweak order (#124)
    - Author: Michael Vogt, Reviewers: Ondřej Budai
  - main: reset the terminal properly on SIGINT (#125)
    - Author: Michael Vogt, Reviewers: Ondřej Budai

— Somewhere on the Internet, 2025-02-05


* Mon Feb 03 2025 Packit <hello@packit.dev> - 9-1
Changes with 9
----------------
  - ci/packit: set downstream name (#116)
    - Author: Simon de Vlieger, Reviewers: Ondřej Budai
  - specfile: build requires `libxcrypt-compat` (#117)
    - Author: Simon de Vlieger, Reviewers: Ondřej Budai

— Somewhere on the Internet, 2025-02-03


* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 7-2
- Add explicit BR: libxcrypt-devel

# the changelog is distribution-specific, therefore there's just one entry
# to make rpmlint happy.

* Fri Jan 24 2025 Image Builder team <osbuilders@redhat.com> - 0-1
- On this day, this project was born and the RPM created.
