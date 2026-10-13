# C extension boundary

Keep C code limited to profiled hotspots. Establish a Python reference implementation first, then:
1. define the input/output contract and memory ownership
2. add a correctness test corpus
3. compile with debug symbols and sanitizers during development
4. compare outputs against the reference implementation
5. benchmark end-to-end impact, not only microbenchmarks
6. keep a portable fallback where practical

Do not introduce unsafe native code before profiling demonstrates a meaningful bottleneck.
