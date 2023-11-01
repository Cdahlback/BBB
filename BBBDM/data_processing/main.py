import pandas as pd
import re
import logging
import numpy as np
from functools import reduce

pd.options.mode.chained_assignment = None  # Disable the warning
logging.basicConfig(filename="functions.log", level=logging.DEBUG)

# Merges dataframes based on their business name - Used for merging BBB and Secretary of State data
def compare_dataframes(
    historicalData: pd.DataFrame, newData: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge historicalData and newData on the 'BusinessName' column
    Calculate MatchesAddress and MatchesZip
    Select the desired columns
    Rename columns for clarity

    Parameters:
    historicalData: DataFrame containing historical data
    newData: DataFrame containing new data

    Returns:
    result_df: DataFrame containing merged data"""

    left_on = "BusinessName"
    right_on = "Business Name"
    try:
        # Merge historicalData and newData on the 'BusinessName' column
        merged_data = historicalData.merge(
            newData, left_on=left_on, right_on=right_on, how="inner"
        )
    except KeyError as e:
        logging.debug(
            "Exception: KeyError {0} occurred when merging historicalData with secretary of state".format(
                e
            )
        )
        logging.debug("Length historical data: {0}".format(len(historicalData)))
        logging.debug("Length new data: {0}".format(len(newData)))
        return False

    try:
        # Calculate MatchesAddress and MatchesZip
        merged_data["MatchesAddress"] = (
            merged_data["Address"] == merged_data["Address 1"]
        )
        merged_data["MatchesZip"] = (
            merged_data["Zip Code_x"] == merged_data["Zip Code_y"]
        )
    except KeyError as e:
        logging.debug(
            "Exception: KeyError {0} occurred when accessing merged_data (historical/secretary)".format(
                e
            )
        )
        return False

    # Select the desired columns
    result_df = merged_data[
        [
            "Firm_id",
            "BusinessName",
            "MatchesAddress",
            "Address 1",
            "MatchesZip",
            "Zip Code_y",
            "Business Filing Type",
            "Filing Date",
            "Status",
            "Address 2",
            "City",
            "Region Code",
            "Party Full Name",
            "Next Renewal Due Date",
        ]
    ]

    # Rename columns for clarity
    result_df.rename(
        columns={"Address 1": "Address_new", "Zip Code_y": "Zip Code_new"}, inplace=True
    )
    logging.info(
        "historicalData has been merged with Secretary Of State data Successfully"
    )

    return result_df


# Normalize Email
def normalize_email(email: str) -> str | None:
    """
    Normalize email addresses by converting to lowercase, removing whitespace, and removing special characters
    except ., @, and -. If the email address does not contain an @ symbol, it is considered invalid and None is

    Parameters:
    email: Email address to normalize

    Returns:
    Normalized email address or None if invalid
    """
    email = email.lower()  # Convert to lowercase
    email = re.sub(r"\s", "", email)  # Remove whitespace
    email = re.sub(
        r"[^a-z0-9.@-]", "", email
    )  # Remove special characters except ., @, and -
    if "@" not in email:
        logging.warning(f"Invalid email: {email}")
        return None  # Invalid email
    return email


# Normalize Phone Number
def normalize_phone_number(phone: str) -> str | None:
    """
    Normalize phone numbers by removing whitespace and non-numeric characters. If the phone number does not
    contain any numeric digits, it is considered invalid and None is returned.

    Parameters:
    phone: Phone number to normalize

    Returns:
    Normalized phone number or None if invalid
    """
    if not any(
        char.isdigit() for char in phone
    ):  # Check if there are no numeric digits in the phone number
        logging.warning(f"Invalid phone number: {phone}")
        return None  # Invalid phone number
    phone = re.sub(r"\s|\D", "", phone)  # Remove whitespace and non-numeric characters
    return phone


# Normalize Zipcode
def normalize_zipcode(zipcode: str) -> str | None:
    """
    Normalize zipcodes by removing whitespace and non-numeric characters. If the zipcode does not contain
    exactly 5 numeric digits, it is considered invalid and None is returned.

    Parameters:
    zipcode: Zipcode to normalize

    Returns:
    Normalized zipcode or None if invalid
    """
    zipcode = re.sub(
        r"\s|\D", "", zipcode
    )  # Remove whitespace and non-numeric characters
    if len(zipcode) == 5:
        return zipcode
    else:
        logging.warning(f"Invalid zipcode: {zipcode}")
        return None  # Invalid zipcode


# Define a function to normalize the entire DataFrame
def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the entire DataFrame by applying the normalize_email, normalize_phone_number, and normalize_zipcode
    functions to the Email, Phone Number, and Zipcode columns respectively. Invalid values are replaced with None.

    Parameters:
    df: DataFrame to normalize

    Returns:
    Normalized DataFrame
    """
    # Apply each normalization function to respective columns
    df["Email"] = df["Email"].apply(normalize_email)
    df["Phone Number"] = df["Phone Number"].apply(normalize_phone_number)
    df["Zipcode"] = df["Zipcode"].apply(normalize_zipcode)

    return df


# Normalize Business Names (using Eli's function)
def standardizeName(name: str) -> str:
    """
    Normalize business names by converting to lowercase, replacing '&' with 'and', removing special characters,
    and removing extra whitespace. If the business name is empty after normalization, it is considered invalid
    and None is returned.

    Parameters:
    name: Business name to normalize

    Returns:
    Normalized business name or None if invalid
    """
    name = name.lower()
    name = re.sub("&", " and ", name)
    name = re.sub("[^a-z\s-]", "", name)
    name = re.sub(" {2,}", " ", name)
    return name.strip()


# Normalize Addresses using regex
def normalize_address(address: str) -> str | None:
    """
    Normalize addresses by converting to lowercase, removing whitespace, and removing special characters except
    ., -, and #. If the address does not match the pattern of a valid address, it is considered invalid and
    None is returned.

    Parameters:
    address: Address to normalize

    Returns:
    Normalized address or None if invalid
    """

    pattern = r"^\d+\s[A-Za-z0-9\s\.\-]+(?:\s(?:Apt|Suite|Ste)\s\d+)?$"

    if re.match(pattern, address):

        logging.info(f"Normalized Address: {address}")
        return address
    else:

        logging.error(f"Invalid Address: {address}")
        return None


# Normalize URL
def normalize_url(url: str) -> str | None:
    """
    Normalize URLs by converting to lowercase, removing whitespace, and removing special characters except
    ., -, and #. If the URL does not match the pattern of a valid URL, it is considered invalid and
    None is returned.

    Parameters:
    url: URL to normalize

    Returns:
    Normalized URL or None if invalid
    """

    url = url.lower()

    url = url.replace(" ", "")

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    logging.info(f"Normalized URL: {url}")

    return url


# Filter out invalid data based on the criteria
def filter_dataframes(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """
    Filter the DataFrame to only keep rows where at least one of the following conditions is true:
    - name is not null and not empty
    - address is not null and not empty
    - phone is not null and matches the pattern for a phone number
    - website is not null and not empty
    - email is not null and not empty

    Parameters:
    df: DataFrame to filter

    Returns:
    Tuple of DataFrames containing the valid and invalid rows respectively
    """
    conditions = (
        (df["name"].notna() & (df["name"] != ""))
        | (df["address"].notna() & (df["address"] != ""))
        | (df["phone"].notna() & df["phone"].str.match(r"^\d{10}$"))
        | (df["website"].notna() & (df["website"] != ""))
        | (df["email"].notna() & (df["email"] != ""))
    )

    valid_df = df[conditions]
    invalid_df = df[~conditions]

    # Log information about the valid and invalid DataFrames
    logging.info("Valid DataFrame:\n%s", valid_df.to_string())
    logging.info("Invalid DataFrame:\n%s", invalid_df.to_string())

    return valid_df, invalid_df


# Join multiple dataframes on FirmID
def join_dataframe_firmid(*data_frames: pd.DataFrame) -> pd.DataFrame | bool:
    """
    Pass in dataframes and merge them on the FirmID column
    Remove any duplicate columns also

    Parameters:
    data_frames: Dataframes to merge

    Returns:
    df: Merged dataframe
    """
    try:
        x = data_frames[0]["firm_id"]
    except Exception as e:
        logging.exception(e)
        logging.exception("Did the dataframes have firm_id?")
        return False
    logging.debug("Dataframe contains FirmID - Success")

    cols_to_keep = [
        "firm_id",
        "state_incorporated",
        "name_id",
        "company_name",
        "phone_id",
        "phone",
        "url_id",
        "url",
        "email_id",
        "email",
        "address_1",
        "address_2",
        "city",
        "zip_code",
    ]
    # Merges multiple dataframes on FirmID via the amazing reduce function and the merge with the lambda to iterate over it
    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on=["firm_id"], how="outer"),
        data_frames,
    )

    # Removes duplicate columns
    # df = df_merged.loc[:,~df_merged.duplicated()]
    df = df_merged
    # Keeps only the needed cols defined earlier
    cols_to_keep = [col for col in cols_to_keep if col in df.columns]
    df = df[cols_to_keep]
    # Filter out all non-MN businesses
    try:
        df = df[df["state_incorporated"] == "MN"]
    except:
        logging.debug("state_incoporated didn't exist")
    # Create a new column with the address
    df["Address"] = df[["address_1", "address_2", "city",]].apply(
        lambda x: np.nan
        if pd.isna(x["address_1"]) or pd.isna(x["address_2"]) or pd.isna(x["city"])
        else f"{x['address_1']} {x['address_2']} {x['city']}",
        axis=1,
    )
    # Renamed the addresses
    df = df.rename(
        columns={
            "company_name": "BusinessName",
            "phone": "Phone",
            "email": "Email",
            "url": "Website",
            "city": "City",
        }
    )
    # Remove duplicate columns in the dataframe
    df = df_merged.loc[:, ~df_merged.columns.duplicated()]
    logging.info("Merging dataframes - Success")
    return df


