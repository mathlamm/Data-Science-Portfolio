# Functions for Streamlit WebApp (see app.py)


# Import libraries
from pdf2image import convert_from_path, convert_from_bytes
import pandas as pd
import pytesseract
from dateutil.relativedelta import relativedelta


# extracts data points from one box in a df by position 
def extract_data_point(df, coord_left_start, coord_left_end, coord_top_start, coord_top_end, further_conditions=None, sentence=True):
    # find data points at defined positions. Only look at data points who are likely text (conf)
    filtered_df = df.loc[(df.left.between(coord_left_start, coord_left_end)) & 
                         (df.top.between(coord_top_start, coord_top_end)) &
                         (df['conf'] > -1)]  # Adjust conf condition as needed

    # Check if any data points were found
    if filtered_df.empty:
        return None

    # Adjust top position of multiple elements in one line, if they only slightly differ, to keep the elements in the right order of sorting
    height_tolerance = 2
    if not filtered_df[filtered_df["text"] != ""].empty:
        pos_first_text = filtered_df[filtered_df["text"] != ""].iloc[0]["top"]
        pos_last_text = filtered_df[filtered_df["text"] != ""].iloc[-1]["top"]

        # adjust line top position in first line
        filtered_df.loc[filtered_df.top.between(pos_first_text-height_tolerance, pos_first_text+height_tolerance), "top"] = pos_first_text

        # adjust line top position in last line
        filtered_df.loc[filtered_df.top.between(pos_last_text-height_tolerance, pos_last_text+height_tolerance), "top"] = pos_last_text

    # sort by top and left
    filtered_df = filtered_df.sort_values(["top", "left"])

    # return results based on the request type (full sentence or single data point)
    if sentence:
        return " ".join(filtered_df["text"]) if not filtered_df.empty else None
    else:
        # Return single data point (first found, if many)
        return filtered_df.iloc[0].to_dict() if not filtered_df.empty else None
        


def extract_iol_v19(file):
    # define local path of tesseract (work around for tesseracts errors)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # convert pdf to image
    pages = convert_from_bytes(file.read())

    # use googles OCR technology in pytesseract to extract text from images
    d = pytesseract.image_to_data(pages[0], output_type=pytesseract.Output.DICT)
    d_df = pd.DataFrame.from_dict(d)

    ### Extract data by position
    half_page_width = 710

    # Patient number
    patnr = extract_data_point(d_df, 360, 380, 220, 240)

    # Examination date
    exam_date = extract_data_point(d_df, 370, 410, 430, 470)

    # birthdate
    birthdate = extract_data_point(d_df, 360, 500, 190, 230)

    # lens category (monofokal vs ...)
    lens_cat = extract_data_point(d_df, 360, 380, 280, 310)

    # IOL RIGHT
    AL_R = extract_data_point(d_df, 215, 250, 970, 990)
    VKT_R = extract_data_point(d_df, 215, 250, 1000, 1020)
    LD_R = extract_data_point(d_df, 215, 250, 1030, 1050)
    WZW_R = extract_data_point(d_df, 215, 250, 1065, 1085)
    R_R = extract_data_point(d_df, 215, 250, 1090, 1115)
    DeltaD_R = extract_data_point(d_df, 215, 250, 1125, 1150)
    R1_R = extract_data_point(d_df, 630, 650, 1090, 1115)
    R2_R = extract_data_point(d_df, 630, 650, 1125, 1150)
    RA_aim_R = extract_data_point(d_df, 275, 300, 895, 915)

    # IOL LEFT
    AL_L = extract_data_point(d_df, 215 + half_page_width, 250 + half_page_width, 970, 990)
    VKT_L = extract_data_point(d_df, 215 + half_page_width, 250 + half_page_width, 1000, 1020)
    LD_L = extract_data_point(d_df, 215 + half_page_width, 250 + half_page_width, 1030, 1050)
    WZW_L = extract_data_point(d_df, 215 + half_page_width, 250 + half_page_width, 1065, 1085)
    R_L = extract_data_point(d_df, 215 + half_page_width, 250 + half_page_width, 1090, 1115)
    DeltaD_L = extract_data_point(d_df, 215 + half_page_width, 250 + half_page_width, 1125, 1150)
    R1_L = extract_data_point(d_df, 630 + half_page_width, 650 + half_page_width, 1090, 1115)
    R2_L = extract_data_point(d_df, 630 + half_page_width, 650 + half_page_width, 1125, 1150)
    RA_aim_L = extract_data_point(d_df, 275 + half_page_width, 300 + half_page_width, 895, 915)
    

    ### Combine to df
    # start df
    data_row = pd.DataFrame([{
            "patnr": patnr,
            "birthdate": birthdate,
            "exam_date": exam_date,
            "lens_cat": lens_cat,
            "AL_R": AL_R,
            "VKT_R": VKT_R,
            "LD_R": LD_R,
            "R_R": R_R,
            "R1_R": R1_R,
            "R2_R": R2_R,
            "DeltaD_R": DeltaD_R,
            "WZW_R": WZW_R,
            "RA_aim_R": RA_aim_R,
            "AL_L": AL_L,
            "VKT_L": VKT_L,
            "LD_L": LD_L,
            "R_L": R_L,
            "R1_L": R1_L,
            "R2_L": R2_L,
            "DeltaD_L": DeltaD_L,
            "WZW_L": WZW_L,
            "RA_aim_L": RA_aim_L,
        }])

    return data_row




