# journal-article-template
This repository contains the relevant files for the "Verification of Moltres
for Multiphysics Simulations of Fast-Spectrum Molten Salt Reactors" manuscript
to be submitted to Annals of Nuclear Energy. This work presents code-to-code
verification of Moltres in the context of the CNRS benchmark which is a
numerical multiphysics benchmark for software dedicated to modeling
fast-spectrum molten salt reactors.

# Outline
The top-level directory contains all TeX files for
the journal article itself.

The `graph-abs` directory holds all files for the
graphical abstract.

The `highlights` directory holds all files for the
3-5 bullet point highlights.

The `letter` directory holds all files for the cover
letter to the journal editor and reviewers.

The `revise` directory holds all files for revision
comments and the corresponding edits. Each new round
of revisions should be covered in a separate TeX
file.

The `python` directory holds all of the output data files from the Moltres simulations
and the python scripts for postprocessing and generating the plots for the
journal article.

# To compile
Run `make` from the base directory.
