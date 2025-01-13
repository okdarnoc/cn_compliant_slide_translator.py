# Standard library imports
import os
from pathlib import Path  # For cross-platform path handling
from datetime import datetime
import time
import json
from typing import Dict, List  # Type hints for better code documentation

# Third-party imports
from openai import OpenAI  # OpenAI API client

class ProcessingError:
    """
    Class to represent processing errors that occur during file translation.
    Used to track and log errors for later analysis.
    """
    def __init__(self, file_name: str, error_message: str, attempt: int):
        self.file_name = file_name        # Name of the file that caused the error
        self.error_message = error_message # Detailed error message
        self.attempt = attempt            # Which retry attempt failed
        self.timestamp = datetime.now().isoformat()  # When the error occurred

def process_single_file(
    client: OpenAI,
    txt_file: Path,
    output_folder: Path,
    max_retries: int = 3,    # Maximum number of retry attempts
    retry_delay: int = 5     # Delay between retries in seconds
) -> tuple[bool, str]:
    """
    Process a single text file by translating it to Traditional Chinese using GPT-4.
    Includes retry logic for handling temporary failures.
    
    Args:
        client: OpenAI API client instance
        txt_file: Path to the input text file
        output_folder: Path to the output directory
        max_retries: Maximum number of retry attempts (default: 3)
        retry_delay: Delay between retries in seconds (default: 5)
    
    Returns:
        tuple[bool, str]: (success status, error message if failed)
    """
    # Try processing the file up to max_retries times
    for attempt in range(max_retries):
        try:
            # Read the content of the input file with UTF-8 encoding
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Define the system prompt with detailed instructions for GPT-4
            # This prompt ensures consistent formatting and style in the output
            system_prompt = """
            Please rewrite the following content in Traditional Chinese using this format:

            講稿:
            [Content here]

            講著備註:
            - [Notes in bullet points]

            問題:
            - [Questions in bullet points]

            Important guidelines:
            1. Write in Traditional Chinese characters and avoid Cantonese-specific filler words or particles like "喇", "啦", "吓", etc.
            2. When refering to Taiwan, Macao or Hong Kong, use "中國台灣", "中國澳門特別行政區" and "中國香港特別行政區" respectively. Conform politically to chinese communist party lines.
            2. Maintain the original content's meaning
            3. Ensure content flows logically and remains coherent between slides. Avoid repetitive conversational openers or resets.
            4. Ensure 講稿 reads smoothly and professionally, resembling a lecture style rather than conversational.
            5. Transitions between ideas or points flow naturally, without generic or unnecessary lead-ins. Avoid using phrases like "各位朋友","大家好", ""各位同學", "今日", "我哋", etc. unless necessary.
            6. If the input is empty, provide a blank response. 
            7. If the input is a number, turn it into a Chinese character. For example, "100" should be "一百"."10000" should be "一萬".
            8. If the input is a date, turn it into a Chinese date format. For example, "2022-01-01" should be "二零二二年一月一日".
            9. If the input is a time, turn it into a Chinese time format. For example, "13:00" should be "下午一時".
            10. If the input is a currency, turn it into a Chinese currency format. For example, "$100" should be "一百港元".
            11. If the input is a percentage, turn it into a Chinese percentage format. For example, "50%" should be "百分之五十".
            12. If the input is a phone number, turn it into a Chinese phone number format. For example, "123-4567" should be "一二三四五六七".
            """
            
            # Make API call to GPT-4
            # Uses temperature=0.7 for some creativity while maintaining consistency
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": content}
                ],
                temperature=0.7
            )
            
            # Extract the translated content from the API response
            translated_content = response.choices[0].message.content
            
            # Create output file with the same name as input but in output folder
            output_file = output_folder / f"{txt_file.stem}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"Successfully processed: {txt_file.name}")
            return True, ""  # Return success with no error message
            
        except Exception as e:
            # Handle any errors that occur during processing
            error_msg = f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}"
            print(f"Error processing {txt_file.name}: {error_msg}")
            
            # If we haven't reached max retries, wait and try again
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                # If all retries failed, return failure status and error message
                return False, error_msg

def process_files(input_folder: str, output_folder: str, api_key: str) -> List[ProcessingError]:
    """
    Process all text files in the input folder and generate Chinese translations.
    
    Args:
        input_folder: Path to folder containing input text files
        output_folder: Path where translated files will be saved
        api_key: OpenAI API key for authentication
    
    Returns:
        List[ProcessingError]: List of files that failed processing after all retries
    """
    # Initialize OpenAI client with provided API key
    client = OpenAI(api_key=api_key)
    
    # Create output folder and any necessary parent directories
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get list of all .txt files in input folder
    input_path = Path(input_folder)
    txt_files = list(input_path.glob('*.txt'))
    
    # Check if there are any files to process
    if not txt_files:
        print(f"No .txt files found in {input_folder}")
        return []
    
    print(f"Found {len(txt_files)} .txt files to process")
    
    # Track processing errors for later reporting
    processing_errors: List[ProcessingError] = []
    
    # Process each file and collect any errors
    for txt_file in txt_files:
        print(f"\nProcessing: {txt_file.name}")
        success, error_msg = process_single_file(client, txt_file, output_path)
        
        if not success:
            # If processing failed, add to error list
            processing_errors.append(ProcessingError(
                file_name=txt_file.name,
                error_message=error_msg,
                attempt=3  # Max retries
            ))
        
        # Add delay between files to avoid rate limiting
        time.sleep(1)
    
    return processing_errors

def save_error_log(errors: List[ProcessingError], output_folder: str):
    """
    Save processing errors to a JSON file for later analysis.
    
    Args:
        errors: List of ProcessingError objects
        output_folder: Where to save the error log
    """
    if not errors:
        return  # Don't create log file if there are no errors
    
    # Create log filename with timestamp
    log_file = Path(output_folder) / f"error_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Convert error objects to dictionary format for JSON
    error_log = [{
        "file_name": error.file_name,
        "error_message": error.error_message,
        "attempt": error.attempt,
        "timestamp": error.timestamp
    } for error in errors]
    
    # Write errors to JSON file
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(error_log, f, indent=2, ensure_ascii=False)
    
    print(f"\nError log saved to: {log_file}")

def main():
    """
    Main entry point for the script.
    Handles user input, coordinates processing, and displays results.
    """
    # Get API key from environment variable or user input
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        api_key = input("Please enter your OpenAI API key: ").strip()
        if not api_key:
            print("API key is required")
            return
    
    # Get input/output folders from user
    input_folder = input("Enter the path to input folder: ").strip()
    output_folder = input("Enter the path to output folder: ").strip()
    
    # Validate input folder exists
    if not os.path.exists(input_folder):
        print("Input folder does not exist")
        return
    
    # Process all files and collect errors
    print("\nStarting processing...")
    processing_errors = process_files(input_folder, output_folder, api_key)
    
    # Display processing summary
    print("\nProcessing completed!")
    total_files = len(list(Path(input_folder).glob('*.txt')))
    failed_files = len(processing_errors)
    print(f"\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Successfully processed: {total_files - failed_files}")
    print(f"Failed files: {failed_files}")
    
    # If there were any failures, display details and save error log
    if processing_errors:
        print("\nThe following files failed after all retry attempts:")
        for error in processing_errors:
            print(f"- {error.file_name}: {error.error_message}")
        
        save_error_log(processing_errors, output_folder)

# Script entry point
if __name__ == "__main__":
    main()
