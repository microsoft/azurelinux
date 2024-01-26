# How The Build System Works

## Next: [Initial Prep](1_initial_prep.md)

## General Build Flow

This section is intended to give an overview of Mariner's build process and toolkit. The diagrams below follow conventions stated in the key.

```mermaid
---
title: Flowchart key
---
flowchart TD
    %% style definitions
    classDef io fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;
    classDef process fill:#B05E2F,stroke:#333,stroke-width:2px,color:#fff;
    classDef decision fill:#51344D,stroke:#333,stroke-width:2px,color:#fff;
    classDef goodState fill:#566E40,stroke:#333,stroke-width:2px,color:#fff;
    classDef badState fill:#BC4B51,stroke:#333,stroke-width:2px,color:#fff;
    classDef collection fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;

    %% node definitions
    input[/input or output/]:::io
    process[process]:::process
    decision{{decision}}:::decision
    goodstate([good state]):::goodState
    badstate(["error state"]):::badState
    collection[(object collection)]:::collection
```

### High-level RPM flow

Mariner is an RPM based distro. A single package (or RPM) is built using a combination of sources and a spec file. A signature file is used to verify the sources' hashes.

```mermaid
flowchart LR
    %% style definitions
    classDef io fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;
    classDef process fill:#B05E2F,stroke:#333,stroke-width:2px,color:#fff;
    classDef decision fill:#51344D,stroke:#333,stroke-width:2px,color:#fff;
    classDef goodState fill:#566E40,stroke:#333,stroke-width:2px,color:#fff;
    classDef badState fill:#BC4B51,stroke:#333,stroke-width:2px,color:#fff;
    classDef collection fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;

    %% nodes
    spec[/Spec/]:::io
    localSourceTar[/Local sources if present/]:::io
    sigFile[/Signature file/]:::io
    remoteSourceTar[/Remote source/]:::io
    patches[/Patches/]:::io
    pack[Pack SRPM]:::process
    srpm[/SRPM/]:::io
    buildRPM[Build RPM]:::process
    rpm[/RPM/]:::io

    %% node flow
    spec --> pack
    localSourceTar --> pack
    remoteSourceTar --> pack
    patches --> pack
    sigFile --> pack
    pack --> srpm
    srpm --> buildRPM
    buildRPM --> rpm
```

### High-level build flow

 The build process can be split into three components: tooling, package generation, and image generation. When building, `make` options can be used to build Mariner from end to end or to download prebuilt artifacts.

```mermaid
flowchart LR
    %% style definitions
    classDef io fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;
    classDef process fill:#B05E2F,stroke:#333,stroke-width:2px,color:#fff;
    classDef decision fill:#51344D,stroke:#333,stroke-width:2px,color:#fff;
    classDef goodState fill:#566E40,stroke:#333,stroke-width:2px,color:#fff;
    classDef badState fill:#BC4B51,stroke:#333,stroke-width:2px,color:#fff;
    classDef collection fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;

    %% nodes
    buildTC[Build toolchain from scratch]:::process
    pullTC[Pull toolchain from remote]:::process
    tcRPMS[/Toolchain RPMs/]:::io
    buildRPMS[Build RPMs from scratch]:::process
    pullRPMS[Pull RPMs from remote]:::process
    rpms[/RPMs/]:::io
    buildImage[Build image from scratch]:::process
    image[(Image: Container vhd vhdx iso)]:::collection

    %% node flow
    buildTC --> tcRPMS
    pullTC --> tcRPMS
    tcRPMS --> buildRPMS
    buildRPMS --> rpms
    pullRPMS --> rpms
    rpms --> buildImage
    buildImage --> image

```

### Tools

The tooling consists of a set of makefiles, various Go programs, a bootstrapping environment running in `Docker`, and a `chroot` environment to build in. These are discussed [here](1_initial_prep.md). The toolkit is able to re-build all of the tools from source if desired.

