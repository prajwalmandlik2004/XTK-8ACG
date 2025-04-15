import hashlib
import pandas as pd

def generate_code_from_columns(df, selected_columns, target_column):
    def generate_code(row):
        data_str = ''.join([str(row[col]) for col in selected_columns])
        hash_object = hashlib.sha256(data_str.encode())
        hex_digest = hash_object.hexdigest()
        alpha_chars = ''.join(filter(str.isalpha, hex_digest))[:8].upper()
        return alpha_chars

    df[target_column] = df.apply(generate_code, axis=1)
    return df
