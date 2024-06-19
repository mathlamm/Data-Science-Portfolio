###
### ** Webapp Prototype for Predicion of Postoperative Refraction Error in Cataract Surgery **
###
### This app enables users to predict the individual patients refraction error after cataract surgery. 
### The ML model is trained on +5000 cataract surgeries.
### The app uses Optical Biometry markers (as measured by ZEUSS IOL Master) and
### the selected lens parameters as input. The aim is to find the correct lens power that is needed for a
### disered postoperative refraction error (often -0.5 to 0.0).
###
### This project was my final project during a Data Science Bootcamp at WBS Coding School in 2024. 
###
###
### Disclaimer: At this moment, the models performance is not sufficient for a reliable prediction. Further refinement and
### possibly data acquirement is necessary.
###
### Mathis Lammert
### JUN 2024
### 


# Import libraries
import pandas as pd
import streamlit as st
import pickle
from functions import extract_iol_v19, iol_clean, generate_centered_list

# Initialize input variables
default_AL_R = ""
default_VKT_R = ""
default_LD_R = ""
default_R_R = ""
default_R1_R = ""
default_DeltaD_R = ""
default_WZW_R = ""
default_AL_L = ""
default_VKT_L = ""
default_LD_L = ""
default_R_L = ""
default_R1_L = ""
default_DeltaD_L = ""
default_WZW_L = ""
default_Age = ""


# Load model
model_path = "data/trained_pipe_v1.sav"
loaded_model = pickle.load(open(model_path, 'rb'))

# Load additional tables
lens_types_in_v1 = pd.read_csv("data/lens_types_in_v1.csv")

# Session state initialization
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = False



#### Start Page 

# Title and info
st.title("Intraocular Lens Finder")

info_text = """This model predicts the refraction error after cataract surgery, based on patient data and lens type. \n\n
It is trained on +5000 cases of primary Phacoemulsification or Femto-Laser assisted cataract surgery with the Implantation of either monofocal or toric lenses between 2016 and 2024."""
st.info(info_text, icon="ℹ️")

# Drag and drop PDF file
with st.container(border=True):
    st.write("Start with uploading the IOL Master PDF here")
    pdf_file = st.file_uploader("IOL Master PDF (v1.9)", type="pdf")

# Cache data functions
@st.cache_data
def extract_and_clean_data(pdf_file):
    # Extract data from PDF and clean it
    data_raw = extract_iol_v19(pdf_file) 
    data = iol_clean(data_raw)  
    return data


# Extract Information from PDF file
if pdf_file is not None:

    # inititalize cached extract and clean-function 
    data = extract_and_clean_data(pdf_file)
    
    if not data.empty:

        # Try to set default values based on the data extracted from the PDF
        if not data[data['side'] == 'R'].empty:
            default_AL_R = data.loc[data['side'] == 'R', 'AL'].iloc[0]
            default_VKT_R = data.loc[data['side'] == 'R', 'VKT'].iloc[0]
            default_LD_R = data.loc[data['side'] == 'R', 'LD'].iloc[0]
            default_R_R = data.loc[data['side'] == 'R', 'R'].iloc[0]
            default_R1_R = data.loc[data['side'] == 'R', 'R1'].iloc[0]
            default_DeltaD_R = data.loc[data['side'] == 'R', 'DeltaD'].iloc[0]
            default_WZW_R = data.loc[data['side'] == 'R', 'WZW'].iloc[0]
            default_Age = data.loc[data['side'] == 'R', 'age'].iloc[0]
        if not data[data['side'] == 'L'].empty:
            default_AL_L = data.loc[data['side'] == 'L', 'AL'].iloc[0]
            default_VKT_L = data.loc[data['side'] == 'L', 'VKT'].iloc[0]
            default_LD_L = data.loc[data['side'] == 'L', 'LD'].iloc[0]
            default_R_L = data.loc[data['side'] == 'L', 'R'].iloc[0]
            default_R1_L = data.loc[data['side'] == 'L', 'R1'].iloc[0]
            default_DeltaD_L = data.loc[data['side'] == 'L', 'DeltaD'].iloc[0]
            default_WZW_L = data.loc[data['side'] == 'L', 'WZW'].iloc[0]
            default_Age = data.loc[data['side'] == 'L', 'age'].iloc[0]

