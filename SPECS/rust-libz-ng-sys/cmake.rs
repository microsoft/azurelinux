fn main() {
    println!("cargo:rustc-link-lib=dylib=z-ng");
    println!("cargo:rustc-cfg=zng");
}
