#!python3.13

import duckdb
import pandas as pd
import tabulate

def main():
	con: duckdb.DuckDBPyConnection = duckdb.connect("main.duckdb")
	con.sql("INSTALL httpfs")
	con.sql("LOAD httpfs")

	try:
		con.sql("ATTACH 'https://data.baseball.computer/dbt/bc_remote.db' (READ_ONLY TRUE)")
	except Exception as e:
		print(f"Error attaching remote database: {e}")
		return

	con.sql("USE bc_remote")
	con.sql("USE main_models")

	df: pd.DataFrame = con.sql("SELECT MAX(date) FROM main_models.standings").df()

	print(tabulate.tabulate(df, headers=df.columns))


if __name__ == "__main__":
	main()
