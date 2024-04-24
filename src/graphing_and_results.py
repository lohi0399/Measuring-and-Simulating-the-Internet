import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Gaphing for box and bar plots
# Uncomment what is neccessary while graphing


# Create a mock dataset based on the boxplot provided
# np.random.seed(0) # for reproducibility
# websites = ['Website Emissions.com', 'Website Carbon', 'EcoGrader', 'Digital Beacon']
# avg_co2 = [1.5, 2, 1, 1.8] # mean CO2 values as interpreted from the graph
# sd_co2 = [0.2, 0.5, 0.3, 0.4] # standard deviation values as interpreted from the graph


# # Create samples for each website
# data = {}
# for website, mean, sd in zip(websites, avg_co2, sd_co2):
#     data[website] = np.random.normal(mean, sd, n_samples)

# # Convert to a DataFrame for easier handling
# df = pd.DataFrame(data)

# # Add an 'amp' column that will hold whether the website is AMP or non-AMP
# # 'Website Carbon' and 'EcoGrader' are better with AMP according to user instructions
# df['amp'] = ['AMP' if website in ['Website Carbon', 'EcoGrader'] else 'non-AMP' for website in df.columns[:-1]]
# df_long = pd.melt(df, id_vars=['amp'], var_name='Website', value_name='CO2')

# # Save the dataframe to a csv file
# csv_file_path = '/mnt/data/final_co2_data.csv'
# df_long.to_csv(csv_file_path, index=False)

# csv_file_path, df_long.head()




# # Separate the AMP and non-AMP websites
# amp_data = df_combined[df_combined['amp'] == 'AMP']
# non_amp_data = df_combined[df_combined['amp'] == 'non-AMP']

# # Create a new DataFrame to hold the comparison data
# comparison_data = {
#     'Website': amp_data['Website'].unique(),
#     'AMP': [amp_data[amp_data['Website'] == website]['CO2'].mean() for website in amp_data['Website'].unique()],
#     'non-AMP': [non_amp_data[non_amp_data['Website'] == website]['CO2'].mean() for website in non_amp_data['Website'].unique()]
# }
# comparison_df = pd.DataFrame(comparison_data)

# # Plotting the comparison data
# plt.figure(figsize=(10, 6))
# comparison_df.set_index('Website').plot(kind='bar', stacked=False)
# plt.title('Average CO2 Emissions for AMP vs non-AMP Websites')
# plt.ylabel('Average g of CO2 per Page View')
# plt.xlabel('Emission Calculator Website')
# plt.xticks(rotation=45)
# plt.legend(title='Page Type')
# plt.grid(axis='y')
# plt.tight_layout()
# plt.show()

#----------------------------------------------------------------------------------------------#

# Final result estimation

# emissions_data = {
#     'Website Emissions.com': {'AMP': 1.7, 'non-AMP': 2.0},
#     'Website Carbon': {'AMP': 0.8, 'non-AMP': 1.3},
#     'EcoGrader': {'AMP': 0.7, 'non-AMP': 1.9},
#     'Digital Beacon': {'AMP': 1.5, 'non-AMP': 1.8}
# }

# # Calculate the differences
# differences = {calculator: data['non-AMP'] - data['AMP'] for calculator, data in emissions_data.items()}

# # Calculate the average reduction
# average_reduction = np.mean(list(differences.values()))

# average_reduction, differences

