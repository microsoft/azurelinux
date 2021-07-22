FROM cblmariner.azurecr.io/base/core:1.0
RUN tdnf install -y dnf
RUN mkdir -p /abidiff/rpms
COPY ./mariner-container-abidiff.sh /abidiff/
ENTRYPOINT ["./abidiff/mariner-container-abidiff.sh", "/abidiff/rpms"]
