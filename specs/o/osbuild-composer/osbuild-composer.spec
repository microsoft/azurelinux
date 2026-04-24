# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Do not build with tests by default
# Pass --with tests to rpmbuild to override
%bcond_with tests

# When --with relax_requires is specified osbuild-composer-tests
# will require osbuild-composer only by name, excluding version/release
# This is used internally during nightly pipeline testing!
%bcond_with relax_requires

# The minimum required osbuild version
%global min_osbuild_version 171

%global goipath         github.com/osbuild/osbuild-composer

Version:        164

%gometa

%global common_description %{expand:
A service for building customized OS artifacts, such as VM images and OSTree
commits, that uses osbuild under the hood. Besides building images for local
usage, it can also upload images directly to cloud.

It is compatible with composer-cli and cockpit-composer clients.
}

Name:           osbuild-composer
Release: 2%{?dist}
Summary:        An image building service based on osbuild

# osbuild-composer doesn't have support for building i686 and armv7hl images
ExcludeArch:    i686 armv7hl

# Upstream license specification: Apache-2.0
License:        Apache-2.0
URL:            %{gourl}
Source0:        %{gosource}


BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires:  systemd
BuildRequires:  krb5-devel
BuildRequires:  python3-docutils
BuildRequires:  make
# Build requirements of 'theproglottis/gpgme' package
BuildRequires:  gpgme-devel
BuildRequires:  libassuan-devel
# Build requirements of 'github.com/containers/storage' package
BuildRequires:  device-mapper-devel
%if 0%{?fedora}
BuildRequires:  systemd-rpm-macros
BuildRequires:  git
# Build requirements of 'github.com/containers/storage' package
BuildRequires:  btrfs-progs-devel
# DO NOT REMOVE the BUNDLE_START and BUNDLE_END markers as they are used by 'tools/rpm_spec_add_provides_bundle.sh' to generate the Provides: bundled list
# BUNDLE_START
Provides: bundled(golang(cel.dev/expr)) = 0.24.0
Provides: bundled(golang(cloud.google.com/go)) = 0.121.6
Provides: bundled(golang(cloud.google.com/go/auth)) = 0.16.5
Provides: bundled(golang(cloud.google.com/go/auth/oauth2adapt)) = 0.2.8
Provides: bundled(golang(cloud.google.com/go/compute)) = 1.45.0
Provides: bundled(golang(cloud.google.com/go/compute/metadata)) = 0.8.0
Provides: bundled(golang(cloud.google.com/go/iam)) = 1.5.2
Provides: bundled(golang(cloud.google.com/go/monitoring)) = 1.24.2
Provides: bundled(golang(cloud.google.com/go/storage)) = 1.56.1
Provides: bundled(golang(dario.cat/mergo)) = 1.0.2
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azcore)) = 1.19.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azidentity)) = 1.11.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/internal)) = 1.11.2
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/compute/armcompute/v5)) = 5.7.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/network/armnetwork/v7)) = 7.0.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/resources/armresources)) = 1.2.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/storage/armstorage)) = 1.8.1
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/storage/azblob)) = 1.6.2
Provides: bundled(golang(github.com/AzureAD/microsoft-authentication-library-for-go)) = 1.4.2
Provides: bundled(golang(github.com/BurntSushi/toml)) = 1.6.0
Provides: bundled(golang(github.com/GoogleCloudPlatform/opentelemetry-operations-go/detectors/gcp)) = 1.27.0
Provides: bundled(golang(github.com/GoogleCloudPlatform/opentelemetry-operations-go/exporter/metric)) = 0.53.0
Provides: bundled(golang(github.com/GoogleCloudPlatform/opentelemetry-operations-go/internal/resourcemapping)) = 0.53.0
Provides: bundled(golang(github.com/Microsoft/go-winio)) = 0.6.2
Provides: bundled(golang(github.com/Microsoft/hcsshim)) = 0.13.0
Provides: bundled(golang(github.com/VividCortex/ewma)) = 1.2.0
Provides: bundled(golang(github.com/acarl005/stripansi)) = 5a71ef0
Provides: bundled(golang(github.com/apapsch/go-jsonmerge/v2)) = 2.0.0
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2)) = 1.41.1
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream)) = 1.7.1
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/config)) = 1.32.7
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/credentials)) = 1.19.7
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/feature/ec2/imds)) = 1.18.17
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/feature/s3/manager)) = 1.19.4
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/internal/configsources)) = 1.4.17
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/internal/endpoints/v2)) = 2.7.17
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/internal/ini)) = 1.8.4
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/internal/v4a)) = 1.4.6
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/autoscaling)) = 1.64.0
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/ec2)) = 1.289.0
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding)) = 1.13.4
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/checksum)) = 1.8.6
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/presigned-url)) = 1.13.17
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/internal/s3shared)) = 1.19.6
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/s3)) = 1.87.3
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/signin)) = 1.0.5
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/sso)) = 1.30.9
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/ssooidc)) = 1.35.13
Provides: bundled(golang(github.com/aws/aws-sdk-go-v2/service/sts)) = 1.41.6
Provides: bundled(golang(github.com/aws/smithy-go)) = 1.24.0
Provides: bundled(golang(github.com/aymerick/douceur)) = 0.2.0
Provides: bundled(golang(github.com/beorn7/perks)) = 1.0.1
Provides: bundled(golang(github.com/cenkalti/backoff/v4)) = 4.3.0
Provides: bundled(golang(github.com/cespare/xxhash/v2)) = 2.3.0
Provides: bundled(golang(github.com/cncf/xds/go)) = 2ac532f
Provides: bundled(golang(github.com/containerd/cgroups/v3)) = 3.0.5
Provides: bundled(golang(github.com/containerd/errdefs)) = 1.0.0
Provides: bundled(golang(github.com/containerd/errdefs/pkg)) = 0.3.0
Provides: bundled(golang(github.com/containerd/stargz-snapshotter/estargz)) = 0.16.3
Provides: bundled(golang(github.com/containerd/typeurl/v2)) = 2.2.3
Provides: bundled(golang(github.com/containers/common)) = 0.64.1
Provides: bundled(golang(github.com/containers/image/v5)) = 5.36.1
Provides: bundled(golang(github.com/containers/libtrust)) = c1716e8
Provides: bundled(golang(github.com/containers/ocicrypt)) = 1.2.1
Provides: bundled(golang(github.com/containers/storage)) = 1.59.1
Provides: bundled(golang(github.com/coreos/go-semver)) = 0.3.1
Provides: bundled(golang(github.com/coreos/go-systemd/v22)) = 22.7.0
Provides: bundled(golang(github.com/cyberphone/json-canonicalization)) = 19d51d7
Provides: bundled(golang(github.com/cyphar/filepath-securejoin)) = 0.4.1
Provides: bundled(golang(github.com/davecgh/go-spew)) = d8f796a
Provides: bundled(golang(github.com/distribution/reference)) = 0.6.0
Provides: bundled(golang(github.com/docker/distribution)) = 2.8.3+incompatible
Provides: bundled(golang(github.com/docker/docker)) = 28.3.2+incompatible
Provides: bundled(golang(github.com/docker/docker-credential-helpers)) = 0.9.3
Provides: bundled(golang(github.com/docker/go-connections)) = 0.5.0
Provides: bundled(golang(github.com/docker/go-units)) = 0.5.0
Provides: bundled(golang(github.com/dougm/pretty)) = add1dbc
Provides: bundled(golang(github.com/dprotaso/go-yit)) = 9ba8df1
Provides: bundled(golang(github.com/envoyproxy/go-control-plane/envoy)) = 1.32.4
Provides: bundled(golang(github.com/envoyproxy/protoc-gen-validate)) = 1.2.1
Provides: bundled(golang(github.com/felixge/httpsnoop)) = 1.0.4
Provides: bundled(golang(github.com/getkin/kin-openapi)) = 0.133.0
Provides: bundled(golang(github.com/getsentry/sentry-go)) = 0.42.0
Provides: bundled(golang(github.com/getsentry/sentry-go/echo)) = 0.42.0
Provides: bundled(golang(github.com/getsentry/sentry-go/logrus)) = 0.42.0
Provides: bundled(golang(github.com/go-jose/go-jose/v4)) = 4.0.5
Provides: bundled(golang(github.com/go-logr/logr)) = 1.4.3
Provides: bundled(golang(github.com/go-logr/stdr)) = 1.2.2
Provides: bundled(golang(github.com/go-openapi/jsonpointer)) = 0.21.1
Provides: bundled(golang(github.com/go-openapi/swag)) = 0.23.1
Provides: bundled(golang(github.com/gobwas/glob)) = 0.2.3
Provides: bundled(golang(github.com/gogo/protobuf)) = 1.3.2
Provides: bundled(golang(github.com/golang-jwt/jwt/v4)) = 4.5.2
Provides: bundled(golang(github.com/golang-jwt/jwt/v5)) = 5.3.0
Provides: bundled(golang(github.com/golang/glog)) = 1.2.5
Provides: bundled(golang(github.com/golang/groupcache)) = 2c02b82
Provides: bundled(golang(github.com/golang/protobuf)) = 1.5.4
Provides: bundled(golang(github.com/google/go-cmp)) = 0.7.0
Provides: bundled(golang(github.com/google/go-containerregistry)) = 0.20.3
Provides: bundled(golang(github.com/google/go-intervals)) = 0.0.2
Provides: bundled(golang(github.com/google/s2a-go)) = 0.1.9
Provides: bundled(golang(github.com/google/uuid)) = 1.6.0
Provides: bundled(golang(github.com/googleapis/enterprise-certificate-proxy)) = 0.3.6
Provides: bundled(golang(github.com/googleapis/gax-go/v2)) = 2.15.0
Provides: bundled(golang(github.com/gorilla/css)) = 1.0.0
Provides: bundled(golang(github.com/gorilla/mux)) = 1.8.1
Provides: bundled(golang(github.com/hashicorp/errwrap)) = 1.1.0
Provides: bundled(golang(github.com/hashicorp/go-cleanhttp)) = 0.5.2
Provides: bundled(golang(github.com/hashicorp/go-multierror)) = 1.1.1
Provides: bundled(golang(github.com/hashicorp/go-retryablehttp)) = 0.7.8
Provides: bundled(golang(github.com/hashicorp/go-version)) = 1.7.0
Provides: bundled(golang(github.com/jackc/chunkreader/v2)) = 2.0.1
Provides: bundled(golang(github.com/jackc/pgconn)) = 1.14.3
Provides: bundled(golang(github.com/jackc/pgio)) = 1.0.0
Provides: bundled(golang(github.com/jackc/pgpassfile)) = 1.0.0
Provides: bundled(golang(github.com/jackc/pgproto3/v2)) = 2.3.3
Provides: bundled(golang(github.com/jackc/pgservicefile)) = 091c0ba
Provides: bundled(golang(github.com/jackc/pgtype)) = 1.14.4
Provides: bundled(golang(github.com/jackc/pgx/v4)) = 4.18.3
Provides: bundled(golang(github.com/jackc/puddle)) = 1.3.0
Provides: bundled(golang(github.com/josharian/intern)) = 1.0.0
Provides: bundled(golang(github.com/json-iterator/go)) = 1.1.12
Provides: bundled(golang(github.com/julienschmidt/httprouter)) = 1.3.0
Provides: bundled(golang(github.com/klauspost/compress)) = 1.18.0
Provides: bundled(golang(github.com/klauspost/pgzip)) = 1.2.6
Provides: bundled(golang(github.com/kolo/xmlrpc)) = a4b6fa1
Provides: bundled(golang(github.com/kr/text)) = 0.2.0
Provides: bundled(golang(github.com/kylelemons/godebug)) = 1.1.0
Provides: bundled(golang(github.com/labstack/echo/v4)) = 4.13.4
Provides: bundled(golang(github.com/labstack/gommon)) = 0.4.2
Provides: bundled(golang(github.com/letsencrypt/boulder)) = de9c061
Provides: bundled(golang(github.com/mailru/easyjson)) = 0.9.0
Provides: bundled(golang(github.com/mattn/go-colorable)) = 0.1.14
Provides: bundled(golang(github.com/mattn/go-isatty)) = 0.0.20
Provides: bundled(golang(github.com/mattn/go-runewidth)) = 0.0.16
Provides: bundled(golang(github.com/mattn/go-sqlite3)) = 1.14.28
Provides: bundled(golang(github.com/microcosm-cc/bluemonday)) = 1.0.25
Provides: bundled(golang(github.com/miekg/pkcs11)) = 1.1.1
Provides: bundled(golang(github.com/mistifyio/go-zfs/v3)) = 3.0.1
Provides: bundled(golang(github.com/moby/docker-image-spec)) = 1.3.1
Provides: bundled(golang(github.com/moby/sys/capability)) = 0.4.0
Provides: bundled(golang(github.com/moby/sys/mountinfo)) = 0.7.2
Provides: bundled(golang(github.com/moby/sys/user)) = 0.4.0
Provides: bundled(golang(github.com/modern-go/concurrent)) = bacd9c7
Provides: bundled(golang(github.com/modern-go/reflect2)) = 1.0.2
Provides: bundled(golang(github.com/mohae/deepcopy)) = c48cc78
Provides: bundled(golang(github.com/munnerz/goautoneg)) = a7dc8b6
Provides: bundled(golang(github.com/oapi-codegen/oapi-codegen/v2)) = 2.5.1
Provides: bundled(golang(github.com/oapi-codegen/runtime)) = 1.1.2
Provides: bundled(golang(github.com/oasdiff/yaml)) = f31be36
Provides: bundled(golang(github.com/oasdiff/yaml3)) = d218240
Provides: bundled(golang(github.com/opencontainers/go-digest)) = 1.0.0
Provides: bundled(golang(github.com/opencontainers/image-spec)) = 1.1.1
Provides: bundled(golang(github.com/opencontainers/runtime-spec)) = 1.2.1
Provides: bundled(golang(github.com/opencontainers/selinux)) = 1.12.0
Provides: bundled(golang(github.com/openshift-online/ocm-sdk-go)) = 0.1.486
Provides: bundled(golang(github.com/oracle/oci-go-sdk/v54)) = 54.0.0
Provides: bundled(golang(github.com/osbuild/blueprint)) = 1.23.0
Provides: bundled(golang(github.com/osbuild/images)) = 0.239.0
Provides: bundled(golang(github.com/osbuild/osbuild-composer/pkg/splunk_logger)) = 0239db5
Provides: bundled(golang(github.com/perimeterx/marshmallow)) = 1.1.5
Provides: bundled(golang(github.com/pkg/browser)) = 5ac0b6a
Provides: bundled(golang(github.com/pkg/errors)) = 0.9.1
Provides: bundled(golang(github.com/planetscale/vtprotobuf)) = 0393e58
Provides: bundled(golang(github.com/pmezard/go-difflib)) = 5d4384e
Provides: bundled(golang(github.com/proglottis/gpgme)) = 0.1.4
Provides: bundled(golang(github.com/prometheus/client_golang)) = 1.23.2
Provides: bundled(golang(github.com/prometheus/client_model)) = 0.6.2
Provides: bundled(golang(github.com/prometheus/common)) = 0.66.1
Provides: bundled(golang(github.com/prometheus/procfs)) = 0.16.1
Provides: bundled(golang(github.com/rivo/uniseg)) = 0.4.7
Provides: bundled(golang(github.com/secure-systems-lab/go-securesystemslib)) = 0.9.0
Provides: bundled(golang(github.com/segmentio/ksuid)) = 1.0.4
Provides: bundled(golang(github.com/sigstore/fulcio)) = 1.6.6
Provides: bundled(golang(github.com/sigstore/protobuf-specs)) = 0.4.1
Provides: bundled(golang(github.com/sigstore/sigstore)) = 1.9.5
Provides: bundled(golang(github.com/sirupsen/logrus)) = 1.9.4
Provides: bundled(golang(github.com/skratchdot/open-golang)) = eef8423
Provides: bundled(golang(github.com/smallstep/pkcs7)) = 0.1.1
Provides: bundled(golang(github.com/sony/gobreaker)) = dd874f9
Provides: bundled(golang(github.com/speakeasy-api/jsonpath)) = 0.6.0
Provides: bundled(golang(github.com/speakeasy-api/openapi-overlay)) = 0.10.2
Provides: bundled(golang(github.com/spiffe/go-spiffe/v2)) = 2.5.0
Provides: bundled(golang(github.com/stefanberger/go-pkcs11uri)) = 7828495
Provides: bundled(golang(github.com/stretchr/testify)) = 1.11.1
Provides: bundled(golang(github.com/sylabs/sif/v2)) = 2.21.1
Provides: bundled(golang(github.com/tchap/go-patricia/v2)) = 2.3.3
Provides: bundled(golang(github.com/titanous/rocacheck)) = afe7314
Provides: bundled(golang(github.com/ubccr/kerby)) = 412be7b
Provides: bundled(golang(github.com/ulikunitz/xz)) = 0.5.12
Provides: bundled(golang(github.com/valyala/bytebufferpool)) = 1.0.0
Provides: bundled(golang(github.com/valyala/fasttemplate)) = 1.2.2
Provides: bundled(golang(github.com/vbatts/tar-split)) = 0.12.1
Provides: bundled(golang(github.com/vbauerster/mpb/v8)) = 8.10.2
Provides: bundled(golang(github.com/vmware-labs/yaml-jsonpath)) = 0.3.2
Provides: bundled(golang(github.com/vmware/govmomi)) = 0.52.0
Provides: bundled(golang(github.com/woodsbury/decimal128)) = 1.3.0
Provides: bundled(golang(github.com/zeebo/errs)) = 1.4.0
Provides: bundled(golang(go.opencensus.io)) = 0.24.0
Provides: bundled(golang(go.opentelemetry.io/auto/sdk)) = 1.1.0
Provides: bundled(golang(go.opentelemetry.io/contrib/detectors/gcp)) = 1.36.0
Provides: bundled(golang(go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc)) = 0.61.0
Provides: bundled(golang(go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp)) = 0.61.0
Provides: bundled(golang(go.opentelemetry.io/otel)) = 1.36.0
Provides: bundled(golang(go.opentelemetry.io/otel/metric)) = 1.36.0
Provides: bundled(golang(go.opentelemetry.io/otel/sdk)) = 1.36.0
Provides: bundled(golang(go.opentelemetry.io/otel/sdk/metric)) = 1.36.0
Provides: bundled(golang(go.opentelemetry.io/otel/trace)) = 1.36.0
Provides: bundled(golang(go.yaml.in/yaml/v2)) = 2.4.2
Provides: bundled(golang(go.yaml.in/yaml/v3)) = 3.0.3
Provides: bundled(golang(golang.org/x/crypto)) = 0.41.0
Provides: bundled(golang(golang.org/x/exp)) = 7d7fa50
Provides: bundled(golang(golang.org/x/mod)) = 0.27.0
Provides: bundled(golang(golang.org/x/net)) = 0.43.0
Provides: bundled(golang(golang.org/x/oauth2)) = 0.30.0
Provides: bundled(golang(golang.org/x/sync)) = 0.16.0
Provides: bundled(golang(golang.org/x/sys)) = 0.35.0
Provides: bundled(golang(golang.org/x/term)) = 0.34.0
Provides: bundled(golang(golang.org/x/text)) = 0.28.0
Provides: bundled(golang(golang.org/x/time)) = 0.12.0
Provides: bundled(golang(golang.org/x/tools)) = 0.36.0
Provides: bundled(golang(google.golang.org/api)) = 0.248.0
Provides: bundled(golang(google.golang.org/genproto)) = 513f239
Provides: bundled(golang(google.golang.org/genproto/googleapis/api)) = 3122310
Provides: bundled(golang(google.golang.org/genproto/googleapis/rpc)) = 3122310
Provides: bundled(golang(google.golang.org/grpc)) = 1.74.2
Provides: bundled(golang(google.golang.org/protobuf)) = 1.36.8
Provides: bundled(golang(gopkg.in/ini.v1)) = 1.67.0
Provides: bundled(golang(gopkg.in/yaml.v2)) = 2.4.0
Provides: bundled(golang(gopkg.in/yaml.v3)) = 3.0.1
# BUNDLE_END
%endif

Requires: %{name}-core = %{version}-%{release}
Requires: %{name}-worker = %{version}-%{release}
Requires: systemd

Provides: weldr

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

# Fedora and RHEL versions disable Go modules by default, but we want to use them.
# Unconditionally undefine the macro which disables it to use the default behavior.
%undefine gomodulesmode

# btrfs-progs-devel is not available on RHEL
%if 0%{?rhel}
GOTAGS="exclude_graphdriver_btrfs"
%endif

# Set the commit hash so that composer can report what source version
# was used to build it. This has to be set explicitly when calling rpmbuild,
# this script will not attempt to automatically discover it.
%if %{?commit:1}0
export LDFLAGS="${LDFLAGS} -X 'github.com/osbuild/osbuild-composer/internal/common.GitRev=%{commit}'"
%endif
export LDFLAGS="${LDFLAGS} -X 'github.com/osbuild/osbuild-composer/internal/common.RpmVersion=%{name}-%{?epoch:%epoch:}%{version}-%{release}.%{_arch}'"

%gobuild ${GOTAGS:+-tags=$GOTAGS} -o _bin/osbuild-composer %{goipath}/cmd/osbuild-composer
%gobuild ${GOTAGS:+-tags=$GOTAGS} -o _bin/osbuild-worker %{goipath}/cmd/osbuild-worker
%gobuild ${GOTAGS:+-tags=$GOTAGS} -o _bin/osbuild-worker-executor %{goipath}/cmd/osbuild-worker-executor

make man

%if %{with tests} || 0%{?rhel}

# Build test binaries with `go test -c`, so that they can take advantage of
# golang's testing package. The golang rpm macros don't support building them
# directly. Thus, do it manually, taking care to also include a build id.

TEST_LDFLAGS="${LDFLAGS:-} -B 0x$(od -N 20 -An -tx1 -w100 /dev/urandom | tr -d ' ')"

%if 0%{?rhel}
GOTAGS="${GOTAGS:+$GOTAGS,}rhel%{rhel}"
%endif

go test -c -tags="integration${GOTAGS:+,$GOTAGS}" -ldflags="${TEST_LDFLAGS}" -o _bin/osbuild-composer-cli-tests %{goipath}/cmd/osbuild-composer-cli-tests
go test -c -tags="integration${GOTAGS:+,$GOTAGS}" -ldflags="${TEST_LDFLAGS}" -o _bin/osbuild-weldr-tests %{goipath}/internal/client/
go test -c -tags="integration${GOTAGS:+,$GOTAGS}" -ldflags="${TEST_LDFLAGS}" -o _bin/osbuild-auth-tests %{goipath}/cmd/osbuild-auth-tests
go test -c -tags="integration${GOTAGS:+,$GOTAGS}" -ldflags="${TEST_LDFLAGS}" -o _bin/osbuild-koji-tests %{goipath}/cmd/osbuild-koji-tests
go test -c -tags="integration${GOTAGS:+,$GOTAGS}" -ldflags="${TEST_LDFLAGS}" -o _bin/osbuild-composer-dbjobqueue-tests %{goipath}/cmd/osbuild-composer-dbjobqueue-tests
go test -c -tags="integration${GOTAGS:+,$GOTAGS}" -ldflags="${TEST_LDFLAGS}" -o _bin/osbuild-service-maintenance-tests %{goipath}/cmd/osbuild-service-maintenance
go build -tags="integration${GOTAGS:+,$GOTAGS}" -ldflags="${TEST_LDFLAGS}" -o _bin/osbuild-mock-openid-provider %{goipath}/cmd/osbuild-mock-openid-provider

%endif

%install
install -m 0755 -vd                                                %{buildroot}%{_libexecdir}/osbuild-composer
install -m 0755 -vp _bin/osbuild-composer                          %{buildroot}%{_libexecdir}/osbuild-composer/
install -m 0755 -vp _bin/osbuild-worker                            %{buildroot}%{_libexecdir}/osbuild-composer/
install -m 0755 -vp _bin/osbuild-worker-executor                   %{buildroot}%{_libexecdir}/osbuild-composer/

# Only include repositories for the distribution and release
install -m 0755 -vd                                                %{buildroot}%{_datadir}/osbuild-composer/repositories

# CentOS also defines rhel so we check for centos first
%if 0%{?centos}

# Latest CentOS supports building all CentOS versions
%if 0%{?centos} >= 10
install -m 0644 -vp vendor/github.com/osbuild/images/data/repositories/centos-*                          %{buildroot}%{_datadir}/osbuild-composer/repositories/

%else
# All other CentOS versions support building for the same version
install -m 0644 -vp vendor/github.com/osbuild/images/data/repositories/centos-%{centos}*                 %{buildroot}%{_datadir}/osbuild-composer/repositories/
# centos-stream-* are symlinks
cp -a repositories/centos-stream-%{centos}*          %{buildroot}%{_datadir}/osbuild-composer/repositories/
%endif

%else

%if 0%{?rhel}
# RHEL 10 supports building all RHEL versions
%if 0%{?rhel} >= 10
for REPO_FILE in $(ls vendor/github.com/osbuild/images/data/repositories/rhel-* ); do
    install -m 0644 -vp ${REPO_FILE}                               %{buildroot}%{_datadir}/osbuild-composer/repositories/$(basename ${REPO_FILE})
done

# RHEL-8 auxiliary key is signed using SHA-1, which is not enabled by default on RHEL-10 and later
for REPO_FILE in $(ls repositories/rhel-8*-no-aux-key.json); do
    install -m 0644 -vp ${REPO_FILE}                               %{buildroot}%{_datadir}/osbuild-composer/repositories/$(basename ${REPO_FILE} | sed 's/-no-aux-key//g')
done

%else
# All other RHEL versions support building for the same version
for REPO_FILE in $(ls vendor/github.com/osbuild/images/data/repositories/rhel-%{rhel}* ); do
    install -m 0644 -vp ${REPO_FILE}                               %{buildroot}%{_datadir}/osbuild-composer/repositories/$(basename ${REPO_FILE})
done

# RHEL 9 supports building also for RHEL 8
%if 0%{?rhel} == 9
for REPO_FILE in $(ls vendor/github.com/osbuild/images/data/repositories/rhel-8* ); do
    install -m 0644 -vp ${REPO_FILE}                               %{buildroot}%{_datadir}/osbuild-composer/repositories/$(basename ${REPO_FILE})
done
%endif

%endif
%endif
%endif

