import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, classification_report
from statsmodels.stats.stattools import medcouple
import sys
import os
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
import wittgenstein as lw
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from itertools import product
from scikit_posthocs import posthoc_dunn
from scipy.stats import kruskal

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
def print_frequency_anal_for_cat_var(df, column_name, possible_values=[], outlier_threshold=1):
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



def print_outliers_tukey(df, column_name, weak_coefficient=1.5, strong_coefficient=3.0):
    column_dataframe = df[column_name].describe()
    data = np.array(df[column_name])
    q1 = column_dataframe['25%']
    q3 = column_dataframe['75%']
    iqr = q3 - q1
    #mc = medcouple(data)
    #print(f'El coeficiente MC (Medcouple Coefficient) de balanceo es: {mc}')
    low_strong_iqr_lmt = q1 - strong_coefficient * iqr
    high_strong_iqr_lmt = q3 + strong_coefficient * iqr
    low_weak_iqr_lmt = q1 - weak_coefficient * iqr
    high_weak_iqr_lmt = q3 + weak_coefficient * iqr
    print(f"Rango valores atípicos extremos (Tukey): [{low_strong_iqr_lmt},{high_strong_iqr_lmt}]")
    print(f"Rango valores atípicos leves (Tukey): [{low_weak_iqr_lmt},{high_weak_iqr_lmt}]")

    num_low_strong_outliers = len(df[df[column_name] < low_strong_iqr_lmt].index)
    num_low_weak_outliers = len(df[df[column_name] < low_weak_iqr_lmt].index)
    num_high_weak_outliers = len(df[df[column_name] > high_weak_iqr_lmt].index)
    num_high_strong_outliers = len(df[df[column_name] > high_strong_iqr_lmt].index)

    num_low_strong_outliers_pct = num_low_strong_outliers / len(df[column_name]) * 100
    num_low_weak_outliers_pct = num_low_weak_outliers / len(df[column_name]) * 100
    num_high_weak_outliers_pct = num_high_weak_outliers / len(df[column_name]) * 100
    num_high_strong_outliers_pct = num_high_strong_outliers / len(df[column_name]) * 100

    print(f'-3.0IQR: {num_low_strong_outliers} instancias tienen un valor para {column_name} inferior a {low_strong_iqr_lmt} (Q1-3*IQR) para {column_name}. Representando un {num_low_strong_outliers_pct:.4}% del total de instancias.')
    print(f'-1.5IQR: {num_low_weak_outliers} instancias tienen un valor para {column_name} inferior a {low_weak_iqr_lmt} (Q1-1.5*IQR) para {column_name}. Representando un {num_low_weak_outliers_pct:.4}% del total de instancias.')
    print(f'+1.5IQR: {num_high_weak_outliers} instancias tienen un valor para {column_name} superior a {high_weak_iqr_lmt} (Q3+1.5*IQR) para {column_name}. Representando un {num_high_weak_outliers_pct:.4}% del total de instancias.')
    print(f'+3.0IQR: {num_high_strong_outliers} instancias tienen un valor para {column_name} superior a {high_strong_iqr_lmt} (Q3-3*IQR) para {column_name}. Representando un {num_high_strong_outliers_pct:.4}% del total de instancias.')


def print_outliers_mad(df, column_name, k=3):
    data = np.array(df[column_name])
    median = np.median(data)
    mad = 1.4826 * np.median(np.abs(data - median))
    mad_lower_limit = median - (k * mad)
    mad_upper_limit = median + (k * mad)
    print(f"Rango valores atípicos MAD (Median Absolute Deviation): [{mad_lower_limit},{mad_upper_limit}]")

    num_low_mad_outliers = len(df[df[column_name] < mad_lower_limit].index)
    num_high_mad_outliers = len(df[df[column_name] > mad_upper_limit].index)
    num_low_mad_outliers_pct = num_low_mad_outliers / len(df[column_name]) * 100
    num_high_mad_outliers_pct = num_high_mad_outliers / len(df[column_name]) * 100
    print(
        f'MAD Inferior: {num_low_mad_outliers} instancias tienen un valor para {column_name} inferior a {mad_lower_limit} para {column_name}. Representando un {num_low_mad_outliers_pct:.4}% del total de instancias.')
    print(
        f'MAD Superior: {num_high_mad_outliers} instancias tienen un valor para {column_name} superior a {mad_upper_limit} para {column_name}. Representando un {num_high_mad_outliers_pct:.4}% del total de instancias.')


