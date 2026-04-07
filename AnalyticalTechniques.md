Based on the course slides provided, here is a comprehensive list of the mathematical, statistical, and analytical techniques that can be applied to a dataset, categorized by their function:

### 1. Descriptive Statistics (Measures of Central Tendency & Dispersion)
These techniques summarize the basic features of a dataset[cite: 242]:
* **Mean (Arithmetic Average):** Calculating the population mean ($\mu$) or sample mean ($\overline{x}$)[cite: 136, 138].
* **Median:** Identifying the "middle" value that separates the higher half from the lower half of the data[cite: 144, 146].
* **Mode:** Finding the most frequent value(s) in a dataset (unimodal, bimodal, or multimodal) [cite: 150-154].
* **Range:** Calculating the difference between the highest and lowest values[cite: 202, 203].
* **Variance:** Measuring the spread of the data for both populations ($\sigma^2$) and samples ($s^2$) [cite: 205-208].
* **Standard Deviation:** Calculating the square root of the variance to understand data spread in original units[cite: 212, 213].
* **Percentiles and Quartiles:** Identifying values below which a certain percentage of data falls (e.g., $Q1$, $Q2$/Median, $Q3$)[cite: 232, 237].
* **Interquartile Range (IQR):** Calculating the range between the third and first quartiles ($Q3 - Q1$)[cite: 238].
* **Five-Number Summary:** Compiling the Minimum, $Q1$, Median, $Q3$, and Maximum [cite: 243, 244-248].

### 2. Data Visualization & Graphical Summaries
These techniques are used to visually explore data distributions and relationships:
* **Aesthetic Mapping:** Using position, shape, size, color, line width, and line type to represent variables[cite: 450].
* **Coordinate Systems:** Utilizing Cartesian or Polar coordinates for 2D visualization [cite: 526, 774-775].
* **Bar Plots:** Visualizing amounts, including simple, grouped, and stacked variations[cite: 809, 970].
* **Histograms:** Visualizing the distribution of continuous data by dividing it into bins[cite: 1150, 1193].
* **Kernel Density Estimates (Density Plots):** Creating smoothed curves to visualize distributions[cite: 1205, 1277].
* **Box Plots:** Visualizing the Five-Number Summary and detecting outliers[cite: 252, 283, 1696].
* **Scatter Plots:** Treating pairs of values as coordinates to see clusters and outliers[cite: 1383, 1385].
* **Heatmaps:** Using color to represent magnitudes in a 2D grid[cite: 810].
* **Age Pyramids:** Specialized visualization for comparing distributions between two groups (e.g., gender)[cite: 1357].

### 3. Correlation & Covariance (Bivariate Analysis)
These techniques explore the relationship between two variables:
* **Sample Covariance:** Calculating the formal measure of how two continuous features change together [cite: 1728-1730].
* **Correlation Coefficient:** Calculating a normalized form of covariance that ranges between $-1$ and $+1$ to determine the strength and direction of a linear relationship [cite: 1738-1740].
* **Covariance/Correlation Matrices:** Tools for exploring relationships between multiple continuous features simultaneously[cite: 1752, 1754, 1757].

### 4. Inferential Statistics & Hypothesis Testing
These techniques allow for making inferences about a population based on a sample:
* **1-Sample t-Test:** Determining if a sample mean differs significantly from a known population mean[cite: 27].
* **1-Sample Proportion Test:** Testing if a sample proportion differs from a known population proportion[cite: 39].
* **Two-Sample t-Test:** Comparing means between two independent groups[cite: 52].
* **Paired t-Test:** Comparing means between two dependent/paired samples (e.g., pre/post analysis)[cite: 63, 69].
* **A/B Testing:** Controlled experiments comparing two versions (A and B) to determine which performs better[cite: 75].
* **Confidence Intervals:** Calculating a range of values likely to contain a population parameter at a specified confidence level (e.g., 95%)[cite: 1974, 1975, 1991].

### 5. Probability Analysis
These techniques model the likelihood of various outcomes:
* **Combinatorial Analysis:** Using permutations (order matters) and combinations (order does not matter) for counting possibilities[cite: 2016, 2033].
* **Conditional Probability:** Determining the probability of an event occurring given that another event has already occurred ($P(A|B)$)[cite: 2103].
* **Bayes' Theorem:** Calculating updated probabilities based on prior knowledge of related conditions[cite: 2157, 2158].
* **Probability Distributions:** Applying specific models based on data type, including **Bernoulli**, **Binomial**, **Poisson**, **Geometric**, **Normal (Gaussian)**, **Uniform**, **Exponential**, and **Student’s t-Distribution**[cite: 2219, 2220].

### 6. Analytical Theorems & Principles
Theoretical tools used to validate data findings:
* **Law of Large Numbers (LLN):** The principle that sample means approach the expected value as the number of trials increases[cite: 1887].
* **Chebyshev's Inequality:** Predicting probability bounds (the proportion of data within $k$ standard deviations of the mean) for any dataset, regardless of its distribution[cite: 1914, 1930, 1934].