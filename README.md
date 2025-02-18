# Math Agent Web UI

This project is a simple AI-powered Math Agent that processes mathematical expressions from text or images using Google's Gemini API. It provides a FastAPI backend with a web UI for interactive use.

## Features

- **Process Text Equations:** Input mathematical expressions in text form.
- **Process Image Equations:** Upload images containing handwritten or digital equations.
- **View Stored Variables:** Displays all computed variables dynamically.
- **Simple Web Interface:** Interact using a web-based UI.

## Prerequisites

1. **Python 3.8+**
2. **Google Gemini API Key** (Get from [Google AI Studio](https://makersuite.google.com/))
3. **Required Libraries** (Installed via `pip`)

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/math-agent.git
   cd math-agent
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the project root:
     ```sh
     GOOGLE_API_KEY=your_google_api_key_here
     ```
   - Or set it manually:
     ```sh
     export GOOGLE_API_KEY="your_google_api_key_here"  # Linux/macOS
     set GOOGLE_API_KEY=your_google_api_key_here       # Windows CMD
     ```

## Running the Application

Start the FastAPI server:
```sh
uvicorn main:app --reload
```

Open a browser and navigate to:
```sh
http://127.0.0.1:8000/
```

## API Endpoints

### `GET /`
Returns the web UI.

### `POST /compute`
**Description:** Computes mathematical expressions from text.
**Request:**
```json
{
  "expression": "a = 2"
}
```
**Response:**
```json
{
  "status": "success",
  "variables": {"a": 2.0}
}
```

### `POST /compute-image`
**Description:** Computes mathematical expressions from an uploaded image.
**Request:** Upload an image file (`.jpg`, `.png`).
**Response:**
```json
{
  "status": "success",
  "variables": {"a": 2.0, "b": 3.0}
}
```

### `GET /variables`
**Description:** Returns all stored variables.
**Response:**
```json
{
  "variables": {"a": 2.0, "b": 3.0}
}
```

## Troubleshooting

1. **API Key Not Found:** Ensure the API key is correctly set in the `.env` file.
2. **Image Not Processing:** Ensure the image is clear and in a supported format.
3. **Server Not Running:** Verify FastAPI is installed and try restarting the server.

## Future Enhancements

- Store and retrieve past computations.
- Support for more complex mathematical operations.
- Improved OCR for image-based equations.

## License

MIT License. Free to use and modify.

---

### Author
Developed by Abel 🚀

