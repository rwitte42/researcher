# Research Assistant

## Description

The Research Assistant is a Python-based application designed to help users search for articles on various topics within a specified time range. The application utilizes multiple agents to handle different aspects of the research process, including parsing user input, conducting searches, and outputting results to a Markdown file.

## Features

- User-friendly interaction with a friendly AI-generated greeting.
- Ability to search for articles based on user-defined topics and time frames.
- Results are compiled and saved in a Markdown file for easy access and readability.
- Modular architecture using agents for better maintainability and scalability.

## Installation

To set up the project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/researcher.git
   cd researcher
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Follow the prompts**:
   - Enter the research topic you want to explore.
   - Specify the time frame for the search (e.g., '2 weeks', '3 months', or a number of days).
   - The application will display a confirmation message and await results.

3. **View the results**:
   - Once the research is complete, the results will be saved in a Markdown file located in the `research_results` directory.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thank you to the contributors and libraries that made this project possible.
- Special thanks to the OpenAI API for providing powerful language processing capabilities.
