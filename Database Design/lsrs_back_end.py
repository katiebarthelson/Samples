import os
import json
from datetime import datetime, date
from decimal import Decimal
from itertools import groupby

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

#######################
# SETUP
#######################

load_dotenv()
app = Flask(__name__)
CORS(app)

def env(key):
  return os.environ.get(key)

def sql_connection():
  #return psycopg2.connect(database=env('db'), user=env('user'), password=env('pw'),
                          #host=env('host'), port=env('port'))
  return psycopg2.connect(database='lsrs', user='postgres', password='B00b33$',
                          host='localhost', port='5432')

def json_serializer(obj):
  if isinstance(obj, (datetime, date)):
    return obj.isoformat()
  elif isinstance(obj, Decimal):
    return str(obj)
  raise TypeError ("Type %s not serializable" % type(obj))

def select_list_of_dicts(sql):
  with sql_connection() as connection:
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
      cursor.execute(sql)
      return cursor.fetchall()

def update_db(sql):
  with sql_connection() as connection:
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
      cursor.execute(sql)
      connection.commit()
      cursor.close()

def select_json(sql):
  return json.dumps(select_list_of_dicts(sql), default=json_serializer)

def extract_values_list_from_dicts(list_of_dicts, dict_key):
  return [d[dict_key] for d in list_of_dicts]

#######################
# ROUTES
#######################


@app.route('/mainmenu')
def main_menu():
    campaign_count = select_list_of_dicts("""
      SELECT COUNT(campaign_description) AS campaign_count FROM advertising_campaign;
    """)
    foodstores = select_list_of_dicts("""
      SELECT COUNT(store_number) AS food_store_count FROM store WHERE has_restaurant;
    """)
    products = select_list_of_dicts("""
      SELECT COUNT(pid) AS product_count FROM product;
    """)
    childstore_count = select_list_of_dicts("""
      SELECT COUNT(store_number) AS childcare_store_count FROM childcare_store;
    """)
    store_count = select_list_of_dicts("""
      SELECT COUNT(store_number) AS store_count FROM store;
    """)
    st = []
    st.append(campaign_count[0])
    st.append(foodstores[0])
    st.append(products[0])
    st.append(childstore_count[0])
    st.append(store_count[0])
    return json.dumps(st)

# MAIN MENU SUBTASKS
@app.route('/viewholiday')
def view_holiday():
  return select_json("""
    SELECT date, holiday_names FROM holiday;
  """)

@app.route('/updateholiday',methods=['GET','POST'])
def update_holiday():
    # test row
    json_data = json.loads('{"date": "2020-02-02","holiday_names": "WORDS222"}')
    #json_data = json.loads(request.get_json())
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    # Validate input
    try:
        date = json_data["date"]
        holiday_names = json_data["holiday_names"]
        query = f"""
        IF EXISTS(select date from holiday where date = DATE({date}))
            UPDATE holiday SET holiday_names = {holiday_names} WHERE date = DATE({date})
        ELSE
            INSERT into holiday(DATE({date})) values({holiday_names});
        """
        update_db(query)
    except ValidationError as err:
        return jsonify(err.messages), 422
    return jsonify({"message": "Updated Holiday."})

@app.route('/viewpopulation')
def view_population():
  return select_json("""
    SELECT city_name, state, population FROM city;
  """)

@app.route('/updatepopulation',methods=['GET','POST'])
def update_population():
    # test row
    #json_data = json.loads('{"city_name": "Atlanta","state": "GA","population":"1"}')
    json_data = json.loads(request.get_json())
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    # Validate input
    try:
        city_name = json_data["city_name"]
        state = json_data["state"]
        population = json_data["population"]
        query=f"""
        UPDATE city
        SET population = '{population}'
        WHERE city_name = '{city_name}' AND state = '{state}';
        """
        update_db(query)
    except ValidationError as err:
        return jsonify(err.messages), 422
    return jsonify({"message": "Updated City."})

