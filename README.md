# Spotify Listening Analysis Dashboard

> **Note:** These instructions are for running the project with a standard Python **`venv`** (virtual environment). This project is not configured to use `conda`. Please follow the `venv` steps below.

A Streamlit web app that analyzes your Spotify listening habits. It connects to the Spotify API to calculate your total listening time from recent plays and visualizes your top 15 tracks by popularity.

----

## Features

* **Secure Login:** Uses Spotify's OAuth to securely log in and access your data.
* **Listening Time:** Calculates your total listening time (in minutes) from your 50 most recently played tracks.
* **Top Tracks:** Displays your top 15 most-listened-to tracks in an interactive bar chart and a sortable table.

---

## How to Run This Project

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

* **Python 3.8+**
* A **Spotify Developer account** (it's free) to get API keys.

### 2. Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/sanjitmathur/Spotify-Song-Analyzer.git](https://github.com/sanjitmathur/Spotify-Song-Analyzer.git)
    cd Spotify-Song-Analyzer
    ```

2.  **Create a Spotify Developer App:**
    * Go to the **Spotify Developer Dashboard** and log in.
    * Click **"Create App"**. Give it any name (e.g., "Song Analyzer") and description.
    * Once created, find your **Client ID**. Click **"Show client secret"** to see your **Client Secret**. You will need both.
    * Click **"Edit Settings"**.
    * Find the **"Redirect URIs"** section. Add this exact URL:
        ```
        [http://127.0.0.1:8501](http://127.0.0.1:8501)
        ```
    * Click **"Add"** and then **"Save"** at the bottom of the form.

3.  **Set Environment Variables (.env):**
    * In the root of your project directory, create a file named **`.env`**.
    * Open the `.env` file and add your credentials:
        ```env
        CLIENT_ID="your-spotify-client-id"
        CLIENT_SECRET="your-spotify-client-secret"
        ```

4.  **Create and Activate Environment:**

    > **Important Conda/Anaconda Fix:** If your terminal prompt shows `(base)` or another name in parentheses, you are in a Conda environment. You **must** deactivate it before proceeding. Run:
    > ```bash
    > conda deactivate
    > ```
    > This ensures you use the correct Python environment.

    * **Create the virtual environment**:
        ```bash
        python -m venv .venv
        ```
    * **Activate the environment (Windows/PowerShell):**
        ```powershell
        Set-ExecutionPolicy RemoteSigned -Scope Process
        .\.venv\Scripts\Activate.ps1
        ```
    * **Activate the environment (macOS / Linux):**
        ```bash
        source .venv/bin/activate
        ```

5.  **Install Dependencies:**
    * With the environment active, install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

---

## Run the Application

Start the Streamlit web app from your activated virtual environment:

```bash
streamlit run main.py
