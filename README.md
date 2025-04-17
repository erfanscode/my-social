# My-Social

A feature-rich social media platform built with Django that enables users to connect, share posts, follow others, and interact with content.

## Features

- **User Authentication**: Custom user model with registration, login, and profile management
- **Posts**: Create, view, like, and save posts
- **Social Interactions**: Follow/unfollow users, view followers and following
- **Content Discovery**: Search posts by tags or content, view trending posts
- **Responsive Design**: Modern UI that works across devices

## Technologies Used

- Django 5.1
- Django Taggit for tag management
- Easy Thumbnails for image processing
- Pillow for image handling
- SQLite database (can be configured for other databases)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/My-Social.git
cd My-Social
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create .env file
```bash
cp .env-exapmle .env
```

5. Edit the .env file with your settings
```
SECRET_KEY=your_secret_key
DEBUG=True
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

6. Apply migrations
```bash
python manage.py migrate
```

7. Create a superuser
```bash
python manage.py createsuperuser
```

8. Run the development server
```bash
python manage.py runserver
```

## Project Structure

- `social/`: Main app with all social functionality
  - Models for users, posts, and relationships
  - Views for post handling, user interactions
  - Templates for rendering pages
- `base/`: Project settings and configuration
- `media/`: User uploaded content
- `static/`: CSS, JavaScript, and images

## Usage

- Sign up for an account
- Edit your profile with personal information
- Create posts with content and tags
- Like and save posts from other users
- Follow other users to see their content
- Use the search functionality to find content
