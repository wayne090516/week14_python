class AddStu:
    def __init__(self,client,add_dict):
        self.client = client
        self.add_dict=add_dict

    def execute(self):
        self.client.send_command("add", self.add_dict)
        if eval(self.client.wait_response())["status"] == "OK":
            reason=f"Add {self.add_dict} success"
            print(reason)
            return {'status': "OK", 'reason': reason}
        else:
            reason=f"Add {self.add_dict} failed"
            print(reason)
            return {'status': "Fail", 'reason': reason}