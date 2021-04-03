from background_interface.dao.keyInfoDao import KeyInfoDao
import time


class KeyInfoService:

    def __init__(self):
        pass

    def query_data_by_page(self, key_name, curr_page, page_size):
        return KeyInfoDao().query_data_by_page(key_name, int(curr_page), int(page_size))

    def remove_analyze_token(self, recordId, token):
        token = str(token).strip()
        origin_data = KeyInfoDao().get_doc_by_id(recordId)
        origin_analyze = self._parse_analyze_data(origin_data)
        if token not in origin_analyze:
            return False
        if token not in origin_analyze.split():
            return False
        new_analyze = []
        for origin_token in origin_analyze.split():
            if token != origin_token:
                new_analyze.append(origin_token)
        new_analyze = ' '.join(new_analyze)
        KeyInfoDao().update_analyze(recordId, new_analyze)
        return True

    def add_analyze_token(self, recordId, token):
        token = str(token).strip()
        origin_data = KeyInfoDao().get_doc_by_id(recordId)
        origin_analyze = self._parse_analyze_data(origin_data)
        print("origin analyze is {}".format(origin_analyze))
        if token in origin_analyze:
            return False
        if token in origin_analyze.split():
            return False
        new_analyze = origin_analyze.split() + [token]
        new_analyze = ' '.join(new_analyze)
        KeyInfoDao().update_analyze(recordId, new_analyze)
        return True

    def update_isStop(self, recordId, isStop):
        return KeyInfoDao().update_isStop( recordId, isStop)

    def _parse_analyze_data(self, data):
        if data["hits"]["total"] == 0:
            return ""
        try:
            return data['hits']['hits'][0]["_source"]["analyze"]
        except Exception as e:
            print(e)
            return ""


KS = KeyInfoService()


if __name__ == '__main__':
    print(KeyInfoService().query_data_by_page("苏州兆鑫驰智能科技有限公", 1, 10))
    print(KeyInfoService().update_isStop("fnUNPXcBpOF4N_9ZQYHg", "1"))
    print(KeyInfoService().add_analyze_token("fnUNPXcBpOF4N_9ZQYHg", "起飞"))
    print(KeyInfoService().add_analyze_token("fnUNPXcBpOF4N_9ZQYHg", "开炮"))
    print(KeyInfoService().remove_analyze_token("fnUNPXcBpOF4N_9ZQYHg", "起飞"))
    time.sleep(1)
    print(KeyInfoService().query_data_by_page("苏州兆鑫驰智能科技有限公", 1, 10))

