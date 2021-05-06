// Databricks notebook source
// STARTER CODE - DO NOT EDIT THIS CELL
import org.apache.spark.sql.functions.desc
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import spark.implicits._
import org.apache.spark.sql.expressions.Window

// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
val customSchema = StructType(Array(StructField("lpep_pickup_datetime", StringType, true), StructField("lpep_dropoff_datetime", StringType, true), StructField("PULocationID", IntegerType, true), StructField("DOLocationID", IntegerType, true), StructField("passenger_count", IntegerType, true), StructField("trip_distance", FloatType, true), StructField("fare_amount", FloatType, true), StructField("payment_type", IntegerType, true)))

// COMMAND ----------

// STARTER CODE - YOU CAN LOAD ANY FILE WITH A SIMILAR SYNTAX.
val df = spark.read
   .format("com.databricks.spark.csv")
   .option("header", "true") // Use first line of all files as header
   .option("nullValue", "null")
   .schema(customSchema)
   .load("/FileStore/tables/nyc_tripdata.csv") // the csv file which you want to work with
   .withColumn("pickup_datetime", from_unixtime(unix_timestamp(col("lpep_pickup_datetime"), "MM/dd/yyyy HH:mm")))
   .withColumn("dropoff_datetime", from_unixtime(unix_timestamp(col("lpep_dropoff_datetime"), "MM/dd/yyyy HH:mm")))
   .drop($"lpep_pickup_datetime")
   .drop($"lpep_dropoff_datetime")

// COMMAND ----------

// LOAD THE "taxi_zone_lookup.csv" FILE SIMILARLY AS ABOVE. CAST ANY COLUMN TO APPROPRIATE DATA TYPE IF NECESSARY.

// ENTER THE CODE BELOW
val customSchema2 = StructType(Array(StructField("LocationID", IntegerType, true), StructField("Borough", StringType, true), StructField("Zone", StringType, true), StructField("service_zone", StringType, true)))
val ds2 = spark.read
   .format("com.databricks.spark.csv")
   .option("header", "true") // Use first line of all files as header
   .option("nullValue", "null")
   .schema(customSchema2)
   .load("/FileStore/tables/taxi_zone_lookup.csv") // the csv file which you want to work with

// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
// Some commands that you can use to see your dataframes and results of the operations. You can comment the df.show(5) and uncomment display(df) to see the data differently. You will find these two functions useful in reporting your results.
// display(df)
df.show(5) // view the first 5 rows of the dataframe

// COMMAND ----------

// STARTER CODE - DO NOT EDIT THIS CELL
// Filter the data to only keep the rows where "PULocationID" and the "DOLocationID" are different and the "trip_distance" is strictly greater than 2.0 (>2.0).

// VERY VERY IMPORTANT: ALL THE SUBSEQUENT OPERATIONS MUST BE PERFORMED ON THIS FILTERED DATA

val df_filter = df.filter($"PULocationID" =!= $"DOLocationID" && $"trip_distance" > 2.0)
df_filter.show(5)

// COMMAND ----------

// PART 1a: The top-5 most popular drop locations - "DOLocationID", sorted in descending order - if there is a tie, then one with lower "DOLocationID" gets listed first
// Output Schema: DOLocationID int, number_of_dropoffs int 

// Hint: Checkout the groupBy(), orderBy() and count() functions.

// ENTER THE CODE BELOW
val df1a = df_filter.groupBy(col("DOLocationID")).count().orderBy(desc("count"),asc("DOLocationID")).limit(5).withColumnRenamed("count","number_of_dropoffs")
df1a.show(5)

// COMMAND ----------

// PART 1b: The top-5 most popular pickup locations - "PULocationID", sorted in descending order - if there is a tie, then one with lower "PULocationID" gets listed first 
// Output Schema: PULocationID int, number_of_pickups int

// Hint: Code is very similar to part 1a above.

// ENTER THE CODE BELOW
val df1b = df_filter.groupBy(col("PULocationID")).count().orderBy(desc("count"),asc("PULocationID")).limit(5).withColumnRenamed("count","number_of_pickups")
df1b.show(5)

