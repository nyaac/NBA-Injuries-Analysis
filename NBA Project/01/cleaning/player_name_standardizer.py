import numpy as np

def player_name_standardizer(player_names_series, relinquished_series, acquired_series=None):
    """
    Standardizes player name spellings based on the unique player names.
    
    Inputs:
    - player_names_series: Series of unique, standardized player names.
    - relinquished_series: Series of player names from the 'Relinquished' column.
    - acquired_series: Series of player names from the 'Acquired' column, optional.
    
    Output:
    - A dictionary mapping original player names to standardized names or the original name if no match found.
    """
    name_set = set(player_names_series)
    name_dictionary = {}
    
    # Convert NaN to a string representation to avoid type errors
    relinquished_series = relinquished_series.astype(str)
    all_names = relinquished_series.unique()
    if acquired_series is not None:
        acquired_series = acquired_series.astype(str)
        all_names = np.union1d(all_names, acquired_series.unique())
    
    for name in all_names:
        if name in name_set:
            name_dictionary[name] = name
        else:
            name_dictionary[name] = name  # Keep the original name if no match found
    return name_dictionary
