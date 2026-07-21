# show_data.py
# This connects to Databricks and PRINTS some rows of data.
# It only READS data. It does not change or delete anything. Safe to run.

from databricks.connect import DatabricksSession

print("Connecting to Databricks... (this can take ~30 seconds the first time)")
spark = DatabricksSession.builder.serverless(True).getOrCreate()
print("Connected!\n")

# ---- This is the "data selection". It just asks for 10 rows from a table. ----
query = "SELECT * FROM samples.bakehouse.sales_transactions LIMIT 10"

print("Asking Databricks for data with this query:")
print("   " + query + "\n")

spark.sql(query).show()   # <-- this line prints the table of results

print("\nDone! That table above is your data. 🎉")

# ---------------------------------------------------------------------------
# Want to try something else? Replace the query line above with one of these:
#
#   query = "SELECT * FROM samples.nyctaxi.trips LIMIT 10"
#
#   query = ("SELECT product, SUM(quantity) AS total_units "
#            "FROM samples.bakehouse.sales_transactions "
#            "GROUP BY product ORDER BY total_units DESC LIMIT 10")
# ---------------------------------------------------------------------------
