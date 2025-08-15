# Reads Depth and Feature Annotation Plotting Tool (DAplot)

This tool generates **SVG, PDF, or PNG plots** that combine genome feature annotations from a GFF3 file and sequencing depth from a `samtools depth` file.

Developed and maintained by Henry Li from [Foundation Plant Services](https://fps.ucdavis.edu/index.cfm) at [UC Davis](https://www.ucdavis.edu/), this utility overhauls an over-engineered implementation, replacing legacy tools that previously relied on deprecated packages. Built in Python using only `numpy`, `matplotlib` and `pyyaml`, this is a quick tool for generating aligned and customizable feature annotation-depth plots in one combined figure.

---

## Table of Contents

- [Reads Depth and Feature Annotation Plotting Tool (DAplot)](#reads-depth-and-feature-annotation-plotting-tool-daplot)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Installation](#installation)
  - [Inputs](#inputs)
  - [Usage](#usage)
    - [Common Options](#common-options)
    - [Supplementary Script](#supplementary-script)
  - [Customization](#customization)
  - [License](#license)

---

## Overview

In Next Generation Sequencing (NGS), reads **depth** provides a measure of how confidently a region of the genome was sequenced. When depth is visualized alongside gene or product annotations, it allows researchers to:

- Identify under or over-sequenced regions.
- Assess the relationship between functional elements and read depth.
- Validate annotations visually.
- Visualize contiguous coverage intervals and reveal potential breaks or low‑support regions.

This tool generates a vertically stacked plot:
- **Top**: Gene product annotations (e.g. RdRp, CP, MP, etc.) as labeled colored boxes on a genome line.
- **Bottom**: Sequencing depth plot over the same genomic range, with optional shading of below‑threshold gaps.

Both plots are **aligned on a shared x-axis** and exported as vector-format graphics suitable for use in publications, with other output options available for downstream fine-tuning. 

---

## Installation

This tool runs with standard Python 3 and requires only:

- `matplotlib`
- `pyyaml`

We recommend using [Anaconda](https://docs.anaconda.com/anaconda/install/) for isolated environment and dependency management:

```bash
conda create -n daplot matplotlib pyyaml
conda activate daplot
```

Alternatively, install from the environment config file that comes with this tool.

```bash
cd bin
conda env create -f env.yml
conda activate daplot
```

No external packages are needed. All file parsing is done using native Python libraries.

---

## Inputs

Three input files are required:

1. **GFF3 file** (`.gff3`) — genome annotations containing features like CDS, product, region, etc
2. **Depth file** — generated from `samtools depth` on aligned reads
3. **YAML file** — customization settings including feature colors, font sizes, depth line color, or title content

Example YAML (`spec.yml`):

```yaml
color_mapping:
  P0 protein: '#88B04B'
  RdRp: '#ef9b20'
  CP: '#ea5545'
  MP: '#27aeef'

default_color: '#9F9F9F'
shade_color: '#CA4F35'
depth_line_color: '#0077CC'
annotation_fontsize: 9
title: ""
```

---

## Usage

To make the combined plot:

```bash
./daplot [-h] -g GFF -d DEPTH -y YAML [-o OUTDIR] [-n] [--grid] [--smooth] [--name NAME] [--no-label] [--no-border] [-t THRESHOLDS [T ...]] [-r] [--shade-breaks] [--title] [--Opdf] [--Opng]
```

### Common Options

```
-g, --gff         GFF3 file containing genome features
-d, --depth       Depth file from samtools depth
-y, --yaml        YAML file with configurations
-o, --outdir      Output directory (default: current folder)
-n, --normalize   Normalize depth values (scales max depth to 1)
-t, --threshold   Depth cut‑offs defining contiguous intervals and breaks (default: 1 5)
-r, --report      Write CSV reports of contiguous intervals and gaps for each threshold tested
--shade-breaks    Shade regions in the depth plot where coverage falls below each specified threshold
--Opdf            Output as PDF
--Opng            Output as PNG
--name            Base name for output file (default: daplot)
--smooth          Smooth depth plot using moving average
--grid            Enable background grid on depth plot
--no-label        Remove labels in features rectangles
--no-border       Remove borders around annotation rectangles
--title           Show title specified in YAML
```

The resulting plot will contain:

- A genome line labeled 5' -> 3'
- Color-coded feature rectangles alternating above and below the genome line
- Optional product names labeled inside or near each box
- A smooth or raw depth curve aligned below
- Optional shaded gap regions for each threshold tested
- Optional CSV report listing contiguous coverage intervals and gaps

### Supplementary Script

This utility includes two separate scripts to assist with parsing depth files:

- `depth_filter.py` – Filters depth entries using a specified target sequence header. This is useful when the reference file contains multiple sequences and only a subset is needed.
- `depth_merger.py` – Merges depth counts across multiple depth files for a single target sequence header. This helps gather total counts at each position across multiple alignment runs.

The depth filter takes a larger depth file and writes depth information to a new depth file, filtering by the sequence header.

```bash
python3 depth_filter.py [-h] -i INPUT -o OUTPUT --seq SEQ
```

The depth merger takes multiple depth files of a single target sequence, sums the counts at each spot to a combined total, and outputs to a new depth file.

```bash
python3 depth_merger.py [-h] -i INPUT [INPUT ...] [-o OUTPUT]
```

---

## Customization

All major visual elements are customizable via the YAML file:

| Key                   | Description                               |
| --------------------- | ----------------------------------------- |
| `color_mapping`       | Maps product names to colors              |
| `default_color`       | Color for unmapped products               |
| `shade_color`         | Color for shaded gap regions              |
| `depth_line_color`    | Line color for depth plot                 |
| `annotation_fontsize` | Font size for labels inside feature boxes |
| `title`               | Plot title                                |

To update feature colors or fonts, edit `spec.yml` and rerun the script.

Due to constraints of `matplotlib.pyplot.subplots`, customization of the spacing between the two plots is limited. Manual adjustments after plot generation is needed if a more compact view is desired.

---

## License

This project is released under the MIT License.
