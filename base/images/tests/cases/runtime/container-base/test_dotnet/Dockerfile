ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y dotnet-sdk-10.0 curl && dnf clean all
WORKDIR /src
COPY webapp/ ./webapp/
COPY restclient/ ./restclient/
RUN dotnet publish webapp -c Release -o /app/webapp \
 && dotnet publish restclient -c Release -o /app/restclient
EXPOSE 8080
