# Databricks notebook source
from pyspark.sql.functions import col, round, avg, count

df_silver = spark.table("default.silver_booking_cleaned").filter((col("price_egp") > 100) & (col("price_egp") < 1000000))

df_gold_final = df_silver.groupBy("destination", "source_website").agg(
    count("name").alias("total_hotels"),
    round(avg("price_egp"), 2).alias("avg_price"),
    round(avg("rating"), 2).alias("avg_rating")
).orderBy(col("avg_price").desc())

df_gold_final.write.format("delta").mode("overwrite").saveAsTable("default.gold_booking_analytics")

display(df_gold_final)

# COMMAND ----------

from pyspark.sql.functions import round, avg, count, col

df_gold = spark.table("default.silver_booking_cleaned").filter(
    (col("price_egp") > 100) & (col("price_egp") < 1000000)
)

df_gold_final = df_gold.groupBy("destination", "source_website").agg(
    count("name").alias("total_hotels"),
    round(avg("price_egp"), 2).alias("avg_price"),
    round(avg("rating"), 2).alias("avg_rating")
).orderBy(col("avg_price").desc())

df_gold_final.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("default.gold_booking_analytics")

display(df_gold_final)

# COMMAND ----------

df_gold_pandas = spark.table("default.gold_booking_analytics").toPandas()

df_gold_pandas.to_csv("/tmp/final_booking_visualization.csv", index=False)

print("تم")
print("file:/tmp/final_booking_visualization.csv")

# COMMAND ----------

from pyspark.sql.functions import round, avg, count, col, first

df_silver = spark.table("default.silver_booking_cleaned")

df_gold_final = df_silver.groupBy("destination", "source_website").agg(
    count("name").alias("total_hotels"),
    round(avg("price_egp"), 2).alias("avg_price"),
    round(avg("rating"), 2).alias("avg_rating"),
    first("image_url").alias("sample_image") 
).orderBy(col("avg_price").desc())

df_gold_final.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("default.gold_booking_analytics")

display(df_gold_final)

# COMMAND ----------

display(df_gold_final)