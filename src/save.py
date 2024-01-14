import json
import os
import base64

class SaveFile:
    """
    Creates or updates a file.

    Attributes:
    - _username (str): stores the user's name.
    - _filename (str): generates a file name based on username.
    - _path (str): file path where the file is stored.

    Methods:
    - save(website, data): Handles the file creation and file updates.
    - load(): Loads the user's data.
    - remove(website, delete): Removes a data entry in the json file
    """
    
    CONFIG_FILE_NAME = "user_config.json"

    def __init__(self, user: str ="Default"):
            self._username = user
            self._filename = f"{user}.json"
            self._config_path = os.path.join(os.path.expanduser("~"), self.CONFIG_FILE_NAME)
            self._path = f"C:\\Users\\Andrei\\Desktop\\VScode\\Users\\{self._filename}"

    def get_path(self) -> str:
        user_config = self.load_user_config()
        for user in user_config["Users"]:
            if user["Username"] == self._username:
                return user["Path"]

    def save(self, key: str, data: dict) -> None:
        """
        Handles the file creation and file updates.

        Parameters:
        - key (str): Key name
        - data (dict): User's data

        Returns:
        - None
        """
        try:
            with open(self._path, "r") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
                existing_data = {self._username: {key: []}}
        if key not in existing_data[self._username]:
            existing_data[self._username][key] = []
        existing_data[self._username][key].append(data)
        with open(self._path, "w") as file:
            json.dump(existing_data, file, indent=2)
                                            
    def load(self) -> dict:
        """
        Loads the JSON file.

        Parameters:
        - None

        Returns:
        JSON data
        """
        try:
            self._path = self.get_path()
            with open(self._path, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return False

    def remove(self, website: str, delete: int) -> None:
        """
        Deletes an entry from the JSON file.

        Parameters:
        - website (str): Website name
        - delete (int): dictionary pair to be removed

        Returns:
        - None
        """
        try:
            with open(self._path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError

        del data[self._username][website][delete]
        with open(self._path, "w") as file:
            json.dump(data, file, indent=2)
        return 

    def edit(self, website: str, index: int, replace: dict) -> None:
        """
        Edit entries in the file.
        """
        try: 
            with open(self._path, "r"):
                data = json.load()
        except FileNotFoundError:
            raise FileNotFoundError
        
        data[self._username][website][index]["Username"] = replace.get("Username", None)
        data[self._username][website][index]["Password"] = replace.get("Password", None)

    
        
    def new_user(self, user_path: str ="Default") -> None:
        """
        Initialize a new user and saves the user's prefered path.

        Parameters:
        - user_path - user's prefered path
        """
        salt = os.urandom(16)
        str_salt = base64.b64encode(salt).decode('utf-8')
        self._path = os.path.join(user_path, self._filename)
        
        self.create_config_file(user_path)  
        self.save("User_info", {"Salt": str_salt}) 

    def load_user_config(self) -> None:
        """
        Load the user's configuration.
        """
        try:
            with open(self._config_path, "r") as file:
                user_config = json.load(file)

            return user_config
        except FileNotFoundError:
            self.new_user()

    def save_user_config(self, user_path: str =None) -> None:
        """
        Saves the user's configuration.
        """
        if not user_path:
            user_path = os.path.expanduser("~")
        user_config = self.load_user_config()
        if self._username in user_config:
            user_config["Users"][self._username] = user_path
        else:
            user_config["Users"].append({"Username": self._username ,"Path": user_path})
        with open(self._config_path, "w") as file:
            json.dump(user_config, file, indent=2)
        
    def create_config_file(self, user_path=None) -> None:
        """
        Create a file to save each user's prefered file path.
        """
        if os.path.exists(self._config_path):
            self.save_user_config(os.path.join(user_path, self._filename))
        else:
            username = self._username
            with open(self._config_path, "w") as file:
                default_config = {"Users": []}
                if user_path:
                    default_config["Users"].append({"Username": "Username", "Path": "Path"})
                json.dump(default_config, file, indent=2)

        


    