# Math Agent with Interactive Mode

This project is a simple AI agent that utilizes Google's Gemini API to solve mathematical equations. The agent can process both text-based mathematical expressions (e.g., `a = 2`) and image inputs containing handwritten or printed equations. It maintains a dictionary of variables and evaluates expressions dynamically.

## Features

- **Text Input**: Solve equations like `a = 2` or `x + y = 10`.
- **Image Input**: Upload images of handwritten or digital equations (e.g., `equation.jpg`).
- **Interactive Mode**: Continuously interact with the agent until you type `exit`.
- **Variable Storage**: Stores variables in a dictionary for use in future calculations.

## Prerequisites

1. **Python 3.8+**: Ensure Python is installed on your system.
2. **Gemini API Key**: Obtain an API key from [Google AI Studio](https://makersuite.google.com/).
3. **Tesseract OCR (optional)**: Install Tesseract for better image processing:
   - **Windows**: [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - **Mac**: `brew install tesseract`
   - **Linux**: `sudo apt install tesseract-ocr`

## Installation

1. Clone the repository or download the `math_agent.py` file.
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Replace `your_google_api_key` in `math_agent.py` with your actual Gemini API key.

## Usage

### Running the Script

1. Open a terminal and navigate to the project directory.
2. Run the script:
   ```bash
   python math_agent.py
   ```
3. The interactive mode will start, allowing you to:
   - Enter equations directly (e.g., `a = 2`).
   - Provide the path to an image file (e.g., `equation.jpg`).
   - Type `exit` to quit the program.

### Example Interaction
```
Enter equation or image path: a = 2
Current variables: {'a': 2.0}

Enter equation or image path: b = 3
Current variables: {'a': 2.0, 'b': 3.0}

Enter equation or image path: equation.jpg
Current variables: {'a': 2.0, 'b': 3.0, 'c': 5.0}

Enter equation or image path: exit
```

## File Structure

- `math_agent.py`: Main script containing the Math Agent logic.
- `requirements.txt`: List of dependencies.
- `README.md`: This file.
- `equation.jpg`: Example image file for testing (optional).

## Customization

### Enhancing Features

1. **Save/Load Variables**: Implement saving and loading of stored variables.
2. **Improved Error Handling**: Add validation for incorrect inputs or API failures.
3. **Advanced Math Operations**: Extend support for calculus, trigonometry, and matrix operations.

## Troubleshooting

1. **API Key Issues**:
   - Ensure the API key is valid and has the necessary permissions.
   - Verify internet connectivity.

2. **Image Processing Errors**:
   - Check that the image file path is correct.
   - Use high-quality images for improved OCR accuracy.

3. **Gemini API Errors**:
   - Review the API response for error messages.
   - Modify input formats or prompts if needed.

## License

This project is open-source and available under the **MIT License**.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

Enjoy using the Math Agent! 🚀

