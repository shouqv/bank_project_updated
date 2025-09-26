import csv 
from .custome_exceptions import CustomerNotFoundError

class FileManagement():
    def __init__(self,file_name):
        self.file_name = file_name
        self.data_list = []
        self.fields = []
        if file_name != "": #to be able to instate it in the test class
            self.load_data()
        
    def is_number(self, string):
        # crediting https://www.geeksforgeeks.org/python/python-check-if-given-string-is-numeric-or-not/
        try:
            float(string)
            return True
        except ValueError:
            return False
        except TypeError:
            return False



    def load_data(self):
        # from https://www.geeksforgeeks.org/python/working-csv-files-python/
        with open(self.file_name, 'r' , newline="") as file:
            csv_reader = csv.DictReader(file)  

            for row in csv_reader:
                self.data_list.append(row)
                
            self.fields = csv_reader.fieldnames 
        

            self.convert_data_type()




    def write_to_file(self):
        # from https://www.geeksforgeeks.org/python/working-csv-files-python/
        with open(self.file_name, 'w', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(self.data_list)
        self.convert_data_type()



    def get_row(self,customer_id):
        
        for data in self.data_list:
            if data["account_id"] == customer_id:
                return data
        raise CustomerNotFoundError(f"The id {customer_id}, does not exist")

    def add_row(self , **kwargs):
        for key in kwargs:
            if key not in self.fields:
                raise ValueError(f"The field {key}, is not compatible with the file field!") 
        
        self.data_list.append(kwargs)
        self.write_to_file()

    def update_row(self,customer_id, field , new_value):
        not_updated = True
        for i in range(len(self.data_list)):
            if self.data_list[i]["account_id"] == customer_id:
                self.data_list[i][field] = new_value
                not_updated = False
        if not_updated:
            raise CustomerNotFoundError(f"The id {customer_id}, does not exist")
        self.write_to_file()
        
    def get_field_info(self,customer_id , field):
        data_row= self.get_row(customer_id)
        for key , value in data_row.items():
            if key == field:
                return value

    def get_last_row_id(self):
        if not self.data_list:
            raise ValueError("The file is empty!")
        return self.data_list[-1]["account_id"]

    def convert_data_type(self):
            for row in self.data_list:
                for key,value in row.items():
                    if key == "password":
                        continue
                    if key == "account_id" or key == "operation_id":
                        row[f"{key}"] = int(value)
                        continue
                    if self.is_number(value):
                        row[f"{key}"] = float(value)





