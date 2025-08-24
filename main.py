import time
import streamlit as st
import os
import pandas as pd
from database import *
from face_matching import get_requisition_numbers
from files_handler import process_uploaded_files
from config import UPLOADS_FOLDER

st.title("Upload and get a person's records")
print("\n" * 50)

if "connection" not in st.session_state and "cursor" not in st.session_state:
    st.session_state.connection, st.session_state.cursor = get_db_connection()

connection = st.session_state.connection
cursor = st.session_state.cursor

st.sidebar.title("Upload Files")
uploaded_files = st.sidebar.file_uploader(
    "Select files", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

if st.sidebar.button("Upload"):
    if uploaded_files:
        try:
            with st.spinner("Processing..."):
                start = time.time()
                process_uploaded_files(
                    uploaded_files,
                )
                time_taken = time.time() - start
                print(
                    f"Processing uploaded files took: {time_taken:.2f}, ({len(uploaded_files)} images)"
                )
                st.toast("Files uploaded successfully!")
        except Exception as e:
            st.error(str(e).replace("\n", "  \n"))
            st.stop()
    else:
        st.toast("Please upload at least one file.")

uploaded_img = st.file_uploader(
    label="Upload an image", type=["jpg", "jpeg", "png"], accept_multiple_files=False
)


if not os.path.exists(UPLOADS_FOLDER):
    os.mkdir(UPLOADS_FOLDER)

if uploaded_img:
    with st.expander("View image:"):
        st.image(
            uploaded_img,
            caption="Uploaded image",
            width=300,
        )
    try:
        img_path = os.path.join(UPLOADS_FOLDER, uploaded_img.name)
        with open(img_path, "wb") as f:
            f.write(uploaded_img.read())

        if st.button("Get Records"):
            with st.spinner("Please wait"):
                start = time.time()

                try:
                    requisition_number = get_requisition_numbers(
                        img_path=img_path,
                    )

                    if requisition_number:
                        try:
                            records = get_records(
                                requisition_number=requisition_number,
                                connection=connection,
                                cursor=cursor,
                            )
                            records.sort(key=lambda x: int(x["REQUISITIONNO"]))

                            number_of_records = len(records)
                            name = records[0]["VISITORNAME"]

                            dept = set()
                            for rec in records:
                                dept.add(rec["DEPARTMENT"])
                            dept = list(dept)
                            emp_id = records[0]["EMPLOYEEID"]

                            st.markdown(f"- **Number of visits**: {number_of_records}")
                            st.markdown(f"- **Name**: {name.title()}")
                            st.markdown(f"- **Department**: {', '.join(dept)}")
                            st.markdown(f"- **ID**: {emp_id}")

                            with st.expander("View detailed results:"):
                                df = pd.DataFrame(records)
                                st.success("Records Found:")
                                st.dataframe(df)
                        except:
                            st.info("No records exist.")
                    else:
                        st.error("No matching faces found for the uploaded image.")
                except ValueError:
                    st.error("No faces found in the uploaded image.")

                time_taken = time.time() - start
                st.toast(f"Time taken: {round(time_taken)} seconds")
                print(f"Time taken: {round(time_taken)} seconds\n\n\n")

    finally:
        try:
            os.remove(img_path)
        except:
            pass