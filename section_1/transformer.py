import hashlib
import configs

class Transformer:
    def __init__(self, logger, successful_application):
        self.logger = logger
        self.successful_application = successful_application
    
    def get_first_name(self, full_name):
        # get first name from full name
        

        full_name = full_name.split(" ")
        if len(full_name) == 1:
            # if name only consists of one word
            first_name = full_name
        else :
            # first name are the subset of full name from first word up to second last word
            first_name = full_name[0: len(full_name)-1]
        return " ".join(first_name)
    
    def get_last_name(self, full_name):
        full_name = full_name.split(" ")
        return full_name[-1]
    
    def transform_birthday(self, birthday):
        birthday = birthday.strftime(configs.BIRTHDAY_FORMAT)
        return birthday
    
    def get_membership_id(self, application):
        last_name, birthday = application
        hashed_birthday = hashlib.sha256( birthday.encode(configs.MEMBERSHIP_ID_BIRTHDAY_ENCODING )) \
                            .hexdigest()
        hashed_birthday = hashed_birthday[: configs.MEMBERSHIP_ID_SHA_LENGTH]
        return f"{last_name}_{hashed_birthday}"
    
    def transform(self):
        try :
            self.logger.info("Transforming successful application : start")

            self.logger.info("Transforming first_name")
            self.successful_application['first_name'] = self.successful_application["full_name"] \
                                                        .apply(self.get_first_name)

            self.logger.info("Transforming last_name")
            self.successful_application['last_name'] = self.successful_application["full_name"] \
                                                        .apply(self.get_last_name)

            self.logger.info("Transforming birthday")
            self.successful_application["birthday"] = self.successful_application["birthday"] \
                                                        .apply(self.transform_birthday)

            self.logger.info("Transforming membership_id")
            self.successful_application["membership_id"] = self.successful_application[["last_name", "birthday"]] \
                                                                .apply(self.get_membership_id, axis=1)

            self.logger.info("Transforming above 18")
            self.successful_application["above_18"] = True
            
            columns = ["first_name", "last_name", "birthday", "above_18", "membership_id"]
            self.successful_application = self.successful_application[columns]
            self.logger.info("Transforming successful application : success")

            return self.successful_application
        
        except Exception as e:
            self.logger.error(f"Transforming successful application : fail\n{e}")
            raise Exception(e)