```mermaid
flowchart TD

    %% style definitions
    classDef io fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;
    classDef process fill:#B05E2F,stroke:#333,stroke-width:2px,color:#fff;
    classDef decision fill:#51344D,stroke:#333,stroke-width:2px,color:#fff;
    classDef goodState fill:#566E40,stroke:#333,stroke-width:2px,color:#fff;
    classDef badState fill:#BC4B51,stroke:#333,stroke-width:2px,color:#fff;
    classDef collection fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;

    %% state nodes
    start(["Start (make toolchain)"]):::goodState
    done([Done]):::goodState
    %% error([Error]):::badState

    %% TC nodes
    tcManifests[/Local Toolchain Manifests/]:::io
    tcRebuild{{"Rebuild Toolchain? (REBUILD_TOOLCHAIN=y/n)"}}:::decision
    toolchainChoice{{"Toolchain archive available? (TOOLCHAIN_ARCHIVE=...)"}}:::decision
    tcPopulated([Toolchain populated]):::goodState
    tcRPMs[(Toolchain RPMs)]:::collection
    tcArchiveOld[/Old Toolchain archive/]:::io
    tcArchiveNew[/Toolchain archive/]:::io
    pullTC([Local toolchain archive available]):::goodState
    hydrateTC[Extract Toolchain RPMs]:::process
    buildRawTC[Build raw toolchain]:::process
    sources[/Sources/]:::io
    localSpecs[/Local SPECS/]:::io
    bsRPMS[/Bootstraped environment/]:::io
    buildTC[Build toolchain proper]:::process
    pullRemote[Download remote RPMs]:::process

    %% TC flow
    start --> tcRebuild
    tcRebuild -->|yes| buildRawTC
    sources --> buildRawTC
    tcManifests --> hydrateTC
    tcManifests --> pullRemote
    tcManifests --> buildTC
    tcRebuild -->|no| toolchainChoice
    toolchainChoice -->|no| pullRemote
    toolchainChoice -->|yes| pullTC
    pullRemote --> tcRPMs
    pullTC --> hydrateTC
    tcArchiveOld --> pullTC
    hydrateTC --> tcRPMs
    buildRawTC --> bsRPMS
    bsRPMS --> buildTC
    sources --> buildTC
    localSpecs --> buildTC
    buildTC --> tcArchiveNew
    tcArchiveNew --> pullTC
    tcRPMs --> tcPopulated
    tcPopulated --> done
```

### Package Generation

Package generation is discussed in detail [here](2_local_packages.md) and [here](3_package_building.md). At a high level, the build system scans the local project directory for `*.spec` files which define the local packages. It then packages these files into `*.src.rpm` files by either including local source files, or downloading matching ones from a source server. The `*.src.rpm` files required for the currently selected configuration are then built in the correct order to resolve all dependencies. The build system will automatically download any build dependencies not satisfied by the local packages.

```mermaid
flowchart TD

    %% style definitions
    classDef io fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;
    classDef process fill:#B05E2F,stroke:#333,stroke-width:2px,color:#fff;
    classDef decision fill:#51344D,stroke:#333,stroke-width:2px,color:#fff;
    classDef goodState fill:#566E40,stroke:#333,stroke-width:2px,color:#fff;
    classDef badState fill:#BC4B51,stroke:#333,stroke-width:2px,color:#fff;
    classDef collection fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;

    %% state nodes
    start(["Start (make build-packages)"]):::goodState
    done([Done]):::goodState
    error([Error]):::badState

    %% Rpm nodes
    tcPopulated([Toolchain populated]):::goodState
    localSpecs[/Local SPECS/]:::io
    tcRPMs[(Toolchain RPMs)]:::collection
    createChroot[Create chroot]:::process
    chroot[/chroot/]:::io
    iSRPMs[/Intermediate SRPMs/]:::io
    parse["Parse specs (specreader)"]:::process
    specjson[/"Dependency data (specs.json)"/]:::io
    buildGraph[" Build graph (grapher) "]:::process
    depGraph[/"Dependency graph (graph.dot)"/]:::io
    cacheGraph[/"Cached graph (cached_graph.dot)"/]:::io
    sources[/Sources/]:::io
    packSRPM[Pack SRPM]:::process
    pkgFetcher["Package fetcher (graphpkgfetcher)"]:::process
    rpmCache[(RPM cache)]:::collection
    remoteRepo[(Remote repo)]:::collection
    missingDep[/RPMs to fill missing dependencies/]:::io
    outRPMS[(RPMs built locally)]:::io
    buildRPMs[Build RPMs]:::process

    %% Rpms flow
    start --> tcPopulated
    tcPopulated & sources & localSpecs --> packSRPM
    packSRPM --> iSRPMs
    iSRPMs --> parse
    parse --> specjson
    specjson --> buildGraph
    buildGraph --> depGraph
    remoteRepo --> missingDep
    depGraph & missingDep --> pkgFetcher
    pkgFetcher --> rpmCache & cacheGraph
    tcRPMs --> createChroot
    createChroot --> chroot
    chroot -...-> packSRPM & parse & pkgFetcher & worker
    builtRPMs ----> outRPMS
    doneBuild -->|yes| done
    leafNodesAvail -->|no| error
    cacheGraph --> currentGraph
    tcRPMs --> getDeps
    rpmCache ----> getDeps
    outRPMS --> getDeps

    %% Subgraph for scheduler
        %% scheduler nodes
        subgraph sched ["Scheduler tool (scheduler)"]
        currentGraph[/Current graph/]:::io
        trim[Remove unneeded branches from graph]:::process
        doneBuild{{Done building all required nodes?}}:::decision
        leafNodesAvail{{Leaf nodes available?}}:::decision
        worker[Schedule a chroot worker to build the SRPM]:::process
        builtRPMs[/Built RPMs/]:::io
        updateDeps[Scan new RPMs and update graph dependencies]:::process
        getDeps[Add dependencies to worker]:::process

        %% scheduler flow
        currentGraph --> trim
        trim --> doneBuild
        doneBuild -->|no| leafNodesAvail
        leafNodesAvail -->|yes| worker
        updateDeps --> currentGraph
        worker --> getDeps
        getDeps --> buildRPMs
        buildRPMs --> builtRPMs
        builtRPMs --> updateDeps
        end
    %% end of scheduler

```