// COMMAND ----------

// PART 2: List the top-3 locations with the maximum overall activity, i.e. sum of all pickups and all dropoffs at that LocationID. In case of a tie, the lower LocationID gets listed first.
// Output Schema: LocationID int, number_activities int

// Hint: In order to get the result, you may need to perform a join operation between the two dataframes that you created in earlier parts (to come up with the sum of the number of pickups and dropoffs on each location). 

// ENTER THE CODE BELOW
val df2atemp = df_filter.groupBy(col("DOLocationID")).count().orderBy(desc("count"),asc("DOLocationID")).withColumnRenamed("count","number_of_dropoffs")
val df2btemp = df_filter.groupBy(col("PULocationID")).count().orderBy(desc("count"),asc("PULocationID")).withColumnRenamed("count","number_of_pickups").withColumnRenamed("count","number_of_dropoffs")
val df2 = df2atemp.join(df2btemp,$"DOLocationID" === $"PULocationID").withColumn("number_activities",$"number_of_pickups"+$"number_of_dropoffs").drop("number_of_pickups","PULocationID","number_of_dropoffs").withColumnRenamed("DOLocationID","LocationID").orderBy(desc("number_activities"),asc("LocationID")).limit(3)
df2.show(5)

// COMMAND ----------

// PART 3: List all the boroughs in the order of having the highest to lowest number of activities (i.e. sum of all pickups and all dropoffs at that LocationID), along with the total number of activity counts for each borough in NYC during that entire period of time.
// Output Schema: Borough string, total_number_activities int

// Hint: You can use the dataframe obtained from the previous part, and will need to do the join with the 'taxi_zone_lookup' dataframe. Also, checkout the "agg" function applied to a grouped dataframe.

// ENTER THE CODE BELOW
val df2temp = df2atemp.join(df2btemp,$"DOLocationID" === $"PULocationID").withColumn("number_activities",$"number_of_pickups"+$"number_of_dropoffs").drop("number_of_pickups","PULocationID","number_of_dropoffs").withColumnRenamed("DOLocationID","LocationID").orderBy(desc("number_activities"),asc("LocationID")).withColumnRenamed("LocationID","LocationID2")
val df3 = df2temp.join(ds2,$"LocationID" === $"LocationID2","left_outer").drop("LocationID2","LocationID","Zone","service_zone").groupBy("Borough").agg(sum("number_activities")).withColumnRenamed("sum(number_activities)","total_number_activities").orderBy(desc("total_number_activities"))
df3.show(10)

// COMMAND ----------

// PART 4: List the top 2 days of week with the largest number of (daily) average pickups, along with the values of average number of pickups on each of the two days. The day of week should be a string with its full name, for example, "Monday" - not a number 1 or "Mon" instead.
// Output Schema: day_of_week string, avg_count float

// Hint: You may need to group by the "date" (without time stamp - time in the day) first. Checkout "to_date" function.

// ENTER THE CODE BELOW
val df4 = df_filter.withColumn("day_of_week",date_format($"pickup_datetime", "EEEE")).withColumn("day",date_format($"pickup_datetime", "YYYY-mm-dd")).drop("DOLocationID","passenger_count","trip_distance","fare_amount","payment_type","dropoff_datetime").groupBy("day","day_of_week").agg(count("PULocationID")).groupBy("day_of_week").agg(avg("count(PULocationID)")).withColumnRenamed("avg(count(PULocationID))","avg_count").orderBy(desc("avg_count")).limit(2)
df4.show(5)

// COMMAND ----------

// PART 5: For each particular hour of a day (0 to 23, 0 being midnight) - in their order from 0 to 23, find the zone in Brooklyn borough with the LARGEST number of pickups. 
// Output Schema: hour_of_day int, zone string, max_count int

// Hint: You may need to use "Window" over hour of day, along with "group by" to find the MAXIMUM count of pickups

