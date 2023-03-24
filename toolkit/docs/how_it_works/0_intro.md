How The Build System Works
===
## Next: [Initial Prep](1_initial_prep.md)
## General Build Flow

This section is intended to give an overview of Mariner's build process and toolkit. The diagrams below follow conventions stated in the key.
```mermaid
---
title: Flowchart key
---
flowchart TD
input[/input or output/]
process[process]
decision{{decision}}
state([state])
```
<br/>

### High level RPM Flow
Mariner is an RPM based distro. A single package (or RPM) is built using a combination of sources and a spec file. A signature file is used to verify the sources' hashes. 

```mermaid
flowchart LR
    spec[/Spec/]
    localSourceTar[/Local Sources if present/]
    sigFile[/Signature file/]
    remoteSourceTar[/Remote Source/]
    patches[/Patches/]
    pack[Pack SRPM]
    srpm[/SRPM/]
    buildRPM[Build RPM]
    rpm[/RPM/]

    spec --> pack
    localSourceTar --> pack
    remoteSourceTar --> pack
    patches --> pack
    sigFile --> pack
    pack -->srpm 
    srpm --> buildRPM
    buildRPM --> rpm
```
</br>

### High level Build Flow
 The build process can be split into three components: tooling, package generation, and image generation. When building, Makefile options can be used to build Mariner entirely from end to end or to download prebuilt artifacts.


```mermaid
flowchart LR
    buildTC[Build toolchain from scratch]
    pullTC[Pull toolchain from remote]
    tcRPMS[/Toolchain RPMs/]
    buildRPMS[Build RPMs from scratch]
    pullRPMS[Pull RPMs from remote]
    rpms[/RPMs/]
    buildImage[Build Image from scratch]
    image[(Image: Container vhd vhdx iso)]

    buildTC --> tcRPMS
    pullTC --> tcRPMS
    tcRPMS --> buildRPMS
    buildRPMS --> rpms
    pullRPMS --> rpms
    rpms --> buildImage
    buildImage --> image

```

</br>

### Tools
The tooling consists of a set of `Makefiles`, various go programs, a bootstrapping environment running in `Docker`, and a `chroot` environment to build in. These are discussed [here](1_initial_prep.md). The toolkit is able to re-build all of the tools from source if desired.

```mermaid
flowchart TD
    start(["Start (make toolchain)"])
    done([Done])
    style done fill:#597D35,stroke:#333,stroke-width:4px
    style start fill:#0074D9,stroke:#333,stroke-width:4px
 %% TC nodes
    tcManifests[/Local Toolchain Manifests/]
    tcRebuild{{"Rebuild Toolchain? (REBUILD_TOOLCHAIN=y/n)"}}
    toolchainChoice{{"Toolchain archive available? (TOOLCHAIN_ARCHIVE=...)"}}
    tcPopulated([Toolchain populated])
    tcRPMs[(Toolchain RPMs)]
    tcArchiveOld[/Old Toolchain archive/]
    tcArchiveNew[/Toolchain archive/]
    pullTC([Local Toolchain Archive available])
    hydrateTC[Extract Toolchain RPMs]
    buildRawTC[Build Raw Toolchain]
    localSpecs[/Local SPECS/]
    bsRPMS[/Bootstrap Toolchain RPMs/]
    buildTC[Build Toolchain proper]
    pullRemote[Download remote RPMs]

%% TC flow
    start --> tcRebuild
    tcRebuild -->|yes| buildRawTC
    tcManifests --> toolchainChoice
    tcRebuild -->|no|toolchainChoice
    toolchainChoice -->|no| pullRemote
    toolchainChoice -->|yes| pullTC 
    pullRemote --> tcRPMs
    pullTC -->hydrateTC
    tcArchiveOld --> pullTC
    hydrateTC --> tcRPMs

    
    localSpecs --> buildRawTC
    buildRawTC --> bsRPMS
    bsRPMS --> buildTC
    localSpecs --> buildTC
    buildTC --> tcArchiveNew
    tcArchiveNew --> pullTC
    tcRPMs-->tcPopulated
    tcPopulated --> done
```

<br/>

### Package Generation
Package generation is discussed in detail [here](2_local_packages.md) and [here](3_package_building.md). At a high level, the build system scans the local project directory for `*.spec` files which define the local packages. It then packages these files into `*.src.rpm` files by either including local source files, or downloading matching ones from a source server. The `*.src.rpm` files required for the currently selected configuration are then built in the correct order to resolve all dependencies. The build system will automatically download any build dependencies not satisfied by the local packages.

