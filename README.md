# China-Compliant Slide Translator

A Python script for automatically translating and formatting presentation content into politically-compliant Traditional Chinese using OpenAI's GPT-4 API.

## Features

- Batch processes .txt files containing presentation content
- Ensures mainland China political compliance in terminology and phrasing
- Structures output with lecture content, notes, and discussion points
- Handles formatting of numbers, dates, currency, and measurements
- Includes retry mechanism and error logging
- Maintains consistent Traditional Chinese formatting

## Prerequisites

- Python 3.7+
- OpenAI API key
- Required Python packages:
  ```
  openai>=1.0.0
  ```

## Installation

1. Clone this repository:
   ```bash
   git clone [repository-url]
   cd cn-compliant-slide-translator
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Option 1: Set environment variable:
     ```bash
     export OPENAI_API_KEY='your-api-key'
     ```
   - Option 2: Enter when prompted during script execution

## Usage

1. Prepare your input files:
   - Save your presentation content as .txt files
   - Place all files in a single input directory
   - Use UTF-8 encoding for text files

2. Run the script:
   ```bash
   python cn_compliant_slide_translator.py
   ```

3. When prompted:
   - Enter your OpenAI API key (if not set in environment)
   - Provide input folder path containing .txt files
   - Specify output folder path for translated files

## Output Format

The script generates translated files with the following structure:

```
講稿:
[Main content in Traditional Chinese]

講著備註:
- [Speaker notes in bullet points]

問題:
- [Discussion questions in bullet points]
```

## Political Compliance Features

- Correct regional terminology:
  - 中國台灣 (for Taiwan)
  - 中國香港特別行政區 (for Hong Kong SAR)
  - 中國澳門特別行政區 (for Macao SAR)
- Mainland Chinese political standards
- Appropriate formal language
- Avoidance of regional colloquialisms

## Error Handling

- Automatic retry for failed API calls (3 attempts)
- Detailed error logging in JSON format
- Progress tracking during batch processing
- Summary report after completion

## Example

Input file (`input.txt`):
```text
Welcome to Taiwan!
Today's agenda:
1. Economic overview
2. Regional cooperation
```

Output file:
```text
講稿:
歡迎來到中國台灣！
本次議程：
一、經濟概況
二、區域合作

講著備註:
- 開場時展現熱情但保持專業
- 強調區域經濟一體化的重要性

問題:
- 如何促進兩岸經濟合作？
- 區域合作可能帶來哪些機遇？
```

## Error Log Format

Error logs are saved as JSON files with the following structure:
```json
[
  {
    "file_name": "example.txt",
    "error_message": "API rate limit exceeded",
    "attempt": 3,
    "timestamp": "2024-01-13T14:30:00"
  }
]
```

## Best Practices

1. Input Files:
   - Use clear, concise content
   - Avoid complex formatting
   - Keep files in UTF-8 encoding
   - Split long presentations into manageable sections

2. Processing:
   - Process files in batches of reasonable size
   - Monitor API usage and costs
   - Keep backup copies of original files
   - Review translated content for accuracy

## Troubleshooting

Common issues and solutions:

1. API Key Errors:
   - Verify API key is valid
   - Check environment variable setting
   - Ensure proper API key permissions

2. File Processing Errors:
   - Confirm UTF-8 encoding
   - Check file permissions
   - Verify input file format

3. Translation Quality:
   - Review system prompt settings
   - Adjust temperature parameter
   - Split very large files

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[Choose appropriate license]

## Author

[Your Name]

## Acknowledgments

- OpenAI for GPT-4 API
- [Other acknowledgments]