@app.route('/report1')
def report1():
  return select_json("""
    SELECT
 		c.category_name,
		COUNT(p.pid) AS product_count,
		MIN(p.retail_price) AS min_retail_price,
		ROUND(AVG(p.retail_price), 2) AS avg_retail_price,
		MAX(p.retail_price) AS max_retail_price
	FROM category AS c
	INNER JOIN belongs_to AS bt ON bt.category_name = c.category_name
	INNER JOIN product AS p ON p.pid = bt.pid
	GROUP BY c.category_name
	ORDER BY c.category_name ASC;
  """)

@app.route('/report2')
def report2():
  return select_json("""
    WITH sales_with_totals AS (
		SELECT
			 s.store_number,
			 s.date,
			 s.pid,
			 s.quantity,
			 COALESCE(dis.discount_price, p.retail_price) AS sale_price,
			 COALESCE(dis.discount_price, p.retail_price) * s.quantity AS sale_total,
			 (NOT dis.discount_price IS NULL) AS is_discounted
		FROM sold AS s
		INNER JOIN date AS d ON d.date = s.date
		INNER JOIN product AS p ON p.pid = s.pid
		LEFT JOIN discounted_on AS dis ON dis.date = s.date AND dis.pid = s.pid
	)
	SELECT
		 p.pid,
		 p.product_name,
		 p.retail_price,
		 SUM(s.quantity) AS total_quantity_sold,
		 SUM(CASE WHEN s.is_discounted THEN s.quantity ELSE 0 END) AS discounted_quantity_sold,
		 SUM(CASE WHEN (NOT s.is_discounted) THEN s.quantity ELSE 0 END) AS not_discounted_quantity_sold,
		 SUM(s.sale_total) AS actual_revenue,
		 ROUND(SUM(s.quantity) * p.retail_price * 0.75, 2) AS predicted_revenue,
		 SUM(s.sale_total) - ROUND(SUM(s.quantity) * p.retail_price * 0.75, 2) AS revenue_difference
	FROM product AS p
	INNER JOIN sales_with_totals AS s ON s.pid = p.pid
	INNER JOIN belongs_to AS bt ON bt.pid = p.pid
	WHERE bt.category_name = 'Couches and Sofas'
	GROUP BY p.pid, p.product_name, p.retail_price
	HAVING ABS(SUM(s.sale_total) - ROUND(SUM(s.quantity) * p.retail_price * 0.75, 2)) > 5000
	ORDER BY revenue_difference DESC;
  """)

@app.route('/report3/<state>')
def report3(state=None):
  return select_json(f"""
    WITH sales_with_totals AS (
		SELECT
			 s.store_number,
			 s.date,
			 s.pid,
			 s.quantity,
			 COALESCE(dis.discount_price, p.retail_price) AS sale_price,
			 COALESCE(dis.discount_price, p.retail_price) * s.quantity AS sale_total,
			 (NOT dis.discount_price IS NULL) AS is_discounted
		FROM sold AS s
		INNER JOIN date AS d ON d.date = s.date
		INNER JOIN product AS p ON p.pid = s.pid
		LEFT JOIN discounted_on AS dis ON dis.date = s.date AND dis.pid = s.pid
	)
	SELECT
		 st.store_number,
		 st.street_address,
		 st.city_name,
		 SUM(so.sale_total) AS yearly_revenue,
		 EXTRACT(YEAR FROM so.date) AS sale_year
	FROM store AS st
	INNER JOIN sales_with_totals AS so ON so.store_number = st.store_number
	WHERE st.state = '{state}'
	GROUP BY st.store_number, st.street_address, st.city_name, sale_year
	ORDER BY sale_year ASC, yearly_revenue DESC;
  """)

@app.route('/report4')
def report4():
  return select_json("""
    SELECT
      EXTRACT(YEAR FROM s.date)::int as year,
      SUM(quantity) AS total_units_sold,
      ROUND(SUM(quantity)/365.0, 2) AS avg_quantity,
      SUM(CASE WHEN EXTRACT(MONTH FROM s.date) = 2 AND EXTRACT(DAY FROM s.date) = 2 THEN quantity ELSE 0 END) AS groundhog_day_sales
    FROM sold AS s
    LEFT JOIN belongs_to AS bt ON s.PID = bt.PID
    WHERE bt.category_name = 'Outdoor Furniture'
    GROUP BY EXTRACT(YEAR FROM s.date)
    ORDER BY Year ASC;
  """)