# Extract all potential lenses from page 1 and 2 (up to 4 on each page): their name and their 5 versions differing in strenght, including the predicted refraction error
def iol_lenses_v19(pdf_file):
    # initiate pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # convert pdf to image
    pages = convert_from_path(pdf_file)

    # distances between bounding boxes
    block_width = 350
    block_height = 355
    LR_width = 709
    lens_version_line_height = 31

    # inittiate df
    iol_v = pd.DataFrame()

    # iterate through page 1 and 2
    for p in range(2 if len(pages) >= 2 else 1):

        # use googles OCR technology in pytesseract to extract text from images.
        d = pytesseract.image_to_data(pages[p], output_type=pytesseract.Output.DICT)
        d_df = pd.DataFrame.from_dict(d)

        # look for page header "IOL-Berechnung" -> break loop if it does not exist
        header = extract_data_point(d_df, 700, 800, 630, 700)
        if not header or ("rechnung" not in header):
            break

        # extract general information to identify the IOL biometry
        patnr = extract_data_point(d_df, 360, 380, 220, 240)        # Patient number  
        exam_date = extract_data_point(d_df, 370, 410, 430, 470)    # examination date
        lens_cat = extract_data_point(d_df, 360, 380, 280, 310)     # lens category 

        # iterate through right and left side (eye R and eye L)
        for LR in range(2):
            # define side as string
            LR_str = "R" if LR == 0 else "L"

            RA_aim = extract_data_point(d_df, 275 + LR*LR_width, 300 + LR*LR_width, 895, 915)     # Refraction aim

            # iterate through the lens suggestions vertically: up to down
            for v_ver in range(2):

                # iterate through the lens suggestions horizontally: left to right
                for v_hor in range(2):

                    # lens name
                    lens = extract_data_point(
                        d_df,
                        170 + v_hor * block_width + LR * LR_width,
                        490 + v_hor * block_width + LR * LR_width,
                        1230 + v_ver * block_height,
                        1280 + v_ver * block_height,
                    )   

                    # lens a constants
                    lens_a_const = extract_data_point(
                        d_df,
                        150 + v_hor * block_width + LR * LR_width,
                        480 + v_hor * block_width + LR * LR_width,
                        1310 + v_ver * block_height,
                        1340 + v_ver * block_height,
                    )

                    # iterate through each of the 5 lens suggestions (IOL in dpt) and their according expected refraction error (Refr in dpt)
                    for v in range(5):

                        # left column of potential lens versions (IOL in dpt)
                        iol = extract_data_point(
                            d_df,
                            215 + v_hor * block_width + LR * LR_width,
                            325 + v_hor * block_width + LR * LR_width,
                            1370 + v_ver * block_height + v * lens_version_line_height,
                            1400 + v_ver * block_height + v * lens_version_line_height,
                        )

                        # right column of potential lens versions (predicted Refraction in dpt)
                        refr = extract_data_point(
                            d_df,
                            378 + v_hor * block_width + LR * LR_width,
                            455 + v_hor * block_width + LR * LR_width,
                            1370 + v_ver * block_height + v * lens_version_line_height,
                            1400 + v_ver * block_height + v * lens_version_line_height,
                        )

                        # build dataframe
                        iol_v_line = pd.DataFrame(
                            {
                                "filename": pdf_file,
                                "patnr": patnr,
                                "exam_date": exam_date,
                                "lens_cat": lens_cat,
                                "RA_aim": RA_aim,
                                "side": LR_str,
                                "lens": lens,
                                "v": v + 1,
                                "iol": [iol],
                                "refr": [refr],
                                "lens_a_const" : lens_a_const
                            }
                        )
                        iol_v = pd.concat([iol_v, iol_v_line], axis=0)

    return iol_v



