fn main() {
    println!("cargo:rerun-if-changed=build.rs");

    pkg_config::Config::new()
        .cargo_metadata(true)
        .print_system_libs(false)
        .probe("zlib")
        .unwrap();
}
