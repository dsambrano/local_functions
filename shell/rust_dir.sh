#!/usr/bin/env bash

# https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/book/first-edition/getting-started.html


mkdir -p $1/src
echo '
fn main() {
    println!("Hello, world!");
}
' >> $1/src/main.rs

TOML='
[package]

name = "hello_world"
version = "0.0.1"
authors = [ "Your name <you@example.com>" ]
'
echo TOML >> Cargo.toml

