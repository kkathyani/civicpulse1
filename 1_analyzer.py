import streamlit as st
from PIL import Image
from utils.database_manager import insert_complaint
from utils.classifier import classify_complaint
from utils.mapper import get_department
from utils.priority import get_priority
from utils.generator import generate_summary
from utils.database_manager import (
    create_table,
    insert_complaint
)
from utils.database_manager import get_all_complaints
create_table()
st.write("Current Database:")

st.dataframe(get_all_complaints())


st.title("📢 CivicPulse")

st.markdown(
    "### Submit Civic Complaint"
)

tab1, tab2, tab3 = st.tabs(
    [
        "📝 Text Complaint",
        "🎤 Voice Complaint",
        "📷 Image Complaint"
    ]
)

complaint = ""

with tab1:

    complaint = st.text_area(
        "Enter Complaint in Telugu",
        height=150
    )

with tab2:

    uploaded_file = st.file_uploader(
        "Upload Complaint Image",
        type=["png","jpg","jpeg"]
    )

    if uploaded_file:

        image = Image.open(
            uploaded_file
        )

        st.image(
            image,
            width=400
        )

        st.info(
            "OCR Integration Coming Next"
        )

with tab3:

    uploaded_file = st.file_uploader(
        "Upload Complaint Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        st.image(
            image,
            width=400
        )

        temp_path = "temp_image.jpg"

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        from utils.ocr import extract_text

        extracted_text = extract_text(
            temp_path
        )

        st.subheader(
            "📝 Extracted Text"
        )

        st.text_area(
            "OCR Output",
            extracted_text,
            height=150
        )


if st.button(
    "Analyze Complaint",
    use_container_width=True
):
    st.write("ANALYZE BUTTON CLICKED")
    st.write("Complaint Value:", complaint)

    if complaint:

        category = classify_complaint(
            complaint
        )

        department = get_department(
            category
        )

        priority = get_priority(
            complaint
        )

        summary = generate_summary(
            complaint,
            category
        )

        tracking_id = insert_complaint(
            complaint,
            category,
            department,
            priority
        )
        st.write("Tracking ID:", tracking_id)
        st.write("Saved Successfully")
        st.dataframe(get_all_complaints())
     

        st.success(
            f"Complaint Registered Successfully - {tracking_id}"
        )

        col1,col2,col3 = st.columns(3)

        with col1:
            st.metric(
                "Category",
                category
            )

        with col2:
            st.metric(
                "Department",
                department
            )

        with col3:
            st.metric(
                "Priority",
                priority
            )

        st.subheader(
            "Generated Complaint Summary"
        )

        st.write(summary)

        st.download_button(
            "Download Complaint",
            summary,
            file_name=f"{tracking_id}.txt"
        )