from sqlalchemy import create_engine, inspect, text
import pandas as pd

class DBInspector:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.inspector = inspect(self.engine)

    def get_tables(self) -> list[str]:
        return self.inspector.get_table_names()

    def get_table_context(self, table: str) -> dict:
        """Build rich context dict for AI prompt."""
        columns = self.inspector.get_columns(table)
        pk = self.inspector.get_pk_constraint(table)
        fks = self.inspector.get_foreign_keys(table)
        indexes = self.inspector.get_indexes(table)

        col_details = []
        for c in columns:
            col_details.append({
                "name":     c["name"],
                "type":     str(c["type"]),
                "nullable": c.get("nullable", True),
                "default":  str(c.get("default","")) or "",
                "is_pk":    c["name"] in (pk.get("constrained_columns") or [])
            })

        sample_data, row_count = [], 0
        try:
            with self.engine.connect() as conn:
                row_count = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table}")
                ).scalar()
                df = pd.read_sql(
                    f"SELECT * FROM {table} LIMIT 5", conn)
                sample_data = df.to_dict(orient="records")
        except Exception:
            pass

        fk_desc = [
            f"{f['constrained_columns']} → "
            f"{f['referred_table']}.{f['referred_columns']}"
            for f in fks
        ]

        return {
            "table":      table,
            "row_count":  row_count,
            "columns":    col_details,
            "primary_key": pk.get("constrained_columns", []),
            "foreign_keys": fk_desc,
            "indexes":    [i["name"] for i in indexes],
            "sample_rows": sample_data[:3]
        }