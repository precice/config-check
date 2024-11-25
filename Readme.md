# Errors to detect

- The aim of this project is not to find syntactic and semantic errors, but only logical ones.
We execute (the equivalent of) `precice-tools check` beforehand, so that we can be sure that the config file is at least
valid.
- Warning: `<data: />` is never used
- Info (maybe only on log level debug): At least two participants to make sense (only valid use case we could think of: one participant using PreCICE's implicit coupling functions/mappings etc. on multiple meshes, so they don't have to implement implicit coupling themselves - so no warning if there are multiple meshes?)
- Socket-Edges must be in same direction as data flow? Is this an error, because `precice-tools check` does not complain.
- To be defined: Config checker and config visualizer currently do not care about existence of provide-mesh and receive-mesh
- More valid configs in the integration tests: https://github.com/precice/precice/tree/develop/tests . Test them and check if they are actually valid.
