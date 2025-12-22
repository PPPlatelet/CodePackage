import polars
import numpy as np
import torch

def test_polars():
    df = polars.DataFrame(
        {
            "a": [1, 2, 3, 4, 5],
            "b": [5, 4, 3, 2, 1],
        }
    )
    assert df.shape == (5, 2)
    assert df["a"].sum() == 15
    assert df["b"].sum() == 15
    assert df["a"].sum() == df["b"].sum()
