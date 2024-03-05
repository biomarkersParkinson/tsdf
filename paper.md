---
title: 'TSDF: A Python package for Time Series Data Format'
tags:
  - Python
  - Matlab
  - time series
  - sensor data
  - metadata
  - binary data
authors:
  - name: Vedran Kasalica
    email: v.kasalica@esciencecenter.nl
    affiliation: 1
    orcid: 'https://orcid.org/0000-0002-0097-1056'

  - name: Pablo Rodríguez-Sánchez
    email: p.rodriguez-sanchez@esciencecenter.nl
    affiliation: 1
    orcid: 'https://orcid.org/0000-0002-2855-940X'

  - name: Luc J.W. Evers
    email: luc.evers@radboudumc.nl
    affiliation: 2, 3
    orcid: 'https://orcid.org/0000-0002-8241-5087'
    corresponding: false

  - name: Max A. Little
    email: maxl@mit.edu
    affiliation: 4, 5
    orcid: 'https://orcid.org/0000-0002-1507-3822'

  - name: Peter Kok
    email: p.kok@esciencecenter.nl
    affiliation: 1
    orcid: 'https://orcid.org/0000-0002-6630-7326'
    corresponding: true

affiliations:
 - name: Netherlands eScience Center, Amsterdam, The Netherlands
   index: 1
 - name: Radboud University, Institute for Computing and Information Sciences, Department of Data Science, Nijmegen, Netherlands, 
   index: 2
 - name: Radboud University Medical Center, Donders Institute for Brain, Cognition and Behaviour, Department of Neurology, Center of Expertise for Parkinson and Movement Disorders, Nijmegen, Netherlands
   index: 3
 - name: School of Computer Science, University of Birmingham, UK
   index: 4
 - name: MIT, Cambridge, MA, USA
   index: 5
   # Add other author affiliations here
date: 4 March 2024
bibliography: paper.bib
---

# Summary

The `tsdf` package[^1] is a comprehensively documented reference implementation of the Time Series Data Format (TSDF) standard[^2], proposed by [@claes2022tsdf]. TSDF simplifies data storage and exchange of multi-channel digital sensor data, thereby promoting interpretability and reproducibility of scientific results across studies. Sensor measurements and timestamps are stored as raw tabular binary array files. To ensure unambiguous reconstruction, binary array files are accompanied by human-readable JSON metadata files, which contain a set of mandatory fields that are limited to essential sensor measurement information. 

The `tsdf` Python package implements functions for reading and writing Time Series Data Format (TSDF) [@claes2022tsdf] files. It guarantees formatting and metadata consistency. It enforces usage of the essential metadata such as study identification, time frame, data channel descriptions and data attributes corresponding to the binary data. It also includes a convenient Matlab wrapper [@tsdf4mat].

# Statement of need

Digital sensors are being used to monitor health and disease at an increasingly larger scale, resulting in large amounts of high-frequency, multi-channel time series data [@coravos2019developing]. To facilitate efficient data storage and re-use, the TSDF standard [@claes2022tsdf] was proposed as an open, unified format for storing all types of digital sensor data, across diverse disease areas. Here, we present the `tsdf` Python package, a public reference implementation of the TSDF standard, to facilitate its adoption by the scientific community. The `tsdf` package has already been used to facilitate large-scale data analysis of the Personalized Parkinson Project, a cohort study of 513 people with Parkinson's disease, which includes the continuous collection of multi-channel raw sensor data from a wrist-worn device, for 2 up to 3 years [@bloem2019personalized].

There are many approaches to store time series data as files. Simply storing the data as binary blocks leaves the user with too much freedom to interpret it, lacking a metadata structure. On the other end of the spectrum, textual formats like CSV or JSON are too inefficient on space, while libraries for reading and writing are readily available.
The efficiency of Prototocol Buffers[^3] is limited by complex structures. It involves compiling custom message schemas into a programming language of choice, providing the developer with a custom implementation. We deem this approach too complicated for many researchers.
NetCDF[^4], though robust, introduces usability and collaboration challenges due to its complexity.

Although the TSDF standard is to a large extent self-explanatory and basic read/write functionality is straightforward to implement, we believe that a stable, documented and flexible reference implementation is beneficial for a number of reasons. Implementing common functionality in a package increases readability, reduces redundancy by preventing repeated code, while simultaneously reducing the chance of errors in an implementation by researchers who might not be proficient in coding.


# Features

For loading numerical data (i.e. sensor measurements and associated timestamps), the `tsdf` package interacts with the NumPy [@harris2020array] and Pandas [@reback2020pandas] libraries. A dedicated data structure, `TSDFMetadata`, manages the metadata file's structure and this structure can be used to load or save binary data directly from/to NumPy arrays and Pandas DataFrames. To save resources, numerical data can be randomly accessed by loading only a selection of rows. The library ensures that alterations made to the loaded data, such as data type, are automatically reflected in the updated metadata file upon saving. The saved metadata is optimized to minimize redundancy: it makes use of the hierarchical JSON structure to maximize sharing of common fields.
In addition, the library can be used as a validator, both from code and as a command line tool, to check the compliance of existing data with the TSDF standard.

# Acknowledgements

This work was supported by the Netherlands eScience Center under grant number ASDI.2020.060 and by the Michael J Fox Foundation (grant #MJFF.020425). 

# References

<!-- Footnotes -->
[^1]: [https://pypi.org/project/tsdf/](https://pypi.org/project/tsdf/)
[^2]: [https://biomarkersparkinson.github.io/tsdf/](https://biomarkersparkinson.github.io/tsdf/)
[^3]: [https://protobuf.dev/](https://protobuf.dev/)
[^4]: [https://www.unidata.ucar.edu/software/netcdf/] (https://www.unidata.ucar.edu/software/netcdf/)
