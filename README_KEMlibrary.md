# Tamarin KEM Library

## Description

The file `KEMLibrary.splib` provides a library enabling in-depth verification of a Tamarin model regarding Key Encapsulation Mechanisms (KEMs) with various sets of security properties.

Refer to "Keeping Up with the KEMs: Stronger Security Notions for KEMs and automated analysis of KEM-based protocols" for further details.

## Usage

To integrate the library, include it in the target `.spthy` file using `#include "KEMLibrary.splib"` after starting a theory.

For KEM operations, use the action fact `Encaps` for encapsulation and `Decaps` for decapsulation of a given ciphertext.

For example, the rule:

```
[In(pub), !KeyValues(k), !CTValues(ct)]--[Encaps(k,ct,pub)]->[Out(ct)]
```

encapsulates a public key `pub` from the network, producing a ciphertext `ct` and a final key `k`.

Decapsulation works similarly:

```
[In(ct), !KeyValues(k), !LTK(sk,pub)]--[Decaps(k,ct,pub,sk)]->[Out(k)]
```

Here, given a ciphertext and a keypair, decapsulation provides a final key `k`.

Both `!KeyValues(k)` and `!CTValues(ct)` represent the keyspace and the ciphertext space, respectively. Include them in every rule involving `Encaps` or `Decaps`.

The user can use any key generation for the KEM public key pair, but denote public keys with the function symbol `kem_pk`.

For generating KEM keys for an honest party, include the action fact:

```
GoodKey(kem_pk(sk))
```

This event distinguishes keys from key generation and potential adversary-generated values.

The library includes multiple flags enabling various KEM behaviors. Execute the target file with the following command:

```
tamarin-prover target.spthy -D=Param1 ... -D=Paramn
```

By default, the KEM provides properties modeling IND-CCA2 and Correctness, which can be deactivated with flags `NoCCa` and `noCorrectness`.

```
tamarin-prover target.spthy -D=NoCCa -D=noCorrectness
```

### Binding Properties

Enable binding properties from "Keeping Up with the KEMs: Stronger Security Notions for KEMs and automated analysis of KEM-based protocols" using preprocessor flags. For property `X-Bind-P-Q`:

```
if X=MAL:
    bindPtoQ /\ MAL
else 
    bindPtoQ
```

For example, invoke `MAL-Bind-{ct}-{k}` with:

```
tamarin-prover target.spthy -D=bindcttok -D=MAL
```

and `HON-Bind-{ct}-{pk}` with:

```
tamarin-prover target.spthy -D=bindcttopk
```

### Honest Key Generation

In addition to binding properties, the flag:

```
GoodKeysOnly
```

restricts Tamarin to only allow `Encaps` and `Decaps` with public keys annotated with `GoodKey`. This mode disables the adversary's capability to inject 'bogus' values into the KEM.
