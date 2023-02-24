# Formula Student Mapping Tools

A set of simple utilities for track mapping, designed for Formula Student autonomous events.

## Motivation

This library is created in order to provide with a normalized model for track mapping processes.

## Implementations

* `cones`: module containing cone mapping utilities.
  * `Cone`: cone representation class. Allows categorization and plotting. Works just like a `Coordinate` instance, but with a linked type.
  * `ConeArray`: cone organization class. Allows categorization, collection and plotting. List-like behavior, but with enforced type rules.

It is intended for future releases to implement ROS custom messages for all classes in this repository.
