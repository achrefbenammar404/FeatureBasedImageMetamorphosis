# Feature-Based Image Metamorphosis (Variation)

## Visual Demonstration

![Feature Based Image Metamorphosis](Image/image.png)

This repository contains an implementation of a variation of the **Feature-Based Image Metamorphosis** algorithm, inspired by the research paper ["Feature-Based Image Metamorphosis"](https://dl.acm.org/doi/10.1145/133994.134003) by Thaddeus Beier and Shawn Neely (1992). The variation is designed for use with a single image and a set of coupled vectors, enabling creative and unique image transformations.

---

## Algorithm Overview

Feature-based image metamorphosis is a geometric warping technique that uses a set of **line pairs** (corresponding features) to guide the transformation of an image. The transformation involves two main steps:
1. **Warping the image based on feature lines.**
2. **Interpolating between source and target images using a blend factor.**

### Core Warping Formula

Given:
- A source image $I_s$.
- A target image $I_t$.
- A set of feature lines in the source image $\{(P_i, Q_i)\}$.
- Corresponding feature lines in the target image $\{(P'_i, Q'_i)\}$.
- A blending factor $t \in [0, 1]$.

#### Step 1: Compute Per-Pixel Warp

Each pixel $X$ in the destination image is mapped back to the source image using a weighted sum of transformations induced by all feature line pairs. The warping function is defined as:

$$
X_s = X + \sum_{i=1}^N \text{weight}_i \cdot \text{displacement}_i
$$

Where:
- $\text{displacement}_i = \frac{\overrightarrow{X'P'_i} \cdot \overrightarrow{Q'_iP'_i}}{\|\overrightarrow{Q'_iP'_i}\|^2} \cdot \overrightarrow{Q_iP_i} + \frac{\overrightarrow{X'Q'_i} \cdot \overrightarrow{Q'_iP'_i}}{\|\overrightarrow{Q'_iP'_i}\|^2} \cdot \overrightarrow{P_iQ_i}$.

- $\text{weight}_i = \frac{\|Q'_iP'_i\|^p}{(a + \text{distance}(X', L'_i))^b}$, where:
  - $L'_i$ is the line defined by $P'_i, Q'_i$.
  - $p$, $a$, and $b$ are user-defined constants controlling the smoothness and influence of the transformation.

#### Step 2: Blend Images

The pixel intensities in the final output image are computed as a linear interpolation between the source and target images:

$$
I(X) = (1 - t) \cdot I_s(X_s) + t \cdot I_t(X_t)
$$

Where $t$ controls the blending ratio between the source and target images.

---

## Usage

Refer to the [How to Use Notebook](HowToUse.ipynb) for detailed instructions on applying the Feature-Based Image Metamorphosis algorithm with a single image and coupled vectors.

---

## Implementation Details

- **`ImageMorphism.py`**: Core implementation of the Feature-Based Image Metamorphosis algorithm variation.
- **`Line.py`**: Definition of a class later needed in the algorithm.
- **`How_to_Use.ipynb`**: Jupyter Notebook providing a step-by-step guide to using the algorithm.

---

## Requirements

Ensure you have the following dependencies installed:

- **Python 3.x**
- Required Python packages (listed in `requirements.txt`).

---

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/achrefbenammar404/FeatureBasedImageMetamorpohosis.git
   cd FeatureBasedImageMetamorphosis
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Refer to the **`How_to_Use.ipynb`** notebook for instructions on using the algorithm.

---

## Mathematical Insights

### Influence of Parameters
- **Line Pair Influence**: The parameters $p$, $a$, and $b$ allow fine-tuning of how much each line pair affects the pixels. Increasing $p$ reduces the influence of distant lines, while larger $b$ sharpens the transformation near the line.
- **Blending Factor $t$**: Controls the interpolation between the source and target image. A value of $t = 0$ results in the source image, while $t = 1$ gives the target image.

### Smoothness and Complexity
The algorithm handles smooth warping by adjusting weights dynamically for every pixel. However, the computational complexity grows with the number of feature lines and image resolution.

---

## Contributing

If you encounter issues or have suggestions, feel free to:

- Open an issue.
- Submit a pull request.

---

## References

This implementation is inspired by the following paper:

- Thaddeus Beier and Shawn Neely, [**"Feature-Based Image Metamorphosis"**](https://dl.acm.org/doi/10.1145/133994.134003), Proceedings of SIGGRAPH '92, ACM, 1992.  

The algorithm adapts concepts from the original research to support single images and coupled vector transformations for enhanced creative flexibility.
