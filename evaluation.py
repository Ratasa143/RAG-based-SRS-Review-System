import pandas as pd
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix

def compute_metrics(y_true, y_pred):
    labels = ["ok", "ambiguous", "missing", "conflict"]
    
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average=None, zero_division=0
    )
    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1.mean()

    print(f"\n✅ Accuracy:  {accuracy:.4f}")
    print(f"✅ Macro F1:  {macro_f1:.4f}")
    print("\nPer-class metrics:")
    print(f"{'Label':<12} {'Precision':<12} {'Recall':<12} {'F1':<12} {'Support'}")
    print("-" * 55)
    for i, label in enumerate(labels):
        print(f"{label:<12} {precision[i]:<12.4f} {recall[i]:<12.4f} {f1[i]:<12.4f} {support[i]}")

    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print(cm_df)

    return {
        "accuracy": round(accuracy, 4),
        "macro_f1": round(macro_f1, 4),
    }

# Load ground truth
df = pd.read_csv("ground_truth.csv")

# Drop rows with empty labels
df = df.dropna(subset=["true_label"])
df = df[df["true_label"].str.strip() != ""]

print(f"Total labeled rows: {len(df)}")
print(f"Label distribution:\n{df['true_label'].value_counts()}")

# For now test the evaluation using true labels as predictions
# (next week your model predictions will replace y_pred)
y_true = df["true_label"].str.strip().tolist()
y_pred = y_true  # placeholder until model is ready

compute_metrics(y_true, y_pred)