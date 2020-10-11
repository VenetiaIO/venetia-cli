
class adyen:

    @staticmethod
    def encrypt_0_1_16(data, key):
        options = {
            "enableValidations":False,
            "name":"adyen-encrypted-data",
            "fieldNameAttribute":"data-encrypted-name"
        }

