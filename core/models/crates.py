from core import db
from typing import List, Dict
class Crate(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    CrateName = db.Column(db.String())
    ReleaseDate = db.Column(db.String())
    URLTag = db.Column(db.String())


    def toDict(self):
        ret = {
            self.id : {
                "CrateName" : self.CrateName,
                "ReleaseDate" : self.ReleaseDate,
                "URLTag" : self.URLTag
            }
        }
        return ret
    
    
    def to_dict(self, includes: List[str]) -> Dict[str, str]:
        retItem = {}
        for inc in includes:
            retItem[inc] = vars(self)[inc]
        return retItem
    
    def __repr__(self):
        return f"{self.URLTag} | {self.CrateName} | {self.ReleaseDate}"
