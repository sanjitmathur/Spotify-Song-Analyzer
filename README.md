# Spotify Listening Analysis Dashboard

> **Note:** These instructions are for running the project with a standard Python **`venv`** (virtual environment). This project is not configured to use `conda`. Please follow the `venv` steps below.

A Streamlit web app that analyzes your Spotify listening habits. It connects to the Spotify API to calculate your total listening time from recent plays and visualizes your top 15 tracks by popularity.

## 📋 Features

* **Secure Login:** Uses Spotify's OAuth to securely log in and access your data.
* **Listening Time:** Calculates your total listening time (in minutes) from your 50 most recently played tracks.
* **Top Tracks:** Displays your top 15 most-listened-to tracks in an interactive bar chart and a sortable table.

---

## 🚀 How to Run This Project

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

* Python 3.8+
* A Spotify Developer account (it's free) to get API keys.

### 2. Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Create a Spotify Developer App:**
    * Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in.
    * Click **"Create app"**.
    * Give it a name (e.g., "Streamlit Analysis") and a description.
    * Click **"Edit Settings"**.
    * In the **Redirect URIs** box, add this exact URL: `http://127.0.0.1:8501`
    * Click **"Save"**.
    * On your app's page, you will see your **Client ID** and **Client Secret**.

3.  **Create Your Environment File:**
    * In the project's main folder, create a new file named exactly **`.env`**
    * Copy and paste the following into this file, replacing the `...` with your keys from Step 2.
    ```
    CLIENT_ID=...
    CLIENT_SECRET=...
    ```
    > **IMPORTANT:** You must create a `.gitignore` file and add `.env` and `venv/` to it. **Never** upload your secret keys to GitHub.

4.  **Create & Activate Virtual Environment:**
    * Create the `venv`:
        ```bash
        python -m venv venv
        ```
    * Activate it (as requested in your notes). For Windows PowerShell:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

5.  **Install Dependencies:**
    * (You should first create a `requirements.txt` file by running `pip freeze > requirements.txt`)
    * Install all the packages:
        ```bash
        pip install -r requirements.txt
        ```

### 3. Run the App

1.  Make sure your virtual environment is still active (you should see `(venv)` in your terminal prompt).
2.  Run the Streamlit app using this command:
    ```bash
    streamlit run main.py
    ```
    Your browser will automatically open to `http://127.0.0.1:8501`, where you will be prompted to log in to Spotify.
