#	Multi-stage docker build file (see https://docs.docker.com/develop/develop-images/multistage-build/)
#	Use a Microsoft image with .NET core runtime (https://hub.docker.com/r/microsoft/dotnet/tags/)
FROM microsoft/dotnet:2.2-sdk AS build

WORKDIR /src

#	Copy source code into the source folder
COPY MyApiSolution .

#	Publish the app into the app folder
RUN dotnet publish MyApi -c release -o app

###########################################################
#	Final container image
#	Use a Microsoft image with .NET core runtime (https://hub.docker.com/r/microsoft/dotnet/tags/)
FROM microsoft/dotnet:2.2-aspnetcore-runtime AS final

#	Set the working directory to /work
WORKDIR /work

#	Copy package
COPY --from=build /src/MyApi/app .

# Make port 80 available to the world outside this container

EXPOSE 80

#	Run console app
CMD ["dotnet", "MyApi.dll"]