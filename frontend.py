# Making a Streamlit website for interaction with Patient Management System API

import streamlit as st
import requests

BASE_URL = "https://patient-management-system-fastapi-4em.onrender.com"

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


# ============================================================
# HELPER FUNCTION FOR ERROR HANDLING
# ============================================================

def show_error(response):
    """
    Displays API errors safely.
    Handles both JSON and non-JSON responses.
    """

    try:
        error_data = response.json()

        if isinstance(error_data, dict):
            detail = error_data.get("detail")

            if detail:
                st.error(str(detail))
            else:
                st.error(str(error_data))
        else:
            st.error(str(error_data))

    except ValueError:
        st.error(
            f"Request failed with status code {response.status_code}"
        )

        if response.text:
            st.code(response.text)


# ============================================================
# CREATE PATIENT
# ============================================================

if menu == "Create Patient":

    st.header("Create New Patient")

    patient_id = st.text_input("Patient ID")
    name = st.text_input("Patient Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=1
    )

    weight = st.number_input(
        "Weight",
        min_value=1.0,
        value=1.0
    )

    if st.button("Create"):

        if not patient_id:
            st.warning("Please enter Patient ID.")

        elif not name:
            st.warning("Please enter Patient Name.")

        else:

            payload = {
                "id": patient_id,
                "name": name,
                "age": age,
                "weight": weight
            }

            try:

                response = requests.post(
                    f"{BASE_URL}/create",
                    json=payload,
                    timeout=30
                )

                if response.status_code in [200, 201]:

                    st.success("Patient Created Successfully")

                    try:
                        st.json(response.json())
                    except ValueError:
                        st.write(response.text)

                else:
                    show_error(response)

            except requests.exceptions.RequestException as e:
                st.error(f"Unable to connect to backend: {e}")


# ============================================================
# VIEW ALL PATIENTS
# ============================================================

elif menu == "View All Patients":

    st.header("All Patients")

    if st.button("Load Patients"):

        try:

            response = requests.get(
                f"{BASE_URL}/view",
                timeout=30
            )

            if response.status_code == 200:

                try:
                    st.json(response.json())

                except ValueError:
                    st.error("Backend returned an invalid response.")

            else:
                show_error(response)

        except requests.exceptions.RequestException as e:
            st.error(f"Unable to connect to backend: {e}")


# ============================================================
# VIEW ONE PATIENT
# ============================================================

elif menu == "View One Patient":

    st.header("Search Patient")

    patient_id = st.text_input("Enter Patient ID")

    if st.button("Search"):

        if not patient_id:
            st.warning("Please enter Patient ID.")

        else:

            try:

                response = requests.get(
                    f"{BASE_URL}/view/{patient_id}",
                    timeout=30
                )

                if response.status_code == 200:

                    try:
                        st.json(response.json())

                    except ValueError:
                        st.error(
                            "Backend returned an invalid response."
                        )

                else:
                    show_error(response)

            except requests.exceptions.RequestException as e:
                st.error(f"Unable to connect to backend: {e}")


# ============================================================
# UPDATE PATIENT
# ============================================================

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

        if not patient_id:
            st.warning("Please enter Patient ID.")

        else:

            payload = {}

            if name:
                payload["name"] = name

            if age > 0:
                payload["age"] = age

            if weight > 0:
                payload["weight"] = weight

            if not payload:

                st.warning(
                    "Please enter at least one field to update."
                )

            else:

                try:

                    response = requests.put(
                        f"{BASE_URL}/update/{patient_id}",
                        json=payload,
                        timeout=30
                    )

                    if response.status_code == 200:

                        st.success(
                            "Patient Updated Successfully"
                        )

                        try:
                            st.json(response.json())

                        except ValueError:
                            st.write(response.text)

                    else:
                        show_error(response)

                except requests.exceptions.RequestException as e:
                    st.error(
                        f"Unable to connect to backend: {e}"
                    )


# ============================================================
# DELETE PATIENT
# ============================================================

elif menu == "Delete Patient":

    st.header("Delete Patient")

    patient_id = st.text_input("Patient ID")

    if st.button("Delete"):

        if not patient_id:
            st.warning("Please enter Patient ID.")

        else:

            try:

                response = requests.delete(
                    f"{BASE_URL}/delete/{patient_id}",
                    timeout=30
                )

                if response.status_code == 200:

                    st.success(
                        "Patient Deleted Successfully"
                    )

                    try:
                        st.json(response.json())

                    except ValueError:
                        st.write(response.text)

                else:
                    show_error(response)

            except requests.exceptions.RequestException as e:
                st.error(
                    f"Unable to connect to backend: {e}"
                )


# ============================================================
# SORT PATIENTS
# ============================================================

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

        try:

            response = requests.get(
                f"{BASE_URL}/sort",
                params={
                    "sort_by": sort_by,
                    "order": order
                },
                timeout=30
            )

            if response.status_code == 200:

                try:
                    st.json(response.json())

                except ValueError:
                    st.error(
                        "Backend returned an invalid response."
                    )

            else:
                show_error(response)

        except requests.exceptions.RequestException as e:
            st.error(
                f"Unable to connect to backend: {e}"
            )
