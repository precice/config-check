# preCICE configuration validation rules

This checker in development for the coupling library preCICE.

Currently, through the preCICE native command `precice-tools check`, syntax and basic setup mistakes will get checked.

Our checker assumes that this command has been executed beforehand and returned without an error.
Cases that get handled beforehand do <em>not</em> get checked by this logical checker.
Instead, we try to find <em>logical</em> mistakes in the configuration file, which adhere to the defined syntax of
preCICE, but will lead to errors when actually running the simulation.

Here you will find an overview over all logical errors, which we refer to as 'rules', which currently get handled by our
preCICE config checker.
Our rules have been sorted into three categories of <em>severity</em>:

- `error`: These rules should be adhered to, in order to guarantee (a flawless) execution of the coupled simulation.
- `warning`: Rules in this category do not necessarily cause errors during the simulation, yet should be inspected to
  ensure the intended outcome.
- `debug`: These rules are simply hints and do not get checked or printed by default. 
Usually they do not represent mistakes but are meant to help find the most hidden bugs 🪲

Rules with `TODO` before their names have not yet been implemented but will be soon.

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

### `TODO` Coupling-scheme without mapping

To ensure that exchanged data between one participant and its mesh to another participant and its mesh, the mapping has
to be defined.
If the mapping does not get defined, it is not certain that the meshes “fit together” and data gets exchanged
correctly.

It is possible, however, that meshes fit together naturally.

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

### `TODO` Unused mesh

A participant can provide a mesh to another participant, who receives it but does not use it.
This means that the mesh is not used in any coupling scheme.

This does not necessarily cause the simulation to malfunction or misbehave.

## Rules with severity `debug`

### `TODO` Disjoint simulations

A simulation between participants A and B and a second one between participants C and D can run simultaneously, but will
deteriorate the readability of the preCICE-config and will make it more prone to errors.

In most cases, however, running multiple “disjoint simulations” simultaneously is intended.   