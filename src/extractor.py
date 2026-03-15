import pandas as pd

def extract_data(files_list):
    combined_text = ""
    for f in files_list:
        if f.name.endswith('.txt'):
            combined_text += f.read().decode("utf-8") + "\n"
        elif f.name.endswith('.xlsx'):
            df = pd.read_excel(f)
            combined_text += " ".join(df.astype(str).values.flatten()) + "\n"
    return combined_text