def print_outliers_mad_zero_inflated(df, column_name, k=3, th=0):
    total_samples = len(df[column_name])
    no_zero_data = np.array(df[df[column_name] > th][column_name])
    median = np.median(no_zero_data)
    mad = 1.4826 * np.median(np.abs(no_zero_data - median))
    mad_lower_limit = median - (k * mad)
    mad_upper_limit = median + (k * mad)

    print(f"Rango valores atípicos MAD excluyendo las instancias con valor 0 (Median Absolute Deviation): [{mad_lower_limit},{mad_upper_limit}]")

    num_low_mad_outliers = len(no_zero_data[no_zero_data < mad_lower_limit])
    num_high_mad_outliers = len(no_zero_data[no_zero_data > mad_upper_limit])
    num_low_mad_outliers_pct = num_low_mad_outliers / total_samples * 100
    num_high_mad_outliers_pct = num_high_mad_outliers / total_samples * 100
    print(
        f'MAD Inferior: {num_low_mad_outliers} instancias tienen un valor para {column_name} inferior a {mad_lower_limit} y diferente de 0 para {column_name}. Representando un {num_low_mad_outliers_pct:.4}% del total de instancias.')
    print(
        f'MAD Superior: {num_high_mad_outliers} instancias tienen un valor para {column_name} superior a {mad_upper_limit} para {column_name}. Representando un {num_high_mad_outliers_pct:.4}% del total de instancias.')


