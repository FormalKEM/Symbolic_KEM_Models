# Keeping Up with the KEMs

This repository contains all case studies from

`Keeping Up with the KEMs: Stronger Security Notions for KEMs and automated analysis of KEM-based protocols`

and the means to reproduce them.

## Structure

All Tamarin protcol models can be found in the folders

```
Kyber
OnepassAKE
PQSPDM
Sigma_Zero
```

and the precomputed Results can be found in `precomputed_RES`

## Dependencies

We rely on the [Tamarin prover](https://tamarin-prover.com/) version 1.9.0. on the develop branch

```
tamarin-prover 1.9.0, (C) David Basin, Cas Cremers, Jannik Dreier, Simon Meier, Ralf Sasse, Benedikt Schmidt, 2010-2023

This program comes with ABSOLUTELY NO WARRANTY. It is free software, and you
are welcome to redistribute it according to its LICENSE, see
'https://github.com/tamarin-prover/tamarin-prover/blob/master/LICENSE'.

maude tool: 'maude'
checking version: 2.7.1. OK.
checking installation: OK.
Generated from:
Tamarin version 1.9.0
Maude version 2.7.1
Git revision: 86014ad1844247b4faac36bc15f83befde30dcd7, branch: develop
```

Details regarding installation can be found on [Tamarin's webpage](https://tamarin-prover.com/manual/master/book/002_installation.html)

### Python Dependencies

To install all dependencies to execute the case studies, run

```
apt-get install python3
apt-get install python3-pip
pip3 install tabulate matplotlib graphviz
```

## Instructions to reproduce the results

### Main analysis

To execute all case studies run

```
sh analysis.sh all
```

Alternativley, to execute single case studies, replace the `all` with `onepass`,`kyber`,`sigma`,`perfectsigma` or `pqspdm`.

### Finding the right binding properties

To search the minimal needed binding properties of the lemmas mentioned in Table 4 of the paper,
execute

```
sh Onepass.sh
```

```
sh kyber.sh
```

```
sh sigma.sh
```

and you can find the results as `.pdf`-files in the respective protocol folders

### Oracle Tests

To see that the hierarchy of binding properties from Figure 7 also in the symbolic model
one can also run

```
python3 test_cases.py --test
```

which will run all combinations of binding properties on Tamarin models capturing
the binding games from Figure 5 and Figure 6.

## KEM Library

All details on how to use the KEMlibrary can be found [here](README_KEMlibrary.md)
