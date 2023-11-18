import re
import openai
import os
import sys
import time
import traceback

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def global_exception_handler(exctype, value, traceback):
    print("An exception occurred:")
    print("Exception type:", exctype)
    print("Exception value:", value)
    print("Traceback:")
    traceback.print_tb(traceback)

# Set the global exception handler
sys.excepthook = global_exception_handler

def read_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Read the API key from key.txt
openai.api_key = read_api_key('../key.txt')

def get_user_choice(options):
    while True:
        print("Chat GPT is a ________ author\nChoice:")
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        choice = input()
        if choice.isdigit() and int(choice) in range(1, len(options) + 1):
            return options[int(choice) - 1]
        else:
            print("Invalid choice. Please enter a valid option number.")

def get_gpt_response(messages, max_retries=5):
    retry_count = 0
    while retry_count <= max_retries:
        try:
            # Check the length of the message
            total_tokens = sum(len(message['content'].split()) for message in messages)
            if total_tokens > 4000:
                # Reduce the message length by removing characters from the end
                while total_tokens > 4000:
                    messages[-1]['content'] = messages[-1]['content'][:-1]
                    total_tokens -= 1

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=3000,
                n=1,
                stop=None,
                temperature=0.5,
            )
            return response.choices[0].message['content']
        except openai.error.RateLimitError:
            retry_count += 1
            if retry_count <= max_retries:
                print(f"Rate limit error, retrying ({retry_count}/{max_retries})...")
                continue
            else:
                raise

def write_file(file_name, content, mode='w'):
    with open(file_name, mode) as file:
        file.write(content)

def create_message(role, content):
    return {"role": role, "content": content}

def generate_questions(author_type, user_input, user_content):
    return [
        create_message("system", f"You are an {author_type} author writing a book about {user_input}"),
        create_message("user", user_content)
    ]

# Set User Input:
valid_options = ["fiction", "non-fiction", "sci-fi", "children's book", "teen fantasy", "educational", "scientific", "romance", "mystery", "biography", "historical fiction", "self-help", "horror", "poetry", "adventure", "dungeons and dragons"]
chatGPT_author_type = get_user_choice(valid_options)
clear_screen()
user_input = input(f"Chat GPT is a {chatGPT_author_type} author writing a book about: ")
clear_screen()
print(f"Chat GPT is a {chatGPT_author_type} author writing a book about {user_input}")

# Initial Question:
print("Creating your chapter list now...")
initial_question = generate_questions(chatGPT_author_type, user_input, "Write the chapter index and the details to be covered in each chapter. Each Chapter must contain a sub menu.")
response = get_gpt_response(initial_question)
print("Chapter list created...")

#Fixing/Expanding The Initial Question: (Commented out due to issues in response adding chapters and not including initial chapters)
#second_question = generate_questions(chatGPT_author_type, user_input, f"Here is your chapter list, it seems it is not as indepth as it should be. Make sure the list has ALL tools if educational not just a few for each chapter. Start at Chapter 1. \n{response}")
#response = get_gpt_response(second_question)
#print(response)

# Extracting The Chapters:
pattern = r'Chapter \d+[.: -].*?(?=Chapter \d+[.: -]|\Z)'
chapters = re.findall(pattern, response, re.MULTILINE | re.DOTALL)

write_file('Chapters.md', response, 'w')  # 'w' mode will overwrite the existing file

# Fact based functionality.
if chatGPT_author_type in ["non-fiction", "educational", "scientific", "self-help"]:
    for chapter_number, chapter in enumerate(chapters, start=1):
        chapter_responses = get_gpt_response(generate_questions(chatGPT_author_type, user_input, f"The current chapter you are writing: {chapter}"))
        chapter_file_name = f"Chapter{chapter_number}.md"
        write_file(chapter_file_name, chapter_responses)
        print(f"Writing: Chapter {chapter_number}")
        lines = chapter_responses.split("\n")
        for line in lines:
            if line.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
                split_result = re.split(r'\.\s', line, maxsplit=1)
                if len(split_result) == 2:
                    explain_info = f"You should give in-depth examples, use multiple examples for each to help with understanding:\n ```{line}```"
                    print(f"Getting more context for any numbered lists for Chapter {chapter_number}")
                    explanation = get_gpt_response(generate_questions(chatGPT_author_type, user_input, explain_info))
                    write_file(chapter_file_name, explanation, mode='a')
                else:
                    print(f"Invalid line format: {line}")

