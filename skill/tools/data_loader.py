"""
data_loader.py — Unified ingestion for CSV/Excel
Normalizes columns, validates schema, returns standardized structures
"""

from typing import Dict, List, Optional, Tuple, Any
import re

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


# Column normalization map: varied inputs -> canonical names
COLUMN_MAP = {
    # Revenue variants
    "revenue": "revenue", "sales": "revenue", "income": "revenue", "turnover": "revenue",
    "إيراد": "revenue", "ايراد": "revenue", "المبيعات": "revenue",
    # COR
    "cogs": "cogs", "cor": "cogs", "cost_of_revenue": "cogs", "cost of revenue": "cogs",
    "cost": "cogs", "تكلفة": "cogs",
    # Units
    "units": "units", "total_units": "total_units", "sold": "sold_units", "sold_units": "sold_units",
    "available": "available_units",
    # Area
    "area": "area", "sellable_area": "sellable_area", "bua": "bua", "built_up_area": "bua",
    # Price
    "price": "price", "price_per_unit": "price_per_unit", "price_per_sqm": "price_per_sqm",
    # Cash flow
    "inflow": "inflow", "inflows": "inflow", "outflow": "outflow", "outflows": "outflow",
    "collections": "collections", "collected": "collected",
}


def normalize_columns(columns: List[str]) -> Dict[str, str]:
    """
    Map raw column names to canonical names.
    Lowercase, strip, replace spaces.
    """
    mapping = {}
    for col in columns:
        key = col.strip().lower().replace(" ", "_")
        # Direct map or fallback to key itself
        canonical = COLUMN_MAP.get(key, key)
        # Also try without underscores
        if canonical == key:
            # Try lookup with original lower
            canonical = COLUMN_MAP.get(col.strip().lower(), key)
        mapping[col] = canonical
    return mapping


def load_csv(filepath: str, **kwargs) -> Any:
    """Load CSV via pandas if available, else fallback to csv module"""
    if HAS_PANDAS:
        try:
            df = pd.read_csv(filepath, **kwargs)
            return df
        except Exception as e:
            raise ValueError(f"Failed to load CSV {filepath}: {e}")
    else:
        import csv
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            # Simulate minimal DataFrame-like: return list of dicts
            return rows


def load_excel(filepath: str, sheet_name: int | str = 0, **kwargs) -> Any:
    if not HAS_PANDAS:
        raise ImportError("pandas required for Excel loading")
    if not HAS_OPENPYXL:
        raise ImportError("openpyxl required for Excel loading")
    df = pd.read_excel(filepath, sheet_name=sheet_name, engine="openpyxl", **kwargs)
    return df


def validate_schema(df, required_columns: List[str]) -> Tuple[bool, List[str]]:
    """
    Check if normalized df has required columns.
    Returns (is_valid, missing_columns)
    """
    if HAS_PANDAS and hasattr(df, 'columns'):
        cols = [c.lower().strip() for c in df.columns]
        # Normalize required similarly
        missing = []
        for req in required_columns:
            # Check if any col maps to req via COLUMN_MAP
            # Simple: check if req in cols or any mapped col == req
            normalized = [COLUMN_MAP.get(c, c) for c in cols]
            if req not in normalized and req not in cols:
                missing.append(req)
        return (len(missing) == 0, missing)
    else:
        # List of dicts fallback
        if not df:
            return (False, required_columns)
        cols = [k.lower().strip() for k in df[0].keys()]
        missing = [r for r in required_columns if r not in cols]
        return (len(missing) == 0, missing)


def df_to_records(df) -> List[Dict]:
    """Convert DataFrame or list to list of dicts with normalized keys"""
    if HAS_PANDAS and hasattr(df, 'to_dict'):
        # Normalize columns first
        col_map = normalize_columns(list(df.columns))
        df_renamed = df.rename(columns=col_map)
        # Strip whitespace from string columns
        records = df_renamed.to_dict(orient="records")
        return records
    elif isinstance(df, list):
        # Already list of dicts, normalize keys
        normalized = []
        for row in df:
            new_row = {}
            for k, v in row.items():
                nk = COLUMN_MAP.get(k.strip().lower().replace(" ", "_"), k.strip().lower().replace(" ", "_"))
                new_row[nk] = v
            normalized.append(new_row)
        return normalized
    else:
        return []


def clean_numeric_series(series, fill_na: float = 0.0) -> List[float]:
    """Clean numeric: handle commas, currency symbols, empty"""
    cleaned = []
    for v in series:
        if v is None or (HAS_PANDAS and pd.isna(v)):
            cleaned.append(fill_na)
            continue
        if isinstance(v, (int, float)):
            cleaned.append(float(v))
            continue
        s = str(v).strip().replace(",", "").replace("EGP", "").replace("SAR", "").replace("$", "").strip()
        if s == "" or s == "-":
            cleaned.append(fill_na)
            continue
        try:
            cleaned.append(float(s))
        except:
            cleaned.append(fill_na)
    return cleaned
