import json
import os

class Save:

    def __init__(self):
        pass

    def save_campaign(self, campaign):

        saves_path = "./docs/save_data"
        files = os.listdir(saves_path)

        if len(files) == 0:
            campaign.set_id("000")
        else:
            files.sort()
            last_file = files[-1]
            last_id = int(last_file.split(".")[0])
            new_id = last_id + 1
            campaign.set_id(str(new_id).zfill(3))

        file_path = f"{saves_path}/{campaign.get_id()}.json"

        campaign_dict = campaign.toJson()

        with open(file_path, 'w') as f:
            json.dump(campaign_dict, f, indent=4)

    def delete_campaign(self, campaign_name):

        campaign = self.get_campaign(campaign_name)
        campaign_id = campaign["id"]

        file_path = f"./docs/save_data/{campaign_id}.json"
        os.remove(file_path)

    def get_campaign(self, campaign_name):

        saves = os.listdir("./docs/save_data")

        for save in saves:
            with open(f"./docs/save_data/{save}", "r") as f:
                campaign = json.load(f)
                if campaign["name"] == campaign_name:
                    return campaign