# Biometry data input - should be filled in automatically after PDF upload
with st.expander("Optical Biometry Data", expanded=True):

    st.write("Upload PDF or fill in manually.")

    tabR, tabL = st.tabs(["Right", "Left"])

    with tabR: 
        iolm_c1, iolm_c2 = st.columns(2)
        with iolm_c1:
            input_AL_R = st.text_input("AL", value=default_AL_R, key="input_AL_R")
            input_VKT_R = st.text_input("VKT", value=default_VKT_R, key="input_VKT_R")
            input_LD_R = st.text_input("LD", value=default_LD_R, key="input_LD_R")

        with iolm_c2:
            input_R_R = st.text_input("R", value=default_R_R, key="input_R_R")
            input_R1_R = st.text_input("R1", value=default_R1_R, key="input_R1_R")
            input_DeltaD_R = st.text_input("Delta D", value=default_DeltaD_R, key="input_DeltaD_R")
            input_WZW_R = st.text_input("WZW", value=default_WZW_R, key="input_WZW_R")

    with tabL: 
        iolm_c1, iolm_c2 = st.columns(2)
        with iolm_c1:
            input_AL_L = st.text_input("AL", value=default_AL_L, key="input_AL_L")
            input_VKT_L = st.text_input("VKT", value=default_VKT_L, key="input_VKT_L")
            input_LD_L = st.text_input("LD", value=default_LD_L, key="input_LD_L")

        with iolm_c2:
            input_R_L = st.text_input("R", value=default_R_L, key="input_R_L")
            input_R1_L = st.text_input("R1", value=default_R1_L, key="input_R1_L")
            input_DeltaD_L = st.text_input("Delta D", value=default_DeltaD_L, key="input_DeltaD_L")
            input_WZW_L = st.text_input("WZW", value=default_WZW_L, key="input_WZW_L")  

# Input Age and Sex
with st.container(border=True):
    pat_c1, pat_c2 = st.columns(2)
    with pat_c1:
        input_age = st.text_input("Age", value=default_Age,key="input_age")
    with pat_c2:
        # Select Sex (1 = male, 2= female)
        sex_options = {"male": 1, "female": 2}
        input_sex = st.selectbox("Sex", list(sex_options), key="input_sex")  

# Input Lens type and Power
with st.container(border=True):
    st.write("Chose a Lens Series and Power")
    iol_c1, iol_c2= st.columns(2)
    with iol_c1:
        # Chose Lens Series. Preselected: most common lens type
        input_lens_series = st.selectbox(
            "Lens Series",
            options=lens_types_in_v1["lens_series"]
            .value_counts()
            .reset_index()["lens_series"],
        )

        st.markdown('#')

        # Submit Button
        button_model = st.button("Run Prediction", key="button_model")

        # Set initialized to True after data is loaded
        if button_model:
            st.session_state['initialized'] = True

    with iol_c2:
        # Chose Lens Power from a list of possible lens powers, depending on lens type. Preselected: Median of possible lens powers
        lens_series_list = (
            lens_types_in_v1.loc[lens_types_in_v1["lens_series"] == input_lens_series]
            .drop_duplicates()["IOL_dpt"]
            .sort_values()
        )
        input_lens_power = st.selectbox(
            "Lens Power", options=lens_series_list, index=int(len(lens_series_list) / 2)
        )  # only show those that exist in training dataset per lens series

        range_col1, range_col2, range_col3 = st.columns(3)
        with range_col1:
            input_side = st.selectbox("Side", options=["R", "L"])
        with range_col2:
            input_steps = st.selectbox("Steps", options=[0.5, 1.0, 1.5])
        with range_col3:
            options_range = {"None":1,"+-1":3, "+-2":5, "+-10":21}
            input_range = st.selectbox("Range", options=options_range)


# Create dataframe with input data for predict, including left and right
if 'initialized' in st.session_state and st.session_state['initialized']:
    features_df = pd.DataFrame(
    {   "side": ["R", "L"],
        "lens_series": [input_lens_series]*2,
        "IOL_dpt": [input_lens_power]*2,
        "AL": [input_AL_R, input_AL_L],
        "VKT": [input_VKT_R, input_VKT_L],
        "LD": [input_LD_R, input_LD_L],
        "R": [input_AL_R, input_AL_L],
        "R1": [input_R1_R, input_R1_L],
        "DeltaD": [input_DeltaD_R, input_DeltaD_L],
        "WZW": [input_WZW_R, input_WZW_L],
        "sex": [sex_options[input_sex]]*2,
        "age": [input_age]*2,
    }
)
    pass


# Show prediction results
if button_model or (st.session_state['initialized'] and not button_model):
    with st.container(border=True):

        # expand df with to fit range of predictions
        num = options_range[input_range]
        features_expanded_df = pd.concat([features_df] * num, ignore_index=True)
        features_expanded_df.loc[features_expanded_df["side"] == "R", "IOL_dpt"] = (
            generate_centered_list(
                input_lens_power,
                total_count=num,
                step=input_steps,
            )
        )
        features_expanded_df.loc[features_expanded_df["side"] == "L", "IOL_dpt"] = (
            generate_centered_list(
                input_lens_power,
                total_count=num,
                step=input_steps,
            )
        )

        # Compute predictions
        pred_outcome = loaded_model.predict(features_expanded_df.drop(["side"], axis=1)).round(2)

        # build combined df
        pred_df = pd.concat([features_expanded_df, pd.DataFrame({"se": pred_outcome})], axis=1)

        # select prediction
        pred_sel = pred_df.loc[pred_df["side"] == input_side, ["IOL_dpt", "se"]]
        pred_sel = pred_sel.rename(columns={"IOL_dpt": "Lens Power", "se": "Predicted Refraction Error"})


        pred_c1, pred_c2= st.columns(2)
        with pred_c1:
            # show prediction dataframe
            st.dataframe(pred_sel, hide_index=True)
        with pred_c2:
            st.line_chart(pred_sel, x="Lens Power", y="Predicted Refraction Error")

