from pathlib import Path
import numpy as np
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from BBBDM.lib.data_processing import (
    extract_data,
    filter_dataframes,
    get_valid_businesses_info,
    join_dataframe_firmid,
)
from BBBDM.lib.google_places_tools import google_validation
from BBBDM.lib.Normalizing import normalize_dataframe
from BBBDM.lib.sos_tools import compare_dataframes_sos
from BBBDM.lib.yellow_pages_tools import update_dataframe_with_yellow_pages_data

import pandas as pd
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
    mn_columns_expected_set=set(expected_df.columns)
    mn_business_path=str(Path(__file__).parent.parent / "Data/mn_business.csv")
    mn_business_df=extract_data(mn_business_path)
    mn_columns_set=set(mn_business_df.columns)
    mn_business_df=mn_business_df.head(10)
    assert mn_columns_set==mn_columns_expected_set




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
    mn_columns_expected_set=set(expected_df.columns)
    mn_business_address_path=str(Path(__file__).parent.parent / "Data/mn_business_address.csv")
    mn_business_address_df=extract_data(mn_business_address_path)
    mn_columns_set=set(mn_business_address_df.columns)
    mn_business_address_df=mn_business_address_df.head(10)
    assert mn_columns_set==mn_columns_expected_set


    

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
    mn_columns_expected_set=set(expected_df.columns)
    mn_business_email_path=str(Path(__file__).parent.parent / "Data/mn_business_email.csv")
    mn_business_email_df=extract_data(mn_business_email_path)
    mn_columns_set=set(mn_business_email_df.columns)
    mn_business_email_df=mn_business_email_df.head(10)
    assert mn_columns_set==mn_columns_expected_set
   



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
    mn_columns_expected_set=set(expected_df.columns)
    mn_business_name_path=str(Path(__file__).parent.parent / "Data/mn_business_name.csv")
    mn_business_name_df=extract_data(mn_business_name_path)
    mn_columns_set=set(mn_business_name_df.columns)
    mn_business_name_df=mn_business_name_df.head(10)
    assert mn_columns_set==mn_columns_expected_set
   


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
    mn_columns_expected_set=set(expected_df.columns)
    mn_business_phone_path=str(Path(__file__).parent.parent / "Data/mn_business_phone.csv")
    mn_business_phone_df=extract_data(mn_business_phone_path)
    mn_columns_set=set(mn_business_phone_df.columns)
    mn_business_phone_df=mn_business_phone_df.head(10)
    assert mn_columns_set==mn_columns_expected_set
   

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
    mn_columns_expected_set=set(expected_df.columns)
    mn_business_url_path=str(Path(__file__).parent.parent / "Data/mn_business_url.csv")
    mn_business_url_df=extract_data(mn_business_url_path)
    mn_columns_set=set(mn_business_url_df.columns)
    mn_business_url_df=mn_business_url_df.head(10)
    assert mn_columns_set==mn_columns_expected_set
   


test_regression_extract_data()

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
     data_df = pd.DataFrame(data, columns=columns)


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
    "state_incorporated": ["MN", "None", "MN", "MN", "None", "None", "None", "None"],
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

     mn_columns_expected_set=set(expected_df.columns)
     mn_business_path=str(Path(__file__).parent.parent / "Data/mn_business.csv")
     mn_business_active_df = get_valid_businesses_info(mn_business_path)
     mn_columns_set=set(mn_business_active_df.columns)
     mn_business_active_df=mn_business_active_df.head(10)
     assert mn_columns_set==mn_columns_expected_set
get_valid_businesses_info(str(Path(__file__).parent.parent / "Data/mn_business.csv"))


