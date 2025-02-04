
#  🛒 E-Auction System for Personalized Bidding 🛒

## 📋 Project Overview
The **E-Auction System for Personalized Bidding** is an innovative online auction platform designed to enhance user experiences through AI-driven personalized recommendations and real-time bidding. Leveraging **collaborative filtering** with **cosine similarity**, it offers tailored product suggestions based on user preferences and past interactions. The system integrates an **AI-powered chatbot** using Hugging Face transformers for seamless user support.

## 🚀 Features
- **Personalized Recommendations:** Utilizes cosine similarity to suggest items aligned with user interests based on bid history and watchlists.
- **AI Chatbot Assistance:** Provides real-time, AI-driven support for product-related queries and auction guidelines.
- **Real-time Bidding:** Instantaneous bid placement and updates for a dynamic auction experience.
- **Admin Control Panel:** Secure backend for managing auctions, setting bid limits, and closing auctions.
- **Watchlist Functionality:** Track favorite items with real-time status updates and notifications.
- **Secure User Authentication:** Ensures data privacy and secure transactions.

## 🏗️ System Architecture
The platform consists of two main components:
1. **User Interface:** Allows users to browse, bid, and interact with personalized recommendations.
2. **Admin Dashboard:** Enables auction management, including bid monitoring, auction settings, and closing.

The system is built using the **Django framework** with a secure database to store user data, bid history, and auction details.

## 🧠 Technology Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite / MySQL
- **AI & ML:** Cosine Similarity (scikit-learn), Collaborative Filtering
- **Chatbot:** Hugging Face Transformers
- **Version Control:** Git & GitHub

## ⚙️ Installation & Setup

1. **Clone the Repository:**
```bash
git clone https://github.com/Pseudo-Sid26/E-Auction-System-for-Personalized-Bidding.git
cd E-Auction-System-for-Personalized-Bidding
```

2. **Create a Virtual Environment:**
```bash
# For Linux/Mac
python -m venv env
source env/bin/activate

# For Windows
python -m venv env
env\Scripts\activate
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run Migrations:**
```bash
python manage.py migrate
```

5. **Start the Development Server:**
```bash
python manage.py runserver
```

6. **Access the Application:**
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## 🔑 Usage
- **Register/Login:** Create an account or log in to access auction features.
- **Browse Auctions:** Explore active auctions tailored to your interests.
- **Place Bids:** Participate in real-time bidding with instant updates.
- **Watchlist:** Add items to your watchlist for quick access and updates.
- **Chatbot Assistance:** Use the chatbot for instant support.

## 📊 Recommendation Engine
- **Collaborative Filtering:** Analyzes user behavior to identify patterns and preferences.
- **Cosine Similarity:** Measures the similarity between user interests and auction items to deliver relevant recommendations.

## 🔐 Admin Features
- Manage users and auctions.
- Set and modify bid limits.
- Close auctions and announce winners.
- Monitor real-time auction activity.

## 🗂️ Folder Structure
```
E-Auction-System-for-Personalized-Bidding/
├── e_auction/             # Django project files
├── auctions/              # Core auction app
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 🔮 Future Enhancements
- Integration with **blockchain** for secure, transparent transactions.
- **Mobile app** development for greater accessibility.
- Advanced **fraud detection** using anomaly detection algorithms.
- Multilingual support for the **AI chatbot**.

## 🤝 Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your fork:
   ```bash
   git push origin feature-branch
   ```
5. Open a Pull Request.




