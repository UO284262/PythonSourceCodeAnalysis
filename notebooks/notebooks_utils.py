import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
from matplotlib import pyplot
from statsmodels.stats.stattools import medcouple
import math
import numpy as np
import sys
import os
import dataset.db.db_utils as db_utils
from numpy import inf

# Database connection properties
DB_CONNECTION_STR = f"postgresql://{db_utils.connection_string['user']}:{db_utils.connection_string['password']}@{db_utils.connection_string['host']}:{db_utils.connection_string['port']}/{db_utils.connection_string['dbname']}"

# Directory to store the results.
RESULTS_FOLDER_DIR = './results'
if not os.path.exists(RESULTS_FOLDER_DIR):
    os.makedirs(RESULTS_FOLDER_DIR)


# To detect columns with empty non-null values, we will define the following formula.
def print_empty_cols(df):
    for col in df.columns:
        print(col)
        print('-' * len(col))
        res = df[df[col] == ''].index
        print(f"{len(res)} instancias no tienen un valor para la columna {col}")
        if len(res) > 0:
            print(res)
        print('\n')


def get_percentage(e):
    return e[1]


# Frequency analysis of the values of a categorical variable
def print_frequency_anal_for_cat_var(df, column_name, possible_values=[], outlier_threshold=0.2):
    unique_values = df[column_name].unique().tolist()
    unique_values = list(set(unique_values) | set(possible_values))
    #unique_values = unique_values.union(possible_values)
    unique_values_count = len(unique_values)
    threshold = outlier_threshold / unique_values_count
    print(f'La variable {column_name} contiene {unique_values_count} valores distintos.')
    print(f'El umbral de outlier es de {threshold}%')
    total_number_of_items = len(df[column_name])
    values_and_percentages = []
    for value in unique_values:
        val_count = len(df[df[column_name] == value].index)
        val_count_percentage = val_count / total_number_of_items * 100
        is_outlier = val_count_percentage < threshold
        values_and_percentages.append((value, val_count_percentage, is_outlier))

    values_and_percentages.sort(reverse=True, key=get_percentage)
    for value in values_and_percentages:
        if value[2]:
            print(f'La variable {column_name} toma el valor de {value[0]} en un {value[1]:.4}% de los items. [OUTLIER]')
        else:
            print(f'La variable {column_name} toma el valor de {value[0]} en un {value[1]:.4}% de los items.')


def print_outliers_for_df_column(df, column_name, weak_coefficient=1.5, strong_coefficient=3.0):
    column_dataframe = df[column_name].describe()
    column_np_array = np.array(column_dataframe)
    q1 = column_dataframe['25%']
    q3 = column_dataframe['75%']
    iqr = q3 - q1
    mc = medcouple(column_np_array)
    print(f'El coeficiente MC (Medcouple Coefficient) de balanceo es: {mc}')
    low_strong_iqr_lmt = q1 - strong_coefficient * iqr
    low_weak_iqr_lmt = q1 - weak_coefficient * iqr
    high_weak_iqr_lmt = q3 + weak_coefficient * iqr
    high_strong_iqr_lmt = q3 + strong_coefficient * iqr
    print(f"Rango valores atípicos extremos (Tukey): [{low_strong_iqr_lmt},{high_strong_iqr_lmt}]")
    print(f"Rango valores atípicos leves (Tukey): [{low_weak_iqr_lmt},{high_weak_iqr_lmt}]")

    if mc < 0.0:
        low = (q1-1.5 * math.exp(-4*mc) * iqr)
        high = (q3+1.5 * math.exp(3.5*mc) * iqr)
    else:
        low = (q1-1.5 * math.exp(-3.5*mc) * iqr)
        high = (q3+1.5 * math.exp(4*mc) * iqr)

    print(f"Rango valores atípicos extremos (Fixed BoxPlot): [{low},{high}]")
    num_low_strong_outliers = len(df[df[column_name] < low_strong_iqr_lmt].index)
    num_low_weak_outliers = len(df[df[column_name] < low_weak_iqr_lmt].index)
    num_high_weak_outliers = len(df[df[column_name] > high_weak_iqr_lmt].index)
    num_high_strong_outliers = len(df[df[column_name] > high_strong_iqr_lmt].index)

    num_low_strong_outliers_pct = num_low_strong_outliers / len(df[column_name]) * 100
    num_low_weak_outliers_pct = num_low_weak_outliers / len(df[column_name]) * 100
    num_high_weak_outliers_pct = num_high_weak_outliers / len(df[column_name]) * 100
    num_high_strong_outliers_pct = num_high_strong_outliers / len(df[column_name]) * 100

    num_low_out_ad_boxplot = len(df[df[column_name] < low].index)
    num_high_out_ad_boxplot = len(df[df[column_name] > high].index)
    num_low_out_ad_boxplot_pct = num_low_out_ad_boxplot / len(df[column_name]) * 100
    num_high_out_ad_boxplot_pct = num_high_out_ad_boxplot / len(df[column_name]) * 100

    print(f'-3.0IQR: {num_low_strong_outliers} instancias tienen un valor para {column_name} inferior a {low_strong_iqr_lmt} (Q1-3*IQR) para {column_name}. Representando un {num_low_strong_outliers_pct:.4}% del total de instancias.')
    print(f'-1.5IQR: {num_low_weak_outliers} instancias tienen un valor para {column_name} inferior a {low_weak_iqr_lmt} (Q1-1.5*IQR) para {column_name}. Representando un {num_low_weak_outliers_pct:.4}% del total de instancias.')
    print(f'+1.5IQR: {num_high_weak_outliers} instancias tienen un valor para {column_name} superior a {high_weak_iqr_lmt} (Q3+1.5*IQR) para {column_name}. Representando un {num_high_weak_outliers_pct:.4}% del total de instancias.')
    print(f'+3.0IQR: {num_high_strong_outliers} instancias tienen un valor para {column_name} superior a {high_strong_iqr_lmt} (Q3-3*IQR) para {column_name}. Representando un {num_high_strong_outliers_pct:.4}% del total de instancias.')

    print(f'L: {num_low_out_ad_boxplot} instancias tienen un valor para {column_name} inferior a {low} para {column_name}. Representando un {num_low_out_ad_boxplot_pct:.4}% del total de instancias.')
    print(f'U: {num_high_out_ad_boxplot} instancias tienen un valor para {column_name} superior a {high} para {column_name}. Representando un {num_high_out_ad_boxplot_pct:.4}% del total de instancias.')


def print_frequency_anal_for_num_var(df, column_name):
    sns.boxplot(df[column_name])
    print_outliers_for_df_column(df, column_name)


def get_statistics(df, columns, size):
    total = len(df.index)
    result = df.groupby(columns) \
        .size() \
        .reset_index(name='count') \
        .sort_values(['count'], ascending=False) \
        .head(size)
    result['percentage'] = (result['count'] * 100) / total
    return result.to_string(index=False) + '\n'


def get_bin(bins, value):
    for x, y in bins:
        if value >= x:
            if value == x and value == y:
                return "[" + str(x) + "_" + str(y) + "]"
            if value < y:
                return "[" + str(x) + "_" + str(y) + ("]" if y == inf else ")")
    return "unknown"


def create_bins(df, column, bins):
    return df[column].apply(lambda value: get_bin(bins, value))


def discretize_columns(df, columns):
    for k in columns:
        df[k] = create_bins(df, k, columns[k])
