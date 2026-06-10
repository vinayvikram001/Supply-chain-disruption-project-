import pandas as pd

df = pd.read_csv(
    "data/supply_chain_disruption_recovery.csv"
)

print("Dataset loaded successfully!")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
print("\nMissing Values:")
print(df.isnull().sum())
print("\nDuplicate Rows:")
print(df.duplicated().sum())
categorical_cols = [
    'disruption_type',
    'industry',
    'supplier_tier',
    'supplier_region',
    'supplier_size',
    'disruption_severity'
]

for col in categorical_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.title()
    )

print("\nText columns standardized!")
severity_map = {
    'Low': 1,
    'Medium': 2,
    'High': 3,
    'Critical': 4
}

print("\nUnique Severity Values:")
print(df['disruption_severity'].unique())

df['risk_score'] = (
    df['disruption_severity']
    .astype(int)
)

severity_labels = {
    1: 'Low',
    2: 'Medium',
    3: 'High',
    4: 'Critical'
}

df['severity_label'] = (
    df['risk_score']
    .map(severity_labels)
)

print("\nRisk Score Created!")

print(
    df[
        [
            'disruption_severity',
            'risk_score',
            'severity_label'
        ]
    ].head()
)
df.to_csv(
    "data/processed_disruptions.csv",
    index=False
)