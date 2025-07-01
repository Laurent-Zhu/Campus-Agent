# Campus Agent Backend

## Overview
The Campus Agent Backend is a web application designed to facilitate the generation of exam papers using AI. It leverages the ZhipuAI API to generate text based on user-defined parameters and formats the output into downloadable PDF files.

## Project Structure
```
campus-agent-backend
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── utils
│   │   ├── model_client.py
│   │   └── pdf_utils.py
│   ├── routes
│   │   └── exam.py
│   └── templates
│       └── exam_template.html
├── requirements.txt
└── README.md
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd campus-agent-backend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Start the application:
   ```
   python app/main.py
   ```

2. Access the application in your web browser at `http://localhost:8000`.

3. Use the provided interface to select courses, knowledge points, and question types to generate exams.

4. After generating an exam, you can download the PDF file directly from the interface.

## API Endpoints
- **POST /api/v1/exams/generate**: Generates an exam based on the provided parameters.
- **GET /api/v1/exams/download/{exam_id}**: Downloads the generated exam PDF.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.