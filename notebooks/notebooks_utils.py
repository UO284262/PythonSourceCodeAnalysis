import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from statsmodels.stats.stattools import medcouple
import sys
import os
from sklearn.preprocessing import RobustScaler
import dataset.db.db_utils as db_utils
from numpy import inf
import pickle
from datetime import datetime
import sqlalchemy
import numpy as np
from scipy.stats import gaussian_kde
from IPython.display import display
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split
from scipy.stats import kruskal
from scikit_posthocs import posthoc_dunn

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
        if value is None:
            val_count = df[column_name].isna().sum()
        else:
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


def print_values_usage_for_cat_var(df, column_name, possible_values=[]):
    unique_values = df[column_name].unique().tolist()
    unused_values = list(set(possible_values) - set(unique_values))
    unknown_values = list(set(unique_values) - set(possible_values))
    possible_values_count = len(possible_values)
    unique_values_count = len(unique_values)
    unused_values_count = len(unused_values)
    print(f'La variable {column_name} puede tomar {possible_values_count} valores distintos')
    print(f'\t{unique_values_count} ({((unique_values_count * 100) / possible_values_count):.4}%) valores utilizados')
    print(
        f'\t{unused_values_count} ({((unused_values_count * 100) / possible_values_count):.4}%) valores NO utilizados')
    for value in unused_values:
        print(f'\t\tLa variable {column_name} nunca toma valor {value}.')
    if len(unknown_values) > 0:
        print(f'La variable {column_name} toma {len(unknown_values)} valores desconocidos')
        for value in unknown_values:
            print(f'\t\tLa variable {column_name} toma valor el desconocido {value}.')


"""
def print_outliers_for_df_column2(df, column_name, weak_coefficient=1.5, strong_coefficient=3.0):

    column_dataframe = df[column_name].describe()
    column_np_array = np.array(column_dataframe)
    q1 = column_dataframe['25%']
    q3 = column_dataframe['75%']
    iqr = q3 - q1
    mc = medcouple(column_np_array)
    print(f'El coeficiente MC (Medcouple Coefficient) de balanceo es: {mc}')
    print('Dependiendo del coeficiente de MC se deben tomar unos límites u otros:')
    print('     |MC| < 0.3    ->  Tukey')
    print('     |MC| >=  0.3  ->  MAD')
    low_strong_iqr_lmt = q1 - strong_coefficient * iqr
    high_strong_iqr_lmt = q3 + strong_coefficient * iqr
    low_weak_iqr_lmt = q1 - weak_coefficient * iqr
    high_weak_iqr_lmt = q3 + weak_coefficient * iqr
    print(f"Rango valores atípicos extremos (Tukey): [{low_strong_iqr_lmt},{high_strong_iqr_lmt}]")
    print(f"Rango valores atípicos leves (Tukey): [{low_weak_iqr_lmt},{high_weak_iqr_lmt}]")


    if mc < 0.0:
        low = (q1-1.5 * math.exp(-4*mc) * iqr)
        high = (q3+1.5 * math.exp(3.5*mc) * iqr)
    else:
        low = (q1-1.5 * math.exp(-3.5*mc) * iqr)
        high = (q3+1.5 * math.exp(4*mc) * iqr)

    print(f"Rango valores atípicos extremos (Fixed BoxPlot): [{low},{high}]")
    
    k = 3
    median = np.median(column_np_array)
    mad = np.median(np.abs(column_np_array - median))
    mad_lower_limit = median - (k * mad)
    mad_upper_limit = median + (k * mad)
    print(f"Rango valores atípicos MAD (Median Absolute Deviation): [{mad_lower_limit},{mad_upper_limit}]")
    
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

    num_low_mad_outliers = len(df[df[column_name] < mad_lower_limit].index)
    num_high_mad_outliers = len(df[df[column_name] > mad_upper_limit].index)
    num_low_mad_outliers_pct = num_low_mad_outliers / len(df[column_name]) * 100
    num_high_mad_outliers_pct = num_high_mad_outliers / len(df[column_name]) * 100

    print(f'-3.0IQR: {num_low_strong_outliers} instancias tienen un valor para {column_name} inferior a {low_strong_iqr_lmt} (Q1-3*IQR) para {column_name}. Representando un {num_low_strong_outliers_pct:.4}% del total de instancias.')
    print(f'-1.5IQR: {num_low_weak_outliers} instancias tienen un valor para {column_name} inferior a {low_weak_iqr_lmt} (Q1-1.5*IQR) para {column_name}. Representando un {num_low_weak_outliers_pct:.4}% del total de instancias.')
    print(f'+1.5IQR: {num_high_weak_outliers} instancias tienen un valor para {column_name} superior a {high_weak_iqr_lmt} (Q3+1.5*IQR) para {column_name}. Representando un {num_high_weak_outliers_pct:.4}% del total de instancias.')
    print(f'+3.0IQR: {num_high_strong_outliers} instancias tienen un valor para {column_name} superior a {high_strong_iqr_lmt} (Q3-3*IQR) para {column_name}. Representando un {num_high_strong_outliers_pct:.4}% del total de instancias.')

    print(f'L: {num_low_out_ad_boxplot} instancias tienen un valor para {column_name} inferior a {low} para {column_name}. Representando un {num_low_out_ad_boxplot_pct:.4}% del total de instancias.')
    print(f'U: {num_high_out_ad_boxplot} instancias tienen un valor para {column_name} superior a {high} para {column_name}. Representando un {num_high_out_ad_boxplot_pct:.4}% del total de instancias.')

    print(f'MAD Inferior: {num_low_mad_outliers} instancias tienen un valor para {column_name} inferior a {mad_lower_limit} para {column_name}. Representando un {num_low_mad_outliers_pct:.4}% del total de instancias.')
    print(f'MAD Superior: {num_high_mad_outliers} instancias tienen un valor para {column_name} superior a {mad_upper_limit} para {column_name}. Representando un {num_high_mad_outliers_pct:.4}% del total de instancias.')
"""


