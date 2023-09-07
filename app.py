import streamlit as st
from FinTable import AnnualReport
from io import StringIO, BytesIO



@st.cache_data
def convert_df(df):
    
    return df.to_csv(header=False).encode('utf-8-sig')

report_dict = {
    "Profit or Loss": "SOPL",
    "Financial Position": "SOFP",
    "Cash Flows": "SOCF"
}


st.title("FinTable📝")


bank_col, empty_col, download_col = st.columns(spec=[0.3, 0.3, 0.3], gap="large")

with bank_col:
    bank_toggle = st.toggle(
        "Bank🏦",
        help="Toggle widget if the company is a bank"
    )


report = st.file_uploader(
    label="Please upload annual report file",
    type=["pdf"],
    key=1,
    help="Click to upload pdf file of your annual report"
)



report_col, empty_col = st.columns(spec=[1, 2], gap="large")

report_type_list = []
with report_col:
    report_type_list.clear()
    report_type = st.selectbox(
        "Choose your report type📃",
        ["Profit or Loss", "Financial Position", "Cash Flows"],
        help="Select report statement you need. Financial Position, Cash Flow, Profit or Loss"
    )
    report_type_list.append(report_type)

if report is not None:

    try:
        report_data = BytesIO(report.getvalue())
        comp = AnnualReport(report_data, bank_toggle)
        report_type = report_dict[report_type_list[0]]

        report_file, filename = comp.download_report(
            type=report_type,
            name = report.name
        )

        csv = convert_df(report_file)

        
        with download_col:    
            st.download_button(
                label="Download Report as CSV",
                data=csv,
                file_name=filename,
                mime='text/csv',
            )
    
    except:
        st.error('An error occurred while processing the report', icon="🚨")