df1 = pd.DataFrame(
    {
        "firm_id": [1, 2, 3],
        "state_incorporated": ["MN", "MN", "MN"],
        "name_id": [1, 2, 3],
        "company_name": ["ABC Inc.", "XYZ Corp.", "123 LLC"],
        "phone_id": [1, 2, 3],
        "phone": ["123-456-7890", "555-555-5555", "999-999-9999"],
    }
)
df2 = pd.DataFrame(
    {
        "firm_id": [2, 3, 4],
        "url_id": [1, 2, 3],
        "url": [
            "http://www.xyzcorp.com",
            "http://www.123llc.com",
            "http://www.456inc.com",
        ],
        "email_id": [1, 2, 3],
        "email": ["info@xyzcorp.com", "info@123llc.com", "info@456inc.com"],
    }
)
df3 = pd.DataFrame(
    {
        "firm_id": [1, 3, 4],
        "address_1": ["123 Main St", "456 Elm St", "789 Oak St"],
        "address_2": ["Suite 100", "Suite 200", ""],
        "city": ["Minneapolis", "St. Paul", "Bloomington"],
        "zip_code": ["55401", "55101", "55420"],
    }
)


print(join_dataframe_firmid(df1, df2, df3))
# Read data from the specified file and return a DataFrame containing information for the active businesses
def get_valid_businesses_info(file_path: str) -> pd.DataFrame | None:
    """
    Read the data from the specified file into a DataFrame and filter the DataFrame to only keep rows where
    'active' == 'TRUE'. If an error occurs, None is returned.

    Parameters:
    file_path: Relative path to the file to read

    Returns:
    DataFrame containing information for the active businesses or None if an error occurs
    """
    try:
        # Read the data from the specified file into a DataFrame
        df = pd.read_csv(file_path)

        # Ensure the "active" column is treated as a string
        df["active"] = df["active"].astype(str)

        # Filter the DataFrame to only keep rows where 'active' == 'TRUE'
        active_businesses_df = df[df["active"].str.strip().str.upper() == "TRUE"]

        # Log success message
        logging.info(f"Successfully read and filtered data from file: {file_path}")

        # Only return business information for the active businesses
        return active_businesses_df
    except Exception as e:
        # Log error message
        logging.error(
            f"Error reading or filtering data from file: {file_path}. Error: {e}"
        )
        return None


