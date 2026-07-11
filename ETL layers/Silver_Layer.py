# Databricks notebook source
from pyspark.sql.functions import col, lit, regexp_extract, expr

df_bronze_hotels = spark.table("default.bronze_hotels")
df_bronze_airbnb = spark.table("workspace.default.airbnb_v_2")
df_bronze_booking = spark.table("default.bronze_booking_live")
df_bronze_northy = spark.table("default.bronze_northy")

unified_df = (
    df_bronze_hotels.select(col("title").alias("name"), lit("North Coast, Egypt").alias("destination"), expr("cast(regexp_extract(price, '\\\\$(\\\\d+)', 1) as double) * 48.0").alias("price_egp"), expr("cast(regexp_extract(rate, '^(\\\\d+\\\\.\\\\d+|\\\\d+)', 1) as double)").alias("rating"), col("link").alias("url"), lit("Hotels.com").alias("source_website"))
    .union(df_bronze_airbnb.select(col("title").alias("name"), lit("North Coast, Egypt").alias("destination"), expr("cast(replace(replace(regexp_extract(price, '([\\\\d,]+)', 1), ',', ''), 'EGP', '') as double)").alias("price_egp"), lit(8.0).cast("double").alias("rating"), col("link").alias("url"), lit("Airbnb").alias("source_website")))
    .union(df_bronze_booking.select("name", "destination", expr("cast(replace(replace(regexp_extract(price, '([\\\\d,]+)', 1), ',', ''), 'EGP', '') as double)").alias("price_egp"), expr("cast(regexp_extract(rating, '(\\\\d+\\\\.\\\\d+|\\\\d+)', 1) as double)").alias("rating"), "url", "source_website"))
    .union(df_bronze_northy.select("name", "destination", expr("cast(replace(replace(cast(price as string), ',', ''), 'EGP', '') as double)").alias("price_egp"), expr("cast(regexp_extract(cast(rating as string), '(\\\\d+\\\\.\\\\d+|\\\\d+)', 1) as double)").alias("rating"), "url", lit("Booking").alias("source_website")))
)

cleaned_final_df = unified_df.dropna(subset=["name", "price_egp"]).dropDuplicates(["url"])
cleaned_final_df.write.format("delta").mode("overwrite").saveAsTable("default.silver_booking_cleaned")

# COMMAND ----------

from pyspark.sql.functions import col, lit, expr

df_silver = (
    spark.table("default.bronze_hotels")
    .select(
        col("title").alias("name"), 
        lit("North Coast, Egypt").alias("destination"), 
        expr("cast(regexp_extract(price, '\\\\$(\\\\d+)', 1) as double) * 48.0").alias("price_egp"), 
        expr("cast(regexp_extract(rate, '^(\\\\d+\\\\.\\\\d+|\\\\d+)', 1) as double)").alias("rating"), 
        col("link").alias("url"), 
        lit("Hotels.com").alias("source_website")
    )
    .union(
        spark.table("default.bronze_airbnb")
        .select(
            col("title").alias("name"), 
            lit("North Coast, Egypt").alias("destination"), 
            expr("cast(replace(replace(regexp_extract(price, '([\\\\d,]+)', 1), ',', ''), 'EGP', '') as double)").alias("price_egp"), 
            lit(8.0).cast("double").alias("rating"), 
            col("link").alias("url"), 
            lit("Airbnb").alias("source_website")
        )
    )
    .union(
        spark.table("default.bronze_booking_live")
        .select(
            "name", 
            "destination", 
            expr("cast(replace(replace(regexp_extract(price, '([\\\\d,]+)', 1), ',', ''), 'EGP', '') as double)").alias("price_egp"), 
            expr("cast(regexp_extract(rating, '(\\\\d+\\\\.\\\\d+|\\\\d+)', 1) as double)").alias("rating"), 
            col("url").alias("url"), 
            lit("Booking").alias("source_website")
        )
    )
)

df_silver.write.format("delta").mode("overwrite").saveAsTable("default.silver_booking_cleaned")

# COMMAND ----------

display(df_silver)

# COMMAND ----------

from pyspark.sql.functions import col, lit, expr

df_silver = (
    spark.table("default.bronze_hotels")
    .select(
        col("title").alias("name"), 
        lit("North Coast, Egypt").alias("destination"), 
        expr("cast(regexp_extract(price, '\\\\$(\\\\d+)', 1) as double) * 48.0").alias("price_egp"), 
        expr("cast(regexp_extract(rate, '^(\\\\d+\\\\.\\\\d+|\\\\d+)', 1) as double)").alias("rating"), 
        col("link").alias("url"), 
        lit("Hotels.com").alias("source_website"),
        col("img").alias("image_url")
    )
    .union(
        spark.table("default.bronze_airbnb")
        .select(
            col("title").alias("name"), 
            lit("North Coast, Egypt").alias("destination"), 
            expr("cast(replace(replace(regexp_extract(price, '([\\\\d,]+)', 1), ',', ''), 'EGP', '') as double)").alias("price_egp"), 
            lit(8.0).cast("double").alias("rating"), 
            col("link").alias("url"), 
            lit("Airbnb").alias("source_website"),
            col("img").alias("image_url")
        )
    )
    .union(
        spark.table("default.bronze_booking_live")
        .select(
            "name", 
            "destination", 
            expr("cast(replace(replace(regexp_extract(price, '([\\\\d,]+)', 1), ',', ''), 'EGP', '') as double)").alias("price_egp"), 
            expr("cast(regexp_extract(rating, '(\\\\d+\\\\.\\\\d+|\\\\d+)', 1) as double)").alias("rating"), 
            col("url").alias("url"), 
            lit("Booking").alias("source_website"),
            lit(None).alias("image_url")
        )
    )
)

df_silver.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("default.silver_booking_cleaned")

# COMMAND ----------

from pyspark.sql.functions import avg,round, col
avrg=df_silver.select(avg("rating")).first()[0]
df_silver=df_silver.fillna({"rating":avrg})
df_silver=df_silver.withColumn("rating",round(col("rating"),1))

# COMMAND ----------

display(df_silver)