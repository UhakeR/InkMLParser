# InkMLParser

![Project Image](project_image.png)

The purpose of this project is to extract and use the data from InkML files, you can save the data as a `.png`, and as a `CVS` table.
it's not complete, I want to add more features in the future

## Table of Contents

- [InkMLParser](#inkmlparser)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Key Features](#key-features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Examples](#examples)

## Introduction

The `InkMLParser` is a Python class designed to simplify the process of parsing INKML files, a common format for representing handwritten or sketch-based data. This parser allows you to extract valuable information from INKML files, including user interface annotations, annotations, trace data (X and Y coordinates), and symbol data.

## Key Features

- **User Interface Information (UI):** Extract user interface annotations.
- **Annotations:** Retrieve annotations associated with ink data.
- **Trace Data:** Parse raw ink trace data (X and Y coordinates).
- **Symbol Data:** Associate annotations with corresponding trace data for symbol-level information.

## Getting Started

Follow these steps to get started with the `InkMLParser`:

### Prerequisites
(Yet to define)

- Python 3.x
- Required libraries (list any required libraries or dependencies)

### Installation
(Yet to define)

1. Clone this repository.
2. Install any required libraries using `pip install -r requirements.txt` (if applicable).

## Usage

Here's how you can use the `InkMLParser` in your Python project:

```python
from InkMLParser import InkMLParser

# Initialize the parser with the path to your INKML file
parser = InkMLParser('path_to_your_file.inkml')

# Access parsed data
data = parser.get_data()

# Use the data as needed
print(data['UI'])
print(data['Annotation'])
print(data['TraceData'])
print(data['SymbolsData'])