def main():
    # Extract the data
    # Need to build a function which takes in a file path for a csv file, and outputs a dataframe
    mn_business = get_valid_businesses_info("BBBDM/Data/mn_business.csv")
    mn_business_address = extract_data("BBBDM/Data/mn_business_address.csv")
    mn_business_contact = extract_data("BBBDM/Data/mn_business_contact.csv")
    mn_business_email = extract_data("BBBDM/Data/mn_business_email.csv")
    mn_business_name = extract_data("BBBDM/Data/mn_business_name.csv")
    mn_business_phone = extract_data("BBBDM/Data/mn_business_phone.csv")
    mn_business_url = extract_data("BBBDM/Data/mn_business_url.csv")

    # Merge the data
    merged_data = join_dataframe_firmid(
        mn_business,
        mn_business_address,
        mn_business_contact,
        mn_business_email,
        mn_business_name,
        mn_business_phone,
        mn_business_url,
    )

    # Create valid/invalid dataframes
    valid_data, invalid_data = filter_dataframes(merged_data)

    # Standardize the valid data
    valid_data = normalize_dataframe(valid_data)
    invalid_data = normalize_dataframe(invalid_data)

    # Compare to SOS, updating when necessary
    path_to_sos = ""
    SOS_data = extract_data(path_to_sos)
    valid_data = compare_dataframes(valid_data, SOS_data)

    # Compare to Google API

    # Compare to YP

    # Merge with bad data

    # Output csv
    pass


if __name__ == "__main__":
    main()