def print_outliers_for_df_column(df, column_name, weak_coefficient=1.5, strong_coefficient=3.0):
    column_dataframe = df[column_name].describe()
    column_np_array = np.array(column_dataframe)
    q1 = column_dataframe['25%']
    q3 = column_dataframe['75%']
    iqr = q3 - q1
    mc = medcouple(column_np_array)
    print(f'El coeficiente MC (Medcouple Coefficient) de balanceo es: {mc}')
    print('Dependiendo del coeficiente de MC se deben tomar unos límites u otros:')
    print('     |MC| < 0.3    ->  Tukey')
    print('     |MC| >=  0.3  ->  MAD')
    low_weak_iqr_lmt = q1 - weak_coefficient * iqr
    high_weak_iqr_lmt = q3 + weak_coefficient * iqr
    print(f"Rango valores atípicos leves (Tukey): [{low_weak_iqr_lmt},{high_weak_iqr_lmt}]")

    k = 3
    median = np.median(column_np_array)
    mad = np.median(np.abs(column_np_array - median))
    mad_lower_limit = median - (k * mad)
    mad_upper_limit = median + (k * mad)
    print(f"Rango valores atípicos MAD (Median Absolute Deviation): [{mad_lower_limit},{mad_upper_limit}]")

    num_low_weak_outliers = len(df[df[column_name] < low_weak_iqr_lmt].index)
    num_high_weak_outliers = len(df[df[column_name] > high_weak_iqr_lmt].index)
    num_low_weak_outliers_pct = num_low_weak_outliers / len(df[column_name]) * 100
    num_high_weak_outliers_pct = num_high_weak_outliers / len(df[column_name]) * 100

    num_low_mad_outliers = len(df[df[column_name] < mad_lower_limit].index)
    num_high_mad_outliers = len(df[df[column_name] > mad_upper_limit].index)
    num_low_mad_outliers_pct = num_low_mad_outliers / len(df[column_name]) * 100
    num_high_mad_outliers_pct = num_high_mad_outliers / len(df[column_name]) * 100

    print(
        f'-1.5IQR: {num_low_weak_outliers} instancias tienen un valor para {column_name} inferior a {low_weak_iqr_lmt} (Q1-1.5*IQR) para {column_name}. Representando un {num_low_weak_outliers_pct:.4}% del total de instancias.')
    print(
        f'+1.5IQR: {num_high_weak_outliers} instancias tienen un valor para {column_name} superior a {high_weak_iqr_lmt} (Q3+1.5*IQR) para {column_name}. Representando un {num_high_weak_outliers_pct:.4}% del total de instancias.')

    print(
        f'MAD Inferior: {num_low_mad_outliers} instancias tienen un valor para {column_name} inferior a {mad_lower_limit} para {column_name}. Representando un {num_low_mad_outliers_pct:.4}% del total de instancias.')
    print(
        f'MAD Superior: {num_high_mad_outliers} instancias tienen un valor para {column_name} superior a {mad_upper_limit} para {column_name}. Representando un {num_high_mad_outliers_pct:.4}% del total de instancias.')

    if np.abs(mc) > 0.3:
        print("")
        print(f"Con un MC de {mc} utilizamos MAD.")
        print(f"Se consideran anómalos los valores superiores a {mad_upper_limit} o inferiores a {mad_lower_limit}")
        print("Describimos los valores de las variables de la tabla, cuando el valor de la variable es anómalo")
        outlier_df = df[(df[column_name] > mad_upper_limit) | (df[column_name] < mad_lower_limit)]
    else:
        print("")
        print(f"Con un MC de {mc} utilizamos Tukey.")
        print(f"Se consideran anómalos los valores superiores a {high_weak_iqr_lmt} o inferiores a {low_weak_iqr_lmt}")
        print("Describimos los valores de las variables de la tabla, cuando el valor de la variable es anómalo")
        outlier_df = df[(df[column_name] > high_weak_iqr_lmt) | (df[column_name] < low_weak_iqr_lmt)]

    if 'ipykernel' in sys.modules:  # Verificar si se ejecuta en Jupyter Notebook
        display(outlier_df.describe(percentiles=[.25, .50, .75], include=['object', 'float', 'bool', 'int']))
    else:
        print(outlier_df.describe(percentiles=[.25, .50, .75], include=['object', 'float', 'bool', 'int']))


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


