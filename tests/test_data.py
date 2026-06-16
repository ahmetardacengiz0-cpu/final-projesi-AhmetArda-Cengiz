from src.data import load_data, prepare_xy


def test_dataset_shape_and_required_columns():
    df = load_data()
    assert len(df) == 649
    assert {"G1", "G2", "G3", "absences"}.issubset(df.columns)


def test_binary_target_contains_both_classes():
    X, y = prepare_xy(load_data())
    assert len(X) == len(y)
    assert set(y.unique()) == {0, 1}
    assert y.sum() > 0
