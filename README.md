# Reads Depth and Feature Annotation Plotting Tool (DAplot)

This tool generates **SVG, PDF, or PNG plots** that combine genome feature annotations from a GFF3 file and sequencing depth from a `samtools depth` file.

Maintained by Henry Li from [Foundation Plant Services](https://fps.ucdavis.edu/index.cfm) at [UC Davis](https://www.ucdavis.edu/), this utility replaces legacy tools that relied on deprecated packages. It is built Python using only `numpy`, `matplotlib` and `pyyaml`, and is a quick tool for generating aligned, customizable annotation and depth plots in one combined graph.

---

## Table of Contents

- [Reads Depth and Feature Annotation Plotting Tool (DAplot)](#reads-depth-and-feature-annotation-plotting-tool-daplot)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Installation](#installation)
  - [Inputs](#inputs)
  - [Usage](#usage)
    - [Common Options](#common-options)
  - [Customization](#customization)
  - [License](#license)

---

## Overview

In Next Generation Sequencing (NGS), reads **depth** provides a measure of how confidently a region of the genome was sequenced. When depth is visualized alongside gene or product annotations, it allows researchers to:

- Identify under or over-sequenced regions.
- Assess the relationship between functional elements and read depth.
- Validate annotations visually.

This tool generates a vertically stacked plot:
- **Top**: Gene product annotations (e.g. RdRp, CP, MP, etc) as labeled colored boxes on a genome line.
- **Bottom**: Sequencing depth plot over the same genomic range.

Both plots are **aligned on a shared x-axis** and exported as vector-format graphics suitable for use in publications while offering other output options.

---

## Installation

This tool runs with standard Python 3 and requires only:

- `matplotlib`
- `pyyaml`

We recommend using [Anaconda](https://docs.anaconda.com/anaconda/install/) for environment and dependency management:

```bash
conda create -n daplot numpy matplotlib pyyaml
conda activate daplot
```

No external packages are needed. All file parsing is done using native Python libraries.

---

## Inputs

Three input files are required:

1. **GFF3 file** (`.gff3`) — genome annotations containing features like CDS, product, region, etc
2. **Depth file** — generated from `samtools depth` on aligned reads
3. **YAML file** — customization settings including feature colors, font sizes, and line color

Example YAML (`spec.yml`):

```yaml
color_mapping:
  P0 protein: '#88B04B'
  RdRp: '#ef9b20'
  CP: '#ea5545'
  MP: '#27aeef'

default_color: '#9F9F9F'
depth_line_color: '#0077CC'
annotation_fontsize: 9
title: ""
```

---

## Usage

```bash
daplot [-h] -g GFF -d DEPTH -y YAML [-o OUTDIR] [-n] [--grid] [--smooth] [--no-border] [--Osvg] [--Opdf] [--Opng]
```

### Common Options

```bash
-g, --gff         GFF3 file containing genome features
-d, --depth       Depth file from samtools depth
-y, --yaml        YAML file with color/font configuration
-o, --outdir      Output directory (default: current folder)
--Osvg            Output as SVG (default)
--Opdf            Output as PDF
--Opng            Output as PNG
--normalize       Normalize depth values (scales max depth to 1)
--smooth          Smooth depth plot using moving average
--grid            Enable background grid on depth plot
--no-border       Remove borders around annotation rectangles
```

The resulting plot will contain:

- A genome line labeled 5' -> 3'
- Color-coded boxes alternating above and below the genome line
- Product names inside each box
- A smooth or raw depth curve aligned below

---

## Customization

All major visual elements are customizable via the YAML file:

| Key                   | Description                                       |
| --------------------- | ------------------------------------------------- |
| `color_mapping`       | Maps product names to colors                      |
| `default_color`       | Color for unmapped products                       |
| `depth_line_color`    | Line color for depth plot                         |
| `annotation_fontsize` | Font size for labels inside feature boxes         |
| `title`               | Plot title (not yet implemented)                  |

To update feature colors or fonts, edit `spec.yml` and rerun the script.

---

## License

This project is released under the MIT License.