def print_outliers_tukey_zero_inflated(df, column_name, weak_coefficient=1.5, strong_coefficient=3.0, th=0):
    total_samples = len(df[column_name])
    no_zero_data = np.array(df[df[column_name] > th][column_name])
    column_dataframe = df[df[column_name] > th][column_name].describe()
    q1 = column_dataframe['25%']
    q3 = column_dataframe['75%']
    iqr = q3 - q1
    #mc = medcouple(no_zero_data)
    #print(f'El coeficiente MC (Medcouple Coefficient) de balanceo es: {mc}')
    low_strong_iqr_lmt = q1 - strong_coefficient * iqr
    high_strong_iqr_lmt = q3 + strong_coefficient * iqr
    low_weak_iqr_lmt = q1 - weak_coefficient * iqr
    high_weak_iqr_lmt = q3 + weak_coefficient * iqr
    print(f"Rango valores atípicos extremos (Tukey): [{low_strong_iqr_lmt},{high_strong_iqr_lmt}]")
    print(f"Rango valores atípicos leves (Tukey): [{low_weak_iqr_lmt},{high_weak_iqr_lmt}]")

    num_low_strong_outliers = len(no_zero_data[no_zero_data < low_strong_iqr_lmt])
    num_low_weak_outliers = len(no_zero_data[no_zero_data < low_weak_iqr_lmt])
    num_high_weak_outliers = len(no_zero_data[no_zero_data > high_weak_iqr_lmt])
    num_high_strong_outliers = len(no_zero_data[no_zero_data > high_strong_iqr_lmt])

    num_low_strong_outliers_pct = num_low_strong_outliers / total_samples * 100
    num_low_weak_outliers_pct = num_low_weak_outliers / total_samples * 100
    num_high_weak_outliers_pct = num_high_weak_outliers / total_samples * 100
    num_high_strong_outliers_pct = num_high_strong_outliers / total_samples * 100

    print(f'-3.0IQR: {num_low_strong_outliers} instancias tienen un valor para {column_name} inferior a {low_strong_iqr_lmt} (Q1-3*IQR) para {column_name}. Representando un {num_low_strong_outliers_pct:.4}% del total de instancias.')
    print(f'-1.5IQR: {num_low_weak_outliers} instancias tienen un valor para {column_name} inferior a {low_weak_iqr_lmt} (Q1-1.5*IQR) para {column_name}. Representando un {num_low_weak_outliers_pct:.4}% del total de instancias.')
    print(f'+1.5IQR: {num_high_weak_outliers} instancias tienen un valor para {column_name} superior a {high_weak_iqr_lmt} (Q3+1.5*IQR) para {column_name}. Representando un {num_high_weak_outliers_pct:.4}% del total de instancias.')
    print(f'+3.0IQR: {num_high_strong_outliers} instancias tienen un valor para {column_name} superior a {high_strong_iqr_lmt} (Q3-3*IQR) para {column_name}. Representando un {num_high_strong_outliers_pct:.4}% del total de instancias.')



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
    """
    Detecta outliers con KDE calculando el umbral de densidad directamente sobre los datos,
    lo cual es mejor para distribuciones con picos o huecos.
    Args:
        dataframe: DataFrame con los datos.
        column: Columna sobre la que aplicar la detección.
        percentile: Percentil (ej. 0.05 para el 5%) como umbral de outliers.
    Returns:
        Serie booleana indicando qué instancias son outliers.
    """
    series = dataframe[column]
    # Ajustar KDE a la serie
    kde = gaussian_kde(series)
    # Calcular densidad en los valores reales de la serie
    density_values = kde(series)
    # Umbral de outliers: densidades por debajo del percentil dado
    lower_threshold = np.percentile(density_values, percentile * 100)
    print(f"Umbral de densidad (calculado sobre los datos reales): {lower_threshold:.6f}")
    # Máscara de outliers: densidades por debajo del umbral
    outliers_mask = density_values < lower_threshold
    # Verificar si se han detectado outliers
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
    colors = {0: 'blue', 1: 'orange', 2: 'green', 3: 'purple', 4: 'yellow'}
    labels = {0: 'Cluster 0', 1: 'Cluster 1', 2: 'Cluster 2', 3: 'Cluster 3', 4: 'Cluster 4'}

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

def plot_dimension_reduction(X: pd.DataFrame, dimensions: int, table: str):
    tsne = TSNE(n_components=dimensions)
    df_tsne = tsne.fit_transform(X)

    categories = ['BEGINNER' if x == 1 else 'PROFESSIONAL' for x in X[table + '__expertise_level_BEGINNER']]

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


def train_val_split(X: pd.DataFrame, y: pd.Series, val_size: float, table: str):
    expert_column = table + '__expertise_level_PROFESSIONAL'
    beg_column = table + '__expertise_level_BEGINNER'
    target_column = table + '__expertise_level'
    y = y.apply(lambda t: 1 if t else 0)
    X_y = X.copy()
    X_y[target_column] = y
    X_y.drop([beg_column, expert_column], axis=1, inplace=True)

    df_train, df_val = train_test_split(
        X_y,
        test_size=val_size,
        stratify=X_y[target_column],  # Asegura el equilibrio de clases
        shuffle=True  # Barajar antes de dividir
    )

    X_train = df_train.copy()
    X_train = X_train.drop([target_column], axis=1)
    y_train = df_train[target_column].copy()

    X_val = df_val.copy()
    X_val = X_val.drop([target_column], axis=1)
    y_val = df_val[target_column].copy()

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

