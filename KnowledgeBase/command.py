"""import .json file into the database"""

mongoimport --db smart_home --collection state_1 --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/state_1.json
mongoimport --db smart_home --collection state_2 --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/state_2.json
mongoimport --db smart_home --collection operator --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/operators.json
mongoimport --db smart_home --collection state --drop --file ~/Documents/DIYSmartHome/KnowledgeBase/state.json




"""clear a collection"""
db.collection_name.remove({})

