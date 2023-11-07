import importlib.util
import os
from pathlib import Path

import pandas as pd
import pytest


from BBBDM.lib.data_processing import extract_data, get_valid_businesses_info
from BBBDM.lib.data_processing import join_dataframe_firmid
"""
This file is meant to be used for regression testing main

"""


def test_regression_extract_data():

    data1=[
    [2, True, 1, 9, 1, 1, "1972-04-01 00:00:00", "MN", "1972-04-24 00:00:00", "MN", "1977-07-01 00:00:00", None, False, "2002-07-19 00:00:00"],
    [5, True, 0, 4, 1, 1, "1946-01-01 00:00:00", "MN", None, "", "1974-04-26 00:00:00", None, False, "2016-03-18 00:00:00"],
    [7, True, 1, 12, 1, 2, "1968-06-22 00:00:00", "MN", "1968-06-22 00:00:00", "MN", "2008-02-28 00:00:00", None, False, "2008-03-03 00:00:00"],
    [9, True, 16, 5, 1, 1, "1914-01-01 00:00:00", "MN", "1987-08-01 00:00:00", "MN", "1991-03-01 00:00:00", None, False, "2001-06-29 00:00:00"],
    [10, False, 0, 10, 1, 1, "1969-01-01 00:00:00", "MN", "1969-01-01 00:00:00", "MN", "1972-08-09 00:00:00", "2005-04-14 00:00:00", False, "2013-09-21 00:00:00"],
    [14, False, None, 1, 1, 1, "1855-01-01 00:00:00", None, None, "", "1971-06-01 00:00:00", None, False, "2013-01-08 00:00:00"],
    [18, True, 1, 8000, 1, 4, "1903-01-01 00:00:00", "MN", None, "", "1984-08-07 00:00:00", None, True, "2010-06-08 00:00:00"],
    [19, True, 3, 1, 1, 1, "1999-06-04 00:00:00", "MN", None, "", "2004-12-20 00:00:00", None, False, "2004-12-20 00:00:00"],
    [22, True, 1, 25, 1, 1, "1979-03-01 00:00:00", "MN", "1979-09-04 00:00:00", "", "1980-10-01 00:00:00", None, False, "2012-07-02 00:00:00"],
    [29, True, 0, 121, 1, 3, "1924-01-01 00:00:00", "MN", None, "", "1985-07-15 00:00:00", None, False, "2001-06-29 00:00:00"]
    ]

    columns=["firm_id","active","business_type_id","number_of_employees","number_of_locations",
          "size_id","date_established","state_established","date_incorporated","state_incorporated",
          "date_joined_bbb","outofbusiness_date","hq","lastupdate"]

    expected_df=pd.DataFrame(data1,columns=columns)
    mn_columns_expected=expected_df.columns
    print(expected_df)
    mn_business_path="../Data/mn_business.csv"
    mn_business_df=extract_data(mn_business_path)
    mn_columns=mn_business_df.columns
    mn_business_df=mn_business_df.head(10)
    print(mn_business_df)
    assert mn_columns==mn_columns_expected

test_regression_extract_data()