def plot_pairplot(df, columns):
    """
    Genera un pairplot con las variables numéricas especificadas de un DataFrame.

    :param df: DataFrame de pandas con los datos.
    :param columns: Lista de nombres de columnas a incluir en el pairplot.
    """
    numeric_df = df[columns].select_dtypes(include=['number'])  # Seleccionar solo columnas numéricas especificadas
    if numeric_df.shape[1] > 1:
        sns.pairplot(numeric_df)
        plt.show()
    else:
        print("No hay suficientes variables numéricas para generar un pairplot.")

def analizar_bins(df, feature):
    print(f"\n--- Análisis de la feature: '{feature}' ---")

    # Discretización por igual anchura
    bins_anchura = pd.cut(df[feature], bins=3)
    freq_anchura = bins_anchura.value_counts().sort_index()
    total = len(df)
    print("\nDiscretización en 3 bins de **igual anchura**:")
    for bin_label, count in freq_anchura.items():
        porcentaje = (count / total) * 100
        print(f"  {bin_label}: {count} ({porcentaje:.1f}%)")

    # Discretización por igual frecuencia
    try:
        bins_frecuencia = pd.qcut(df[feature], q=3, duplicates='drop')
        freq_frecuencia = bins_frecuencia.value_counts().sort_index()
        print("\nDiscretización en 3 bins de **igual frecuencia**:")
        for bin_label, count in freq_frecuencia.items():
            porcentaje = (count / total) * 100
            print(f"  {bin_label}: {count} ({porcentaje:.1f}%)")
    except ValueError as e:
        print("\nDiscretización en igual frecuencia no posible:", e)


def extract_and_filter_tree_rules(df, table, min_conf=0.9, min_support=0.05, max_conditions=3):
    """
    Extrae las reglas de un árbol de decisión y las filtra según:
    - min_conf: confianza mínima
    - min_support: soporte mínimo (en proporción)
    - max_conditions: número máximo de condiciones en el antecedente
    """
    expert_column = table + '__expertise_level_PROFESSIONAL'
    beg_column = table + '__expertise_level_BEGINNER'
    target_column = table + '__expertise_level'
    X = df.copy()

    target_columns = [beg_column, expert_column]

    X["expertise_level"] = X[target_columns].idxmax(axis=1)
    X["expertise_level"] = X["expertise_level"].str.replace(table + "__", "")

    y = X["expertise_level"]
    X = X.drop(target_columns + ["expertise_level"], axis=1)

    # Entrenar el árbol de decisión con profundidad máxima de 3:
    tree = DecisionTreeClassifier(max_depth=3)
    tree.fit(X, y)

    class_names = tree.classes_
    feature_names = list(df.columns)

    tree_ = tree.tree_
    total_samples = tree_.n_node_samples[0]

    def recurse(node, rule_conditions):
        if tree_.children_left[node] == -1 and tree_.children_right[node] == -1:
            node_samples = tree_.n_node_samples[node]
            support = node_samples / total_samples

            counts = tree_.value[node][0]
            predicted_class_index = np.argmax(counts)
            predicted_class = class_names[predicted_class_index]
            confidence = counts[predicted_class_index]

            if len(rule_conditions) <= max_conditions and support >= min_support and confidence >= min_conf:
                rule_str = " AND ".join(rule_conditions) if rule_conditions else "TRUE"
                print(f"Rule: IF {rule_str} THEN class = {predicted_class}")
                print(f"       Support: {support:.2%}, Confidence: {confidence:.2%}\n")
        else:

            feature_index = tree_.feature[node]
            threshold = tree_.threshold[node]
            condition_left = f"{feature_names[feature_index]} <= {threshold:.2f}"
            recurse(tree_.children_left[node], rule_conditions + [condition_left])

            condition_right = f"{feature_names[feature_index]} > {threshold:.2f}"
            recurse(tree_.children_right[node], rule_conditions + [condition_right])

    recurse(0, [])


