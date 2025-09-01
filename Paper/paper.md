---
title: 'Alpaga: A Python package for automated analysis of Second Harmonic Generation polarization experiments'
tags:
  - Python
  - Experimental Results Analysis 
  - Nonlinear optics
  - Surface Second Harmonic Generation
  - Second Harmonic Scattering
  - Hyper Rayleigh Scattering
  - Polarization Analysis
authors:
  - name: Fabien Rondepierre
    orcid: 0000-0003-4721-4690
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 1
  - name: Maxime Fery 
    affiliation: 1
  - name: Oriane Bonhomme
    orcid: 0000-0001-6009-2240
    affiliation: 1
  - name: Guillaume Le Breton
    orcid: 0000-0002-2019-6106
    corresponding: true
    equal-contrib: true
    affiliation: 1 
affiliations:
 - name: Institut Lumière Matière, UMR5306, Villeurbanne, France
   index: 1
date: 1 September 2025
bibliography: paper.bib
csl: https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl
---

# Summary

`Alpaga` (AnaLyse en PolArisation de la Génération de second hArmonique) is a Python package designed for the automated analysis of Second Harmonic Generation (SHG) experimental acquisitions. The software provides a comprehensive workflow for processing spectroscopic measurements from Surface Second Harmonic Generation (SSHG) [@shen1989surface ; @tran2017applications] and Second Harmonic Scattering (SHS) experiments, which are crucial techniques in surface science and nonlinear optics research.

The package implements a robust automated procedure that extracts Gaussian peak intensities from spectral measurements through three main steps: automatic file detection and organization, spectral cleaning and averaging with  removing non-physical artifacts, and Gaussian fitting for intensity extraction. This automated approach significantly reduces the time and potential human error associated with manual data processing while providing consistent and reproducible analysis results.

# Statement of need

SHG experiments involve long acquisition times, which generate large volumes of spectroscopic data often affected by significant noise, requiring careful processing to extract meaningful physical parameters. Researchers typically face several challenges when analyzing SHG data: (1) handling numerous acquisition files with varying experimental parameters, (2) removing non-physical artifacts, (3) averaging multiple acquisitions to improve signal-to-noise ratios, and (4) consistently fitting Gaussian profiles to extract peak intensities. These tasks are often performed manually or with custom scripts, leading to inconsistencies between research groups and potential analysis errors.

![Alpaga goal: a) robustly extract from raw spectra meaningful information from second harmonic generation experimental setups. b) Sequence of second-harmonic signal processing steps: Suppression of spurious peaks and averaging of multiple acquisitions performed with the averaging_and_cleaning function;  Noise estimation and correction across distinct processing regions using the remove_noise function; Extraction of the second-harmonic component followed by Gaussian fitting with the fit_gauss function; c) Fourier analysis of polarization-resolved SHS measurements using the analysis_polarisation_SHS_V function.](fig1.pdf){ width=85% }

`Alpaga` addresses these challenges by providing a standardized, automated workflow specifically designed for SHG polarization analysis. The Figure presents this robust data processing: going from experimental raw results to a research-oriented analysis, thanks to noise cleaning and peak intensity extraction. The software is particularly valuable for research groups working with SSHG and SHS experiments, where systematic analysis of polarization-dependent measurements is essential for understanding surface properties and molecular orientation. Python enables `Alpaga` to provide a user-friendly interface while leveraging efficient numerical libraries for computationally intensive operations.

`Alpaga` was designed to be used by both experienced researchers in nonlinear optics and students learning SHG analysis techniques. The automated nature, supported by comprehensive documentation (wiki) and tutorials, makes the workflow accessible to newcomers while providing the reliability and consistency required for research applications.

# Key Features and Implementation

`Alpaga` is built on established Python scientific libraries, including NumPy, SciPy, and Matplotlib, providing reliable numerical operations and visualization capabilities. The software architecture follows a modular design with several key components:

**Automated File Management**: The software automatically identifies and organizes spectroscopic data files based on experimental parameters, streamlining the analysis workflow for large datasets with consistent naming conventions.

**Spectral Cleaning and Averaging**: Detection and removal of electronic noise and other non-physical spikes from spectra. The cleaning procedure includes configurable parameters for spike detection sensitivity and handles the averaging of multiple acquisitions with identical experimental parameters to improve signal-to-noise ratios.

**Gaussian Fitting with Multiple Options**: The package offers various fitting approaches for extracting peak intensities from Gaussian profiles. Users can select from different fitting algorithms and configure parameters such as baseline handling (fluorescence background) to optimize results based on their specific experimental conditions.

**Domain-Specific Analysis Tools**: Dedicated modules for SSHG and SHS analysis provide specialized functionality for extracting physical parameters relevant to surface science applications, including polarization-dependent analysis and orientation parameter extraction.

# Related Work
The automated workflow of `Alpaga` sets it apart from the manual analysis methods often used in the field, offering greater consistency and efficiency for SHG research groups.
In contrast to general-purpose spectroscopic packages such as rampy [@rampy], `Alpaga` addresses the specific needs of the SHG community by providing dedicated tools for polarization-dependent measurements.
It embeds domain knowledge of SHG experiments, including typical artifact patterns, polarization conventions, and the mathematical frameworks required for SSHG and SHS analysis.
In addition, `Alpaga` features a file management system designed for handling multiple spectra per acquisition, a capability particularly relevant for polarization-based studies.

# Usage and Impact
The `Alpaga` project started in 2022 at the Institut Lumière Matière laboratory (ILM), France, to merge all the different analysis tools established in our experimental group. The four authors of this publication participated in the code development and usage. 
To date, about a dozen scientists have used `Alpaga` to treat experimental data. 
The software has already enabled more efficient and consistent data analysis workflows for research groups working with SSHG and SHS experiments (at ILM or other labs, thanks to the automated file management procedure), and contributes to improved reproducibility in SHG research.
This procedure has been used in multiple scientific communications and publications [@le2022second ; @le2023liquid ; @le2024microscopic ; @fery2025sonder ; @rondepierre2025correlations ; @rf1 ; @rf2 ], while not always being directly mentioned. 

The package includes comprehensive documentation with detailed examples and parameter explanations, making it accessible to both experienced researchers and newcomers to SHG analysis. Installation is straightforward through standard Python package management tools, and the software is distributed under the LGPL v2.1 license to ensure broad accessibility.

# Acknowledgements
We are grateful to Estelle Salmon, Emmanuel Benichou, and Pierre-François Brevet for their valuable help, insightful guidance, and for generously sharing their previous implementation, which has significantly shaped `Alpaga` current workflow.
We also warmly acknowledge the former members of the ONLI group, Aurélie Bruyère, Lucile Sanchez, and Antonin Pardon ADD MORE?, whose pioneering contributions laid the foundation for the present development of the experimental workflow.
This work was conducted at the Institut Lumière Matière (ILM).

# References

