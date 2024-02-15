import re
from collections import defaultdict

from rich.console import Console
from rich.table import Table

from loader import MSCDataLoader


def extract_questions(text):
    """
    Extracts questions from a given dialogue.

    :param dialogue: A string containing the dialogue.
    :return: A list of sentences from the dialogue that are questions.
    """
    # Split the dialogue into sentences using regular expressions to account for punctuation
    sentences = re.split(r"(?<=[.!?]) +", text)

    # Filter out sentences that end with a question mark
    questions = [sentence for sentence in sentences if sentence.endswith("?")]

    return questions


def analyze_dialogue_data(data):
    """
    Analyze dialogue data to extract insights such as number of turns,
    average turn length, personas information, and previous dialogues.

    :param data: List of dialogue instances.
    :return: Analysis results as a dictionary.
    """
    analysis_results = {
        "total_dialogues": len(data),
        "average_turns_per_dialogue": 0,
        "average_turn_length": 0,
        "average_personas_per_dialogue": 0,
        "average_previous_dialogues": 0,
    }

    total_turns = 0
    total_turn_length = 0
    total_personas = 0
    total_previous_dialogues = 0

    for dialogue in data:
        # Analyze dialogue turns
        turns = dialogue["dialog"]
        total_turns += len(turns)
        total_turn_length += sum(len(turn["text"]) for turn in turns)

        # Analyze personas
        personas = dialogue["personas"]
        total_personas += sum(len(persona) for persona in personas)

        # Analyze previous dialogues
        previous_dialogues = dialogue["previous_dialogs"]
        total_previous_dialogues += len(previous_dialogues)

    # Calculating averages
    if data:
        analysis_results["average_turns_per_dialogue"] = total_turns / len(data)
        analysis_results["average_turn_length"] = (
            total_turn_length / total_turns if total_turns else 0
        )
        analysis_results["average_personas_per_dialogue"] = total_personas / (
            2 * len(data)
        )  # Assuming 2 personas per dialogue
        analysis_results["average_previous_dialogues"] = total_previous_dialogues / len(
            data
        )

    return analysis_results


import random


def format_dialogue(dialogue):
    """
    Format and print a single dialogue session in a readable way.

    :param dialogue: A dialogue instance from the dataset.
    """
    # Print metadata
    print("\nMetadata:")
    for key, value in dialogue["metadata"].items():
        print(f"  {key}: {value}")

    # Print personas
    print("Personas:")
    for i, persona_list in enumerate(dialogue["personas"], start=1):
        print(f"  Persona {i}:")
        for persona in persona_list:
            print(f"    - {persona}")

    # Print dialogues
    print("\nDialogue:")

    speaker_questions = defaultdict(list)
    for turn in dialogue["dialog"]:
        speaker = turn["id"]
        speaker_questions[speaker].extend(extract_questions(turn["text"]))
        print(f"  {speaker}: {turn['text']}")

    # Print questions asked by each speaker
    print("\nQuestions Asked:")
    for speaker, questions in speaker_questions.items():
        print(f"  {speaker}:")
        if len(questions) == 0:
            print("    No questions asked.")
        for question in questions:
            print(f"    - {question}")

    # Optionally, print previous dialogues if needed
    # For brevity, not included here but can be added similarly to above sections


def format_dialogue_with_rich(dialogue):

    console = Console()

    # Print metadata
    metadata_table = Table(show_header=True, header_style="bold magenta")
    metadata_table.add_column("Key", style="bold")
    metadata_table.add_column("Value")
    for key, value in dialogue["metadata"].items():
        metadata_table.add_row(key, str(value))

    console.print("\nMetadata:", style="bold underline")
    console.print(metadata_table)

    # Print personas with rich
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Persona 1", style="dim", width=50)
    table.add_column("Persona 2", style="dim", width=50)

    max_len = max(len(dialogue["personas"][0]), len(dialogue["personas"][1]))
    for i in range(max_len):
        persona1 = (
            dialogue["personas"][0][i] if i < len(dialogue["personas"][0]) else ""
        )
        persona2 = (
            dialogue["personas"][1][i] if i < len(dialogue["personas"][1]) else ""
        )
        table.add_row(persona1, persona2)

    console.print("Personas:", style="bold underline")
    console.print(table)

    # Print initial personas
    # table = Table(show_header=True, header_style="bold magenta")
    # table.add_column("Initial Persona 1", style="dim", width=50)
    # table.add_column("Initial Persona 2", style="dim", width=50)

    # max_len = max(len(dialogue['init_personas'][0]), len(dialogue['init_personas'][1]))
    # for i in range(max_len):
    #     init_persona1 = dialogue['init_personas'][0][i] if i < len(dialogue['init_personas'][0]) else ""
    #     init_persona2 = dialogue['init_personas'][1][i] if i < len(dialogue['init_personas'][1]) else ""
    #     table.add_row(init_persona1, init_persona2)

    # console.print("\nInitial Personas:", style="bold underline")
    # console.print(table)

    # Print previous dialogues, if any
    # [ISSUE] Turn do not exist in previous dialogues
    # if dialogue['previous_dialogs']:
    #     console.print("\n[bold underline]Previous Dialogues[/bold underline]:")
    #     for i, prev_dialogue in enumerate(dialogue['previous_dialogs'], start=1):
    #         prev_dialogue_table = Table(show_header=True, header_style="bold magenta", title=f"Previous Dialogue {i}")
    #         prev_dialogue_table.add_column("Speaker", justify="right")
    #         prev_dialogue_table.add_column("Text", style="bold")
    #         for turn in prev_dialogue['dialog']:
    #             speaker = turn['id']
    #             prev_dialogue_table.add_row(speaker, turn['text'])
    #         time_info = f"{prev_dialogue['time_num']} {prev_dialogue['time_unit']} later"
    #         prev_dialogue_table.title += f" - {time_info}"
    #         console.print(prev_dialogue_table)

    # Print dialogues with rich
    dialogue_table = Table(show_header=True, header_style="bold magenta")
    dialogue_table.add_column("Speaker", justify="right")
    dialogue_table.add_column("Text", style="bold")

    for turn in dialogue["dialog"]:
        speaker = turn["id"]
        dialogue_table.add_row(speaker, turn["text"])

    console.print("\nDialogue:", style="bold underline")
    console.print(dialogue_table)


def inspect_random_dialogue(data):
    """
    Select and format a random dialogue session from the dataset.

    :param data: List of dialogue instances.
    """
    if not data:
        print("No data available.")
        return

    random_dialogue = random.choice(data)
    format_dialogue(random_dialogue)


# Example Usage
if __name__ == "__main__":
    loader = MSCDataLoader(
        "msc"
    )  # Replace 'msc' with the actual path to your MSC dataset
    loader.load_data()

    for i in range(2, 5):
        session_id = f"session_{i}"
        train_data_session = loader.get_data("msc_dialogue", session_id, "train")
        print(
            f"Loaded {len(train_data_session)} training data items for msc_dialogue {session_id}."
        )

        analysis_results = analyze_dialogue_data(train_data_session)
        print("Analysis Results:")
        for key, value in analysis_results.items():
            print(f"{key}: {value}")

        print("\nInspecting a randomly picked dialogue session:")
        for i in range(10):
            inspect_random_dialogue(train_data_session)
            print("\n")