```mermaid
flowchart TD
    start(["Start (make build-packages)"])
    style done fill:#597D35,stroke:#333,stroke-width:4px
    style start fill:#0074D9,stroke:#333,stroke-width:4px
    style error fill:#8B0000,stroke:#333,stroke-width:4px
%% Rpm nodes
    tcPopulated([Toolchain populated])
    localSpecs[/Local SPECS/]
    buildPackage{{"Make package? (REBUILD_PACKAGES=y/n)"}}
    remoteRPM{{Pull remote RPM?}}
    tcRPMs[(Toolchain RPMs)]
    createChroot[Create Chroot]
    chroot[/chroot/]
    iSRPMs[/Intermediate SRPMs/]
    parse["Parse Specs (specreader) "]
    specjson[/Spec json/]
    buildGraph[" Build Graph (grapher) "]
    depGraph[/"Dependency Graph (graph.dot)"/]
    cacheGraph[/"Cached Graph (cached_graph.dot)"/]
    
    packSRPM[Pack SRPM]
    beginBuild[Begin Build]
    pkgFetcher[Package fetcher]
    rpmCache[(RPM cache)]
    remoteRepo[(remote repo)]
    missingDep[/RPMs to fill Missing Dependencies/]
    outRPMS[(RPMs built locally)]
    error([error])
    done([Done])

%% Rpms flow
    start --> tcPopulated
    tcPopulated --> buildPackage
    buildPackage -->|yes|packSRPM
    remoteRPM -->|no|beginBuild
    beginBuild --> packSRPM
    localSpecs-->packSRPM
    packSRPM-->iSRPMs
    iSRPMs--> parse
    parse--> specjson
    specjson --> buildGraph
    buildGraph--> depGraph
    depGraph --> pkgFetcher
    remoteRepo-->missingDep
    missingDep-->pkgFetcher
    pkgFetcher-->rpmCache
    pkgFetcher-->cacheGraph

    createChroot-->chroot
    tcRPMs-->createChroot
    chroot-...->packSRPM
    chroot-...->parse
    chroot-...->pkgFetcher
    
    rpmCache-->getDeps
    tcRPMs-->getDeps
    chroot-...->worker
    builtRPMs-->outRPMS
    outRPMS-->getDeps
    doneBuild-->|yes|done
    leafNodesAvail-->|no|error
    cacheGraph-->currentGraph

%% Subgraph for scheduler
    subgraph sched ["Scheduler tool (scheduler)"]
    currentGraph[/Current Graph/]
    trim[Remove unneeded branches from graph]
    doneBuild{{Done building all required nodes?}} 
    leafNodesAvail{{Leaf nodes available?}}
    worker[Worker to build rpm]
    builtRPMs[/Built RPMs/]
    updateDeps[Update Dependency]
    getDeps[Get dependencies]

    currentGraph-->trim
    trim-->doneBuild
    doneBuild-->|no|leafNodesAvail
    leafNodesAvail-->|yes|worker

    builtRPMs-->updateDeps
    updateDeps-->currentGraph
    getDeps-->worker
    worker-->builtRPMs
    end
%% end of scheduler
```

<br/>

### Image Generation
Image generation is discussed in detail [here](4_image_generation.md). The image generation step creates a new filesystem, and then installs packages into it based on the currently selected configuration file. These packages can be either the locally built packages, or packages pulled from one or more package servers. Once the filesystem is composited any additional changes listed in the config file are made, the filesystem is then packaged into the requested format (`vhd`, `vhdx`, `ISO`, etc).

```mermaid
flowchart TD
    start(["Start (make image)"])
    done([Done])
    style done fill:#597D35,stroke:#333,stroke-width:4px
    style start fill:#0074D9,stroke:#333,stroke-width:4px
%% Image nodes
    imageConfig[/Image config or json/]
    raw[/Raw image or file system/]
    roast[roast]
    initrd[/initrd/]
    iso[/"iso (imager tool, pkgs, config files)"/]
    image[/image/]
    pkgFetcher[Package fetcher]
    rpmCache[(local RPMs)]
    remoteRepo[(remote repo)]
    missingDep[/RPMs to fill Missing Dependencies/]
    imager["Image tool (imager)"]
    isoBuild{{iso installer or offline build?}}
    isoBuilder[iso maker]

%% Image flow
    
    start-->pkgFetcher
    imageConfig-->pkgFetcher
    rpmCache-->pkgFetcher
    remoteRepo-->missingDep
    missingDep-->pkgFetcher
    
    pkgFetcher-->isoBuild
    isoBuild-->|iso installer|isoBuilder
    initrd-->isoBuilder
    isoBuilder-->iso
    iso-->done
    isoBuild-->|offline|imager
    imager-->raw
    raw-->roast
    roast-->image

    image-->done
    
```

## In Depth Explanations
### [1. Initial Prep](1_initial_prep.md)
- Makefiles, Go Tooling, Toolchain, Chroots
### [2. Local Packages](2_local_packages.md)
- Local Spec Files, Creating Local SRPMs
### [3. Package Building](3_package_building.md)
- Dependency Graphing, Downloading Dependencies, Building Packages
### [4. Image Generation](4_image_generation.md)
- Composing Images, Creating ISOs
### [5. Misc](5_misc.md)
- Chroots