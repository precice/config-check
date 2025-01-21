# Architecture

## Rules and Violations

_This part of the documentation details the design of the software. See `Rules.md` for a list of implemented Rules._

This program is designed to collect all messages, and then print them out at once. This allows for multiple features over directly printing messages upon finding something, including:
- easier testing
- potential use as a library
- merging multiple related messages into one

The actual logic for checking for Violations is implemented in Rules. A Rule is a class with a `check` method, that takes in the graph built from the config file and stores zero or more Violations. Each Violation refers to one (potential) error. Since one Rule can be violated multiple times, Rules and Violations have a `1:N` relation.

### Mixed Violations

Sometimes, rules can be summarized. Take as example the `<data />` node. It can be read, but never written to. It can also be written to, but never read. Additionally, it can never be written or read. In the latter case, it would be confusing to print two errors ("this data is never written to" and "this data is never read").

Therefore, some Rules have mixed Violation types. For our example, this means the `DataUseReadWrite`-Rule produces Violations that are of different types (`DataNotUsedNotReadNotWrittenViolation`, `DataUsedNotReadNotWrittenViolation`, etc.).
