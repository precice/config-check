Some title info here

- logic checker for precice, rules for precice config
- for suggestions / new rules: github issue (check here first)
- we assume `precice-tools check` has been executed -> cases that get handled there do not get checked in our checker

Here you will find an overview over all logical errors, which we refer to as 'rules', which currently get handled by our
preCICE config checker.
Our rules have been sorted into three categories of <em>severity</em>:

- `error`: These rules should be adhered to ("eingehalten"), in order to guarantee a flawless ("fehlerfreie")
  execution (bzw. überhaupt eine) of the coupled simulation.
- `warning`: Rules in this category represent an oversight in the config and are not necessary to implement.
- `debug`: These rules are simply hints and do not get checked by default. Usually they do not represent mistakes but
  are meant to help find the most hidden bugs 🪲

## Rules with severity `error`

### Missing coupling-scheme

If a preCICE config.xml is missing a coupling-scheme (or a multi-coupling-scheme), then no data gets exchanged between
participants.

Since preCICE is a tool for running coupled simulations between multiple participants, not defining a coupling-scheme is
an error.

### Missing exchange

In order for data to get exchanged, it has to be communicated through an 'exchange'. If data gets declared but not
exchanged through an exchange, then its declaration is redundant.

#### Missing exchange: no full usage of data

Data gets declared but not fully utilized (not used in a mesh, not read or not written by a participant). Additionally,
there exists no exchange for this data element.

#### Missing exchange: full usage of data 

Data gets declared and used in a mesh, read and written by a participant, but not exchanged in a coupling-scheme.

## Rules with severity `warning`

### Data rules

A data element in a preCICE needs to be mentioned at many locations to finally allow it to be communicated from one
participant to another.
To exchange it from one participant to another, after declaration, data has to be:

- used in a mesh
- written by a participant
- read by a participant (or read through other means, e.g., of immediate export)
- exchanged in a coupling-scheme

The last point already gets checked in `Missing coupling-scheme` and `Missing exchange`.<br>
All other cases get checked here (minus the ones that get handled by `precice-tools check`).

Using, reading or writing data without the respective other tags is not as severe an error, as this data element is
likely not used in the simulation yet, due to multiple tags missing.

For the exact implementation, see `rules/data_use_read_write.py`.

#### Data gets used but not written or read

The data element gets used in a mesh, but no participant is reading or writing it.

#### Data gets used and read, but not written

The data element gets used in a mesh and read by a participant (or other ways of acquiring the data), but no participant
is writing the data.

#### Data gets used and written, but not read

The data element gets used in a mesh and written by a participant, but nobody is reading it (or acquiring the data
through other means).

#### Data does not get used, read or written

The data element gets declared but not used in a mesh, read or written by any participant.

## Rules with severity `debug`