@app.route('/report5/<year>/<month>')
def report5(year=None, month=None):
  return select_json(f"""
    SELECT
      bt.category_name,
      st.state,
      SUM(s.quantity)
    FROM belongs_to bt
    LEFT JOIN sold s ON s.pid = bt.pid
    LEFT JOIN store st ON st.store_number = s.store_number
    WHERE EXTRACT(YEAR FROM s.date) = {year} AND EXTRACT(MONTH FROM s.date) = {month}
    GROUP BY bt.category_name, st.state
    ORDER BY bt.category_name;
  """)

@app.route('/report5/year')
def report5year(year=None, month=None):
   return select_json("""
    SELECT DISTINCT EXTRACT(YEAR FROM date)::int AS year FROM date;
  """)

@app.route('/report6')
def report6():
  return select_json("""
    WITH population_category AS (
      SELECT
        city_name,
        state,
        population,
        (CASE
          WHEN population < 3700000 THEN 'Small'
          WHEN population < 6700000 THEN 'Medium'
          WHEN population < 9000000 THEN 'Large'
          ELSE 'Extra Large'
        END) AS category
      FROM city
    ), sales_with_totals AS (
      SELECT
        s.store_number,
        s.date,
        s.pid,
        s.quantity,
        COALESCE(dis.discount_price, p.retail_price) AS sale_price,
        COALESCE(dis.discount_price, p.retail_price) * s.quantity AS sale_total,
        (NOT dis.discount_price IS NULL) AS is_discounted
      FROM sold AS s
      INNER JOIN Date AS d ON d.date = s.date
      INNER JOIN product AS p ON p.pid = s.pid
      LEFT JOIN discounted_on AS dis ON dis.date = s.date AND dis.pid = s.pid
    )
    SELECT
      EXTRACT(YEAR FROM s.date)::int AS year,
      SUM(CASE WHEN pc.category = 'Small' THEN s.sale_total ELSE 0 END) as small,
      SUM(CASE WHEN pc.category = 'Medium' THEN s.sale_total ELSE 0 END) as medium,
      SUM(CASE WHEN pc.category = 'Large' THEN s.sale_total ELSE 0 END) as large,
      SUM(CASE WHEN pc.category = 'Extra Large' THEN s.sale_total ELSE 0 END) as extra_large
    FROM sales_with_totals s
    INNER JOIN store st ON st.store_number = s.store_number
    INNER JOIN population_category pc ON pc.city_name = st.city_name AND pc.state = st.state
    GROUP BY EXTRACT(YEAR FROM s.date)
    ORDER BY year;
  """)

