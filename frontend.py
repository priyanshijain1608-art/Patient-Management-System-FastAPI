#making a streamlit website for interaction of patient management system api with frontend
import streamlit as st
import requests
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Patient Management System",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Patient Management System")

menu = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Create Patient",
        "View All Patients",
        "View One Patient",
        "Update Patient",
        "Delete Patient",
        "Sort Patients"
    ]
)

# ---------------- CREATE ----------------

if menu == "Create Patient":

    st.header("Create New Patient")

    patient_id = st.text_input("Patient ID")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    weight = st.number_input("Weight", min_value=1.0)

    if st.button("Create"):

        payload = {
            "id": patient_id,
            "name": name,
            "age": age,
            "weight": weight
        }

        response = requests.post(
            f"{BASE_URL}/create",
            json=payload
        )

        if response.status_code == 201:
            st.success("Patient Created Successfully")
        else:
            st.error(response.text)

# ---------------- VIEW ALL ----------------

elif menu == "View All Patients":

    st.header("All Patients")

    if st.button("Load Patients"):

        response = requests.get(f"{BASE_URL}/view")

        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Unable to fetch data")

# ---------------- VIEW ONE ----------------

elif menu == "View One Patient":

    st.header("Search Patient")

    patient_id = st.text_input("Enter Patient ID")

    if st.button("Search"):

        response = requests.get(
            f"{BASE_URL}/view/{patient_id}"
        )

        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(response.json()["detail"])

# ---------------- UPDATE ----------------

elif menu == "Update Patient":

    st.header("Update Patient")

    patient_id = st.text_input("Patient ID")

    name = st.text_input("New Name")

    age = st.number_input(
        "New Age",
        min_value=0,
        max_value=120,
        value=0
    )

    weight = st.number_input(
        "New Weight",
        min_value=0.0,
        value=0.0
    )

    if st.button("Update"):

        payload = {}

        if name:
            payload["name"] = name

        if age > 0:
            payload["age"] = age

        if weight > 0:
            payload["weight"] = weight

        response = requests.put(
            f"{BASE_URL}/update/{patient_id}",
            json=payload
        )

        if response.status_code == 200:
            st.success("Patient Updated Successfully")
        else:
            st.error(response.text)

# ---------------- DELETE ----------------

elif menu == "Delete Patient":

    st.header("Delete Patient")

    patient_id = st.text_input("Patient ID")

    if st.button("Delete"):

        response = requests.delete(
            f"{BASE_URL}/delete/{patient_id}"
        )

        if response.status_code == 200:
            st.success("Patient Deleted Successfully")
        else:
            st.error(response.text)

# ---------------- SORT ----------------

elif menu == "Sort Patients":

    st.header("Sort Patients")

    sort_by = st.selectbox(
        "Sort By",
        ["age", "weight"]
    )

    order = st.selectbox(
        "Order",
        ["asc", "desc"]
    )

    if st.button("Sort"):

        response = requests.get(
            f"{BASE_URL}/sort",
            params={
                "sort_by": sort_by,
                "order": order
            }
        )

        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error(response.text)