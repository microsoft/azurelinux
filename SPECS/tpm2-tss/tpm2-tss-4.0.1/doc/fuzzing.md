# Fuzzing

Fuzz tests use [libFuzzer](http://llvm.org/docs/LibFuzzer.html) to test the SAPI
`_Prepare` and `_Complete` functions.

Building fuzz tests can be enabled using the `--with-fuzzing=` option. For which
there are two possible values.

- [libfuzzer](#libfuzzer)
- [ossfuzz](#oss-fuzz)

## libFuzzer

libFuzzer tests can be built natively or using the docker `fuzzing` target.

### Natively

Build the fuzz tests by setting `--with-fuzzing=libfuzzer` and statically
linking to the fuzzing TCTI.

```console
export GEN_FUZZ=1

./bootstrap
./configure \
  CC=clang \
  CXX=clang++ \
  --enable-debug \
  --with-fuzzing=libfuzzer \
  --enable-tcti-fuzzing \
  --enable-tcti-device=no \
  --enable-tcti-mssim=no \
  --with-maxloglevel=none \
  --disable-shared

make -j $(nproc) check
```

Run the fuzz tests by executing any binary ending in `.fuzz` in `test/fuzz/`.

```console
./test/fuzz/Tss2_Sys_ZGen_2Phase_Prepare.fuzz
```

### Docker

Build the fuzz targets and check that they work by building the `fuzzing` docker
target.

```console
docker build --target fuzzing -t tpm2-tss:fuzzing .
```

Run a fuzz target and mount a directory as a volume into the container where it
should store its findings should it produce any.

```console
docker run --rm -ti tpm2-tss:fuzzing \
   -v "${PWD}/findings_dir":/artifacts \
   ./test/fuzz/Tss2_Sys_PolicyPhysicalPresence_Prepare.fuzz \
  -artifact_prefix=/artifacts
```

## OSS Fuzz

OSS fuzz integration can be found under the
[tpm2-tss](https://github.com/google/oss-fuzz/tree/master/projects/tpm2-tss)
project in OSS Fuzz.

The `Dockerfile` there builds the dependencies. `build.sh` Runs the compilation
as seen under the `fuzzing` target of the `Dockerfile` in this repo, only
`--with-fuzzing=ossfuzz`.

## Hacking

Currently only fuzz targets for the System API have been implemented.

### TCTI

The fuzzing TCTI is used as a temporary storage location for the `Data` and
`Size` arguments of `LLVMFuzzerTestOneInput`.

For `_Complete` calls the TCTI uses `Data` and `Size` as the response buffer and
response size for `TSS2_TCTI_RECEIVE`.

### SAPI

Fuzz tests are generated via `script/gen_fuzz.py`.

Setting `GEN_FUZZ=1` when running `bootstrap` will run `script/gen_fuzz.py`.

```console
GEN_FUZZ=1 ./bootstrap
```

`script/gen_fuzz.py` reads the SAPI header file and generates a fuzz target for
each `_Prepare` and `_Complete` call using similar templates.

For `_Prepare` calls the `fuzz_fill` function in the fuzzing TCTI will fill each
TPM2 structure used can copy from `LLVMFuzzerTestOneInput`'s `Data` into it.
