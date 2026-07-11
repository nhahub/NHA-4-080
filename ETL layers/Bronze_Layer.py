# Databricks notebook source
df_hotels = spark.table("default.hotels")
df_airbnb = spark.table("workspace.default.airbnb_v_2")
df_booking_live = spark.table("default.mediterranean_hotels_egypt_only")
df_northy = spark.table("default.booking_results_20260701_112914")

df_hotels.write.format("delta").mode("overwrite").saveAsTable("default.bronze_hotels")
df_airbnb.write.format("delta").mode("overwrite").saveAsTable("default.bronze_airbnb")
df_booking_live.write.format("delta").mode("overwrite").saveAsTable("default.bronze_booking_live")
df_northy.write.format("delta").mode("overwrite").saveAsTable("default.bronze_northy")

# COMMAND ----------

display(df_airbnb)