import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Get the directory where the script is located
directory = os.path.dirname(os.path.abspath(__file__))

# Output file for the aggregated analysis
output_file = os.path.join(directory, 'aggregated_genre_analysis.csv')

# Define the numeric columns globally
numeric_columns = ['betweenness', 'degree', 'closeness', 'pagerank', 'eigenvector', 'clustering_coeffs']

def analyze_all_csvs(directory):
    """
    Analyze all CSV files in the directory and perform a comparative analysis across genres.
    Returns a DataFrame with aggregated statistics.
    """
    all_data = []

    # Iterate over all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv') and filename.startswith('sub_genre_'):
            sub_genre = filename.split('_')[2]  # Extract the sub-genre from the filename
            file_path = os.path.join(directory, filename)

            try:
                print(f"Processing file: {filename}")

                # Load the CSV with the correct separator
                df = pd.read_csv(file_path, sep=';')
                print(f"Loaded file: {filename} with shape {df.shape}")
                print(f"Columns in {filename}: {df.columns.tolist()}")

                # Validate required columns
                missing_columns = [col for col in numeric_columns if col not in df.columns]
                if missing_columns:
                    raise ValueError(f"Missing columns {missing_columns} in {filename}")

                # Add the sub-genre as a new column
                df['sub_genre'] = sub_genre

                # Append to the list of all data
                all_data.append(df)
                print(f"Successfully processed {len(df)} rows from {filename}.")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if not all_data:
        raise ValueError("No valid data loaded. Ensure the directory contains correctly formatted files.")

    # Combine all data into a single DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)

    # Ensure numeric columns are properly parsed
    for col in numeric_columns:
        combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')

    # Drop rows with missing values in numeric columns
    combined_df = combined_df.dropna(subset=numeric_columns)

    if combined_df.empty:
        raise ValueError("No valid numeric data available after cleaning. Ensure the files contain numeric metrics.")

    return combined_df

def generate_statistics_and_plots(combined_df):
    """
    Generate summary statistics and visualizations for the genres.
    """
    # Group by sub-genre and calculate summary statistics
    aggregated_stats = combined_df.groupby('sub_genre')[numeric_columns].agg(['mean', 'std', 'min', 'max', 'median'])

    # Save aggregated statistics to CSV
    aggregated_stats.to_csv(output_file)
    print(f"Aggregated analysis complete. Report saved to {output_file}.")

    # Loop through each numeric column and create boxplots
    for col in numeric_columns:
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='sub_genre', y=col, data=combined_df)
        plt.title(f'Comparison of {col.capitalize()} by Genre')
        plt.xticks(rotation=90)
        plt.show()

    # Correlation heatmap of metrics
    correlation_matrix = combined_df[numeric_columns].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix of Network Metrics')
    plt.show()

    # Pairplot for visual comparison of the metrics
    sns.pairplot(combined_df[numeric_columns + ['sub_genre']], hue='sub_genre', diag_kind='kde', markers='o')
    plt.show()

def main():
    try:
        # Perform the analysis
        combined_df = analyze_all_csvs(directory)

        # Generate summary statistics and visualizations
        generate_statistics_and_plots(combined_df)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
