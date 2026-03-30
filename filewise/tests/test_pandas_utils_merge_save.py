import pandas as pd
import pytest

from filewise.pandas_utils import data_manipulation as dm
from filewise.pandas_utils import pandas_obj_handler as poh


def test_concat_dfs_aux_axis0_default_and_dedup(tmp_path):
    file1 = tmp_path / "a.csv"
    file2 = tmp_path / "b.csv"
    pd.DataFrame({"x": [1, 2], "y": ["a", "b"]}).to_csv(file1, index=False)
    pd.DataFrame({"x": [2, 3], "y": ["b", "c"]}).to_csv(file2, index=False)

    merged = dm.concat_dfs_aux(
        input_file_list=[str(file1), str(file2)],
        separator_in=",",
        engine="python",
        encoding=None,
        header=0,
        parse_dates=False,
        index_col=None,
        decimal=".",
        drop_duplicates=True,
    )

    assert list(merged.columns) == ["x", "y"]
    assert merged.to_dict(orient="records") == [
        {"x": 1, "y": "a"},
        {"x": 2, "y": "b"},
        {"x": 3, "y": "c"},
    ]


def test_save2csv_fallback_delete_recreate_when_replace_fails(tmp_path, monkeypatch):
    out_file = tmp_path / "out.csv"
    first_df = pd.DataFrame({"v": [1]})
    second_df = pd.DataFrame({"v": [2]})

    assert poh.save2csv(str(out_file), first_df, separator=",", save_header=True) == 0

    monkeypatch.setattr(poh.os, "replace", lambda src, dst: (_ for _ in ()).throw(OSError("replace failed")))
    monkeypatch.setattr("builtins.input", lambda _: "y")

    assert poh.save2csv(str(out_file), second_df, separator=",", save_header=True) == 0
    reloaded = pd.read_csv(out_file)
    assert reloaded["v"].tolist() == [2]


def test_merge_excel_files_handles_duplicate_sheet_names(monkeypatch):
    file_a = "/tmp/a.xlsx"
    file_b = "/tmp/b.xlsx"

    df_a = pd.DataFrame({"v": [1]})
    df_b = pd.DataFrame({"v": [2]})
    df_c = pd.DataFrame({"v": [3]})

    def fake_excel_handler(file_path, **kwargs):
        if file_path == file_a:
            return {"sheet1": df_a, "other": df_b}
        if file_path == file_b:
            return {"sheet1": df_c}
        raise AssertionError("Unexpected file path")

    monkeypatch.setattr(poh, "excel_handler", fake_excel_handler)

    merged = poh.merge_excel_files(
        input_file_list=[file_a, file_b],
        output_file_path="/tmp/out.xlsx",
        save_merged_file=False,
    )

    assert set(merged.keys()) == {"sheet1", "other", "sheet1_b"}
    assert merged["sheet1"].equals(df_a)
    assert merged["other"].equals(df_b)
    assert merged["sheet1_b"].equals(df_c)


def test_merge_excel_files_out_single_dataframe_axis0_with_dedup(monkeypatch):
    file_a = "/tmp/a.xlsx"
    file_b = "/tmp/b.xlsx"

    def fake_excel_handler(file_path, **kwargs):
        if file_path == file_a:
            return {"sheet1": pd.DataFrame({"x": [1, 2]})}
        if file_path == file_b:
            return {"sheet1": pd.DataFrame({"x": [2, 3]})}
        raise AssertionError("Unexpected file path")

    monkeypatch.setattr(poh, "excel_handler", fake_excel_handler)

    merged = poh.merge_excel_files(
        input_file_list=[file_a, file_b],
        output_file_path="/tmp/out.xlsx",
        out_single_DataFrame=True,
        axis=0,
        drop_duplicates=True,
        save_merged_file=False,
    )

    assert isinstance(merged, pd.DataFrame)
    assert merged["x"].tolist() == [1, 2, 3]


def test_merge_csv_files_axis1_user_cancel_raises(tmp_path, monkeypatch):
    file1 = tmp_path / "a.csv"
    file2 = tmp_path / "b.csv"
    pd.DataFrame({"x": [1, 2]}).to_csv(file1, index=False)
    pd.DataFrame({"x": [3]}).to_csv(file2, index=False)

    monkeypatch.setattr("builtins.input", lambda _: "n")

    with pytest.raises(ValueError, match="cancelled"):
        poh.merge_csv_files(
            input_file_list=[str(file1), str(file2)],
            output_file_path=str(tmp_path / "out.csv"),
            separator_in=",",
            header=0,
            axis=1,
            out_single_DataFrame=True,
            keep_data_in_sections=False,
            save_merged_file=False,
        )
