# 📊 YouTube Trending Videos ETL Pipeline

## 📝 Description

This project is a basic ETL (Extract, Transform, Load) pipeline designed to demonstrate core Data Engineering skills. It fetches trending video data from the YouTube Data API v3, cleans and transforms the data using Python (Pandas), and loads it into a PostgreSQL database running locally via Docker.

This serves as a foundational portfolio project showcasing the ability to:
*   🔄 Interact with external APIs.
*   🧹 Process and clean JSON data.
*   🔄 Perform data type conversions and basic transformations using Pandas.
*   💾 Load structured data into a relational database.
*   🐳 Utilize Docker for managing local development services.

## ✨ Features

*   **Extract:** 📡 Fetches the top 50 trending videos for a specified region (default: US) using the YouTube Data API v3.
*   **Transform:** 🔧
    *   Parses the JSON response from the API.
    *   Selects relevant fields (video ID, title, published date, channel info, statistics).
    *   Cleans data and converts view counts, like counts, and comment counts to nullable integer types using Pandas.
    *   Converts publish dates to datetime objects.
*   **Load:** 📥 Loads the cleaned, transformed data into a PostgreSQL table (`trending_videos`), replacing the table on each run.
*   **Configuration:** ⚙️ Uses a `.env` file to securely manage the YouTube API key.
*   **Environment:** 🐳 Utilizes Docker to run the PostgreSQL database locally.

## 🛠️ Tech Stack

*   **Language:** 🐍 Python 3.x
*   **Libraries:** 📚
    *   `requests` (for API calls)
    *   `pandas` (for data transformation)
    *   `SQLAlchemy` (for database interaction abstraction)
    *   `psycopg2-binary` (PostgreSQL adapter for Python)
    *   `python-dotenv` (for environment variables)
*   **Database:** 🗃️ PostgreSQL (running in Docker)
*   **Tools:** 🐳 Docker Desktop

## 🔄 Workflow

1.  Load YouTube API Key from `.env` file.
2.  Call YouTube Data API v3.
3.  Receive JSON response containing trending video data.
4.  Parse JSON and transform data into a Pandas DataFrame, cleaning and converting data types.
5.  Establish connection to the PostgreSQL database running in Docker via SQLAlchemy.
6.  Load the Pandas DataFrame into the `trending_videos` table in PostgreSQL 

## 🚀 Setup and Usage

### Prerequisites

*   🐍 Python 3.8+ installed
*   🐳 Docker Desktop installed and running
*   ☁️ A Google Cloud Platform project with the YouTube Data API v3 enabled
*   🔑 A YouTube Data API v3 Key

### Installation & Configuration

1.  **Clone the repository:** 📥
    ```bash
    git clone [Your GitHub Repository URL]
    cd youtube-pipeline
    ```

2.  **Create and activate a virtual environment:** 🔒
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:** 📦
    
    pip install -r requirements.txt
    
    

4.  **Set up environment variables:** ⚙️
    *   Create a file named `.env` in the project root directory (`youtube_pipeline/.env`).
    *   Add your YouTube API key to the `.env` file:
        ```
        YOUTUBE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
        ```
    *   **IMPORTANT:** Ensure `.env` is listed in your `.gitignore` file to avoid committing your secret key!

5.  **Start the PostgreSQL Docker container:** 🐳
    *   Open a separate terminal window.
    *   Run the following command :
        ```bash
        docker run --name youtube-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=youtubedb -p 5433:5432 -d postgres:14
        ```
        

### Running the Pipeline

1.  Make sure your virtual environment is activated and the Docker container is running.
2.  Execute the Python script from the project root directory: ▶️
    ```bash
    python pipeline.py
    ```

### Verifying the Output

1.  ✅ Check the console output for success messages ("API call successful", "Data transformation successful", "Data Successfully loaded into DB", "Pipeline completed.").
2.  📄 A `transformed_videos.csv` file will be created/updated in the project directory with the cleaned data.
3.  🔍 Connect to the PostgreSQL database using a GUI tool (like DBeaver, pgAdmin) or `psql` via `docker exec`:
    *   **Connection Details:**
        *   Host: `localhost`
        *   Port: `5433`
        *   Database: `youtubedb`
        *   User: `user`
        *   Password: `password`
    *   **Check Table:** Look for the `trending_videos` table in the `public` schema.
    *   **Query Data:** Run `SELECT * FROM trending_videos LIMIT 10;` to view the loaded data.

## 📁 Project Structure
```
youtube-pipeline/
├── .env # Stores API key
├── .gitignore 
├── pipeline.py # Main Python script for the ETL pipeline
├── requirements.txt # Python dependencies
└── README.md 
```

## 📬 Contact

*   **Name:** Ramesh Manthirakumar
*   **LinkedIn:** linkedin.com/in/ramesh-manthirakumar-a49191199
*   **GitHub:**  https://github.com/rameshmkumar