# Fedora can build for all included fedora releases
%if 0%{?fedora}
install -m 0644 -vp vendor/github.com/osbuild/images/data/repositories/fedora-*                          %{buildroot}%{_datadir}/osbuild-composer/repositories/
%endif

install -m 0755 -vd                                                %{buildroot}%{_unitdir}
install -m 0644 -vp distribution/*.{service,socket}                %{buildroot}%{_unitdir}/

install -m 0755 -vd                                                %{buildroot}%{_sysusersdir}
install -m 0644 -vp distribution/osbuild-composer.conf             %{buildroot}%{_sysusersdir}/

install -m 0755 -vd                                                %{buildroot}%{_localstatedir}/cache/osbuild-composer/dnf-cache

install -m 0755 -vd                                                %{buildroot}%{_mandir}/man7
install -m 0644 -vp docs/*.7                                       %{buildroot}%{_mandir}/man7/

%if %{with tests} || 0%{?rhel}

install -m 0755 -vd                                                %{buildroot}%{_libexecdir}/osbuild-composer-test
install -m 0755 -vp _bin/osbuild-composer-cli-tests                %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp _bin/osbuild-weldr-tests                       %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp _bin/osbuild-auth-tests                        %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp _bin/osbuild-koji-tests                        %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp _bin/osbuild-composer-dbjobqueue-tests         %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp _bin/osbuild-service-maintenance-tests         %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp _bin/osbuild-mock-openid-provider              %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/define-compose-url.sh                    %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/provision.sh                             %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/gen-certs.sh                             %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/gen-ssh.sh                               %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/run-koji-container.sh                    %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/koji-compose.py                          %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/libvirt_test.sh                          %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/s3_test.sh                               %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/generic_s3_test.sh                       %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/generic_s3_https_test.sh                 %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/run-mock-auth-servers.sh                 %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vp tools/set-env-variables.sh                     %{buildroot}%{_libexecdir}/osbuild-composer-test/
install -m 0755 -vd                                                %{buildroot}%{_libexecdir}/tests/osbuild-composer
install -m 0755 -vp test/cases/*.sh                                %{buildroot}%{_libexecdir}/tests/osbuild-composer/

install -m 0755 -vd                                                %{buildroot}%{_libexecdir}/tests/osbuild-composer/api
install -m 0755 -vp test/cases/api/*.sh                            %{buildroot}%{_libexecdir}/tests/osbuild-composer/api/

install -m 0755 -vd                                                %{buildroot}%{_libexecdir}/tests/osbuild-composer/api/common
install -m 0755 -vp test/cases/api/common/*.sh                     %{buildroot}%{_libexecdir}/tests/osbuild-composer/api/common/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/ansible
install -m 0644 -vp test/data/ansible/*                            %{buildroot}%{_datadir}/tests/osbuild-composer/ansible/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/azure
install -m 0644 -vp test/data/azure/*                              %{buildroot}%{_datadir}/tests/osbuild-composer/azure/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/cloud-init
install -m 0644 -vp test/data/cloud-init/*                         %{buildroot}%{_datadir}/tests/osbuild-composer/cloud-init/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/composer
install -m 0644 -vp test/data/composer/*                           %{buildroot}%{_datadir}/tests/osbuild-composer/composer/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/worker
install -m 0644 -vp test/data/worker/*                             %{buildroot}%{_datadir}/tests/osbuild-composer/worker/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/repositories
install -m 0644 -vp test/data/repositories/*                       %{buildroot}%{_datadir}/tests/osbuild-composer/repositories/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/kerberos
install -m 0644 -vp test/data/kerberos/*                           %{buildroot}%{_datadir}/tests/osbuild-composer/kerberos/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/keyring
install -m 0644 -vp test/data/keyring/id_rsa.pub                   %{buildroot}%{_datadir}/tests/osbuild-composer/keyring/
install -m 0600 -vp test/data/keyring/id_rsa                       %{buildroot}%{_datadir}/tests/osbuild-composer/keyring/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/koji
install -m 0644 -vp test/data/koji/*                               %{buildroot}%{_datadir}/tests/osbuild-composer/koji/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/x509
install -m 0644 -vp test/data/x509/*                               %{buildroot}%{_datadir}/tests/osbuild-composer/x509/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/schemas
install -m 0644 -vp pkg/jobqueue/dbjobqueue/schemas/*              %{buildroot}%{_datadir}/tests/osbuild-composer/schemas/

install -m 0755 -vd                                                %{buildroot}%{_datadir}/tests/osbuild-composer/rhel-upgrade
install -m 0644 -vp test/data/rhel-upgrade/*                       %{buildroot}%{_datadir}/tests/osbuild-composer/rhel-upgrade/

%endif

%check
export GOFLAGS="-buildmode=pie"
%if 0%{?rhel}
export GOFLAGS+=" -tags=exclude_graphdriver_btrfs"
%endif

export GOPATH=$PWD/_build:%{gopath}
# cd inside GOPATH, otherwise go with GO111MODULE=off ignores vendor directory
cd $PWD/_build/src/%{goipath}

%post
%systemd_post osbuild-composer.service osbuild-composer.socket osbuild-composer-api.socket osbuild-composer-prometheus.socket osbuild-remote-worker.socket

%preun
%systemd_preun osbuild-composer.service osbuild-composer.socket osbuild-composer-api.socket osbuild-composer-prometheus.socket osbuild-remote-worker.socket

%postun
%systemd_postun_with_restart osbuild-composer.service osbuild-composer.socket osbuild-composer-api.socket osbuild-composer-prometheus.socket osbuild-remote-worker.socket

%files
%license LICENSE
%doc README.md
%{_mandir}/man7/%{name}.7*
%{_unitdir}/osbuild-composer.service
%{_unitdir}/osbuild-composer.socket
%{_unitdir}/osbuild-composer-api.socket
%{_unitdir}/osbuild-composer-prometheus.socket
%{_unitdir}/osbuild-local-worker.socket
%{_unitdir}/osbuild-remote-worker.socket
%{_sysusersdir}/osbuild-composer.conf

%package core
Summary:    The core osbuild-composer binary
Requires:   osbuild-depsolve-dnf >= %{min_osbuild_version}
Provides:   %{name}-dnf-json = %{version}-%{release}
Obsoletes:  %{name}-dnf-json < %{version}-%{release}

%description core
The core osbuild-composer binary. This is suitable both for spawning in containers and by systemd.

%files core
%{_libexecdir}/osbuild-composer/osbuild-composer
%{_datadir}/osbuild-composer/

%package worker
Summary:    The worker for osbuild-composer
Requires:   systemd
Requires:   qemu-img
Requires:   osbuild >= %{min_osbuild_version}
Requires:   osbuild-ostree >= %{min_osbuild_version}
Requires:   osbuild-lvm2 >= %{min_osbuild_version}
Requires:   osbuild-luks2 >= %{min_osbuild_version}
Requires:   osbuild-depsolve-dnf >= %{min_osbuild_version}
Provides:   %{name}-dnf-json = %{version}-%{release}
Obsoletes:  %{name}-dnf-json < %{version}-%{release}

%description worker
The worker for osbuild-composer

%files worker
%{_libexecdir}/osbuild-composer/osbuild-worker
%{_libexecdir}/osbuild-composer/osbuild-worker-executor
%{_unitdir}/osbuild-worker@.service
%{_unitdir}/osbuild-remote-worker@.service

%post worker
%systemd_post osbuild-worker@.service osbuild-remote-worker@.service

%preun worker
# systemd_preun uses systemctl disable --now which doesn't work well with template services.
# See https://github.com/systemd/systemd/issues/15620
# The following lines mimicks its behaviour by running two commands.
# The scriptlet is supposed to run only when the package is being removed.
if [ $1 -eq 0 ] && [ -d /run/systemd/system ]; then
    # disable and stop all the worker services
    systemctl --no-reload disable osbuild-worker@.service osbuild-remote-worker@.service
    systemctl stop "osbuild-worker@*.service" "osbuild-remote-worker@*.service"
fi

%postun worker
# restart all the worker services
%systemd_postun_with_restart "osbuild-worker@*.service" "osbuild-remote-worker@*.service"

%if %{with tests} || 0%{?rhel}

%package tests
Summary:    Integration tests
%if %{with relax_requires}
Requires:   %{name}
%else
Requires:   %{name} = %{version}-%{release}
%endif
Requires:   composer-cli
Requires:   createrepo_c
Requires:   xorriso
Requires:   qemu-kvm-core
Requires:   systemd-container
Requires:   jq
Requires:   unzip
Requires:   container-selinux
Requires:   dnsmasq
Requires:   krb5-workstation
Requires:   podman
Requires:   python3
Requires:   sssd-krb5
Requires:   libvirt-client libvirt-daemon
Requires:   libvirt-daemon-config-network
Requires:   libvirt-daemon-config-nwfilter
Requires:   libvirt-daemon-driver-interface
Requires:   libvirt-daemon-driver-network
Requires:   libvirt-daemon-driver-nodedev
Requires:   libvirt-daemon-driver-nwfilter
Requires:   libvirt-daemon-driver-qemu
Requires:   libvirt-daemon-driver-secret
Requires:   libvirt-daemon-driver-storage
Requires:   libvirt-daemon-driver-storage-disk
Requires:   libvirt-daemon-kvm
Requires:   qemu-img
Requires:   qemu-kvm
Requires:   rpmdevtools
Requires:   virt-install
Requires:   expect
Requires:   python3-lxml
Requires:   httpd
Requires:   mod_ssl
Requires:   openssl
Requires:   firewalld
# podman-plugins has been deprecated since podman version 5.0.0,
# which is in Fedora 40+ and in c10s / el10
%if (0%{?rhel} && 0%{?rhel} < 10) || (0%{?fedora} && 0%{?fedora} < 40)
Requires:   podman-plugins
%endif
Requires:   dnf-plugins-core
Requires:   skopeo
Requires:   make
Requires:   python3-pip
%if 0%{?fedora}
# koji and ansible are not in RHEL repositories. Depending on them breaks RHEL
# gating (see OSCI-1541). The test script must enable EPEL and install those
# packages manually.
Requires:   koji
Requires:   ansible
%endif
%ifarch %{arm}
Requires:   edk2-aarch64
%endif

%description tests
Integration tests to be run on a pristine-dedicated system to test the osbuild-composer package.

%files tests
%{_libexecdir}/osbuild-composer-test/
%{_libexecdir}/tests/osbuild-composer/
%{_datadir}/tests/osbuild-composer/

%endif

%changelog
* Wed Feb 18 2026 Packit <hello@packit.dev> - 164-1
Changes with 164
----------------
  - build(deps): bump actions/upload-artifact from 5 to 6 (#4961)
    - Author: {}, Reviewers: Achilleas Koutsou, Tomáš Hozza
  - chore(deps): update konflux references (#5023)
    - Author: {}, Reviewers: Sanne Raymaekers, Tomáš Hozza

— Somewhere on the Internet, 2026-02-18


* Wed Feb 11 2026 Packit <hello@packit.dev> - 162-1
Changes with 162
----------------
  - Add Transactions and Modules fields to depsolve job result (HMS-9090) (#5006)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  - Move workers to rhel 10 (HMS-9987) (#4975)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli, Simon de Vlieger
  - Update snapshots to 20260201 (#4997)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - cloudapi/v2: allow upload types for pxe & network installer (HMS-10178) (#5004)
    - Author: Gianluca Zuccarelli, Reviewers: Lukáš Zapletal, Sanne Raymaekers
  - go.mod: bump osbuild/images to v0.236.0 (HMS-10105) (#4990)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Ondřej Budai
  - templates/packer: fix registration script (#5007)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli, Lukáš Zapletal
  - tests: Update Upgrade test to RHEL 9.8 from 9.7 (#4999)
    - Author: Tomáš Koscielniak, Reviewers: Brian C. Lane, Tomáš Hozza
  - tools/build-rpms: build rpms on rhel 10 (#5005)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Lukáš Zapletal, Simon de Vlieger

— Somewhere on the Internet, 2026-02-11


* Wed Feb 04 2026 Packit <hello@packit.dev> - 161-1
Changes with 161
----------------
  - Update snapshots to 20260118 (#4985)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - chore: bump dependencies via gobump (#4988)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - packit: Build RHEL10 RPMs for x86 and ARM in COPR (#4982)
    - Author: Simon Steinbeiß, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - worker: add job to generate bootc manifests [HMS-10006] (#4977)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Tomáš Hozza

— Somewhere on the Internet, 2026-02-04


* Wed Jan 21 2026 Packit <hello@packit.dev> - 160-1
Changes with 160
----------------
  - Update snapshots to 20260106 (#4976)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - chore(deps): update konflux references (#4978)
    - Author: {}, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - chore: bump dependencies via gobump (#4979)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Tomáš Hozza
  - ci: gobump blueprint separately (#4973)
    - Author: Lukáš Zapletal, Reviewers: Sanne Raymaekers, Simon de Vlieger

— Somewhere on the Internet, 2026-01-21


* Wed Dec 24 2025 Packit <hello@packit.dev> - 158-1
Changes with 158
----------------
  - Add new job type for generating manifests using image-builder-cli [HMS-9049] (#4904)
    - Author: Achilleas Koutsou, Reviewers: Nobody
  - chore(deps): update quay.io/konflux-ci/konflux-vanguard/task-rpms-signature-scan:0.2 docker digest to 90c2b32 (#4937)
    - Author: {}, Reviewers: Florian Schüller, Sanne Raymaekers
  - go.mod: update osbuild/images to v0.230.0 (#4964)
    - Author: Achilleas Koutsou, Reviewers: Gianluca Zuccarelli, Lukáš Zapletal
  - konflux: osbuild-composer use tasks with valid cosign (HMS-9721) (#4956)
    - Author: Florian Schüller, Reviewers: Sanne Raymaekers, Tomáš Hozza
  - osbuild-worker-executor: ignore item order in tarball in test (#4965)
    - Author: Achilleas Koutsou, Reviewers: Lukáš Zapletal, Michael Vogt
  - schutzfile: pin osbuild to version ignoring PQC keys (#4968)
    - Author: Ondřej Budai, Reviewers: Simon Steinbeiß
  - templates/openshift: switch to konflux images (HMS-9722) (#4957)
    - Author: Sanne Raymaekers, Reviewers: Nobody
  - test/{api,ubi}: pin cloud-tools to an older version (#4966)
    - Author: Ondřej Budai, Reviewers: Tomáš Hozza
  - worker: support separate set of s3 credentials (#4958)
    - Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli, Lukáš Zapletal, Tomáš Hozza

— Somewhere on the Internet, 2025-12-24


* Wed Dec 10 2025 Packit <hello@packit.dev> - 157-1
Changes with 157
----------------
  - .github/renovate: disable dockerfile updates (#4945)
    - Author: Sanne Raymaekers, Reviewers: Brian C. Lane
  - Red Hat Konflux update osbuild-composer-maintenance (HMS-9721) (#4951)
    - Author: red-hat-konflux[bot], Reviewers: Florian Schüller, Sanne Raymaekers
  - build(deps): bump golangci/golangci-lint-action from 6 to 9 (#4914)
    - Author: dependabot[bot], Reviewers: Achilleas Koutsou, Simon de Vlieger
  - chore(deps): update konflux references (#4948)
    - Author: red-hat-konflux[bot], Reviewers: Florian Schüller, Tomáš Hozza
  - cloudapi: add job progress to compose status (HMS-9341) (#4947)
    - Author: Sanne Raymaekers, Reviewers: Lukáš Zapletal, Michael Vogt
  - schutzbot: don't print the slack webhook url (#4944)
    - Author: Ondřej Budai, Reviewers: Sanne Raymaekers, Tomáš Hozza
  - templates/packer: retry vector start multiple times (#4953)
    - Author: Sanne Raymaekers, Reviewers: Ondřej Budai, Tomáš Hozza
  - test: disable cloud-image-validator (#4954)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Tomáš Hozza

— Somewhere on the Internet, 2025-12-10


* Wed Nov 12 2025 Packit <hello@packit.dev> - 155-1
Changes with 155
----------------
  - build(deps): bump actions/upload-artifact from 4 to 5 (#4906)
    - Author: dependabot[bot], Reviewers: Achilleas Koutsou, Sanne Raymaekers
  - chore: bump dependencies via gobump (#4907)
    - Author: SchutzBot, Reviewers: Florian Schüller, Lukáš Zapletal, Simon de Vlieger
  - chore: bump dependencies via gobump (#4912)
    - Author: SchutzBot, Reviewers: Sanne Raymaekers, Tomáš Hozza
  - cloudapi/v2: add netinst image type (HMS-9566) (#4913)
    - Author: Tomáš Koscielniak, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - schutzbot/terraform: bump terraform sha (#4909)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Florian Schüller, Lukáš Zapletal, Simon de Vlieger
  - weldr,cloudapi: tweaks around the reporegistry handling (#4910)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Brian C. Lane, Lukáš Zapletal

— Somewhere on the Internet, 2025-11-12


* Wed Oct 29 2025 Packit <hello@packit.dev> - 154-1
Changes with 154
----------------
  - CI: run testing on RHEL 9.8 and 10.2 nightly (HMS-9226) (#4893)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Update snapshots to 20251023 (#4905)
    - Author: SchutzBot, Reviewers: Sanne Raymaekers, Simon de Vlieger
  - chore: bump dependencies via gobump (#4895)
    - Author: SchutzBot, Reviewers: Achilleas Koutsou, Lukáš Zapletal, Simon de Vlieger
  - cloudapi: add new dnf customizations [HMS-9335] (#4899)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Tomáš Hozza
  - cloudapi: split out resolver job enqueueing into a separate function (#4894)
    - Author: Achilleas Koutsou, Reviewers: Sanne Raymaekers, Tomáš Hozza
  - fix worker AMI builds by not running mock as root (#4902)
    - Author: Ondřej Budai, Reviewers: Florian Schüller, Sanne Raymaekers
  - gitlab: only update github status at the end of the pipeline(s) (#4900)
    - Author: Achilleas Koutsou, Reviewers: Anna Vítová, Brian C. Lane, Sanne Raymaekers
  - go.mod: update images to v0.209.0 (#4901)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - go.mod: update osbuild/images to v0.208.0 (#4898)
    - Author: Sanne Raymaekers, Reviewers: Lukáš Zapletal, Ondřej Budai
  - test/cases/usbi-wsl: delete azure resources in order (#4896)
    - Author: Sanne Raymaekers, Reviewers: Simon de Vlieger, Tomáš Hozza
  - worker: support partial results (HMS-9343) (#4897)
    - Author: Sanne Raymaekers, Reviewers: Lukáš Zapletal, Tomáš Hozza

— Somewhere on the Internet, 2025-10-29


* Wed Oct 15 2025 Packit <hello@packit.dev> - 153-1
Changes with 153
----------------
  - CloudAPI: fix `/compose/{id}/manifests` endpoint behavior on manifest generation errors (HMS-9501) (#4885)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Michael Vogt
  - Many: adjust code to unified rpmmd.Package struct (HMS-9504) (#4889)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Test/api/gcp: set root partition size to at least 4 GiB (#4879)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Sanne Raymaekers, Simon de Vlieger
  - Update snapshots to 20251001 (#4880)
    - Author: SchutzBot, Reviewers: Sanne Raymaekers, Tomáš Hozza
  - build(deps): bump actions/setup-go from 5 to 6 (#4853)
    - Author: dependabot[bot], Reviewers: Simon de Vlieger, Tomáš Hozza
  - chore: bump dependencies via gobump (#4891)
    - Author: SchutzBot, Reviewers: Simon de Vlieger, Tomáš Hozza
  - cloudapi/v2: add pxe-tar-xz image type (HMS-9472) (#4882)
    - Author: Lucas Garfield, Reviewers: Sanne Raymaekers, Tomáš Hozza
  - executor: remove internet access entirely (HMS-9304) (#4884)
    - Author: Sanne Raymaekers, Reviewers: Brian C. Lane, Tomáš Hozza
  - go.mod: update osbuild/images to v0.202.0 (#4886)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - internal/cloudapi: rename OverrideSerializeManifestFunc for consistency (#4887)
    - Author: Tomáš Hozza, Reviewers: Michael Vogt, Simon de Vlieger
  - internal/worker: delete unneeded compatibility layers (HMS-9455) (#4875)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2025-10-15


* Wed Oct 01 2025 Packit <hello@packit.dev> - 152-1
Changes with 152
----------------
  - Remove internal/runner/ (#4874)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Gianluca Zuccarelli, Lukáš Zapletal, Michael Vogt
  - Weldr API endpoints & store: don't use `rpmmd` package structs for serialization (HMS-9376) (#4868)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Brian C. Lane, Sanne Raymaekers, Simon de Vlieger
  - chore: bump dependencies via gobump (#4872)
    - Author: SchutzBot, Reviewers: Lukáš Zapletal, Sanne Raymaekers
  - cloudapi/v2: recover from panics in serializeManifest (HMS-9379) (#4869)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Florian Schüller
  - go.mod: update osbuild/images to v0.198.0 (HMS-9444) (#4877)
    - Author: Achilleas Koutsou, Reviewers: Lukáš Zapletal, Sanne Raymaekers, Tomáš Hozza
  - go.mod: update to v0.197.0 (#4873)
    - Author: Michael Vogt, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - templates/packer/worker: remove unbound variable (#4871)
    - Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli, Tomáš Hozza
  - worker/executor: drop cloudwatch logging from executor (HMS-9304) (#4870)
    - Author: Sanne Raymaekers, Reviewers: Lukáš Zapletal, Tomáš Hozza

— Somewhere on the Internet, 2025-10-01


* Wed Sep 17 2025 Packit <hello@packit.dev> - 151-1
Changes with 151
----------------
  - Bump distro aliased for RHEL 9 and 10 (HMS-9174) (#4854)
    - Author: Tomáš Hozza, Reviewers: Gianluca Zuccarelli, Lukáš Zapletal, Sanne Raymaekers
  - Dockerfile-ubi-packer: do not use quay.io/app-sre/packer image (HMS-9246) (#4848)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  - Many: refactor 'osbuild-depsolve-dnf' mocking in tests to support refactoring in `osbuild/images` (HMS-9355) (#4862)
    - Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - Packer: install 'rsync' in the ubi-packer container (HMS-9287) (#4850)
    - Author: Tomáš Hozza, Reviewers: Michael Vogt, Sanne Raymaekers
  - build(deps): bump actions/github-script from 7 to 8 (#4852)
    - Author: dependabot[bot], Reviewers: Achilleas Koutsou, Lukáš Zapletal
  - gha: split gobump and images (#4859)
    - Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger
  - go.mod: update osbuild/images to 0.190.0 (`dnfjson` -> `depsolvednf` rename) (HMS-9365) (#4865)
    - Author: Tomáš Hozza, Reviewers: Lukáš Zapletal, Simon de Vlieger
  - go.mod: update osbuild/images to v0.188.0 (#4849)
    - Author: Achilleas Koutsou, Reviewers: Nobody
  - templates/packer: handle vector error (#4866)
    - Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli, Tomáš Hozza
  - test: run older CIV tag on nightlies (#4861)
    - Author: Achilleas Koutsou, Reviewers: Brian C. Lane, Simon de Vlieger
  - worker & executor: use vector to forward logs from executor to worker (HMS-9304) (#4858)
    - Author: Sanne Raymaekers, Reviewers: Lukáš Zapletal, Tomáš Hozza

— Somewhere on the Internet, 2025-09-17


* Wed Sep 03 2025 Packit <hello@packit.dev> - 150-1
Changes with 150
----------------
  - Test/regression-old-worker-new-composer: make the test case more robust (#4839)
    - Author: Tomáš Hozza, Reviewers: Lukáš Zapletal, Sanne Raymaekers
  - Update snapshots to 20250825 (#4840)
    - Author: SchutzBot, Reviewers: Sanne Raymaekers, Tomáš Hozza
  - test/cases/rhel-upgrade: increase virt-install memory (#4843)
    - Author: Sanne Raymaekers, Reviewers: Michael Vogt, Simon de Vlieger

— Somewhere on the Internet, 2025-09-03


* Thu Aug 21 2025 Packit <hello@packit.dev> - 149-1
Changes with 149
----------------
  - go.mod: bump images to v0.178.0 (#4837)
    - Author: Sanne Raymaekers, Reviewers: Michael Vogt, Simon de Vlieger
  - internal: use manifest build/payload pipelines (images#1766) (#4834)
    - Author: Michael Vogt, Reviewers: Brian C. Lane, Simon de Vlieger, Tomáš Hozza

— Somewhere on the Internet, 2025-08-21


* Fri Aug 15 2025 Maxwell G <maxwell@gtmx.me> - 147-2
- Rebuild for golang-1.25.0

* Wed Aug 06 2025 Packit <hello@packit.dev> - 147-1
Changes with 147
----------------
  * GH: remove the PR template (#4787)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Michael Vogt, Simon de Vlieger
  * Update snapshots to 20250730 (#4800)
    * Author: SchutzBot, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  * chore: bump dependencies via gobump (#4803)
    * Author: SchutzBot, Reviewers: Simon de Vlieger, Tomáš Hozza
  * cloudapi: new image type: azure-sapapps-rhui [HMS-8738] (#4790)
    * Author: Achilleas Koutsou, Reviewers: Michael Vogt, Tomáš Hozza
  * cloudapi: use distrofactory to get rhel-9.3 (#4789)
    * Author: Achilleas Koutsou, Reviewers: Michael Vogt, Tomáš Hozza
  * deps: update sentry dependency (#4771)
    * Author: Lukáš Zapletal, Reviewers: Simon de Vlieger, Tomáš Hozza
  * go.mod: update osbuild/images to v0.168.0 (#4799)
    * Author: Achilleas Koutsou, Reviewers: Sanne Raymaekers, Simon de Vlieger
  * jobqueue: handle escaped null bytes in postgres (HMS-8885) (#4779)
    * Author: Sanne Raymaekers, Reviewers: Lukáš Zapletal, Simon de Vlieger
  * many: fix various linter warnings (#4792)
    * Author: Lukáš Zapletal, Reviewers: Michael Vogt, Simon de Vlieger
  * many: switch to osbuild/images/pkg/upload for azure (HMS-8940) (#4798)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon de Vlieger, Tomáš Hozza
  * schutzbot/update_github_status.sh: fix GA pipeline status reporting (#4786)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  * templates/packer: avoid errors in worker-executor startup (#4788)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers, Tomáš Hozza
  * test/repositories: use CDN repos for 9.5, 9.6 and 10.0 (#4783)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Tomáš Koscielniak
  * workflows: use correct token for gobump (#4795)
    * Author: Lukáš Zapletal, Reviewers: Sanne Raymaekers, Simon de Vlieger

— Somewhere on the Internet, 2025-08-06


* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 146-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Packit <hello@packit.dev> - 146-1
Changes with 146
----------------
  *  go.mod: bump go version to 1.23.9 & update dependencies (#4760)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * Preparation to consolidate Koji upload code to `osbuild/images` (HMS-8803) (#4770)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli
  * Use Koji upload implementation from `osbuild/images` (HMS-8803) (#4772)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  * cloudapi: Use error 400 for cloudapi delete errors (#4750)
    * Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * deps: bump images to 0.164 (#4781)
    * Author: Simon de Vlieger, Reviewers: Ondřej Budai, Tomáš Hozza
  * go.mod: update osbuild/images to v0.156.0 (#4773)
    * Author: Achilleas Koutsou, Reviewers: Ondřej Budai, Sanne Raymaekers
  * test/ubi-wsl.sh: add backward compatibility for composer < v146 (#4784)
    * Author: Tomáš Hozza, Reviewers: Lukáš Zapletal, Tomáš Koscielniak
  * tests/CI: Add RHEL 9.6 and 10.0 GA (HMS-8726) (#4767)
    * Author: Tomáš Koscielniak, Reviewers: Florian Schüller, Sanne Raymaekers

— Somewhere on the Internet, 2025-07-23


* Wed Jul 09 2025 Packit <hello@packit.dev> - 145-1
Changes with 145
----------------
  * Test/repositories/el8*: use rhui-4 instead of rhui-3 (#4665)
    * Author: Tomáš Hozza, Reviewers: Gianluca Zuccarelli, Michael Vogt
  * Update snapshots to 20250626 (#4763)
    * Author: SchutzBot, Reviewers: Brian C. Lane, Tomáš Hozza
  * ci: introduce gobump gha (#4758)
    * Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  * cloudapi/v2: add patch_url to customizations (#4756)
    * Author: rverdile, Reviewers: Brian C. Lane, Tomáš Hozza
  * common: fix unclosed logrus logging pipes (#4728)
    * Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Simon de Vlieger, Tomáš Hozza
  * fix: update gobump GHA (#4761)
    * Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Sanne Raymaekers

— Somewhere on the Internet, 2025-07-09


* Wed Jun 25 2025 Packit <hello@packit.dev> - 144-1
Changes with 144
----------------
  * CI: disable know to be bad tests (#4754)
    * Author: Tomáš Hozza, Reviewers: Gianluca Zuccarelli, Lukáš Zapletal, Ondřej Budai, Simon de Vlieger
  * GHA: enable the stale action to delete its saved state (#4752)
    * Author: Tomáš Hozza, Reviewers: Lukáš Zapletal, Sanne Raymaekers, Simon de Vlieger
  * Schutzfile: Bump all osbuild hashes (#4748)
    * Author: Simon Steinbeiß, Reviewers: Sanne Raymaekers, Simon de Vlieger
  * Schutzfile: add fedora-42 (#4749)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * Stop testing on Fedora 40 - Start testing on Fedora 42 (#4745)
    * Author: Achilleas Koutsou, Reviewers: Gianluca Zuccarelli, Simon de Vlieger
  * Update snapshots to 20250605 (#4743)
    * Author: SchutzBot, Reviewers: Achilleas Koutsou, Brian C. Lane, Tomáš Hozza
  * cloudapi: Disk customization tweaks (adding swap), validation fixes, and tests (#4740)
    * Author: Achilleas Koutsou, Reviewers: Lukáš Zapletal, Simon de Vlieger, Tomáš Hozza
  * cloudapi: add azure-cvm image type (#4755)
    * Author: Achilleas Koutsou, Reviewers: Lukáš Zapletal, Sanne Raymaekers
  * deps: upgrade go-systemd from v1 to v22 (#4729)
    * Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger, Tomáš Hozza
  * go.mod: update osbuild/images to v0.151.0 (#4744)
    * Author: Achilleas Koutsou, Reviewers: Gianluca Zuccarelli, Simon de Vlieger
  * many: remove jobsite code (#4746)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli, Simon de Vlieger, Tomáš Hozza
  * templates/packer: fix installing rpms from copr (#4753)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli, Tomáš Hozza

— Somewhere on the Internet, 2025-06-25


* Wed Jun 11 2025 Packit <hello@packit.dev> - 143-1
Changes with 143
----------------
  * Add job delete support (#4717)
    * Author: Brian C. Lane, Reviewers: Tomáš Hozza
  * GH Action/create-tag: allow passing the version when run manually (#4668)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * Improve OCI CI scripts (HMS-8591) (#4742)
    * Author: Florian Schüller, Reviewers: Achilleas Koutsou, Brian C. Lane, Lukáš Zapletal
  * Packer: update Fedora and RHEL images used for workers (#4733)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli
  * gitlab: enable OCI tests (#4741)
    * Author: Achilleas Koutsou, Reviewers: Florian Schüller, Simon de Vlieger, Tomáš Hozza
  * go.mod: update osbuild/images to v0.148.0 (#4732)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza, Tomáš Koscielniak
  * osbuild-store-dump: use `distrofactory` instead of importing fedora (#4738)
    * Author: Michael Vogt, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * tests/CI: Add runners for RHEL 9.7 and 10.1 (HMS-6278) (#4716)
    * Author: Tomáš Koscielniak, Reviewers: Achilleas Koutsou, Tomáš Hozza

— Somewhere on the Internet, 2025-06-11


* Wed May 28 2025 Packit <hello@packit.dev> - 142-1
Changes with 142
----------------
  * Update snapshots to 20250515 (#4724)
    * Author: SchutzBot, Reviewers: Simon de Vlieger, Tomáš Hozza
  * templates/packer: set wanted-by to cloud-init.target (#4723)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli, Lukáš Zapletal, Ondřej Budai

— Somewhere on the Internet, 2025-05-28


* Wed May 14 2025 Packit <hello@packit.dev> - 141-1
Changes with 141
----------------
  * Add templates to subscription image options (HMS-6050) (#4712)
    * Author: rverdile, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * Replace logrus with log (#4715)
    * Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * Test/cross-distro: add version check for cross-building el8 on el9 (#4706)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Brian C. Lane
  * Test/cross-distro: fix one issue and make the test more robust on "ZStream" branches (#4694)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  * cloudapi: Fix missing specs for koji ContainerResolve (#4709)
    * Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  * cloudapi: drop ImageRequest.GetImageOptions() method (#4711)
    * Author: Achilleas Koutsou, Reviewers: Michael Vogt, Sanne Raymaekers
  * go.mod: bump images to v0.144.0 (#4718)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller, Lukáš Zapletal, Simon de Vlieger
  * go.mod: update osbuild/images to v0.143.0 (#4713)
    * Author: Achilleas Koutsou, Reviewers: Michael Vogt, Sanne Raymaekers
  * internal: drop `internal/fsnode` package (#4714)
    * Author: Michael Vogt, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2025-05-14


* Tue Apr 22 2025 Packit <hello@packit.dev> - 139-1
Changes with 139
----------------
  * Delete internal/blueprint/ and import from osbuild/blueprint (#4659)
    * Author: Achilleas Koutsou, Reviewers: Michael Vogt, Simon de Vlieger
  * Disable vmware tests and verification step in vsphere builds (#4680)
    * Author: Achilleas Koutsou, Reviewers: Ondřej Budai, Tomáš Hozza
  * Update snapshots to 20250417 (#4683)
    * Author: SchutzBot, Reviewers: Achilleas Koutsou, Sanne Raymaekers
  * go.mod: update jwt-go to v4.5.2 and v5.2.2 to fix CVE-2025-30204 (HMS-5996) (#4684)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Lukáš Zapletal
  * go.mod: update osbuild/images to v0.134.1-0.20250416092909-a1ca7f (#4686)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou
  * test/data/repositories: fix snapshot dates (#4687)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou
  * update packit validate-config command (#4685)
    * Author: Irina Gulina, Reviewers: Sanne Raymaekers

— Somewhere on the Internet, 2025-04-22


* Wed Apr 16 2025 Packit <hello@packit.dev> - 138-1
Changes with 138
----------------
  * GH Action: check the SPEC osbuild/images deps minimum version (#4669)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * client/blueprints_test.go: delete condition for composer version < 83 (#4673)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2025-04-16


* Wed Apr 02 2025 Packit <hello@packit.dev> - 137-1
Changes with 137
----------------
  * Add modularity support (#4644)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * Advanced partitioning customizations in cloud API (COMPOSER-2403) (#4650)
    * Author: Achilleas Koutsou, Reviewers: Sanne Raymaekers
  * Fix: osbuild-composer is not able to build RHEL-8 images since RHEL-9.5 (RHEL-71397) (#4651)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * Schutzfile: bump osbuild to 142 (#4653)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * Test/api.sh/vsphere: configure cloud-init via VM's extraConfig (#4664)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Tomáš Koscielniak
  * cloudapi/v2: mark md5 signature as required in package metadata (#4654)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou
  * go.mod: bump github.com/getkin/kin-openapi to v0.131.0 (#4655)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Ondřej Budai
  * test: migrate the openshift virt test to a new cluster (COMPOSER-2458) (#4647)
    * Author: Ondřej Budai, Reviewers: Tomáš Koscielniak

— Somewhere on the Internet, 2025-04-02


* Wed Mar 19 2025 Packit <hello@packit.dev> - 136-1
Changes with 136
----------------
  * Return compose request details as part of metadata response (#4451)
    * Author: Brian C. Lane, Reviewers: Florian Schüller, Tomáš Hozza
  * cloudapi: silence logrus in tests (#4614)
    * Author: Michael Vogt, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * go.mod: update osbuild/images to v0.123.0 (#4642)
    * Author: Sanne Raymaekers, Reviewers: Simon Steinbeiß, Simon de Vlieger
  * templates/dashboards: increase timespan readability (#4633)
    * Author: Florian Schüller, Reviewers: Gianluca Zuccarelli, Sanne Raymaekers

— Somewhere on the Internet, 2025-03-19


* Wed Mar 05 2025 Packit <hello@packit.dev> - 135-1
Changes with 135
----------------
  * CI: Update slack notifications and remove Alex (#4623)
    * Author: Tomáš Koscielniak, Reviewers: Achilleas Koutsou, Simon Steinbeiß, Tomáš Hozza
  * CODEOWNERS: set people for `/templates` (#4636)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers, Tomáš Hozza
  * Preparation for RHEL 9.7 and 10.1 (COMPOSER-2451) (#4629)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Ondřej Budai
  * Update snapshots to 20250225 (#4626)
    * Author: SchutzBot, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * Use golangci-lint v1.60 and cleanup the errors it returns (#4612)
    * Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Florian Schüller
  * cloudapi: Use constants for distro in compose_test.go (#4620)
    * Author: Brian C. Lane, Reviewers: Achilleas Koutsou, Michael Vogt
  * internal/cloud/gcp/compute: Add TDX_CAPABLE guest OS feature (#4587)
    * Author: Beñat Gartzia, Reviewers: Ondřej Budai, Tomáš Hozza
  * tests/CI: Disable installer test for RHEL 10.0 nightly (#4634)
    * Author: Tomáš Koscielniak, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * tests/CI: Re-enable the vmware tests on RHEL 10 (#4577)
    * Author: Tomáš Koscielniak, Reviewers: Ondřej Budai, Tomáš Hozza

— Somewhere on the Internet, 2025-03-05


* Thu Feb 20 2025 Packit <hello@packit.dev> - 134-1
Changes with 134
----------------
  * Update snapshots to 20250218 (#4616)
    * Author: SchutzBot, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * build(deps): bump stackrox/kube-linter-action from 1.0.5 to 1.0.6 (#4565)
    * Author: dependabot[bot], Reviewers: Ondřej Budai
  * go.mod: update osbuild/images to v0.118.0 (#4617)
    * Author: Achilleas Koutsou, Reviewers: Michael Vogt, Tomáš Hozza
  * many: update for new reporegistry.New() api (c.f. pr#1179) (#4603)
    * Author: Michael Vogt, Reviewers: Achilleas Koutsou, Brian C. Lane

— Somewhere on the Internet, 2025-02-20


* Wed Feb 12 2025 Packit <hello@packit.dev> - 132-1
Changes with 132
----------------
  * Add support for advanced partitioning customizations (COMPOSER-2399) (#4535)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza
  * ITM26 last-minute fixes (#4609)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Michael Vogt, Simon de Vlieger
  * cloudapi download (#4590)
    * Author: Brian C. Lane, Reviewers: Gianluca Zuccarelli, Tomáš Hozza
  * go.mod: update to latest images@v0.115.0 (#4599)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza

— Somewhere on the Internet, 2025-02-12


* Wed Feb 05 2025 Packit <hello@packit.dev> - 131-1
Changes with 131
----------------
  * Update snapshots to 20250201 (#4591)
    * Author: SchutzBot, Reviewers: Achilleas Koutsou
  * cloudapi: Add /distributions/ to cloudapi (#4336)
    * Author: Brian C. Lane, Reviewers: Gianluca Zuccarelli

— Somewhere on the Internet, 2025-02-05


* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 129-2
- Add explicit BR: libxcrypt-devel

* Wed Jan 22 2025 Packit <hello@packit.dev> - 129-1
Changes with 129
----------------
  * Fix non-constant log strings (#4563)
    * Author: Brian C. Lane, Reviewers: Michael Vogt
  * README: remove mailing list (#4562)
    * Author: Florian Schüller, Reviewers: Ondřej Budai
  * blueprint: add cacert customization (#4487)
    * Author: Lukáš Zapletal, Reviewers: Tomáš Hozza
  * build(deps): bump deps specifically CVE-2024-45338 (#4545)
    * Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou
  * many: update images Manifest() API for PR#1107 (#4539)
    * Author: Michael Vogt, Reviewers: Tomáš Hozza

— Somewhere on the Internet, 2025-01-22


* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 128-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Packit <hello@packit.dev> - 128-1
Changes with 128
----------------
  * Exclude vendor directory ci: do not perform linting on vendor/from linting (#4547)
    * Author: Lukáš Zapletal, Reviewers: Brian C. Lane, Michael Vogt
  * github/actions: Enable /jira-epic slash commands (HMS-5161) (#4529)
    * Author: Simon Steinbeiß, Reviewers: Ondřej Budai
  * go.mod: upgrade golang.org/x/crypto (#4526)
    * Author: Florian Schüller, Reviewers: Ondřej Budai
  * schutzbot: update Achilleas' ssh keys (#4538)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza
  * upgrade_verify.sh: update el10 repo URLs to non-Beta (#4534)
    * Author: Tomáš Hozza, Reviewers: Tomáš Koscielniak

— Somewhere on the Internet, 2025-01-08


* Wed Dec 11 2024 Packit <hello@packit.dev> - 127-1
Changes with 127
----------------
  * CI: remove jrusz from notifications (#4505)
    * Author: Jakub Rusz, Reviewers: Ondřej Budai
  * Clean up orphaned instances and security groups (HMS-3632) (#4513)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers
  * Update osbuild/images to v0.105.0 (COMPOSER-2357, COMPOSER-2400) (#4519)
    * Author: Tomáš Hozza, Reviewers: Ondřej Budai
  * Update snapshots to 20241203 (#4512)
    * Author: SchutzBot, Reviewers: Tomáš Hozza
  * Verify hyperv gen (HMS-5090) (#4497)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * build(deps): bump codecov/codecov-action from 4 to 5 (#4476)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * cloud/awscloud: exclude really old instance types (#4496)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * cloud/awscloud: give secure instances a name (#4504)
    * Author: Sanne Raymaekers, Reviewers: Lukáš Zapletal, Ondřej Budai
  * cloud/awscloud: use any instance create fleet returns (#4507)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * cloudapi: carry ostree MTLS secret over (#4508)
    * Author: Lukáš Zapletal, Reviewers: Sanne Raymaekers
  * cmd: extra env logging for osbuild worker (#4495)
    * Author: Lukáš Zapletal, Reviewers: Michael Vogt
  * deps: update images to 0.102 (#4499)
    * Author: Lukáš Zapletal, Reviewers: Tomáš Hozza
  * github: prevent script injections via PR branch names (#4511)
    * Author: Ondřej Budai, Reviewers: Achilleas Koutsou
  * tests: Bump RHEL 10 from beta to nightly and update osbuild deps SHA (#4501)
    * Author: Tomáš Koscielniak, Reviewers: Sanne Raymaekers
  * tools/tests: Update rhel10 compose url (#4518)
    * Author: Tomáš Koscielniak, Reviewers: Tomáš Hozza

— Somewhere on the Internet, 2024-12-11


* Wed Nov 27 2024 Packit <hello@packit.dev> - 126-1
Changes with 126
----------------
  * Schutzfile: update osbuild commit (COMPOSER-2406) (#4490)
    * Author: Sanne Raymaekers, Reviewers: Tomáš Hozza
  * Support customizing azure HyperV generation (HMS-4986) (#4470)
    * Author: Sanne Raymaekers, Reviewers: Brian C. Lane
  * Test with rhel-9.6 nightly (#4468)
    * Author: Tomáš Koscielniak, Reviewers: Jakub Rusz
  * awscloud/secure-instance: enrich logging with secure instance id (#4479)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers
  * awscloud/secure-instance: fix cleaning up fleets with creation errors (#4489)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * awscloud/secure-instance: retry on error in terminated waiter (#4485)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers
  * awscloud: add very verbose logging to createFleet creation (COMPOSER-2407) (#4494)
    * Author: Ondřej Budai, Reviewers: Florian Schüller, Sanne Raymaekers
  * deps: update images to 0.99 (#4481)
    * Author: Lukáš Zapletal, Reviewers: Simon de Vlieger
  * internal/worker/server: return an error on depsolve timeout (HMS-2989) (#4398)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers
  * templates/composer: bump rhel-9 distro alias (#4492)
    * Author: Sanne Raymaekers, Reviewers: Tomáš Hozza
  * worker: check MTLS proxy for nil (#4472)
    * Author: Lukáš Zapletal, Reviewers: Ondřej Ezr
  * worker: log proxy setting (#4477)
    * Author: Lukáš Zapletal, Reviewers: Sanne Raymaekers
  * worker: report cashes directly to logrus (#4482)
    * Author: Michael Vogt, Reviewers: Lukáš Zapletal, Sanne Raymaekers

— Somewhere on the Internet, 2024-11-27


* Wed Nov 13 2024 Packit <hello@packit.dev> - 125-1
Changes with 125
----------------
  * Implement running db tests locally (#4431)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers
  * Introduce grafana number of pending jobs (#4462)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers
  * Makefile: clean golangci-lint cache on `make clean` (#4444)
    * Author: Florian Schüller, Reviewers: Brian C. Lane
  * Test/data: add test repo configs for RHEL-9.6 (#4456)
    * Author: Tomáš Hozza, Reviewers: Ondřej Budai
  * cloud/awscloud: don't specify max spot price (#4446)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller, Ondřej Budai
  * go.mod: update osbuild/images to v0.95.0 (#4448)
    * Author: Achilleas Koutsou, Reviewers: Lukáš Zapletal, Tomáš Hozza
  * osbuild-worker: use the new ostree resolver API (HMS-4773) (#4412)
    * Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou
  * worker/server: update metrics on requeue (#4461)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * worker: check MTLS config for ostree (#4467)
    * Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Sanne Raymaekers

— Somewhere on the Internet, 2024-11-13


* Wed Oct 30 2024 Packit <hello@packit.dev> - 124-1
Changes with 124
----------------
  * Enable the anaconda modules customization (#4421)
    * Author: Achilleas Koutsou, Reviewers: Ondřej Budai, Simon de Vlieger
  * Remove leftover secure instances in service maintenance (#4420)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * Update snapshots to 20241015 (#4410)
    * Author: SchutzBot, Reviewers: Achilleas Koutsou
  * cloud/awscloud: fix another nilpointer in maintenance functions (#4442)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * cloud/awscloud: fix nil pointer dereference in maintenance fns (#4434)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * cloud/awscloud: fix retrying to create secure instances (#4437)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * cloud/awscloud: rework create fleet retry logic (#4430)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * cmd/osbuild-service-maintenance: respect dry run (#4428)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * deps: update images to 0.94 (#4439)
    * Author: Simon de Vlieger, Reviewers: Achilleas Koutsou
  * packer: don't deregister old AMIs (COMPOSER-2376) (#4418)
    * Author: Ondřej Budai, Reviewers: Sanne Raymaekers
  * repositories: add fedora 41 (#4389)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * schutzbot: shorten the slack notification (#4433)
    * Author: Ondřej Budai, Reviewers: Jakub Rusz, Sanne Raymaekers
  * templates/packer: allow setting executor type in worker config (#4441)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai, Simon de Vlieger
  * templates/packer: fix fedora 40 aarch64 base image (#4450)
    * Author: Sanne Raymaekers, Reviewers: Tomáš Hozza
  * tests/packer: Disable Packer job in scheduled GA pipelines (#4419)
    * Author: tkoscieln, Reviewers: Ondřej Budai
  * worker: fix OSBUILD_SOURCES_CURL_SSL_CA_CERT variable (#4423)
    * Author: Lukáš Zapletal, Reviewers: Achilleas Koutsou, Simon de Vlieger

— Somewhere on the Internet, 2024-10-30


* Wed Oct 16 2024 Packit <hello@packit.dev> - 123-1
Changes with 123
----------------
  * cloud/aws: add a third secure instance fallback across AZs (#4401)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * cloud/awscloud: retry CreateFleet regardless of the error code (#4413)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller, Lukáš Zapletal
  * repositories: add rhel-9.6 (#4408)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * test: disable ostree-remount service checking since /sysroot is ro and /var rw already (#4394)
    * Author: mcattamoredhat, Reviewers: Sayan Paul, Simon de Vlieger
  * tests/filesystem: increase /usr size (#4400)
    * Author: Jakub Rusz, Reviewers: Achilleas Koutsou
  * tests/regression: Add config for v3 certificates (#4395)
    * Author: Jakub Rusz, Reviewers: Florian Schüller

— Somewhere on the Internet, 2024-10-16


* Wed Oct 02 2024 Packit <hello@packit.dev> - 122-1
Changes with 122
----------------
  * Add fedora-41 (#4369)
    * Author: Sanne Raymaekers, Reviewers: Brian C. Lane
  * CI: integration test rules fixup (#4383)
    * Author: Jakub Rusz, Reviewers: Brian C. Lane
  * Revert "Add fedora-41" (#4380)
    * Author: Sanne Raymaekers, Reviewers: Jakub Rusz
  * Update snapshots to 20240924 (#4381)
    * Author: SchutzBot, Reviewers: Tomáš Hozza
  * cloud: fixed typo UnfulfillableCapacity (HMS-4676) (#4385)
    * Author: Lukáš Zapletal, Reviewers: Sanne Raymaekers
  * composer: don't create RepoRegistry using reporegistry.New() (#4378)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou
  * test/cases: Use openscap customization + enable oci api test on RHEL-10  (#4356)
    * Author: Jakub Rusz, Reviewers: Tomáš Hozza

— Somewhere on the Internet, 2024-10-02


* Fri Sep 20 2024 Packit <hello@packit.dev> - 121-1
Changes with 121
----------------
  * Add initial support for generating SPDX SBOM documents (COMPOSER-2274) (#4359)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Florian Schüller, Gianluca Zuccarelli

— Somewhere on the Internet, 2024-09-20


* Wed Sep 18 2024 Packit <hello@packit.dev> - 120-1
Changes with 120
----------------
  * Openscap compliance facts (HMS-2836) (#4349)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli
  * Update Fedora-40 repositories to branched ones (#4355)
    * Author: Jakub Rusz, Reviewers: Sanne Raymaekers
  * blueprint: sshkey to users in images blueprint conversion (#4363)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza
  * internal/worker/client.go: refactor reading worker ID (#4351)
    * Author: Florian Schüller, Reviewers: Michael Vogt, Sanne Raymaekers
  * osbuild-worker: fix "crashing" on worker registration issues (#4357)
    * Author: Michael Vogt, Reviewers: Florian Schüller, Sanne Raymaekers
  * test/cases: adapt upgrade to support rhel9to10 (#4319)
    * Author: Jakub Rusz, Reviewers: Tomáš Hozza
  * tools/build-rpms: fix ec2 client initialisation (#4361)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * tools/build-rpms: increase rpm builder instance disk size (#4360)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * upload/azure: turn off public access on storage accounts (#4353)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Ondřej Budai

— Somewhere on the Internet, 2024-09-18


* Wed Sep 04 2024 Packit <hello@packit.dev> - 119-1
Changes with 119
----------------
  * Add channel to worker logs (#4316)
    * Author: Florian Schüller, Reviewers: Brian C. Lane
  * Update osbuild/images to v0.82.0 (#4343)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou
  * Worker: move GCE image guest OS features to upload target options (#4334)
    * Author: Tomáš Hozza, Reviewers: Brian C. Lane
  * build(deps): bump the go-deps group across 1 directory with 13 updates (#4337)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump the go-deps group across 1 directory with 2 updates (#4342)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * osbuild-composer: add `Requires: osbuild-dnf-json-api = 7` (#4308)
    * Author: Michael Vogt, Reviewers: Brian C. Lane, Tomáš Hozza
  * osbuild-worker: handle error wrapping from dnfjson package (#4341)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller, Michael Vogt
  * tools/appsre-ansible: fix unregister (#4326)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * tools/build-rpms: increase size of instances (#4338)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * tools/build-rpms: use rhel 9.4 instances as a baseline (#4344)
    * Author: Sanne Raymaekers, Reviewers: Tomáš Hozza
  * worker: move `api.BasePath` setup to the start of the funcs (#4328)
    * Author: Michael Vogt, Reviewers: Florian Schüller, Tomáš Hozza
  * worker: rename `server` -> `serverURL` (#4325)
    * Author: Michael Vogt, Reviewers: Florian Schüller, Sanne Raymaekers
  * worker: simplify the `POST` in workerHeartbeat() (#4327)
    * Author: Michael Vogt, Reviewers: Florian Schüller, Sanne Raymaekers

— Somewhere on the Internet, 2024-09-04


* Fri Aug 23 2024 Packit <hello@packit.dev> - 118-1
Changes with 118
----------------
  * [RHEL-10] Add `gce` and `image-installer` image types (COMPOSER-2193) (#4314)
    * Author: Tomáš Hozza, Reviewers: Gianluca Zuccarelli
  * tools/appsre-ansible: retry subscribing rpmbuild machines (#4317)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller

— Somewhere on the Internet, 2024-08-23


* Wed Aug 21 2024 Packit <hello@packit.dev> - 117-1
Changes with 117
----------------
  * Add rhel-10.0 image manifests and enable image_tests (#4307)
    * Author: Jakub Rusz, Reviewers: Tomáš Hozza
  * ci: fix edge test failures in cs9 and fedora40 (#4309)
    * Author: He Yi, Reviewers: Achilleas Koutsou
  * cloud/awscloud: aws sdk v2 (HMS-4538) (#4287)
    * Author: Sanne Raymaekers, Reviewers: Michael Vogt

— Somewhere on the Internet, 2024-08-21


* Thu Aug 15 2024 Packit <hello@packit.dev> - 116-1
Changes with 116
----------------
  * Integration testing on CS10 & RHEL 10 (#4263)
    * Author: Alexander Todorov, Reviewers: Tomáš Hozza
  * OpenSCAP json tailoring (HMS-3827) (#4272)
    * Author: Gianluca Zuccarelli, Reviewers: Sanne Raymaekers
  * Update images to `v0.77.0` and enable `rpm` and `rhsm` customizations (COMPOSER-2308) (#4295)
    * Author: Tomáš Hozza, Reviewers: Gianluca Zuccarelli
  * ci: move rhel for edge rhel9.5 test to testing-farm (#4240)
    * Author: He Yi, Reviewers: Achilleas Koutsou
  * logrus: add deployment channel as field to the logs (#4285)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers, Tomáš Hozza
  * osbuild-composer: activate deployment-channel reporting for splunk (#4299)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers
  * prepare-source: Move go fmt to last step (#4296)
    * Author: Brian C. Lane, Reviewers: Achilleas Koutsou
  * splunk_logger: move environment hook to splunk_logger pt1 (#4301)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers

— Somewhere on the Internet, 2024-08-15


* Wed Aug 07 2024 Packit <hello@packit.dev> - 115-1
Changes with 115
----------------
  * Change log_format for the service to json (#4279)
    * Author: Florian Schüller, Reviewers: Sanne Raymaekers
  * Makefile for templates/openshift (#4103)
    * Author: Florian Schüller, Reviewers: Brian C. Lane
  * build(deps): bump the go-deps group across 1 directory with 8 updates (#4274)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * clienterrors: rename `WorkerClientError` to `clienterrors.New` (#4278)
    * Author: Michael Vogt, Reviewers: Sanne Raymaekers
  * cloud/awscloud: fix nil pointer dereference (#4283)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * dbjobqueue: correct error wrapping (#4284)
    * Author: Sanne Raymaekers, Reviewers: Michael Vogt
  * osbuild-worker: rework the `workerClientErrorFrom()` error (#4254)
    * Author: Michael Vogt, Reviewers: Tomáš Hozza
  * osbuildexecutor: show full osbuild exector on json decode errors (#4289)
    * Author: Michael Vogt, Reviewers: Sanne Raymaekers
  * test/api: silent dump_db() (#4276)
    * Author: Achilleas Koutsou, Reviewers: Jakub Rusz, Tomáš Hozza

— Somewhere on the Internet, 2024-08-07


* Wed Jul 24 2024 Packit <hello@packit.dev> - 114-1
Changes with 114
----------------
  * (HMS-4453) Add password to User customization schema (#4267)
    * Author: Andrea Waltlová, Reviewers: Ondřej Ezr
  * Build RPMs on RHEL-10.0-nightly and c10s (COMPOSER-2161) (#4268)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Alexander Todorov
  * Create a nightly pipeline for GA/EUS releases (#4046)
    * Author: tkoscieln, Reviewers: Nobody
  * Fix distro alias loading from ENV (#4265)
    * Author: Tomáš Hozza, Reviewers: Sanne Raymaekers
  * Fix slack GA pipeline notification job failure (#4271)
    * Author: tkoscieln, Reviewers: Alexander Todorov, Jakub Rusz
  * schutzbot/terraform: bump sha (#4266)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou

— Somewhere on the Internet, 2024-07-24


* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 113-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Packit <hello@packit.dev> - 113-1
Changes with 113
----------------
  * build(deps): bump the go-deps group across 1 directory with 10 updates (#4259)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * osbuild-worker: tweak error to not include a \n for a failed stage (#4257)
    * Author: Michael Vogt, Reviewers: Tomáš Hozza
  * repositories: update Fedora 40 gpg keys (#4258)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza

— Somewhere on the Internet, 2024-07-11


* Wed Jun 12 2024 Packit <hello@packit.dev> - 110-1
Changes with 110
----------------
  * :broom: Add c10s and el10 repos, update distro aliases, update SPEC, c8s EOL (#4179)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Alexander Todorov, Florian Schüller, Simon de Vlieger
  * Fix condition in `tools/provision.sh` for el10 and re-enable snapshot URL validation (#4186)
    * Author: Tomáš Hozza, Reviewers: Alexander Todorov
  * GH actions / containerfiles: update F37 to F40 (#4168)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou
  * Testing with rhel-9.5 nightly (#4126)
    * Author: Alexander Todorov, Reviewers: Jakub Rusz
  * cmd/osbuild-worker-executor: add oaas as worker executor (#4189)
    * Author: Michael Vogt, Reviewers: Sanne Raymaekers
  * go.mod: bump osbuild/images to v0.65.0 (#4198)
    * Author: Achilleas Koutsou, Reviewers: Sanne Raymaekers
  * main: rework the way the mock logger is passed (#4196)
    * Author: Michael Vogt, Reviewers: Tomáš Hozza
  * obuild-worker: extract workerClientErrorFrom() helper and add tests (#4188)
    * Author: Michael Vogt, Reviewers: Achilleas Koutsou, Florian Schüller
  * osbuild-worker-executor: fix order of `assert.Equal()` in tests (#4192)
    * Author: Michael Vogt, Reviewers: Brian C. Lane
  * osbuild-worker-executor: make test output silent again (#4191)
    * Author: Michael Vogt, Reviewers: Sanne Raymaekers
  * osbuild-worker: do not use `error` in clienterror.Error.Details (#4145)
    * Author: Michael Vogt, Reviewers: Florian Schüller
  * templates/openshift/composer: remove maintenance cronjob (#4178)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * templates/packer: switch to fedora-40 (#4162)
    * Author: Sanne Raymaekers, Reviewers: Tomáš Hozza
  * templates/packer: use import_tasks instead of include_tasks (#4176)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * test/cases/ubi-wsl: test rhel9 ga (HMS-4207) (#4165)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli
  * test: skip ostree-remount due to issue RHEL-25249 (#4121)
    * Author: mcattamoredhat, Reviewers: Achilleas Koutsou, Xiaofeng Wang
  * test: update ostree osname in pending test cases (#4173)
    * Author: mcattamoredhat, Reviewers: Achilleas Koutsou

— Somewhere on the Internet, 2024-06-12


* Wed May 29 2024 Packit <hello@packit.dev> - 109-1
Changes with 109
----------------
  * Add RHEL-9.5 repo definitions (#4158)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou
  * Add support for arbitrary kickstart file injection into ISOs (HMS-3879) (#4135)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza
  * Minor user customization test improvements (#4007)
    * Author: andremarianiello, Reviewers: Brian C. Lane
  * templates/packer: invert tag logic (#4150)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller, Ondřej Budai
  * test: execute dmesg task as privileged user (#4094)
    * Author: mcattamoredhat, Reviewers: Achilleas Koutsou, Brian C. Lane

— Somewhere on the Internet, 2024-05-29


* Wed May 15 2024 Packit <hello@packit.dev> - 108-1
Changes with 108
----------------
  * Reenable codecov via action (#4119)
    * Author: Alexander Todorov, Reviewers: Jakub Rusz
  * Update osbuild/images v0.59.0 (HMS-4031) (#4127)
    * Author: Achilleas Koutsou, Reviewers: Sanne Raymaekers, Tomáš Hozza
  * Use copr rpms for the community workers (#4129)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * build(deps): bump github.com/docker/docker from 25.0.3+incompatible to 25.0.5+incompatible (#4080)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump github.com/go-jose/go-jose/v3 from 3.0.1 to 3.0.3 (#4000)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump golangci/golangci-lint-action from 4 to 5 (#4110)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump gopkg.in/go-jose/go-jose.v2 from 2.6.1 to 2.6.3 (#3999)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump the go-deps group across 1 directory with 14 updates (#4123)
    * Author: dependabot[bot], Reviewers: Achilleas Koutsou, Ondřej Budai, Tomáš Hozza
  * cloudapi: Add UploadTypesLocal for local_save status reports (#4038)
    * Author: Brian C. Lane, Reviewers: Simon Steinbeiß
  * templates/dashboards: fix community-stage tenant variable (#4100)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * templates/packer: add failure script (#4101)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai, Tomáš Hozza
  * test: update osname for edge deployments (#4148)
    * Author: mcattamoredhat, Reviewers: Achilleas Koutsou
  * tools/fedora-worker-packer: increase timeout further (#4134)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * tools/fedora-worker-packer: small fixes (commit sha + timeout increase) (#4133)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller

— Somewhere on the Internet, 2024-05-15


* Wed Apr 24 2024 Packit <hello@packit.dev> - 106-1
Changes with 106
----------------
  * Active worker gauge (COMPOSER-2215) (#4089)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli
  * Add CI job to detect possible problematic usage of `trap` (#3977)
    * Author: Alexander Todorov, Reviewers: Tomáš Hozza
  * Makefile: remove installation of dnf-json (#4076)
    * Author: Achilleas Koutsou, Reviewers: Sanne Raymaekers
  * Show worker count on grafana dashboard (COMPOSER-2215) (#4092)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * Update Arm EC2 instance to a newer one (#4064)
    * Author: Alexander Todorov, Reviewers: Jakub Rusz
  * Update osbuild/images to v0.56.0 (#4096)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Ondřej Budai
  * configurable worker timeouts (COMPOSER-2215) (#4090)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller
  * osbuild-worker: fix mtls credentials injection in depsolve job (#4082)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Brian C. Lane
  * osbuild-worker: fix nil pointer in depsolve job (#4086)
    * Author: Sanne Raymaekers, Reviewers: Florian Schüller, Tomáš Hozza
  * osbuild/images 0.55 (#4075)
    * Author: Sanne Raymaekers, Reviewers: Brian C. Lane
  * osbuildexecutor/ec2: pass extraEnv only to sources invocation (#4083)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon Steinbeiß
  * templates/packer: fix proxy config in ldap service account init (#4098)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou
  * tests: Fix leapp repo url (#4085)
    * Author: Jakub Rusz, Reviewers: Alexander Todorov
  * worker: support http proxy for depsolve and osbuild sources job HMS-3798 (#4066)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou

— Somewhere on the Internet, 2024-04-24


* Wed Apr 03 2024 Packit <hello@packit.dev> - 104-1
Changes with 104
----------------
  * Add installer customizations to blueprints and cloud API (HMS-1161) (#4005)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza
  * Execute OpenShift Virtualization tests only on RHEL 9.x nightly (#4044)
    * Author: Alexander Todorov, Reviewers: Jakub Rusz, Tomáš Hozza
  * bump osbuild/images to 51 and add expiredate fields to user customizations (#4041)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * cloud/awscloud: allow internet access on secure instance again (#4025)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou
  * cloudapi: Override the request distro with the blueprint distro (#4006)
    * Author: Brian C. Lane, Reviewers: Achilleas Koutsou
  * osbuild-jobsite-builder: disable http.Server timeouts (#4031)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * osbuild-jobsite-manager: close writer before sending the store (#4029)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * osbuild-jobsite: increase populate timeout (#4027)
    * Author: Sanne Raymaekers, Reviewers: Michael Vogt, Simon de Vlieger
  * osbuild-worker: add support for mtls dnf repo secrets (HMS-3798) (#4035)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * repositories: remove rhel-8-beta (#4024)
    * Author: Simon de Vlieger, Reviewers: Tomáš Hozza
  * templates/packer: support ldap service account for repo mtls conf (#4049)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * test: drop oscap test script and gitlab job (HMS-3710) (#3991)
    * Author: Achilleas Koutsou, Reviewers: Simon Steinbeiß
  * worker: drop backwards compatibility for DepsolveJob serialisation (COMPOSER-1612) (#4021)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza

— Somewhere on the Internet, 2024-04-03


* Wed Mar 06 2024 Packit <hello@packit.dev> - 102-1
Changes with 102
----------------
  * CI: Drop SonarQube in favor of Snyk (#3984)
    * Author: Jakub Rusz, Reviewers: Simon Steinbeiß
  * Enable masked systemd services in cloudapi (HMS-3661) (#3972)
    * Author: Gianluca Zuccarelli, Reviewers: Brian C. Lane, Tomáš Hozza
  * Enable testing in OpenShift (#3681)
    * Author: Alexander Todorov, Reviewers: Jakub Rusz, Tomáš Hozza
  * README: Fix reference to developer guide (#3969)
    * Author: Brian C. Lane, Reviewers: Tomáš Hozza
  * Skip Image Tests tests for image types already covered in osbuild/images (#3967)
    * Author: Alexander Todorov, Reviewers: Jakub Rusz, Tomáš Hozza
  * build(deps): bump golangci/golangci-lint-action from 3 to 4 (#3941)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump stackrox/kube-linter-action from 1.0.4 to 1.0.5 (#3982)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * ci: skip ostree-remount check in CS9 due to bug RHEL-25249 (#3978)
    * Author: mcattamoredhat, Reviewers: Irene Díez, Xiaofeng Wang
  * images: update dependency (#3983)
    * Author: Simon de Vlieger, Reviewers: Tomáš Hozza
  * integration test for worker-executor (HMS-3634) (#3968)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * templates/packer: fix vector repos (#3987)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * test: remove libvirt workaround (#3975)
    * Author: tkoscieln, Reviewers: Alexander Todorov, Jakub Rusz, Tomáš Hozza
  * tests: Drop bigiso test (HMS-3710) (#3988)
    * Author: Simon Steinbeiß, Reviewers: Ondřej Budai

— Somewhere on the Internet, 2024-03-06


* Mon Feb 26 2024 Packit <hello@packit.dev> - 101-1
Changes with 101
----------------
  * Add minimal-raw and clean up the compose handler a bit (#3962)
    * Author: Ondřej Budai, Reviewers: Achilleas Koutsou
  * RHEL-16006: improve error on missing package name (#3964)
    * Author: Florian Schüller, Reviewers: Ondřej Budai, Tomáš Hozza
  * Support configuring distro aliases via ENV and set aliases in the composer template. (#3927)
    * Author: Tomáš Hozza, Reviewers: Ondřej Budai, Sanne Raymaekers
  * Tag rhel 9.2+ with SEV_LIVE_MIGRATABLE_V2 (#3970)
    * Author: Amelia Crate, Reviewers: Ondřej Budai, Tomáš Hozza
  * Update osbuild/images to v0.40.0 (#3973)
    * Author: Tomáš Hozza, Reviewers: Gianluca Zuccarelli, Simon de Vlieger
  * cloud/awscloud: create secure instance in the same subnet (#3961)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * cloud/awscloud: describe security groups using filters (#3965)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Gianluca Zuccarelli, Ondřej Budai
  * cloud/awscloud: max 4 overrides are allowed when creating a fleet (#3946)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * cloud/awscloud: remove restricting egress rule from SG (#3954)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * cloud/awscloud: take instance type from host (#3947)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon Steinbeiß, Simon de Vlieger
  * cmd/osbuild-jobsite-builder: actually assign the stdout buffer (#3958)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * cmd/osbuild-jobsite: capture osbuild's stdout (#3953)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * composer: glitchtip integration (#3907)
    * Author: Diaa Sami, Reviewers: Ondřej Budai
  * errors-level logs to glitchtip (#3934)
    * Author: Diaa Sami, Reviewers: Ondřej Budai
  * jobsite/manager: create export directory (#3955)
    * Author: Simon de Vlieger, Reviewers: Sanne Raymaekers
  * jobsite/manager: turn off compression (#3957)
    * Author: Simon de Vlieger, Reviewers: Sanne Raymaekers
  * jobsite: `manager` and `builder` (#3937)
    * Author: Simon de Vlieger, Reviewers: Sanne Raymaekers
  * osbuild-runner: run osbuild in an ec2 vm (#3939)
    * Author: Sanne Raymaekers, Reviewers: Nobody
  * osbuildexecutor/aws.ec2: pass the manifest to the job manager (#3948)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon Steinbeiß
  * switch to images/pkg/dnfjson and remove internal copy (#3828)
    * Author: Diaa Sami, Reviewers: Nobody
  * templates/packer: let the executor listen on all interfaces (#3949)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * templates/packer: rename executor log group (#3959)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * templates/packer: set -builder-path to /var/cache/osbuild-builder (#3950)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou
  * templates/packer: setup vector in osbuild-executor (#3952)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou
  * tools/appsre-build-fedora: wait until rpms are built upstream (#3971)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger
  * worker-executor followups: fix oneshot service and secure instance for non-default vpcs (#3945)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger

— Somewhere on the Internet, 2024-02-26


* Sun Feb 11 2024 Maxwell G <maxwell@gtmx.me> - 100-2
- Rebuild for golang 1.22.0

* Wed Feb 07 2024 Packit <hello@packit.dev> - 100-1
Changes with 100
----------------
  * CI: update terraform SHA (#3919)
    * Author: Jakub Rusz, Reviewers: Achilleas Koutsou
  * Cloud API: Add Fedora IoT bootable container (#3916)
    * Author: Achilleas Koutsou, Reviewers: Ondřej Budai
  * DEPLOYING/HACKING.md: Consistently use inline refs (#3930)
    * Author: Simon Steinbeiß, Reviewers: Tomáš Hozza
  * HACKING/DEPLOYING.md: Markdown syntax fixes (#3929)
    * Author: Simon Steinbeiß, Reviewers: Ondřej Budai
  * Update osbuild/images to v0.35.0 (#3932)
    * Author: Tomáš Hozza, Reviewers: Sanne Raymaekers
  * Use dot to separate distro major and minor version and replace distro registry with factory (#3887)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou
  * build(deps): bump actions/setup-go from 4 to 5 (#3842)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump actions/upload-artifact from 3 to 4 (#3855)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump the go-deps group with 10 updates (#3923)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * pkg/jobqueue: fix worker status update query (#3922)
    * Author: Sanne Raymaekers, Reviewers: Diaa Sami, Gianluca Zuccarelli
  * templates/dashboards: add community stage service to orgs (#3931)
    * Author: Sanne Raymaekers, Reviewers: Simon Steinbeiß
  * templates/packer: deal with unbound variables (#3920)
    * Author: Sanne Raymaekers, Reviewers: Simon Steinbeiß
  * test: remove workarounds for fixed bugs (#3933)
    * Author: Xiaofeng Wang, Reviewers: Jakub Rusz
  * tests/CI: Add RHEL 9.3 and 8.9 GA to pipeline (#3892)
    * Author: tkoscieln, Reviewers: Alexander Todorov, Jakub Rusz

— Somewhere on the Internet, 2024-02-07


* Wed Jan 24 2024 Packit <hello@packit.dev> - 99-1
Changes with 99
----------------
  * Add a tool script to help check for unused runners (#3614)
    * Author: Brian C. Lane, Reviewers: Tomáš Hozza
  * Bump azure (#3853)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * COMPOSER-2096: Add blueprint support to cloudapi & local access to cloudapi service (#3757)
    * Author: Brian C. Lane, Reviewers: Sanne Raymaekers
  * Fedora worker images (#3902)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * Invert wrong boolean condition in filesystem test (#3889)
    * Author: Alexander Todorov, Reviewers: Tomáš Hozza
  * Remove oscap.sh firewalld rules workaround (#3905)
    * Author: Alexander Todorov, Reviewers: Tomáš Hozza
  * Update test runners to Fedora 39 (#3820)
    * Author: Alexander Todorov, Reviewers: Achilleas Koutsou, Michael Vogt, Ondřej Budai, Tomáš Hozza
  * edge: add iot-simplified-installer image type (#3900)
    * Author: djach7, Reviewers: Achilleas Koutsou
  * image-info: update for new "partition" option in mounts.Mount (#3883)
    * Author: Michael Vogt, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * tools/build-rpms: fix getting the osbuild commit from Schutzfile (#3897)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon Steinbeiß
  * tools/fedora-worker-packer: fix packer only/except (#3910)
    * Author: Sanne Raymaekers, Reviewers: Tomáš Hozza

— Somewhere on the Internet, 2024-01-24


* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Packit <hello@packit.dev> - 98-1
Changes with 98
----------------
  * Update snapshots to 20240101 (#3876)
    * Author: SchutzBot, Reviewers: Jakub Rusz
  * build(deps): bump the go-deps group with 5 updates (#3877)
    * Author: dependabot[bot], Reviewers: Ondřej Budai
  * schutzbot: add my "mvogt" SSH key (#3882)
    * Author: Michael Vogt, Reviewers: Achilleas Koutsou

— Somewhere on the Internet, 2024-01-10


* Wed Dec 13 2023 Packit <hello@packit.dev> - 96-1
Changes with 96
----------------
  * .gitlab-ci.yml: upgade neetle early to workaround RHEL-17890 (#3847)
    * Author: Alexander Todorov, Reviewers: Tomáš Hozza
  * README: remove IRC in favour of matrix channel (#3844)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * Worker status heartbeat (#3766)
    * Author: Sanne Raymaekers, Reviewers: Nobody
  * build(deps): bump actions/github-script from 6 to 7 (#3806)
    * Author: dependabot[bot], Reviewers: Nobody
  * build(deps): bump the go-deps group with 5 updates (#3837)
    * Author: dependabot[bot], Reviewers: Achilleas Koutsou
  * cloudapi/v2: fix verbiage of customizations (#3839)
    * Author: Sanne Raymaekers, Reviewers: Diaa Sami
  * rpmbuild: add fedora-40 (#3838)
    * Author: Jakub Rusz, Reviewers: Alexander Todorov
  * test: fix ansible playbook conditional statements error (#3845)
    * Author: Xiaofeng Wang, Reviewers: Achilleas Koutsou
  * test: remove persistent log checking on minimal raw test (#3836)
    * Author: Xiaofeng Wang, Reviewers: Achilleas Koutsou

— Somewhere on the Internet, 2023-12-13


* Wed Nov 29 2023 Packit <hello@packit.dev> - 95-1
Changes with 95
----------------
  * :lock: Update `filesystem.sh` test case to reflect update mountpoint policy (#3796)
    * Author: Tomáš Hozza, Reviewers: Brian C. Lane
  * Cloud API: Support selecting multiple upload targets and add Pulp OSTree uploads (#3744)
    * Author: Achilleas Koutsou, Reviewers: Sanne Raymaekers
  * Fix rhel9 oscap test (#3816)
    * Author: Gianluca Zuccarelli, Reviewers: Alexander Todorov, Jakub Rusz
  * Revert "containers/osbuild-composer: wait for fluentd in entrypoint" (#3819)
    * Author: Diaa Sami, Reviewers: Sanne Raymaekers
  * Switch testing to RHEL-8.10 and RHEL-9.4 nightly (#3775)
    * Author: Jakub Rusz, Reviewers: Alexander Todorov
  * composer: use logrus hook instead of k8s sidecar for splunk log forwa… (#3795)
    * Author: Diaa Sami, Reviewers: Sanne Raymaekers
  * deps: update images to v0.18.0 (#3635)
    * Author: Achilleas Koutsou, Reviewers: Simon de Vlieger
  * pkg/splunk_logger: make it a module that can be imported seprately (#3799)
    * Author: Diaa Sami, Reviewers: Achilleas Koutsou
  * schutzbot/terraform: aws instance types rework (#3791)
    * Author: Sanne Raymaekers, Reviewers: Achilleas Koutsou
  * test/cases/ubi-wsl: query Windows VM ip address via vm show (#3800)
    * Author: Sanne Raymaekers, Reviewers: Jakub Rusz

— Somewhere on the Internet, 2023-11-29


* Wed Nov 15 2023 Packit <hello@packit.dev> - 94-1
Changes with 94
----------------
  * .github: update apt metadata before installing deps (#3788)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai, Simon de Vlieger, Tomáš Hozza
  * Add pkg splunk_logging (#3750)
    * Author: Diaa Sami, Reviewers: Ondřej Budai, Sanne Raymaekers
  * Added hyper_v_generation metadata to the instance used by CIV. (#3769)
    * Author: Nicolás M., Reviewers: Alexander Todorov, Jakub Rusz, Tomáš Hozza
  * Blueprints: Fix TOML filesystem `minsize` keyword (#3783)
    * Author: Gianluca Zuccarelli, Reviewers: Achilleas Koutsou, Tomáš Hozza
  * Generate RHEL-94 and RHEL-810 manifests + update (#3778)
    * Author: Jakub Rusz, Reviewers: Alexander Todorov
  * build(deps): bump the go-deps group with 10 updates (#3794)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * schutzbot/terraform: update rhel-9.2 aarch64 image (#3789)
    * Author: Sanne Raymaekers, Reviewers: Simon Steinbeiß
  * store: Fix RepoConfig (#3764)
    * Author: Brian C. Lane, Reviewers: Ondřej Budai
  * tools/provision: disable tracing before manipulating OCI secrets (#3784)
    * Author: Sanne Raymaekers, Reviewers: Brian C. Lane

— Somewhere on the Internet, 2023-11-15


* Wed Nov 01 2023 Packit <hello@packit.dev> - 93-1
Changes with 93
----------------
  * :package: Packit configuration enhancements (#3768)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Ondřej Budai, Simon Steinbeiß
  * Add partitioning mode support to cloudapi and weldr api (#3723)
    * Author: Brian C. Lane, Reviewers: Ondřej Budai
  * Add support for uploading an ostree commit to Pulp (#3636)
    * Author: Achilleas Koutsou, Reviewers: Nobody
  * Build rpms on RHEL-8.10 and RHEL-9.4 (#3772)
    * Author: Jakub Rusz, Reviewers: Alexander Todorov
  * Post `osbuild/images` split autumn cleanup :broom: (#3754)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * test/README: run go tests when updating images (#3763)
    * Author: Achilleas Koutsou, Reviewers: Tomáš Hozza, djach7

— Somewhere on the Internet, 2023-11-01


* Tue Oct 24 2023 Packit <hello@packit.dev> - 88.2-1
Changes with 88.2
-----------------
  * deps: update osbuild/images to v0.3.0-r9.3.3 (#3756)

Contributions from: Achilleas Koutsou

— Berlin, 2023-10-24

* Wed Oct 18 2023 Packit <hello@packit.dev> - 92-1
Changes with 92
----------------
  * Enable Azure testing on HyperV Gen2 (#3679)
    * Author: Alexander Todorov, Reviewers: Jakub Rusz, Tomáš Hozza
  * Internal: delete unused `common.VersionLessThan()` (#3729)
    * Author: Tomáš Hozza, Reviewers: Ondřej Budai
  * Small fixes for Koji data consolidation PR#3599 (#3719)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * Support F40, EL8.10, EL9.4, ppc64le and s390x on Fedora (#3740)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * build(deps): bump the go-deps group with 2 updates (#3748)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump the go-deps group with 7 updates (#3737)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * cloudapi/v2: add all existing customizations to openapi spec (#3716)
    * Author: Sanne Raymaekers, Reviewers: Brian C. Lane
  * cloudapi: Move Services to an actual struct (#3735)
    * Author: Brian C. Lane, Reviewers: Sanne Raymaekers
  * fix ostree vmdk test timeout (#3724)
    * Author: He Yi, Reviewers: Xiaofeng Wang
  * go.mod: update images to 0.11 (#3722)
    * Author: Ondřej Budai, Reviewers: Brian C. Lane

— Somewhere on the Internet, 2023-10-18


* Wed Oct 04 2023 Packit <hello@packit.dev> - 91-1
Changes with 91
----------------
  * Add checksums to mock data (#3683)
    * Author: Brian C. Lane, Reviewers: Achilleas Koutsou
  * Consolidation & extension of information imported to Koji builds (#3659)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou, Simon de Vlieger
  * Revert "Add softlockup_all_cpu_backtrace=1 boot argument" (#3680)
    * Author: Alexander Todorov, Reviewers: Tomáš Hozza
  * build(deps): bump actions/checkout from 3 to 4 (#3678)
    * Author: dependabot[bot], Reviewers: Tomáš Hozza
  * build(deps): bump the go-deps group with 1 update (#3704)
    * Author: dependabot[bot], Reviewers: Sanne Raymaekers
  * build(deps): bump the go-deps group with 6 updates (#3703)
    * Author: dependabot[bot], Reviewers: Nobody
  * cloudapi/v2: log manifest generation errors as a warning (#3709)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli
  * dashboard: worker api dashboard (#3712)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli
  * dashboards: fix composer dash request rate errors (#3710)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli
  * lint: fix memory aliasing (#3711)
    * Author: Brian C. Lane, Reviewers: Achilleas Koutsou
  * templates/compose: add startingDeadlineSeconds to maintenance job (#3698)
    * Author: Sanne Raymaekers, Reviewers: Tomáš Hozza
  * templates/composer: parameterise maintenance job cpu req/limit (#3697)
    * Author: Sanne Raymaekers, Reviewers: Ondřej Budai
  * templates/packer: configure oracle cloud credentials on startup (#3694)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli
  * test: remove fdo package workaround from PR#3690 (#3713)
    * Author: Xiaofeng Wang, Reviewers: Brian C. Lane
  * tools/appsre-ansible/rpmbuild: retry all tasks (#3701)
    * Author: Sanne Raymaekers, Reviewers: Diaa Sami

— Somewhere on the Internet, 2023-10-04


* Wed Sep 20 2023 Packit <hello@packit.dev> - 90-1
Changes with 90
----------------
  * Actions: add workflow for marking and closing stale issues and PRs (#3676)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou
  * Add test case for iot-qcow2-image (#3668)
    * Author: He Yi, Reviewers: Xiaofeng Wang
  * OpenSCAP cloudapi tailoring (#3617)
    * Author: Gianluca Zuccarelli, Reviewers: Tomáš Hozza
  * oci object storage target (#3675)
    * Author: Sanne Raymaekers, Reviewers: Gianluca Zuccarelli
  * test/cases/ubi-wsl: set --os-type when creating vm (#3686)
    * Author: Sanne Raymaekers, Reviewers: Tomáš Hozza
  * test: remove workaround for bug BZ#2234390 (#3684)
    * Author: Xiaofeng Wang, Reviewers: Achilleas Koutsou, Brian C. Lane
  * test: workaround fdo package issue (#3690)
    * Author: Xiaofeng Wang, Reviewers: Achilleas Koutsou

— Somewhere on the Internet, 2023-09-20


* Wed Sep 06 2023 Packit <hello@packit.dev> - 89-1
Changes with 89
----------------
  * Handle panics in the osbuild job & fix panic when OCI authentication fails (#3666)
  * Oci test (#3629)
  * Tests: Add softlockup_all_cpu_backtrace=1 boot argument (#3656)
  * Tests: Remove deprecated --os-type cli argument (#3643)
  * build(deps): bump the go-deps group with 2 updates (#3661)
  * cloudapi/v2: expose wsl image type (#3660)
  * test/cases/ubi-wsl: fix waiting for a valid ipv4 (#3670)
  * test/cases/ubi-wsl: public ip fixes (#3653)
  * test: add workaround for bug BZ#2234390 (#3663)
  * test: fix "Waiter SnapshotImported failed: Max attempts exceeded" (#3662)

Contributions from: Alexander Todorov, Ondřej Budai, Sanne Raymaekers, Xiaofeng Wang, dependabot[bot]

— Somewhere on the Internet, 2023-09-06


* Thu Aug 24 2023 Packit <hello@packit.dev> - 88-1
Changes with 88
----------------
  * COMPOSER-2016: blueprint: make Convert respect nils (#3612)
  * Update rhel ga runners (#3596)
  * Use newer RHEL 8.9 & 9.3 images for testing (#3603)
  * build(deps): bump github.com/aws/aws-sdk-go from 1.44.318 to 1.44.322 (#3620)
  * build(deps): bump github.com/openshift-online/ocm-sdk-go from 0.1.315 to 0.1.362 (#3627)
  * cloudapi: Add ability to skip uploading and save image locally (#3585)
  * dashboards/worker: default to showing the past 6 hours (#3651)
  * dependabot: group go package updates (#3642)
  * deps: update osbuild/images to 9548bf0d0140 (#3606)
  * deps: update osbuild/images to v0.3.0 (#3634)
  * go.mod: bump osbuild/images to c2aa82cc9a86 (#3640)
  * internal/cloud/gcp/compute: Add SEV_SNP_CAPABLE Guest OS Feature (#3579)
  * schutzbot: unregister test hosts (#3630)
  * test/cases/ubi-wsl: double ssh timeout (#3624)
  * test: add workaround for bug 2230537 and 2229722 (#3615)
  * test: run greenboot rollback test on ostree.sh, ostree-ami-image.sh and ostree-vsphere.sh (#3618)
  * test: update edge-ami test to support aarch64 (#3613)
  * test: wait for ami image avaiable to use before tag creation (#3619)

Contributions from: Achilleas Koutsou, Alexander Todorov, Brian C. Lane, Ondřej Budai, Sanne Raymaekers, Timothée Ravier, Tomáš Hozza, Xiaofeng Wang, dependabot[bot]

— Somewhere on the Internet, 2023-08-24


* Wed Aug 09 2023 Packit <hello@packit.dev> - 87-1
Changes with 87
----------------
  * Koji: expose image metadata in build extra metadata, including boot mode (#3599)
  * Main cloud size (#3597)
  * Update snapshots to 20230801 (#3592)
  * deps: update osbuild/images to 157e798fdf8d (#3593)
  * test/cases/api: add check for subscription-manager facts (#3257)
  * test: Fix Fedora 39 snapshot urls in test repo (#3574)
  * tests: Add a check for valid snapshot urls (#3572)

Contributions from: Achilleas Koutsou, Brian C. Lane, Jakub Rusz, Sanne Raymaekers, Tomáš Hozza, Xiaofeng Wang, schutzbot, yih

— Somewhere on the Internet, 2023-08-09


* Wed Jul 26 2023 Packit <hello@packit.dev> - 86-1
Changes with 86
----------------
  * Openapi revision (#3286)
  * Start collecting logs from virt-install (#3557)
  * Ubi wsl (#3473)
  * Update osbuild/images (#3565)
  * ci: fix the gitlab trigger (#3568)
  * packer: Move to Fedora 38 and use cheaper GP3 volumes (#3554)
  * spec: require osbuild >= 89 (#3524)
  * test/README: describe vendoring modified images repo (#3564)
  * tools: Set a+x on rpm_spec_vendor2provides (#3562)
  * tools: replace spec Provides generator (#3560)

Contributions from: Achilleas Koutsou, Alexander Todorov, Brian C. Lane, Diaa Sami, Mario Cattamo, Ondřej Budai, Sanne Raymaekers, Simon de Vlieger, Xiaofeng Wang

— Somewhere on the Internet, 2023-07-26


* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 85-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Packit <hello@packit.dev> - 85-1
Changes with 85
----------------
  * Allow any hashing algorithm in osbuild stage inputs (#3514)
  * COMPOSER-1959: Test on 8.9 and 9.3 nightly (#3422)
  * Deprecated mas sso (#3531)
  * Enable CI for Fedora 38 & a few cleanups (#3481)
  * Fix ISO building on F39 (#3523)
  * Fix for possibly undefined variable in CI script (#3549)
  * Introduce test conditions for AWS & Azure (#3493)
  * Packit/copr: Remove EPEL builds in favor of RHEL ones (#3507)
  * Remove Juan from the list of QE associates (#3550)
  * Remove redundant script in upgrade8to9 test (#3508)
  * Set the tenant in the request context, reuse it for the status and request duration metrics (#3510)
  * Update Cloud API with new manifest generation process (#3482)
  * Update manifests (#3494)
  * Update snapshots to 20230701 (#3540)
  * Upgrade 8to9 upgrade test for 9.3 (#3505)
  * cloudapi/v2: cleanup rebase leftovers (#3552)
  * cloudapi: openscap integration (#3522)
  * containers/osbuild-composer: add prometheus port parameter (#3497)
  * distro/rhel8: fix Azure EAP7 RHUI image definition (#3502)
  * jsondb: improve performance of list operation (#3504)
  * reorder middlewares in worker and cloud apis (#3534)
  * templates/dasbhoards: rework composer dashboard (#3538)
  * test/repos: use EUS CDN repos for RHEL 8.4 / 8.6 / 9.0 (#3467)
  * test: Four fixes for RHEL for Edge tests (#3532)
  * test: Remove rebase test shell script (#3530)
  * test: Some enhancements to make test stable (#3495)

Contributions from: Achilleas Koutsou, Alexander Todorov, Diaa Sami, Eng Zer Jun, Gianluca Zuccarelli, Ondřej Budai, Sanne Raymaekers, Simon de Vlieger, Tomáš Hozza, Xiaofeng Wang, dependabot[bot], schutzbot

— Somewhere on the Internet, 2023-07-12


* Wed Jun 14 2023 Packit <hello@packit.dev> - 84-1
Changes with 84
----------------
  * Add the 'edge-ami' image type based on edge-raw-image (#3429)
  * CI: Move RHEL for Edge CI into osbuild/rhel-edge-ci repo (#3460)
  * Cleanup of Fedora cloud images (#3480)
  * Finalise interface between composer and image definitions (#3444)
  * Update snapshots to 20230522 (#3451)
  * build(deps): bump google.golang.org/api from 0.123.0 to 0.126.0 (#3485)
  * cloudapi: add vsphere-ova type (#3474)
  * fedora: f36 went EOL (#3445)
  * internal/cloudapi: new prometheus listener (#3430)
  * internal/osbuild: yum repos ssl verify (#3419)
  * osbuild: Add validation error logging (#3483)
  * templates/composer:  parametrise replicas and tweak cpu requests/limits (#3472)

Contributions from: Achilleas Koutsou, Brian C. Lane, Diaa Sami, Gianluca Zuccarelli, Irene Diez, Ondřej Budai, Sanne Raymaekers, Simon de Vlieger, Tomáš Hozza, Xiaofeng Wang, dependabot[bot], jabia99, schutzbot

— Somewhere on the Internet, 2023-06-14


* Wed May 31 2023 Packit <hello@packit.dev> - 83-1
Changes with 83
----------------
  * Add support for VMware ovf image type (#3371)
  * Add tests for blueprint package name globs and fix blueprint freeze with globs (#3425)
  * CI: update centos-stream-8 images and snapshots (#3466)
  * Dockerfile*: update to ubi9 and chown the files when copying (#3443)
  * Fedora/iot-raw-image: support custom files and directories in `/etc` (+ services customization) (#3303)
  * Fixes for the koji integration (#3399)
  * Revert the hybrid boot mode changes on RHEL (RHUI) EC2 images prior to 8.9 / 9.3 (#3455)
  * Support hybrid boot mode on x86_64 AMI images and set the AMI boot mode on image registration (#3446)
  * build(deps): bump cloud.google.com/go/compute from 1.10.0 to 1.19.3 (#3442)
  * build(deps): bump cloud.google.com/go/storage from 1.27.0 to 1.30.1 (#3428)
  * build(deps): bump github.com/docker/distribution from 2.8.1+incompatible to 2.8.2+incompatible (#3437)
  * build(deps): bump github.com/labstack/echo/v4 from 4.10.0 to 4.10.2 (#3454)
  * build(deps): bump github.com/stretchr/testify from 1.8.2 to 1.8.3 (#3457)
  * build(deps): bump google.golang.org/api from 0.122.0 to 0.123.0 (#3453)
  * internal/GCP: remove all remaining uses of `cloudbuild` (#3450)
  * iot: add fedora-release-iot to iot-installer (#3441)

Contributions from: Alexander Todorov, Brian C. Lane, Jakub Rusz, Ondřej Budai, Paul Whalen, Sanne Raymaekers, Tomáš Hozza, dependabot[bot]

— Somewhere on the Internet, 2023-05-31


* Wed May 17 2023 Packit <hello@packit.dev> - 82-1
Changes with 82
----------------
  * Adjust packer build to work with the amazon plugin 1.2.3 (#3402)
  * Disable firewalld for RHEL 8 Azure EAP (#3421)
  * Update terraform SHA (#3420)
  * cloudapi: custom repos add missing fields (#3418)
  * internal/manifest: install rhc-worker-playbook when using rhc (#3432)

Contributions from: Achilleas Koutsou, Gianluca Zuccarelli, Jakub Rusz, Ondřej Budai, Sanne Raymaekers, dependabot[bot], jabia99

— Somewhere on the Internet, 2023-05-17


* Wed Apr 19 2023 Packit <hello@packit.dev> - 80-1
Changes with 80
----------------
  * COMPOSER-1936: Enable regression-insecure-repo test for nightly CI pipeline (#3380)
  * COMPOSER-1943: Fix failure in cross-distro.sh (#3379)
  * Save manifest lists when pulling containers (#3336)
  * Simplify packit config (#3339)
  * Test/fix cs9 edge-simplified-installer test failure (#3382)
  * build(deps): bump github.com/docker/docker from 20.10.17+incompatible to 20.10.24+incompatible (#3376)
  * cloudapi/v2: expose repo metadata verification (#3387)
  * dbjobqueue: Make dequeuing atomic (#3389)
  * internal/worker: log dequeue failures (#3369)
  * rpi firmware copy (#3391)

Contributions from: Achilleas Koutsou, Alexander Todorov, Gianluca Zuccarelli, Jiri Popelka, Ondřej Budai, Sanne Raymaekers, Simon de Vlieger, dependabot[bot], yih

— Somewhere on the Internet, 2023-04-19


* Wed Apr 05 2023 Packit <hello@packit.dev> - 79-1
Changes with 79
----------------
  * Add Butane test and Ignition logs (#3223)
  * Add tags to CIV instances (#3343)
  * COMPOSER-1936: Use check_gpg=True during testing (#3353)
  * New image type: Azure EAP for RHEL 8.6+ (no RHEL 9). (#3288)
  * build(deps): bump github.com/opencontainers/runc from 1.1.3 to 1.1.5 (#3365)
  * containers/osbuild-composer: wait for fluentd in entrypoint (#3357)
  * distro/rhel: add payload repos to os package set (#3329)
  * internal/boot: boot VMWare VMs with EFI and SCSI (#3351)
  * packit: build RPMs also for EPEL 9 and RHEL (#3359)
  * per-distro rpmmd cache directory (#3317)
  * upload/azure: modernize & do not upload zeroed pages (#3367)
  * weldr+distro: allow to send Manifest warnings on ComposeReply (#3319)

Contributions from: Achilleas Koutsou, Alexander Todorov, Brian C. Lane, Diaa Sami, Irene Diez, Jakub Rusz, Juan Abia, Mario Cattamo, Ondřej Budai, Sanne Raymaekers, Tomáš Hozza, dependabot[bot]

— Somewhere on the Internet, 2023-04-05


* Wed Mar 22 2023 Packit <hello@packit.dev> - 78-1
Changes with 78
----------------
  * Change civ repo name (#3340)
  * File resolver job (#3254)
  * Introduce jobtype variable in worker dashboard (#3262)
  * Test/ostree: add sysroot permission test (#3325)
  * build(deps): bump actions/setup-go from 3 to 4 (#3337)
  * distro/fedora: add support for Fedora 39 (#3324)
  * distro: remove duplicate version checks for fonts (#3280)
  * image-installer: switch payload to minimal-rpm (#3249)
  * iot-raw-image: partitioning changes (#3246)
  * simplified-installer: enable isolinux (#3327)
  * test/vmware: boot VMs with EFI and use SCSI as a disk controller (#3330)
  * tests/ostree: Change centos-8 BOOT_LOCATION to a working boot.iso (#3338)

Contributions from: Antonio Murdaca, Gianluca Zuccarelli, Jakub Rusz, Juan Abia, Sanne Raymaekers, Simon de Vlieger, dependabot[bot], yih

— Somewhere on the Internet, 2023-03-22


* Wed Mar 08 2023 Packit <hello@packit.dev> - 77-1
Changes with 77
----------------
  * Add open-vm-tools to Fedora VMDK image default package set (#3300)
  * Update deprecated io/ioutil functions and go:build tags (#3323)
  * Update rpmrepo snapshots to 20230223 (including necessary fixes and workarounds) (#3311)
  * Use CDN repos when making the worker rpms and images (#3320)
  * koji: log unsuccessful requests only once (#3314)
  * manifest/os: fix SUPPRESSED_ERROR issue reported by Coverity (#3304)
  * packer ansible: fix unregister and aarch64 cdn repos (#3322)
  * tools/appsre-ansible: don't subscribe machines used for rpmbuild (#3315)
  * worker: allow configuring number of upload threads for Azure (#3321)

Contributions from: Brian C. Lane, Diaa Sami, Sanne Raymaekers, Tomáš Hozza, schutzbot, yih

— Somewhere on the Internet, 2023-03-08


* Wed Mar 01 2023 Packit <hello@packit.dev> - 76-1
Changes with 76
----------------
  * Fix CIV_OPTIONS bug (#3297)
  * Update test suite after rebase to weldr-client-35.9 (#3296)
  * distro: assign pipeline-specific repos to package sets (#3291)
  * ignition: enable systemd firstboot condition through kargs (#3308)

Contributions from: Achilleas Koutsou, Alexander Todorov, Antonio Murdaca, Juan Abia

— Somewhere on the Internet, 2023-03-01


* Wed Feb 22 2023 Packit <hello@packit.dev> - 75-1
Changes with 75
----------------
  * Blueprint: add support for custom files and directories in `/etc` (#3281)
  * Image info: Update from manifest-db (#3278)
  * `edge-simplified-installer` allows User & Group customizations (#3285)
  * cloudapi: Add subscription option for rhc  (#3240)
  * internal/prometheus: add more buckets for job durations (#3273)
  * osbuild-worker/koji: Add logging for koji requests/responses (#3252)
  * rhel: fix conditionals for sysroot.readonly enablement (#3276)
  * test/cases: move CIV options into a variable (#3279)

Contributions from: Antonio Murdaca, Brian C. Lane, Diaa Sami, Irene Diez, Jakub Rusz, Juan Abia, Mario Cattamo, Sanne Raymaekers, Thomas Lavocat, Tomáš Hozza, Xiaofeng Wang

— Somewhere on the Internet, 2023-02-22


* Wed Feb 08 2023 Packit <hello@packit.dev> - 74-1
Changes with 74
----------------
  * Add repositories for test case generation for RHEL 9.1 (rhel-91) (#3247)
  * Adding metadata signing check (#3230)
  * Enable RHEL 8 Azure images for aarch64 (#3250)
  * Fix dracut modules for Anaconda installers in RHEL 9 and CS9 (#3253)
  * Rewrite RHEL 7 image definitions using the new framework (#3239)
  * build(deps): bump github.com/openshift-online/ocm-sdk-go from 0.1.287 to 0.1.315 (#3269)
  * cleanup leftovers, fix ignition in edge raw image and add tests (#3267)
  * distro/rhel8: don't install missing MSFT key into azure-sap-rhui (#3270)
  * internal/distro/rhel9+8/edge: add sos package (#3234)
  * osbuild: unify implementations of files input 🧹 (#3248)
  * repositories: fix rhel-90 repositories (#3263)

Contributions from: Achilleas Koutsou, Antonio Murdaca, Brian C. Lane, Diaa Sami, Irene Diez, Ondřej Budai, Sanne Raymaekers, Sarita Mahajan, Simon de Vlieger, Tomáš Hozza, Xiaofeng Wang, dependabot[bot]

— Somewhere on the Internet, 2023-02-08


* Wed Jan 25 2023 Packit <hello@packit.dev> - 73-1
Changes with 73
----------------
  * Packer: workaround missing authselect-compat-1.2.5-2.el9_1 in RHUI repos (#3237)
  * Rewrite RHEL 8 and CS8 image definitions using the new framework (#3213)
  * Schutzfile: bump osbuild commit for GA RHEL (#3214)
  * Support ignition in simplified-installer and raw-image (#3130)
  * build(deps): bump github.com/Azure/azure-sdk-for-go from 66.0.0+incompatible to 68.0.0+incompatible (#3229)
  * distro/rhel8: ensure the Azure SAP RHUI image uses appropriate config (#3233)
  * fix ostree cannot boot on fedora37 (#3217)
  * osbuild/mkdir: support new stage options and small fixes (#3226)
  * schutzbot: delete ckellner's SSH key (#3224)

Contributions from: Achilleas Koutsou, Antonio Murdaca, Gianluca Zuccarelli, Sanne Raymaekers, Tomáš Hozza, Xiaofeng Wang, dependabot[bot], yih

— Somewhere on the Internet, 2023-01-25


* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Packit <hello@packit.dev> - 72-1
Changes with 72
----------------
  * Dashboard metrics update (#3191)
  * Enable 8.8 and 9.2 test runnners (#3134)
  * Migrate to SPDX license (#3198)
  * Schutzfile: update osbuild version to current main (v75) (#3201)
  * Update to Go 1.18 and introduce a generic ToPtr method (#3204)
  * build(deps): bump github.com/theupdateframework/go-tuf from 0.3.1 to 0.3.2 (#3205)
  * osbuild-worker: add dnf-json error reason to depsolve job error (#3174)
  * remove Fedora 35 support (#3179)
  * terraform: update to the latest definitions (#3208)
  * worker/server: log unresponsive job removal (#3206)

Contributions from: Achilleas Koutsou, Alexander Todorov, Gianluca Zuccarelli, Jakub Rusz, Miroslav Suchý, Ondřej Budai, Sanne Raymaekers, dependabot[bot]

— Somewhere on the Internet, 2023-01-11


* Wed Dec 28 2022 Packit <hello@packit.dev> - 71-1
Changes with 71
----------------
  * Enable Azure images for aarch64 (#3192)
  * Ignition blueprint config support on rhel9 (#3161)
  * Update building instructions (#3049)

Contributions from: Achilleas Koutsou, Irene Diez, Lukáš Zapletal, Sanne Raymaekers, Tomáš Hozza

— Somewhere on the Internet, 2022-12-28



* Wed Dec 14 2022 Packit <hello@packit.dev> - 70-1
Changes with 70
----------------
  * Bugfix: Add RHSM Fact (APIType) to RHEL 9 image definitions (#3160)
  * Create and add Journald stage to rhel8/9 pipeline (#3118)
  * Enable isolinux only for x86_64 (#3171)
  * Enable isolinux only for x86_64 (removed stage) (#3182)
  * Extend firewall customizations to add sources (#3055)
  * Measure 5xx errors on all requests for image-builder-composer/worker (#3147)
  * RHEL 9 & Fedora: Anaconda boot arguments (#3180)
  * RHEL 9: Do not enable user module in Anaconda Edge Installer when no users are specified (#3187)
  * RHEL 9: update edge-simplified-installer to new definitions (#3166)
  * Schutzfile: bump osbuild dependency (#3177)
  * `internal/rpmmd` cleanup 🧹 (#3159)
  * cloudapi/v2: set ostree rhsm option on image options (#3172)
  * distro/rhel9: add consumer certificates on ostree rhsm option (#3176)
  * gcp: Cross-reference to coreos-assembler code (#3163)
  * metrics: update status metrics label (#3165)
  * re-enable cs9 runner for simplified installer (#3145)
  * rhel8/9: make edge images properly sysroot.readonly=true (#3178)
  * templates/packer: increase polling delay (#3183)
  * worker: fix reporting the import error to composer (#3162)

Contributions from: Achilleas Koutsou, Antonio Murdaca, Brian C. Lane, Colin Walters, Gianluca Zuccarelli, Irene Diez, Mario Cattamo, Ondřej Budai, Sanne Raymaekers, Sayan Paul, Tomáš Hozza, Xiaofeng Wang

— Somewhere on the Internet, 2022-12-14



* Wed Nov 30 2022 Packit <hello@packit.dev> - 69-1
Changes with 69
----------------
  * Add /blueprints/change/NAME/COMMIT route and save blueprint changes in the store (#3121)
  * CloudAPI: add description for `Repository` definition (#3158)
  * Rewrite RHEL 9 and CS9 image definitions using the new framework (#3120)
  * SPEC: run the %preun commands in worker package only on removal (#3149)
  * Update snapshots to 20221115 (#3136)
  * azure-sap image (#3074)
  * ci: update Fedora 37 runners to GA (#3157)
  * cloudapi/v2: pass rhsm requirement to ostree resolve job (#3142)
  * disk: align LVM2 volumes to the extent size  (#3137)
  * image: create image-installer image type for fedora (#3077)
  * tools: silence version comparison in get_build_info() (#3150)

Contributions from: Achilleas Koutsou, Antonio Murdaca, Brian C. Lane, Christian Kellner, Ondřej Budai, Sanne Raymaekers, Sarita Mahajan, Simon de Vlieger, Tomáš Hozza, Xiaofeng Wang, fkolwa, schutzbot

— Somewhere on the Internet, 2022-11-30



* Wed Nov 16 2022 Packit <hello@packit.dev> - 68-1
Changes with 68
----------------
  * Fix iot-installer build via the cloud API (#3132)
  * Fix issues reported by Coverity (#3092)
  * Fix loading cross distro compose results (#3090)
  * RHEL-8/9 EC2 image definitions fixes (#3135)
  * Refactor the RHEL 9 SAP config and packages to be useful on other platforms (#3100)
  * ci: add my SSH keys to the CI ssh keys (#3119)
  * ci: add tags to AWS instances (#3127)
  * cloudapi/v2: expose ostree contenturl and rhsm options (#3105)
  * dbjobqueue: acquire a new connection for each listen query (#3116)
  * diff-manifests.sh: Use shared_lib for greenprint and redprint (#3133)
  * distro: SELinux should be the last stage (#3117)
  * docker-compose: remove unavailable `--dnf-json` (#3124)
  * tools/provision.sh: copy RHEL repo overrides using wildcard (#3111)

Contributions from: Brian C. Lane, Jakub Rusz, Ondřej Budai, Paul Whalen, Sanne Raymaekers, Simon de Vlieger, Thomas Lavocat, Tom Gundersen, Tomáš Hozza

— Somewhere on the Internet, 2022-11-16



* Wed Nov 02 2022 Packit <hello@packit.dev> - 67-1
Changes with 67
----------------
  * Cloud API: make `location` optional for Azure Upload Options (#3093)
  * Content url and rhsm ostree resolve (#3091)
  * Fix blueprint firewall support (#3099)
  * Ostree resolve job (#3072)
  * RHEL-8.7+/9.1+: replace RHSM config on EC2 RHUI images with `redhat-cloud-client-configuration` package (#3081)
  * Update snapshots to 20221025 (#3098)
  * build(deps): bump github.com/spf13/cobra from 1.5.0 to 1.6.1 (#3094)
  * distro: add support for RHEL 8.8 and 9.2 (#3095)
  * internal/cloudapi: add ostree options for all otree image types (#3089)
  * koji: put artifacts uploaded to koji under a second level directory (#3083)
  * schutzbot/update_github_status: fix release fast-forwarding (#3082)
  * spec: Fix ownership of the dnf-json rpmmd files (#3085)
  * tests: Update the version of azurerm terraform provider (#3075)
Contributions from: Alexander Todorov, Antonio Murdaca, Brian C. Lane, Jakub Rusz, Ondřej Budai, Sanne Raymaekers, Tomáš Hozza, dependabot[bot], schutzbot
— Somewhere on the Internet, 2022-11-02





* Wed Oct 19 2022 Packit <hello@packit.dev> - 66-1
Changes with 66
----------------
  * Build rpms on RHEL 8.8 and 9.2 (#3066)
  * Fixes for Fedora IoT image types (#3038)
  * Weldr/Cloud API: simplify GCP upload options (#3023)
  * build(deps): bump github.com/aws/aws-sdk-go from 1.44.112 to 1.44.114 (#3054)
  * cloudapi: add iot-installer (#3037)
  * schutzbot/mockbuild: stop running mock as root (#3073)
Contributions from: Achilleas Koutsou, Jakub Rusz, Sanne Raymaekers, Tomáš Hozza, dependabot[bot], schutzbot
— Somewhere on the Internet, 2022-10-19





* Wed Oct 05 2022 Packit <hello@packit.dev> - 65-1
Changes with 65
----------------
  * Appsre cleanups (#3024)
  * Fix blueprint commit message (#3026)
  * Update Fedora IoT Installer definition (#3020)
  * [main] distro/rhel9: edge images default to LVM (#2861)
  * app-sre: Update AMIs to rhel-9.0 (#3019)
  * build(deps): bump cloud.google.com/go/compute from 1.9.0 to 1.10.0 (#2998)
  * build(deps): bump github.com/aws/aws-sdk-go from 1.44.104 to 1.44.108 (#3034)
  * build(deps): bump github.com/google/go-cmp from 0.5.8 to 0.5.9 (#3003)
  * build(deps): bump google.golang.org/api from 0.96.0 to 0.97.0 (#3012)
  * build(deps): bump google.golang.org/api from 0.97.0 to 0.98.0 (#3027)
  * dbjobqueue: Backoff after listener error (#3036)
  * packer: add fedora 36 (#3008)
  * packer: remove Fedora 35 (#3035)
  * packit: Enable Bodhi updates for unstable Fedoras (#3017)
  * spec: bump osbuild dep to >= 65 (#3007)
  * tagging a blueprint wasn't working correctly (#3031)
  * templates/composer.yml: update splunk port for splunk cloud (#3009)
  * templates/packer: Allow token url to be set by cloud-init vars (#3010)
  * test: add CIV tool to azure.sh (#2923)
  * test: get correct CIV tag in azure.sh (#3043)
  * worker: log error details on job failure (#3025)
Contributions from: Achilleas Koutsou, Antonio Murdaca, Brian C. Lane, Diaa Sami, Irene Diez, Juan Abia, Ondřej Budai, Sanne Raymaekers, Simon Steinbeiss, Xiaofeng Wang, dependabot[bot]
— Somewhere on the Internet, 2022-10-05





* Wed Sep 21 2022 Packit <hello@packit.dev> - 64-1
Changes with 64
----------------
  * CI: Introduce x86_64 rules (#2975)
  * Cache the results of dnf-json dump and search commands (#2918)
  * Enable integration testing on aarch64 (#2895)
  * Expose Fedora IoT types in Cloud API (#3001)
  * Fix packer builds (#2969)
  * Introduce logging adapter for jobqueue (#2811)
  * New image type: Fedora IoT Raw Image (#2914)
  * RHEL-8/9: base `vhd` image on `azure-rhui` pkg sets and configuration (#2971)
  * Update snapshots to 20220906 (#2959)
  * `test/api.sh`: cleanups (#2988)
  * build(deps): bump cloud.google.com/go/compute from 1.7.0 to 1.9.0 (#2942)
  * build(deps): bump github.com/labstack/echo/v4 from 4.8.0 to 4.9.0 (#2994)
  * build(deps): bump github.com/openshift-online/ocm-sdk-go from 0.1.266 to 0.1.287 (#2985)
  * build(deps): bump google.golang.org/api from 0.94.0 to 0.96.0 (#2996)
  * build(deps): bump gopkg.in/ini.v1 from 1.66.6 to 1.67.0 (#2944)
  * distro: use storage capacity multiple constants in partition tables (#2992)
  * pkg/dbjobqueue: fix dequeue constraint error (#2963)
  * s3 upload: add an option to upload images publicly (#2897)
  * templates/dashboards: Worker tenant fixes and uncollapsed queue times (#2987)
  * templates/packer: Append distro and architecture to the ami name (#2993)
  * test: User in commit will not be supported after osbuild-composer 64 (#3000)
  * test: change CIV tag (#2958)
  * workflow: Update to golangci-lint v1.49.0 (#2973)
Contributions from: Achilleas Koutsou, Alexander Todorov, Brian C. Lane, Diaa Sami, Gianluca Zuccarelli, Jakub Rusz, Juan Abia, Lukas Zapletal, Ondřej Budai, Sanne Raymaekers, Tomas Hozza, Tomáš Hozza, Xiaofeng Wang, dependabot[bot], schutzbot, yih
— Somewhere on the Internet, 2022-09-21





* Fri Sep 16 2022 Packit <hello@packit.dev> - 62.1-1
v62.1


* Fri Sep 16 2022 Packit <hello@packit.dev> - 63.1-1
v63.1


* Wed Sep 07 2022 Packit <hello@packit.dev> - 63-1
Changes with 63
----------------
  * Add GCP guest agent config stage (#2884)
  * CI: update test execution on nightly pipelines (#2930)
  * Create multiple aws images from a single compose (#2809)
  * No rhsm facts stage on rhel or for koji composes (#2919)
  * appsre-ansible: support aarch64 machines (#2718)
  * build(deps): bump cloud.google.com/go/storage from 1.22.1 to 1.26.0 (#2934)
  * build(deps): bump github.com/Azure/go-autorest/autorest from 0.11.27 to 0.11.28 (#2937)
  * build(deps): bump github.com/containers/common from 0.48.0 to 0.49.1 (#2933)
  * build(deps): bump github.com/golang-jwt/jwt/v4 from 4.4.1 to 4.4.2 (#2938)
  * build(deps): bump github.com/gophercloud/gophercloud from 0.24.0 to 1.0.0 (#2939)
  * build(deps): bump github.com/jackc/pgx/v4 from 4.16.0 to 4.17.1 (#2926)
  * build(deps): bump github.com/labstack/echo/v4 from 4.7.2 to 4.8.0 (#2940)
  * build(deps): bump github.com/prometheus/client_golang from 1.12.1 to 1.13.0 (#2883)
  * dbjobqueue: use background context when closing listener (#2721)
  * distro/`ImageConfig`: use pointers to simple types and reflection in `InheritFrom()` (#2953)
  * rhel9: explicitly add containernetworking-plugins to edge (#2951)
  * schutzbot: Fast-forward release branch after green main run (#2922)
  * templates/packer: Increase aws timeouts for rhel-8-aarch64 (#2955)
  * test aws arm images via cloud API (#2905)
  * test/gcp: Run cleanup function at the end (#2917)
  * tests: add aarch64 rhel-9.0 runner to API tests (#2948)
  * weldr: Preload metadata at startup (#2941)
Contributions from: Achilleas Koutsou, Brian C. Lane, Diaa Sami, Jakub Rusz, Juan Abia, Lukas Zapletal, Sanne Raymaekers, Tomas Hozza, dependabot[bot], fkolwa
— Somewhere on the Internet, 2022-09-07





* Mon Aug 29 2022 Packit <hello@packit.dev> - 62-1
Changes with 62
----------------
  * cloudapi/v2: Don't add rhsm facts (#2920)
  * go.mod: update github.com/containers/image/v5 (#2925)
Contributions from: Ondřej Budai, Sanne Raymaekers
— Somewhere on the Internet, 2022-08-29





* Mon Aug 29 2022 Packit <hello@packit.dev> - 62-1
Changes with 62
----------------
  * cloudapi/v2: Don't add rhsm facts (#2920)
  * go.mod: update github.com/containers/image/v5 (#2925)
Contributions from: Ondřej Budai, Sanne Raymaekers
— Somewhere on the Internet, 2022-08-29





* Fri Aug 26 2022 Packit <hello@packit.dev> - 61-1
Changes with 61
----------------
  * Add the `rhsm.facts` stage. (#2909)
  * Disable skipped tests (#2885)
  * Support hybrid boot for edge installers (#2912)
  * worker/osbuild: use `os-release` to determine host OS (#2842)
Contributions from: Achilleas Koutsou, Juan Abia, Simon de Vlieger, Tomas Hozza, Xiaofeng Wang
— Somewhere on the Internet, 2022-08-26





* Wed Aug 24 2022 Packit <hello@packit.dev> - 60-1
Changes with 60
----------------
  * Add search command to dnf-json and use it for package searches (#2908)
  * Modify repositories/rhel-xy.json file before testing nightly compose (#2894)
  * Update terraform SHA with more aarch64 runner options (#2907)
  * [GCE images] don't install SDK and turn off GPG check on el9 (#2900)
  * distro/image-installer: remove nvmf dracut module for RHEL-9.1 (#2899)
  * distro: add oscap packages to image (#2898)
  * tests: Add comment to make it more obvious what's happening (#2888)
  * tests: Remove useless JSON file overrides (#2881)
  * update civ (#2796)
Contributions from: Alexander Todorov, Brian C. Lane, Gianluca Zuccarelli, Jakub Rusz, Juan Abia, Tomas Hozza, Xiaofeng Wang
— Somewhere on the Internet, 2022-08-24





* Wed Aug 10 2022 Packit <hello@packit.dev> - 59-1
Changes with 59
----------------
  * Allow for `/boot` to be customized (#2865)
  * CI: use only medium runners on Openstack (#2866)
  * Cloud API - support uploading to container registries (#2858)
  * Cloud API: add support for container embedding (#2877)
  * Exclude dracut-config-rescue in ec2 and qemu-guest-agent in ec2 and gce images (#2862)
  * Fix Go 1.19 issues (stable `fstab` ordering and wrong `errors.As` usages) (#2860)
  * Fix UEFI HTTP boot for RHEL 9 ISOs (#2854)
  * Use JWT for Koji tests (#2853)
  * clienterrors: Remove ellipsis operator (#2876)
  * internal/container: delete leftover dead code (#2867)
  * metrics: add `arch` label to prometheus metrics (#2845)
  * osbuild-mock-openid-provider: support `client_credentials` grant type (#2880)
  * osbuild-service-maintenance: Honor dry run config option (#2868)
  * osbuild-service-maintenance: Run vacuum analyze after each delete (#2863)
  * oscap: implement OpenSCAP build remediation (#2695)
  * templates/dashboard: filter worker dashboard on `arch` (#2847)
  * templates/dashboards: Add brew tenants (#2872)
  * templates/dashboards: Drop arch from osbuild jobtype (#2871)
  * test: Remove BIOS installation test because edge-installer supports UEFI only (#2870)
  * tests: Workaround for mkksiso options coming from newer lorax RPM (#2875)
  * worker: fix crash if no autoscale instance is defined (#2879)
Contributions from: Achilleas Koutsou, Alexander Todorov, Christian Kellner, Gianluca Zuccarelli, Jakub Rusz, Ondřej Budai, Sanne Raymaekers, Tomas Hozza, Xiaofeng Wang, Ygal Blum
— Somewhere on the Internet, 2022-08-10





* Wed Jul 27 2022 Packit <hello@packit.dev> - 58-1
Changes with 58
----------------
  * Add support for container embedding (#2814)
  * CI: drop /tmp/artifacts upload to Gitlab (#2857)
  * COMPOSER-1623: Enable Fedora 36 testing (#2782)
  * Container embedding: support accessing protected resources (#2849)
  * Embedding container in OSTree commits (#2848)
  * Filesystems test update (#2843)
  * Improvements for gen-manifests tool and Manifest-diff test (#2821)
  * Koji cloud upload fixups (#2852)
  * Regenerate fedora-35 manifests + switch RHOS-01 to non ssd (#2825)
  * Remove centos-8 repos (#2827)
  * Remove image info from all test manifests (#2855)
  * Remove koji API and the osbuild-koji job (#2822)
  * Remove osbuild1 package (#2823)
  * Support cloud upload for Koji composes (#2844)
  * Tests: Use unified diff format - easier to read (#2820)
  * Update snapshots to 20220715 (#2835)
  * blueprint: Hash all user passwords (#2834)
  * build(deps): bump actions/setup-go from 2 to 3 (#2815)
  * ci/tests: Change the way artifacts are collected (#2474)
  * image: introduce an ImageKind abstraction (#2813)
  * jobqueue: store an expiry date (#2816)
  * tag created vmare VMs (#2819)
  * templates: update dashboards to include tenant (#2756)
  * test: Install package sssd in all edge images for BZ#2088459 (#2681)
  * test: Update test for push container image to registry (#2831)
Contributions from: Achilleas Koutsou, Alexander Todorov, Brian C. Lane, Chloe Kaubisch, Christian Kellner, Gianluca Zuccarelli, Jakub Rusz, Juan Abia, Ondřej Budai, Simon de Vlieger, Tom Gundersen, Tomas Hozza, Xiaofeng Wang, dependabot[bot], schutzbot
— Somewhere on the Internet, 2022-07-27





* Wed Jul 27 2022 Packit <hello@packit.dev> - 58-1
Changes with 58
----------------
  * Add support for container embedding (#2814)
  * CI: drop /tmp/artifacts upload to Gitlab (#2857)
  * COMPOSER-1623: Enable Fedora 36 testing (#2782)
  * Container embedding: support accessing protected resources (#2849)
  * Embedding container in OSTree commits (#2848)
  * Filesystems test update (#2843)
  * Improvements for gen-manifests tool and Manifest-diff test (#2821)
  * Koji cloud upload fixups (#2852)
  * Regenerate fedora-35 manifests + switch RHOS-01 to non ssd (#2825)
  * Remove centos-8 repos (#2827)
  * Remove image info from all test manifests (#2855)
  * Remove koji API and the osbuild-koji job (#2822)
  * Remove osbuild1 package (#2823)
  * Support cloud upload for Koji composes (#2844)
  * Tests: Use unified diff format - easier to read (#2820)
  * Update snapshots to 20220715 (#2835)
  * blueprint: Hash all user passwords (#2834)
  * build(deps): bump actions/setup-go from 2 to 3 (#2815)
  * ci/tests: Change the way artifacts are collected (#2474)
  * image: introduce an ImageKind abstraction (#2813)
  * jobqueue: store an expiry date (#2816)
  * tag created vmare VMs (#2819)
  * templates: update dashboards to include tenant (#2756)
  * test: Install package sssd in all edge images for BZ#2088459 (#2681)
  * test: Update test for push container image to registry (#2831)
Contributions from: Achilleas Koutsou, Alexander Todorov, Brian C. Lane, Chloe Kaubisch, Christian Kellner, Gianluca Zuccarelli, Jakub Rusz, Juan Abia, Ondřej Budai, Simon de Vlieger, Tom Gundersen, Tomas Hozza, Xiaofeng Wang, dependabot[bot], schutzbot
— Somewhere on the Internet, 2022-07-27





* Tue Jul 19 2022 Maxwell G <gotmax@e.email> - 57-2
- Rebuild for CVE-2022-{1705,32148,30631,30633,28131,30635,30632,30630,1962} in
  golang

* Wed Jul 13 2022 Packit <hello@packit.dev> - 57-1
Changes with 57
----------------
  * Composer API - add support for service enable/disable (#2755)
  * Dockerfile: bump the shutdown period to 15 seconds (#2808)
  * Drop support for RHEL 8.3 (rhel8) and rename rhel86 to rhel8 (#2793)
  * Enable Image Builder to build GCP-compatible RHEL 9.0 images (#2771)
  * Ground work to enable cloud uploads for Koji composes (#2748)
  * Merge RHEL 8.4 distro definition into distro/rhel8 package (#2805)
  * Merge RHEL 8.5 distro definition into the distro/rhel86 package (#2787)
  * Minor test fixes (#2792)
  * build(deps): bump gopkg.in/ini.v1 from 1.66.4 to 1.66.6 (#2719)
  * containers/osbuild-composer: Sleep before shutdown to mitigate connections being reset/terminated on shutdown (#2797)
  * image-tests: skip azure-rhui test on rhel-86 (#2785)
  * jobqueue: Move jobqueue out of internal packages (#2736)
  * manifest+playground: improve developer experience (#2812)
  * manifest/os: minor refactoring to make more arguments optional (#2799)
  * manifest/os: move over bootloader packages (#2801)
  * manifest: introduce `platform`, `environment` and `workload` abstractions (#2804)
  * osbuild-image-tests: ignore LVM UUID (#2818)
  * packer: use 8.6 as a base for RHEL images (#2790)
  * packit: Enable Bodhi update feature (#2828)
  * pipeline: add Manifest abstraction (#2776)
  * set a job error when a heartbeat fails & fix koji-finalize job (#2784)
  * tag azure resources with gitlab-ci-test (#2786)
  * test/api: split into multiple files (#2789)
Contributions from: Achilleas Koutsou, Christian Kellner, Gianluca Zuccarelli, Jakub Rusz, Juan Abia, Ondřej Budai, Sanne Raymaekers, Tom Gundersen, Tomas Hozza, Ygal Blum, dependabot[bot], fkolwa, imagebuilder-bot, schutzbot
— Somewhere on the Internet, 2022-07-13





* Wed Jun 29 2022 Packit <hello@packit.dev> - 56-1
Changes with 56
----------------
  * CI: new test for checking if any manifests changed in a PR (#2749)
  * Consolidate Koji target options values meaning (#2758)
  * Fedora - Use vendor instead of rpm dependencies (#2762)
  * Remove vhd image type from RHEL 7 (#2768)
  * Support the insecure option in curl sources (#2752)
  * Switch to latest RHEL versions for testing (#2678)
  * [rhel7] add initial support (qcow2, vhd, azure-rhui) (#2705)
  * build(deps): bump github.com/aws/aws-sdk-go from 1.44.4 to 1.44.43 (#2777)
  * cloudapi: get specific error from openapi (#2666)
  * cmd/osbuild-upload-gcp: fix typo in skip-import's help string (#2761)
  * dnf-json: fix depsolve error handling (#2775)
  * dnfjson: Load subscriptions when creating a new solver (#2751)
  * docker-compose: fix osbuild-worker unable load libcrypt.so.1 (#2745)
  * manifests: regenerate RHEL-8.6 qcow2 test cases (#2781)
  * pipelines: introduce declarative pipeline abstractions (#2773)
  * rpmbuild: add fedora-36 (#2770)
  * upload: initial draft for container upload (#2462)
  * worker: clean up the config and add tests (#2779)
Contributions from: Achilleas Koutsou, Alexander Todorov, Chloe Kaubisch, Christian Kellner, Jakub Rusz, Juan Abia, Ondřej Budai, Sanne Raymaekers, Tom Gundersen, Tomas Hozza, Ygal Blum, dependabot[bot], zwtop
— Somewhere on the Internet, 2022-06-29





* Wed Jun 29 2022 Packit <hello@packit.dev> - 56-1
Changes with 56
----------------
  * CI: new test for checking if any manifests changed in a PR (#2749)
  * Consolidate Koji target options values meaning (#2758)
  * Fedora - Use vendor instead of rpm dependencies (#2762)
  * Remove vhd image type from RHEL 7 (#2768)
  * Support the insecure option in curl sources (#2752)
  * Switch to latest RHEL versions for testing (#2678)
  * [rhel7] add initial support (qcow2, vhd, azure-rhui) (#2705)
  * build(deps): bump github.com/aws/aws-sdk-go from 1.44.4 to 1.44.43 (#2777)
  * cloudapi: get specific error from openapi (#2666)
  * cmd/osbuild-upload-gcp: fix typo in skip-import's help string (#2761)
  * dnf-json: fix depsolve error handling (#2775)
  * dnfjson: Load subscriptions when creating a new solver (#2751)
  * docker-compose: fix osbuild-worker unable load libcrypt.so.1 (#2745)
  * manifests: regenerate RHEL-8.6 qcow2 test cases (#2781)
  * pipelines: introduce declarative pipeline abstractions (#2773)
  * rpmbuild: add fedora-36 (#2770)
  * upload: initial draft for container upload (#2462)
  * worker: clean up the config and add tests (#2779)
Contributions from: Achilleas Koutsou, Alexander Todorov, Chloe Kaubisch, Christian Kellner, Jakub Rusz, Juan Abia, Ondřej Budai, Sanne Raymaekers, Tom Gundersen, Tomas Hozza, Ygal Blum, dependabot[bot], zwtop
— Somewhere on the Internet, 2022-06-29





* Wed Jun 15 2022 Packit <hello@packit.dev> - 55-1
Changes with 55
----------------
  * Add an option to tag page blobs in Azure (#2644)
  * Add support for uploading to generic S3 service using the Composer API (#2686)
  * Blacklist amdgpu module on Azure images (#2717)
  * CI: Integrate cloud image val (#2692)
  * COMPOSER-1576: Start building rpms on 9.0 and 8.6 GA (#2716)
  * Migrate scheduled cloud cleaner to separate repo (#2728)
  * Remove UnmarshalJSON for Stage and StageOptions in osbuild packages (#2741)
  * Service maintenance: Delete results from manifest and depsolve jobs (#2707)
  * Size-based cleanup for dnf-json cache directories (#2733)
  * ci: Adjust release schedule timer (#2744)
  * cloudapi: standardize format of url strings (#2659)
  * cloudapi: use `osbuild` jobs for Koji composes (#2636)
  * dbjobqueue-tests: fix issue introduced by PR #2618 (#2730)
  * distro/rhel90: remove skx_edac, intel_cstate from denylist again (#2708)
  * dnfjson: add repository name and URL to repo-related error messages (#2734)
  * osbuild-service-maintenance:  vacuum  analyze after update (#2727)
  * osbuild-service-maintenance: Delete/update results in chunks (#2724)
  * osbuild-worker: Correct cast of dnfjson error in depsolve job (#2731)
  * packer: pin the vector version (#2725)
  * prometheus: add tenant label (#2618)
  * templates/composer: Map db secrets to maintenance container (#2722)
  * worker/osbuild: fix forgotten return when koji upload fails (#2746)
Contributions from: Achilleas Koutsou, Alexander Todorov, Chloe Kaubisch, Christian Kellner, Juan Abia, Major Hayden, Ondřej Budai, Sanne Raymaekers, Simon Steinbeiss, Tomas Hozza, Ygal Blum
— Somewhere on the Internet, 2022-06-15





* Wed Jun 01 2022 Packit <hello@packit.dev> - 54-1
Changes with 54
----------------
  * Add kube-linter check to github tests workflow (#2698)
  * Compress Azure RHUI artefacts (#2693)
  * Upload to HTTPS S3 - Support self signed certificate (#2655)
  * [rhel86/rhel90] blacklist skx_edac,intel_cstate kernel modules and enable nm-cloud-setup on azure  (#2706)
  * [rhel9] Fixes for grub2 config (ImageConfig) and azure-rhui (#2674)
  * cloudapi: Drop bucket from composer config (#2697)
  * dnf-json script and Go module rewrite (#2537)
  * templates: add Fedora prod tenant to the ACL (#2699)
  * terraform: bump to a version that does spot fleets (#2610)
  * test/old-worker: change user and package verification check (#2689)
  * test: add prominent message in test script cleanup functions (#2687)
  * tests/gcp: pick machine type from those available in the zone (#2684)
Contributions from: Achilleas Koutsou, Christian Kellner, Ondřej Budai, Sanne Raymaekers, Tomas Hozza, Ygal Blum
— Somewhere on the Internet, 2022-06-01





* Thu May 19 2022 Packit <hello@packit.dev> - 53-1
Changes with 53
----------------
  * Old worker - New composer test: Use Cloud API (#2654)
  * Post release version bump (#2670)
  * distro/rhel90: add support for azure marketplace (#2665)
  * go.mod: Update openshift-online/ocm-sdk-go (#2660)
Contributions from: Achilleas Koutsou, Christian Kellner, Sanne Raymaekers, Simon Steinbeiss
— Somewhere on the Internet, 2022-05-19





* Wed May 04 2022 Packit <hello@packit.dev> - 51-1
Changes with 51
----------------
  * Add 9.1 alias & 8.7 test repositories (#2602)
  * Devcontainer update to Fedora 36.  (#2609)
  * Don't support `gce-rhui` image type on CentOS Stream 8 (#2600)
  * New functions for resizing partitions based on directory size requirements (#2588)
  * RHEL-8.6/9.0 EC2 SAP image changes (#2574)
  * Schutzfile: Pin osbuild version to use minimal required caps (#2597)
  * Update GPG keys for all RHEL 8.x repos (#2563)
  * Use array of objects to maintain order for RPM stage inputs (#2578)
  * build(deps): bump cloud.google.com/go/cloudbuild from 1.0.0 to 1.2.0 (#2553)
  * build(deps): bump cloud.google.com/go/compute from 1.6.0 to 1.6.1 (#2587)
  * build(deps): bump github.com/Azure/azure-sdk-for-go from 63.1.0+incompatible to 63.4.0+incompatible (#2583)
  * build(deps): bump github.com/Azure/go-autorest/autorest from 0.11.25 to 0.11.27 (#2579)
  * build(deps): bump github.com/aws/aws-sdk-go from 1.43.42 to 1.44.4 (#2606)
  * build(deps): bump github.com/google/go-cmp from 0.5.7 to 0.5.8 (#2607)
  * build(deps): bump github.com/hashicorp/go-retryablehttp from 0.7.0 to 0.7.1 (#2571)
  * build(deps): bump google.golang.org/api from 0.74.0 to 0.75.0 (#2585)
  * cloudapi/v2: Generate valid GCP image name (#2586)
  * disk: fix ensureLVM for partition tables without /boot (#2580)
  * entrypoint - add parameters for socket bind address and port (#2605)
  * image-info: dynamically detect the rpm database (#2594)
  * rhel85: automatically convert to LVM on fs customizations (#2552)
  * tools/generate-all-test-cases: add `manifests` command (#2593)
  * worker: add proxy support to worker (#2576)
  * 📦🔗📦  Introduce chain dependency solving (#2568)
Contributions from: Achilleas Koutsou, Alexander Todorov, Christian Kellner, Ondřej Budai, Sanne Raymaekers, Simon de Vlieger, Tomas Hozza, Ygal Blum, dependabot[bot]
— Somewhere on the Internet, 2022-05-04





* Thu Apr 28 2022 Packit <hello@packit.dev> - 46.3-1
CHANGES WITH 46.3:
----------------
 * disk: fix ensureLVM for partition tables without /boot (#2580)
Contributions from: Achilleas Koutsou, Christian Kellner
— Liberec, 2022-04-28




* Wed Apr 20 2022 Packit <hello@packit.dev> - 50-1
Changes with 50
----------------
  * COMPOSER-1401: Add tests for blueprints without explicit definition for / (#2412)
  * Empty manifest check for osbuild jobs (#2520)
  * Generic S3 test - retry creating the alias in case the service is not yet up (#2543)
  * Introduce Google GCE image type (RHEL, CentOS Stream) and support importing to GCP on premise (#2155)
  * Pin fedora repositories in Schutzfile + override mock templates with rpmrepo snapshots (#2508)
  * Support uploading to any S3 service via the WELDR API (#2471)
  * Worker dependency errors (#2505)
  * build(deps): bump cloud.google.com/go/storage from 1.18.2 to 1.22.0 (#2565)
  * build(deps): bump github.com/Azure/azure-sdk-for-go from 57.4.0+incompatible to 63.1.0+incompatible (#2532)
  * build(deps): bump github.com/Azure/go-autorest/autorest/azure/auth from 0.5.8 to 0.5.11 (#2534)
  * build(deps): bump github.com/BurntSushi/toml from 0.4.1 to 1.1.0 (#2525)
  * build(deps): bump github.com/aws/aws-sdk-go from 1.42.25 to 1.43.38 (#2548)
  * build(deps): bump github.com/aws/aws-sdk-go from 1.43.38 to 1.43.42 (#2566)
  * build(deps): bump github.com/google/go-cmp from 0.5.6 to 0.5.7 (#2526)
  * build(deps): bump github.com/gophercloud/gophercloud from 0.22.0 to 0.24.0 (#2536)
  * build(deps): bump github.com/jackc/pgtype from 1.8.1 to 1.10.0 (#2524)
  * build(deps): bump github.com/jackc/pgx/v4 from 4.13.0 to 4.15.0 (#2530)
  * build(deps): bump github.com/labstack/echo/v4 from 4.6.1 to 4.7.2 (#2531)
  * build(deps): bump github.com/prometheus/client_golang from 1.12.0 to 1.12.1 (#2549)
  * build(deps): bump github.com/spf13/cobra from 0.0.3 to 1.4.0 (#2560)
  * build(deps): bump github.com/stretchr/testify from 1.7.0 to 1.7.1 (#2535)
  * build(deps): bump github.com/vmware/govmomi from 0.26.1 to 0.27.4 (#2554)
  * build(deps): bump gopkg.in/ini.v1 from 1.63.0 to 1.66.4 (#2292)
  * cloudapi: specify min_size type (#2319)
  * gitlab: fix nightly testing (#2569)
  * lib: upgrade prometheus client to 1.12 (#2528)
  * osbuild2: QEMU stage implementation enhancement and code de-duplication (#2521)
  * templates/packer: Rely on instance metadata to set region (#2562)
  * workflows/trigger-gitlab: run Gitlab CI in new image-builder project (#2547)
Contributions from: Alexander Todorov, Chloe Kaubisch, Christian Kellner, Gianluca Zuccarelli, Jakub Rusz, Ondřej Budai, Sanne Raymaekers, Thomas Lavocat, Tomas Hozza, Ygal Blum, dependabot[bot]
— Somewhere on the Internet, 2022-04-20





* Wed Apr 06 2022 Packit <hello@packit.dev> - 49-1
Changes with 49
----------------
  * Add Xiaofeng to notifications for nightly pipeline (#2486)
  * Add `cloud-init` to VMDK image and test it in VSphere (#2459)
  * Centos pinning + Schutzfile update (#2494)
  * Create users at install time for image and edge installers (#2375)
  * Dependency joberrors (#2477)
  * Fix excessive logging and monitoring (#2497)
  * Minor CI changes (#2468)
  * RHEL (all): Create users at install time for image and edge installers (#2516)
  * RHEL-90: use XBOOTLDR partition GUID for `/boot` (#2473)
  * Regression tests split (#2498)
  * `rhel{86,90}`: set default grub boot entry to `saved` (#2418)
  * build(deps): bump actions/checkout from 2.4.0 to 3 (#2394)
  * build(deps): bump actions/github-script from 5 to 6 (#2463)
  * build(deps): bump actions/setup-go from 2.1.5 to 3 (#2395)
  * build(deps): bump github.com/Azure/go-autorest/autorest from 0.11.21 to 0.11.25 (#2507)
  * ci: re-enabled Installer test on centos-stream-9 (#2514)
  * cloudapi: improve gpgkey handling & enable edge-commit on Fedora (#2479)
  * cloudapi: prevent dangling goroutines after the server is terminated (#2518)
  * cmd: add `osbuild-package-sets` for printing package sets of an image (#2484)
  * container: fix liveness probe (#2482)
  * gitlab: split integration tests (#2488)
  * koji: fix retries when uploading chunks (#2466)
  * osbuild2: honor GPG key setting for rpm inputs (#2432)
  * repositories: update key for RHEL 9.0 (#2509)
  * rhel8/9: fix path to fdo diun root certificates (#2434)
  * templates/composer: Add prod service accounts owner (#2478)
  * templates/composer: Drop unused variables (#2481)
  * templates/composer: Remove unused acl claims (#2483)
  * test/ostree-simplified-installer: destroy VM fixup (#2487)
  * test: Add retries on ubi8 image and greenboot package downloading (#2493)
  * test: Clean up and improve ostree-simplified-installer.sh (#2485)
  * test: Enable CS9 test for ostree-rebase and ostree (#2515)
  * test: use `T.TempDir` to create temporary test directory (#2417)
  * tests: Run SonarQube analysis only on main branch (#2489)
  * tools/define-compose-url: change url back to nightly (#2513)
Contributions from: Achilleas Koutsou, Alexander Todorov, Antonio Murdaca, Christian Kellner, Diaa Sami, Eng Zer Jun, Gianluca Zuccarelli, Jakub Rusz, Ondřej Budai, Sanne Raymaekers, Tomas Hozza, Xiaofeng Wang, dependabot[bot], yih
— Somewhere on the Internet, 2022-04-06





* Sat Apr 02 2022 Packit <hello@packit.dev> - 46.2-1
CHANGES WITH 46.2:
----------------
 * repositories: update key for RHEL 9.0  (#2509)
Contributions from: Ondřej Budai
— Liberec, 2022-04-02




* Fri Apr 01 2022 Packit <hello@packit.dev> - 46.1-1
CHANGES WITH 46.1:
----------------
  * internal/distro/rhel{86,90}: drop console kargs from raw image deployment (#2377)
  * RHEL-90: use XBOOTLDR partition GUID for /boot (#2473)
  * Create users at install time for image and edge installers (#2375)
  * rhel{86,90}: set default grub boot entry to saved (#2418)
  * rhel8/9: fix path to fdo diun root certificates (#2434)
  * nightly: update GPG key in prepare-rhel-internal & fix some tests (#2389)
  * mockbuild: use public EPEL-9 (#2364)
  * api.sh: encrypt the DB dump artifact (#2472)
  * image tests: update GPG keys used for RHEL-9.0 repos (#2390)
  * gitlab: split integration tests (#2488)
  * test/cases/simpl installer: bump to use fdo 0.4.0 (#2380)
  * test/ostree-simplified-installer: destroy VM fixup (#2487)
  * test/image-tests: temporarily skip azure_rhui image testing (#2402)
  * test: Clean up and improve ostree-simplified-installer.sh (#2485)
  * test: Add retries on ubi8 image and greenboot package downloading (#2493)
  * tests/upgrade: update gpg key (#2467)
  * test: add tests purpose (#2346)
  * test/api.sh cleanup (#2444)
  * Centos pinning + Schutzfile update (#2494)
  * Update snapshots to 20220301 (#2376)
  * ci: run ci_details.sh in before_script (#2403)
  * ci: Minor CI changes (#2468)
  * ci: skip CI for draft and WIP PRs (#2286)
  * ci: modify Gitlab CI trigger (#2416)
  * ci: Fix Gitlab CI trigger + revert debug (#2457)
Contributions from: Achilleas Koutsou, Alexander Todorov, Antonio Murdaca, Christian Kellner,
                    Jakub Rusz, Juan Abia, Ondřej Budai, Tomas Hozza, Xiaofeng Wang
— Vöcklabruck, 2022-04-01




* Wed Mar 23 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 48-1
CHANGES WITH 48:
----------------
  * create-tag: Fix bash typo (#2476)
  * image tests: update GPG keys used for RHEL-9.0 repos (#2390)
  * create-tag: Fix upstream release schedule (#2475)
  * api.sh: encrypt the DB dump artifact (#2472)
  * Enable scheduled upstream releases (#2458)
  * dbjobqueue: fix race condition (#2456)
  * container: graceful shutdown (#2447)
  * tests/upgrade: update gpg key (#2467)
  * deploy: work around a podman bug in CS8  (#2464)
  * templates/composer: Add stage service accounts owner (#2465)
  * workflows: Fix Gitlab CI trigger + revert debug (#2457)
  * Client creds grant worker client (#2433)
  * workflows: debug Gitlab CI trigger (#2441)
  * osbuild-worker: Log unexpected dnf-json errors (#2454)
  * packer: use unique name tag for Fedora workers (#2429)
  * `test/api.sh` cleanup (#2444)
  * internal/distro/rhel{86,90}: drop console kargs from raw image deploy… (#2377)
  * Dashboards - Minor fixes (#2435)
  * github workflows: modify Gitlab CI trigger (#2416)
  * ci: run ci_details.sh in before_script (#2403)
  * packer: fix the secret ID variable in get_koji_creds.sh (#2431)
  * packer: make subscribing optional (#2430)
  * packer: make all credentials optional and add support for koji credentials (#2426)
  * dnf-json: use the default connection timeout (#2428)
  * Pass repo name to `dnf-json` and use it in `dnf-json` (#2427)
  * dbjobqueue: reduce the number of needed connections (#2393)
  * cmd/osbuild-worker: dnf-json returns MarkingErrors (plural) (#2361)
  * use app-sre packer image (#2409)
  * packer: Build Fedora 35 x86_64 and aarch64 images (#2423)
  * github: fix job names and IDs for the tests workflow (#2422)
  * weldr: Run on unsupported distros (#2399)
  * koji: reduce excessive logging by retryablehttp (#2397)
  * test: add tests purpose (#2346)
  * Packit: build SRPMs in Copr (#2414)
  * mockbuild: use public EPEL-9 (#2364)
  * cmd/osbuild-worker: Pass bucket config to job implementation (#2411)
Contributions from: Achilleas Koutsou, Antonio Murdaca, Diaa Sami, Feng Huang, Gianluca Zuccarelli, Jakub Rusz, Juan Abia, Laura Barcziova, Ondřej Budai, Sanne Raymaekers, Simon Steinbeiss, Tom Gundersen, Tomas Hozza, kingsleyzissou
— Somewhere on the Internet, 2022-03-23





* Wed Mar 09 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 47-1
CHANGES WITH 47:
----------------
  * cloudapi/v2: add error object to ImageStatus (#2298)
  * cmd/osbuild-worker: Configure s3 bucket on the worker itself (#2404)
  * 🍏  Make CI green again (#2401)
  * 🍏  test/image-tests: temporarily skip azure_rhui image testing (#2402)
  * templates/composer: give access to Fedora org (#2405)
  * dnf-json codestyle cleanup (#2391)
  * cloudapi: add support for multi-tenancy (#2344)
  * ci: skip CI for draft and WIP PRs  (#2286)
  * nightly: update GPG key in prepare-rhel-internal & fix some tests (#2389)
  * templates/packer: Remove -u flag from creds mapping script (#2396)
  * Implement HTTP retries for koji jobs (#2352)
  * `rhel86` various fixes for the `azure-rhui` image (#2387)
  * Update snapshots to 20220301 (#2376)
  * schutzbot: update terraform SHA (#2385)
  * test/cases/simpl installer: bump to use fdo 0.4.0 (#2380)
  * schutzbot: fix jrusz ssh key (#2384)
  * schutzbot: add jrusz ssh-key (#2383)
  * Small cloudapi cleanups (#2379)
  * cmd/osbuild-service-maintenance: Log aws error (#2315)
  * templates/composer: Parametrize bucket name (#2372)
Contributions from: Achilleas Koutsou, Antonio Murdaca, Christian Kellner, Diaa Sami, Gianluca Zuccarelli, Jakub Rusz, Ondřej Budai, Sanne Raymaekers, Tomas Hozza, Xiaofeng Wang, ondrejbudai, schutzbot
— Cork, 2022-03-09




* Mon Feb 28 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 46-1
CHANGES WITH 46:
----------------
  * Simplified installer: add support for encrypted raw images (#2295)
  * rhel86: automatically convert to LVM on fs customizations (#2373)
  * RHEL9.0: convert layout to LVM on filesystem customisations (#2354)
  * Update snapshots to 20220227 (#2370)
  * Add Azure Marketplace images (#2358)
  * devcontainer: adapt to composer (#2306)
  * Update snapshots to 20220226 (#2368)
  * RHEL 8.6: Add lvm2 to build root (#2367)
  * schutzbot: keep runners alive when users are logged on (#2328)
  * Adjust filesystem tests (#2362)
  * Set selinux to permissive mode for installers (#2359)
  * RHEL-90: use C.UTF-8 for images that only have glibc-minimal-langpack (#2351)
  * test: Add work around for bug bz#2057769 (#2366)
  * templates: Add production worker account to acl (#2365)
  * tests/libvirt: add some regression tests (#2294)
  * test/manifest/image-installer: fix conflicting merge (#2360)
  * rhel86/90: change isolevel of image-installer to 3 (#2325)
  * Update snapshots to 20220222 (#2343)
  * simplified installer (8/9): support FDO (#1884)
  * Image installer on aarch64 (#2355)
  * FS minimum size (#2353)
  * templates/composer: Verify against mass sso and rh sso (#2349)
  * RHEL 9.0: Fix customisation of Kernel command line options (#2342)
  * internal/cloudapi: Allow bp.Customizations being nil (#2340)
  * Support specifying OSTree Parent and URL for creating upgrade commits (#2201)
  * COMPOSER-1343: Revert "tests: Conditionally enable osbuild-dnf-json-tests" (#2338)
  * Update team_ssh_keys.txt (#2333)
  * templates/worker: fix depsolve error rate (#2337)
  * worker/osbuild-koji: fix double-reporting of osbuild-koji job status (#2327)
  * Revert "mockbuild: temporarily pin RHEL 9 compose to an older one" (#2332)
  * test: Remove "ansible-galaxy collection install" (#2334)
  * Schutzfile: Pin centos-9's osbuild commit (#2339)
  * LUKS & LVM support and file system refactoring (#2141)
  * internal/cloudapi: Log error in manifest job (#2336)
  * internal/cloud: Allow aws creds from defaults (#2291)
  * worker: use default transport instead of "blank" one (#2316)
  * cloudapi: expose filesystem customizations (#2285)
Contributions from: Achilleas Koutsou, Alexander Todorov, Antonio Murdaca, Chloe Kaubisch, Christian Kellner, Djebran Lezzoum, Gianluca Zuccarelli, He Yi, Jakub Rusz, Ondřej Budai, Sanne Raymaekers, Tom Gundersen, Tomas Hozza, Xiaofeng Wang
— Vöcklabruck, 2022-03-01




* Fri Feb 18 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 45-1
CHANGES WITH 45:
----------------
  * mockbuild: temporarily pin RHEL 9 compose to an older one (#2321)
  * Add CentOS Stream 9 support (#2142)
  * Cancel waiting compose (#2237)
  * tests: Use human readable size for mountpoint (#2304)
  * worker: Properly log successful image builds (#2313)
  * Deduplicate some code in distro definitions (#2314)
  * tests/upgrade: gather more logs (#2299)
  * packer: make the worker image smaller (#2311)
  * ci/nightly: report composer NVR in slack (#2317)
  * fsjobqueue: refactor to allow dequeuing by multiple criteria (#2307)
  * github: fetch more PRs when triggering gitlab (#2312)
  * Update greenboot packaging names (#2196)
  * github: split checks into 3 jobs (#2308)
  * cmd/osbuild-service-maintenance: GCP deletes by image name (#2293)
  * Extend information gathered by `image-info` (#2303)
  * Fix problem with undo creating empty blueprint (#2207)
  * Support associating repositories to package sets (#2265)
  * Use the latest RPMRepo snapshot for RHEL-9.0 image tests (#2279)
  * tests: update IDs in Openstack image boot test (#2263)
  * Pre-define an ostree remote for RFE raw images (including created via simplified installer) (#2284)
Contributions from: Achilleas Koutsou, Alexander Todorov, Brian C. Lane, Christian Kellner, Jakub Rusz, Ondřej Budai, Peter Robinson, Sanne Raymaekers, Simon Steinbeiss, Thomas Lavocat, Tomas Hozza, Xiaofeng Wang
— Liberec, 2022-02-18




* Fri Feb 11 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 44-1
CHANGES WITH 44:
----------------
  * Relax TCP timeouts for koji connections (#2282)
  * cloudapi/v2: add support for aws-*-rhui image types (#2281)
  * Add oracle-oci.md under image-types/rhel8 (#2283)
  * Appsre packer 85 (#2274)
  * Add missing F34 and F35 image test cases (#2276)
  * templates/dashboard: worker metric queries (#2277)
  * distro: add an alias for RHEL 8.7 (#2270)
  * metrics: change job metrics namespace (#2272)
  * Revert "templates: Add dnf-json template" (#2273)
  * Sonarqube fix + Schutzfile repo rename (#2261)
  * Drop F33 support and add F34/F35 image tests (#2264)
  * github: fix gitlab trigger (#2271)
  * Skip CI for draft PRs or WIP label (#2238)
  * service-maintenance: Skip db cleanup (#2252)
  * templates/dashboards: worker error metrics (#2267)
  * build(deps): bump cloud.google.com/go/cloudbuild from 0.2.0 to 1.0.0 (#2153)
  * update testing doc with cloud cleaner info (#2256)
  * RHEL-90: Remove deprecated `crashkernel=auto` option (#2262)
  * templates: Add dnf-json template (#2259)
  * Worker error validation (#2260)
  * Prepare CI to build -tests RPM for downstream testing from source (#2093)
  * worker: fix error status codes (#2258)
  * Workers error metrics (#2247)
  * gitlab-ci: make every stage interruptible (#2248)
  * internal/cloud/gcp: use `pkg.go.dev/cloud.google.com/go` for Compute Engine (#2162)
  * EC2: Disable password based authentication (#2235)
  * Dnf json (#2194)
  * worker/api: align error handler with cloudapi (#2152)
  * cloupapi/v2: add koji support (#2214)
  * RHEL 9.0: Drop IA32 (#2219)
  * jwt: support multiple key providers (#2239)
  * Mock OpenID: add token type, expires in and scope fields (#2240)
  * distro/rhel86: fix ec2 boot partition for arm64 (#2228)
  * Extend scheduled cloud cleaner to vmware (#2200)
  * Kojiapi: fix error check in koji job (#2236)
  * osbuild-worker: change error handling for OCI upload (#2234)
  * distro/rhel90: special case root user for ssh keys (#2220)
  * OCI support (#2031)
  * distro/rhel90: no uuids in dos partition table (#2233)
  * Worker errors backwards compatibility (#2192)
  * repo runner (#2216)
  * test/koji: remove the koji-cli patch (#2223)
  * packit: re-enable builds for s390x architecture (#2246)
Contributions from: Achilleas Koutsou, Alexander Todorov, Antonio
                    Murdaca, Christian Kellner, Diaa Sami, Gianluca
                    Zuccarelli, Jakub Rusz, Juan Abia, Ondřej Budai,
                    Pavel Raiskup, Roy Golan, Sanne Raymaekers,
                    Tom Gundersen, Tomas Hozza, Thomas Lavocat
— Grenoble, 2022-02-11




* Wed Jan 26 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 43-1
CHANGES WITH 43:
----------------
  * templates/dashboards: Fixed grafana uids (#2202)
  * CI: Updates to ensure smoother running (#2198)
  * templates/packer: Make cdn host check less sensitive (#2199)
  * templates/packer: Correct priority for worker rpms (#2195)
  * tools/appsre-ansible: Don't use /tmp for rpmbuilds (#2186)
Contributions from: Alexander Todorov, Jakub Rusz, Thomas Lavocat,
                    Sanne Raymaekers
— Grenoble, 2022-01-26




* Wed Jan 12 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 42-1
CHANGES WITH 42:
----------------
  * RHEL-86/90: refactoring of `osPipeline` and its variants (#2139)
  * api/cloud: drop v1 API (#2163)
  * weldr: return an error if host distro wasn't found in distro registry (#2158)
  * dnf json cache cleaner (#2119)
  * Update terraform SHA (#2157)
  * build(deps): bump actions/setup-go from 2.1.4 to 2.1.5 (#2156)
Contributions from: Achilleas Koutsou, Jakub Rusz, Juan Abia,
                    Ondřej Budai, Thomas Lavocat, Tomas Hozza,
                    Sanne Raymaekers
— Grenoble, 2022-01-12




* Wed Dec 22 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 41-1
CHANGES WITH 41:
----------------
  * build(deps): bump actions/checkout from 2.3.4 to 2.4.0 (#2007)
  * build(deps): bump github.com/aws/aws-sdk-go from 1.40.49 to 1.42.25 (#2150)
  * osbuild2: fix typo in tar stage option value (#2151)
  * osbuild2: support 'format' and 'root-node' Tar stage options (#2146)
  * Tools: add 'no-image-info' option to image test case requests (#2143)
  * generate-all-test-cases: use `make scratch` for building RPMs (#2138)
  * osbuild-auth-tests: add a build constraint also to certificates.go (#2097)
  * dbjobqueue: fix FinishJob not returning an error if already finished (#2133)
  * osbuild2: Expand dnf_config stage (#2113)
  * test: make test more resilient (#2132)
  * worker: Treat a non echo.HTTPError like a regular error (#2140)
  * osbuild2: ensure that empty sysconfig options members are omitted (#2134)
  * Add support for new osbuild stages needed for GCE image (#2126)
  * tools: use image_type_tags in repos used for image test cases (#2135)
  * composer: Only set queue and artifact dir for fsqueue (#2095)
  * cloudapi: improve logging for errors (#2088)
  * Tracing: measure IO during each job (#2106)
  * Tests: trim dependencies for test generation (#2128)
  * metrics: add additional buckets (#2130)
  * distro/depsolve/cloudapi: Add 3rd-party repository support. (#2101)
  * templates: add worker dashboard (#2127)
  * dnf json as a service (#2062)
  * Extend scheduled cloud cleaner to GCP (#2115)
  * openstack: use rhos-01 (#2120)
  * RHEL-9.0: unify the default partitioning scheme used by all non-EDGE images (#2019)
  * ci: CC QE in notification message (#2118)
  * enable gosec tool (#2073)
  * release-action: Send notification to our Slack channel (#2117)
Contributions from: Alexander Todorov, Diaa Sami, Djebran Lezzoum, Gianluca Zuccarelli, Juan Abia, Ondřej Budai, Sanne Raymaekers, Simon Steinbeiss, Thomas Lavocat, Tomas Hozza, dependabot[bot]
— Liberec, 2021-12-22




* Thu Dec 09 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 40-1
CHANGES WITH 40:
----------------
  * Regression test fixes (#2109)
  * store: set RHSM when initialising SourceConfig with a repo (#2105)
  * spec: build all binaries with PIE (#2102)
  * Job metrics (#2080)
  * tests: Fix several permission and koji failures (#2099)
  * templates: Max concurrent requests is required for the maintenance job (#2107)
  * templates: CronJob is part of the batch/v1 api (#2104)
  * generate-all-test-cases: add `--build-rpms` option (#2098)
  * templates: Add maintenance cronjob (#2100)
  * Use PackIt for building RPMs in COPR for PRs and commits to `main` (#2094)
  * Image Builder Composer - Grafana dashboard Updates (#2089)
  * Cloud API: Support more image types as S3 objects (#2081)
  * osbuild-service-maintenance: Clean up expired images (#2074)
  * cloudapi/v2: No ObjectReference in request bodies (#2042)
  * distro/rhel90: enable edge-simplified-installer image type (#2015)
  * ci: Install gssapi/gssapi.h for Coverity Scan (#2087)
  * 8.5 runners (#2079)
  * RHEL-9.0: Install TuneD by default and stop using `@core` package group (#2084)
  * Build a worker AMI using Schutzbot (#2068)
  * osbuild2: update cloud-init stage with new options (#2051)
  * tests: Small updates to docs (#2011)
  * api/koji: fix /compose/log route (#2078)
  * ci: make some jobs interruptible (#2061)
  * tests/nightly: Re-enable satellite regression test on nightly composes (#2052)
  * test: cloud cleaner aws s3 (#2005)
  * rpmmd: Reload subscriptions (#2067)
  * Two minor logging improvements (#2063)
  * terraform: update to use the new instance type (#2065)
  * spec: add epoch to nevra only if it's set (#2060)
Contributions from: Achilleas Koutsou, Alex Njaastad, Alexander Todorov, Chloe Kaubisch, Gianluca Zuccarelli, Jakub Rusz, Juan Abia, Martin Sehnoutka, Ondřej Budai, Sanne Raymaekers, Tomas Hozza
— Liberec, 2021-12-09




* Wed Nov 24 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 39-1
CHANGES WITH 39:
----------------
  * RHEL-9.0: install and enable TuneD by default on all EC2 images (#2050)
  * Improve contributing.md (#2043)
  * osbuild2: selinux stage - introduce force_autorelabel option (#2033)
  * internal: cleanup dracut modules and default kargs (#2045)
  * Namespaced composer metrics (#2037)
  * cloudapi/v2: Add support for edge-container (#2035)
  * template: bump postgres max conns to 20 (#2044)
  * templates: bump max postgres connections to 10 (#2040)
  * osbuild2: update rhsm stage (#2014)
  * internal: mandate installation device for the simplified installer (#1755)
  * distro/rhel86: use the new coreos-installer-dracut (#1752)
  * Switch api tests to v2 & manifest job in api v2 (#2026)
  * cloudapi/v1: Adapt metadata handler to osbuild2 results (#2028)
  * osbuild: check if result objects are nil in Write() (#2022)
  * distro/rhel90*: minor code cleanup (#2004)
  * osbuild2: support 'install' command in the modprobe stage and rework data validation (#1983)
  * Use RHUI-4 for RHEL-9 EC2 image test cases (#1977)
  * Logging improvements (#1989)
  * worker: Correct servers in openapi spec (#1988)
  * job/osbuild: skip the job if manifest generation failed (#2018)
  * spec: bump osbuild version to 41 (#2012)
  * composer: Add metrics endpoint to auth excludes again (#2013)
  * Use V2 results internally (#1754)
  * worker: Introduce manifest-id-only job (#1999)
  * jobqueue: add the ability to dequeue by ID (#1997)
  * Multiple new stages (#2006)
  * containers: mock oauth container (#2003)
  * osbuild2: new stage sshd config (#1992)
Contributions from: Achilleas Koutsou, Alexander Todorov, Antonio Murdaca, Diaa Sami, Gianluca Zuccarelli, Jakub Rusz, Juan Abia, Martin Sehnoutka, Ondřej Budai, Sanne Raymaekers, Simon Steinbeiss, Tomas Hozza, Xiaofeng Wang, diaasami, sanne, yih
— Berlin, 2021-11-24































* Wed Nov 10 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 38-1
- Revert "templates: Add prometheus scrape annotations to composer-api" (Sanne Raymaekers)
- templates: Add prometheus scrape annotations to composer-api (sanne)
- distroregistry: disable CentOS Stream 9 (Achilleas Koutsou)
- test/cases: rm ostree-ng-og.sh (Achilleas Koutsou)
- distro/rhel90: remove all mentions of obsolete firmware packages (Achilleas Koutsou)
- test/data: update manifests for edge-container images (Achilleas Koutsou)
- distro/rhel90: make nginx log and lib directories world writable (Achilleas Koutsou)
- distro/rhel90: disable edge-simplified-installer image type (Achilleas Koutsou)
- Schutzfile: remove osbuild version pin for RHEL 9.0 (Achilleas Koutsou)
- tools: update distro-arch-imagetype-map for RHEL 9.0 types (Achilleas Koutsou)
- tools: update RHEL 9.0 repos for test case generators (Achilleas Koutsou)
- test/data: update RHEL 9.0 and beta manifests (Achilleas Koutsou)
- test/ostree-simplified: variable string fixes (Achilleas Koutsou)
- distro/rhel90: update unit tests (Achilleas Koutsou)
- rhel90: drop -ga suffix and alias from beta (Achilleas Koutsou)
- test/api: ssh key fixes for RHEL 9.0 (Achilleas Koutsou)
- test/cases: support weldr-client output structure (Achilleas Koutsou)
- CI: test new edge types on RHEL 9.0 (Achilleas Koutsou)
- test/ostree: install python3 instead of specific version (Achilleas Koutsou)
- mockbuild: change RHEL 9 template to use latest non-beta repos (Achilleas Koutsou)
- test/cases: add RHEL 9.0 and CentOS 9 cases to test scripts (Achilleas Koutsou)
- CI: enable tests for RHEL 9.0 (Achilleas Koutsou)
- schutzbot: update terraform sha (Achilleas Koutsou)
- test: update test manifests for rhel-90-ga (Achilleas Koutsou)
- tools: add centos-9 to distro-arch-imagetype-map (Achilleas Koutsou)
- tools: copy rhel-90 distro-arch-imagetype-map to -beta and -ga (Achilleas Koutsou)
- distro/rhel90: update to match 8.6 and add centos-9 alias (Achilleas Koutsou)
- distro/rhel86: remove genisoimage (Achilleas Koutsou)
- distro/rhel86: single osbuild import (Achilleas Koutsou)
- test/data: copy rhel-90 test manifests to -ga and -beta (Achilleas Koutsou)
- test: add repositories for rhel-90-beta and -ga (Achilleas Koutsou)
- distroregistry: add rhel-90-ga to registry (Achilleas Koutsou)
- distro: copy rhel90beta to rhel90 (Achilleas Koutsou)
- composer: Add worker openapi spec endpoint to auth excludes (sanne)
- CI: Journal-log is accessible and encrypted (Thomas Lavocat)
- spec: Only run worker preun if systemd is running (sanne)
- gitlab-ci: Remove RHEL9.0-beta runners (Martin Sehnoutka)
- schutzbot: double quote jq argument to prevent shellcheck failures (Martin Sehnoutka)
- distribution: worker dnf-json & cache dir (Gianluca Zuccarelli)
- cloudapi/v2: 5xx error metrics (Gianluca Zuccarelli)
- internal/blueprint: allow filesystem size specified with units (Martin Sehnoutka)
- internal/blueprint: introduce custom fs customization parser (Martin Sehnoutka)
- internal/blueprint: introduce new test for parsing blueprints (Martin Sehnoutka)
- internal/common: introduce function to convert data sizes (Martin Sehnoutka)
- prepare_rhel_internal: configure s3cmd explicitly (Jakub Rusz)
- templates: add latency metrics to dashboard (Gianluca Zuccarelli)
- Let schutzbot do the post-release version bump (Simon Steinbeiss)
- Post release version bump (Simon Steinbeiss)
- cloudapi: record error metrics (Gianluca Zuccarelli)
- prometheus: add middleware function (Gianluca Zuccarelli)
- prometheus: compose latency metric (Gianluca Zuccarelli)
- prometheus: update metrics (Chloe Kaubisch)
- templates: fix liveness/readiness check url (Ondřej Budai)
- templates: add s3 bucket name (Ondřej Budai)
- templates: update dashboard config map (Gianluca Zuccarelli)
- templates: add grafana dashboard (Gianluca Zuccarelli)
- build(deps): bump github.com/openshift-online/ocm-sdk-go (dependabot[bot])
- templates: hook up simple probes and default limits (Tom Gundersen)
- templates: add service account (Tom Gundersen)

* Wed Oct 27 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 37-1
- Bump version numbers ahead of release (Simon Steinbeiss)
- Switch to simple upstream releases (Simon Steinbeiss)
- distro/rhel86: special case root user for ssh keys (Christian Kellner)
- Revert "Revert "cloudapi/v1: Move depsolving to workers"" (Tom Gundersen)
- templates: image-builder-ci access to composer (Tom Gundersen)
- ci: remove 8.5 nightly testing (Ondřej Budai)
- composer: add json log formatting (Diaa Sami)
- test: timestamp messages in test scripts (Achilleas Koutsou)
- Add news item for updated CentOS Stream 8 definitions (Achilleas Koutsou)
- test/api: SSH_USER=ec2-user for centos on AWS (Achilleas Koutsou)
- test/cases: add centos-8 as support to test scripts (Achilleas Koutsou)
- test/ansible: install greenboot-failing-unit from public source (Achilleas Koutsou)
- CI: enable OSTree tests on CentOS 8 (Achilleas Koutsou)
- test/data: regenerate manifests for CentOS 8 (Achilleas Koutsou)
- distro/rhel86: skip RHSM config stage for non-RHEL (Achilleas Koutsou)
- distro/rhel86: distro private method isRHEL() (Achilleas Koutsou)
- test/data/repositories: update cs8 rpmrepo snapshot (Achilleas Koutsou)
- tools: add all supported image types for centos-8 (Achilleas Koutsou)
- tools/test-case-generators: fix typo in imagetype-map (Achilleas Koutsou)
- distro/rhel86: add distro specific package set (Achilleas Koutsou)
- test: add RHEL 8.6 image installer test manifest (Achilleas Koutsou)
- distro/rhel86: add CentOS Stream 8 as alias to RHEL 8.6 (Achilleas Koutsou)
- distro/rhel86: remove redundant rhel-86 alias (Achilleas Koutsou)
- spec: dnf-json conflicts with old composer (Achilleas Koutsou)
- ostree: change the URL for OC client temporarily (Ondřej Budai)
- test/aws: remove a no longer needed key from an instance (Ondřej Budai)
- ci: pin a specific RHEL 9.0b compose (Ondřej Budai)
- ci: rotate secret names (Ondřej Budai)
- mockbuild: explicitly configure s3cmd (Ondřej Budai)
- mockbuild: remove subscriptions (Ondřej Budai)
- .gitlab-ci: Don't save the journal as an artifact (sanne)
- jobqueue: Better logging (Diaa Sami)
- templates: Claims based on user_ids (sanne)
- worker: Configurable timeout for RequestJob (sanne)
- build(deps): bump cloud.google.com/go/storage from 1.16.1 to 1.18.1 (dependabot[bot])
- build(deps): bump github.com/labstack/echo/v4 from 4.5.0 to 4.6.1 (dependabot[bot])
- build(deps): bump github.com/gophercloud/gophercloud (dependabot[bot])
- worker: Separate goroutine for depsolve jobs (sanne)
- cloudapi/v2: Plural path section when querying a collection (sanne)
- cloudapi/v2: Do not require auth for /openapi or /errors (sanne)
- worker: Configure AWS credentials in the worker (Thomas Lavocat)
- cloudapi/v2: ensure only one image per a compose in the API spec (Ondřej Budai)
- cloudapi/v2: clean up targets (Ondřej Budai)
- cloudapi/v2: move multi-image compose check to the beginning (Ondřej Budai)

* Wed Oct 13 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 36-1
- 36 (Achilleas Koutsou)
- Revert "cloudapi/v1: Move depsolving to workers" (Sanne Raymaekers)
- worker: Prefix https always (sanne)
- cloudapi/v1: Move depsolving to workers (sanne)
- cloudapi/v2: fix newV2Server() call in test (Achilleas Koutsou)
- templates: Name service ports (sanne)
- SPEC: Exclude `armv7hl` architecture (Tomas Hozza)
- distro/rhel90 -> distro/rhel90beta: rename package (Achilleas Koutsou)
- distro/rhel90: rename to rhel-90-beta and alias base name (Achilleas Koutsou)
- spec: Split dnf-json into a subpackage (sanne)
- cloudapi/v2: Use worker to depsolve (Ondřej Budai)
- worker: Add a depsolve job type (Tom Gundersen)
- packit: Push downstream instead of creating PR (Simon Steinbeiss)
- templates: Name services after endpoints (sanne)
- worker: Make BasePath configurable (sanne)
- cloudapi/v2: Listen on /api/image-builder-composer/v2 (sanne)
- test/ostree: remove --ip-range from podman network (Achilleas Koutsou)
- RHEL-8.6: add support for official EC2 SAP image (Tomas Hozza)
- tools/provision: set up nightly repos for RHEL 8.6 (Achilleas Koutsou)
- test/cases: add support for RHEL 8.6 to test scripts (Achilleas Koutsou)
- schutzbot: pin osbuild to current main for 8.6 (Achilleas Koutsou)
- schutzbot: update terraform sha (Achilleas Koutsou)
- news: add entry about RHEL 8.6 (Achilleas Koutsou)
- test: add RHEL 8.6 test manifests (Achilleas Koutsou)
- test: add rpmrepo snapshots for RHEL 8.6 (Achilleas Koutsou)
- ci: run all tests on RHEL 8.6 (Achilleas Koutsou)
- test/data/repositories: add test repos for rhel-86 (Achilleas Koutsou)
- distro/rhel85: remove rhel86 alias (Achilleas Koutsou)
- distro/rhel86: copy all definitions from rhel85 (Achilleas Koutsou)
- cloudapi/v2: Configurable aws bucket (sanne)
- cloudapi/v2: Replace upload types with image types (sanne)
- Tests/RHEL-9.0: add EC2 SAP image test (Tomas Hozza)
- Tests/RHEL-9.0: add repos needed for EC2 SAP image tests (Tomas Hozza)
- RHEL-9.0: add EC2 SAP image definition. (Tomas Hozza)
- Tests/RHEL-9.0: add EC2 and EC2 HA image tests (Tomas Hozza)
- Tests/RHEL-9.0: add repos needed for EC2 and EC2 HA image tests (Tomas Hozza)
- Image tests: skip rpm-ostree-1-autovar.conf tmpfiles.d config on Fedora (Tomas Hozza)
- composer: Don't dump sensitive fields from config (sanne)
- tests: Update image_tests (Jakub Rusz)
- templates: Duplicate value in composer config (sanne)
- templates: Port names should be less than 15 characters (sanne)
- templates: Make sure ports are unquoted (sanne)
- cloudapi/v1: Return status created in compose handler (sanne)
- worker: Use Recover middleware to handle panics (Diaa Sami)
- worker: Improve logging (Diaa Sami)
- Regenerate affected image test cases (Tomas Hozza)
- generate-all-test-cases: allow specifying additional DNF repos (Tomas Hozza)
- image-info: ensure that directory is analysed as read-only (Tomas Hozza)
- tests: enable koji.sh test on RHEL-9 (Jakub Rusz)
- tests/ci: enable vmware.sh and cross-distro.sh on rhel-9 (Jakub Rusz)
- README: Add a link to our developer guide (Simon Steinbeiss)
- templates: Composer OSD template (sanne)
- internal/rpmmd: log repository files loaded during composer startup (Martin Sehnoutka)
- dnf-json: expire metadata by default (Tom Gundersen)
- schutzbot: Clean up non-default storage accounts (sanne)
- main: IsNotExist() is no longer a valid check (Achilleas Koutsou)
- config: update NonExisting test to check for default (Achilleas Koutsou)
- config: don't fail LoadConfig if file doesn't exist (Achilleas Koutsou)
- Test: regenerate all image test cases (Tomas Hozza)
- Image tests: use RPMRepo with released RHEL-8.4 content (Tomas Hozza)
- image-info: fix undefined variable in analyse_directory() (Tomas Hozza)
- image-info: sort partitions list in the report. (Tomas Hozza)
- image-info: use subprocess_check_output() in read_selinux_ctx_mismatch() (Tomas Hozza)
- image-info: check not installed documentation (Tomas Hozza)
- image-info: read content of /etc/resolv.conf (Tomas Hozza)
- image-info: read sysctl.d config files from multiple paths (Tomas Hozza)
- image-info: read security limits config files from multiple paths (Tomas Hozza)
- image-info: read tmpfiles.d config files from multiple paths (Tomas Hozza)
- image-info: read systemd service unit drop-ins from multiple paths (Tomas Hozza)
- image-info: read cloud-init configs from multiple paths (Tomas Hozza)
- image-info: read systemd-logind configs from multiple paths (Tomas Hozza)
- image-info: read dracut configs from multiple paths (Tomas Hozza)
- image-info: read modprobe configs from multiple paths (Tomas Hozza)
- composer: More configuration of how composer is served (sanne)

* Sat Oct 02 2021 Packit Service <user-cont-team+packit-service@redhat.com> - 35-1
- 35 (Simon Steinbeiss)
- gitleaks: add allow list for test passwords and keys (Achilleas Koutsou)
- mockbuild: use download.devel of download.eng.bos (Ondřej Budai)
- ci: install ansible-core instead of ansible for EL9 (Ondřej Budai)
- dnf-json: disable zchunk (Ondřej Budai)
- composer: improve logging (Diaa Sami)
- cloudapi: Add extra logging & improve existing (Diaa Sami)
- cloudapi: use Logrus as default logger in Echo (Diaa Sami)
- logging: add logrus dependency (Diaa Sami)
- ci: don't run nightly pipeline on ga releases (Jakub Rusz)
- distro/rhel90: use qcow2 compat 1.1 for qcows (Ondřej Budai)
- tools: Push ubi container to quay.io/app-sre/composer (sanne)
- blueprints: change minsize from int to uint64 (Gianluca Zuccarelli)
- test/regression: Adapt to new rhel-84-ga runners (sanne)
- schutzbot: Also build container on branch pushes (sanne)
- schutzbot: pin osbuild to >=37 on all distros (Ondřej Budai)
- spec: bump osbuild depedendency to 37 (Ondřej Budai)
- distro/rhel85: set bootloader to none for edge (Christian Kellner)
- osbuild2: add bootloader option to ostree.config (Christian Kellner)
- osbuild2: small doc fix for ostree.config (Christian Kellner)
- build(deps): bump github.com/labstack/echo/v4 from 4.5.0 to 4.6.0 (dependabot[bot])
- build(deps): bump github.com/aws/aws-sdk-go from 1.40.46 to 1.40.49 (dependabot[bot])
- workers: Backwards compatible api.openshift.com spec compliance (sanne)
- Disable regression-composer-works-behind-satellite.sh, Refs #1834 (Alexander Todorov)
- test/ostree: use 8.4 when testing on 8.4 (Ondřej Budai)
- ci: add workaround for missing redhat.repo in EC2 (Ondřej Budai)
- schutzfile: remove rhel-8.3 (Ondřej Budai)
- test/koji: always build the latest RHEL (Ondřej Budai)
- mockbuild: use REPO_BUCKET when defining the base URL (Ondřej Budai)
- test: use hyphen in DISTRO_CODE instead of underscore (Ondřej Budai)
- test: move env variables into set-env-variables helper (Ondřej Budai)
- test/koji: remove the workaround for rhel-8 (Ondřej Budai)
- test/api: don't source os-release again (Ondřej Budai)
- test: use cdn repos for 8.3 and 8.4 (Ondřej Budai)
- mockbuild: reuse nightly repos from redhat.repo (Ondřej Budai)
- ci: assume subscribed machines (Ondřej Budai)
- terraform: update (Ondřej Budai)
- build(deps): bump github.com/Azure/azure-sdk-for-go (dependabot[bot])
- distribution: Use After=network.target instead of multi-user (Martin Sehnoutka)
- internal/common: introduce git revision and rpm version (Martin Sehnoutka)
- test/ostree: support weldr-client output structure (Achilleas Koutsou)
- test/data: update test manifests for RHEL 9.0 edge (Achilleas Koutsou)
- distro/rhel90: explicitly enable greenboot services for edge (Achilleas Koutsou)
- distro/rhel90: add gnome-kiosk to installer package set (Achilleas Koutsou)
- tools/provision: install community.general ansible collection (Achilleas Koutsou)
- test/ostree: remove debug callback from ansible calls (Achilleas Koutsou)
- test/ostree: install python3 instead of specific version (Achilleas Koutsou)
- distro/rhel90: remove unavailable packages from edge-installer (Achilleas Koutsou)
- ci: enable ostree tests on RHEL 9.0-beta (Achilleas Koutsou)
- NEWS: Drop title line (Simon Steinbeiss)
- cloudapi: use Recover middleware to handle panics (Diaa Sami)
- HACKING: fix container command (Gianluca Zuccarelli)
- containers: worker client base url protocol (Gianluca Zuccarelli)
- containers: update composer log level flag (Gianluca Zuccarelli)
- Regenerate relevant image test cases (Tomas Hozza)
- distro/rhel90: re-include nss-altfiles for edge (Christian Kellner)
- generate-test-cases: drop `--with-customizations` option (Tomas Hozza)
- format-request-map.json: remove redundant overrides (Tomas Hozza)
- generate-test-cases: don't leak "supported_arches" to compose request (Tomas Hozza)
- tools: improve deploy-openstack script (Diaa Sami)
- weldr: deleting an unknown source should return an error (Brian C. Lane)
- Update distro-arch-imagetype-map.json (Tomas Hozza)
- test: update image test case generation part of README (Tomas Hozza)
- generate-all-test-cases: add option to keep created workdir on runner (Tomas Hozza)
- generate-all-test-cases: report results when Runner finishes (Tomas Hozza)
- generate-all-test-cases: support using existing remote hosts (Tomas Hozza)
- generate-all-test-cases: remove '--keep-image-info' option (Tomas Hozza)
- generate-all-test-cases: move current generator method to 'qemu' command (Tomas Hozza)
- generate-all-test-cases: fix log level in multiprocessing processes (Tomas Hozza)
- generate-all-test-cases: don't use virtfs to copy data from/to the VM (Tomas Hozza)
- generate-all-test-cases: don't use paramiko for SSH (Tomas Hozza)
- generate-all-test-cases: use SSH keys instead of password for VMs (Tomas Hozza)
- generate-all-test-cases: don't use cloud-init to install RPMs (Tomas Hozza)
- generate-all-test-cases: fix generating of cloud-init cdrom on MacOS (Tomas Hozza)
- generate-all-test-cases: separate generic parts of BaseRunner (Tomas Hozza)
- build(deps): bump github.com/aws/aws-sdk-go from 1.40.43 to 1.40.46 (dependabot[bot])
- generate-test-cases: check `supported_arches` from format-request-map.json (Tomas Hozza)
- schutzbot: Update terraform sha (sanne)
- Drop RELEASING.md and point to dev guide (Simon Steinbeiss)
- build(deps): bump github.com/Azure/go-autorest/autorest (dependabot[bot])
- build(deps): bump github.com/aws/aws-sdk-go from 1.40.38 to 1.40.43 (dependabot[bot])
- build(deps): bump github.com/openshift-online/ocm-sdk-go (dependabot[bot])

* Wed Aug 11 2021 Ondřej Budai <ondrej@budai.cz> - 31-1
- New upstream release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 14 2021 Ondřej Budai <ondrej@budai.cz> - 30-1
- New upstream release

* Fri Mar 05 2021 Martin Sehnoutka <msehnout@redhat.com> - 29-1
- New upstream release

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 28-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Sat Feb 20 2021 Martin Sehnoutka <msehnout@redhat.com> - 28-1
- New upstream release

* Thu Feb 04 2021 Ondrej Budai <obudai@redhat.com> - 27-1
- New upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 17 2020 Ondrej Budai <obudai@redhat.com> - 26-2
- Fix the compatibility with a new golang-github-azure-storage-blob 0.12

* Thu Dec 17 2020 Ondrej Budai <obudai@redhat.com> - 26-1
- New upstream release

* Thu Nov 19 2020 Ondrej Budai <obudai@redhat.com> - 25-1
- New upstream release

* Thu Nov 12 2020 Ondrej Budai <obudai@redhat.com> - 24-1
- New upstream release

* Fri Nov 06 2020 Ondrej Budai <obudai@redhat.com> - 23-1
- New upstream release

* Fri Oct 16 2020 Ondrej Budai <obudai@redhat.com> - 22-1
- New upstream release

* Sun Aug 23 2020 Tom Gundersen <teg@jklm.no> - 20-1
- New upstream release

* Tue Aug 11 2020 Tom Gundersen <teg@jklm.no> - 19-1
- New upstream release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Ondrej Budai <obudai@redhat.com> - 18-1
- New upstream release

* Wed Jul 08 2020 Ondrej Budai <obudai@redhat.com> - 17-1
- New upstream release

* Mon Jun 29 2020 Ondrej Budai <obudai@redhat.com> - 16-1
- New upstream release

* Fri Jun 12 2020 Ondrej Budai <obudai@redhat.com> - 15-1
- New upstream release

* Thu Jun 04 2020 Ondrej Budai <obudai@redhat.com> - 14-1
- New upstream release

* Fri May 29 2020 Ondrej Budai <obudai@redhat.com> - 13-2
- Add missing osbuild-ostree dependency

* Thu May 28 2020 Ondrej Budai <obudai@redhat.com> - 13-1
- New upstream release

* Thu May 14 2020 Ondrej Budai <obudai@redhat.com> - 12-1
- New upstream release

* Wed Apr 29 2020 Ondrej Budai <obudai@redhat.com> - 11-1
- New upstream release

* Wed Apr 15 2020 Ondrej Budai <obudai@redhat.com> - 10-1
- New upstream release

* Wed Apr 01 2020 Ondrej Budai <obudai@redhat.com> - 9-1
- New upstream release

* Mon Mar 23 2020 Ondrej Budai <obudai@redhat.com> - 8-1
- Initial package (renamed from golang-github-osbuild-composer)