@app.route('/report7')
def report7():
  time_limit_rows = select_list_of_dicts('SELECT minutes FROM time_limit ORDER BY minutes ASC;')
  time_limits = extract_values_list_from_dicts(time_limit_rows, 'minutes')
  pivot_columns_clause = ', '.join([f'"{t}" NUMERIC' for t in time_limits])
  data = select_list_of_dicts(f"""
    SELECT * FROM crosstab('
    WITH sales_with_totals AS (
      SELECT
        s.store_number,
        s.date,
        s.pid,
        s.quantity,
        COALESCE(dis.discount_price, p.retail_price) AS sale_price,
        COALESCE(dis.discount_price, p.retail_price) * s.quantity AS sale_total,
        (NOT dis.discount_price IS NULL) AS is_discounted
      FROM sold AS s
      INNER JOIN Date AS d ON d.date = s.date
      INNER JOIN product AS p ON p.pid = s.pid
      LEFT JOIN discounted_on AS dis ON dis.date = s.date AND dis.pid = s.pid
    ), stores_childcare_categories AS (
      SELECT
        s.store_number,
        COALESCE(tl.minutes::text, ''No childcare'') AS childcare_category
      FROM store s
      LEFT JOIN childcare_store cs ON s.store_number = cs.store_number
      FULL OUTER JOIN time_limit tl ON cs.minutes = tl.minutes
    ), stores_childcare_months AS (
      SELECT DISTINCT
        s.store_number,
        s.childcare_category,
        date_trunc(''month'', d.date) as month
      FROM stores_childcare_categories s
      CROSS JOIN date d
      WHERE d.date > date_trunc(''month'', CURRENT_DATE) - INTERVAL ''1 year''
    )
    SELECT
      TO_CHAR(scm.month, ''Month'') || '' '' || EXTRACT(YEAR FROM scm.month) AS month,
      scm.childcare_category,
      COALESCE(SUM(s.sale_total), 0.00) AS sale_total
    FROM stores_childcare_months scm
    LEFT JOIN sales_with_totals s ON s.store_number = scm.store_number AND date_trunc(''month'', s.date) = scm.month
    GROUP BY scm.month, scm.childcare_category
    ORDER BY scm.month DESC, scm.childcare_category;')
    AS ct(sale_month TEXT, {pivot_columns_clause}, "no_childcare" NUMERIC);
  """)

  def pull_time_limits_into_list_of_dicts(row):
    return {
      'sale_month': row['sale_month'],
      'no_childcare': row['no_childcare'],
      'time_limit_cols': [{'limit': k, 'value': v} for k, v in row.items() if k.isdigit()]
    }

  return json.dumps([pull_time_limits_into_list_of_dicts(row) for row in data], default=json_serializer)

@app.route('/report8')
def report8():
  data = select_list_of_dicts("""
    WITH store_type_counts AS (
      SELECT
        bt.category_name,
        SUM(CASE WHEN st.has_restaurant THEN quantity ELSE 0 END) AS restaurant,
        SUM(CASE WHEN NOT st.has_restaurant THEN quantity ELSE 0 END) AS non_restaurant
      FROM store AS st
      LEFT JOIN sold AS s ON st.store_number = s.store_number
      LEFT JOIN belongs_to AS bt ON s.pid = bt.pid
      GROUP BY bt.category_name
    )
    SELECT
      category_name,
      'Restaurant' AS store_type,
      restaurant AS quantity_sold
    FROM store_type_counts
    UNION
    SELECT
      category_name,
      'Non-restaurant' AS store_type,
      non_restaurant AS quantity_sold
    FROM store_type_counts
    ORDER BY category_name, store_type;
  """)

  def row_without_category(row):
    return {'store_type': row['store_type'], 'quantity_sold': row['quantity_sold']}

  grouped_data = [{k: [row_without_category(x) for x in list(v)]} for (k, v) in groupby(data, key=lambda x: x['category_name'])]
  return json.dumps(grouped_data, default=json_serializer)

@app.route('/report9')
def report9():
  return select_json("""
    WITH campaign_sale_quantities AS (
      SELECT
        p.pid,
        p.product_name,
        SUM(CASE WHEN ao.date IS NOT NULL THEN quantity ELSE 0 END) AS sold_during_campaign,
        SUM(CASE WHEN ao.date IS NULL THEN quantity ELSE 0 END) AS sold_outside_campaign,
        SUM(CASE WHEN ao.date IS NOT NULL THEN quantity ELSE 0 END) - SUM(CASE WHEN ao.date IS NULL THEN Quantity ELSE 0 END) AS ad_difference
      FROM product AS p
      INNER JOIN sold AS s ON s.pid = p.pid
      LEFT JOIN active_on AS ao ON ao.date = s.date
      GROUP BY p.pid, p.product_name
    ), top10 AS (
      SELECT
        *
      FROM campaign_sale_quantities
      ORDER BY ad_difference DESC
      LIMIT 10
    ), bottom10 AS (
      SELECT
        *
      FROM campaign_sale_quantities
      ORDER BY ad_difference ASC
      LIMIT 10
    )
    SELECT * FROM top10
    UNION
    SELECT * FROM bottom10
    ORDER BY ad_difference DESC;
  """)
