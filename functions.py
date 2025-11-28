# functions.py
"""
Malaysian Tax Input Program - Functions Module
Author: <Your Name>
Course: SQITK 3073 Business Analytic Programming

This module contains helper functions for:
- user verification
- tax calculation (Malaysia YA2024 onwards brackets)
- CSV read/write using pandas
"""

import os
import pandas as pd


def verify_user(ic_number: str, password: str) -> bool:
    """
    Verify IC and password rules:
    - IC must be exactly 12 digits (numbers only)
    - password must match last 4 digits of IC
    """
    if not ic_number.isdigit() or len(ic_number) != 12:
        return False
    return password == ic_number[-4:]


def calculate_tax(income: float, tax_relief: float) -> float:
    """
    Calculate tax payable based on Malaysian resident tax rates
    for YA 2024 onwards.

    Chargeable income = income - tax_relief
    Progressive tax brackets (resident):
      0 – 5,000            : 0%
      5,001 – 20,000       : 1%
      20,001 – 35,000      : 3%
      35,001 – 50,000      : 6%
      50,001 – 70,000      : 11%
      70,001 – 100,000     : 19%
      100,001 – 400,000    : 25%
      400,001 – 600,000    : 26%
      600,001 – 2,000,000  : 28%
      > 2,000,000          : 30%
    Sources: LHDN / PwC tax summaries YA2024 onwards. 
    """
    chargeable = max(0.0, income - tax_relief)

    brackets = [
        (0, 5000, 0.00),
        (5000, 20000, 0.01),
        (20000, 35000, 0.03),
        (35000, 50000, 0.06),
        (50000, 70000, 0.11),
        (70000, 100000, 0.19),
        (100000, 400000, 0.25),
        (400000, 600000, 0.26),
        (600000, 2000000, 0.28),
        (2000000, float("inf"), 0.30),
    ]

    tax = 0.0
    for lower, upper, rate in brackets:
        if chargeable > lower:
            taxable_part = min(chargeable, upper) - lower
            tax += taxable_part * rate
        else:
            break

    return round(tax, 2)


def save_to_csv(data: dict, filename: str) -> None:
    """
    Save user tax record to CSV using pandas.
    - If file doesn't exist, create with header.
    - If exists, append row.
    """
    df_new = pd.DataFrame([data])

    if not os.path.exists(filename):
        df_new.to_csv(filename, index=False)
    else:
        df_old = pd.read_csv(filename)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
        df_all.to_csv(filename, index=False)


def read_from_csv(filename: str):
    """
    Read records CSV and return DataFrame.
    If file doesn't exist, return None.
    """
    if not os.path.exists(filename):
        return None
    return pd.read_csv(filename)
