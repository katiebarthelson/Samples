import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

pd.options.display.max_columns = 100
pd.options.display.width = 200

load_dotenv()

def main():
    engine = create_engine(f"postgresql://{env('user')}:{env('pw')}@localhost:{env('port')}/{env('db')}")
    with engine.connect() as con:
        con.execute(read_file_to_str('table_definitions.sql'))

    # date
    date_df = read_tsv('date')
    df_to_sql(date_df, 'date', engine)

    # advertising_campaign, active_on
    ad_camp_df = read_tsv('ad_campaigns').rename(columns={'date_ad': 'date', 'campaign': 'campaign_description'})
    df_to_sql(ad_camp_df[['campaign_description']].drop_duplicates(), 'advertising_campaign', engine)
    df_to_sql(ad_camp_df, 'active_on', engine)

    # holiday
    holiday_df = read_tsv('holidays').rename(columns={'holidayname': 'holiday_names'})
    df_to_sql(holiday_df, 'holiday', engine)

    # category
    category_df = read_tsv('categories').rename(columns={'Name': 'category_name'})
    df_to_sql(category_df, 'category', engine)

    # product
    product_df = read_tsv('products').rename(columns={'productid': 'pid', 'name': 'product_name', 'retailprice': 'retail_price'})
    product_df['retail_price'] = product_df['retail_price'].apply(lambda x: '{0:.2f}'.format(x))
    df_to_sql(product_df, 'product', engine)

    # belongs_to
    belongs_to_df = read_tsv('productcategories').rename(columns={'productid': 'pid', 'categoryname': 'category_name'})
    df_to_sql(belongs_to_df, 'belongs_to', engine)

    # discounted_on
    discounted_on_df = read_tsv('discounts').rename(columns={'productid': 'pid', 'discountprice': 'discount_price'})
    discounted_on_df['discount_price'] = discounted_on_df['discount_price'].apply(lambda x: '{0:.2f}'.format(x))
    df_to_sql(discounted_on_df, 'discounted_on', engine)

    # city
    city_df = read_tsv('population').rename(columns={'Name': 'city_name', 'State': 'state', 'Population': 'population'})
    df_to_sql(city_df, 'city', engine)

    # store, childcare_store, time_limit
    store_df = read_tsv('stores').rename(columns={
        'storeid': 'store_number', 
        'phone': 'phone_number', 
        'address': 'street_address',
        'cityname': 'city_name',
        'restaurant': 'has_restaurant',
        'snackbar': 'has_snack_bar',
        'childcare_time': 'minutes'
    })
    store_df['has_restaurant'] = store_df['has_restaurant'].astype('bool')
    store_df['has_snack_bar'] = store_df['has_snack_bar'].astype('bool')

    df_to_sql(store_df[['store_number', 'phone_number', 'street_address', 'city_name', 'state', 'has_restaurant', 'has_snack_bar']], 'store', engine)
    df_to_sql(store_df[['minutes']].drop_duplicates().dropna(), 'time_limit', engine)
    df_to_sql(store_df[['store_number', 'minutes']].dropna(), 'childcare_store', engine)

    # sold
    sold_df = read_tsv('sales').rename(columns={'productid': 'pid', 'storeid': 'store_number'})
    df_to_sql(sold_df, 'sold', engine)


def read_tsv(file_name):
    return pd.read_csv(f'Demo Data/{file_name}.tsv', sep='\t')


def df_to_sql(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='append', index=False)


def env(key):
  return os.environ.get(key)


def read_file_to_str(filepath):
    with open(filepath, 'r') as f:
        return f.read()


def summarize(df):
    print(df.info())
    print(df.head())


if __name__ == '__main__':
    main()