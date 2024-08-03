# Alumni Management System

## Introduction

The Alumni Management System aims to tackle the challenges of alumni engagement and event participation. This system provides a platform for organizing and presenting alumni details, covering various categories like graduation year, current employment, skills, and residency.


![Image Alt](https://github.com/anishLS3/Alumni-And-Higher-Studies/blob/b1bd471dea3480b842f437f6aa4335d06e2717f3/Alumnator.png)

## Features

- **Alumni Profiles:** Organize and present alumni details including graduation year, current employment, skills, and residency.
- **Event Management:** Manage and track alumni engagement in various events.
- **Integration with LinkedIn:** Scrape data from LinkedIn to keep alumni information up-to-date.
- **Messaging Templates:** Use the Gemini API to create message templates for specific events and contact alumni via WhatsApp.

## Technologies Used

### Frontend
- **React**
- **Next.js**
- **Next UI**

### Backend
- **MongoDB**

### Data Scraping
- **Python Selenium**

## Setup

### Prerequisites
- Node.js
- MongoDB
- Python
- Selenium WebDriver

### Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/yourusername/alumni-management-system.git
    cd alumni-management-system
    ```

2. **Install frontend dependencies**
    ```sh
    cd client
    npm install
    ```

3. **Install backend dependencies**
    ```sh
    cd ../server
    npm install
    ```

4. **Setup MongoDB**
    - Ensure MongoDB is running locally or set up a MongoDB Atlas account.
    - Create a `.env` file in the `server` directory and add your MongoDB connection string:
      ```env
      MONGO_URI=your_mongodb_connection_string
      ```

5. **Setup Python Environment**
    ```sh
    cd ../data-scraper
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

### Running the Application

1. **Run the backend**
    ```sh
    cd server
    npm start
    ```

2. **Run the frontend**
    ```sh
    cd client
    npm run dev
    ```

3. **Run the data scraper**
    ```sh
    cd data-scraper
    python scraper.py
    ```

## Usage

- **Access the frontend:** Open `http://localhost:3000` in your web browser.
- **Backend API:** Accessible at `http://localhost:5000`.
- **Data Scraper:** Use the script to update alumni information from LinkedIn.

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.