def get_data(table: str, use_cache=True) -> pd.DataFrame:
    table_file = f'.{os.sep}cache{os.sep}{table}.pk'
    if use_cache and os.path.exists(table_file):
        print(datetime.now(), 'Data cache files found ...')
        with open(table_file, 'rb') as handle:
            full_table = pickle.load(handle)
        print(datetime.now(), 'Data cache files successfully loaded!!')
        return full_table
    else:
        full_table = load_data(table)
        print(datetime.now(), 'Creating data cache files ...')
        with open(file=f'.{os.sep}cache{os.sep}{table}.pk', mode='wb') as handle:
            pickle.dump(full_table, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(datetime.now(), 'Data cache files successfully created!!')
        return full_table


def load_data(table: str) -> pd.DataFrame:
    print(datetime.now(), 'Loading data ...')
    db_connection = sqlalchemy.create_engine(DB_CONNECTION_STR)
    sql_query = open(file=f'.{os.sep}queries{os.sep}{table}.sql', mode='r').read()
    full_table = pd.read_sql_query(sql=sql_query, con=db_connection)
    print(datetime.now(), 'Data successfully load!!')
    return full_table


def print_histogram(data: pd.DataFrame, column: str, expertise_column: str, bins: int = 30, include_all: bool = True,
                    include_beginners: bool = True, include_experts: bool = True, min_value: float = None,
                    max_value: float = None):
    plt.figure(figsize=(12, 6))

    # Filtrar según valores mínimos y máximos
    if min_value is not None:
        data = data[data[column] >= min_value]
    if max_value is not None:
        data = data[data[column] <= max_value]

    data_min = data[column].min()
    data_max = data[column].max()

    # Crear bins
    num_bins = np.linspace(data_min, data_max, bins + 1)

    # Calcular el total de instancias para los porcentajes
    total_count = len(data)

    if include_all:
        counts, _ = np.histogram(data[column], bins=num_bins)
        percentages = counts / total_count * 100
        plt.hist(num_bins[:-1], num_bins, weights=percentages, alpha=0.5, label='All', color='blue')

    if include_experts:
        expert_data = data[data[f'{expertise_column}_PROFESSIONAL'] == 1]
        expert_count = len(expert_data)
        counts, _ = np.histogram(expert_data[column], bins=num_bins)
        if expert_count > 0:
            percentages = counts / expert_count * 100  # Porcentaje en relación a los expertos
            plt.hist(num_bins[:-1], num_bins, weights=percentages, alpha=0.5, label='Professional', color='green')

    if include_beginners:
        beginner_data = data[data[f'{expertise_column}_PROFESSIONAL'] == 0]
        beginner_count = len(beginner_data)
        counts, _ = np.histogram(beginner_data[column], bins=num_bins)
        percentages = counts / beginner_count * 100  # Porcentaje en relación a los principiantes
        plt.hist(num_bins[:-1], num_bins, weights=percentages, alpha=0.5, label='Beginners', color='red')

    # Etiquetas y leyenda
    plt.xlabel(column)
    plt.ylabel('Percentage')
    plt.title(f'{column} by expertise level histogram (Percentage)')
    plt.legend()
    plt.show()


def print_categorical_histogram(
        data: pd.DataFrame,
        column: str,
        expertise_column: str,
        vertical: bool = False,
        fillna: bool = False,
        include_all: bool = True,
        include_beginners: bool = True,
        include_experts: bool = True,
        height: int = 6,
):
    if fillna:
        data[column] = data[column].fillna('None')

    # Crear figura
    plt.figure(figsize=(12, height))

    # Configurar colores para los grupos
    colors = {
        'All': 'blue',
        'Beginners': 'red',
        'Professionals': 'green',
    }

    # Trazar histograma para "All"
    if include_all:
        total_count = len(data)
        counts = data[column].value_counts()
        percentages = counts / total_count * 100
        if vertical:
            plt.bar(percentages.index, percentages, color=colors['All'], alpha=0.5, label='All')
        else:
            plt.barh(percentages.index, percentages, color=colors['All'], alpha=0.5, label='All')

    # Trazar histograma para "Beginners"
    if include_beginners:
        beginner_data = data[data[expertise_column] == 'BEGINNER']
        total_beginners = len(beginner_data)
        if total_beginners > 0:
            counts = beginner_data[column].value_counts()
            percentages = counts / total_beginners * 100
            if vertical:
                plt.bar(percentages.index, percentages, color=colors['Beginners'], alpha=0.5, label='Beginners')
            else:
                plt.barh(percentages.index, percentages, color=colors['Beginners'], alpha=0.5, label='Beginners')

    # Trazar histograma para "Professionals"
    if include_experts:
        expert_data = data[data[expertise_column] == 'PROFESSIONAL']
        total_experts = len(expert_data)
        if total_experts > 0:
            counts = expert_data[column].value_counts()
            percentages = counts / total_experts * 100
            if vertical:
                plt.bar(percentages.index, percentages, color=colors['Professionals'], alpha=0.5, label='Professionals')
            else:
                plt.barh(percentages.index, percentages, color=colors['Professionals'], alpha=0.5,
                         label='Professionals')

    # Ajustar orientación
    if vertical:
        plt.xticks(rotation=90)
        plt.ylabel('Percentage')
    else:
        plt.xlabel('Percentage')
        plt.ylabel(column)

    # Agregar título y leyenda
    plt.title(f'{column} Distribution by Expertise Level')
    plt.legend()
    plt.tight_layout()
    plt.show()


def detect_outliers_kde(dataframe: pd.DataFrame, column, percentile: float):
    # Ajustar la KDE
    series = dataframe[column]

    # Ajustar la KDE
    kde = gaussian_kde(series)
    x_grid = np.linspace(series.min(), series.max(), 1000)
    density = kde(x_grid)

    # Calcular umbral inferior basado en percentil
    lower_threshold = np.percentile(density, percentile * 100)

    # Detectar outliers solo en regiones de baja densidad
    density_values = kde(series)
    outliers_mask = density_values < lower_threshold

    # Verificar si se han detectado outliers
    print(f"Umbral de outliers: valores con densidad menor que {lower_threshold:.6f}")
    if any(outliers_mask):
        # Mostrar porcentaje de outliers
        outlier_percentage = (outliers_mask.sum() / len(series)) * 100
        print(f"Porcentaje de valores detectados como outliers: {outlier_percentage:.2f}%")
    else:
        print("No se detectaron outliers con el umbral dado.")

    return pd.Series(outliers_mask, index=series.index)


def plot_clusters(X: np.array, clusters: np.array, title1: str) -> None:
    """
    Plot the clusters (left) in a 2D space using t-SNE.
    The colors of the points represent the cluster labels.
    :param X: the dataset
    :param clusters: the cluster labels
    :param title1: title for the clusters plot
    """
    # Reduce the features to 2D using t-SNE
    tsne = TSNE(n_components=2, random_state=42)
    X_tsne = tsne.fit_transform(X)

    # Define colors for each cluster
    colors = {0: 'blue', 1: 'orange', 2: 'green'}
    labels = {0: 'Cluster 0', 1: 'Cluster 1', 2: 'Cluster 2'}

    plt.figure(figsize=(8, 6))

    # Scatter plot with assigned colors
    for cluster in np.unique(clusters):
        mask = clusters == cluster
        plt.scatter(X_tsne[mask, 0], X_tsne[mask, 1],
                    c=colors[cluster], label=labels[cluster], s=50)

    plt.title(title1)
    plt.xlabel('TSNE 1')
    plt.ylabel('TSNE 2')
    plt.legend()
    plt.show()


def show_cluster_distribution_numerical(X: pd.DataFrame, clusters: np.array, n_clusters: int, feature_name: str,
                                        bins: int, min: float = None, max: float = None) -> None:
    """
    Show the distribution of a feature for each cluster
    :param X: the dataset to visualize
    :param clusters: the clusters of the dataset (labels)
    :param n_clusters: the number of clusters
    :param feature_name: the name of the feature in X
    :param bins: the number of bins to categorize the data
    :param min: (optional) lower bound for the x-axis, defaults to the minimum value of the feature
    :param max: (optional) upper bound for the x-axis, defaults to the maximum value of the feature
    """
    if min is None:
        min = X[feature_name].min() - (X[feature_name].max()/10)
    if max is None:
        max = X[feature_name].max() + (X[feature_name].max()/10)

    plt.figure(figsize=(10, 6))
    for cluster in range(n_clusters):
        sns.kdeplot(X[clusters == cluster][feature_name], label=f'Cluster {cluster}')
    plt.title(f'Distribution of {feature_name} for each Cluster')
    plt.xlabel(feature_name)
    plt.ylabel('Density')
    plt.xlim(min, max)
    plt.legend()
    plt.show()



def show_cluster_distribution_boolean(X: pd.DataFrame, clusters: np.array, n_clusters: int, feature_name: str) -> None:
    """
    Muestra la distribución de una variable booleana para cada cluster, expresada en porcentaje
    respecto al total de registros de cada cluster.

    :param X: el conjunto de datos a visualizar
    :param clusters: los clusters del conjunto de datos (etiquetas)
    :param n_clusters: el número de clusters
    :param feature_name: el nombre de la variable booleana en X
    """
    # Crear una copia del dataframe y agregar la columna de clusters
    X_plot = X.copy()
    X_plot['Cluster'] = "Cluster " + pd.Series(clusters).astype(str)

    # Calcular el conteo de cada valor (True/False) por cluster
    df_counts = X_plot.groupby(['Cluster', feature_name]).size().reset_index(name='count')
    # Calcular el porcentaje respecto al total de cada cluster
    df_counts['percent'] = df_counts.groupby('Cluster')['count'].transform(lambda x: 100 * x / x.sum())

    plt.figure(figsize=(10, 6))
    # Graficar usando barplot con la columna de porcentaje
    sns.barplot(data=df_counts, x=feature_name, y='percent', hue='Cluster')
    plt.title(f'Distribución de {feature_name} (booleano) para cada Cluster (porcentaje)')
    plt.xlabel(feature_name)
    plt.ylabel('Porcentaje (%)')
    plt.legend(title='Cluster')
    plt.ylim(0, 100)
    plt.show()


def show_cluster_distribution_categorical(X: pd.DataFrame, clusters: np.array, n_clusters: int,
                                          feature_name: str) -> None:
    """
    Muestra la distribución de una variable categórica para cada cluster.
    Si la variable fue one-hot encoded (por ejemplo, columnas con nombres como
    'name_convention_SnakeCase', 'name_convention_UpperCase'), las combina en una sola columna.
    Los valores se muestran como porcentaje del total de cada cluster.

    :param X: el conjunto de datos a visualizar
    :param clusters: los clusters del conjunto de datos (etiquetas)
    :param n_clusters: el número de clusters
    :param feature_name: el prefijo de la variable categórica en X (e.g., 'name_convention')
    """
    X_plot = X.copy()

    # Buscar columnas que tengan el prefijo 'feature_name_' (one-hot encoded)
    onehot_cols = [col for col in X_plot.columns if col.startswith(feature_name + '_')]

    if onehot_cols:
        # Se asume que cada fila tiene un único 1 entre las columnas one-hot.
        # Se extrae el nombre de la categoría eliminando el prefijo.
        X_plot[feature_name] = X_plot[onehot_cols].idxmax(axis=1).str.replace(feature_name + '_', '')
        cat_column = feature_name
    else:
        cat_column = feature_name

    # Agregar la columna de clusters
    X_plot['Cluster'] = "Cluster " + pd.Series(clusters).astype(str)

    # Calcular la cantidad de ocurrencias por cluster y categoría
    df_counts = X_plot.groupby(['Cluster', cat_column]).size().reset_index(name='count')
    # Calcular el porcentaje respecto al total de cada cluster
    df_counts['percent'] = df_counts.groupby('Cluster')['count'].transform(lambda x: 100 * x / x.sum())

    plt.figure(figsize=(10, 6))
    # Graficar usando sns.barplot con la columna de porcentaje
    sns.barplot(data=df_counts, x=cat_column, y='percent', hue='Cluster')
    plt.title(f'Distribución de {feature_name} para cada Cluster (porcentaje)')
    plt.xlabel(feature_name)
    plt.ylabel('Porcentaje (%)')
    plt.legend(title='Cluster')
    plt.ylim(0, 100)
    plt.show()

def plot_dimension_reduction(X: pd.DataFrame, dimensions: int):
    tsne = TSNE(n_components=dimensions)
    df_tsne = tsne.fit_transform(X)

    categories = ['BEGINNER' if x == 1 else 'PROFESSIONAL' for x in X['module__expertise_level_BEGINNER']]

    plt.figure(figsize=(10, 8))
    palette = {'BEGINNER': 'blue', 'PROFESSIONAL': 'red'}

    sns.scatterplot(
        x=df_tsne[:, 0],
        y=df_tsne[:, 1],
        hue=categories,
        palette=palette,
        legend='full',
        alpha=0.5
    )

    plt.title("Clusters diferenciados por Expertise Level")
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend(title="Expertise Level")
    plt.show()


def train_val_split(X: pd.DataFrame, y: pd.Series, val_size: float):
    y = y.apply(lambda t: 1 if t else 0)
    X_y = X.copy()
    X_y['module__expertise_level'] = y
    X_y.drop(['module__expertise_level_BEGINNER', 'module__expertise_level_PROFESSIONAL'], axis=1, inplace=True)

    df_train, df_val = train_test_split(
        X_y,
        test_size=val_size,
        stratify=X_y['module__expertise_level'],  # Asegura el equilibrio de clases
        shuffle=True  # Barajar antes de dividir
    )

    X_train = df_train.copy()
    X_train = X_train.drop(['module__expertise_level'], axis=1)
    y_train = df_train['module__expertise_level'].copy()

    X_val = df_val.copy()
    X_val = X_val.drop(['module__expertise_level'], axis=1)
    y_val = df_val['module__expertise_level'].copy()

    return X_train, y_train, X_val, y_val

def compute_silhouette_scores(X: np.array, from_k: int, to_k: int) -> np.array:
    """
    Compute the silhouette scores for k=from_k to k=to_k
    :param X: the dataset
    :param from_k: the minimum number of clusters
    :param to_k: the maximum number of clusters
    :return: a list with the silhouette scores for each k
    """
    scores = []
    for k in range(from_k, to_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=0)
        clusters = kmeans.fit_predict(X)
        score = silhouette_score(X, clusters)
        scores.append(score)
    # Plot the silhouette scores
    plt.figure(figsize=(8, 4))
    plt.plot(range(from_k, to_k + 1), scores, marker='o')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score for Optimal k')
    plt.show()
    return scores

def apply_kruskal_dunn(df, variable, cluster_labels):
    """
    Aplica Kruskal-Wallis y Dunn's post-hoc a una variable continua en función de clusters.

    :param df: DataFrame de pandas con los datos.
    :param variable: Nombre de la columna con la variable continua (string).
    :param cluster_labels: Array de NumPy o lista con las etiquetas de cluster.
    :return: (Kruskal-Wallis statistic, p-value, Dunn's post-hoc DataFrame).
    """
    # Paso 1: Asegurar que cluster_labels sea una columna en df
    df = df.copy()  # Evitar modificar el DataFrame original
    df['_cluster_temp'] = cluster_labels  # Columna temporal

    # Paso 2: Filtrar NaN y obtener grupos
    cluster_groups = [group[variable].dropna() for _, group in df.groupby('_cluster_temp')]

    # Paso 3: Kruskal-Wallis
    kw_statistic, p_value = kruskal(*cluster_groups)

    print(f"Kruskal-Wallis - H-statistic: {kw_statistic:.4f}, p-value: {p_value:.4f}")

    # Paso 4: Dunn's post-hoc si hay diferencias significativas
    if p_value < 0.05:
        print("Hay diferencias significativas entre al menos un par de clusters.")
        dunn_results = posthoc_dunn(
            df,
            val_col=variable,
            group_col='_cluster_temp',
            p_adjust='bonferroni'
        )
        print("\nDunn's post-hoc test (p-values ajustados):")
        print(dunn_results)
    else:
        print("No hay diferencias significativas entre los clusters.")
        dunn_results = None

    # Eliminar columna temporal (opcional)
    df.drop('_cluster_temp', axis=1, inplace=True)

    return kw_statistic, p_value, dunn_results
