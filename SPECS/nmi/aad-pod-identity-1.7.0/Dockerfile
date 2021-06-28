ARG BASEIMAGE=gcr.io/distroless/static:nonroot

FROM golang:1.15 AS builder
WORKDIR /go/src/github.com/Azure/aad-pod-identity
ADD . .
RUN go mod download
ARG IMAGE_VERSION
RUN make build

FROM us.gcr.io/k8s-artifacts-prod/build-image/debian-iptables-amd64:v12.1.2 AS nmi
RUN clean-install ca-certificates
COPY --from=builder /go/src/github.com/Azure/aad-pod-identity/bin/aad-pod-identity/nmi /bin/
RUN useradd -u 10001 nonroot
USER nonroot
ENTRYPOINT ["nmi"]

FROM $BASEIMAGE AS mic
COPY --from=builder /go/src/github.com/Azure/aad-pod-identity/bin/aad-pod-identity/mic /bin/
ENTRYPOINT ["mic"]

FROM $BASEIMAGE AS demo
COPY --from=builder /go/src/github.com/Azure/aad-pod-identity/bin/aad-pod-identity/demo /bin/
ENTRYPOINT ["demo"]

FROM $BASEIMAGE AS identityvalidator
COPY --from=builder /go/src/github.com/Azure/aad-pod-identity/bin/aad-pod-identity/identityvalidator /bin/
ENTRYPOINT ["identityvalidator"]