### Image Generation

Image generation is discussed in detail [here](4_image_generation.md). The image generation step creates a new filesystem, and then installs packages into it based on the currently selected configuration file. These packages can be either the locally built packages, or packages pulled from one or more package servers. Once the filesystem is composited any additional changes listed in the config file are made, the filesystem is then packaged into the requested format (`vhd`, `vhdx`, `ISO`, etc).

```mermaid
flowchart TD
    %% style definitions
    classDef io fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;
    classDef process fill:#B05E2F,stroke:#333,stroke-width:2px,color:#fff;
    classDef decision fill:#51344D,stroke:#333,stroke-width:2px,color:#fff;
    classDef goodState fill:#566E40,stroke:#333,stroke-width:2px,color:#fff;
    classDef badState fill:#BC4B51,stroke:#333,stroke-width:2px,color:#fff;
    classDef collection fill:#247BA0,stroke:#333,stroke-width:2px,color:#fff;

    %% state nodes
    start(["Start (make image / make ISO)"]):::goodState
    done([Done]):::goodState
    %% error([Error]):::badState

    %% Image nodes
    imageConfig[/Image config.json/]:::io
    raw[/Raw image or file system/]:::io
    roast["Image format converter (roast)"]:::process
    initrd[/initrd/]:::io
    iso[/"ISO (imager tool, pkgs, config files)"/]:::io
    image[/image/]:::io
    pkgFetcher["Package fetcher (imagepkgfetcher)"]:::process
    rpmCache[(Local RPMs)]:::collection
    remoteRepo[(Remote repo)]:::collection
    missingDep[/RPMs to fill Missing Dependencies/]:::io
    imager["Image tool (imager)"]:::process
    isoBuild{{ISO installer or offline build?}}:::decision
    isoBuilder["ISO maker (isomaker)"]:::process
    %% Image flow
    start --> pkgFetcher
    imageConfig -->pkgFetcher
    rpmCache --> pkgFetcher
    remoteRepo --> missingDep
    missingDep --> pkgFetcher
    pkgFetcher --> isoBuild
    isoBuild -->|iso installer| isoBuilder
    initrd --> isoBuilder
    isoBuilder --> iso
    iso --> done
    isoBuild -->|offline| imager
    imager --> raw
    raw --> roast
    roast --> image
    image --> done

```

## In Depth Explanations

### [1. Initial Prep](1_initial_prep.md)

* Makefiles, Go Tooling, Toolchain, Chroots

### [2. Local Packages](2_local_packages.md)

* Local Spec Files, Creating Local SRPMs

### [3. Package Building](3_package_building.md)

* Dependency Graphing, Downloading Dependencies, Building Packages

### [4. Image Generation](4_image_generation.md)

* Composing Images, Creating ISOs

### [5. Misc](5_misc.md)

- Chroots

### [6. Logs](6_logs.md)

- Understanding common build logs errors
