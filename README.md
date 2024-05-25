# Populate SAS-format CSV file with random marks and grades for use with SITS by Tribal Group

Populates SAS_ACTM and SAS_ACTG fields on importable-SAT-type csv.

## Dependencies

- **pandas** for data manipulation, supported by **numexpr** and **bottleneck** which accelerate operations on large dataset and are used by pandas by default where available.
- **random** in-built library for generating pseudo-random numbers
- **numpy** is used for NaN-type only.

## Inputs

In an "exports" folder, provide:
- "NEW_MKC.CSV" file contain all MKC records for the MKSs under consideration
- "SAS_MKS.CSV" file containing exported SAT records, joined to the relevant MKS (field name = "NEWMKS")

## SAT fields

1. SAS_ACTM = actual mark, four digits (0000)
2. SAS_ACTG = actual grade, one or two characters (XX)

Primary key fields on for SAS records are:

- SPR_CODE
- MOD_CODE
- MAV_OCCUR
- AYR_CODE
- PSL_CODE
- MAP_CODE
- MAB_SEQ

## Mark generation

Some MKSs are grade only. Where a SAT is associated with an grade-only scheme, no mark is generated.

**Note** - schemes are identified as mark/grade by their naming pattern - i.e. fourth character = "M" (not "G").
*It would be possible to implement a more reliable check by also exporting MKS records.*

Otherwise, a pseudo-random mark of between 0 and 100 is added to the SAS_ACTM field.

## Grade generation

Grades are generated based on the associated mark scheme - i.e. a randomly selected but *valid* grade is selected for the given SAS record based on the chosen mark and selected MKS.

**Note** - because of the random distribution of marks and random selection of valid grades, certain grades will be comparatively uncommon (e.g. FN, other grades that require a specific mark) and other grades much more common (e.g. AO, other grades that permit any mark).

# MKS records in use 01/05/24

Of the unique values in NEWMKS field, the following are **new MKS records**:

- P1AMFR
- U1AMFR
- P1AGFR
- U1AGNR
- U1AGFR
- U1AMNR
- U1AMAR
- P1AMNR
- P1AMAR

The adopted approach is to produce a **filtered data frame** where the value of NEWMKS corresponds with a new mark scheme code.

## Ouput process

Requirement is to ouput primary key fields (see above) and new fields (SAS_ACTM and SAS_ACTG) only.

There are two outputs, both stored in the "output" folder:
- **SAS_SUMMARY.CSV** which contains all generated fields, derived from the original SAS export
- **SAS_TO_IMPORT.CSV**, a trimmed down version of SAS_SUMMARY with only the fields required for import
