# Document-Understanding AI Assistant

## Overview
This application leverages advanced AI to understand and answer questions based on PDF or CSV files. It utilizes LangChain, ChromaDB, and OpenAI's models.

## Features
- Custom file handling command for PDF/CSV files.
- Django Rest API Backend with a frontend application.
- Integration with LangChain and OpenAI's models.
- ChromaDB for embedding data storage and retrieval.
- LangChain for conversational and user feedback mechanism

## Running the Application
### Backend (Port 8000)
1. Navigate to the backend directory.
2. Run `python manage.py runserver 8000` to start the Django server on port 8000.

### Frontend (Port 8001)
1. Navigate to the frontend directory.
2. Open new terminal and start a separate (frontend) server on `python manage.py runserver 8001`
3. Alternatively, you may run live server from VS Code on the templates/index.html

### File Handling
Use `python manage.py file_handler <filename>` to upload and process files.

## API Interaction
The application is secured with authentication and uses Django's REST framework.

## Frontend Application
A web-based UI for user interaction, featuring a loading bar for processing.

## Contributing
Contributions are welcome. Please fork the repository and submit pull requests.

## License
Apache
