import json
class UI_data(object):
    width = 0
    height = 0
    fps = 0
    path = ""
    class_name = ""
    num_frames = 0
    length_minute = 0
    length_second = 0
    questions1={}
    questions2 = {}
    defaut_data = {}
    file_name = "example"
    current_questions1 = 0
    current_questions2 = 0
    def load_defualt(self):
        with open("config.json","r") as file:
            self.defaut_data = json.load(file)
            self.width = self.defaut_data["info"]["w"]
            self.height = self.defaut_data["info"]["h"]
            self.path = self.defaut_data["info"]["video_path"]
            self.fps = self.defaut_data["info"]["fps"]
            self.num_frames = self.defaut_data["info"]["num_frame"]
            self.length_minute = int(self.num_frames/(self.fps * 60))
            self.length_second = int((self.num_frames - self.length_minute * 60 * self.fps)/self.fps)
            self.class_name = self.defaut_data["info"]["class"]

    def add_questions1(self,question,answer):
        self.questions1[question] = answer

    def add_questions2(self,question,answer):
        self.questions2[question]  = answer