def test_regression_join_dataframe_firmid():
    data1_df=pd.DataFrame({

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
    "state_incorporated": ["MN", "None", "MN", "MN", "None", "None", "None", "None"],
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

    data2_df=pd.DataFrame({

    "address_id": [1, 2, 3, 4, 5, 6, 8, 9, 10, 12],
    "firm_id": [2, 5, 5, 5, 5, 7, 9, 9, 10, 10],
    "address_1": ["78 Acker St E", "2200 Nicollet Ave", "6855 Rowland Rd", "PO Box 46147", "2024 Blackberry Ln", "1408 County Road C W", "366 Saint Peter St", "772 Cleveland Ave S", "14601 Spring Lake Rd", "12285 Rush Cir NW"],
    "address_2": ["", "", "", "", "", "", "", "", "", ""],
    "city": ["Saint Paul", "Minneapolis", "Eden Prairie", "Eden Prairie", "Wayzata", "Roseville", "Saint Paul", "Saint Paul", "Minnetonka", "Elk River"],
    "state": ["MN", "MN", "MN", "MN", "MN", "MN", "MN", "MN", "MN", "MN"],
    "zip": ["55117", "55404", "55344", "55344", "55391", "55113", "55102", "55116", "55345", "55330"],
    "verified": [True, True, False, True, True, True, False, True, True, True],
    "verifiedon": ["2011-08-31 11:47:57", "2011-08-31 11:47:57", None, "2015-10-13 12:19:00", "2016-03-18 11:38:00", "2011-08-31 11:47:57", None, "2011-08-31 11:47:57", "2017-07-18 13:18:48.437", "2017-07-18 13:18:45.187"]

    })
   
    data3_df=pd.DataFrame({
    "name_id": [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
    "firm_id": [2, 5, 5, 5, 7, 7, 9, 9, 10, 10],
    "company_name": ["Able Fence, Inc.", "Albin Chapel", "Albin Funeral Chapel Inc", "Albin Endeavor, Inc.", "Albrecht Company", "Albrecht Enterprises, LLC", "Arthur Williams Opticians", "Arthur Williams Optical Inc", "Able Movers LLC", "Able Moving & Storage Inc"],
    "condensed_name": ["ablefenceinc", "albinchapel", "albinfuneralchapelinc", "albinendeavorinc", "albrechtcompany", "albrechtenterprisesllc", "arthurwilliamsopticians", "arthurwilliamsopticalinc", "ablemoversllc", "ablemovingandstorageinc"],
    "main": [True, False, False, True, True, False, False, False, True, False]


    })

    data4_df=pd.DataFrame({
    
    "email_id": [2, 3, 5, 6, 7, 8, 9, 11, 12, 13],
    "firm_id": [5, 5, 7, 7, 9, 10, 18, 18, 22, 22],
    "email": ["office@albinchapel.com", "jimalbinson@gmail.com", "mail@albrechtcompany.com", "edward@albrechtcompany.com", "arthurwilliamsoptical@gmail.com", "ablemovers@izoom.net", "donna.dingle@andersencorp.com", "jennifer.lamson@andersen.com", "mitch@asphaltmn.com", "office@asphaltmn.com"],
    "modifiedon": [None, None, "2023-02-08 09:41:51.75", None, None, None, None, None, None, None]

    })

    data5_df=pd.DataFrame({
    
    "name_id": [1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
    "firm_id": [2, 5, 5, 5, 7, 7, 9, 9, 10, 10],
    "company_name": ["Able Fence, Inc.", "Albin Chapel", "Albin Funeral Chapel Inc", "Albin Endeavor, Inc.", "Albrecht Company", "Albrecht Enterprises, LLC", "Arthur Williams Opticians", "Arthur Williams Optical Inc", "Able Movers LLC", "Able Moving & Storage Inc"],
    "condensed_name": ["ablefenceinc", "albinchapel", "albinfuneralchapelinc", "albinendeavorinc", "albrechtcompany", "albrechtenterprisesllc", "arthurwilliamsopticians", "arthurwilliamsopticalinc", "ablemoversllc", "ablemovingandstorageinc"],
    "main": [True, False, False, True, True, False, False, False, True, False]



    })

    data6_df=pd.DataFrame({
    "phone_id": [1, 2, 3, 4, 5, 8, 9, 10, 11],
    "firm_id": [2, 5, 5, 5, 7, 9, 9, 9, 10],
    "address_id": [1, 3, 3, 5, 6, None, 9, 8, 11],
    "phone": ["6512224355", "9529149410", "6128711418", "6122700491", "6516334510", "6512242883", "7632242883", "6516451976", "9529350331"],
    "verified": [False, False, False, False, False, False, False, False, False],
    "verifiedon": [None, None, None, None, None, None, None, None, None],
    "modifiedon": ["2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", None, "1972-08-01 00:00:00"],
    "createdon": ["2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", "2016-03-25 07:01:12.733", None, None]

    })

    data7_df=pd.DataFrame({
    "url_id": [1, 3, 5, 6, 9, 10, 12, 13, 15, 16],
    "firm_id": [5, 9, 10, 18, 22, 22, 22, 22, 30, 31],
    "url": ["http://www.albinchapel.com/", "http://www.arthurwilliamsoptical.com/", "http://www.ablemovers.net", "http://www.andersencorp.com", "http://www.asphaltmn.com", "http://asphaltmn.com", "http://twitter.com/asphaltmn", "http://www.facebook.com/asphaltmn", "http://www.adt.com", "http://www.amfam.com"],
    "main": [True, True, False, False, True, False, False, False, True, True],
    "verified": [False, True, False, True, True, True, True, True, True, False],
    "verifiedon": [None, "2019-10-11 10:10:03.84", "2017-10-17 13:16:13.123", "2022-10-26 13:24:22.983", "2018-09-07 17:01:48.963", "2018-09-07 17:01:51.067", "2018-09-07 17:01:54.647", "2018-09-07 17:01:56.977", "2018-05-25 12:07:02.393", None],
    "createdon": [None, None, None, None, None, None, None, None, None, None],
    "modifiedon": [None, "2019-10-11 10:10:03.44", "2017-10-17 13:16:13.217", "2022-10-26 13:24:22.737", "2018-09-07 17:01:48.927", "2018-09-07 17:01:51.03", "2018-09-07 17:01:54.593", "2018-09-07 17:01:56.927", "2018-05-25 12:07:02.457", None]
    })

    mn_business = get_valid_businesses_info(str(Path(__file__).parent.parent / "Data/mn_business.csv"))
    mn_business_address = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_address.csv"))
    mn_business_email = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_email.csv"))
    mn_business_name = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_name.csv"))
    mn_business_phone = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_phone.csv"))
    mn_business_url = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_url.csv"))

    actual_result_df= join_dataframe_firmid(
    mn_business.head(10),
    mn_business_address.head(10),
    mn_business_email.head(10),
    mn_business_name.head(10),
    mn_business_phone.head(10),
    mn_business_url.head(10))
    print(actual_result_df)
    expected_df=pd.DataFrame({
    "Firm_Id": [2, 5, 7, 9, 10, 18, 19, 22, 29, 30, 31],
    "state_incorporated": [["MN"],[np.nan],["MN"],["MN"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan], ["MN"], [np.nan]],
    "name_id": [[1], [2,3,4], [5,6], [8,9], [10,11], [np.nan,np.nan] ,[np.nan],[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],[np.nan],[np.nan],[np.nan] ],
    "BusinessName": [["Able Fence, Inc."], ["Albin Endeavor, Inc.","Albin Funeral Chapel Inc","Albin Chapel"],["Albrecht Company","Albrecht Enterprises, LLC"],["Arthur Williams Opticians","Arthur Williams Optical Inc"],["Able Moving & Storage Inc","Able Movers LLC"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "phone_id":[ [1], [2,3,4], [5], [8,9,10],[11,12],[np.nan,np.nan],[np.nan],[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],[np.nan],[np.nan],[np.nan]],
    "Phone": [["6512224355"],["6122700491","6128711418","9529149410"],["6516334510"],["7632242883","6516451976","6512242883"],["9529350331","6129913264"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "url_id": [[np.nan],[1],[np.nan,np.nan,np.nan,np.nan],[3],[5],[6],[np.nan],[9,10,12,13],[np.nan],[15],[16]],
    "Website": [[np.nan],["http://www.albinchapel.com/"],[np.nan],["http://www.arthurwilliamsoptical.com/"],["http://www.ablemovers.net"],["http://www.andersencorp.com"],[np.nan],["http://twitter.com/asphaltmn","http://asphaltmn.com","http://www.asphaltmn.com","http://www.facebook.com/asphaltmn"],[np.nan],["http://www.adt.com"],["http://www.amfam.com"]],
    "email_id": [[np.nan],[2,3],[5,6],[7],[8],[9,11],[np.nan],[12,13],[np.nan],[np.nan],[np.nan]],
    "Email": [[np.nan],["office@albinchapel.com","jimalbinson@gmail.com"],["edward@albrechtcompany.com","mail@albrechtcompany.com"],["arthurwilliamsoptical@gmail.com"],["ablemovers@izoom.net"],["donna.dingle@andersencorp.com","jennifer.lamson@andersen.com"],[np.nan],["mitch@asphaltmn.com","office@asphaltmn.com"],[np.nan],[np.nan],[np.nan]],
    "address_1": [["78 Acker St E"],["2024 Blackberry Ln","PO Box 46147","2200 Nicollet Ave","6855 Rowland Rd"],["1408 County Road C W"],["772 Cleveland Ave S","366 Saint Peter St"],["14601 Spring Lake Rd","12285 Rush Cir NW"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "address_2": [[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],  
    "City": [["Saint Paul"],["Wayzata","Eden Prairie","Minneapolis"],["Roseville"],["Saint Paul"],["Minnetonka","Elk River"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Zipcode": [["55117"],["55404","55391","55344"],["55113"],["55102","55116"],["55345","55330"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Address": [["78 Acker St E ,Saint Paul,55117"],["PO Box 46147 ,Eden Prairie,55344","2200 Nicollet Ave ,Minneapolis,55404","6855 Rowland Rd ,Eden Prairie,55344","2024 Blackberry Ln ,Wayzata,55391"],["1408 County Road C W ,Roseville,55113"],["366 Saint Peter St ,Saint Paul,55102","772 Cleveland Ave S ,Saint Paul,55116"],["14601 Spring Lake Rd ,Minnetonka,55345","12285 Rush Cir NW ,Elk River,55330"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],

     })
    
    expected_result=expected_df
    print(expected_result)
    mn_columns_expected_set=set(expected_result.columns)
    mn_columns_set=set(actual_result_df.columns)
    assert mn_columns_set==mn_columns_expected_set
     


def test_regression_valid_invalid_dataframe():
    merge_df=pd.DataFrame({
    "Firm_Id": [2, 5, 7, 9, 10, 18, 19, 22, 29, 30, 31],
    "Phone": [["6512224355"],["6122700491","6128711418","9529149410"],["6516334510"],["7632242883","6516451976","6512242883"],["9529350331","6129913264"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Website": [[np.nan],["http://www.albinchapel.com/"],[np.nan],["http://www.arthurwilliamsoptical.com/"],["http://www.ablemovers.net"],["http://www.andersencorp.com"],[np.nan],["http://twitter.com/asphaltmn","http://asphaltmn.com","http://www.asphaltmn.com","http://www.facebook.com/asphaltmn"],[np.nan],["http://www.adt.com"],["http://www.amfam.com"]],
    "Email": [[np.nan],["office@albinchapel.com","jimalbinson@gmail.com"],["edward@albrechtcompany.com","mail@albrechtcompany.com"],["arthurwilliamsoptical@gmail.com"],["ablemovers@izoom.net"],["donna.dingle@andersencorp.com","jennifer.lamson@andersen.com"],[np.nan],["mitch@asphaltmn.com","office@asphaltmn.com"],[np.nan],[np.nan],[np.nan]],
    "City": [["Saint Paul"],["Wayzata","Eden Prairie","Minneapolis"],["Roseville"],["Saint Paul"],["Minnetonka","Elk River"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Zipcode": [["55117"],["55404","55391","55344"],["55113"],["55102","55116"],["55345","55330"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Address": [["78 Acker St E ,Saint Paul,55117"],["PO Box 46147 ,Eden Prairie,55344","2200 Nicollet Ave ,Minneapolis,55404","6855 Rowland Rd ,Eden Prairie,55344","2024 Blackberry Ln ,Wayzata,55391"],["1408 County Road C W ,Roseville,55113"],["366 Saint Peter St ,Saint Paul,55102","772 Cleveland Ave S ,Saint Paul,55116"],["14601 Spring Lake Rd ,Minnetonka,55345","12285 Rush Cir NW ,Elk River,55330"],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],

     })
    expected_valid_rows = pd.DataFrame({
    "Firm_Id": [2, 5, 7, 9, 10],
    "BusinessName": [["Able Fence, Inc."], ["Albin Endeavor, Inc.","Albin Funeral Chapel Inc","Albin Chapel"],["Albrecht Company","Albrecht Enterprises, LLC"],["Arthur Williams Opticians","Arthur Williams Optical Inc"],["Able Moving & Storage Inc","Able Movers LLC"]],
    "Phone": [["6512224355"],["6122700491","6128711418","9529149410"],["6516334510"],["7632242883","6516451976","6512242883"],["9529350331","6129913264"]],
    "Website": [[np.nan],["http://www.albinchapel.com/"],[np.nan],["http://www.arthurwilliamsoptical.com/"],["http://www.ablemovers.net"]],
    "Email": [[np.nan],["office@albinchapel.com","jimalbinson@gmail.com"],["edward@albrechtcompany.com","mail@albrechtcompany.com"],["arthurwilliamsoptical@gmail.com"],["ablemovers@izoom.net"]],
    "City":[["Saint Paul"],["Wayzata","Eden Prairie","Minneapolis"],["Roseville"],["Saint Paul"],["Minnetonka","Elk River"]],
    "Zipcode": [["55117"],["55404","55391","55344"],["55113"],["55102","55116"],["55345","55330"]],
    "Address": [["78 Acker St E ,Saint Paul,55117"],["PO Box 46147 ,Eden Prairie,55344","2200 Nicollet Ave ,Minneapolis,55404","6855 Rowland Rd ,Eden Prairie,55344","2024 Blackberry Ln ,Wayzata,55391"],["1408 County Road C W ,Roseville,55113"],["366 Saint Peter St ,Saint Paul,55102","772 Cleveland Ave S ,Saint Paul,55116"],["14601 Spring Lake Rd ,Minnetonka,55345","12285 Rush Cir NW ,Elk River,55330"]]
})
    expected_invalid_rows =pd.DataFrame({
    "Firm_Id": [18, 19, 22, 29, 30, 31],
    "BusinessName": [[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Phone": [[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Website": [["http://www.andersencorp.com"],[np.nan],["http://www.facebook.com/asphaltmn","http://www.asphaltmn.com","http://twitter.com/asphaltmn","http://asphaltmn.com"],[np.nan],["http://www.adt.com"],["http://www.amfam.com"]],
    "Email": [["jennifer.lamson@andersen.com","donna.dingle@andersencorp.com"],[np.nan],["office@asphaltmn.com","mitch@asphaltmn.com"],[np.nan],[np.nan],[np.nan]],
    "City":[[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Zipcode": [[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Address": [[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]]
})
    print(expected_valid_rows)
    print(expected_invalid_rows)
     # There are no invalid rows in the provided DataFrame

    mn_business = get_valid_businesses_info(str(Path(__file__).parent.parent / "Data/mn_business.csv"))
    mn_business_address = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_address.csv"))
    mn_business_email = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_email.csv"))
    mn_business_name = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_name.csv"))
    mn_business_phone = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_phone.csv"))
    mn_business_url = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_url.csv"))

    merged_df= join_dataframe_firmid(
    mn_business.head(10),
    mn_business_address.head(10),
    mn_business_email.head(10),
    mn_business_name.head(10),
    mn_business_phone.head(10),
    mn_business_url.head(10)
)
    valid_data, invalid_data = filter_dataframes(merged_df)
    print(valid_data)
    print(invalid_data)

    #Sorts the lists inside the dataframe so that the order of the elements in the list does not matter
    valid_data = valid_data.applymap(lambda x: sorted(x) if isinstance(x, list) else x)
    invalid_data = invalid_data.applymap(lambda x: sorted(x) if isinstance(x, list) else x)
    expected_valid_rows = expected_valid_rows.applymap(lambda x: sorted(x) if isinstance(x, list) else x)
    expected_invalid_rows = expected_invalid_rows.applymap(lambda x: sorted(x) if isinstance(x, list) else x)

    assert expected_valid_rows.equals(valid_data)
    assert expected_invalid_rows.equals(invalid_data)



def test_regression_google_places():
    """
    Tests the google_places function with a sample dataframe
    """
    expected_valid_rows = pd.DataFrame({
    "Firm_Id": [2, 5, 7, 9, 10],
    "BusinessName": [["Able Fence, Inc."], ["Albin Endeavor, Inc.","Albin Funeral Chapel Inc","Albin Chapel"],["Albrecht Company","Albrecht Enterprises, LLC"],["Arthur Williams Opticians","Arthur Williams Optical Inc"],["Able Moving & Storage Inc","Able Movers LLC"]],
    "Phone": [["6512224355"],["6122700491","6128711418","9529149410"],["6516334510"],["7632242883","6516451976","6512242883"],["9529350331","6129913264"]],
    "Website": [[np.nan],["http://www.albinchapel.com/"],[np.nan],["http://www.arthurwilliamsoptical.com/"],["http://www.ablemovers.net"]],
    "Email": [[np.nan],["office@albinchapel.com","jimalbinson@gmail.com"],["edward@albrechtcompany.com","mail@albrechtcompany.com"],["arthurwilliamsoptical@gmail.com"],["ablemovers@izoom.net"]],
    "City":[["Saint Paul"],["Wayzata","Eden Prairie","Minneapolis"],["Roseville"],["Saint Paul"],["Minnetonka","Elk River"]],
    "Zipcode": [["55117"],["55404","55391","55344"],["55113"],["55102","55116"],["55345","55330"]],
    "Address": [["78 Acker St E ,Saint Paul,55117"],["PO Box 46147 ,Eden Prairie,55344","2200 Nicollet Ave ,Minneapolis,55404","6855 Rowland Rd ,Eden Prairie,55344","2024 Blackberry Ln ,Wayzata,55391"],["1408 County Road C W ,Roseville,55113"],["366 Saint Peter St ,Saint Paul,55102","772 Cleveland Ave S ,Saint Paul,55116"],["14601 Spring Lake Rd ,Minnetonka,55345","12285 Rush Cir NW ,Elk River,55330"]]
})
    expected_invalid_rows =pd.DataFrame({
    "Firm_Id": [18, 19, 22, 29, 30, 31],
    "BusinessName": [[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Phone": [[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Website": [["http://www.andersencorp.com"],[np.nan],["http://www.facebook.com/asphaltmn","http://www.asphaltmn.com","http://twitter.com/asphaltmn","http://asphaltmn.com"],[np.nan],["http://www.adt.com"],["http://www.amfam.com"]],
    "Email": [["jennifer.lamson@andersen.com","donna.dingle@andersencorp.com"],[np.nan],["office@asphaltmn.com","mitch@asphaltmn.com"],[np.nan],[np.nan],[np.nan]],
    "City":[[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Zipcode": [[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]],
    "Address": [[np.nan],[np.nan],[np.nan],[np.nan],[np.nan],[np.nan]]
})
    print(expected_valid_rows)
    print(expected_invalid_rows)
     # There are no invalid rows in the provided DataFrame

    mn_business = get_valid_businesses_info(str(Path(__file__).parent.parent / "Data/mn_business.csv"))
    mn_business_address = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_address.csv"))
    mn_business_email = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_email.csv"))
    mn_business_name = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_name.csv"))
    mn_business_phone = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_phone.csv"))
    mn_business_url = extract_data(str(Path(__file__).parent.parent / "Data/mn_business_url.csv"))

    merged_df= join_dataframe_firmid(
    mn_business.head(10),
    mn_business_address.head(10),
    mn_business_email.head(10),
    mn_business_name.head(10),
    mn_business_phone.head(10),
    mn_business_url.head(10)
)
    valid_data, invalid_data = filter_dataframes(merged_df)
    print(valid_data)
    print(invalid_data)

    #Sorts the lists inside the dataframe so that the order of the elements in the list does not matter
    valid_data = valid_data.applymap(lambda x: sorted(x) if isinstance(x, list) else x)
    invalid_data = invalid_data.applymap(lambda x: sorted(x) if isinstance(x, list) else x)
    expected_valid_rows = expected_valid_rows.applymap(lambda x: sorted(x) if isinstance(x, list) else x)
    expected_invalid_rows = expected_invalid_rows.applymap(lambda x: sorted(x) if isinstance(x, list) else x)




def test_regression_normalize_dataframe():
    valid_rows=pd.DataFrame({
    "firm_id": [2, 5, 7, 9, 10],
    # "state_incorporated": ["MN", "MN", "MN", "MN"],
    # "name_id": [1, 2, 3, 4],
    "BusinessName": [["Able Fence, Inc."], ["Albin Endeavor, Inc.","Albin Funeral Chapel Inc","Albin Chapel"],["Albrecht Company","Albrecht Enterprises, LLC"],["Arthur Williams Opticians","Arthur Williams Optical Inc"],["Able Moving & Storage Inc","Able Movers LLC"]],
    # "phone_id": [1, 2, 8, 9],
    "Phone": [["6512224355"],["6122700491","6128711418","9529149410"],["6516334510"],["7632242883","6516451976","6512242883"],["9529350331","6129913264"]],
    # "url_id": [3, 6, 10, 12],
    "Website": [[np.nan],["http://www.albinchapel.com/"],[np.nan],["http://www.arthurwilliamsoptical.com/"],["http://www.ablemovers.net"]],
    # "email_id": [3, 6, 12, 13],
    "Email": [[np.nan],["office@albinchapel.com","jimalbinson@gmail.com"],["edward@albrechtcompany.com","mail@albrechtcompany.com"],["arthurwilliamsoptical@gmail.com"],["ablemovers@izoom.net"]],
    # "address_1": ["2200 Nicollet Ave", "PO Box 46147", "366 Saint Peter St", "772 Cleveland Ave S"],
    # "address_2": [np.nan, np.nan, np.nan, np.nan],
    "City":[["Saint Paul"],["Wayzata","Eden Prairie","Minneapolis"],["Roseville"],["Saint Paul"],["Minnetonka","Elk River"]],
    "Zip Code": [["55117"],["55404","55391","55344"],["55113"],["55102","55116"],["55345","55330"]],
    "Address": [["78 Acker St E ,Saint Paul,55117"],
                ["PO Box 46147 ,Eden Prairie,55344","2200 Nicollet Ave ,Minneapolis,55404","6855 Rowland Rd ,Eden Prairie,55344","2024 Blackberry Ln ,Wayzata,55391"],
                ["1408 County Road C W ,Roseville,55113"],
                ["366 Saint Peter St ,Saint Paul,55102","772 Cleveland Ave S ,Saint Paul,55116"],
                ["14601 Spring Lake Rd ,Minnetonka,55345","12285 Rush Cir NW ,Elk River,55330"]]
    })

    invalid_rows=pd.DataFrame()

    expected_normalized_rows=pd.DataFrame({
    "firm_id": [2, 5, 7, 9, 10],
    # "state_incorporated": ["MN", "MN", "MN", "MN"],
    # "name_id": [1, 2, 3, 4],
    "BusinessName": [["able fence, inc."], ["albin endeavor inc.", "albin funeral chapel inc", "albin chapel"], ["albrecht company", "albrecht enterprises llc"],["arthur williams opticians","arthur williams optical inc"],["able moving and storage snc","able movers llc"]],
    # "phone_id": [1, 2, 8, 9],
    "Phone": [["+1 651-222-4355"], ["+1 612-270-0491","+1 612-871-1418","+1 952-914-9410"],["+1 651-633-4510"],["+1 763-224-2883","+1 651-645-1976","+1 651-224-2883"],["+1 952-935-0331","+1 612-991-3264"]],
    # "url_id": [3, 6, 10, 12],
    "Website": [[np.nan],["http://www.albinchapel.com/"],[np.nan],["http://www.arthurwilliamsoptical.com/"],["http://www.ablemovers.net"]],
    # "email_id": [3, 6, 12, 13],
    "Email": [[np.nan],["office@albinchapel.com","jimalbinson@gmail.com"],["edward@albrechtcompany.com","mail@albrechtcompany.com"],["arthurwilliamsoptical@gmail.com"],["ablemovers@izoom.net"]],
    # "address_1": ["2200 Nicollet Ave", "PO Box 46147", "366 Saint Peter St", "772 Cleveland Ave S"],
    # "address_2": [np.nan, np.nan, np.nan, np.nan],
    "City": [["Saint Paul"],["Wayzata","Eden Prairie","Minneapolis"],["Roseville"],["Saint Paul"],["Minnetonka","Elk River"]],
    "Zip Code": [["55117"],["55404","55391","55344"],["55113"],["55102","55116"],["55345","55330"]],
    "Address": [
        ["78 Acker St E ,saint paul,55117"],
        ["PO Box 46147 ,eden prairie,55344","2200 Nicollet Ave ,minneapolis,55404","6855 Rowland Rd ,eden prairie,55344","2024 Blackberry Ln ,wayzata,55391"],
        ["1408 County Road C W ,roseville,55113"],
        ["366 Saint Peter St ,saint paul,55102","772 Cleveland Ave S ,saint paul,55116"],
        ["14601 Spring Lake Rd ,minnetonka,55345","12285 Rush Cir NW ,elk river,55330"]
    ]})

    normalized_df = normalize_dataframe(valid_rows)

    normalized_df = normalized_df.applymap(lambda x: sorted(x) if isinstance(x, list) else x)
    expected_normalized_rows = expected_normalized_rows.applymap(lambda x: sorted(x) if isinstance(x, list) else x)

    assert expected_normalized_rows.equals(normalized_df)


def test_regression_sos_comparison():
    normalized_rows=pd.DataFrame({
    "firm_id": [2, 5, 7, 9, 10],
    # "state_incorporated": ["MN", "MN", "MN", "MN"],
    # "name_id": [1, 2, 3, 4],
    "BusinessName": [["able fence"], ["albin endeavor", "albin funeral chapel inc", "albin chapel"], ["albrecht company", "albrecht enterprises llc"],["arthur williams opticians","arthur williams optical inc"],["able moving and storage snc","able movers llc"]],
    # "phone_id": [1, 2, 8, 9],
    "Phone": [["+1 651-222-4355"], ["+1 612-270-0491","+1 612-871-1418","+1 952-914-9410"],["+1 651-633-4510"],["+1 763-224-2883","+1 651-645-1976","+1 651-224-2883"],["+1 952-935-0331","+1 612-991-3264"]],
    # "url_id": [3, 6, 10, 12],
    "Website": [[np.nan],["http://www.albinchapel.com/"],[np.nan],["http://www.arthurwilliamsoptical.com/"],["http://www.ablemovers.net"]],
    # "email_id": [3, 6, 12, 13],
    "Email": [[np.nan],["office@albinchapel.com","jimalbinson@gmail.com"],["edward@albrechtcompany.com","mail@albrechtcompany.com"],["arthurwilliamsoptical@gmail.com"],["ablemovers@izoom.net"]],
    # "address_1": ["2200 Nicollet Ave", "PO Box 46147", "366 Saint Peter St", "772 Cleveland Ave S"],
    # "address_2": [np.nan, np.nan, np.nan, np.nan],
    "City": [["Saint Paul"],["Wayzata","Eden Prairie","Minneapolis"],["Roseville"],["Saint Paul"],["Minnetonka","Elk River"]],
    "Zip Code": [["55117"],["55404","55391","55344"],["55113"],["55102","55116"],["55345","55330"]],
    "Address": [
        ["78 Acker St E ,saint paul,55117"],
        ["PO Box 46147 ,eden prairie,55344","2200 Nicollet Ave ,minneapolis,55404","6855 Rowland Rd ,eden prairie,55344","2024 Blackberry Ln ,wayzata,55391"],
        ["1408 County Road C W ,roseville,55113"],
        ["366 Saint Peter St ,saint paul,55102","772 Cleveland Ave S ,saint paul,55116"],
        ["14601 Spring Lake Rd ,minnetonka,55345","12285 Rush Cir NW ,elk river,55330"]
    ]})
    string = str(Path(__file__).parent.parent / "Data/sos_data.csv")
    sos_data = extract_data(str(Path(__file__).parent.parent / "Data/sos_data.csv"))
    sos_data = sos_data.drop(labels=['Business Filing Type', 'Filing Date', 'Business Address Type', 'Region Code', 'Zip Code Ext', 'Business Party Name Type', 'Party Full Name', 'Next Renewal Due Date'], axis=1)

    updated_df_sos = compare_dataframes_sos(normalized_rows, sos_data)

    assert not updated_df_sos.empty



def test_regression_yellow_pages_comparison():
    google_places_output = pd.DataFrame({
        "firm_id": [2, 5, 7, 9, 10],
        "BusinessName": [["able fence, inc."], ["albin endeavor inc.", "albin funeral chapel inc", "albin chapel"],
                         ["albrecht company", "albrecht enterprises llc"],
                         ["arthur williams opticians","arthur williams optical inc"],
                         ["able moving and storage snc","able movers llc"]],
        "BusinessNameUpdate": ["Able Fence, Inc.", np.nan, "Albrecht Enterprises, LLC", np.nan, np.nan],
        "BusinessNameCorrect": [True, False, True, False, False],
        "BusinessNameFound": ["SOS", np.nan, "SOS", np.nan, np.nan],
        "Phone": [["+1 651-222-4355"], ["+1 612-270-0491","+1 612-871-1418","+1 952-914-9410"],["+1 651-633-4510"],
                  ["+1 763-224-2883","+1 651-645-1976","+1 651-224-2883"],["+1 952-935-0331","+1 612-991-3264"]],
        "PhoneUpdate": [np.nan, np.nan, np.nan, np.nan, np.nan],
        "PhoneCorrect": [False, False, False, False, False],
        "PhoneFound": [np.nan, np.nan, np.nan, np.nan, np.nan],
        "Website": [[np.nan],["http://www.albinchapel.com/"],[np.nan],["http://www.arthurwilliamsoptical.com/"],
                    ["http://www.ablemovers.net"]],
        "WebsiteUpdate": [np.nan, np.nan, np.nan, np.nan, np.nan],
        "WebsiteCorrect": [False, False, False, False, False],
        "WebsiteFound": ["SOS", np.nan, "SOS", np.nan, np.nan],
        "Email": [[np.nan],["office@albinchapel.com","jimalbinson@gmail.com"],
                  ["edward@albrechtcompany.com","mail@albrechtcompany.com"],["arthurwilliamsoptical@gmail.com"],
                  ["ablemovers@izoom.net"]],
        "EmailUpdate": [np.nan, np.nan, np.nan, np.nan, np.nan],
        "EmailCorrect": [False, False, False, False, False],
        "EmailFound": [np.nan, np.nan, np.nan, np.nan, np.nan],
        "City": [["Saint Paul"],["Wayzata","Eden Prairie","Minneapolis"],["Roseville"],
                 ["Saint Paul"],["Minnetonka","Elk River"]],
        "Zip Code": [["55117"], ["55404", "55391", "55344"], ["55113"], ["55102", "55116"], ["55345", "55330"]],
        "ZipUpdate": ["55117", np.nan, "55113", np.nan, np.nan],
        "ZipCorrect": [True, False, True, False, False],
        "ZipFound": ["SOS", np.nan, "SOS", np.nan, np.nan],
        "Address": [["78 Acker St E ,saint paul,55117"],
                ["PO Box 46147 ,eden prairie,55344","2200 Nicollet Ave ,minneapolis,55404","6855 Rowland Rd ,eden prairie,55344","2024 Blackberry Ln ,wayzata,55391"],
                ["1408 County Road C W ,roseville,55113"],
                ["366 Saint Peter St ,saint paul,55102","772 Cleveland Ave S ,saint paul,55116"],
                ["14601 Spring Lake Rd ,minnetonka,55345","12285 Rush Cir NW ,elk river,55330"]],
        "AddressUpdate": ["78 Acker Str E, St Paul, 55117", np.nan, "1408 W Co Rd C, Roseville, 55113", np.nan, np.nan],
        "AddressCorrect": [True, False, True, False, False],
        "AddressFound": ["SOS", np.nan, "SOS", np.nan, np.nan],
    })

    yp_updated = update_dataframe_with_yellow_pages_data(google_places_output)

    assert not yp_updated.empty