# Story based functionality.
if chatGPT_author_type in ["fiction", "sci-fi", "teen fantasy", "romance", "mystery", "historical fiction", "horror", "adventure"]:
    story_continuation = ""
    story_continuation_deduped = ""
    # Generate Characters and Defining traits
    print(f"Generating Characters for your story.")
    character_response = get_gpt_response(generate_questions(chatGPT_author_type, user_input, f"You need to create a list of characters for the story and some defining traits. Make sure to give them names and descriptions\n {chapters}"))
    character_sheets = f"Character_Sheets.md"
    if character_response:
        write_file(character_response)
    for chapter_number, chapter in enumerate(chapters, start=1):
        # Generate the first chapter
        print(f"Generating Chapter {chapter_number}")
        chapter_responses = get_gpt_response(generate_questions(chatGPT_author_type, user_input, f"List of all Chapters: ```{chapters}```\n\nThe current chapter you are writing: {chapter}\n Characters in the story: {character_response}\n Key information for the story so far:\n{story_continuation_deduped}"))
        # Extract key information from the current chapter for future chapters:
        print(f"Extracting Key Information From Chapter {chapter_number}")
        story_continuation += get_gpt_response(generate_questions(chatGPT_author_type, user_input, f"Extract only the key information from this such as names, places, important details such as relationships between characters: {chapter_responses}"))
        story_continuation_deduped = get_gpt_response(generate_questions(chatGPT_author_type, user_input, f"Clean up these keynotes: ```{story_continuation}```"))
        chapter_file_name = f"Chapter{chapter_number}.md"
        write_file(chapter_file_name, chapter_responses)
        notes_taken = f"Notes_Taken.md"
        if notes_taken:
            write_file(notes_taken, story_continuation_deduped)

# Dungeons and Dragons functionality.
if chatGPT_author_type in ["dungeons and dragons"]:
    character_sheets = f"Character_Sheets.md"
    if character_sheets:
        write_file(character_response)
    story_continuation = ""
    story_continuation_deduped = ""
    # Generate Characters and Defining traits
    print(f"Generating Characters for your story.")
    character_response = get_gpt_response(generate_questions(chatGPT_author_type, user_input, f"You need to create a list of characters and their stats in short form as well as personalities.\n {chapters}"))
    for chapter_number, chapter in enumerate(chapters, start=1):
        # Generate the first chapter
        print(f"Generating Chapter {chapter_number}")
        chapter_responses = get_gpt_response(generate_questions(chatGPT_author_type, user_input, f"List of all Chapters: ```{chapters}```\n\nThe current chapter you are writing: ```{chapter}```\n Characters in the story: ```{character_response}```\n Key information for the story so far:\n```{story_continuation_deduped}```\nMust be multiple choice for actions and outcomes taken within the story"))
        # Extract key information from the current chapter for future chapters:
        print(f"Extracting Key Information From Chapter {chapter_number}")
        story_continuation += get_gpt_response(generate_questions(chatGPT_author_type, user_input, f"Extract only the key information from this such as names, places, important details such as relationships between characters: {chapter_responses}"))
        story_continuation_deduped = get_gpt_response(generate_questions(chatGPT_author_type, user_input, f"Clean up these keynotes: ```{story_continuation}```"))
        chapter_file_name = f"Chapter{chapter_number}.md"
        write_file(chapter_file_name, chapter_responses)
        notes_taken = f"Notes_Taken.md"
        if notes_taken:
            write_file(notes_taken, story_continuation_deduped)

if chatGPT_author_type in ["fantasy", "children's book", "biography", "poetry"]:
    print(f"Not included currently: {chatGPT_author_type}")
    # For Childrens Book, I would like to have ChatGPT give areas and descriptions for where an image might be for the book.