// ENTER THE CODE BELOW
val df5temp = ds2.withColumnRenamed("LocationID","LocationID2")
val df5 = df_filter.join(df5temp,$"PULocationID" === $"LocationID2","left_outer").drop("LocationID2","DOLocationID","passenger_count","trip_distance","fare_amount","payment_type","service_zone","dropoff_datetime","PULocationID").filter($"Borough"==="Brooklyn").drop("Borough").withColumn("hour_of_day",hour(to_date(to_timestamp(unix_timestamp($"pickup_datetime", "yyyy-MM-dd HH:mm:ss"))))).groupBy("hour_of_day","Zone").agg(count("pickup_datetime")).orderBy(asc("hour_of_day"),desc("count(pickup_datetime)"))
val df5result = df5.groupBy("hour_of_day").agg(max("count(pickup_datetime)") as "max_count").join(df5,Seq("hour_of_day")).where($"count(pickup_datetime)" === $"max_count").drop("max_count").withColumnRenamed("count(pickup_datetime)","max_count")
//df5result.show(20)
//df5.collect.foreach(println)
df5.show()
//val w = Window.orderBy(col("hour_of_day"))
//val w = Window.partitionBy($"hour_of_day").orderBy($"count(pickup_datetime)".desc)
//val dfMax = df5.withColumn("rn", row_number.over(w)).where($"rn" === 1).drop("rn")
//val dfMax = df5.groupBy($"hour_of_day".as("max_hour")).agg(max($"count(pickup_datetime)").as("max_count"))

//val dfTopByJoin = df5.join(broadcast(dfMax),
 //   ($"hour_of_day" === $"max_hour") && ($"count(pickup_datetime)" === $"max_count"))
 // .drop("max_hour")
 // .drop("max_value")
//dfTopByJoin.show(10)
//val byHour = df5.groupBy("hour_of_day","Zone").agg("count(pickup_datetime)")//.over(w)//.withColumn("max_count",max("count(pickup_datetime)").over(w)).orderBy(desc("max_count"))//.limit(24)
//byHour.show(24)

// COMMAND ----------

// PART 6 - Find which 3 different days of the January, in Manhattan, saw the largest percentage increment in pickups compared to previous day, in the order from largest increment % to smallest increment %. 
// Print the day of month along with the percent CHANGE (can be negative), rounded to 2 decimal places, in number of pickups compared to previous day.
// Output Schema: day int, percent_change float

// Hint: You might need to use lag function, over a window ordered by day of month.

// ENTER THE CODE BELOW
val df6temp = ds2.withColumnRenamed("LocationID","LocationID2")
val df6 = df_filter.join(df6temp,$"PULocationID" === $"LocationID2","left_outer").drop("LocationID2","DOLocationID","passenger_count","trip_distance","fare_amount","payment_type","service_zone","dropoff_datetime","PULocationID","Zone").withColumn("Datetime", (unix_timestamp($"pickup_datetime", "yyyy-MM-dd HH:mm:ss"))).withColumn("day", date_format(to_date(to_timestamp(unix_timestamp($"pickup_datetime", "yyyy-MM-dd HH:mm:ss"))),"dd")).withColumn("month", date_format(to_date(to_timestamp(unix_timestamp($"pickup_datetime", "yyyy-MM-dd HH:mm:ss"))),"MM")).filter($"Borough"==="Manhattan").filter($"month"==="01").drop("pickup_datetime","Borough").groupBy("day").agg(count("day") as "count").orderBy("day")
val w = Window.orderBy(col("day"))
val byDay = df6.withColumn("prev_count",lag(col("count"),1).over(w)).withColumn("percent_change",(($"count"-$"prev_count")/$"prev_count")*100).orderBy(desc("percent_change")).drop("count","prev_count").limit(3)
val byDay2 = df6.withColumn("prev_count",lag(col("count"),1).over(w)).withColumn("percent_change",(($"count"-$"prev_count")/$"prev_count")*100).orderBy(asc("percent_change")).drop("count","prev_count").limit(4)
byDay.show(10)
byDay2.show(10)
