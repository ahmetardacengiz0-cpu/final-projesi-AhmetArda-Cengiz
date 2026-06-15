from src.model import train_and_save


if __name__ == "__main__":
    _, metrics = train_and_save()
    selected = metrics["selected_model"]
    test = metrics["models"][selected]["test"]
    print(f"Seçilen model: {selected}")
    print(f"Test ROC-AUC: {test['roc_auc']}")
    print(f"Risk recall: {test['recall_risk']}")
    print("Model ve metrikler artifacts/ klasörüne kaydedildi.")
