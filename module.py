
class sohwan :

    def __init__(self,id,accountID,name):
        self.id = id
        self.accountID = accountID
        self.name = name

    def get_match_info(self,team,champId):
        self.team = team
        self.champId = champId
    def __str__(self):
        return self.name