'''''

    data2= [
    [1, 2, "78 Acker St E", "", "Saint Paul", "MN", "55117", True, "2011-08-31 11:47:57"],
    [2, 5, "2200 Nicollet Ave", "", "Minneapolis", "MN", "55404", True, "2011-08-31 11:47:57"],
    [3, 5, "6855 Rowland Rd", "", "Eden Prairie", "MN", "55344", False, None],
    [4, 5, "PO Box 46147", "", "Eden Prairie", "MN", "55344", True, "2015-10-13 12:19:00"],
    [5, 5, "2024 Blackberry Ln", "", "Wayzata", "MN", "55391", True, "2016-03-18 11:38:00"],
    [6, 7, "1408 County Road C W", "", "Roseville", "MN", "55113", True, "2011-08-31 11:47:57"],
    [8, 9, "366 Saint Peter St", "", "Saint Paul", "MN", "55102", False, None],
    [9, 9, "772 Cleveland Ave S", "", "Saint Paul", "MN", "55116", True, "2011-08-31 11:47:57"],
    [10, 10, "14601 Spring Lake Rd", "", "Minnetonka", "MN", "55345", True, "2017-07-18 13:18:48.437"],
    [12, 10, "12285 Rush Cir NW", "", "Elk River", "MN", "55330", True, "2017-07-18 13:18:45.187"]
]
    columns=["address_id","firm_id","address_1","address_2","city","state","zip","verified","verifiedon"]
    
    expected_df=pd.DataFrame(data2,columns=columns)
    print(expected_df)
    mn_business_address_path="../Data/mn_business_address.csv"
    mn_business_address_df=extract_data(mn_business_address_path)
    mn_business_address_df=mn_business_address_df.head(10)
    print(mn_business_address_df)
    assert mn_business_address_df.equals(expected_df)
    

    
    data3=[
    [1, 2, "Able Fence, Inc.", "ablefenceinc", True],
    [2, 5, "Albin Chapel", "albinchapel", False],
    [3, 5, "Albin Funeral Chapel Inc", "albinfuneralchapelinc", False],
    [4, 5, "Albin Endeavor, Inc.", "albinendeavorinc", True],
    [5, 7, "Albrecht Company", "albrechtcompany", True],
    [6, 7, "Albrecht Enterprises, LLC", "albrechtenterprisesllc", False],
    [8, 9, "Arthur Williams Opticians", "arthurwilliamsopticians", False],
    [9, 9, "Arthur Williams Optical Inc", "arthurwilliamsopticalinc", False],
    [10, 10, "Able Movers LLC", "ablemoversllc", True],
    [11, 10, "Able Moving & Storage Inc", "ablemovingandstorageinc", False]
]
    columns=["name_id","firm_id","company_name","condensed_name","main"]
    
    expected_df=pd.DataFrame(data3,columns=columns)
    mn_business_contact_path="../Data/mn_business_contact.csv"
    mn_business_contact_df=extract_data(mn_business_contact_path)
    mn_business_contact_df=mn_business_contact_df.head(10)
    print(mn_business_contact_df)
    assert mn_business_contact_df.equals(expected_df)



    
   
    
    data4=[
    [2, 5, "office@albinchapel.com", None],
    [3, 5, "jimalbinson@gmail.com", None],
    [5, 7, "mail@albrechtcompany.com", "2023-02-08 09:41:51.75"],
    [6, 7, "edward@albrechtcompany.com", None],
    [7, 9, "arthurwilliamsoptical@gmail.com", None],
    [8, 10, "ablemovers@izoom.net", None],
    [9, 18, "donna.dingle@andersencorp.com", None],
    [11, 18, "jennifer.lamson@andersen.com", None],
    [12, 22, "mitch@asphaltmn.com", None],
    [13, 22, "office@asphaltmn.com", None]
]
    columns=["email_id","firm_id","email","modifiedon"]
    
    expected_df=pd.DataFrame(data4,columns=columns)
    print(mn_business_email_df)
    mn_business_email_path="../Data/mn_business_email.csv"
    mn_business_email_df=extract_data(mn_business_email_path)
    mn_business_email_df=mn_business_email_df.head(10)
    print(mn_business_email_df)
    assert mn_business_email_df.equals(expected_df)
   



    data5=[
    [1, 2, "Able Fence, Inc.", "ablefenceinc", True],
    [2, 5, "Albin Chapel", "albinchapel", False],
    [3, 5, "Albin Funeral Chapel Inc", "albinfuneralchapelinc", False],
    [4, 5, "Albin Endeavor, Inc.", "albinendeavorinc", True],
    [5, 7, "Albrecht Company", "albrechtcompany", True],
    [6, 7, "Albrecht Enterprises, LLC", "albrechtenterprisesllc", False],
    [8, 9, "Arthur Williams Opticians", "arthurwilliamsopticians", False],
    [9, 9, "Arthur Williams Optical Inc", "arthurwilliamsopticalinc", False],
    [10, 10, "Able Movers LLC", "ablemoversllc", True],
    [11, 10, "Able Moving & Storage Inc", "ablemovingandstorageinc", False]
     ]
    columns=["name_id","firm_id","company_name","condensed_name","main"]
    
    expected_df=pd.DataFrame(data5,columns=columns)
    mn_business_name_path="../Data/mn_business_name.csv"
    mn_business_name_df=extract_data(mn_business_name_path)
    mn_business_name_df=mn_business_name_df.head(10)
    assert mn_business_name_df.equals(expected_df)
   


    data6=[
     [1, 2, 1, "6512224355", False, None, "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733"],
    [2, 5, 3, "9529149410", False, None, "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733"],
    [3, 5, 3, "6128711418", False, None, "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733"],
    [4, 5, 5, "6122700491", False, None, "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733"],
    [5, 7, 6, "6516334510", False, None, "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733"],
    [8, 9, None, "6512242883", False, None, "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733"],
    [9, 9, 9, "7632242883", False, None, "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733"],
    [10, 9, 8, "6516451976", False, None, None, None],
    [11, 10, 11, "9529350331", False, None, "1972-08-01 00:00:00", None]
]
    columns=["phone_id","firm_id","address_id","phone","verified","verifiedon","modifiedon","createdon"]
    
    expected_df=pd.DataFrame(data6,columns=columns)
    mn_business_phone_path="../Data/mn_business_phone.csv"
    mn_business_phone_df=extract_data(mn_business_phone_path)
    mn_business_phone_df=mn_business_phone_df.head(10)
    assert mn_business_phone_df.equals(expected_df)
   

    data7=[
    [1, 5, "http://www.albinchapel.com/", True, False, None, None, None],
    [3, 9, "http://www.arthurwilliamsoptical.com/", True, True, "2019-10-11 10:10:03.84", None, "2019-10-11 10:10:03.44"],
    [5, 10, "http://www.ablemovers.net", False, True, "2017-10-17 13:16:13.123", None, "2017-10-17 13:16:13.217"],
    [6, 18, "http://www.andersencorp.com", False, True, "2022-10-26 13:24:22.983", None, "2022-10-26 13:24:22.737"],
    [9, 22, "http://www.asphaltmn.com", True, True, "2018-09-07 17:01:48.963", None, "2018-09-07 17:01:48.927"],
    [10, 22, "http://asphaltmn.com", False, True, "2018-09-07 17:01:51.067", None, "2018-09-07 17:01:51.03"],
    [12, 22, "http://twitter.com/asphaltmn", False, True, "2018-09-07 17:01:54.647", None, "2018-09-07 17:01:54.593"],
    [13, 22, "http://www.facebook.com/asphaltmn", False, True, "2018-09-07 17:01:56.977", None, "2018-09-07 17:01:56.927"],
    [15, 30, "http://www.adt.com", True, True, "2018-05-25 12:07:02.393", None, "2018-05-25 12:07:02.457"],
    [16, 31, "http://www.amfam.com", True, False, None, None, None]
]
    columns=["url_id","firm_id","url","main","verified","verifiedon","createdon","modifiedon"]
    
    expected_df=pd.DataFrame(data7,columns=columns)
    mn_business_url_path="../Data/mn_business_url.csv"
    mn_business_url_df=extract_data(mn_business_url_path)
    mn_business_url_df=mn_business_url_df.head(10)
    assert mn_business_url_df.equals(expected_df)
   


def test_regression_get_valid_business():
     data=[
    [2, True, 1, 9, 1, 1, "1972-04-01 00:00:00", "MN", "1972-04-24 00:00:00", "MN", "1977-07-01 00:00:00", None, False, "2002-07-19 00:00:00"],
    [5, True, 0, 4, 1, 1, "1946-01-01 00:00:00", "MN", None, "", "1974-04-26 00:00:00", None, False, "2016-03-18 00:00:00"],
    [7, True, 1, 12, 1, 2, "1968-06-22 00:00:00", "MN", "1968-06-22 00:00:00", "MN", "2008-02-28 00:00:00", None, False, "2008-03-03 00:00:00"],
    [9, True, 16, 5, 1, 1, "1914-01-01 00:00:00", "MN", "1987-08-01 00:00:00", "MN", "1991-03-01 00:00:00", None, False, "2001-06-29 00:00:00"],
    [10, False,0, 10, 1, 1, "1969-01-01 00:00:00", "MN", "1969-01-01 00:00:00", "MN", "1972-08-09 00:00:00", "2005-04-14 00:00:00", False, "2013-09-21 00:00:00"],
    [14, False,None,1, 1, 1, "1855-01-01 00:00:00", None, None, "", "1971-06-01 00:00:00", None, False, "2013-01-08 00:00:00"],
    [18, True, 1, 8000, 1, 4, "1903-01-01 00:00:00", "MN", None, "", "1984-08-07 00:00:00", None, True, "2010-06-08 00:00:00"],
    [19, True, 3, 1, 1, 1, "1999-06-04 00:00:00", "MN", None, "", "2004-12-20 00:00:00", None, False, "2004-12-20 00:00:00"],
    [22, True, 1, 25, 1, 1, "1979-03-01 00:00:00", "MN", "1979-09-04 00:00:00", "", "1980-10-01 00:00:00", None, False, "2012-07-02 00:00:00"],
    [29, True, 0, 121, 1, 3, "1924-01-01 00:00:00", "MN", None, "", "1985-07-15 00:00:00", None, False, "2001-06-29 00:00:00"]
    ]

     columns=["firm_id","active","business_type_id","number_of_employees","number_of_locations",
          "size_id","date_established","state_established","date_incorporated","state_incorporated",
          "date_joined_bbb","outofbusiness_date","hq","lastupdate"]
     data1_df = pd.DataFrame(data, columns=columns)


     expected_df=pd.DataFrame({
    "firm_id": [2, 5, 7, 9, 18, 19, 22, 29],
    "active": ['TRUE', 'TRUE', 'TRUE', 'TRUE', 'TRUE', 'TRUE', 'TRUE', 'TRUE'],
    "business_type_id": [1, 0, 1, 16, 1, 3, 1, 0],
    "number_of_employees": [9, 4, 12, 5, 8000, 1, 25, 121],
    "number_of_locations": [1, 1, 1, 1, 1, 1, 1, 1],
    "size_id": [1, 1, 2, 1, 1, 1, 4, 3],
    "date_established": [
        "1972-04-01 00:00:00",
        "1946-01-01 00:00:00",
        "1968-06-22 00:00:00",
        "1914-01-01 00:00:00",
        "1903-01-01 00:00:00",
        "1999-06-04 00:00:00",
        "1979-03-01 00:00:00",
        "1924-01-01 00:00:00",
    ],
    "state_established": ["MN", "MN", "MN", "MN", "MN", "MN", "MN", "MN"],
    "date_incorporated": [
        "1972-04-24 00:00:00",
        "None",
        "1968-06-22 00:00:00",
        "1987-08-01 00:00:00",
        "None",
        "None",
        "1979-09-04 00:00:00",
        "None",
    ],
    "state_incorporated": ["MN", "1974-04-26 00:00:00", "MN", "MN", "None", "None", "None", "None"],
    "date_joined_bbb": [
        "1977-07-01 00:00:00",
        "None",
        "2008-02-28 00:00:00",
        "1991-03-01 00:00:00",
        "1984-08-07 00:00:00",
        "2004-12-20 00:00:00",
        "1980-10-01 00:00:00",
        "1985-07-15 00:00:00",
    ],
    "outofbusiness_date": ["None", "None", "None", "None", "None", "None", "None", "None"],
    "hq": [False, False, False, False, True, False, False, False],
    "lastupdate": [
        "2002-07-19 00:00:00",
        "2016-03-18 00:00:00",
        "2008-03-03 00:00:00",
        "2001-06-29 00:00:00",
        "2010-06-08 00:00:00",
        "2004-12-20 00:00:00",
        "2012-07-02 00:00:00",
        "2001-06-29 00:00:00",
    ]
     })


     mn_business_path="../Data/mn_business.csv"
     mn_business_active_df = get_valid_businesses_info("Data/mn_business.csv")
     mn_business_active_df=mn_business_active_df.head(10)
     assert mn_business_active_df.equals(expected_df)


def regression_test_merge_dataframe():
    pass
    

    '''