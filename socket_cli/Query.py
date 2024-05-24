class Query:
    def __init__(self,client,quary_dict):
        self.client = client
        self.quary_dict=quary_dict

    def execute(self):
        self.client.send_command("query", self.quary_dict)
        response = eval(self.client.wait_response())
        if response["status"] == 'Fail':
            reason="name not found"
            print(reason)
            return {'status': "OK", 'reason': reason}
        else:
            reason=f"name {self.quary_dict['name']} exist"
            print(reason)
            return {'status': "Fail", 'reason': reason}