def extract_and_filter_irep_rules(df, table, min_conf=0.9, min_support=0.05, max_conditions=3):
    expert_column = table + '__expertise_level_PROFESSIONAL'
    beg_column = table + '__expertise_level_BEGINNER'
    X = df.copy()
    target_columns = [beg_column, expert_column]
    X["expertise_level"] = X[target_columns].idxmax(axis=1)
    X = X.drop(target_columns, axis=1)
    X["expertise_level"] = X["expertise_level"].apply(
        lambda value: 0 if value == beg_column else 1)

    irep = lw.IREP()

    stdout_original = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    irep.fit(X, class_feat="expertise_level")
    sys.stdout = stdout_original

    print("Filtered IREP rules:")
    filter_rules(irep.ruleset_, target_columns, len(X), min_conf, min_support, max_conditions)


def extract_and_filter_ripper_rules(df, table, min_conf=0.9, min_support=0.05, max_conditions=3):
    expert_column = table + '__expertise_level_PROFESSIONAL'
    beg_column = table + '__expertise_level_BEGINNER'
    target_column = table + '__expertise_level'
    X = df.copy()
    target_columns = [beg_column, expert_column]
    X["expertise_level"] = X[target_columns].idxmax(axis=1)
    X = X.drop(target_columns, axis=1)
    X["expertise_level"] = X["expertise_level"].apply(
        lambda value: 0 if value == beg_column else 1)

    ripper = lw.RIPPER()
    ripper.fit(X, class_feat="expertise_level")

    print("Filtered RIPPER rules:")
    filter_rules(ripper.ruleset_, target_columns, len(X), min_conf, min_support, max_conditions)


def filter_rules(ruleset, target_columns, total_samples, min_conf=0.9, min_support=0.05, max_conditions=3):
    for rule in ruleset.rules:
        rule_count = sum(rule.class_ns_)
        if rule_count == 0:
            continue

        confidence = max(rule.class_freqs_)
        support = rule_count / total_samples

        if confidence >= min_conf and support >= min_support and len(rule.conds) <= max_conditions:
            predicted_class_index = rule.class_freqs_.index(max(rule.class_freqs_))
            rule_str = " AND ".join(str(cond) for cond in rule.conds) if rule.conds else "TRUE"
            print("Rule: IF " + rule_str + f" THEN class = {target_columns[predicted_class_index]}")
            print(f"Support: {support:.2%}, Confidence: {confidence:.2%}")
            print("-----")