# Function to clean columns
def clean_col(x):
    return (x.astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace("[^0-9.]", "", regex=True)
        .str.replace("..", ".", regex=False)
        .str.replace('\.(?=\D|$)', '', regex=True)  # remove dot, if followed by non-numeric character or at the end of the string
    )



# Function to insert decimals, if missing
def insert_decimal(s):
    if pd.isna(s):  # Check for NaN values and return as is
        return s
    s = str(s)  # Convert to string to ensure consistency in processing
    if '.' not in s:  # Check if the decimal point is missing
        if len(s) > 2:
            s = s[:-2] + '.' + s[-2:]  # Insert the decimal point before the last two digits
        else:
            s 
    return s



# Function to calculate age
def calculate_age(birthdate, refr_date):
    return relativedelta(refr_date, birthdate).years



def iol_clean(iol_raw):
    # Patnr
    iol_raw["patnr"] = iol_raw["patnr"].astype("int")

    # birthdate date
    iol_raw["birthdate"] = pd.to_datetime(iol_raw["birthdate"], dayfirst=True)

    # exam date
    iol_raw["exam_date"] = pd.to_datetime(iol_raw["exam_date"], dayfirst=True)

    # Lens category
    if (~iol_raw["lens_cat"].isin(["monofokal", "torisch"])).sum() != 0:
        print("only supports Lens types: monofocal, torisch")
        return pd.DataFrame()

    # Refraction aim
    iol_raw.loc[iol_raw["RA_aim_L"] == "Plan", ["RA_aim_L"]] = 0
    iol_raw.loc[iol_raw["RA_aim_R"] == "Plan", ["RA_aim_R"]] = 0

    # define columns
    col_num = iol_raw.drop(["patnr", "exam_date", "lens_cat", "birthdate"], axis=1)

    # Apply cleaning function to multiple columns
    col_num = col_num.apply(clean_col)

    # insert digits in certain columns
    col_2dig = ["AL_R","VKT_R", "LD_R", "R_R", "R1_R", "R2_R", "DeltaD_R", "AL_L","VKT_L", "LD_L", "R_L", "R1_L", "R2_L", "DeltaD_L"]
    for col in col_2dig:
        col_num[col] = col_num[col].apply(insert_decimal)

    # transform to numeric
    col_num = col_num.apply(pd.to_numeric)

    # save in iol_raw
    iol_raw[col_num.columns] = col_num

    # Calculate Age at time of IOL Master
    iol_raw["age"] = iol_raw.apply(
    lambda row: calculate_age(row["birthdate"], row["exam_date"]), axis=1
    )

    iol_long = pd.wide_to_long(
        iol_raw,
        stubnames=[
            "AL",
            "VKT",
            "LD",
            "R",
            "R1",
            "R2",
            "DeltaD",
            "WZW",
            "RA_aim"
        ],
        i=["patnr", "birthdate", "exam_date", "lens_cat", "age"],
        j="side",
        suffix="[RL]",
        sep="_",
    ).reset_index()


    return iol_long

# create a list of numbers, that centers around a given number
def generate_centered_list(num, total_count=5, step=0.5):
    # Calculate the starting point by subtracting half the total desired range from the number
    start = num - (total_count // 2) * step
    # Create the list using a list comprehension
    return [start + i * step for i in range(total_count)]