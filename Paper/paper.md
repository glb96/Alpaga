---
title: 'Alpaga: A Python package for automated analysis of Second Harmonic Generation polarization experiments'
tags:
  - Python
  - Nonlinear optics
  - Second Harmonic Generation
  - Polarization analysis
  - Surface spectroscopy
  - Bulk spectroscopy
authors:
  - name: Guillaume Le Breton
    orcid: 0000-0002-2019-6106
    corresponding: true
    equal-contrib: true
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Fabien Rondepierre
    orcid: 0000-0003-4721-4690
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 1
  - name: Maxime Fery 
    affiliation: 1
  - names: Oriane Bonhomme
    orcid: 0000-0001-6009-2240
    affiliation: 1
affiliations:
 - name: Institut Lumière Matière, UMR5306, Villeurbanne, France
   index: 1
date: 1 September 2025
bibliography: biblio.bib
---

# Summary

Alpaga (AnaLyse en PolArisation de la Génération de second hArmonique) is a Python package designed for the automated analysis of Second Harmonic Generation (SHG) experimental acquisitions. The software provides a comprehensive workflow for processing spectroscopic measurements from Surface Second Harmonic Generation (SSHG) and Second Harmonic Scattering (SHS) experiments, which are crucial techniques in surface science and nonlinear optics research.

The package implements a robust automated procedure that extracts Gaussian peak intensities from spectral measurements through three main steps: automatic file detection and organization, spectral cleaning and averaging with cosmic ray removal, and Gaussian fitting for intensity extraction. This automated approach significantly reduces the time and potential human error associated with manual data processing while providing consistent and reproducible analysis results.

# Statement of need

Second Harmonic Generation experiments generate large volumes of spectroscopic data that require careful processing to extract meaningful physical parameters. Researchers typically face several challenges when analyzing SHG data: (1) handling numerous acquisition files with varying experimental parameters, (2) removing non-physical artifacts such as cosmic ray spikes, (3) averaging multiple acquisitions to improve signal-to-noise ratios, and (4) consistently fitting Gaussian profiles to extract peak intensities. These tasks are often performed manually or with custom scripts, leading to inconsistencies between research groups and potential analysis errors.

`Alpaga` addresses these challenges by providing a standardized, automated workflow specifically designed for SHG polarization analysis. The software is particularly valuable for research groups working with SSHG and SHS experiments, where systematic analysis of polarization-dependent measurements is essential for understanding surface properties and molecular orientation. Python enables `Alpaga` to provide a user-friendly interface while leveraging efficient numerical libraries for computationally intensive operations.

`Alpaga` was designed to be used by both experienced researchers in nonlinear optics and students learning SHG analysis techniques. The automated nature of the workflow makes it accessible to newcomers while providing the reliability and consistency required for research applications.

# Key Features and Implementation

`Alpaga` is built on established Python scientific libraries including NumPy, SciPy, and Matplotlib, providing reliable numerical operations and visualization capabilities. The software architecture follows a modular design with several key components:

**Automated File Management**: The software automatically identifies and organizes spectroscopic data files based on experimental parameters, streamlining the analysis workflow for large datasets with consistent naming conventions.

**Spectral Cleaning and Averaging**: Advanced algorithms detect and remove cosmic ray artifacts and other non-physical spikes from spectra. The cleaning procedure includes configurable parameters for spike detection sensitivity and handles the averaging of multiple acquisitions with identical experimental parameters to improve signal-to-noise ratios.

**Gaussian Fitting with Multiple Options**: The package offers various fitting approaches for extracting peak intensities from Gaussian profiles. Users can select from different fitting algorithms and configure parameters such as baseline handling and peak identification criteria to optimize results based on their specific experimental conditions.

**Domain-Specific Analysis Tools**: Dedicated modules for SSHG and SHS analysis provide specialized functionality for extracting physical parameters relevant to surface science applications, including polarization-dependent analysis and orientation parameter extraction.

# Related Work

While several general-purpose spectroscopic analysis packages exist, such as `scikit-spectra` and `rampy` [@rampy], `Alpaga` fills a specific niche in the SHG community by providing specialized tools tailored to the unique requirements of polarization-dependent SHG measurements. Unlike general spectroscopy packages, `Alpaga` incorporates domain knowledge about SHG experiments, including understanding of typical artifact patterns, polarization conventions, and the specific mathematical frameworks used in SSHG and SHS analysis [:cite:p:`rondepierre2025correlations`; @fery2025sonder; le2022second].

The automated nature of `Alpaga`'s workflow distinguishes it from manual analysis approaches commonly used in the field, providing both consistency and efficiency improvements for SHG research groups.

# Usage and Impact

`Alpaga` has been successfully used in multiple scientific communications and publications, demonstrating its practical value in the SHG research community [@ref1; @ref2; @ref3; @ref4]. The software has enabled more efficient and consistent data analysis workflows for research groups working with SSHG and SHS experiments, contributing to improved reproducibility in SHG research.

The package includes comprehensive documentation with detailed examples and parameter explanations, making it accessible to both experienced researchers and newcomers to SHG analysis. Installation is straightforward through standard Python package management tools, and the software is distributed under the LGPL v2.1 license to ensure broad accessibility.

# Acknowledgements

We acknowledge the Institut Lumière Matière (ILM) for supporting the development of this software and the broader SHG research community for valuable feedback and testing. We also thank the contributors who have helped improve the software through bug reports and feature suggestions.

# References