def decision_tree_weights(dt, table):
    expert_column = table + '__expertise_level_PROFESSIONAL'
    beg_column = table + '__expertise_level_BEGINNER'
    target_column = table + '__expertise_level'
    X_dt = dt.copy()

    target_columns = [beg_column, expert_column]
    X_dt["expertise_level"] = X_dt[target_columns].idxmax(axis=1)
    X_dt["expertise_level"] = X_dt["expertise_level"].str.replace(table + "__", "")
    y = X_dt["expertise_level"]
    X_dt = X_dt.drop(target_columns + ["expertise_level"], axis=1)
    # Entrenar el árbol de decisión con profundidad máxima de 3:
    tree = DecisionTreeClassifier(max_depth=20)
    tree.fit(X_dt, y)

    feature_names = X_dt.columns
    feature_importances_RF = tree.feature_importances_

    importances_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": feature_importances_RF
    }).sort_values(by="Importance", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(importances_df["Feature"], importances_df["Importance"], color='skyblue')
    plt.xlabel("Importancia")
    plt.ylabel("Características")
    plt.title("Importancia de las características en Random Forest")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def random_forest_weights(X_train, y_train, X_val, y_val):
    n_estimators_range = range(50, 201, 25)  # Número de estimadores: 50 a 200 en pasos de 25
    max_depth_range = [None, 10, 20, 30]  # Profundidad máxima del árbol
    min_samples_split_range = [2, 5, 10]  # Muestras mínimas para dividir un nodo

    best_accuracy = 0
    best_f1_score = 0
    best_params = {}

    # Iterar sobre todas las combinaciones de parámetros
    for n_estimators in n_estimators_range:
        for max_depth in max_depth_range:
            for min_samples_split in min_samples_split_range:
                # Crear y entrenar el modelo con la combinación actual de hiperparámetros
                rf_model = RandomForestClassifier(
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    min_samples_split=min_samples_split
                )
                rf_model.fit(X_train, y_train)

                # Predicción y métricas
                y_pred = rf_model.predict(X_val)
                accuracy_value = accuracy_score(y_val, y_pred)
                f1_score_value = f1_score(y_val, y_pred)

                # Mostrar resultados para la combinación actual
                #print(f"Estimators: {n_estimators}, Max Depth: {max_depth}, Min Samples Split: {min_samples_split}.\n\t"
                #      f"Accuracy: {accuracy_value:.4f}.\n\tF1 Score: {f1_score_value:.4f}.")

                # Actualizar la mejor combinación si es necesario
                if accuracy_value > best_accuracy or (
                        accuracy_value == best_accuracy and f1_score_value > best_f1_score):
                    best_accuracy = accuracy_value
                    best_f1_score = f1_score_value
                    best_params = {
                        'n_estimators': n_estimators,
                        'max_depth': max_depth,
                        'min_samples_split': min_samples_split
                    }

    rf_model = RandomForestClassifier(n_estimators=best_params['n_estimators'], min_samples_split=best_params['min_samples_split'], max_depth=best_params['max_depth'], )
    rf_model.fit(X_train, y_train)

    feature_names = X_train.columns
    feature_importances_RF = rf_model.feature_importances_

    importances_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": feature_importances_RF
    }).sort_values(by="Importance", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(importances_df["Feature"], importances_df["Importance"], color='skyblue')
    plt.xlabel("Importancia")
    plt.ylabel("Características")
    plt.title("Importancia de las características en Random Forest")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def logistic_regression(X_train, y_train, X_val, y_val):
    best_accuracy = 0
    best_degree = 0
    best_model = None
    best_poly_features = None
    best_params = None

    # Rango de hiperparámetros a explorar
    param_grid = {
        'penalty': ['elasticnet'],
        'C': [0.001, 0.01, 0.1],
        'solver': ['saga'],
        'l1_ratio': [0.33, 0.5, 0.66]
    }

    # Crear todas las combinaciones posibles de hiperparámetros
    param_combinations = list(product(*param_grid.values()))
    total_combinations = len(param_combinations)

    print(f"Número total de combinaciones de hiperparámetros: {total_combinations}\n")

    # Iterar sobre los grados polinómicos
    for degree in range(1, 3):
        print(f"Probando grado polinómico: {degree}")
        poly_features = PolynomialFeatures(degree=degree)
        X_train_poly = poly_features.fit_transform(X_train)
        X_val_poly = poly_features.transform(X_val)

        # Variables para almacenar los mejores resultados para este grado
        best_accuracy_degree = 0
        best_params_degree = None
        best_model_degree = None

        # Probar cada combinación de hiperparámetros
        for idx, (penalty, C, solver, l1_ratio) in enumerate(param_combinations, start=1):
            print(f"  - Combinación {idx}/{total_combinations} para grado {degree}: "
                  f"penalty={penalty}, C={C}, solver={solver}, l1_ratio={l1_ratio}")

            # Configurar el modelo base de regresión logística
            logistic = LogisticRegression(
                penalty=penalty,
                C=C,
                solver=solver,
                l1_ratio=l1_ratio,
                max_iter=5000
            )

            # Entrenar el modelo
            logistic.fit(X_train_poly, y_train)

            # Evaluar en el conjunto de validación
            accuracy = logistic.score(X_val_poly, y_val)

            # Actualizar los mejores valores para este grado
            if accuracy > best_accuracy_degree:
                best_accuracy_degree = accuracy
                best_params_degree = {
                    'penalty': penalty,
                    'C': C,
                    'solver': solver,
                    'l1_ratio': l1_ratio
                }
                best_model_degree = logistic

            # Guardar el mejor modelo global
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_degree = degree
                best_model = logistic
                best_poly_features = poly_features
                best_params = {
                    'penalty': penalty,
                    'C': C,
                    'solver': solver,
                    'l1_ratio': l1_ratio
                }

        # Imprimir los mejores resultados para este grado
        print("\nMejores resultados para grado {}:".format(degree))
        print("  Accuracy: {:.2f}%".format(best_accuracy_degree * 100))
        print("  Parámetros:", best_params_degree)
        print()

    # Resultados finales
    print(f"Mejor grado polinómico: {best_degree}")
    print(f"Mejores parámetros globales: {best_params}")
    print(f"Mejor accuracy global en validación: {best_accuracy * 100:.2f}%")

    # Evaluación final en el conjunto de validación
    X_val_best_poly = best_poly_features.transform(X_val)
    y_pred = best_model.predict(X_val_best_poly)
    print("\nReporte de clasificación en el conjunto de validación:")
    print(classification_report(y_val, y_pred))
    print("Accuracy en el conjunto de validación:", accuracy_score(y_val, y_pred))


def apply_kruskal_dunn_all(df: pd.DataFrame, variables: list, cluster_labels, alpha: float = 0.05, visualize: bool = True) -> pd.DataFrame:
    """
    Realiza Kruskal-Wallis y Dunn post-hoc para múltiples variables,
    devuelve un único DataFrame con todos los resultados y opcionalmente lo muestra.

    :param df: DataFrame de pandas con los datos.
    :param variables: Lista de nombres de columnas continuas a analizar.
    :param cluster_labels: Array o lista con etiquetas de cluster.
    :param alpha: Nivel de significación para pruebas (por defecto 0.05).
    :param visualize: Si True, muestra el DataFrame con display_dataframe_to_user.
    :return: DataFrame con columnas:
             ['variable','H_stat','p_value','cluster_i','cluster_j','dunn_pvalue','significant']
    """
    df = df.copy()
    df['_cluster_temp'] = cluster_labels

    records = []

    for var in variables:
        # Agrupar datos por cluster y eliminar NaNs
        groups = [grp[var].dropna() for _, grp in df.groupby('_cluster_temp')]
        if len([g for g in groups if len(g) > 0]) < 2:
            continue

        # Kruskal-Wallis
        H, p_kw = kruskal(*groups)

        # Prepara estructura de Dunn: incluso si no es significativo, incluimos NaN
        dunn_matrix = None
        if p_kw < alpha:
            dunn_matrix = posthoc_dunn(df, val_col=var, group_col='_cluster_temp', p_adjust='bonferroni')
        else:
            # Matriz vacía con índices de clusters
            idx = sorted(df['_cluster_temp'].unique())
            dunn_matrix = pd.DataFrame(float('nan'), index=idx, columns=idx)

        # Recorre triángulo superior de la matriz Dunn
        clusters = dunn_matrix.index.tolist()
        for i, ci in enumerate(clusters):
            for cj in clusters[i+1:]:
                p_dunn = dunn_matrix.loc[ci, cj]
                records.append({
                    'variable': var,
                    'H_stat': H,
                    'p_value': p_kw,
                    'cluster_i': ci,
                    'cluster_j': cj,
                    'dunn_pvalue': p_dunn,
                    'significant': (p_dunn < alpha) if pd.notna(p_dunn) else False
                })

    # Construir DataFrame final
    result_df = pd.DataFrame.from_records(records)
    # Ordenar: primero por variable, luego por significant, luego por p_value asc
    result_df = result_df.sort_values(['variable','significant','dunn_pvalue'], ascending=[True, False, True])

    # Visualizar si se desea
    if visualize:
        print("Resultados Kruskal-Dunn")
        result_df.describe()

    # Limpiar
    df.drop('_cluster_temp', axis=1, inplace=True)

    return result_df