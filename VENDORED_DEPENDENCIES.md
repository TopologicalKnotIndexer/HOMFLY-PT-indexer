# Vendored dependencies

This repository is self-contained. Former Git submodules are tracked as regular files at the audited commits below. Their original directory layout is preserved so runtime imports and entry points remain compatible.

| Path | Source | Pinned commit |
| --- | --- | --- |
| `src/HOMFLY-PT-solver` | [HOMFLY-PT-solver](https://github.com/TopologicalKnotIndexer/HOMFLY-PT-solver) | `c801d5dbed2edf57f1c08ed22976bd78cac2b900` |
| `src/HOMFLY-PT-solver/src/x86_64-sage-minimal` | [x86_64-sage-minimal](https://github.com/TopologicalKnotIndexer/x86_64-sage-minimal) | `ebc8eeaeda03e91425ef0d0cc11c3a7c977f0104` |
| `src/HOMFLY-PT-solver/src/pd_code_de_r1_k8` | [pd_code_de_r1_k8](https://github.com/TopologicalKnotIndexer/pd_code_de_r1_k8) | `395d0b272a06e90c28db90a38803412e8eb9edb5` |
| `src/HOMFLY-PT-solver/src/pd_code_input_sanity` | [pd_code_input_sanity](https://github.com/TopologicalKnotIndexer/pd_code_input_sanity) | `9f0233a3b48043a9e164d98ad6cee644cc792a28` |
| `src/HOMFLY-PT-polynomial-list` | [HOMFLY-PT-polynomial-list](https://github.com/TopologicalKnotIndexer/HOMFLY-PT-polynomial-list) | `cf8ca873e165169405565dd7b1b7b8577c49162f` |
| `src/slow_dict_reader` | [slow_dict_reader](https://github.com/TopologicalKnotIndexer/slow_dict_reader) | `85e9af7681b8a9b569d3ffae2c68e8d861f89c54` |
| `src/slow_dict_reader/src/knotname-reg` | [knotname-reg](https://github.com/TopologicalKnotIndexer/knotname-reg) | `fce68fc3d45a8f3d4e6da81efc07b069ed8179ad` |

## Updating a vendored dependency

Replace the listed tree from a reviewed source commit, update this table, and run this repository's complete validation suite. Do not reintroduce Git submodules; every organization project must remain independently cloneable.
