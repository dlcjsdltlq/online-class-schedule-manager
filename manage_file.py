from util import resource_path
import jsonschema
import json

schedule_schema_json = resource_path('resources/json/schedule_schema.json')

class ManageFile():
    def validateJson(self, file_name): #json 스키마와 대조
        schema = self.readJson(schedule_schema_json)
        user_schedule = self.readJson(file_name)
        try:
            jsonschema.validate(instance=user_schedule, schema=schema)
        except: return False
        else: return True
    
    def readJson(self, file_name): 
        with open(file_name, 'rt', encoding='utf-8') as schedule_file :
            return json.loads(schedule_file.read())

    def writeJson(self, file_name, dict_data):
        with open(file_name, 'wt', encoding='utf-8') as schedule_file :
            schedule_file.write(json.dumps(dict_data))

    def updateSchedule(self, file_name, schedule_data): #데이터 형식: ('mon', 2, '수학')
        schedule = self.readJson(file_name)
        schedule['schedule'][schedule_data[0]][schedule_data[1]] = schedule_data[2]
        self.writeJson(file_name, schedule)

    def updateMemo(self, file_name, memo_data): #데이터 형식: ('통사', '출석 체크는 카카오톡에서 15분 이내로 진행함')
        memo = self.readJson(file_name)
        memo['memo'][memo_data[0]] = memo_data[1]
        self.writeJson(file_name, memo)

    def updateTime(self, file_name, time_data): #데이터 형식: ('time', [[9, 0], ~])
        time_dic = self.readJson(file_name)
        time_dic['time'][time_data[0]] = time_data[1]
        self.writeJson(file_name, time_dic)

    def readSchedule(self, file_name):
        schedule = self.readJson(file_name)['schedule']
        return schedule

    def readMemo(self, file_name):
        memo = self.readJson(file_name)['memo']
        return memo

    def readTime(self, file_name):
        time_dic = self.readJson(file_name)['time']
        return time_dic
