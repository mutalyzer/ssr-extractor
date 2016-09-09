# Automatic Extraction and Annotation of Short Tandem Repeats (STR)

We propose a first layout of a workflow for the automatic extraction and
annotation of STRs using the existing ssr-extractor and the Variant
Description Extractor (VDE).

## Step 1 --- Automatic Extraction of STRs from a Reference Sequence

Within a reference sequence we give a certain region of interest
(preferably given by the start and end positions of the repeat structure).
The `start` position will function as point of reference.


```
... AAAA x BBBB y CCCC ...
   ^                  ^
   | start            | end
```

- The ssr-extractor is used to generate:
```
... A[4] x B[4] y C[4] ...
```
In most cases we expect the output to be very close to what is currently
seen as repeat units, however, if this does not result in the preferred
repeat unit, the repeat units can be manually given as input in Step 2.

- From this we select the repeat units according to some thresholds, e.g.,
unit length > 2 and number of repeats > 3; (this should be decided)

- Construct the repeat unit set `{A, B, C}`, including the positions of
their first and last occurrences, e.g., A := 10_14; B := 117_120;
C := 153_157. Numbering starts at `start`.

## Step 2 --- Extraction using the VDE

- Given the reference sequence and the repeat unit set and an observed
sequence;

- A description for the flanking regions (if any) is constructed using
the regular VDE;

- Either the repeat unit set is created using Step 1 or alternatively,
given as input for annotating a priori known repeat units or repeat units
missing from the reference sequence;

- The region between `start` and `end` is extracted c.f. transpositions
in the VDE using the repeat unit set, e.g.,
```
[...;10_14(4);aggttctat;117_120(6);tttattgcg;153_157(7);10_14(4);...]
```
(this part is to be implemented in the VDE)

## Step 3 --- Conversion to (HGVS) Description

- Conversion to HGVS(-like) format:
```
hg38[100000-100300]:l.[-30A>G;-12T>A;10_14(4);aggttctat;117_120(6);tttattgcg;153_157(7);10_14(4);*23G>C]
```
some relevant slice is selected from a reference sequence to do annotation
based on the sequenced part.

or (if preferred with the filled in repeat units):
```
hg38[100000-100300]:l.[-30A>G;-12T>A;TATC(4);aggttctat;TTA(6);tttattgcg;AGGC(7);TATC(4);*23G>C]
```

- (other supported output formats)

Note that the resulting annotation is very similar (maybe equal) to TSSV,
i.e., the observed sequence is always described as a deletion/insertion in
the reference sequence with annotated repeat units. Variants are only
described in the flanking regions. Alternatively, we could extract
(describe variants) in the inter-repeat regions. An example with
repeat unit set = {`aatc`}:
```
 ... aatc aatc aatc aatc aggttctat aatc aatc ...
 ... aatc aatc aatc aggccctat aatc aatc aatc ...
```
could be described and annotated as follows:
```
...; aatc(3); 20_21delinsCC; aatc(3); ...
```
In this case the repeat annotation has meaning as a description; any
number of `aatc`'s in the reference sequence is deleted and a given
number, possibly zero, of `aatc`'s is inserted in the observed sequence.
For the aforementioned example:
```
...; 1_16delins[AATC(3)]; 20_21delinsCC; 26_33delins[AATC(3)]; ...
```

## Outline of the addition to the VDE
Given a reference sequence, an observed sequence and a repeat unit set
(within the region `start`, `end`).
- Delete all occurences of the repeat units from the reference sequence;
- Delete all occurences of the repeat units from the observed sequence and
 save their counts;
- From the remaining parts of both sequences (together with the flanking
 regions)
 construct a new sequence and save the partitioning;
- Perform the regular VDE extraction on the newly constructed sequences;
- Apply the partioning to the resulting description and add the repeat
 unit annotation.

### Example
With repeat unit set = {`aat`}:
```
aat aat aat aat att atc
aat aat att aat atc atg
```
Option 1:
```
1_12delins[1_3(2)]; 15_16ins1_3; 19_20insATG
1_12delins[AAT(2)]; 15_16insAAT(1); 19_20insATG
```
Option 2:
```
1_18delins[1_3(2); 13_15; 1_3; ATG]
1_18delins[AAT(2); 13_15; AAT(1); ATG]
```

### Algorithm Option 2
- Create delins from `start` to `end`;
- Mask repeated units in the reference sequence: `aat $$$ $$$ $$$ att atc`;
- Perform VDE extraction with small transpositions (size should be decided)
 on the masked reference sequence.

