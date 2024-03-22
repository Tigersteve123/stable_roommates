from stable_roommates import StableRoommates

class PreferenceConverter:
    def __init__(self):
        self.name_to_index = {}
        self.index_to_name = {}

    def add_individual(self, name):
        index = len(self.name_to_index)
        self.name_to_index[name] = index
        self.index_to_name[index] = name

    def convert_preferences_to_indices(self, preferences):
        indexed_preferences = []
        for preference_list in preferences:
            indexed_preference = [self.name_to_index[name] for name in preference_list]
            indexed_preferences.append(indexed_preference)
        indexed_preferences.sort(key=lambda x: self.get_missing_index(x))
        return indexed_preferences, self.index_to_name

    def convert_indices_to_preferences(self, indexed_preferences):
        preferences = []
        for indexed_preference in indexed_preferences:
            preference_list = [self.index_to_name[index] for index in indexed_preference]
            preferences.append(preference_list)
        return preferences, self.index_to_name

    def get_missing_index(self, preference_list):
        for i, index in enumerate(preference_list):
            if index != i:
                return i
        return len(preference_list)

def convert_to_names(match_lst, names_dict):
    return [(names_dict[match[0]], names_dict[match[1]]) for match in match_lst]

# Example usage:
preferences_names = [['Dan', 'Bob', 'Charlie'], ['Dan', 'Alice', 'Charlie'], ['Dan', 'Alice', 'Bob'], ['Alice', 'Bob', 'Charlie']]
converter = PreferenceConverter()

# Add individuals to the converter
for preference_list in preferences_names:
    for name in preference_list:
        if name not in converter.name_to_index:
            converter.add_individual(name)

indexed_preferences, index_to_name = converter.convert_preferences_to_indices(preferences_names)
print("Preferences:", {index_to_name[i]:[index_to_name[x] for x in indexed_preferences[i]] for i in range(len(indexed_preferences))})
# print("Index to name mapping:", index_to_name)

# You can now use indexed_preferences with the StableRoommates class

sr = StableRoommates(indexed_preferences)
print(convert_to_names(sr.match_roommates(), index_to_name))
