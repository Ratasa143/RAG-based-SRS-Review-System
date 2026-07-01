import pandas as pd

df = pd.read_csv("ground_truth.csv", encoding="latin1")
print(df['true_label'].value_counts())
print(f'Total labeled: {len(df[df["true_label"].notna()])}')