import os
import json

class MSCDataLoader:
    def __init__(self, dataset_path='msc'):
        self.dataset_path = dataset_path
        self.data = {
            'msc_dialogue': {},
            'msc_personasummary': {}
        }
    
    def load_data(self):
        for subdir, dirs, files in os.walk(self.dataset_path):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(subdir, file)
                    parts = subdir.split(os.sep)
                    if 'msc_dialogue' in parts or 'msc_personasummary' in parts:
                        # data_type: msc_dialogue or msc_personasummary
                        data_type = [part for part in parts if part in ['msc_dialogue', 'msc_personasummary']][0]
                        # session_name: session_1, session_2, etc.
                        session_name = parts[-1]
                        # file_type: train, test, or valid
                        file_type = file.split('.')[0]
                        
                        if data_type not in self.data or file_type not in ['train', 'test', 'valid']:
                            print(f"Unexpected data type or file_type: {data_type}, {file_type}")
                            continue
                        
                        if session_name not in self.data[data_type]:
                            self.data[data_type][session_name] = {
                                'train': [],
                                'test': [],
                                'valid': []
                            }
                        
                        with open(file_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                self.data[data_type][session_name][file_type].append(json.loads(line))

    def get_data(self, data_type, session_name, file_type):
        """
        Retrieve data for a specific type, session, and file type.
        
        :param data_type: 'msc_dialogue' or 'msc_personasummary'
        :param session_name: session name, e.g., 'session_2'
        :param file_type: 'train', 'test', or 'valid'
        :return: List of JSON objects
        """
        return self.data[data_type].get(session_name, {}).get(file_type, [])

# Example Usage
if __name__ == "__main__":
    loader = MSCDataLoader('msc')  # Replace 'path_to_msc_folder' with the actual path to your MSC dataset
    loader.load_data()
    
    # Example to get train data for msc_dialogue session 2
    train_data_session_2 = loader.get_data('msc_dialogue', 'session_2', 'train')
    print(f"Loaded {len(train_data_session_2)} training data items for msc_dialogue session 2.")
