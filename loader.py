import json
import os


class MSCDataLoader:
    def __init__(self, dataset_path="msc"):
        self.dataset_path = dataset_path
        self.data = {"msc_dialogue": {}, "msc_personasummary": {}}

    def load_data(self):
        for subdir, dirs, files in os.walk(self.dataset_path):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(subdir, file)
                    parts = subdir.split(os.sep)
                    if "msc_dialogue" in parts or "msc_personasummary" in parts:
                        # data_type: msc_dialogue or msc_personasummary
                        data_type = [
                            part
                            for part in parts
                            if part in ["msc_dialogue", "msc_personasummary"]
                        ][0]
                        # session_name: session_1, session_2, etc.
                        session_name = parts[-1]
                        # file_type: train, test, or valid
                        file_type = file.split(".")[0]

                        if data_type not in self.data or file_type not in [
                            "train",
                            "test",
                            "valid",
                        ]:
                            print(
                                f"Unexpected data type or file_type: {data_type}, {file_type}"
                            )
                            continue

                        if session_name not in self.data[data_type]:
                            self.data[data_type][session_name] = {
                                "train": [],
                                "test": [],
                                "valid": [],
                            }

                        with open(file_path, "r", encoding="utf-8") as f:
                            for line in f:
                                self.data[data_type][session_name][file_type].append(
                                    json.loads(line)
                                )

    def get_data(self, data_type, session_name, file_type):
        """
        Retrieve data for a specific type, session, and file type.

        :param data_type: 'msc_dialogue' or 'msc_personasummary'
        :param session_name: session name, e.g., 'session_2'
        :param file_type: 'train', 'test', or 'valid'
        :return: List of JSON objects
        """
        return self.data[data_type].get(session_name, {}).get(file_type, [])


def _inspect_structure(instance, depth=1, current_level=0):
    """
    Recursively inspects the structure of the given instance up to a specified depth.

    :param instance: The data instance to inspect.
    :param depth: Maximum depth to explore.
    :param current_level: Current level of depth.
    """
    indent = "  " * current_level  # Indentation for better readability

    if isinstance(instance, dict):
        print(f"{indent}Level {current_level} (Dict): Keys - {list(instance.keys())}")
        if current_level < depth:
            for key, value in instance.items():
                print(f"{indent}Inspecting key: {key}")
                _inspect_structure(value, depth, current_level + 1)
    elif isinstance(instance, list):
        print(f"{indent}Level {current_level} (List): Length - {len(instance)}")
        if current_level < depth and instance:
            print(f"{indent}Inspecting first item of the list...")
            _inspect_structure(instance[0], depth, current_level + 1)
    else:
        print(f"{indent}Level {current_level}: Type - {type(instance)}")


# Example Usage
if __name__ == "__main__":
    loader = MSCDataLoader(
        "msc"
    )  # Replace 'msc' with the actual path to your MSC dataset
    loader.load_data()

    # Example to get train data for msc_dialogue session 2
    train_data_session_2 = loader.get_data("msc_dialogue", "session_2", "train")
    print(
        f"Loaded {len(train_data_session_2)} training data items for msc_dialogue session 2."
    )

    if train_data_session_2:
        print("Inspecting first instance with deeper structure:")
        _inspect_structure(
            train_data_session_2[0], depth=2
        )  # Adjust the depth as needed
    else:
        print("No data found for msc_dialogue session 2 train.")
