### 1. Descriptive Statistics (Measures of Central Tendency & Dispersion)
These techniques summarize the basic features of a dataset:
* **Mean (Arithmetic Average):** Calculating the population mean ($\mu$) or sample mean ($\overline{x}$).
* **Median:** Identifying the "middle" value that separates the higher half from the lower half of the data.
* **Mode:** Finding the most frequent value(s) in a dataset (unimodal, bimodal, or multimodal).
* **Range:** Calculating the difference between the highest and lowest values.
* **Variance:** Measuring the spread of the data for both populations ($\sigma^2$) and samples ($s^2$).
* **Standard Deviation:** Calculating the square root of the variance to understand data spread in original units.
* **Percentiles and Quartiles:** Identifying values below which a certain percentage of data falls (e.g., $Q1$, $Q2$/Median, $Q3$).
* **Interquartile Range (IQR):** Calculating the range between the third and first quartiles ($Q3 - Q1$).
* **Five-Number Summary:** Compiling the Minimum, $Q1$, Median, $Q3$, and Maximum.

### 2. Data Visualization & Graphical Summaries
These techniques are used to visually explore data distributions and relationships:
* **Aesthetic Mapping:** Using position, shape, size, color, line width, and line type to represent variables.
* **Coordinate Systems:** Utilizing Cartesian or Polar coordinates for 2D visualization.
* **Bar Plots:** Visualizing amounts, including simple, grouped, and stacked variations.
* **Histograms:** Visualizing the distribution of continuous data by dividing it into bins.
* **Kernel Density Estimates (Density Plots):** Creating smoothed curves to visualize distributions.
* **Box Plots:** Visualizing the Five-Number Summary and detecting outliers.
* **Scatter Plots:** Treating pairs of values as coordinates to see clusters and outliers.
* **Heatmaps:** Using color to represent magnitudes in a 2D grid.
* **Age Pyramids:** Specialized visualization for comparing distributions between two groups (e.g., gender).

### 3. Correlation & Covariance (Bivariate Analysis)
These techniques explore the relationship between two variables:
* **Sample Covariance:** Calculating the formal measure of how two continuous features change together.
* **Correlation Coefficient:** Calculating a normalized form of covariance that ranges between $-1$ and $+1$ to determine the strength and direction of a linear relationship.
* **Covariance/Correlation Matrices:** Tools for exploring relationships between multiple continuous features simultaneously.

### 4. Inferential Statistics & Hypothesis Testing
These techniques allow for making inferences about a population based on a sample:
* **1-Sample t-Test:** Determining if a sample mean differs significantly from a known population mean.
* **1-Sample Proportion Test:** Testing if a sample proportion differs from a known population proportion.
* **Two-Sample t-Test:** Comparing means between two independent groups.
* **Paired t-Test:** Comparing means between two dependent/paired samples (e.g., pre/post analysis).
* **A/B Testing:** Controlled experiments comparing two versions (A and B) to determine which performs better.
* **Confidence Intervals:** Calculating a range of values likely to contain a population parameter at a specified confidence level (e.g., 95%).

### 5. Probability Analysis
These techniques model the likelihood of various outcomes:
* **Combinatorial Analysis:** Using permutations (order matters) and combinations (order does not matter) for counting possibilities.
* **Conditional Probability:** Determining the probability of an event occurring given that another event has already occurred ($P(A|B)$).
* **Bayes' Theorem:** Calculating updated probabilities based on prior knowledge of related conditions.
* **Probability Distributions:** Applying specific models based on data type, including **Bernoulli**, **Binomial**, **Poisson**, **Geometric**, **Normal (Gaussian)**, **Uniform**, **Exponential**, and **Student’s t-Distribution**.

### 6. Analytical Theorems & Principles
Theoretical tools used to validate data findings:
* **Law of Large Numbers (LLN):** The principle that sample means approach the expected value as the number of trials increases.
* **Chebyshev's Inequality:** Predicting probability bounds (the proportion of data within $k$ standard deviations of the mean) for any dataset, regardless of its distribution.