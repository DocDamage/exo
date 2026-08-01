version "v0.1.0"

build dev {
    entry "./src/main.sx"
    flags "--alt=clang"
    output "./build/bin/exo-dev"
}

build release {
    entry "./src/main.sx"
    flags "--alt=clang --release"
    output "./build/bin/exo"
}

build test {
    entry "./src/main.sx"
    flags "--alt=clang --test"
    output "./build/bin/exo-tests"
}

build hello {
    entry "./examples/hello_world/main.sx"
    flags "--alt=clang"
    output "./build/bin/exo-hello"
}

build snow {
    entry "./examples/snow/main.sx"
    flags "--alt=clang"
    output "./build/bin/exo-snow"
}
